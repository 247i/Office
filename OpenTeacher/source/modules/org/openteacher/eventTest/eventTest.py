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
		return (
			set(self._mm.mods(type="event")) |
			set(self._mm.mods("active", type="javaScriptEvent"))
		)

	def testSendEmptyEvent(self):
		for e in self._mods:
			a = e.createEvent()
			self.assertIsNone(a.send())

	def testEvent(self):
		for e in self._mods:
			def callback():
				called["true"] = True
				return 1
			called = {"true": False}
			a = e.createEvent()
			a.handle(callback)
			self.assertIsNone(a.send())
			self.assertTrue(called["true"])

	def testMultipleEvents(self):
		for e in self._mods:
			def callback():
				counter["value"] += 1
			counter = {"value": 0}

			a = e.createEvent()
			a.handle(callback)
			a.handle(callback) #add a second time, should fail silently
			a.send()
			self.assertEquals(counter["value"], 1) #test that

	def testAddRemoveEvent(self):
		callback = lambda: None
		callback2 = lambda: None
		for e in self._mods:
			a = e.createEvent()
			a.handle(callback)
			a.handle(callback)
			self.assertIsNone(a.unhandle(callback))
			with self.assertRaises(KeyError):
				a.unhandle(callback)

	def testArgs(self):
		testArgs = (1, "s",)
		def callback(*args):
			self.assertEquals(args, testArgs)

		for e in self._mods:
			a = e.createEvent()
			a.handle(callback)
			a.send(*testArgs)

	def testKwargs(self):
		testKwargs = {"a":1, "b": 2}
		def callback(**kwargs):
			self.assertEquals(kwargs, testKwargs)

		for e in self._mods:
			a = e.createEvent()
			a.handle(callback)
			a.send(**testKwargs)

	def testRegisteringHandlerInsideHandler(self):
		"""Expected behaviour is that it'll not call the newly
		   registered handler, but that it won't crash either."""
		def callback():
			a.handle(callback2)

		def callback2():
			self.assertTrue(False, "Shouldn't get here...") # pragma: no cover

		for e in self._mods:
			a = e.createEvent()
			a.handle(callback)
			a.send()

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.uses = (
			self._mm.mods(type="event"),
			self._mm.mods(type="javaScriptEvent"),
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
