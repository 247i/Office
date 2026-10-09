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

import re

class DictFallback(object):
	def check(self, word):
		return True

class TokenizerFallback(object):
	_pattern = re.compile(r"\W", re.UNICODE)

	def __call__(self, text):
		pos = 0
		for word in self._pattern.split(text):
			if word:
				yield word, pos
			pos += len(word) + 1

class Checker(object):
	def __init__(self, languageCode, *args, **kwargs):
		super(Checker, self).__init__(*args, **kwargs)

		if languageCode is None:
			languageCode = "this is the easiest way to make enchant raise an error."

		try:
			self._dict = enchant.Dict(languageCode)
		except enchant.errors.DictNotFoundError:
			self._dict = DictFallback()

		try:
			self._tokenizer = enchant.tokenize.get_tokenizer(languageCode)
		except enchant.errors.TokenizerNotFoundError:
			self._tokenizer = TokenizerFallback()

	def check(self, word):
		return self._dict.check(word)

	def split(self, text):
		return list(self._tokenizer(text))

class SpellCheckModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(SpellCheckModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "spellChecker"
		self.requires = (
			self._mm.mods(type="languageCodeGuesser"),
		)

	_guessLanguageCode = property(lambda self: self._modules.default("active", type="languageCodeGuesser").guessLanguageCode)

	def createChecker(self, language):
		languageCode = self._guessLanguageCode(language)
		return Checker(languageCode)

	def enable(self):
		global enchant
		try:
			import enchant
			import enchant.errors
			import enchant.tokenize
		except ImportError:
			return
		self._modules = next(iter(self._mm.mods(type="modules")))

		self.active = True

	def disable(self):
		self.active = False

		del self._modules

def init(moduleManager):
	return SpellCheckModule(moduleManager)
