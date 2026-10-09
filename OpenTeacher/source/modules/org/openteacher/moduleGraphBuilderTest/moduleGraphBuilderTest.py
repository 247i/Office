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
import tempfile
import os

class TestCase(unittest.TestCase):
	def testModuleGraphBuilder(self):
		if self.mode not in ("all", "module-graph-builder"): # pragma: no cover
			self.skipTest("Too heavy for this test mode.")
		for mod in self._mm.mods("active", type="moduleGraphBuilder"):
			fd, path = tempfile.mkstemp(".svg")
			os.close(fd)
			mod.buildModuleGraph(path)
			#the file must be created, and not empty. Should be enough
			#for now.
			self.assertTrue(os.path.isfile(path))
			try:
				self.assertTrue(os.path.getsize(path) > 0)
			finally:
				#remove the file again
				os.remove(path)

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="moduleGraphBuilder"),
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
