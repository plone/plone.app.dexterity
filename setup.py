from setuptools import setup, find_packages
import os

version = '2.0dev'

setup(name='plone.app.dexterity',
      version=version,
      description="Dexterity is a content type framework for CMF applications, "
                  "with particular emphasis on Plone. It can be viewed as an "
                  "alternative to Archetypes that is more light-weight and modular.",
      long_description=open("README.rst").read() + "\n" +
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
          # Dexterity
          'collective.z3cform.datetimewidget >=1.1dev',
          'plone.app.textfield',
          'plone.behavior>=1.0b5',
          'plone.dexterity >= 1.0rc1',
          'plone.formwidget.namedfile',
          'plone.namedfile[scales] >=1.0b5dev-r36016',
          'plone.rfc822',
          'plone.schemaeditor >=1.0',
          # Plone/Zope core
          'plone.app.content',
          'plone.app.layout',
          'plone.app.uuid',
          'plone.app.z3cform>=0.5.0',
          'plone.autoform >=2.0dev',
          'plone.contentrules',
          'plone.portlets',
          'plone.supermodel>=2.0dev',
          'plone.z3cform>=0.6.0',
          'Products.CMFCore',
          'Products.CMFPlone>=4.0b1',
          'Products.GenericSetup',
          'setuptools',
          'Zope2',
          'zope.app.pagetemplate',
          'zope.interface',
          'zope.component',
          'zope.schema',
          'zope.publisher',
          'z3c.form',
      ],
      extras_require = {
          'test': [
              'plone.app.testing',
              'unittest2'
              ],
          'grok': [
              'five.grok',
              'plone.directives.dexterity',
              'plone.directives.form >=2.0dev',
              ],
          'relations': [
              'plone.app.relationfield',
              'plone.app.intid',
              'z3c.relationfield',
              ]
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
