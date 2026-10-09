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
	@property
	def _mods(self):
		if self.mode not in ("all", "progress-viewer"):
			self.skipTest("Too heavy for this test mode.")
		return self._mm.mods("active", type="progressViewer")

	def testCreateProgressViewerWithEmptyTest(self):
		for mod in self._mods:
			with self.assertRaises(KeyError):
				mod.createProgressViewer({})

	def testCreateProgressViewerWithNormalTest(self):
		for mod in self._mods:
			mod.createProgressViewer({
				"results": [
					{
						"result": "right",
						"givenAnswer": u"one",
						"itemId": 0,
						"active": {
							"start": datetime.datetime.now(),
							"end": datetime.datetime.now(),
						},
					}
				],
				"finished": False,
				"pauses": [
					{
						"start": datetime.datetime.now(),
						"end": datetime.datetime.now(),
					},
				],
			})

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="progressViewer"),
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
