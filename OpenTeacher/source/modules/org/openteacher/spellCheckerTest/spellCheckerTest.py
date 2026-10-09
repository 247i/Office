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
	@property
	def _mods(self):
		if self.mode not in ("all", "spell-check",):
			self.skipTest("Quite io heavy. Both detecting the language and doing the spell checking.")
		return set(self._mm.mods("active", type="spellChecker"))

	def _englishCheckers(self):
		for mod in self._mods:
			yield mod.createChecker(u"English")

	def _nonExistingLanguageCheckers(self):
		for mod in self._mods:
			yield mod.createChecker(u"Non existing language")

	def testUnexistingLanguageCheckerWithANonExistingWord(self):
		for checker in self._nonExistingLanguageCheckers():
			self.assertTrue(checker.check(u"sdfsdf"))

	def testEnglishWord(self):
		for checker in self._englishCheckers():
			self.assertTrue(checker.check(u"test"))

	def testInvalidWord(self):
		for checker in self._englishCheckers():
			self.assertFalse(checker.check(u"djjdk"))

	def testSplit(self):
		for checker in self._englishCheckers():
			self.assertEqual(checker.split("what's new?'"), [
				("what's", 0),
				("new", 7),
			])

	def testSplitNonExistingLanguage(self):
		for checker in self._nonExistingLanguageCheckers():
			self.assertEqual(checker.split(u"just'tésting"), [
				(u"just", 0),
				(u"tésting", 5),
			])

	def testSplitNonExistingLanguageWithDoubleSeparator(self):
		for checker in self._nonExistingLanguageCheckers():
			self.assertEqual(checker.split(u"een, uno"), [
				(u"een", 0),
				(u"uno", 5),
			])

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="spellChecker"),
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
