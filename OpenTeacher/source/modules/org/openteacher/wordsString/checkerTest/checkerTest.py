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

import unittest

class WordsStringCheckerTestCase(unittest.TestCase):
	def setUp(self):
		self.word1 = {
			"id": 0,
			"questions": [[u"in"]],
			"comment": u"+abl",
			"answers": [[u"in", u"op", u"bij"], [u"tijdens"]],
		}

		self.word2 = {
			"id": 1,
			"questions": [[u"in"]],
			"comment": u"+acc",
			"answers": [[u"naar(binnen)", u"in"], [u"tot", u"jegens"]],
		}

		self.emptyWord = {
			"id": 0,
			"questions": [],
			"answers": [],
		}

	def testSingleRightAnswer(self):
		self._test([[u"in"]], self.word1, "wrong")

	def testMultipleRightAnswers(self):
		self._test([[u"in", u"tijdens", u"bij"]], self.word1, "right")

	def testWrongAnswersNextToRightOnes(self):
		#opp != op
		self._test([[u"in", u"tijdens", u"opp"]], self.word1, "wrong")

	def testSingleWrongAnswer(self):
		self._test([[u"opp"]], self.word1, "wrong")

	def testEmptyAnswer(self):
		self._test([], self.word1, "wrong")

	def testEmptyAnswerWithEmptyWord(self):
		self._test([], self.emptyWord, "right")

	def testFullAnswer(self):
		self._test([[u"in", u"op", u"bij"], [u"tijdens"]], self.word1, "right")

	def testFullAnswerWithExtraWrongWords(self):
		#gelijktijdig met isn't in the answers (however it's possibly
		#right linguistically seen.)
		self._test([[u"in", "op", "bij"], [u"tijdens", u"gelijktijdig met"]], self.word1, "wrong")

	def testWordsInWeirdOrder(self):
		self._test([[u"naar(binnen)", "jegens", "tot"]], self.word2, "right")

	def testFullNotationAndDontIncludeAnNonObligatoryWord(self):
		self._test([[u"in", u"naar(binnen)"], [u"jegens"]], self.word2, "right")

	def testForItemId(self):
		THE_ID = 342
		for mod in self._mm.mods("active", type="wordsStringChecker"):
			try:
				result = mod.check([("a",)], {
					"questions": [],
					"answers": [("a",)],
					"id": THE_ID,
				})
				self.assertEqual(THE_ID, result["itemId"])
			except Exception:
				print mod
				raise

	def _test(self, givenAnswer, word, output):
		for mod in self._mm.mods("active", type="wordsStringChecker"):
			try:
				result = mod.check(givenAnswer, word)
				self.assertEqual(result["result"], output)
			except Exception:
				print mod
				raise

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.uses = (
			self._mm.mods(type="wordsStringChecker"),
		)

	def enable(self):
		self.TestCase = WordsStringCheckerTestCase
		self.TestCase._mm = self._mm
		self.active = True

	def disable(self):
		self.active = False
		del self.TestCase

def init(moduleManager):
	return TestModule(moduleManager)
