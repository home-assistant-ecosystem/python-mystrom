"""
Copyright (c) 2015-2016 Fabian Affolter <fabian@affolter-engineering.ch>

Licensed under MIT. All rights reserved.
"""
from setuptools import setup

setup(name='python-mystrom',
      version='0.3.4',
      description='Python API for controlling myStrom switches',
      url='https://github.com/fabaff/python-mystrom',
      author='Fabian Affolter',
      author_email='fabian@affolter-engineering.ch',
      license='MIT',
      install_requires=['requests>=2.0'],
      packages=['pymystrom'],
      zip_safe=True,
      include_package_data=True,
      )
