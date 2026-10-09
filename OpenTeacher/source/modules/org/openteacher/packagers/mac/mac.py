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

import sys
import shutil
import platform
import subprocess

class MacPackagerModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(MacPackagerModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "macPackager"
		self.requires = (
			self._mm.mods(type="pyinstallerInterface"),
			self._mm.mods(type="execute"),
		)
		self.priorities = {
			"package-mac": 0,
			"default": -1,
		}

	def _run(self):
		try:
			dmgPath = sys.argv[1]
		except IndexError:
			sys.stderr.write("Please specify the resultive file name as last command line parameter. (e.g. openteacher.dmg)\n")
			return
		#build to .app
		appDir = self._pyinstaller.build()

		#make dmg
		subprocess.call(["hdiutil", "create", dmgPath, "-srcfolder", appDir])

	def enable(self):
		if platform.system() != "Darwin":
			#remain inactive
			return
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._pyinstaller = self._modules.default("active", type="pyinstallerInterface")

		self._modules.default(type="execute").startRunning.handle(self._run)

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self._pyinstaller

def init(moduleManager):
	return MacPackagerModule(moduleManager)
