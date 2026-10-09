#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2012, Cas Widdershoven
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

class Word(object):
	def __init__(self, word):
		self.mistakes = 0
		self.length = len(word)

		self._word = word

	def __unicode__(self):
		return self._word

	def guessCharacter(self, guessedCharacter):
		results = [
			(match.start(), guessedCharacter)
			for match in re.finditer(guessedCharacter, self._word)
		]

		if len(results) == 0:
			self.mistakes += 1
		return results

	def guessWord(self, guessedWord):
		isCorrect = guessedWord == self._word
		if not isCorrect:
			self.mistakes += 2
		return isCorrect
