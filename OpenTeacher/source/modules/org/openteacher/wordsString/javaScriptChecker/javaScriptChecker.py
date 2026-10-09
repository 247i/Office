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

class JavascriptCheckerModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(JavascriptCheckerModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "wordsStringChecker"
		self.javaScriptImplementation = True
		self.requires = (
			self._mm.mods(type="javaScriptEvaluator"),
		)
		self.priorities = {
			"default": 20,
		}

	def check(self, *args, **kwargs):
		"""Checks if a `givenAnswer` is similar enough to the `answer`
		   to be seen as correct. For examples of what's correct and
		   what's not, please see the tests for this module.

		"""
		return self._js["check"](*args, **kwargs)

	def enable(self):
		modules = set(self._mm.mods(type="modules")).pop()

		with open(self._mm.resourcePath("checker.js")) as f:
			self.code = f.read()
		self._js = modules.default("active", type="javaScriptEvaluator").createEvaluator()
		self._js.eval(self.code)

		self.active = True

	def disable(self):
		self.active = False

		del self._js
		del self.code

def init(moduleManager):
	return JavascriptCheckerModule(moduleManager)
