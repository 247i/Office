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

class TestCase(unittest.TestCase):
	"""A test that specifies how the interface of a character table
	   module ('chars') should be.

	"""
	def testAmountOfColumns(self):
		"""It should have 6 columns"""

		for mod in self._mm.mods("active", type="chars"):
			for row in mod.data:
				self.assertEquals(len(row), 6)

	def testRowLengthNotZero(self):
		"""It should have rows"""
		for mod in self._mm.mods("active", type="chars"):
			self.assertFalse(len(mod.data) == 0)

	def testUpdated(self):
		"""If a mod allows notification on update, check if it works."""

		def func():
			data["called"] = True

		for mod in self._mm.mods("active", type="chars"):
			data = {"called": False}
			if not hasattr(mod, "updated"):
				continue
			mod.updated.handle(func)
			mod.sendUpdated()
			self.assertTrue(data["called"])

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="chars"),
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
