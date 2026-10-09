#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011, 2013, Marten de Vries
#	Copyright 2012, Milan Boers
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

import gettext
import locale
import os

class TranslatorModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TranslatorModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "translator"
		self.requires = (
			self._mm.mods(type="event"),
		)
		self.uses = (
			self._mm.mods(type="settings"),
		)
		self.filesWithTranslations = ("translator.py",)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		createEvent = self._modules.default(type="event").createEvent
		self.languageChanged = createEvent()
		self.languageChangeDone = createEvent()

		try:
			settings = self._modules.default(type="settings")
		except IndexError, e:
			self._languageSetting = {
				"value": None,
			}
		else:
			self._languageSetting = settings.registerSetting(**{
				"internal_name": "org.openteacher.translator.language",
				"type": "language",
				"defaultValue": None,
				"callback": {
					"args": ("active",),
					"kwargs": {"type": "translator"},
					"method": "sendLanguageChanged",
				}
			})
		#add the setting name, which needs to be translated itself
		self._retranslate()
		
		#subscribe this module's _retranslate to itself
		self.languageChanged.handle(self._retranslate)

		self.active = True

	def _retranslate(self):
		_, ngettext = self.gettextFunctions(
			self._mm.resourcePath("translations")
		)
		self._languageSetting.update({
			"name": _("Language"),
			"category": _("General"),
			"subcategory": _("Locale"),
		})

	def sendLanguageChanged(self):
		"""A wrapper method called by the setting callback, which can't
		   call the send() methods directly

		"""
		self.languageChanged.send()
		self.languageChangeDone.send()

	@property
	def language(self):
		lang = self._languageSetting["value"]
		if not lang:
			return locale.getdefaultlocale()[0] or "C"
		return lang

	@language.setter
	def language(self, lang):
		self._languageSetting["value"] = lang
		self.sendLanguageChanged()

	def gettextFunctions(self, localeDir, language=None):
		if not language:
			#Try to fill it
			language = self.language
		path = os.path.join(localeDir, language + ".mo")
		if not os.path.isfile(path):
			path = os.path.join(localeDir, language.split("_")[0] + ".mo")
		if os.path.isfile(path):
			t = gettext.GNUTranslations(open(path, "rb"))
			return t.ugettext, t.ungettext

		#Couldn't find a mo file. Return the default translator
		gettextFallback = unicode
		def ngettextFallback(x, y, n):
			if n == 1:
				return unicode(x)
			else:
				return unicode(y)
		return gettextFallback, ngettextFallback

	def disable(self):
		self.active = False

		del self._modules
		del self.languageChanged
		del self.languageChangeDone
		del self._languageSetting

def init(moduleManager):
	return TranslatorModule(moduleManager)
