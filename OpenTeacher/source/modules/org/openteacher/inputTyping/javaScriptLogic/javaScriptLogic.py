#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2013, Marten de Vries
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

class JSInputTypingLogicModule(object):
	"""This module offers an object that can be used to control the part
	   of a GUI where the user types his/her answer in in a test.

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(JSInputTypingLogicModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "inputTypingLogic"
		self.javaScriptImplementation = True
		self.requires = (
			self._mm.mods("javaScriptImplementation", type="javaScriptEvent"),
			self._mm.mods("javaScriptImplementation", type="wordsStringParser"),
			self._mm.mods("javaScriptImplementation", type="wordsStringChecker"),
			self._mm.mods("javaScriptImplementation", type="wordsStringComposer"),
			self._mm.mods(type="javaScriptEvaluator"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("inputTypingLogic.js",)

	def createController(self, *args, **kwargs):
		return self._js["InputTypingController"].new(*args, **kwargs)

	def enable(self):
		self._modules = next(iter(self._mm.mods(type="modules")))
		self._js = self._modules.default("active", type="javaScriptEvaluator").createEvaluator()

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		with open(self._mm.resourcePath("inputTypingLogic.js")) as f:
			self.code = f.read()
		self.code += self._modules.default("active", "javaScriptImplementation", type="javaScriptEvent").code
		self.code += self._modules.default("active", "javaScriptImplementation", type="wordsStringParser").code
		self.code += self._modules.default("active", "javaScriptImplementation", type="wordsStringComposer").code
		self.code += self._modules.default("active", "javaScriptImplementation", type="wordsStringChecker").code
		self._js.eval(self.code)

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
		self._js["_"] = _
		self._js["ngettext"] = ngettext

	def disable(self):
		self.active = False

		del self._modules
		del self._js
		del self.code

def init(moduleManager):
	return JSInputTypingLogicModule(moduleManager)
