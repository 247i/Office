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

class JavascriptComposerModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(JavascriptComposerModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "wordsStringComposer"
		self.javaScriptImplementation = True
		self.requires = (
			self._mm.mods(type="javaScriptEvaluator"),
		)
		self.priorities = {
			"default": 20,
		}

	def compose(self, *args, **kwargs):
		"""Takes an internal representation of a word as used by
		   OpenTeacher, e.g.:
			   [[u"in", u"op", u"bij"], [u"tijdens"]]

		   ands converts it into a human-readable equivalent, in this
		   case:
		   
			   1. in, op, bij 2. tijdens

		   See the tests for this module for more examples.

		"""
		return self._js["compose"](*args, **kwargs)

	def enable(self):
		with open(self._mm.resourcePath("composer.js")) as f:
			self.code = f.read()

		modules = next(iter(self._mm.mods(type="modules")))
		self._js = modules.default("active", type="javaScriptEvaluator").createEvaluator()
		self._js.eval(self.code)

		self.active = True

	def disable(self):
		self.active = False

		del self._js
		del self.code

def init(moduleManager):
	return JavascriptComposerModule(moduleManager)
