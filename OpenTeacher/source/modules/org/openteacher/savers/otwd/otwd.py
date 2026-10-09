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

class OpenTeachingWordsSaverModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(OpenTeachingWordsSaverModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "save"
		self.priorities = {
			"default": 280,
		}
		
		self.requires = (
			self._mm.mods(type="otxxSaver"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("otwd.py",)

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
		self.name = _("Open Teaching Words")

	def enable(self):		
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._otxxSaver = self._modules.default("active", type="otxxSaver")

		self.saves = {"words": ["otwd"]}

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

	def save(self, type, lesson, path):
		self._otxxSaver.save(lesson, path)

	def disable(self):
		self.active = False

		del self._modules
		del self._otxxSaver
		del self.name
		del self.saves

def init(moduleManager):
	return OpenTeachingWordsSaverModule(moduleManager)
