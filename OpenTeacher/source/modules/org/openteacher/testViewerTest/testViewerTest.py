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
import datetime

class TestCase(unittest.TestCase):
	def testCreateTestViewer(self):
		"""Tests if a test viewer can be created without throwing
		   exceptions.

		"""
		if self.mode not in ("all", "testViewer",):
			self.skipTest("Too heavy for this test mode.")
		#an example list with one test inside.
		list = {
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
		}
		for mod in self._mm.mods("active", type="testViewer"):
			mod.createTestViewer(list, dataType="words", test=list["tests"][0])

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="testViewer"),
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
