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
	@property
	def _mods(self):
		return self._mm.mods("active", type="languageCodeGuesser")

	def _test(self, langName, code):
		for mod in self._mods:
			self.assertEqual(mod.guessLanguageCode(langName), code)

	def testNativeLanguage(self):
		self._test("Deutsch", "de")

	def testWeirdCasing(self):
		self._test("nEdErLaNdS", "nl")

	def testUnicode(self):
		self._test(u"Français", "fr")

	def testEnglishName(self):
		self._test("Spanish", "es")

	def testFrisian(self):
		#This was the 100th test to be written for OT :D
		self._test("Frysk", "fy")
		self._test("Frisian", "fy")
		self._test("fy", "fy")

	def testNonExistingLanguage(self):
		self._test("jdklfjdf", None)

	def testAlpha2Code(self):
		self._test("es", "es")

	def testGetLanguageName(self):
		for mod in self._mods:
			self.assertEqual(mod.getLanguageName("nl"), "Nederlands")
			self.assertIsNone(mod.getLanguageName("kjdf"))

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="languageCodeGuesser"),
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
