#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aviation Weather

Copyright (C) 2018 - 2019 Pedro Rodrigues <prodrigues1990@gmail.com>

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
Test cases for visibility elements, as specified in ICAO Annex 3 sections:

 * Prevailing or minimum distance: section 4.2.4.4 a) b)
 * Abbreviation NDV: section 4.2.4.5
 * Minimum distance: section 4.2.4.4 a)
 * Minimum distane direction: section 4.2.4.4 a)
"""
from . import BaseTest

class TestVisibility(BaseTest):

  def setUp(self):
    super().setUp()

    self.distance = 350
    self.ndv = False
    self.min_distance = None
    self.min_direction = None

  def test_base_visibility(self):
    self.metar_parts['visibility'] = '0350'

  def test_unidirectional_visibility(self):
    self.distance = 7000
    self.ndv = True
    self.metar_parts['visibility'] = '7000NDV'

  def test_minimum_visibility(self):
    self.distance = 2000
    self.min_distance = 1200
    self.min_direction = 'NW'
    self.metar_parts['visibility'] = '2000 1200NW'

  def tearDown(self):
    super().tearDown()

    self.assertEqual(self.distance, self.metar.report.sky.visibility.distance)
    self.assertEqual(self.ndv, self.metar.report.sky.visibility.ndv)
    self.assertEqual(self.min_distance, self.metar.report.sky.visibility.min_distance)
    self.assertEqual(self.min_direction, self.metar.report.sky.visibility.min_direction)
