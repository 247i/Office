#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2013, Marten de Vries
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
import contextlib

class OpenTeacherSaverModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(OpenTeacherSaverModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "save"
		self.priorities = {
			"default": 364,
		}
		self.requires = (
			self._mm.mods(type="wordsStringComposer"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("ot.py",)

	def enable(self):
		global pyratemp
		try:
			import pyratemp
		except ImportError:
			return #remain inactive

		self._modules = set(self._mm.mods(type="modules")).pop()
		self.saves = {"words": ["ot"]}

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
		del self.saves

	@property
	def _compose(self):
		return self._modules.default(
			"active",
			type="wordsStringComposer"
		).compose

	def save(self, type, lesson, path):
		#Copy, because we're going to modify it
		wordList = copy.deepcopy(lesson.list)

		for word in wordList.get("items", []):
			#results
			word["results"] = {"right": 0, "wrong": 0}
			for test in wordList.get("tests", []):
				for result in test["results"]:
					if result["itemId"] == word["id"]:
						with contextlib.ignored(KeyError):
							word["results"][result["result"]] += 1
			#known, foreign and second
			word["known"] = self._compose(word["questions"])
			if len(word["answers"]) == 1 and len(word["answers"][0]) > 1:
				word["foreign"] = word["answers"][0][0]
				word["second"] = self._compose([word["answers"][0][1:]])
			else:
				word["foreign"] = self._compose(word["answers"])
				word["second"] = u""

		templatePath = self._mm.resourcePath("template.xml")
		t = pyratemp.Template(open(templatePath).read())
		data = {
			"wordList": wordList
		}
		content = t(**data)
		with open(path, "w") as f:
			f.write(content.encode("UTF-8"))

		lesson.path = None

def init(moduleManager):
	return OpenTeacherSaverModule(moduleManager)
