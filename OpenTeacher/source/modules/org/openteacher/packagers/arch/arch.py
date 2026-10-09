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

import subprocess
import os
import sys
import shutil
import glob

class ArchPackagerModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(ArchPackagerModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "archPackager"
		self.requires = (
			self._mm.mods(type="sourceWithSetupSaver"),
			self._mm.mods(type="metadata"),
			self._mm.mods(type="execute"),
		)
		self.priorities = {
			"package-arch": 0,
			"default": -1,
		}

	def enable(self):
		global pyratemp
		try:
			import pyratemp
		except ImportError:
			return #leave disabled
		if not os.path.isfile("/usr/bin/pacman"):
			return #arch linux only module, remain inactive
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._metadata= self._modules.default("active", type="metadata").metadata
		self._modules.default(type="execute").startRunning.handle(self._run)

		self.active = True

	def _manPagesSourceAndDestination(self, sourcePath):
		basePath = os.path.join(sourcePath, "linux")
		for file in glob.glob(os.path.join(basePath, "*.1")):
			filename = os.path.basename(file)
			nameWithoutExtension = os.path.splitext(filename)[0]
			langCode = os.path.splitext(nameWithoutExtension)[1].strip(".")
			yield filename, os.path.normpath("/usr/share/man/%s/man1" % langCode)

	def _run(self):
		try:
			package_release = sys.argv[1]
			path = sys.argv[2]
		except IndexError:
			sys.stderr.write("Please specify a package release version and a path ending in .pkg.tar.xz to save the resulting arch package to as the last command line arguments.\n")
			return
		sourcePath = self._modules.default("active", type="sourceWithSetupSaver").saveSource()

		with open(os.path.join(sourcePath, "PKGBUILD"), "w") as f:
			templ = pyratemp.Template(filename=self._mm.resourcePath("PKGBUILD.templ"))
			data = {
				"package_release": package_release,
				"manpages": self._manPagesSourceAndDestination(sourcePath),
			}
			data.update(self._metadata)
			f.write(templ(**data))

		cwd = os.getcwd()
		os.chdir(sourcePath)
		subprocess.check_call(["makepkg"])
		os.chdir(cwd)

		shutil.copy(
			glob.glob(os.path.join(sourcePath, "*.pkg.tar.xz"))[0],
			path
		)

	def disable(self):
		self.active = False

		del self._modules
		del self._metadata

def init(moduleManager):
	return ArchPackagerModule(moduleManager)
