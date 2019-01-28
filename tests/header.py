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
Test cases for the following elements, as specified in ICAO Annex 3 section 4.5:

  * identification of the type of report;
  * location indicator;
  * time of the observation;
  * identification of an automated or missing report, when applicable;
"""
from . import BaseTest

class TestHeaders(BaseTest):

  def setUp(self):
    super().setUp()

    self.metartype = 'METAR'
    self.location = 'YUDO'
    self.time = (22, 16, 30)
    self.reporttype = None

  def test_base_headers(self):
    self.metar_parts['headers'] = 'METAR YUDO 221630Z'

  def test_metarcor(self):
    self.metartype = 'METAR COR'
    self.metar_parts['headers'] = 'METAR COR YUDO 221630Z'

  def test_speci(self):
    self.metartype = 'SPECI'
    self.metar_parts['headers'] = 'SPECI YUDO 221630Z'

  def test_specicor(self):
    self.metartype = 'SPECI COR'
    self.metar_parts['headers'] = 'SPECI COR YUDO 221630Z'

  def test_automated_report(self):
    self.reporttype = 'AUTO'
    self.metar_parts['headers'] = 'METAR YUDO 221630Z AUTO'
    
  def test_nil_report(self):
    self.reporttype = 'NIL'
    self.metar_parts['headers'] = 'METAR YUDO 221630Z NIL'

  def tearDown(self):
    super().tearDown()

    self.assertEqual(self.metartype, self.metar.metartype)
    self.assertEqual(self.location, self.metar.location)

    day, hour, minute = self.time
    self.assertEqual(day, self.metar.time.day)
    self.assertEqual(hour, self.metar.time.hour)
    self.assertEqual(minute, self.metar.time.minute)

    self.assertEqual(self.reporttype, self.metar.reporttype)

    if self.reporttype == 'NIL':
      self.assertIsNone(self.metar.report)
    else:
      self.assertIsNotNone(self.metar.report)
