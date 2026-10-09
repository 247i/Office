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

import os

class KeyAsDefaultDict(dict):
	def __missing__(self, key):
		return key

class FriendlyTranslationNamesModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(FriendlyTranslationNamesModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "friendlyTranslationNames"
		self.requires = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("friendlyTranslationNames.py",)

	@property
	def friendlyNames(self):
		"""Returns a dictionary that needs a language code as input and
		   returns a friendly translation name as output. There's not a
		   name for every code, so be sure to catch the KeyError.

		"""
		translator = self._modules.default("active", type="translator")
		files = os.listdir(self._mm.resourcePath("translations"))
		files = (f for f in files if f.endswith(".po"))
		codes = [f.split(".")[0] for f in files]
		codes.append("C") #English
		#if no nice name is known, just return the language code.
		languages = KeyAsDefaultDict()
		for code in codes:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations"),
				code
			)
			#TRANSLATORS: Please replace 'English' with the native name
			#TRANSLATORS: of the language you're translating to. So
			#TRANSLATORS: don't translate it literally!
			#TRANSLATORS: e.g. translate 'Ik spreek Nederlands' if
			#TRANSLATORS: you're translating to Dutch.
			languages[code] = _("I speak English")
		return languages

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()

		self.active = True

	def disable(self):
		self.active = False

		del self._modules

def init(moduleManager):
	return FriendlyTranslationNamesModule(moduleManager)
