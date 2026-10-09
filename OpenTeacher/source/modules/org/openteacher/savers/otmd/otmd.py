#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011, Milan Boers
#	Copyright 2011-2012, Marten de Vries
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
import copy
import os

class Lesson(object):
	pass

class OpenTeachingMediaSaverModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(OpenTeachingMediaSaverModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "save"
		self.priorities = {
			"default": 112,
		}

		self.requires = (
			self._mm.mods(type="otxxSaver"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
			self._mm.mods(type="settings"),
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
		#TRANSLATORS: saves to.
		self.name = _("Open Teaching Media")
		self._compressionSetting.update({
			#TRANSLATORS: name of a setting
			"name": _("Enable compression"),
			#TRANSLATORS: setting category.
			"category": _("Input and output"),
			#TRANSLATORS: setting subcategory; .otmd is a file extension.
			"subcategory": _(".otmd saving"),
		})

	def enable(self):		
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._otxxSaver = self._modules.default("active", type="otxxSaver")

		self.saves = {"media": ["otmd"]}

		try:
			self._settings = self._modules.default(type="settings")
		except IndexError, e:
			self._compressionSetting = dict()
			self._compressionSetting["value"] = True
		else:
			self._compressionSetting = self._settings.registerSetting(**{
				"internal_name": "org.openteacher.savers.otmd.compression",
				"type": "boolean",
				"defaultValue": True,
				"advanced": True,
			})

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self._otxxSaver
		del self._settings
		del self._compressionSetting
		del self.name
		del self.saves

	def save(self, type, lesson, path):
		compression = zipfile.ZIP_STORED
		if self._compressionSetting["value"]:
			compression = zipfile.ZIP_DEFLATED

		#prepare lesson structure for saving
		lesson_clone = Lesson()
		lesson_clone.list = copy.deepcopy(lesson.list)
		lesson_clone.resources = {}
		for item in lesson_clone.list["items"]:
			if not item["remote"]:
				zipName = os.path.join("resources", os.path.basename(item["filename"]))
				lesson_clone.resources[zipName] = item["filename"]
				item["filename"] = zipName

		resourceFilenames = {}
		for resourceName in lesson_clone.resources:
			resourceFilenames[resourceName] = resourceName

		self._otxxSaver.save(lesson_clone, path, resourceFilenames, compression)
		lesson.changed = False
		lesson.path = path

def init(moduleManager):
	return OpenTeachingMediaSaverModule(moduleManager)
