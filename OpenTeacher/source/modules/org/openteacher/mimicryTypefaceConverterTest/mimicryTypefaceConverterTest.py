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

class TestCase(unittest.TestCase):
	"""Some basic tests."""

	def _test(self, input, assertedOutput):
		for mod in self._mm.mods("active", type="mimicryTypefaceConverter"):
			realOutput = mod.convert(*input)
			self.assertEqual(assertedOutput, realOutput)

	def testNonExistingFont(self):
		self._test([u"d m 9038m4edreolwi4i832 disfdhoiw", u"tést"], u"tést")

	def testGreek(self):
		self._test([u"Greek", u"a b"], u"α β")

	def testSymbol(self):
		self._test([u"Symbol", u"a b D"], u"α β Δ")

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="mimicryTypefaceConverter"),
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
