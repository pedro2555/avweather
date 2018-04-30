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

from avweather.metar import parse
from avweather._metar_parsers import *

@ddt
class MetarTests(unittest.TestCase):

    @data(
        'METAR A000 010000Z NIL',
        'METAR LPPT 010000Z AUTO 00001KT CAVOK 03/M04 Q1013',
        'METAR LPPT 270130Z 34012KT 9999 FEW011 12/10 Q1013',
    )
    def testp(self, string):
        test = parse(string)

        if test.reporttype != 'NIL':
            self.assertEqual(test.report.pressure, 1013)
        else:
            self.assertIs(test.report, None)
        self.assertEqual(test.unmatched, '')

    @data(
        '',
        'METAR A000',
        'SPECI A000',
        'METAR value'
    )
    def testptype(self, string):
        test, tail = ptype(string)

        if test is not None:
            self.assertIn(test, ('METAR', 'SPECI'))
            self.assertNotEqual(tail, string)
        else:
            self.assertEqual(string, tail)

    @data(
        'A000',
        'LPPT',
        'KEWR',
    )
    def testplocation(self, string):
        test, tail = plocation(string)

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
        '300200Z dsfacvx',
    )
    def testptime(self, string):
        test, tail = ptime(string)

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
    def testpreporttype(self, string):
        test, tail = preporttype(string)

        if test is not None:
            self.assertIn(test, ('AUTO', 'NIL'))
        else:
            self.assertEqual(string, tail)

    @data(
        (' NIL sfge', 'NIL'),
        ('AUTO asdf', 'AUTO'),
        ('sdf gre', None),
    )
    @unpack
    def testpreporttype_value(self, string, expected):
        test, _ = preporttype(string)
        self.assertEqual(test, expected)

    @data(
        '01010KT',
        '01010G20KT',
        '01010KT 000V020',
        '01010G20KT 000V020',
    )
    def testpwind(self, string):
        test, tail = pwind(string)

        direction, speed, gust, unit, vrbfrom, vrbto = test
        self.assertIn(direction, (*range(359), 'VRB'))
        self.assertIn(speed, range(999))
        self.assertIn(gust, (*range(999), None))
        self.assertIn(unit, ('KT', 'KMH'))
        self.assertIn(vrbfrom, (*range(999), None))
        self.assertIn(vrbto, (*range(999), None))

    @data(('CAVOK', None),)
    @unpack
    def testpsky(self, string, expected):
        test, tail = psky(string)

        self.assertEqual(test, expected)

    @data(
        '0350',
        '9999',
        '0350NDV',
        '0350 0200N',
        '9000 1000NE',
    )
    def testpvis(self, string):
        test, tail = pvis(string)

        dist, ndv, mindist, mindistdir = test

        self.assertIn(dist, range(10000))
        self.assertIsInstance(ndv, bool)
        self.assertIn(mindist, (*range(10000), None))
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
    def testprvr(self, string):
        test, tail = prvr(string)

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
    def testprvr_value(self, string, expected):
        test, tail = prvr(string)

        test = test[0]
        self.assertEqual(test, expected)

    @data('RA',)
    def testppercipitation(self, string):
        test, tail = ppercipitation(string)

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
        ),)
    @unpack
    def testppercipitation_value(self, string, expected):
        test, tail = ppercipitation(string)

        self.assertEqual(test, expected)

    @data(
        ('', 0),
        ('ICFG', 2),
        ('BLDUFG', 2),
    )
    @unpack
    def testpobscuration(self, string, lenght):
        test, tail = pobscuration(string)

        self.assertIsInstance(test, tuple)
        self.assertTrue(len(test) == lenght)

    @data(
        ('', None),
        ('FG', 1),
        ('VCFG', 1),
        ('BLSA', 1),
    )
    @unpack
    def testpotherphenomena(self, string, lenght):
        test, tail = potherphenomena(string)

        if lenght is None:
            self.assertEqual(test, None)
        else:
            self.assertIsInstance(test, tuple)
            self.assertTrue(len(test.phenomena) == lenght)

    @data(
        'OVC014',
        'FEW011',
        'FEW014 BKN025CB',
    )
    def testpclouds(self, string):
        test, _ = pcloudsverticalvis(string)

        self.assertIsInstance(test, tuple)
        self.assertTrue(len(test) > 0)
        self.assertTrue(len(test) <= 4)
        for cloud in test:
            self.assertIn(cloud.amount, ('FEW', 'SCT', 'BKN', 'OVC'))
            if cloud.height > 0:
                self.assertIsInstance(cloud.height, int)
            self.assertIn(cloud.type, ('CB', 'TCU', '///', None))

    @data('VV010', 'VV001', 'VV///')
    def testpverticalvv(self, string):
        test, _ = pcloudsverticalvis(string)

        self.assertIsInstance(test, int)
        self.assertTrue(test >= -1)

    @data('SKC', 'NSC', 'NCD')
    def testpskyclear(self, string):
        test, _ = pcloudsverticalvis(string)

        self.assertIn(test, ('SKC', 'NSC', 'NCD'))

    @data('FEW011')
    def testpskyconditions(self, string):
        test, _ = pcloudsverticalvis(string)
