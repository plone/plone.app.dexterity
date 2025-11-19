from pathlib import Path
from setuptools import setup


version = "5.0.0a1"

short_description = (
    "Dexterity is a content type framework for CMF  applications, "
    "with particular emphasis on Plone. It can be viewed as an "
    "alternative to Archetypes that is more light-weight and modular."
)

long_description = (
    f"{Path('README.rst').read_text()}\n"
    f"{Path('RELEASE_NOTES.rst').read_text()}\n"
    f"{Path('CHANGES.rst').read_text()}"
)

setup(
    name="plone.app.dexterity",
    version=version,
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/x-rst",
    # Get more strings from
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.2",
        "Framework :: Plone :: Core",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="plone ttw dexterity schema interface",
    author="Martin Aspeli, David Glick, et al",
    author_email="dexterity-development@googlegroups.com",
    url="http://plone.org/products/dexterity",
    license="GPL",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.10",
    install_requires=[
        # Dexterity
        "plone.app.textfield",
        "plone.behavior>=1.0",
        "plone.dexterity>=2.2.2",
        "plone.formwidget.namedfile",
        "plone.namedfile>=1.0.0",
        "plone.rfc822",
        "plone.schemaeditor>1.3.3",
        # Plone/Zope core
        "lxml",
        "plone.base",
        "plone.app.uuid",
        "plone.app.z3cform>=4.6.0",
        "plone.autoform>=1.1",
        "plone.contentrules",
        "plone.portlets",
        "plone.schema>=1.1.0",
        "plone.supermodel>=1.1",
        "plone.z3cform>=0.6.0",
        "Products.GenericSetup",
        "Zope",
        "zope.browserpage",
        "z3c.form>=3.0.0",
        "Products.statusmessages",
        "plone.app.vocabularies",
        "plone.indexer",
        "plone.locking",
        "plone.registry",
        "plone.uuid",
        "zope.cachedescriptors",
        "zope.dottedname",
        "zope.filerepresentation",
    ],
    extras_require={
        "test": [
            "plone.app.robotframework",
            "plone.app.testing",
            "plone.i18n",
            "plone.testing",
            "robotsuite",
            "plone.api",
        ],
        "grok": [
            "five.grok",
            "plone.directives.dexterity",
            "plone.directives.form>=1.1",
        ],
        "relations": [
            "plone.app.relationfield",
            "plone.app.intid",
            "z3c.relationfield",
        ],
    },
    entry_points="""
    [z3c.autoinclude.plugin]
    target = plone
    """,
)
