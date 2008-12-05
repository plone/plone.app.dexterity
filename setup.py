from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='plone.app.dexterity',
      version=version,
      description="Experimental through-the-web Zope 3 schema editor",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone ttw dexterity schema interface',
      author='David Glick',
      author_email='davidglick@onenw.org',
      url='http://svn.plone.org/svn/plone/plone.app.dexterity',
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
          'plone.z3cform',
          'plone.supermodel',
          'plone.dexterity',
          'plone.directives.dexterity',
          'plone.schemaeditor',
          'Products.CMFCore',
          'collective.z3cform.datepicker',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
