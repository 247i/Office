#! /usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright 2008-2011, Milan Boers
#    Copyright 2013, Marten de Vries
#
#    This file is part of OpenTeacher.
#
#    OpenTeacher is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    OpenTeacher is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with OpenTeacher.  If not, see <http://www.gnu.org/licenses/>.

import json

class MapModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(MapModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager
		self.mapName = "United States of America"
		self.mapPath = self._mm.resourcePath("resources/map.gif")
		self.knownPlaces = self._getKnownPlaces()

		self.type = "map"
		self.priorities = {
			"default": 612,
		}

	def enable(self):
		self.active = True

	def disable(self):
		self.active = False
	
	def _getKnownPlaces(self):
		try:
			feedback = ""
			# Open the file
			file = open(self._mm.resourcePath("resources/places.json"))
			# Read the whole file
			for line in file:
				feedback += line
			return json.loads(feedback)
		except IOError:
			# No places file
			return ""

def init(moduleManager):
	return MapModule(moduleManager)
