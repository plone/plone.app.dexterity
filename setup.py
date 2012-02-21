from setuptools import setup, find_packages
import os

version = '1.2'

setup(name='plone.app.dexterity',
      version=version,
      description="Dexterity is a content type framework for CMF applications, "
                  "with particular emphasis on Plone. It can be viewed as an "
                  "alternative to Archetypes that is more light-weight and modular.",
      long_description=open("README.txt").read() + "\n" +
                       open("RELEASE_NOTES.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Development Status :: 5 - Production/Stable",
        ],
      keywords='plone ttw dexterity schema interface',
      author='Martin Aspeli, David Glick, et al',
      author_email='dexterity-development@googlegroups.com',
      url='http://plone.org/products/dexterity',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone','plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'collective.monkeypatcher',
          'collective.z3cform.datetimewidget >=1.1dev',
          'five.localsitemanager>=1.1',
          'plone.app.content',
          'plone.app.jquerytools >=1.0rc1',
          'plone.app.layout',
          'plone.app.relationfield >=1.1dev',
          'plone.app.textfield',
          'plone.app.z3cform>=0.5.0',
          'plone.autoform >=1.0b3dev-r34689',
          'plone.behavior>=1.0b5',
          'plone.contentrules',
          'plone.dexterity >= 1.1.2',
          'plone.directives.form>=1.0b7dev-r34690',
          'plone.directives.dexterity',
          'plone.formwidget.autocomplete >= 1.2.0',
          'plone.formwidget.contenttree',
          'plone.formwidget.namedfile',
          'plone.namedfile[scales] >=1.0b5dev-r36016',
          'plone.portlets',
          'plone.schemaeditor >=1.0',
          'plone.supermodel>=1.0b2',
          'plone.z3cform>=0.6.0',
          'Products.CMFCore',
          'setuptools',
          # Zope 2
          'zope.interface',
          'zope.component',
          'zope.schema',
          'zope.publisher',
          'z3c.form',
      ],
      extras_require = {
          'grok': [],
          'relations': [],
          'test': [],
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
