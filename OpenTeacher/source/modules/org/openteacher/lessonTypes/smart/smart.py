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

import contextlib

class SmartLessonType(object):
	def __init__(self, createEvent, list, indexes, modifyItem=None, *args, **kwargs):
		super(SmartLessonType, self).__init__(*args, **kwargs)

		self.newItem = createEvent()
		self.lessonDone = createEvent()

		self.list = list
		self._indexes = indexes
		self._modifyItem = modifyItem or (lambda item: item)

		self._test = {
			"results": [],
			"finished": False,
			"pauses": [],
		}
		
		self.askedItems = 0

	@property
	def totalItems(self):
		return len(self._indexes) + self.askedItems

	def start(self):
		self._sendNext()

	def addPause(self, pause):
		self._test["pauses"].append(pause)

	def setResult(self, result):
		# Add the test to the list (if it's not already there)
		self._appendTest()

		self.askedItems += 1

		self._test["results"].append(result)
		if result["result"] == "wrong":
			with contextlib.ignored(IndexError):
				if self._indexes[-1] != self._currentIndex:
					self._indexes.append(self._currentIndex)
			with contextlib.ignored(IndexError):
				if self._currentIndex not in (self._indexes[1], self._indexes[2]):
					self._indexes.insert(2, self._currentIndex)

		self._sendNext()

	def skip(self):
		try:
			self._indexes.insert(2, self._currentIndex)
		except IndexError:
			self._indexes.append(self._currentIndex)
		self._sendNext()

	def correctLastAnswer(self, result):
		self._test["results"][-1] = result

		with contextlib.ignored(IndexError):
			if self._indexes[-1] == self._previousIndex:
				del self._indexes[-1]

		with contextlib.ignored(IndexError):
			#2 became 1 because of the new word
			if self._indexes[1] == self._previousIndex:
				del self._indexes[1]
	
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
		with contextlib.ignored(AttributeError):
			self._previousIndex = self._currentIndex
		try:
			self._currentIndex = self._indexes.pop(0)
		except IndexError:
			#end of lesson
			if len(self._test["results"]) != 0:
				self._test["finished"] = True
				try:
					self.list["tests"]
				except KeyError:
					self.list["tests"] = []
			self.lessonDone.send()
		else:
			item = self.list["items"][self._currentIndex]
			self.newItem.send(self._modifyItem(item))

class SmartModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(SmartModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "lessonType"
		self.uses = (
			self._mm.mods(type="event"),
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("smart.py",)
		self.priorities = {
			"default": 130,
		}

	def enable(self):
		#Translations
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
		self.name = _("Smart")

	def disable(self):
		self.active = False

		del self._modules
		del self.newItem
		del self.name

	@property
	def _createEvent(self):
		return self._modules.default(type="event").createEvent

	def createLessonType(self, *args, **kwargs):
		lessonType = SmartLessonType(self._createEvent, *args, **kwargs)
		lessonType.newItem.handle(self.newItem.send)
		return lessonType

def init(moduleManager):
	return SmartModule(moduleManager)
