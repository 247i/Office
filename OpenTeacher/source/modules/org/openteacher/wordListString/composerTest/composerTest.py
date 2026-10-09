#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2012, Marten de Vries
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
import datetime

class TestCase(unittest.TestCase):
	def _test(self, input, expectedOutput):
		for mod in self._mm.mods("active", type="wordListStringComposer"):
			output = mod.composeList({
				"resources": {},
				"list": {
					"items": input,
					"tests": [],
				}
			})
			self.assertEqual(output, expectedOutput)

	def testNoItems(self):
		for mod in self._mm.mods("active", type="wordListStringComposer"):
			output = mod.composeList({
				"resources": {},
				"list": {},
			})
			self.assertEqual(output, "\n")

	def testEmpty(self):
		#one blank line
		self._test([], "\n")

	def testEqualSeparated(self):
		self._test(
			[{
				"id": 0,
				"questions": [(u"a",)],
				"answers": [(u"b",)],
			}],
			u"a = b\n"
		)

	def testExtraAttributes(self):
		"""And of course, that type is non-JSON serializable to
		   reproduce a bug that once happened. ;)

		"""
		self._test(
			[{
				"id": 0,
				"questions": [(u"a",)],
				"answers": [(u"b",)],
				"created": datetime.datetime.now(),
			}],
			u"a = b\n"
		)

	def testEscaping(self):
		self._test(
			[{
				"id": 0,
				"questions": [(u"1 + 2 = 3",)],
				"answers": [("maths",)],
			}],
			"1 + 2 \= 3 = maths\n"
		)

	def testFalseId(self):
		"""Should just ignore the id like is done everywhere"""
		self._test(
			[{
				"id": 34,
				"questions": [("a",)],
				"answers": [("b",)],
			}],
			"a = b\n"
		)

	def testMissingQuestionsOrAnswers(self):
		"""Should crash one way or another. Feel free to add other
		   exceptions if your implementation requires that, as long as
		   it throws something to alert the developer.

		"""
		with self.assertRaises((Exception, KeyError)):
			self._test(
				[{
					"id": 0,
					"answers": [],
				}],
				None
			)

		with self.assertRaises(Exception):
			self._test(
				[{
					"id": 0,
					"questions": [],
				}],
				None
			)

	def testNonAscii(self):
		self._test(
			[{
				"id": 0,
				"questions": [(u"é",)],
				"answers": [(u"à",)],
			}],
			u"é = à\n",
		)

	def testEmptyValues(self):
		self._test(
			[
				{"id": 0, "questions": [("een",)], "answers": []},
				{"id": 1, "questions": [], "answers": [("one",)]},
			],
			"een = \n = one\n"
		)

	def testRealWorldExample(self):
		self._test(
			[
				{
					"id": 0,
					"questions": [("een",)],
					"answers": [("one", "uno"), ("a",)]
				},
				{"id": 1, "questions": [("twee",)], "answers": [("two",)]},
				{"id": 2, "questions": [("drie",)], "answers": [("three",)]},
				{"id": 3, "questions": [("vier",)], "answers": [("four",)]},
				{"id": 4, "questions": [("vijf",)], "answers": [("five",)]},
				{
					"id": 5,
					"questions": [("3 \= 2 + 1",)],
					"answers": [("three equals two plus one",)],
				},
			],
			"""
een = 1. one, uno 2. a
twee = two
drie = three
vier = four
vijf = five
3 \= 2 + 1 = three equals two plus one
			""".strip() + "\n"
		)

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="wordListStringComposer"),
		)

	def enable(self):
		self.TestCase = TestCase
		self.TestCase._mm = self._mm
		self.active = True

	def disable(self):
		self.active = False
		del self.TestCase

def init(moduleManager):
	return TestModule(moduleManager)
