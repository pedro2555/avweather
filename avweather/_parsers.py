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

def search(regex):
    """
    >>> @search('(?P<letter>[A-Z])?')
    ... def getletter(string):
    ...     return string['letter']
    ...
    >>> getletter('ABC')
    ('A', 'BC')
    >>> getletter('0BC')
    (None, '0BC')
    """
    def decorator(parse_func):

        def func_wrapper(tail):
            match = re.search(regex, tail.strip(), re.I | re.X)
            if match is None:
                return None, tail
            item = parse_func(match.groupdict())
            if item is not None:
                tail = tail.strip()[match.end():]
            return item, tail
        
        return func_wrapper
    return decorator

def occurs(times):
    """
    >>> @occurs(2)
    >>> @search('(?P<letter>[A-Z])?')
    ... def get2letters(string):
    ...     return string['letter']
    ...
    >>> get2letters('ABC')
    (('A', 'B'), 'C')
    >>> get2letters('0BC')
    ((), '0BC')
    
    """
    if type(times) != int or times < 1:
        raise ArgumentError('times must be a positive integer.')
    def decorator(search_func):
        
        def func_wrapper(tail):
            items = []
            item, tail = search_func(tail)
            while item is not None:
                items.append(item)
                if len(items) == times:
                    break
                item, tail = search_func(tail)
            return tuple(items), tail

        return func_wrapper
    return decorator

