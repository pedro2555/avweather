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

def _recompile(pattern):
    return re.compile(pattern, re.I | re.X)

def _research(pattern, string):
    items = pattern.search(string.strip())

    if items is None:
        return None

    return items.groupdict(), string[items.end():]

TYPE_RE = _recompile(r"""
    (?P<type>METAR|SPECI)
""")

LOCATION_RE = _recompile(r"""
    (?P<location>[A-Z][A-Z0-9]{3})
""")

TIME_RE = _recompile(r"""
    (?P<time>[0-9]{6})Z
""")

REPORTTYPE_RE = _recompile(r"""
    (?P<reporttype>AUTO|NIL)?
""")

WIND_RE = _recompile(r"""
    (?P<direction>[0-9]{2}0|VRB)
    P?(?P<speed>[0-9]{2,3})
    (GP?(?P<gust>[0-9]{2,3}))?
    (?P<unit>KT|KMH)
    (\s(
        (?P<vrbfrom>[0-9]{2}0)
        V(?P<vrbto>[0-9]{2}0)
    ))?
""")

VIS_RE = _recompile(r"""
    (?P<dist>[\d]{4})
    (?P<ndv>NDV)?
    (\s
        (?P<mindist>[\d]{4})\s
        (?P<mindistdir>N|NE|E|SE|S|SW|W|NW)
    )?
""")

RVR_RE = _recompile(r"""
    (
        R(?P<rwy>[\d]{2}(L|C|R)?)
        /(?P<rvrmod>P|M)?(?P<rvr>[\d]{4})
        (V(?P<varmod>P|M)?(?P<var>[\d]{4}))?
        (?P<tend>U|D|N)?
    )?
""")

SKY_RE = _recompile(r"""(?P<cavok>CAVOK)?""")

PERCIP_RE = _recompile(r"""
    (
        (?P<intensity>\+|-)?
        (?P<phenomena>
            DZ|RA|
            SN|SG|
            PL|DS|
            SS|UP|
            FZDZ|
            FZRA|
            FZUP|
            SHGR|
            SHGS|
            SGRA|
            SHSN|
            TSGR|
            TSGS|
            TSPL|
            TSRA|
            TSSN
        )
    )?
""")

def _parsetype(string):
    match = _research(TYPE_RE, string)
    if match is None:
        return None, string

    metartype, tail = match

    if 'type' in metartype:
        return metartype['type'], tail

    return None, tail

def _parselocation(string):
    match = _research(LOCATION_RE, string)
    if match is None:
        return None, string

    location, tail = match

    if 'location' in location:
        return location['location'], tail

    return None, tail

def _parsetime(string):
    match = _research(TIME_RE, string)
    if match is None:
        return None, string

    time, tail = match

    if 'time' in time:
        time = time['time']

        day = int(time[:2])
        hour = int(time[2:4])
        minute = int(time[4:])

        return (day, hour, minute), tail

    return None, tail

def _parsereporttype(string):
    match = _research(REPORTTYPE_RE, string)

    if match is None:
        return None, string

    reporttype, tail = match

    if 'reporttype' in reporttype:
        return reporttype['reporttype'], tail

    return None, tail

def _parsewind(string):
    match = _research(WIND_RE, string)

    if match is None:
        raise ValueError('Unable to find wind in METAR')

    wind, tail = match

    if wind['gust'] is not None:
        wind['gust'] = int(wind['gust'])

    if wind['vrbfrom'] is not None:
        wind['vrbfrom'] = int(wind['vrbfrom'])

    if wind['vrbto'] is not None:
        wind['vrbto'] = int(wind['vrbto'])

    return (
        int(wind['direction']),
        int(wind['speed']),
        wind['gust'],
        wind['unit'],
        wind['vrbfrom'],
        wind['vrbto']
    ), tail

def _parsesky(string):
    match = _research(SKY_RE, string)

    sky, tail = match

    if sky['cavok'] is not None:
        return None, tail

    vis, tail = _parsevis(tail)
    rvr, tail = _parservr(tail)

    return (vis, rvr), tail

def _parsevis(string):
    match = _research(VIS_RE, string)

    vis, tail = match

    return (
        int(vis['dist']),
        False if vis['ndv'] is None else True,
        None if vis['mindist'] is None else int(vis['mindist']),
        None if vis['mindist'] is None else vis['mindistdir'].upper(),
    ), tail

def _parservr(string):
    tail = string
    result = {}

    while True:
        match = _research(RVR_RE, tail)

        if match is None:
            break

        rvr, tail = match

        if rvr['rwy'] is None or rvr['rvr'] is None:
            break

        result[rvr['rwy']] = (
            int(rvr['rvr']),
            rvr['rvrmod'],
            int(rvr['var']) if rvr['var'] is not None else None,
            rvr['varmod'],
            rvr['tend'],
        )

    return result, tail

def _parsepercip(string):
    tail = string
    intensity = ''
    phenomena = []

    while True:
        match = _research(PERCIP_RE, tail)

        if match is None:
            break

        percipitation, tail = match

        if percipitation['phenomena'] is None:
            break

        if percipitation['intensity'] is not None:
            intensity = percipitation['intensity']
        
        phenomena.append(percipitation['phenomena'])

    if len(phenomena) == 0:
        return None, tail

    return (intensity, tuple(phenomena)), tail


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
