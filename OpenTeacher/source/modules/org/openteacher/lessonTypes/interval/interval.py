#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2013, Marten de Vries
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

import random

class IntervalLessonType(object):
	def __init__(self, createEvent, list, indexes, modifyItem, groupSizeSetting, minQuestionsSetting, whenKnownSetting, *args, **kwargs):
		super(IntervalLessonType, self).__init__(*args, **kwargs)

		self.newItem = createEvent()
		self.lessonDone = createEvent()
		self.list = list
		self._indexes = indexes
		self._modifyItem = modifyItem or (lambda item: item)

		self._groupSizeSetting = groupSizeSetting
		self._minQuestionsSetting = minQuestionsSetting
		self._whenKnownSetting = whenKnownSetting

		self._test = {
			"results": [],
			"finished": False,
			"pauses": [],
		}

	@property
	def totalItems(self):
		#the indexes still to do in the very best case + the amount of
		#items already asked.
		return len(self._indexes) + self.askedItems

	@property
	def askedItems(self):
		#the length of all the unique itemId's in the results of the
		#current tests gives the amount of asked items
		ids = set([result["itemId"] for result in self._test["results"]])
		return len(ids)

	@property
	def _minQuestions(self):
		minQuestions = self._minQuestionsSetting["value"]
		if minQuestions < 1:
			minQuestions = 2
		return minQuestions

	@property
	def _whenKnown(self):
		whenKnown = self._whenKnownSetting["value"]
		if whenKnown < 0 or whenKnown > 99:
			whenKnown = 80
		return whenKnown

	@property
	def _groupSize(self):
		#get the values of some settings
		return max(self._groupSizeSetting["value"], 2)

	def setResult(self, result):
		"""result is a Result-type object saying whether the question
		   was answered right or wrong

		"""
		#Add the test to the list (if it's not already there)
		self._appendTest()
		#and add this result, so it's weighed in the calculations below
		self._test["results"].append(result)

		#get the amount of right and wrong answers for the current item
		#in this test.
		right = 0
		wrong = 0
		currentItem = self.list["items"][self._currentIndex]
		for loopResult in self._test["results"]:
			if loopResult["itemId"] == currentItem["id"]:
				if loopResult["result"] == "right":
					right += 1
				elif loopResult["result"] == "wrong":
					wrong += 1

		#if the item is not known well enough, add it to the list again
		#so it's asked later.
		total = right + wrong
		percentageRight = right / float(total) * 100.0
		if total < self._minQuestions or percentageRight < self._whenKnown:
			#pos may not be 0, because the current item shouldn't be
			#asked again directly. Size is -1 because indexes start at
			#0, and counting at 1.
			try:
				pos = random.randint(1, min(len(self._indexes), self._groupSize -1))
			except ValueError:
				#len(self._indexes) is 0, but the item needs to be asked
				#again. No option other than doing it immediately.
				pos = 0
			self._indexes.insert(pos, self._currentIndex)

		#keep the user busy.
		self._sendNext()

	def addPause(self, pause):
		self._test["pauses"].append(pause)

	def correctLastAnswer(self, result):
		#it's questioned again anyway. Who cares...
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
			self._currentIndex = self._indexes.pop(0)
		except IndexError:
			self._test["finished"] = True
			self.lessonDone.send()
		else:
			item = self.list["items"][self._currentIndex]
			self.newItem.send(self._modifyItem(item))

	#Just send the next question and everything will be fine :)
	start = _sendNext

	def skip(self):
		#just ask again at the end.
		self._indexes.append(self._currentIndex)
		self._sendNext()

class IntervalModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(IntervalModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "lessonType"
		self.requires = (
			self._mm.mods(type="event"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
			self._mm.mods(type="settings"),
		)
		self.filesWithTranslations = ("interval.py",)
		self.priorities = {
			"default": 170,
		}

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()

		# Settings
		try:
			self._settings = self._modules.default(type="settings")
		except IndexError, e:
			self._whenKnownSetting = {"value": 80}
			self._minQuestionsSetting = {"value": 2}
			self.__groupSizeSetting = {"value": 4}
		else:
			self._groupSizeSetting = self._settings.registerSetting(**{
				"internal_name": "org.openteacher.lessonTypes.interval.groupSize",
				"type": "number",
				"defaultValue": 4,
				"minValue": 1,
			})
			self._minQuestionsSetting = self._settings.registerSetting(**{
				"internal_name": "org.openteacher.lessonTypes.interval.minQuestions",
				"type": "number",
				"defaultValue": 2,
				"minValue": 1,
			})
			self._whenKnownSetting = self._settings.registerSetting(**{
				"internal_name": "org.openteacher.lessonTypes.interval.whenKnown",
				"type": "number",
				"defaultValue":80,
				"minValue": 0,
				"maxValue": 99,
			})

		self.newItem = self._createEvent()

		#register _retranslate()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

	def _retranslate(self):
		#install translator
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)

		self.name = _("Interval")

		#settings
		categories = {
			"category": _("Lesson type"),
			"subcategory": _("Interval"),
		}
		self._groupSizeSetting["name"] = _("Maximum size of group")
		self._groupSizeSetting.update(categories)
		self._minQuestionsSetting["name"] = _("Minimum amount of questions asked")
		self._minQuestionsSetting.update(categories)
		self._whenKnownSetting["name"] = _("Percent right before known")
		self._whenKnownSetting.update(categories)

	def disable(self):
		self.active = False

		del self._modules
		del self._settings
		del self._groupSizeSetting
		del self._minQuestionsSetting
		del self._whenKnownSetting

		del self.newItem
		del self.name

	@property
	def _createEvent(self):
		return self._modules.default(type="event").createEvent

	def createLessonType(self, list, indexes, modifyItem=None):
		lessonType = IntervalLessonType(self._createEvent, list, indexes, modifyItem, self._groupSizeSetting, self._minQuestionsSetting, self._whenKnownSetting)
		lessonType.newItem.handle(self.newItem.send)
		return lessonType

def init(moduleManager):
	return IntervalModule(moduleManager)
