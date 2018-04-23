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
from ddt import unpack

from avweather import metar

@ddt
class MetarTests(unittest.TestCase):

    @data(
        'METAR A000 010000Z NIL',
        'METAR LPPT 010000Z AUTO 00001KT CAVOK 03/M04 Q1013'
    )
    def test_parse(self, string):
        test = metar.parse(string)

        self.assertIn('metartype', test)
        self.assertIn('location', test)
        self.assertIn('time', test)
        self.assertIn('reporttype', test)

        self.assertIn('report', test)
        report = test['report']
        if test['reporttype'] == 'NIL':
            self.assertEqual(report, None)
        else:
            self.assertIsInstance(report, dict)
        self.assertIn('unmatched', test)

    @data(
        '',
        'METAR A000',
        'SPECI A000',
        'METAR value'
    )
    def test_parsetype(self, string):
        test, tail = metar._parsetype(string)

        if test is not None:
            self.assertIn(test, ('METAR', 'SPECI'))
            self.assertNotEqual(tail, string)
        else:
            self.assertEqual(string, tail)

    @data(
        'A000',
        'LPPT',
        'KEWR'
    )
    def test_parselocation(self, string):
        test, tail = metar._parselocation(string)

        if test is not None:
            self.assertIsInstance(test, str)
            self.assertEqual(len(test), 4)
            self.assertTrue(test[0].isalpha())
            for char in test[1:]:
                self.assertTrue(char.isalpha() or char.isdigit())
        else:
            self.assertEqual(string, tail)

    @data(
        '010000Z',
        '300200Z dsfacvx'
    )
    def test_parsetime(self, string):
        test, tail = metar._parsetime(string)

        if test is not None:
            day, hour, minute = test
            self.assertIsInstance(day, int)
            self.assertIsInstance(hour, int)
            self.assertIsInstance(minute, int)
        else:
            self.assertEqual(string, tail)

    @data(
        '',
        'afd',
        'AUTO afd',
        'NIL affvdf',
    )
    def test_parsereporttype(self, string):
        test, tail = metar._parsereporttype(string)

        if test is not None:
            self.assertIn(test, ('AUTO', 'NIL'))
        else:
            self.assertEqual(string, tail)

    @data(
        (' NIL sfge', 'NIL'),
        ('AUTO asdf', 'AUTO'),
        ('sdf gre', None)
    )
    @unpack
    def test_parsereporttype_value(self, string, expected):
        test, _ = metar._parsereporttype(string)
        self.assertEqual(test, expected)

    @data(
        '01010KT',
        '01010G20KT',
        '01010KT 000V020',
        '01010G20KT 000V020',
    )
    def test_parsewind(self, string):
        test, tail = metar._parsewind(string)

        direction, speed, gust, unit, vrbfrom, vrbto = test
        self.assertIn(direction, (*range(359), 'VRB'))
        self.assertIn(speed, range(999))
        self.assertIn(gust, (*range(999), None))
        self.assertIn(unit, ('KT', 'KMH'))
        self.assertIn(vrbfrom, (*range(999), None))
        self.assertIn(vrbto, (*range(999), None))

    @data(
        ('CAVOK', None),
    )
    @unpack
    def test_parsesky(self, string, expected):
        test, tail = metar._parsesky(string)

        self.assertEqual(test, expected)

    @data(
        '0350',
        '0350NDV',
        '0350 0200N',
        '9000 1000NE',
    )
    def test_parsevis(self, string):
        test, tail = metar._parsevis(string)

        dist, ndv, mindist, mindistdir = test

        self.assertIn(dist, range(9999))
        self.assertIsInstance(ndv, bool)
        self.assertIn(mindist, (*range(9999), None))
        if mindist is None:
            self.assertEqual(mindistdir, None)
        else:
            self.assertIn(
                mindistdir,
                ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'))

