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

import unittest
import copy

class TestCase(unittest.TestCase):
	_mods = property(lambda self: self._mm.mods("active", type="merger", dataType="words"))

	def testNoItemsAndTests(self):
		for mod in self._mods:
			result = mod.merge({"list": {}}, {"list": {}})
			self.assertEqual(result, {"list": {}})

	def testCompletelyEmptyLesson(self):
		for mod in self._mods:
			result = mod.merge({}, {})
			self.assertEqual(result, {})

	def testMerge(self):
		for mod in self._mods:
			baseLesson = {
				"resources": {},
				"list": {
					"title": "a",
					"questionLanguage": "b",
					"answerLanguage": "c",
					"items": [
						{"answers": []},
					],
					"tests": [
						{"finished": True}
					],
				}
			}
			otherLesson = {
				"resources": {},
				"list": {
					"title": "b",
					"questionLanguage": "c",
					"answerLanguage": "d",
					"items": [
						{"questions": []},
					],
					"tests": [
						{}
					]
				}
			}

			baseLessonCopy = copy.deepcopy(baseLesson)
			otherLessonCopy = copy.deepcopy(otherLesson)

			result = mod.merge(baseLesson, otherLesson)

			self.assertEqual(baseLesson, baseLessonCopy)
			self.assertEqual(otherLesson, otherLessonCopy)

			self.assertEqual(result, {
				"resources": {},
				"list": {
					"title": "a",
					"questionLanguage": "b",
					"answerLanguage": "c",
					"items": [
						{"answers": []},
						{"questions": []},
					],
					"tests": [
						{"finished": True},
						{},
					]
				}
			})

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="merger", dataType="words"),
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
