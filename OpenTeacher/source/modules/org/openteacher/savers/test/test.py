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
import tempfile
import copy
import os
import datetime
import shutil
import contextlib

MODES = ("all", "save")

class Lesson(object):
	def __init__(self, list=None, resources=None):
		self.list = list or {}
		self.resources = resources or {}

class TestCase(unittest.TestCase):
	def _testSavingType(self, type, lesson):
		if self.mode not in MODES:
			self.skipTest("This tests isn't run in this mode.")
		for saver in self._mm.mods("active", type="save"):
			if not type in saver.saves:
				continue

			lessonCopy = copy.deepcopy(lesson)

			#save lesson
			for ext in saver.saves[type]:
				fd, path = tempfile.mkstemp(".%s" % ext)
				os.close(fd)
				saver.save(type, lesson, path)

				#file should exist after saving.
				self.assertTrue(os.path.isfile(path))
				#and it should not be empty.
				self.assertTrue(os.path.getsize(path) > 0)

				os.remove(path)
				with contextlib.ignored(OSError):
					#html saver
					shutil.rmtree(path + ".resources")

			try:
				self.assertEqual(lesson.list, lessonCopy.list)
				self.assertEqual(lesson.resources, lessonCopy.resources)
			except AssertionError:
				print "%s modified the lesson object passed to save(), which isn't allowed. More info:" % saver
				raise

	def testSavingMedia(self):
		metadata = next(iter(self._mm.mods("active", type="metadata"))).metadata
		self._testSavingType("media", Lesson({
			"items": [
				{
					"remote": True, 
					"name": "http://openteacher.org/", 
					"question": "a", 
					"filename": "http://openteacher.org/", 
					"answer": "b", 
					"id": 0
				}, 
				{
					"remote": False, 
					"name": "openteacher-icon.png", 
					"question": "", 
					"filename": metadata["iconPath"], 
					"answer": "", 
					"id": 1
				}
			],
			"tests": []
		}, {}))
		#FIXME: see comment on resources in the .otmd saver file.

	def testSavingTopo(self):
		metadata = next(iter(self._mm.mods("active", type="metadata"))).metadata
		self._testSavingType("topo", Lesson({
			"items": [
				{
					"y": 364,
					"x": 399,
					"id": 0,
					"name": "Test",
				},
			],
			"tests": [
				{
					"finished": True,
					"results": [
						{
							"itemId": 0,
							"active": {
								"start": datetime.datetime.now(),
								"end": datetime.datetime.now(),
							},
							"result": "wrong",
						}
					],
					"pauses": [
					],
				},
				{
					"finished": True,
					"results": [
						{
							"itemId": 0,
							"active": {
								"start": datetime.datetime.now(),
								"end": datetime.datetime.now(),
							},
							"result": "right",
						}
					],
					"pauses": [
					],
				},
			],
		}, {
			"mapPath": metadata["iconPath"],
			"mapScreenshot": metadata["iconPath"],
		}))

	def testSavingWords(self):
		self._testSavingType("words", Lesson({
			"title": u"My títle",
			"questionLanguage": u"Varyíng",
			"answerLanguage": u"Va®ying too. Some úñí©óðé.",
			"items": [
				{
					"id": 0,
					"questions": [(u"eén",), (u"uno", u"un",)],
					"answers": [(u"twee", u"deux"), ("two", "zwei")],
					"created": datetime.datetime.now(),
				},
				{
					"id": 1,
					"questions": [(u"drie",)],
					"answers": [(u"three",)],
				}
			],
			"tests":[
				{
					"finished": True,
					"results": [
						{
							"itemId":0,
							"active": {
								"start": datetime.datetime.now(),
								"end": datetime.datetime.now(),
							},
							"result": "right",
							"givenAnswer": "one",
						},
						{
							"itemId": 1,
							"active": {
								"start": datetime.datetime.now(),
								"end": datetime.datetime.now(),
							},
							"result": "wrong",
							"givenAnswer": "ttwo",
						},
					],
					"pauses": [
					],
				},
			],
		}))

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="save"),
			#re-using the icon as test topo map to save a bit of space.
			self._mm.mods(type="metadata"),
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
