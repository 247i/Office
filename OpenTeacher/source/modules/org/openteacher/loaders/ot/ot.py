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

class OpenTeacherLoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(OpenTeacherLoaderModule, self).__init__(*args, **kwargs)

		self.type = "load"
		self.priorities = {
			"default": 540,
		}
		
		self._mm = moduleManager
		self.requires = (
			self._mm.mods(type="wordsStringParser"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("ot.py",)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self.loads = {"ot": ["words"]}
		self.mimetype = "application/x-openteacher"
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

	def _retranslate(self):
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)

		#TRANSLATORS: Please don't translate 'OpenTeacher' unless you've
		#TRANSLATORS: a good reason for doing so in your language, of
		#TRANSLATORS: course. This is used to describe the file format
		#TRANSLATORS: of the OpenTeacher 2.x series in a file dialog.
		self.name = _("OpenTeacher 2.x")

	def disable(self):
		self.active = False

		del self._modules
		del self.name
		del self.loads
		del self.mimetype

	def getFileTypeOf(self, path):
		if path.endswith(".ot"):
			return "words"

	def load(self, path):
		#Create the new word list
		wordList = {
			"items": [],
			"tests": [],
		}
		#Feed the xml parser
		root = ElementTree.parse(open(path)).getroot()

		#Stores the title, question language and answer language
		wordList["title"] = root.findtext("title") or u""
		wordList["questionLanguage"] = root.findtext("question_language") or u""
		wordList["answerLanguage"] = root.findtext("answer_language") or u""

		#create one test, which is used for all results, because .ot
		#doesn't support multiple tests.
		test = {"results": []}

		#because .ot doesn't give words an id, we use a counter.
		counter = 0
		for treeWord in root.findall("word"):
			#Creates the word and sets its id (which is the current
			#value of the counter)
			listWord = {
				"id": counter,
				"comment": u""
			}

			#Parses the question
			known = treeWord.findtext("known") or u""
			listWord["questions"] = self._modules.default(
				"active",
				type="wordsStringParser"
			).parse(known)

			#Parses the answers
			second = treeWord.findtext("second")
			if second is not None:
				foreign = (treeWord.findtext("foreign") or u"") + ", " + second
			else:
				foreign = treeWord.findtext("foreign") or u""
			#remove so the test is also reliable the next time
			del second
			listWord["answers"] = self._modules.default(
				"active",
				type="wordsStringParser"
			).parse(foreign)

			#Parses the results, all are saved in the test made above.
			wrong, total = (treeWord.findtext("results") or "0/0").split("/")
			wrong = int(wrong)
			total = int(total)
			right = total - wrong
			for i in range(right):
				result = {
					"result": "right",
					"itemId": listWord["id"]
				}
				test["results"].append(result)
			for i in range(wrong):
				result = {
					"result": "wrong",
					"itemId": listWord["id"]
				}
				test["results"].append(result)

			#Adds the generated word to the list
			wordList["items"].append(listWord)
			#Increment the counter (= the next word id)
			counter += 1

		#Adds all results to the list
		if test["results"]:
			wordList["tests"].append(test)
		
		return {
			"list": wordList,
			"resources": {},
		}

def init(moduleManager):
	return OpenTeacherLoaderModule(moduleManager)
