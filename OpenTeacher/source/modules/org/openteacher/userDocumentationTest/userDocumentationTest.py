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
import os
import re

class TestCase(unittest.TestCase):
	@property
	def _mods(self):
		return self._mm.mods(type="userDocumentation")

	def testLinks(self):
		"""Check for dead links (that are specified in the html, but not
		   in the resourcesPath dir.)

		"""
		unique = "this-should-probably-not-be-in-the-output-elsewhere"
		pathRe = re.compile(unique + r"([^\"']+)")
		for mod in self._mods:
			html = mod.getHtml(unique)
			for file in pathRe.findall(html):
				#os.path.basename because there's a / matched.
				path = os.path.join(mod.resourcesPath, os.path.basename(file))
				self.assertTrue(os.path.exists(path))

	def testSwitchingLanguagesDoesntCrash(self):
		"""Just make sure it more or less works."""

		for mod in self._mods:
			mod.getHtml("", lang="C")
			mod.getHtml("", lang="nonexisting")
			mod.getHtml("", lang="nl")

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="userDocumentation"),
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
