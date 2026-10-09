#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2012, Marten de Vries
#	Copyright 2011, Cas Widdershoven
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

class AllOnceLessonType(object):
	"""Events:
	   - newItem
	   - lessonDone

	"""
	def __init__(self, createEvent, list, indexes, modifyItem=None, *args, **kwargs):
		super(AllOnceLessonType, self).__init__(*args, **kwargs)

		self.newItem = createEvent()
		self.lessonDone = createEvent()
		self.list = list
		self._indexes = indexes
		#fallback: it simply doesn't change a thing
		self._modifyItem = modifyItem or (lambda item: item)

		self._test = {
			"results": [],
			"finished": False,
			"pauses": [],
		}

		self.totalItems = len(self._indexes)
		self.askedItems = 0

	def start(self):
		self._sendNext()

	def skip(self):
		self._indexes.append(self._indexes.pop(self.askedItems))
		self._sendNext()

	def setResult(self, result):
		# Add the test to the list (if it's not already there)
		self._appendTest()

		self._test["results"].append(result)

		self.askedItems += 1
		self._sendNext()

	def addPause(self, pause):
		self._test["pauses"].append(pause)

	def correctLastAnswer(self, result):
		self._test["results"][-1] = result
	
	def _appendTest(self):
		try:
			self.list["tests"][-1]
		except KeyError:
			self.list["tests"] = [self._test]
		except IndexError:
			self.list["tests"].append(self._test)
		else:
			if not self.list["tests"][-1] == self._test:
				self.list["tests"].append(self._test)

	def _sendNext(self):		
		try:
			i = self._indexes[self.askedItems]
		except IndexError:
			#lesson end
			if len(self._test["results"]) != 0:
				self._test["finished"] = True
				try:
					self.list["tests"]
				except KeyError:
					self.list["tests"] = []
			self.lessonDone.send()
		else:
			item = self.list["items"][i]
			self.newItem.send(self._modifyItem(item))

class AllOnceModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(AllOnceModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "lessonType"
		self.testName = "allOnce"
		self.requires = (
			self._mm.mods(type="event"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("allOnce.py",)
		self.priorities = {
			"default": 140,
		}

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.newItem = self._createEvent()
		self.active = True

	def _retranslate(self):
		#Translations
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		self.name = _("All once")

	def disable(self):
		self.active = False

		del self._modules
		del self.newItem
		del self.name

	@property
	def _createEvent(self):
		return self._modules.default(type="event").createEvent

	def createLessonType(self, *args, **kwargs):
		lessonType = AllOnceLessonType(self._createEvent, *args, **kwargs)
		lessonType.newItem.handle(self.newItem.send)
		return lessonType

def init(moduleManager):
	return AllOnceModule(moduleManager)
