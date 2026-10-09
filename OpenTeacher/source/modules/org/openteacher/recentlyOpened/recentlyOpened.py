#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011, Marten de Vries
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

class RecentlyOpenedModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(RecentlyOpenedModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "recentlyOpened"

		self.uses = (
			self._mm.mods(type="translator"),
			self._mm.mods(type="settings"),
		)

		self.requires = (
			self._mm.mods(type="event"),
			self._mm.mods(type="dataStore"),
		)
		self.filesWithTranslations = ("recentlyOpened.py",)

	def add(self, **kwargs):
		"""This method adds 'something that was recently opened' to the
		   list. The arguments should be:
		    * label
		     * text describing the recently opened thing. E.g. a title
		       or, if nothing better exists, a file name.
		    * icon
			 * path to an icon file, optional
		    * moduleArgsSelectors, moduleKwargsSelectors
		     * used to select the module that can re-open the recently
		       opened thing. Same as in:
		        self._mm.mods(*moduleArgsSelectors, **moduleKwargselectors)
			* method
			 * the method that should be called on the earlier selected
			   module to re-open the recently opened thing.
			* args
			 * the positional arguments that need to be passed to
			   'method'
			* kwargs
			 * the keyword arguments that need to be passed to 'method'

		"""
		if kwargs in self._recentlyOpened:
			self._recentlyOpened.remove(kwargs)
		self._recentlyOpened.insert(0, kwargs)
		while len(self._recentlyOpened) > self._sizeSetting["value"]:
			self._recentlyOpened.pop()
		self.updated.send()

	def getRecentlyOpened(self):
		return self._recentlyOpened

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		store = self._modules.default(type="dataStore").store
		try:
			self._recentlyOpened = store["org.openteacher.recentlyOpened"]
		except KeyError:
			self._recentlyOpened = store["org.openteacher.recentlyOpened"] = []

		self.updated = self._modules.default(type="event").createEvent()

		try:
			self._sizeSetting = self._modules.default(type="settings").registerSetting(**{
				"internal_name": "org.openteacher.recentlyOpened.size",
				"type": "number",
				"defaultValue": 10,
			})
		except IndexError:
			self._sizeSetting = {
				"value": 10,
			}

		#Make sure this mod retranslates on language change.
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		#Translate the UI for the first time.
		self._retranslate()

		self.active = True

	def _retranslate(self):
		#Install translator for this method
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)

		self._sizeSetting.update({
			"name": _("Amount of recently opened files to remember"),
			"category": _("General"),
		})

	def disable(self):
		self.active = False

		del self.updated
		del self._modules
		del self._recentlyOpened
		del self._sizeSetting

def init(moduleManager):
	return RecentlyOpenedModule(moduleManager)
