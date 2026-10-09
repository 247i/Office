#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2013, Marten de Vries
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
import sys

class TestRunnerModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestRunnerModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "testRunner"
		self.priorities = {
			"test-suite": 0,
			"default": -1,
		}
		self.requires = (
			self._mm.mods(type="execute"),
		)
		self.uses = (
			self._mm.mods(type="test"),
		)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._execute = self._modules.default(type="execute")
		self._execute.startRunning.handle(self._run)

		self.active = True

	def disable(self):
		self.active = False

		self._execute.startRunning.unhandle(self._run)
		del self._execute
		del self._modules

	def _run(self):
		try:
			mode = sys.argv[1]
		except (IndexError, KeyError):
			print >> sys.stderr, "This command needs one command line argument, 'mode', which determines which tests are run. Not sure what to use? Use 'all'."
			return

		testSuite = unittest.TestSuite()
		for module in self._mm.mods("active", type="test"):
			#set the test mode
			module.TestCase.mode = mode
			newTests = unittest.TestLoader().loadTestsFromTestCase(module.TestCase)
			testSuite.addTests(newTests)
		result = unittest.TextTestRunner().run(testSuite)

def init(moduleManager):
	return TestRunnerModule(moduleManager)
