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

class KvtmlSaverModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(KvtmlSaverModule, self).__init__(*args, **kwargs)

		self._mm = moduleManager
		self.type = "save"
		self.priorities = {
			"default": 532,
		}
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.requires = (
			self._mm.mods(type="wordsStringComposer"),
			self._mm.mods(type="metadata"),
			self._mm.mods(type="languageCodeGuesser"),
		)
		self.filesWithTranslations = ("kvtml.py",)

	def _retranslate(self):
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		#TRANSLATORS: A document format used by some KDE applications.
		self.name = _("KDE Vocabulary Document")

	def enable(self):
		global pyratemp
		try:
			import pyratemp
		except ImportError: # pragma: no cover
			return #remain inactive
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._metadata = self._modules.default("active", type="metadata").metadata

		self.saves = {"words": ["kvtml"]}

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
		del self._metadata
		del self.name
		del self.saves

	@property
	def _compose(self):
		return self._modules.default(
			"active",
			type="wordsStringComposer"
		).compose

	@property
	def _guessLanguageCode(self):
		return self._modules.default("active", type="languageCodeGuesser").guessLanguageCode

	def save(self, type, lesson, path):
		class EvalPseudoSandbox(pyratemp.EvalPseudoSandbox):
			def __init__(self2, *args, **kwargs):
				pyratemp.EvalPseudoSandbox.__init__(self2, *args, **kwargs)

				self2.register("compose", self._compose)

		templatePath = self._mm.resourcePath("template.xml")
		t = pyratemp.Template(
			open(templatePath).read(),
			eval_class=EvalPseudoSandbox
		)

		questionLang = lesson.list.get("questionLanguage", u"")
		answerLang = lesson.list.get("answerLanguage", u"")
		data = {
			"list": lesson.list,
			"appname": self._metadata["name"],
			"appversion": self._metadata["version"],
			"questionLocale": self._guessLanguageCode(questionLang),
			"answerLocale": self._guessLanguageCode(answerLang),
		}
		content = t(**data)
		with open(path, "w") as f:
			f.write(content.encode("UTF-8"))
		lesson.path = None

def init(moduleManager):
	return KvtmlSaverModule(moduleManager)
