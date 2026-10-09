#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2013, Marten de Vries
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

import contextlib

class LanguageCodeGuesserModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(LanguageCodeGuesserModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "languageCodeGuesser"
		self.requires = (
			self._mm.mods(type="translator"),
		)

	def guessLanguageCode(self, languageName):
		return tables.NAME_TO_CODE.get(languageName.lower())

	def getLanguageName(self, languageCode):
		return tables.CODE_TO_NAME.get(languageCode)

	def enable(self):
		global tables
		tables = self._mm.import_("tables")

		self._modules = next(iter(self._mm.mods(type="modules")))
		self._modules.default("active", type="translator").languageChanged.handle(self._retranslate)

		self._retranslate()

		self.active = True

	def _retranslate(self):
		self._lookupTable = {}

	def disable(self):
		self.active = False

		del self._lookupTable
		del self._modules

def init(moduleManager):
	return LanguageCodeGuesserModule(moduleManager)
