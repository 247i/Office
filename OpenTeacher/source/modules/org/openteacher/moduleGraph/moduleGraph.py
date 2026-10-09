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

import sys

class ModuleGraphModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(ModuleGraphModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "moduleGraph"

		self.requires = (
			self._mm.mods(type="execute"),
			self._mm.mods(type="moduleGraphBuilder"),
		)
		self.priorities = {
			"default": -1,
			"module-graph": 0,
		}

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._modules.default(type="execute").startRunning.handle(self.run)

		self.active = True

	def run(self):
		try:
			outputPath = sys.argv[1]
		except IndexError:
			sys.stderr.write("Please specify an image path to output to as last command line argument.\n")
			return

		mgb = self._modules.default("active", type="moduleGraphBuilder")
		mgb.buildModuleGraph(outputPath)

	def disable(self):
		self.active = False

		del self._modules

def init(moduleManager):
	return ModuleGraphModule(moduleManager)
