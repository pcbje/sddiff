#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
  name='bufldiff',
  author='Petter Bjelland',
  version='0.1',
  author_email='petter.bjellans@hig.no',
  description='Visuzalizing data similarity',
  license='Apache version 2.0',
  scripts=[],
  zip_safe=False,
  package_data={},
  install_requires=[
    'pyx'
  ]
)