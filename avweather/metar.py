#!/usr/bin/env python
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
from collections import namedtuple
from . import _metar_parsers as _p

def parse(string):
    """Parses a METAR or SPECI text report into python primitives.

    Implementation based on Annex 3 to the Convetion on International Civil
    Aviation, as published by ICAO, 16th Edition July 2007.
    """
    metartuple = namedtuple(
        'Metar',
        'metartype location time reporttype report unmatched')
    reporttuple = namedtuple(
        'Report',
        'wind sky temperature pressure supplementary remarks')

    metartype, string = _p.ptype(string.strip().upper())
    location, string = _p.plocation(string)
    time, string = _p.ptime(string)
    reporttype, string = _p.preporttype(string)

    report = None
    if reporttype != 'NIL':
        wind, string = _p.pwind(string)
        sky, string = _p.psky(string)
        temperature, string = _p.ptemperature(string)
        pressure, string = _p.ppressure(string)
        supplementary, string = _p.psupplementary(string)
        report = reporttuple(wind,
                             sky,
                             temperature,
                             pressure,
                             supplementary,
                             None)

    return metartuple(metartype, location, time, reporttype, report, string)
