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
		if self.mode not in ("settingsWidget", "all"):
			self.skipTest("Too heavy for this mode.")
		return self._mm.mods(type="settingsWidget")

	def _settingsWidgetMod(self, widgetType):
		return next(iter(self._mm.mods(type="settingsWidget", widgetType=widgetType)))

	def testWidgetType(self):
		for mod in self._mods:
			self.assertTrue(mod.widgetType)

	def testBoolean(self):
		self._settingsWidgetMod("boolean").createWidget({"value": True})

	def testCharacterTable(self):
		self._settingsWidgetMod("character_table").createWidget({
			"value": [[
				u"a", u"b", u"c", u"ð", u"é"
			]]
		})

	def testLanguage(self):
		self._settingsWidgetMod("language").createWidget({"value": "C"})

	def testLongText(self):
		self._settingsWidgetMod("long_text").createWidget({"value": "a\nb\nc"})

	def testMultiOption(self):
		self._settingsWidgetMod("multiOption").createWidget({
			"options": [
				("label", "data",),
				("label2", "data2",),
				("label3", "data3",),
			],
			"value": ["data", "data3"],
		})

	def testNumber(self):
		self._settingsWidgetMod("number").createWidget({
			"value": 42,
		})

	def testOption(self):
		self._settingsWidgetMod("option").createWidget({
			"options": [
				("label", "data",),
				("label2", "data2",),
				("label3", "data3",),
			],
			"value": "data2",
		})

	def testPassword(self):
		self._settingsWidgetMod("password").createWidget({
			"value": "secret",
		})

	def testProfile(self):
		self._settingsWidgetMod("profile").createWidget({"value": "words-only"})

	def testShortText(self):
		self._settingsWidgetMod("short_text").createWidget({"value": "abc"})

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="settingsWidget"),
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
