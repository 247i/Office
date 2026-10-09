#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2012-2013, Marten de Vries
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
import copy

class TestCase(unittest.TestCase):
	def setUp(self):
		self._list = {
			"tests": [],
			"items": [
				{
					"id": 0,
					"questions": [["een"]],
					"answers": [["one"]],
				},
				{
					"id": 1,
					"questions": [["twee"]],
					"answers": [["two"]],
				},
			],
		}

	@property
	def _mods(self):
		return (
			set(self._mm.mods("active", type="lessonType")) |
			set(self._mm.mods("active", type="javaScriptLessonType"))
		)

	def testEmptyIndexes(self):
		def newItem(item):
			self.assertTrue(False, msg="newItem should not be called when an empty indexes list is passed.")# pragma: no cover
		for mod in self._mods:
			lessonType = mod.createLessonType(self._list, [])
			lessonType.newItem.handle(newItem)
			lessonType.start()

	def testItemsInList(self):
		def newItem(item):
			self.assertIn(item, self._list["items"])
			lessonType.setResult({"result": "right", "itemId": item["id"]})

		for mod in self._mods:
			lessonType = mod.createLessonType(self._list, range(len(self._list)))
			lessonType.newItem.handle(newItem)
			lessonType.start()

	def testLessonDoneCalled(self):
		for mod in self._mods:
			def newItem(item):
				lessonType.setResult({"result": "right", "itemId": item["id"]})

			def lessonDone():
				self.assertTrue(usedList["tests"][-1]["finished"])
				data["called"] = True

			data = {"called": False}
			usedList = copy.deepcopy(self._list)
			lessonType = mod.createLessonType(usedList, range(len(usedList)))
			lessonType.newItem.handle(newItem)
			lessonType.lessonDone.handle(lessonDone)
			lessonType.start()
			self.assertTrue(data["called"], msg="Lesson should call lessonDone() before stopping sending next items.")

	def testGlobalNewItem(self):
		def func(item):
			pass
		for mod in self._mm.mods("active", type="lessonType"):
			#the JS mod isn't meant to be used on the desktop, so it
			#doesn't need to have this event.
			mod.newItem.handle(func)

	def testSkip(self):
		for mod in self._mods:
			lessonType = mod.createLessonType(self._list, range(len(self._list)))
			lessonType.start()
			lessonType.skip()

	def testAddPause(self):
		for mod in self._mods:
			lessonType = mod.createLessonType(self._list, range(len(self._list)))
			lessonType.start()
			lessonType.addPause({
				"start": datetime.datetime.now(),
				"end": datetime.datetime.now(),
			})

	def testProperties(self):
		for mod in self._mods:
			lessonType = mod.createLessonType(self._list, range(len(self._list)))
			lessonType.start()
			self.assertIsInstance(lessonType.totalItems, int)
			self.assertIsInstance(lessonType.askedItems, int)

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.uses = (
			self._mm.mods(type="lessonType"),
			self._mm.mods(type="javaScriptLessonType"),
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
