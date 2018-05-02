
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
from string import ascii_uppercase
from string import digits
from random import choice

def parser_test(parser_func):
    def decorator(test_func):
        def wrapper(self, string, *args, **kwargs):
            random = ''.join(choice(ascii_uppercase + digits) for _ in range(9))
            test, tail = parser_func(' '.join((string, random)))
            self.assertEqual(tail, ' ' + random)
            self.assertNotEqual(string, tail)
            test_func(self, test, *args, **kwargs) # run the actual tests
        return wrapper
    return decorator

