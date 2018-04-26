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
import unittest

from avweather.parsers import search, occurs

class TestAvweatherParsers(unittest.TestCase):
    def test_search_decorator(self):
        @search(r"""
            (?P<param>[A-Z]{3})
        """)
        def look3letters(string):
            return string['param']

        test, tail = look3letters('AAABBBCCC')

        self.assertEqual(test, 'AAA')
        self.assertEqual(tail, 'BBBCCC')

    def test_search_none(self):
        @search(r"""
            (?P<param>[A-Z]{3})
        """)
        def look3letters(string):
            return string['param']

        test, tail = look3letters('000111222')

        self.assertEqual(test, None)
        self.assertEqual(tail, '000111222')


    def test_occurringsearch_decorator(self):
        @occurs(2)
        @search(r"""
            (?P<param>[A-Z]{3})
        """)
        def look3letters(string):
            return string['param']

        test, tail = look3letters('AAABBBCCCDDD')

        self.assertEqual(test, ('AAA', 'BBB',))
        self.assertEqual(tail, 'CCCDDD')

    def test_occurringsearch_emptytuple(self):
        @occurs(1)
        @search(r"""
            (?P<param>[A-Z]{3})
        """)
        def look3letters(string):
            return string['param']

        test, tail = look3letters('000111222')

        self.assertEqual(test, ())
        self.assertEqual(tail, '000111222')
