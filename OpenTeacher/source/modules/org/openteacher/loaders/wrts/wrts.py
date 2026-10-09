#! /usr/bin/env python
# -*- coding: utf-8 -*-

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

from etree import ElementTree
import locale
import datetime

class WrtsLoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(WrtsLoaderModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "load"
		self.priorities = {
			"default": 756,
		}
		
		self.requires = (
			self._mm.mods(type="wordsStringParser"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("wrts.py",)

	def _retranslate(self):
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		#TRANSLATORS: WRDS is the name of a web service. Also known as
		#TRANSLATORS: WRTS (the Dutch name). International website:
		#http://wrds.eu/
		self.name = _("WRDS")

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.mimetype = "application/x-wrts"
		self.loads = {"wrts": ["words"]}

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self.name
		del self.loads
		del self.mimetype

	def getFileTypeOf(self, path):
		if path.endswith(".wrts"):
			return "words"

	def load(self, path):
		with open(path) as f:
			root = ElementTree.parse(f).getroot()
		#dutch: lijst = list
		listTree = root.find("lijst")

		wordList = {
			"items": list(),
		}

		#dutch: titel = title
		wordList["title"] = listTree.findtext("titel") or u""
		#dutch: taal = language
		wordList["questionLanguage"] = listTree.findtext("taal/a") or u""
		wordList["answerLanguage"] = listTree.findtext("taal/b") or u""

		#change locale temporary; so strptime can do it's work the way
		#it should.
		locale.setlocale(locale.LC_ALL, "C")
		try:
			created = datetime.datetime.strptime(
				listTree.findtext("created").rsplit(" ", 1)[0], #strip tz info
				"%a, %d %b %Y %H:%M:%S" #since our datetime objects are naive
			)
		except (ValueError, AttributeError):
			created = None
		#set locale back to make sure conflicts don't arise with other
		#modules depending on the locale.
		locale.resetlocale()

		#counter is used as word id
		counter = 1

		#dutch: woord = word
		for wordTree in listTree.findall("woord"):
			word = {
				"id": int(),
				"questions": list(),
				"answers": list(),
				"comment": unicode()
			}
			word["id"] = counter
			if created:
				word["created"] = created

			wsp = self._modules.default("active", type="wordsStringParser")
			word["questions"] = wsp.parse(wordTree.findtext("a") or u"")
			word["answers"] = wsp.parse(wordTree.findtext("b") or u"")

			wordList["items"].append(word)

			counter += 1

		return {
			"resources": {},
			"list": wordList,
		}

def init(moduleManager):
	return WrtsLoaderModule(moduleManager)
