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
from collections import namedtuple
from avweather._parsers import search, occurs

@search(r"""
    (?P<type>METAR|SPECI|METAR\sCOR|SPECI\sCOR)
""")
def ptype(metartype):
    return metartype['type']

@search(r"""
    (?P<location>[A-Z][A-Z0-9]{3})
""")
def plocation(location):
    return location['location']

@search(r"""
    (?P<time>[0-9]{6})Z
""")
def ptime(time):
    MetarObsTime = namedtuple('MetarObsTime', 'day hour minute')
    time = time['time']
    day = int(time[:2])
    hour = int(time[2:4])
    minute = int(time[4:])

    return MetarObsTime(day, hour, minute)

@search(r"""
    (?P<reporttype>AUTO|NIL)?
""")
def preporttype(reporttype):
    return reporttype['reporttype']

@search(r"""
    (?P<direction>[0-9]{2}0|VRB)
    P?(?P<speed>[0-9]{2,3})
    (GP?(?P<gust>[0-9]{2,3}))?
    (?P<unit>KT|KMH)
    (\s(
        (?P<vrbfrom>[0-9]{2}0)
        V(?P<vrbto>[0-9]{2}0)
    ))?
""")
def pwind(wind):
    Wind = namedtuple('Wind', 'direction speed gust unit variable_from variable_to')
    if wind['gust'] is not None:
        wind['gust'] = int(wind['gust'])
    if wind['vrbfrom'] is not None:
        wind['vrbfrom'] = int(wind['vrbfrom'])
    if wind['vrbto'] is not None:
        wind['vrbto'] = int(wind['vrbto'])
    return Wind(
        int(wind['direction']),
        int(wind['speed']),
        wind['gust'],
        wind['unit'],
        wind['vrbfrom'],
        wind['vrbto'],
    )

@search(r"""
    (?P<distance>[\d]{4})
    (?P<ndv>NDV)?
    (\s
        (?P<min_distance>[\d]{4})\s
        (?P<min_direction>N|NE|E|SE|S|SW|W|NW)
    )?
""")
def pvis(item):
    Visibility = namedtuple('Visibility', 'distance ndv min_distance min_direction')
    
    ndv = item['ndv'] is not None
    min_distance = item['min_distance']
    if min_distance is not None:
        min_distance = int(min_distance)
    return Visibility(
        int(item['distance']),
        ndv,
        min_distance,
        item['min_direction'],
    )

@occurs(10)
@search(r"""
    (
        R(?P<rwy>[\d]{2}(L|C|R)?)
        /(?P<rvrmod>P|M)?(?P<rvr>[\d]{4})
        (V(?P<varmod>P|M)?(?P<var>[\d]{4}))?
        (?P<tend>U|D|N)?
    )?
""")
def prvr(rvr):
    Rvr = namedtuple('Rvr', 'distance modifier variation variation_modifier tendency')
    if None in (rvr['rwy'], rvr['rvr']):
        return None
    return rvr['rwy'], Rvr(
        int(rvr['rvr']),
        rvr['rvrmod'],
        int(rvr['var']) if rvr['var'] is not None else None,
        rvr['varmod'],
        rvr['tend'],
    )

@search(r'(?P<intensity>\+|-)?')
def pintensity(item):
    return item['intensity']

def ppercipitation(string):
    Percipitation = namedtuple('Percipitation', 'intensity phenomena')

    @occurs(10)
    @search(r"""(?P<phenomena>
        DZ|RA|SN|SG|PL|DS|SS|FZDZ|FZRA|FZUP|SHGR|SHGS|SGRA|SHSN|TSGR|TSGS|TSPL|
        TSRA|TSSN|UP
    )""")
    def pphenomena(item):
        return item['phenomena']

    intensity, tail = pintensity(string)
    if intensity is None:
        intensity = ''
    phenomena, tail = pphenomena(tail)

    if len(phenomena) == 0:
        return None, tail
    return Percipitation(intensity, phenomena), tail

@occurs(10)
@search(r"""
    (?P<obscuration>
        IC|FG|BR|SA|DU|HZ|FU|VA|SQ|PO|FC|TS|BCFG|BLDU|BLSA|BLSN|DRDU|DRSA|
        DRSN|FZFG|MIFG|PRFG
    )?
""")
def pobscuration(obscuration):
    return obscuration['obscuration']

def potherphenomena(string):
    OtherPhenomena = namedtuple('OtherPhenomena', 'intensity phenomena')
    
    @occurs(10)
    @search(r"""(?P<phenomena>
        FG|PO|FC|DS|SS|TS|SH|BLSN|BLSA|BLDU|VA
    )""")
    def pphenomena(item):
        return item['phenomena']

    intensity, tail = pintensity(string)
    phenomena, tail = pphenomena(tail)

    if len(phenomena) == 0:
        return None, tail

    return OtherPhenomena(intensity, phenomena), tail

def pcloudsverticalvis(string):
    @occurs(4)
    @search(r"""
        (?P<amount>FEW|SCT|BKN|OVC)
        (?P<height>[\d]{3}|///)
        (?P<type>CB|TCU|///)?
    """)
    def pclouds(item):
        Cloud = namedtuple('Cloud', 'amount height type')
        height = item['height']
        if height == '///':
            height = -1
        else:
            height = int(height)
        return Cloud(item['amount'], height, item['type'])
    clouds, tail = pclouds(string)
    if len(clouds) > 0:
        return clouds, tail

    @search(r"""
        VV(?P<verticalvis>[\d]{3}|///)
    """)
    def pverticalvis(item):
        verticalvis = item['verticalvis']
        if verticalvis == '///':
            return -1
        return int(verticalvis)
    verticalvis, tail = pverticalvis(string)
    if verticalvis is not None:
        return verticalvis, tail

    @search(r'(?P<skyclear>SKC|NSC|NCD)')
    def pskyclear(item):
        return item['skyclear']
    skyclear, tail = pskyclear(string)
    return skyclear, tail

def psky(string):
    SkyConditions = namedtuple('SkyConditions', 'visibility rvr weather clouds')

    @search(r'(?P<cavok>CAVOK)?')
    def pcavok(item):
        return item['cavok']

    cavok, string = pcavok(string)

    if cavok is not None:
        return None, string

    visibility, string = pvis(string)
    rvr, string = prvr(string)

    Weather = namedtuple('Weather', 'precipitation obscuration other')
    precipitation, string = ppercipitation(string)
    obscuration, string = pobscuration(string)
    other, string = potherphenomena(string)
    current_weather = Weather(precipitation, obscuration, other)

    clouds, string = pcloudsverticalvis(string)

    return SkyConditions(visibility, rvr, current_weather, clouds), string

@search(r"""
    (?P<air_signal>M)?
    (?P<air>[\d]{2})/
    (?P<dewpoint_signal>M)?
    (?P<dewpoint>[\d]{2})
""")
def ptemperature(item):
    Temperature = namedtuple('Temperature', 'air dewpoint')

    air = int(item['air'])
    if item['air_signal'] is not None:
        air = 0 - air
    dewpoint = int(item['dewpoint'])
    if item['dewpoint_signal'] is not None:
        dewpoint = 0 - dewpoint

    return Temperature(air, dewpoint)

@search(r'Q(?P<pressure>[\d]{4})')
def ppressure(item):
    return int(item['pressure'])
