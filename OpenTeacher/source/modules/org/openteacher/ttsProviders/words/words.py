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

class TextToSpeechProviderWords(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TextToSpeechProviderWords, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "ttsProvider"
		self.requires = (
			self._mm.mods(type="wordsStringComposer"),
			self._mm.mods(type="textToSpeech"),
		)
		self.uses = (
			self._mm.mods(type="lessonType"),
			self._mm.mods(type="translator"),
			self._mm.mods(type="settings"),
		)
		self.priorities = {
			#I don't like it if my test suite talks to me (the stuff
			#where textToSpeech responds to is tested in the test suite.
			#)
			"test-suite": -1,
		}
		self.filesWithTranslations = ("words.py",)

	def _retranslate(self):
		#setup translation
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		self._pronounceSetting.update({
			"name": _("Pronounce words"),
			"category": _("Pronounciation"),
		})

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		for module in self._mm.mods("active", type="lessonType"):
			module.newItem.handle(self.itemSent)

		try:
			self._settings = self._modules.default(type="settings")
		except IndexError:
			self._pronounceSetting = {
				"value": False,
			}
		else:
			self._pronounceSetting = self._settings.registerSetting(**{
				"internal_name": "org.openteacher.ttsProviders.words.pronounce",
				"type": "boolean",
				"defaultValue": False,
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
		del self._modules
		for module in self._mm.mods("active", type="lessonType"):
			module.newItem.unhandle(self.itemSent)

		del self._pronounceSetting
		if hasattr(self, "_settings"):
			del self._settings

		self.active = False

	def itemSent(self, item):
		if self._pronounceSetting["value"]:
			try:
				text = self._modules.default(
					"active",
					type="wordsStringComposer"
				).compose(item["questions"])
			except KeyError:
				# No questions, I can't pronounce this
				pass
			else:
				self._modules.default(
					"active",
					type="textToSpeech"
				).say.send(text)

def init(moduleManager):
	return TextToSpeechProviderWords(moduleManager)
