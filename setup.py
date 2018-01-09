"""
Copyright (c) 2015-2018 Fabian Affolter <fabian@affolter-engineering.ch>

Licensed under MIT. All rights reserved.
"""
import sys

from setuptools import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist upload')
    sys.exit()

setup(
    name='python-mystrom',
    version='0.4.0',
    description='Python API for interacting with myStrom devices',
    url='https://github.com/fabaff/python-mystrom',
    author='Fabian Affolter',
    author_email='fabian@affolter-engineering.ch',
    license='MIT',
    install_requires=['requests>=2.0', 'click'],
    packages=find_packages(),
    zip_safe=True,
    include_package_data=True,
    entry_points="""
    [console_scripts]
    mystrom=cli:main
""",
)
