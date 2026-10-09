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

import shutil

class PngSaverModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(PngSaverModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "save"
		self.priorities = {
			"default": 868,
		}
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("png.py",)

	def _retranslate(self):
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		#TRANSLATORS: This is the name of an image format. Please just
		#TRANSLATORS: use the English name of it, unless the format is
		#TRANSLATORS: known under another name in your language (or you
		#TRANSLATORS: have a very good reason yourself for translating
		#TRANSLATORS: it). For more information on PNG:
		#TRANSLATORS: http://en.wikipedia.org/wiki/Portable_Network_Graphics
		self.name = _("Portable Network Graphics")

	def enable(self):		
		self._modules = set(self._mm.mods(type="modules")).pop()
		self.saves = {"topo": ["png"]}

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
		del self.name
		del self.saves

	def save(self, type, lesson, path):
		shutil.copy(lesson.resources["mapScreenshot"], path)

		lesson.path = None

def init(moduleManager):
	return PngSaverModule(moduleManager)
