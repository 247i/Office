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

import copy
import datetime

class Teach2000SaverModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(Teach2000SaverModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "save"
		self.priorities = {
			"default": 448,
		}
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("t2k.py",)

	def _retranslate(self):
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		#TRANSLATORS: This is the name of an application. For more info
		#TRANSLATORS: about Teach2000: http://www.teach2000.org/
		self.name = _("Teach2000")

	def enable(self):
		global pyratemp
		try:
			import pyratemp
		except ImportError:
			return #remain inactive
		self._modules = set(self._mm.mods(type="modules")).pop()
		self.saves = {"words": ["t2k"]}

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
		#copy, we're going to modify it
		wordList = copy.deepcopy(lesson.list)

		for word in wordList.get("items", []):
			word["wrongCount"] = 0
			word["rightCount"] = 0
			for test in wordList.get("tests", []):
				for result in test["results"]:
					if result["itemId"] == word["id"]:
						if result["result"] == "right":
							word["rightCount"] += 1
						else:
							word["wrongCount"] += 1

		for test in wordList.get("tests", []):
			test["note"] = self._calculateNote(test)
			test["start"] = self._startTime(test)
			test["duration"] = self._duration(test)
			test["answerscorrect"] = self._answersCorrect(test)
			test["wrongonce"] = self._wrongOnce(test)
			test["wrongtwice"] = self._wrongTwice(test)
			test["wrongmorethantwice"] = self._wrongMoreThanTwice(test)

		templatePath = self._mm.resourcePath("template.xml")
		t = pyratemp.Template(open(templatePath).read())
		data = {
			"wordList": wordList,
		}
		content = t(**data)
		with open(path, "w") as f:
			f.write(content.encode("UTF-8"))

		lesson.path = None

	def _calculateNote(self, test):
		#dutch note, but with full float representation.
		right = 0
		wrong = 0
		for result in test["results"]:
			if result["result"] == "right":
				right += 1
			else:
				wrong += 1
		return str(right / float(right + wrong) * 9 + 1)

	def _startTime(self, test):
		try:
			t = test["results"][0]["active"][0]["start"]
		except (KeyError, IndexError):
			t = datetime.datetime.now()
		return self._composeDateTime(t)

	def _composeDateTime(self, dt):
		#chop off the last three millisecond decimals, because Teach2000
		#can't handle that kind of precision. That's bad.
		return dt.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]

	def _duration(self, test):
		try:
			start = test["results"][0]["active"]["start"]
			end = test["results"][-1]["active"]["end"]
		except (KeyError, IndexError):
			t = datetime.datetime.fromtimestamp(0)
		else:
			t = datetime.datetime.fromtimestamp(0) + (end - start)
		#Teach2000 is written in Pascal... Blegh :P.
		#use its epoch. (So not the unix one)
		#strftime doesn't allow dates < 1900, so that's why the weird
		#string formatting. See _composeDateTime for info on the [:-3].
		return "1899-12-30T%s" % t.strftime("%H:%M:%S.%f")[:-3]

	def _answersCorrect(self, test):
		correct = 0
		for result in test["results"]:
			if result["result"] == "right":
				correct += 1
		return correct

	def _stats(self, test):
		stats = {}
		for result in test["results"]:
			if result["result"] == "wrong":
				try:
					stats[result["itemId"]] += 1
				except KeyError:
					stats[result["itemId"]] = 1
		return stats

	def _wrongOnce(self, test):
		return self._stats(test).values().count(1)

	def _wrongTwice(self, test):
		return self._stats(test).values().count(2)

	def _wrongMoreThanTwice(self, test):
		count = 0
		for val in self._stats(test).values():
			if val > 2:
				count += 1
		return count

def init(moduleManager):
	return Teach2000SaverModule(moduleManager)
