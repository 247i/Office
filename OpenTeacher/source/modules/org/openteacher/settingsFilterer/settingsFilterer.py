#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2012, Marten de Vries
#	Copyright 2011, Milan Boers
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

class SettingsFiltererModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(SettingsFiltererModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "settingsFilterer"
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("settingsFilterer.py",)

	def byKey(self, key, items):
		catItems = dict()
		for item in items:
			if not key in item:
				if _("Miscellaneous") not in catItems:
					catItems[_("Miscellaneous")] = []
				catItems[_("Miscellaneous")].append(item)
			else:
				if item[key] not in catItems:
					catItems[item[key]] = []
				catItems[item[key]].append(item)
		return catItems

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

	def _retranslate(self):
		#install _ and ngettext
		global _
		global ngettext

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)

	def disable(self):
		self.active = False

		del self._modules

def init(moduleManager):
	return SettingsFiltererModule(moduleManager)
