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
import subprocess
import os
import distutils.spawn

class TestCase(unittest.TestCase):
	def _jsFiles(self):
		for root, dirs, files in os.walk(self._mm.modulesPath):
			for file in files:
				path = os.path.join(root, file)
				jsFile = path.endswith(".js") 
				exclude = "jquery" in path or "jsdiff" in path or "admin_files" in path
				if jsFile and not exclude:
					yield path
		
	def testJsFiles(self):
		if self.mode not in ("all", "jshint"):
			self.skipTest("Too heavy for this test mode.")
		if not distutils.spawn.find_executable("jshint"):
			self.skipTest("JSHint not installed")
		p = subprocess.Popen(["jshint"] + list(self._jsFiles()), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		errors = p.communicate()[0].strip()
		self.assertFalse(errors, "\n" + errors)

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"

	def enable(self):
		self.TestCase = TestCase
		self.TestCase._mm = self._mm
		self.active = True

	def disable(self):
		self.active = False
		del self.TestCase

def init(moduleManager):
	return TestModule(moduleManager)
