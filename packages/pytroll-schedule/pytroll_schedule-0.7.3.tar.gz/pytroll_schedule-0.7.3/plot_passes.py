#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2016 Martin Raspaud

# Author(s):

#   Martin Raspaud <martin.raspaud@smhi.se>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys
import xml.etree.ElementTree as ET
from datetime import datetime

import numpy as np

from mpop.utils import debug_on
from trollsched.satpass import Pass

debug_on()

sat_dict = {'npp': 'Suomi NPP',
            'noaa19': 'NOAA 19',
            'noaa18': 'NOAA 18',
            'noaa15': 'NOAA 15',
            }

if __name__ == '__main__':
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()
    for child in root:
        if child.tag == 'pass':
            print child.attrib
            overpass = Pass(sat_dict.get(child.attrib['satellite'], child.attrib['satellite']),
                            datetime.strptime(child.attrib['start-time'],
                                              '%Y-%m-%d-%H:%M:%S'),
                            datetime.strptime(child.attrib['end-time'],
                                              '%Y-%m-%d-%H:%M:%S'))
            overpass.save_fig(directory='/tmp')
