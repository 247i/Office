#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2012-2013, Marten de Vries
#
#	This file is part of OpenTeacher.
#
#	OpenTeacher is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	OpenTeacher is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with OpenTeacher.  If not, see <http://www.gnu.org/licenses/>.

from etree import ElementTree
import os

class KGeographyMapLoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(KGeographyMapLoaderModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "load"

		self.priorities = {
			"default": 800,
		}
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("kgm.py",)

	def getFileTypeOf(self, path):
		if path.endswith(".kgm"):
			return "topo"

	def load(self, kgmPath):
		#Feed the xml parser
		with open(kgmPath) as f:
			root = ElementTree.parse(f).getroot()
		#load the map, in various later needed formats
		mapPath = os.path.join(os.path.dirname(kgmPath), root.findtext("mapFile"))
		mapImage = Image.open(mapPath).convert("RGB")
		mapImageData = mapImage.load()

		items = []
		for counter, division in enumerate(root.findall("division")):
			#iterate over all places ('divisions')
			if division.findtext("ignore") == "yes":
				#unimportant division: skip
				continue
			item = {
				"id": counter,
				"name": division.findtext("name") or u"",
			}

			#get the color the place has on the map
			r = int(division.findtext("color/red"))
			g = int(division.findtext("color/green"))
			b = int(division.findtext("color/blue"))
			color = (r, g, b)

			#get the average pixel with that color. This is done by
			#iterating over all pixels and using them to calculate an
			#average if the color matches.
			sumX = 0
			sumY = 0
			count = 0
			for x in range(mapImage.size[0]):
				for y in range(mapImage.size[1]):
					if mapImageData[x, y] == color:
						sumX += x
						sumY += y
						count += 1
			#save the averages as coordinate.
			item["x"] = sumX / count
			item["y"] = sumY / count

			items.append(item)

		return {
			"resources": {
				"mapPath": mapPath,
			},
			"list": {
				"items": items,
			},
		}

	def enable(self):
		global Image
		try:
			import Image
		except ImportError: # pragma: no cover
			#remain inactive. If someone doesn't have PIL installed,
			#the program can just function but just not import .kgm.
			return

		self._modules = set(self._mm.mods(type="modules")).pop()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.mimetype = "application/x-kgeographymap"
		self.loads = {"kgm": ["topo"]}

		self.active = True

	def _retranslate(self):
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		#TRANSLATORS: This is the name of an application. For more info
		#TRANSLATORS: about KGeography: http://edu.kde.org/applications/all/kgeography/
		self.name = _("KGeography")

	def disable(self):
		self.active = False

		global Image
		del Image
		del self._modules

		del self.name
		del self.mimetype
		del self.loads

def init(moduleManager):
	return KGeographyMapLoaderModule(moduleManager)
