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
Test cases for present weather phenomena, as specified in ICAO Annex 3
section 4.4.2.2.
"""
from . import BaseTest

class TestPrecipitation(BaseTest):

  def setUp(self):
    super().setUp()

    self.phenomena = ('RA',)
    self.intensity = ''

  def test_base_precipitation(self):
    self.metar_parts['weather'] = 'RA'

  def test_precipitation_heavy_thunderstorm_with_rain(self):
    self.phenomena = ('TSRA',)
    self.intensity = '+'

    self.metar_parts['weather'] = '+TSRA'

  def test_precipitation_heavy_drizzle(self):
    self.phenomena = ('DZ',)
    self.intensity = '+'

    self.metar_parts['weather'] = '+DZ'

  def test_precipitation_light_snow(self):
    self.phenomena = ('SN',)
    self.intensity = '-'

    self.metar_parts['weather'] = '-SN'

  def test_precipitation_heavy_thunderstorm_with_rain_and_snow(self):
    self.phenomena = ('TSRA', 'SN',)
    self.intensity = '+'

    self.metar_parts['weather'] = '+TSRASN'

  def tearDown(self):
    super().tearDown()

    self.assertEqual(self.phenomena, self.metar.report.sky.weather.precipitation.phenomena)
    self.assertEqual(self.intensity, self.metar.report.sky.weather.precipitation.intensity)

class TestObscuration(BaseTest):

  def setUp(self):
    super().setUp()

    self.phenomena = ('HZ',)

  def test_base_obscuration(self):
    self.metar_parts['weather'] = 'HZ'

  def test_obscuration_fog(self):
    self.phenomena = ('FG',)
    self.metar_parts['weather'] = 'FG'

  def test_obscuration_shallow_fog(self):
    self.phenomena = ('MIFG',)
    self.metar_parts['weather'] = 'MIFG'

  def tearDown(self):
    super().tearDown()

    self.assertEqual(self.phenomena, self.metar.report.sky.weather.obscuration)
  