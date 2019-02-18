#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Python pluggable.worker
"""

from setuptools import setup

from Cython.Build import cythonize


install_requires = [
    "pluggable.core",
    "python-rapidjson",
    "umsgpack"]
extras_require = {}
extras_require['test'] = [
    "coverage",
    "codecov",
    "cython",
    "flake8",
    "pytest",
    "pytest-asyncio",
    "pytest-coverage",
    "pytest-mock"],

setup(
    name='pluggable.worker',
    version='0.1.0',
    description='pluggable.worker',
    long_description="pluggable.worker",
    url='https://github.com/phlax/pluggable.worker',
    author='Ryan Northey',
    author_email='ryan@synca.io',
    license='GPL3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        ('License :: OSI Approved :: '
         'GNU General Public License v3 or later (GPLv3+)'),
        'Programming Language :: Python :: 3.5',
    ],
    keywords='python pluggable',
    install_requires=install_requires,
    extras_require=extras_require,
    packages=['pluggable.worker'],
    namespace_packages=['pluggable'],
    ext_modules=cythonize("pluggable/worker/*.pyx", annotate=True),
    include_package_data=True)
