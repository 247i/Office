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

class TxtSaverModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TxtSaverModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "save"
		self.priorities = {
			"default": 924,
		}
		self.requires = (
			self._mm.mods(type="wordsStringComposer"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
			self._mm.mods(type="settings"),
		)
		self.filesWithTranslations = ("txt.py",)

	def _retranslate(self):
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		#TRANSLATORS: This is one of the file types OpenTeacher can
		#TRANSLATORS: export to.
		self.name = _("Plain text")
		self._maxLenSetting.update({
				"name": _("Minimum amount of spaces between words"),
				"category": _("Input and output"),
				"subcategory": _(".txt saving"),
		})

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self.saves = {"words": ["txt"]}

		try:
			self._settings = self._modules.default(type="settings")
		except IndexError, e:
			self._maxLenSetting = dict()
			self._maxLenSetting["value"] = 8
		else:
			self._maxLenSetting = self._settings.registerSetting(**{
				"internal_name": "org.openteacher.savers.txt.maxLen",
				"type": "number",
				"defaultValue":8,
				"minValue": 0,
				"advanced": True,
			})

		#Translations
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
		if hasattr(self, "_settings"):
			del self._settings
		del self._maxLenSetting

	@property
	def _compose(self):
		return self._modules.default(
			"active",
			type="wordsStringComposer"
		).compose

	def _buildMetadata(self, lesson):
		text = u""
		if "title" in lesson.list:
			text += lesson.list["title"] + "\n\n"
		if "questionLanguage" in lesson.list and "answerLanguage" in lesson.list:
			text += lesson.list["questionLanguage"] + " - " + lesson.list["answerLanguage"] + "\n\n"
		return text

	def _maxLength(self, lesson):
		def getQuestionLength(word):
			return len(self._compose(word.get("questions", [])))

		lengths = map(getQuestionLength, lesson.list["items"])
		maxLen = max(lengths) + 1
		if maxLen < self._maxLenSetting["value"]:
			maxLen = 8
		return maxLen

	def _buildListLines(self, lesson):
		if len(lesson.list["items"]) == 0:
			return
		maxLen = self._maxLength(lesson)
		for word in lesson.list["items"]:
			questions = self._compose(word.get("questions", []))

			yield u"".join([
				questions,
				(maxLen - len(questions)) * " ",
				self._compose(word.get("answers", [])),
			])

	def save(self, type, lesson, path):
		text = self._buildMetadata(lesson)
		text += "\n".join(self._buildListLines(lesson))

		with open(path, "w") as f:
			f.write(text.encode("UTF-8"))

		lesson.path = None

def init(moduleManager):
	return TxtSaverModule(moduleManager)
