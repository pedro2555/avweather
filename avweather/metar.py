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

PATTERN = (
    r"""(?P<metartype>
         METAR|METAR\sCOR|SPECI
    )""",
    r"""(?P<station>
        [A-Z][A-Z0-9]{3}
    )""",
    r"""(?P<time>
        [\d]{6}Z
    )""",
    r"""(?P<metreporttype>(AUTO|NIL)?)
        (?P<metreport>.*)""",
)
PATTERN = '^%s$' % r'\s'.join(PATTERN)
PATTERN = re.compile(PATTERN, re.I | re.X)

def match(report):
    """Maps a given METAR textual report into a python dictionary"""

    if not isinstance(report, str):
        raise TypeError('expected string but %s given.' % type(report))

    report = report.strip()
    mobj = PATTERN.search(report)

    if mobj is None:
        raise ValueError('%s is not a valid metar.' % report)

    mobj = mobj.groupdict()

    # validate MET REPORT and TYPE
    metreporttype = mobj['metreporttype']
    metreporttype = metreporttype if metreporttype != '' else None

    metreport = mobj['metreport']
    if metreporttype in ('AUTO', ''):
        metreport = metreport
    elif metreporttype == 'NIL':
        if metreport != '':
            raise ValueError('%s provides both NIL and MET REPORT, only one expected.')
        metreport = None

    return {
        'metartype': mobj['metartype'],
        'station': mobj['station'],
        'metreporttype': metreporttype if metreporttype != '' else None,
        'metreport': metreport,
    }
