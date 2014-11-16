from setuptools import setup, find_packages
import os

version = '2.1.3.dev0'
long_description = open("README.rst").read() + "\n" + \
    open("RELEASE_NOTES.txt").read() + "\n" + \
    open(os.path.join("docs", "HISTORY.txt")).read()

setup(name='plone.app.dexterity',
      version=version,
      description="Dexterity is a content type framework for CMF "
                  "applications, with particular emphasis on Plone. It can "
                  "be viewed as an alternative to Archetypes that is more "
                  "light-weight and modular.",
      long_description=long_description,
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 5.0",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Development Status :: 5 - Production/Stable",
      ],
      keywords='plone ttw dexterity schema interface',
      author='Martin Aspeli, David Glick, et al',
      author_email='dexterity-development@googlegroups.com',
      url='http://plone.org/products/dexterity',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # Dexterity
          'plone.app.textfield',
          'plone.behavior>=1.0b5',
          'plone.dexterity >= 2.2.2dev',
          'plone.formwidget.namedfile',
          'plone.namedfile[scales] >=1.0b5dev-r36016',
          'plone.rfc822',
          'plone.schemaeditor >1.3.3',
          # Plone/Zope core
          'lxml',
          'plone.app.content',
          'plone.app.layout',
          'plone.app.uuid',
          'plone.app.z3cform>=0.7.2',
          'plone.autoform >=1.1dev',
          'plone.contentrules',
          'plone.portlets',
          'plone.supermodel>=1.1dev',
          'plone.z3cform>=0.6.0',
          'Products.CMFCore',
          'Products.CMFPlone>=4.0b1',
          'Products.GenericSetup',
          'setuptools',
          'Zope2',
          'zope.browserpage',
          'zope.interface',
          'zope.component',
          'zope.schema',
          'zope.publisher',
          'z3c.form>=3.0.0a1',
      ],
      extras_require={
          'test': [
              'plone.app.robotframework',
              'plone.app.testing',
              'unittest2'
          ],
          'grok': [
              'five.grok',
              'plone.directives.dexterity',
              'plone.directives.form >=1.1dev',
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
