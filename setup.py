from setuptools import setup, find_packages
import os

version = '1.0a3'

setup(name='plone.app.dexterity',
      version=version,
      description="Integrates the Dexterity content type system into Plone",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
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
          'setuptools',
          # Zope 2
          'zope.interface',
          'zope.component',
          'zope.schema',
          'zope.publisher',
          'z3c.form',
          'plone.z3cform>=0.5.4',
           # ^^ strictly speaking either this dev version OR z3c.form trunk
           # is required, for the textlines widget
          'plone.app.z3cform>=0.4.5',
          # ^ 0.4.5 required for the default datetime widget
          'plone.supermodel',
          'plone.dexterity',
          'plone.behavior>=1.0b4',
          'plone.directives.form',
          'plone.directives.dexterity',
          'plone.schemaeditor',
          'Products.CMFCore',
          'plone.formwidget.autocomplete',
          'plone.formwidget.contenttree',
          'plone.app.content',
          'plone.app.relationfield',
          'plone.portlets',
          'plone.contentrules',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
