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
import math
import uuid

class TestCase(unittest.TestCase):
	"""Tests for the authors module."""

	def setUp(self):
		for mod in self._mm.mods("active", type="authors"):
			#should clear state between runs
			mod.disable()
			mod.enable()

	def testAdding(self):
		for mod in self._mm.mods("active", type="authors"):
			mod.registerAuthor("some work", "name")
			self.assertIn((u"some work", u"name"), mod.registeredAuthors)

	def testAddingMultipleTimes(self):
		"""Persons added twice should only appear once."""

		for mod in self._mm.mods("active", type="authors"):
			#never seen somebody called 3.1415...?
			mod.registerAuthor("Being great with circles", math.pi)
			mod.registerAuthor("Being great with circles", math.pi)

			item = (u"Being great with circles", str(math.pi))
			self.assertEqual(list(mod.registeredAuthors).count(item), 1)

	def testAddingMultipleTimesAndRemoving(self):
		"""Persons added multiple times but that are removed only once
		   should still be there.

		"""
		for mod in self._mm.mods("active", type="authors"):
			remove1 = mod.registerAuthor("Being great with circles", math.pi)
			remove2 = mod.registerAuthor("Being great with circles", math.pi)

			item = (u"Being great with circles", str(math.pi))

			remove1()
			self.assertEqual(list(mod.registeredAuthors).count(item), 1)

			remove2()
 			self.assertEqual(list(mod.registeredAuthors).count(item), 0)

	def testModifyingMods(self):
		"""The registeredAuthors attribute should not expose the
		   internal data structure.

		"""
		for mod in self._mm.mods("active", type="authors"):
			#pretty sure it's unique
			value = uuid.uuid4()
			#ATTENTION: if you don't use a set as return value, feel
			#free to change this to something more generic. As long as
			#the principe (returning copies, not the actual storage
			#object) is adheared to.
			mod.registeredAuthors.add(value)
			self.assertNotIn(value, mod.registeredAuthors)

	def testNotEasyUnicodifyable(self):
		"""Data should be unicode or easily unicodifyable."""

		for mod in self._mm.mods("active", type="authors"):
			with self.assertRaises(UnicodeDecodeError):
				mod.registerAuthor("a", "é".encode("UTF-8"))

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="authors"),
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
