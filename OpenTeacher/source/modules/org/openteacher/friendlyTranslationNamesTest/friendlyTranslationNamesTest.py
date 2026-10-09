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
import uuid

class TestCase(unittest.TestCase):
	def _test(self, key, value):
		for mod in self._mm.mods("active", type="friendlyTranslationNames"):
			self.assertEqual(mod.friendlyNames[key], value)

	def testC(self):
		"""The value for C needs to be fixed."""

		self._test("C", "I speak English")

	def testFallback(self):
		"""When a value is passed that is unknown, it should be
		   returned. It's the only value that still makes a bit of
		   sense.

		"""
		#no chance this is a language code.
		unknown = uuid.uuid4()
		self._test(unknown, unknown)

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="friendlyTranslationNames"),
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
