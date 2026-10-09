#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2013, Marten de Vries
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

class BackpackLoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(BackpackLoaderModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "load"
		self.priorities = {
			"default": 756,
		}
		
		self.requires = (
			self._mm.mods(type="wordListStringParser"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("backpack.py",)

	@property
	def _parseList(self):
		return self._modules.default("active", type="wordListStringParser").parseList

	def _retranslate(self):
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		#TRANSLATORS: This is the name of a file type OpenTeacher can
		#TRANSLATORS: read. It's named after the program with the same
		#TRANSLATORS: name. The program does no longer exist.
		self.name = _("Backpack")

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.mimetype = "application/x-backpack"
		self.loads = {"backpack": ["words"]}

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self.name
		del self.loads
		del self.mimetype

	def getFileTypeOf(self, path):
		if path.endswith(".backpack"):
			return "words"

	def load(self, path):
		"""Loads .backpack (Backpack) files. Based on file format
		   inspection. (as exported by WRTS, so no very reliable, but
		   there's nothing that's better...)

		"""
		#mind the U. It's important... (Mac style line endings)
		with open(path, "rU") as f:
			data = f.read().decode("UTF-8")

		return self._parseList(data)

def init(moduleManager):
	return BackpackLoaderModule(moduleManager)
