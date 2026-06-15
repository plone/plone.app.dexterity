"""Proactive warmer for the process-global Dexterity schema/behavior caches.

Building a Dexterity type's schema (and its behavior schemata) is lazy and, on a
cold process, expensive (zope.interface construction + resolution order). This
module builds them up front via the canonical ``iterSchemataForType`` API, so the
first real render does not pay that cost.

See the design doc: 2026-06-15-dexterity-cache-warmer-design.
"""

import logging
import os
import time
from dataclasses import dataclass, field

from zope.component import adapter
from zope.component.hooks import getSite, setSite
from zope.processlifetime import IDatabaseOpenedWithRoot

from Products.CMFCore.utils import getToolByName
from plone.base.interfaces import IPloneSiteRoot
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import iterSchemataForType

log = logging.getLogger("plone.app.dexterity.warmup")

ENABLED_ENV = "DEXTERITY_WARMER_ENABLED"
BUDGET_ENV = "DEXTERITY_WARMER_BUDGET_SECONDS"
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
