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

    @data(
        'R01/0250',
        'R01L/0250 R01R/0100',
        'R01/P0250',
    )
    def test_parservr(self, string):
        test, tail = metar._parservr(string)

        self.assertIsInstance(test, tuple)

        for rwy, rvr_data in test:
            self.assertIsInstance(rwy, str)
            self.assertIsInstance(rvr_data, tuple)

            # this should always succeed in returning the rwy number part
            self.assertIn(int(rwy[:2]), range(36))

            if len(rwy) == 3:
                self.assertIn(rwy[2], ('L', 'C', 'R'))

            rvr, rvrmod, var, varmod, tend = rvr_data

            self.assertIsInstance(rvr, int)
            self.assertIn(rvr, range(9999))

    @data(
        ('R01/0250', ('01', (250, None, None, None, None))),
        ('R01/P0250', ('01', (250, 'P', None, None, None))),
        ('R01/0250V0500', ('01', (250, None, 500, None, None))),
        ('R01/M0250VP0500U', ('01', (250, 'M', 500, 'P', 'U'))),
    )
    @unpack
    def test_parservr_value(self, string, expected):
        test, tail = metar._parservr(string)

        test = test[0]
        self.assertEqual(test, expected)

    @data(
        'RA',
    )
    def test_parsepercip(self, string):
        test, tail = metar._parsepercip(string)

        intensity, phenomena = test

        self.assertIn(intensity, ('+', '-', ''))
        self.assertIsInstance(phenomena, tuple)
        self.assertTrue(len(phenomena) > 0)

    @data(
        (
            '',
            None
        ),
        (
            'RA',
            ('', ('RA', ))
        ),
        (
            '-RA',
            ('-', ('RA', ))
        ),
        (
            '+RASN',
            ('+', ('RA', 'SN'))
        ),
    )
    @unpack
    def test_parsepercip_value(self, string, expected):
        test, tail = metar._parsepercip(string)

        self.assertEqual(test, expected)

    @data(
        ('', 0),
        ('ICFG', 2),
        ('BLDUFG', 2),
    )
    @unpack
    def test_parseobscuration(self, string, lenght):
        test, tail = metar._parseobscuration(string)

        self.assertIsInstance(test, tuple)
        self.assertTrue(len(test) == lenght)
    
    @data(
        ('', None),
        ('FG', 1),
        ('VCFG', 1),
        ('BLSA', 1),
    )
    @unpack
    def test_parseotherphenomena(self, string, lenght):
        test, tail = metar._parseotherphenomena(string)

        if lenght is None:
            self.assertEqual(test, None)
        else:
            self.assertIsInstance(test, tuple)
            self.assertTrue(len(test.phenomena) == lenght)
    
    @data(
        'OVC014',
        'FEW014 BKN025CB',
    )
    def test_parseclouds(self, string):
        test, _ = metar._parsecloudsvv(string)

        self.assertIsInstance(test, tuple)
        self.assertTrue(len(test) > 0)
        self.assertTrue(len(test) <= 4)
        for cloud in test:
            self.assertIn(cloud.amount, ('FEW', 'SCT', 'BKN', 'OVC'))
            if cloud.height > 0:
                self.assertIsInstance(cloud.height, int)
            self.assertIn(cloud.type, ('CB', 'TCU', '///', None))

    @data('VV010', 'VV001', 'VV///')
    def test_parseverticalvv(self, string):
        test, _ = metar._parsecloudsvv(string)

        self.assertIsInstance(test, int)
        self.assertTrue(test >= -1)

    @data('SKC', 'NSC', 'NCD')
    def test_parseskyclear(self, string):
        test, _ = metar._parsecloudsvv(string)

        self.assertIn(test, ('SKC', 'NSC', 'NCD'))
