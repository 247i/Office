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
import os
import glob

class TestCase(unittest.TestCase):
	def testFilesWithTranslations(self):
		"""Test if all files specified in filesWithTranslations exist.

		"""
		for mod in self._mm.mods:
			if not hasattr(mod, "filesWithTranslations"):
				continue
			directory = os.path.dirname(mod.__class__.__file__)
			files = mod.filesWithTranslations
			for file in files:
				path = os.path.join(directory, file)
				self.assertTrue(os.path.exists(path), msg="Mod %s's filesWithTranslations contains %s, but that doesn't exist." % (mod.__class__.__file__, file))


	def testPotFiles(self):
		"""Test if every module with a translations dir has a .pot file
		   in place, which is required.

		"""
		potFiles = set()
		for mod in self._mm.mods:
			base = os.path.dirname(mod.__class__.__file__)
			dir = os.path.join(base, "translations")
			if not os.path.exists(dir):
				continue
			matches = glob.glob(os.path.join(dir, "*.pot"))

			self.assertEqual(len(matches), 1, msg="No pot file at %s" % base)
			self.assertNotIn(matches[0], potFiles)
			potFiles.add(matches[0])

	def testLanguageChanged(self):
		"""Tests if:
		   1. translator mods have a working sendLanguageChanged
		      method.
		   2. modules subscribing to events offered by the translator
		      modules are doing that correctly (i.e. don't crash when
		      the actual events are send.)

		"""
		if self.mode not in ("all", "translation"): # pragma: no cover
			self.skipTest("Too heavy for this test mode.")
		for mod in self._mm.mods("active", type="translator"):
			mod.sendLanguageChanged()

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.uses = (
			self._mm.mods(type="translator"),
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
