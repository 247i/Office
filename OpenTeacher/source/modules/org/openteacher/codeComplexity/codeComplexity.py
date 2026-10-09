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

import os

class CodeComplexityModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(CodeComplexityModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "codeComplexity"
		self.requires = (
			self._mm.mods(type="execute"),
		)
		self.priorities = {
			"default": -1,
			"code-complexity": 0,
		}

	def enable(self):
		self._modules = next(iter(self._mm.mods(type="modules")))
		self._modules.default("active", type="execute").startRunning.handle(self._run)

		self.active = True

	def _run(self):
		basePath = os.path.normpath(os.path.join(self._mm.modulesPath, ".."))
		self._mm.import_("impl").main(basePath)

	def disable(self):
		self.active = False

		self._modules.default("active", type="execute").startRunning.unhandle(self._run)
		del self._modules

def init(moduleManager):
	return CodeComplexityModule(moduleManager)
