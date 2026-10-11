"""Proactive warmer for the process-global Dexterity schema/behavior caches.

Building a Dexterity type's schema (and its behavior schemata) is lazy and, on a
cold process, expensive (zope.interface construction + resolution order). This
module builds them up front via the canonical ``iterSchemataForType`` API, so the
first real render does not pay that cost.

See the design doc: 2026-06-15-dexterity-cache-warmer-design.
"""

from dataclasses import dataclass
from dataclasses import field
from plone.base.interfaces import IPloneSiteRoot
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import iterSchemataForType
from Products.CMFCore.utils import getToolByName
from zope.component import adapter
from zope.component.hooks import getSite
from zope.component.hooks import setSite
from zope.processlifetime import IDatabaseOpenedWithRoot

import logging
import os
import time

log = logging.getLogger("plone.app.dexterity.warmup")

DEXTERITY_WARMER_ENABLED = "DEXTERITY_WARMER_ENABLED"
DEXTERITY_WARMER_BUDGET_SECONDS = "DEXTERITY_WARMER_BUDGET_SECONDS"
DEFAULT_BUDGET = 30.0


@dataclass
class WarmReport:
    """Result of a warm pass."""

    warmed_types: list = field(default_factory=list)  # portal_type ids warmed OK
    schemata: int = 0  # total schemata built (main + behaviors)
    errors: list = field(default_factory=list)  # list of (portal_type, repr(exc))
    duration: float = 0.0  # seconds

    def merge(self, other):
        self.warmed_types.extend(other.warmed_types)
        self.schemata += other.schemata
        self.errors.extend(other.errors)
        self.duration += other.duration


def warm_site(site, deadline=None):
    """Build the schema + behavior schemata for every Dexterity FTI of ``site``.

    Isolated per FTI: a failure is recorded and warming continues. ``deadline`` is
    an optional ``time.monotonic()`` value after which the pass stops early.
    """
    report = WarmReport()
    start = time.monotonic()
    types_tool = getToolByName(site, "portal_types")
    for fti in types_tool.objectValues():
        if not IDexterityFTI.providedBy(fti):
            continue
        if deadline is not None and time.monotonic() > deadline:
            log.warning("warmup: time budget exceeded, stopping early")
            break
        portal_type = fti.getId()
        try:
            schemata = list(iterSchemataForType(portal_type))
            report.warmed_types.append(portal_type)
            report.schemata += len(schemata)
        except Exception as exc:  # noqa: BLE001 - best-effort, never propagate
            log.exception("warmup failed for type %s", portal_type)
            report.errors.append((portal_type, repr(exc)))
    report.duration = time.monotonic() - start
    return report


def warm_all(app, budget_seconds=DEFAULT_BUDGET):
    """Warm every Plone site found directly under the Zope app root.

    ``setSite`` is set around each site so CA/utility lookups resolve, and restored
    afterwards. A single ``budget_seconds`` deadline is shared across all sites.
    """
    report = WarmReport()
    deadline = time.monotonic() + budget_seconds if budget_seconds else None
    previous_site = getSite()
    try:
        for obj in app.objectValues():
            if not IPloneSiteRoot.providedBy(obj):
                continue
            setSite(obj)
            report.merge(warm_site(obj, deadline=deadline))
    finally:
        setSite(previous_site)
    return report


def _enabled():
    return os.environ.get(DEXTERITY_WARMER_ENABLED, "true").strip().lower() not in (
        "0",
        "false",
        "no",
        "off",
    )


def _budget():
    try:
        return float(os.environ.get(DEXTERITY_WARMER_BUDGET_SECONDS, DEFAULT_BUDGET))
    except (TypeError, ValueError):
        return DEFAULT_BUDGET


@adapter(IDatabaseOpenedWithRoot)
def warm_on_startup(event):
    """Synchronously warm all Plone sites at process startup.

    Best-effort: any failure is logged and swallowed so process startup always
    proceeds. Runs before the WSGI server starts serving, so a container's
    readiness probe only passes once warming is done.
    """
    if not _enabled():
        log.info("Dexterity cache warmer disabled via %s", DEXTERITY_WARMER_ENABLED)
        return
    connection = event.database.open()
    try:
        app = connection.root()["Application"]
        report = warm_all(app, budget_seconds=_budget())
        log.info(
            "Dexterity cache warmer: %d types, %d schemata, %d errors in %.2fs",
            len(report.warmed_types),
            report.schemata,
            len(report.errors),
            report.duration,
        )
        if report.errors:
            log.warning("Dexterity cache warmer errors: %r", report.errors)
    except Exception:  # noqa: BLE001 - never block startup
        log.exception("Dexterity cache warmer failed; continuing startup")
    finally:
        connection.close()
