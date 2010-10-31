# -*- coding: utf-8 -*-
"""
This module contains the tool of collective.recipe.hudsonjob
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.1'

long_description = (
    read('README.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('collective', 'recipe', 'hudsonjob', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
   'Download\n'
    '********\n')

entry_points = {
    "zc.buildout": ["default = collective.recipe.hudsonjob:Recipe"],
}

tests_require = ['zope.testing', 'zc.buildout']

setup(name='collective.recipe.hudsonjob',
      version=version,
      description="Hudson configuration for Plone in buildout",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: Zope Public License',
        ],
      keywords='hudson, plone',
      author='',
      author_email='',
      url='',
      license='ZPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zc.buildout',
          'genshi>=0.6',
          'zc.recipe.egg',
          'collective.recipe.template',
          'mocker',
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='collective.plone.hudsonjob.tests.test_suite',
      entry_points=entry_points,
 )
