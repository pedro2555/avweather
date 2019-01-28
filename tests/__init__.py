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
from collections import OrderedDict

from avweather import metar

class BaseTest(unittest.TestCase):
  def setUp(self):
    self.metar_parts = OrderedDict()
    self.metar_parts['headers'] = 'METAR YUDO 221630Z'
    self.metar_parts['wind'] = '24008KT'
    self.metar_parts['visibility'] = '0350'
    self.metar_parts['rvr'] = 'R32/0400'
    self.metar_parts['weather'] = 'RA'
    self.metar_parts['cloud'] = 'FEW015'
    self.metar_parts['air'] = '17/10 Q0995'
    self.metar_parts['supplementary'] = 'REFZRA'
    self.metar_parts['trend'] = 'NOSIG'

  def tearDown(self):
    self.metar = metar.parse(' '.join([
      part for part in self.metar_parts.values()
      if part is not None
    ]))