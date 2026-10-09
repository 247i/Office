#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2012, Milan Boers
#	Copyright 2012, Marten de Vries
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

import zipfile
import contextlib

class OpenTeachingMediaLoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(OpenTeachingMediaLoaderModule, self).__init__(*args, **kwargs)
		
		self.type = "load"
		self.priorities = {
			"default": 216,
		}
		
		self._mm = moduleManager
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.requires = (
			self._mm.mods(type="otxxLoader"),
		)
		self.filesWithTranslations = ("otmd.py",)

	def _retranslate(self):
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		#TRANSLATORS: This is one of the file formats OpenTeacher
		#TRANSLATORS: can read.
		self.name = _("Open Teaching Media")

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._otxxLoader = self._modules.default("active", type="otxxLoader")

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.loads = {"otmd": ["media"]}
		self.mimetype = "application/x-openteachingmedia"

		self.active = True

	def disable(self):
		self.active = False

		del self.name
		del self.loads
		del self.mimetype

		del self._modules
		del self._otxxLoader

	def getFileTypeOf(self, path):
		if path.endswith(".otmd"):
			return "media"

	def load(self, path):
		resourceFilenames = {}
		with contextlib.closing(zipfile.ZipFile(path, "r")) as zipFile:
			names = zipFile.namelist()
		names.remove("list.json")
		for name in names:
			resourceFilenames[name] = name

		lesson = self._otxxLoader.load(path, resourceFilenames)

		# Replace filenames with their real (temporary) files
		for item in lesson["list"]["items"]:
			with contextlib.ignored(KeyError):
				#Remote-data items give a KeyError
				item["filename"] = lesson["resources"][item["filename"]]

		return lesson

def init(moduleManager):
	return OpenTeachingMediaLoaderModule(moduleManager)
