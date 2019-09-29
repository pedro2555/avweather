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
Test cases for all wind indication elements, as specified in ICAO Annex 3 section 4.6.1:

  * mean direction;
  * mean speed;
  * significant direction variations;
  * significant speed variations;
"""
from . import BaseTest

class TestWind(BaseTest):

  def setUp(self):
    super().setUp()

    self.direction = 240
    self.speed = 8
    self.gust = None
    self.unit = 'KT'
    self.variable_from = None
    self.variable_to = None

  def test_base_wind(self):
    self.metar_parts['wind'] = '24008KT'

  def test_unit(self):
    self.speed = 15
    self.unit = 'KMH'
    self.metar_parts['wind'] = '24015KMH'

  def test_gust(self):
    self.direction = 120
    self.speed = 6
    self.gust = 18
    self.metar_parts['wind'] = '12006G18KT'

  def test_significant_variations(self):
    self.direction = 20
    self.speed = 10
    self.variable_from = 350
    self.variable_to = 70
    self.metar_parts['wind'] = '02010KT 350V070'

  def test_variable_direction(self):
    self.direction = 'VRB'
    self.speed = 2
    self.metar_parts['wind'] = 'VRB02KT'

  def tearDown(self):
    super().tearDown()

    self.assertEqual(self.direction, self.metar.report.wind.direction)
    self.assertEqual(self.speed, self.metar.report.wind.speed)
    self.assertEqual(self.gust, self.metar.report.wind.gust)
    self.assertEqual(self.unit, self.metar.report.wind.unit)
    self.assertEqual(self.variable_from, self.metar.report.wind.variable_from)
    self.assertEqual(self.variable_to, self.metar.report.wind.variable_to)
