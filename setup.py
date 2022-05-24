from setuptools import find_packages
from setuptools import setup


version = "3.0.0a11"

short_description = (
    "Dexterity is a content type framework for CMF  applications, "
    "with particular emphasis on Plone. It can be viewed as an "
    "alternative to Archetypes that is more light-weight and modular."
)

long_description = "{}\n{}\n{}".format(
    open("README.rst").read(),
    open("RELEASE_NOTES.rst").read(),
    open("CHANGES.rst").read(),
)

setup(
    name="plone.app.dexterity",
    version=version,
    description=short_description,
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 6.0",
        "Framework :: Plone :: Core",
        "Framework :: Zope :: 5",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="plone ttw dexterity schema interface",
    author="Martin Aspeli, David Glick, et al",
    author_email="dexterity-development@googlegroups.com",
    url="http://plone.org/products/dexterity",
    license="GPL",
    packages=find_packages(),
    namespace_packages=["plone", "plone.app"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # Dexterity
        "plone.app.textfield",
        "plone.behavior>=1.0",
        "plone.dexterity>=2.2.2",
        "plone.formwidget.namedfile",
        "plone.namedfile>=1.0.0",
        "plone.rfc822",
        "plone.schemaeditor >1.3.3",
        # Plone/Zope core
        "lxml",
        "plone.app.content",
        "plone.app.layout",
        "plone.app.uuid",
        "plone.app.z3cform>=1.1.0",
        "plone.autoform>=1.1",
        "plone.contentrules",
        "plone.portlets",
        "plone.schema>=1.1.0",
        "plone.supermodel>=1.1",
        "plone.z3cform>=0.6.0",
        "Products.CMFCore",
        "Products.GenericSetup",
        "setuptools",
        "Zope",
        "zope.browserpage",
        "zope.interface",
        "zope.component",
        "zope.deprecation",
        "zope.schema",
        "zope.publisher",
        "z3c.form>=3.0.0",
    ],
    extras_require={
        "test": [
            "plone.app.robotframework",
            "plone.app.testing",
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
