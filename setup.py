#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Aviation Weather

Copyright (C) 2018  Pedro Rodrigues <prodrigues1990@gmail.com>

This file is part of Aviation Weather.

Aviation Weather is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 2 of the License.

Aviation Weather is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Aviation Weather.  If not, see <http://www.gnu.org/licenses/>.
"""
from setuptools import setup

long_description = ''
with open('./README.rst', 'r') as readme:
    long_description = readme.read()

setup(
    name = 'avweather',
    packages = ['avweather',],
    version = '0.0.8',
    description = "Aviation Weather Tools",
    long_description = long_description,
    keywords = ['metar',],
    author = "Pedro Rodrigues",
    author_email = 'prodrigues1990@gmail.com',
    license = 'GPLv2',
    url = 'https://github.com/pedro2555/avweather',
    install_requires = [],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite = 'tests',
    tests_require = [],
)
