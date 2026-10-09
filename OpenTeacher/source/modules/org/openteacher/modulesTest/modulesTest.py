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
import uuid

class TestCase(unittest.TestCase):
	"""Test the really critical behaviour of the modules module.
	   (all else is impossible to test without adding all kinds of mock
	   modules, but this is a good start)"""

	def testDefault(self):
		for mod in self._mm.mods(type="modules"):
			a = mod.default(type="test", name="modulesTest")
			self.assertEquals(a, self.thisMod)

	def testDefaultUnexisting(self):
		for mod in self._mm.mods(type="modules"):
			with self.assertRaises(IndexError):
				#random, no chance this property really exist...
				mod.default(uuid=uuid.uuid4())
			with self.assertRaises(IndexError):
				#same here.
				mod.default(str(uuid.uuid4()))

	def testIfInSort(self):
		for mod in self._mm.mods(type="modules"):
			a = mod.sort(type="test")
			self.assertIn(self.thisMod, a)

	def testModuleManagerImport(self):
		"""Test for the module manager."""
		pyMod = self._mm.import_("fileToImport")
		self.assertEquals(pyMod.test, "sure")

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.name = "modulesTest"
		self.uses = (
			self._mm.mods(type="modules"),
		)

	def enable(self):
		self.TestCase = TestCase
		self.TestCase._mm = self._mm
		self.TestCase.thisMod = self
		self.active = True

	def disable(self):
		self.active = False
		del self.TestCase

def init(moduleManager):
	return TestModule(moduleManager)
