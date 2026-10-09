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

from etree import ElementTree

import datetime
import re
import atexit
import tempfile
import os

class Teach2000LoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(Teach2000LoaderModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "load"
		self.priorities = {
			"default": 648,
		}
		
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.requires = (
			self._mm.mods(type="mimicryTypefaceConverter"),
		)
		self.filesWithTranslations = ("t2k.py",)
		self._tempPaths = set()
		atexit.register(self._cleanUp)

	@property
	def _convertMimicryTypeface(self):
		return self._modules.default("active", type="mimicryTypefaceConverter").convert

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
		self._modules = set(self._mm.mods(type="modules")).pop()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.mimetype = "application/x-teach2000"
		self.loads = {"t2k": ["words"]}

		self.active = True

	def _cleanUp(self):
		for path in getattr(self, "_tempPaths", []):
			os.remove(path)

	def disable(self):
		self.active = False

		del self._modules
		del self.name
		del self.loads
		del self.mimetype

	def getFileTypeOf(self, path):
		if path.endswith(".t2k"):
			root = ElementTree.parse(open(path)).getroot()
			if root.find("message_data/items//item/answers[@type='4']") is not None:
				return "topo"
			else:
				#also support other formats in the future? Well,
				#everything that's left can be opened like it's of type 'words'...
				return "words"

	def load(self, path):
		"""Loads a .t2k file into the OpenTeacher data structure.
		   http://www.teach2000.nl/help/00513_advanced_file_format.htm

		"""
		root = ElementTree.parse(open(path)).getroot()
		if self.getFileTypeOf(path) == "topo":
			return self._loadTopo(root)
		else:
			return self._loadWords(root)

	def _loadResults(self, root):
		#create one test to save all results in that are in the t2k file
		#(t2k doesn't have enough information to know which word was
		#wrong in which test, so we can have only one test.)
		test = {
			"finished": True,
			"results": [],
		}
		for item in root.findall("message_data/items/item"):
			#add a result for every time this word was wrong
			for i in range(int(item.findtext("errors") or 0)):
				test["results"].append({
					"itemId": self._getId(item), "result": "wrong",
				})
			#add a result for every time this word was right
			for i in range(int(item.findtext("correctcount") or 0)):
				test["results"].append({
					"itemId": self._getId(item),
					"result": "right",
				})

		#if there were results
		if test["results"]:
			#get the time of the first start result and the one of the
			#last for a global idea of the time range of this 'mega'
			#test. Duration isn't used, since it's way off anyway.
			try:
				startTime = root.findall("message_data/testresults/testresult")[0].findtext("dt")
				endTime = root.findall("message_data/testresults/testresult")[-1].findtext("dt")
			except IndexError:
				pass
			else:
				startTime = self._parseDt(startTime)
				endTime = self._parseDt(endTime)

				#store those times in the first and last result. (which may
				#be the same, technically, but that doesn't matter...)
				test["results"][0]["active"] = {
					"start": startTime,
					"end": startTime,
				}
				test["results"][-1]["active"] = {
					"start": endTime,
					"end": endTime
				}
		return test

	def _getId(self, item):
		return int(item.get("id"))

	def _loadTopo(self, root):
		placesList = {
			"items": [],
			"tests": [],
		}

		for item in root.findall("message_data/items/item"):
			answers = item.find(".//answers")
			answerTexts = [a.text for a in answers.findall(".//answer")]
			place = {
				"id": self._getId(item),
				"x": int(answers.get("x") or 0),
				"y": int(answers.get("y") or 0),
				"name": self._stripBBCode(u", ".join(answerTexts)),
			}
			placesList["items"].append(place)

		#append the test to the list
		test = self._loadResults(root)
		if test["results"]:
			placesList["tests"] = [test]

		mapElement = root.find("message_data/mapquizfile")
		fd, mapPath = tempfile.mkstemp("." + mapElement.get("ext"))
		os.close(fd)
		self._tempPaths.add(mapPath)
		with open(mapPath, "wb") as f:
			f.write(mapElement.text.decode("base64"))

		return {
			"resources": {
				"mapPath": mapPath,
			},
			"list": placesList,
		}

	def _loadWords(self, root):
		wordList = {
			"items": [],
			"tests": [],
		}

		questionFont = root.findtext("message_data/font_question") or u""
		answerFont = root.findtext("message_data/answer_question") or u""

		for item in root.findall("message_data/items/item"):
			word = {
				"id": int(),
				"questions": list(),
				"answers": list(),
			}

			#id
			word["id"] = self._getId(item)

			#questions
			word["questions"].append([])
			for question in item.findall(".//question"):
				#strip BBCode for now
				text = self._stripBBCode(question.text)
				convertedText = self._convertMimicryTypeface(questionFont, text)
				word["questions"][0].append(convertedText)

			#answers
			word["answers"].append([])
			for answer in item.findall(".//answer"):
				#strip BBCode for now
				text = self._stripBBCode(answer.text)
				convertedText = self._convertMimicryTypeface(questionFont, text)
				word["answers"][0].append(convertedText)

			#remarks (comment in OT)
			comment = item.findtext("remarks")
			if comment:
				word["comment"] = comment

			#remarks_aa (commentAfterAnswering in OT)
			commentAfterAnswering = item.findtext("remarks_aa")
			if commentAfterAnswering:
				word["commentAfterAnswering"] = commentAfterAnswering

			wordList["items"].append(word)

		#append the test to the list
		test = self._loadResults(root)
		if test["results"]:
			wordList["tests"] = [test]

		return {
			"resources": {},
			"list": wordList,
		}

	def _stripBBCode(self, string):
		"""Strips all BBCode tags"""
		return re.sub(r"\[[\w/]*\]", u"", string)

	def _parseDt(self, string):
		"""Parses a date string as found in T2K files to a datetime
		   object."""
		return datetime.datetime.strptime(string, "%Y-%m-%dT%H:%M:%S.%f")

def init(manager):
	return Teach2000LoaderModule(manager)
