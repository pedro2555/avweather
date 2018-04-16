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
from ddt import ddt
from ddt import data

from avweather import metar

@ddt
class MetarClassTests(unittest.TestCase):

    @data(0, ('', ''))
    def test_match_typeerror(self, report):
        with self.assertRaises(TypeError):
            metar.match(report)

    @data(
        '',
        'METAR A000 010000Z NIL METREPORT',
    )
    def test_match_valueerror(self, report):
        with self.assertRaises(ValueError):
            metar.match(report)

    @data(
        'METAR A000 010000Z METREPORT',
        'METAR A000 010000Z AUTO METREPORT',
        'METAR A000 010000Z NIL',
    )
    def test_match(self, report):
        test = metar.match(report)

        # mandatory METAR items
        self.assertIn(test['metartype'], ('METAR', 'METAR COR', 'SPECI'))
        self.assertEqual(len(test['station']), 4)
        self.assertIn(test['metreporttype'], ('NIL', 'AUTO', None))
