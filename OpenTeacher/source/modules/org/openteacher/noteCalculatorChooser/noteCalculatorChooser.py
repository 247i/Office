#! /usr/bin/env python
# -*- coding: utf-8 -*-

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

class NoteCalculatorChooserModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(NoteCalculatorChooserModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "noteCalculatorChooser"
		self.requires = (
			#without at least one, the module is useless
			self._mm.mods(type="noteCalculator"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
			self._mm.mods(type="settings"),
		)
		self.filesWithTranslations = ("noteCalculatorChooser.py",)

	def _retranslate(self):
		#Load translations
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)

		self._setting.update({
			"name": _("Note notation"),
			"category": _("General"),
		})

	def _updateOptions(self):
		noteCalculators = map(
			lambda mod: (mod.name, mod.__class__.__file__),
			sorted(self._mm.mods("active", type="noteCalculator"), key=lambda m: m.name)
		)

		self._setting["options"] = noteCalculators

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()

		default = self._modules.default("active", type="noteCalculator").__class__.__file__
		try:
			settings = self._modules.default(type="settings")
		except IndexError:
			self._setting = {"value": default}
		else:
			self._setting = self._modules.default(type="settings").registerSetting(**{
				"internal_name": "org.openteacher.noteCalculatorChooser.noteCalculator",
				"type": "option",
				"defaultValue": default,
			})

		#Connect to the languageChanged event so retranslating is done.
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
			translator.languageChangeDone.handle(self._updateOptions)
		self._retranslate()
		self._updateOptions()

		self.active = True

	@property
	def noteCalculator(self):
		for mod in self._mm.mods("active", type="noteCalculator"):
			if mod.__class__.__file__ == self._setting["value"]:
				return mod
		#just in case the file isn't there anymore.
		return self._modules.default("active", type="noteCalculator")

	def disable(self):
		self.active = False

		del self._setting
		del self._modules

def init(moduleManager):
	return NoteCalculatorChooserModule(moduleManager)
