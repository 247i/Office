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

class JavascriptParserModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(JavascriptParserModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "wordsStringParser"
		self.javaScriptImplementation = True
		self.requires = (
			self._mm.mods(type="javaScriptEvaluator"),
		)
		self.priorities = {
			"default": 20,
		}

	def parse(self, *args, **kwargs):
		"""Parses a string like:

			   1. in, op, bij 2. tijdens

		   into the following representation (used by OpenTeacher
		   internally):

			   [[u"in", u"op", u"bij"], [u"tijdens"]]

		   See the tests for this module for more examples.

		"""
		return self._js["parse"](*args, **kwargs)

	def enable(self):
		with open(self._mm.resourcePath("parser.js")) as f:
			self.code = f.read()

		modules = next(iter(self._mm.mods(type="modules")))
		self._js = modules.default("active", type="javaScriptEvaluator").createEvaluator()
		self._js.eval(self.code)

		self.active = True

	def disable(self):
		self.active = False

		del self.code
		del self._js

def init(moduleManager):
	return JavascriptParserModule(moduleManager)
