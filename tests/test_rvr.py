#!/usr/bin/env python3
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
"""
Test cases for runway visual range elements, as specified in ICAO Annex 3:

 * Section 4.3.6
 * Table A3-2.
"""
from . import BaseTest

class TestRunwayVisualRange(BaseTest):

  def setUp(self):
    super().setUp()

    self.expected = {
      '32': {
        'distance': 400,
        'modifier': None,
        'variation': None,
        'variation_modifier': None,
        'tendency': None
      }
    }

  def test_base_rvr(self):
    self.metar_parts['rvr'] = 'R32/0400'

  def test_rvr_modifier_m(self):
    self.expected = {
      '10': {
        'distance': 50,
        'modifier': 'M',
        'variation': None,
        'variation_modifier': None,
        'tendency': None
      }
    }

    self.metar_parts['rvr'] = 'R10/M0050'

  def test_rvr_modifier_p(self):
    self.expected = {
      '14L': {
        'distance': 2000,
        'modifier': 'P',
        'variation': None,
        'variation_modifier': None,
        'tendency': None
      }
    }

    self.metar_parts['rvr'] = 'R14L/P2000'

  def test_rvr_mulitple_runways(self):
    self.expected = {
      '16L': {
        'distance': 650,
        'modifier': None,
        'variation': None,
        'variation_modifier': None,
        'tendency': None
      },
      '16C': {
        'distance': 500,
        'modifier': None,
        'variation': None,
        'variation_modifier': None,
        'tendency': None
      }
    }

    self.metar_parts['rvr'] = 'R16L/0650 R16C/0500'

  def test_rvr_variation(self):
    self.expected = {
      '20': {
        'distance': 700,
        'modifier': None,
        'variation': 1200,
        'variation_modifier': None,
        'tendency': None
      }
    }

    self.metar_parts['rvr'] = 'R20/0700V1200'

  def test_rvr_variation_modifier(self):
    self.expected = {
      '19': {
        'distance': 350,
        'modifier': None,
        'variation': 1200,
        'variation_modifier': 'P',
        'tendency': None
      }
    }

    self.metar_parts['rvr'] = 'R19/0350VP1200'

  def test_rvr_tendency(self):
    self.expected = {
      '12': {
        'distance': 1100,
        'modifier': None,
        'variation': None,
        'variation_modifier': None,
        'tendency': 'U'
      }
    }

    self.metar_parts['rvr'] = 'R12/1100U'

  def test_rvr_tendency_multiple_runways(self):
    self.expected = {
      '26': {
        'distance': 550,
        'modifier': None,
        'variation': None,
        'variation_modifier': None,
        'tendency': 'N'
      },
      '20': {
        'distance': 800,
        'modifier': None,
        'variation': None,
        'variation_modifier': None,
        'tendency': 'D'
      }
    }

    self.metar_parts['rvr'] = 'R26/0550N R20/0800D'

  def test_rvr_variation_and_tendency(self):
    self.expected = {
      '09': {
        'distance': 375,
        'modifier': None,
        'variation': 600,
        'variation_modifier': None,
        'tendency': 'U'
      }
    }

    self.metar_parts['rvr'] = 'R09/0375V0600U'

  def test_rvr_modifier_variation_and_tendency(self):
    self.expected = {
      '10': {
        'distance': 150,
        'modifier': 'M',
        'variation': 500,
        'variation_modifier': None,
        'tendency': 'D'
      }
    }

    self.metar_parts['rvr'] = 'R10/M0150V0500D'

  def tearDown(self):
    super().tearDown()

    self.assertEqual(len(self.expected), len(self.metar.report.sky.rvr))

    for runway, rvr in self.metar.report.sky.rvr:
        self.assertIn(runway, self.expected)
        expected = self.expected[runway]
        
        self.assertEqual(expected['distance'], rvr.distance)
        self.assertEqual(expected['modifier'], rvr.modifier)
        self.assertEqual(expected['variation'], rvr.variation)
        self.assertEqual(expected['variation_modifier'], rvr.variation_modifier)
        self.assertEqual(expected['tendency'], rvr.tendency)
