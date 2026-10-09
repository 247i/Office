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

#Incomplete. Emulatinng jQuery is ugly. But I don't like removing tests,
#so it's here!

import unittest

class CheckableCall(object):
	def __init__(self):
		self.called = False

	def __call__(self, *args, **kwargs):
		self.called = True
		self.args = args
		self.kwargs = kwargs

class TestCase(unittest.TestCase):
	def setUp(self):
		self._evaluators = set()

		browserEmulationCode = """
			var localStorage, $, document, callLater, callNow;
			localStorage = {};
			document = null;
			$ = function () {
				return {
					on: function (name) {}
				};
			};
			callLater = function (callback) {
				callNow = callback;
			}
		"""

		modules = next(iter(self._mm.mods(type="modules")))
		createEvaluator = modules.default("active", type="javaScriptEvaluator").createEvaluator
		for mod in self._mm.mods("active", type="javaScriptApi"):
			js = createEvaluator()
			js.eval(browserEmulationCode)
			js.eval(mod.code)
			self._evaluators.add(js)

	def testIfApiAvailable(self):
		for js in self._evaluators:
			self.assertTrue(js["Api"])

	def testGettingListsWhileOnline(self):
		for js in self._evaluators:
			js.eval("""
				$.getJSON = function (url, success) {
					callLater(success);
					return {
						fail: function () {}
					}
				}
			""")
			func = CheckableCall()
			js["Api"].getLists(func)
			self.assertFalse(func.called)
			js.eval("callNow({result: [{}]})")
			self.assertTrue(func.called)
			self.assertEqual(func.args, ([{}],))

	def testGettingListsWhileOffline(self):
		for js in self._evaluators:
			js.eval("""
				$.getJSON = function (url, success) {
					return {
						fail: function (callback) {
							callLater(callback);
						}
					}
				}
			""")
			func = CheckableCall()
			js["Api"].getLists(func)
			self.assertFalse(func.called)
			js["callNow"]()
			self.assertTrue(func.called)
			self.assertEqual(func.args, ([],))

	def testNewListOnline(self):
		for js in self._evaluators:
			js.eval("""
				$.post = function (url, data) {
					var funcs;
					funcs = {
						always: function (callback) {
							callLater(callback);
							return funcs;
						},
						fail: function (callback) {
							return funcs;
						}
					};
					return funcs;
				};
			""")
			func = CheckableCall()
			js["Api"].newList({}, func)
			self.assertFalse(func.called)
			js["callNow"]()
			self.assertTrue(func.called)
			self.assertEqual(func.args, ())

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="javaScriptEvaluator"),
			self._mm.mods(type="javaScriptApi"),
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
