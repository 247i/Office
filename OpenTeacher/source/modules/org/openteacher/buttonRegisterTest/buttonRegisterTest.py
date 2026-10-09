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

MODES = ("all", "buttonRegister",)

class TestCase(unittest.TestCase):
	"""Tests for the buttonRegister module"""

	def testAddButton(self):
		"""Test if the addButton event works"""

		def func(myB):
			data["myB"] = myB
		for mod in self._mm.mods("active", type="buttonRegister"):
			data = {}
			mod.addButton.handle(func)
			b = mod.registerButton("category")
			self.assertEqual(b, data["myB"])

	def testRemoveButton(self):
		"""Test if the removeButton event works"""

		def func(myB):
			data["myB"] = myB
		for mod in self._mm.mods("active", type="buttonRegister"):
			data = {}
			mod.removeButton.handle(func)
			b = mod.registerButton("category")
			mod.unregisterButton(b)
			self.assertEqual(b, data["myB"])

	def testRegisterButton(self):
		"""Test if the button interface is correct"""

		def checkEvent(item):
			self.assertIsNotNone(item.handle)
			self.assertIsNotNone(item.unhandle)
			self.assertIsNotNone(item.send)

		for mod in self._mm.mods("active", type="buttonRegister"):
			b = mod.registerButton("myCategory")
			self.assertEqual(b.category, "myCategory")
			checkEvent(b.clicked)
			checkEvent(b.changeText)
			checkEvent(b.changePriority)
			checkEvent(b.changeIcon)
			checkEvent(b.changeSize)

	def testClickingRegisteredButtons(self):
		if self.mode not in MODES:
			return
		for button in self._buttons:
			button.clicked.send()

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="buttonRegister"),
		)

	def _addButton(self, button):
		self.TestCase._buttons.add(button)

	def _removeButton(self, button):
		self.TestCase._buttons.remove(button)

	def enable(self):
		self.TestCase = TestCase
		self.TestCase._mm = self._mm
		self.TestCase._buttons = set()

		for mod in self._mm.mods(type="buttonRegister"):
			mod.addButton.handle(self._addButton)
			mod.removeButton.handle(self._removeButton)

		self.active = True

	def disable(self):
		self.active = False

		del self.TestCase
		for mod in self._mm.mods(type="buttonRegister"):
			mod.addButton.unhandle(self._addButton)
			mod.removeButton.unhandle(self._removeButton)

def init(moduleManager):
	return TestModule(moduleManager)
