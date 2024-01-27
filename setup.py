"""Set up the Python API for myStrom devices."""
import os


from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, "README.rst"), encoding="utf-8") as readme:
    long_description = readme.read()

setup(
    name="python-mystrom",
    version="2.2.0",
    description="Asynchronous Python API client for interacting with myStrom devices",
    long_description=long_description,
    url="https://github.com/home-assistant-ecosystem/python-mystrom",
    author="Fabian Affolter",
    author_email="fabian@affolter-engineering.ch",
    license="MIT",
    install_requires=[
        "requests",
        "click",
        "aiohttp",
        "setuptools",
        "async_timeout",
    ],
    packages=find_packages(),
    python_requires=">=3.9",
    zip_safe=True,
    include_package_data=True,
    entry_points="""
    [console_scripts]
    mystrom=pymystrom.cli:main
""",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Utilities",
    ],
)
