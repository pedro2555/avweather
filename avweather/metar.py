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
import re
from collections import namedtuple

from avweather.parsers import search, occurs

def _recompile(pattern):
    return re.compile(pattern, re.I | re.X)

def _research(pattern, string):
    items = pattern.search(string.strip())

    if items is None:
        return (), string

    return items.groupdict(), string[items.end():]

RVR_RE = _recompile(r"""
    (
        R(?P<rwy>[\d]{2}(L|C|R)?)
        /(?P<rvrmod>P|M)?(?P<rvr>[\d]{4})
        (V(?P<varmod>P|M)?(?P<var>[\d]{4}))?
        (?P<tend>U|D|N)?
    )?
""")


def _newsearch(regex):
    def decorator(parse_func):

        @wraps(parse_func)    
        def parse_func_wrapper(tail):
            match = re.search(regex, tail.strip(), re.I | re.X)
            if match is None:
                return None, tail
            return parse_func(match.groupdict()), tail.strip()[match.end():]
        
        return parse_func_wrapper
    return decorator

@search(r"""
    (?P<type>METAR|SPECI|METAR\sCOR|SPECI\sCOR)
""")
def _parsetype(metartype):
    return metartype['type']

@search(r"""
    (?P<location>[A-Z][A-Z0-9]{3})
""")
def _parselocation(location):
    return location['location']

@search(r"""
    (?P<time>[0-9]{6})Z
""")
def _parsetime(time):
    MetarObsTime = namedtuple('MetarObsTime', 'day hour minute')
    time = time['time']
    day = int(time[:2])
    hour = int(time[2:4])
    minute = int(time[4:])

    return MetarObsTime(day, hour, minute)

@search(r"""
    (?P<reporttype>AUTO|NIL)?
""")
def _parsereporttype(reporttype):
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
def _parsewind(wind):
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


def _parsesky(string):

    @search('(?P<cavok>CAVOK)?')
    def parsecavok(item):
        return item['cavok']

    cavok, tail = parsecavok(string)

    if cavok is not None:
        return None, tail

    vis, tail = _parsevis(tail)
    rvr, tail = _parservr(tail)

    return (vis, rvr), tail

@search(r"""
    (?P<dist>[\d]{4})
    (?P<ndv>NDV)?
    (\s
        (?P<mindist>[\d]{4})\s
        (?P<mindistdir>N|NE|E|SE|S|SW|W|NW)
    )?
""")
def _parsevis(vis):
    Visibility = namedtuple('Visibility', 'distance ndv min_distance min_direction')
    return Visibility(
        int(vis['dist']),
        False if vis['ndv'] is None else True,
        None if vis['mindist'] is None else int(vis['mindist']),
        None if vis['mindist'] is None else vis['mindistdir'].upper(),
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
def _parservr(rvr):
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


@search('(?P<intensity>\+|-)?')
def _parseintensity(item):
    return item['intensity']

def _parsepercip(string):
    Percipitation = namedtuple('Percipitation', 'intensity phenomena')

    @occurs(10)
    @search(r"""(?P<phenomena>
        DZ|RA|SN|SG|PL|DS|SS|FZDZ|FZRA|FZUP|SHGR|SHGS|SGRA|SHSN|TSGR|TSGS|TSPL|
        TSRA|TSSN|UP
    )""")
    def parsephenomena(item):
        return item['phenomena']

    intensity, tail = _parseintensity(string)
    if intensity is None:
        intensity = ''
    phenomena, tail = parsephenomena(tail)

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
def _parseobscuration(obscuration):
    return obscuration['obscuration']

def _parseotherphenomena(string):
    OtherPhenomena = namedtuple('OtherPhenomena', 'intensity phenomena')
    
    @occurs(10)
    @search(r"""(?P<phenomena>
        FG|PO|FC|DS|SS|TS|SH|BLSN|BLSA|BLDU|VA
    )""")
    def parsephenomena(item):
        return item['phenomena']

    intensity, tail = _parseintensity(string)
    phenomena, tail = parsephenomena(tail)

    if len(phenomena) == 0:
        return None, tail

    return OtherPhenomena(intensity, phenomena), tail

def parse(string):
    """Parses a METAR or SPECI text report into python primitives.

    Implementation based on Annex 3 to the Convetion on Internation Civil
    Aviation, as published by ICAO, 16th Edition July 2007.
    """
    res = {}
    tail = None

    metartype, tail = _parsetype(string.strip().upper())
    res['metartype'] = metartype

    location, tail = _parselocation(tail)
    res['location'] = location

    time, tail = _parsetime(tail)
    res['time'] = time

    reporttype, tail = _parsereporttype(tail)
    res['reporttype'] = reporttype

    report = None
    if reporttype != 'NIL':
        report = {}

        wind, tail = _parsewind(tail)
        report['wind'] = wind

    res['report'] = report
    res['unmatched'] = tail if tail is not None else string

    return res
