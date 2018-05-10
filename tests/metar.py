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

from . import parser_test

@ddt
class MetarTests(unittest.TestCase):

    @data(
        'METAR A000 010000Z NIL',
        'METAR LPPT 010000Z AUTO 00001KT CAVOK 03/M04 Q1013',
        'METAR LPPT 270130Z 34012KT 9999 FEW011 12/10 Q1013',
    )
    def test_p(self, string):
        test = parse(string)

        if test.reporttype != 'NIL':
            self.assertEqual(test.report.pressure, 1013)
        else:
            self.assertIs(test.report, None)
        self.assertEqual(test.unmatched, '')

    @data(
        (
            'METAR LPPT 191800Z 35015KT FEW040TCU 11/06 Q1016',
            'Missing required field visibility in metar .*$',
        ),
    )
    @unpack
    def test_p_attributeerror_vis(self, string, errorexp):
        with self.assertRaisesRegexp(ValueError, errorexp):
            parse(string)

    @data(
        'METAR',
        'SPECI',
    )
    @parser_test(ptype)
    def test_ptype(self, test):
        self.assertIn(test, ('METAR', 'SPECI'))

    @data(
        'A000',
        'LPPT',
        'KEWR',
    )
    @parser_test(plocation)
    def test_plocation(self, test):
        self.assertIsInstance(test, str)
        self.assertEqual(len(test), 4)
        self.assertTrue(test[0].isalpha())
        for char in test[1:]:
            self.assertTrue(char.isalpha() or char.isdigit())

    @data(
        '010000Z',
        '300200Z',
    )
    @parser_test(ptime)
    def test_ptime(self, test):
        day, hour, minute = test
        self.assertIsInstance(day, int)
        self.assertIsInstance(hour, int)
        self.assertIsInstance(minute, int)

    @data(
        'AUTO',
        'NIL',
    )
    @parser_test(preporttype)
    def test_preporttype(self, test):
        self.assertIn(test, ('AUTO', 'NIL'))

    @data(
        ('NIL', 'NIL'),
        ('AUTO', 'AUTO'),
        ('', None),
    )
    @unpack
    @parser_test(preporttype)
    def test_preporttype_value(self, test, expected):
        self.assertEqual(test, expected)

    @data(
        '01010KT',
        '01010G20KT',
        '01010KT 000V020',
        '01010G20KT 000V020',
        'VRB03KT',
        'VRB03G17KT',
        '/////KT',
    )
    @parser_test(pwind)
    def test_pwind(self, test):
        direction, speed, gust, unit, vrbfrom, vrbto = test
        self.assertIn(direction, (*range(359), 'VRB', '///'))
        self.assertIn(speed, (*range(999), '//'))
        self.assertIn(gust, (*range(999), None))
        self.assertIn(unit, ('KT', 'KMH'))
        self.assertIn(vrbfrom, (*range(999), None))
        self.assertIn(vrbto, (*range(999), None))


    @data(('CAVOK', None),)
    @unpack
    @parser_test(psky)
    def test_psky(self, test, expected):
        self.assertEqual(test, expected)

    @data(
        '0350',
        '9999',
        '0350NDV',
        '0350 0200N',
        '9000 1000NE',
    )
    @parser_test(pvis)
    def test_pvis(self, test):
        dist, ndv, mindist, mindistdir = test

        if dist % 5 != 0:
            self.fail('Wrong approximation in visibility')

        self.assertIn(dist, range(10001))
        self.assertIsInstance(ndv, bool)
        self.assertIn(mindist, (*range(10001), None))
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
    @parser_test(prvr)
    def test_prvr(self, test):
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
    @parser_test(prvr)
    def test_prvr_value(self, test, expected):
        test = test[0]
        self.assertEqual(test, expected)

    @data('RA',)
    @parser_test(ppercipitation)
    def test_ppercipitation(self, test):
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
    @parser_test(ppercipitation)
    def test_ppercipitation_value(self, test, expected):
        self.assertEqual(test, expected)

    @data(
        ('', 0),
        ('ICFG', 2),
        ('BLDUFG', 2),
    )
    @unpack
    @parser_test(pobscuration)
    def test_pobscuration(self, test, lenght):
        self.assertIsInstance(test, tuple)
        self.assertTrue(len(test) == lenght)

    @data(
        ('', None),
        ('FG', 1),
        ('VCFG', 1),
        ('BLSA', 1),
    )
    @unpack
    @parser_test(potherphenomena)
    def test_potherphenomena(self, test, lenght):
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
    @parser_test(pcloudsverticalvis)
    def test_pclouds(self, test):
        self.assertIsInstance(test, tuple)
        self.assertTrue(len(test) > 0)
        self.assertTrue(len(test) <= 4)
        for cloud in test:
            self.assertIn(cloud.amount, ('FEW', 'SCT', 'BKN', 'OVC'))
            if cloud.height > 0:
                self.assertIsInstance(cloud.height, int)
            self.assertIn(cloud.type, ('CB', 'TCU', '///', None))

    @data('VV010', 'VV001', 'VV///')
    @parser_test(pcloudsverticalvis)
    def test_pverticalvv(self, test):
        self.assertIsInstance(test, int)
        self.assertTrue(test >= -1)

    @data('SKC', 'NSC', 'NCD')
    @parser_test(pcloudsverticalvis)
    def test_pskyclear(self, test):
        self.assertIn(test, ('SKC', 'NSC', 'NCD'))

    @data('RERA', 'RETS')
    @parser_test(precentweather)
    def test_precentweather(self, test):
        self.assertIsInstance(test, tuple)
        self.assertNotIn('RE', test)

    @data(
        ('WS ALL RWYS', 0),
        ('WS RWY03', 1),
        ('WS RWY26L RWY26R', 2),
    )
    @unpack
    @parser_test(pwindshear)
    def test_pwindshear(self, test, lenght):
        if lenght == 0:
            self.assertEqual(test, 'ALL')
        else:
            self.assertIsInstance(test, tuple)
            self.assertTrue(len(test) == lenght)

    @data(
        'W15/S2',
        'WM03/S2',
    )
    @parser_test(psea)
    def test_psea(self, test):
        temperature, state = test
        self.assertIsInstance(temperature, int)
        self.assertIn(temperature, range(-99, 99))
        self.assertIsInstance(state, int)
        self.assertIn(state, range(9))
