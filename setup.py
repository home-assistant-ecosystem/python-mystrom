"""Set up the Python API for myStrom devices."""
import os

import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

if sys.argv[-1] == 'publish':
    os.system('python3 setup.py sdist upload')
    sys.exit()

setup(
    name='python-mystrom',
    version='0.5.0',
    description='Python API for interacting with myStrom devices',
    long_description=long_description,
    url='https://github.com/fabaff/python-mystrom',
    author='Fabian Affolter',
    author_email='fabian@affolter-engineering.ch',
    license='MIT',
    install_requires=['requests', 'click'],
    packages=find_packages(),
    zip_safe=True,
    include_package_data=True,
    entry_points="""
    [console_scripts]
    mystrom=pymystrom.cli:main
""",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities',
    ],
)
