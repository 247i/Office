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
import subprocess
import os
import shutil
import glob
import platform

class DebianPackagerModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(DebianPackagerModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "debianPackager"
		self.requires = (
			self._mm.mods(type="sourceWithSetupSaver"),
			self._mm.mods(type="metadata"),
			self._mm.mods(type="execute"),
		)
		self.priorities = {
			"package-debian": 0,
			"default": -1,
		}

	def enable(self):
		if not platform.linux_distribution()[0] in ("Debian", "Ubuntu"):
			return #debian-based only module, remain inactive
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._metadata = self._modules.default("active", type="metadata").metadata
		self._modules.default(type="execute").startRunning.handle(self._run)

		self.active = True

	def _run(self):
		try:
			buildNumber = sys.argv[1]
			path = sys.argv[2]
			cExtensions = sys.argv[3] == "true"
		except IndexError:
			sys.stderr.write("Please specify 1) a debian build number, 2) a path for the deb file (ending in .deb) and 3) 'true' to enable c extensions and 'false' to disable c extensions as the last command line arguments.\n")
			return

		sourceWithSetupSaver = self._modules.default("active", type="sourceWithSetupSaver")
		if cExtensions:
			sourcePath = sourceWithSetupSaver.saveSourceWithCExtensions()
		else:
			sourcePath = sourceWithSetupSaver.saveSource()
		packageName = self._metadata["name"].lower()

		oldCwd = os.getcwd()
		os.chdir(sourcePath)
		with open("stdeb.cfg", "w") as f:
			f.write("""
[DEFAULT]
Package: {package}
Section: misc
XS-Python-Version: >= 2.6
Depends: python-qt4, python-qt4-phonon, python-qt4-gl, espeak, python-chardet, tesseract-ocr, python-enchant, ibus-qt4
			""".strip().format(
				package=packageName
			))
		subprocess.check_call([
			sys.executable or "python",
			"setup.py",
			"--command-packages=stdeb.command", "sdist_dsc",
			"--force-buildsystem", "False",
			#e.g. 0openteachermaintainers1
			"--debian-version", "0" + self._metadata["email"].split("@")[0] + buildNumber,
		])
		os.chdir("deb_dist/%s-%s" % (
			packageName,
			self._metadata["version"],
		))
		with open("debian/%s.manpages" % packageName, "w") as f:
			#this asserts there are only manpages of category 1. Which
			#is currently just fine.
			f.write("\n".join(glob.glob("linux/*.1")))
		subprocess.check_call(["dpkg-buildpackage", "-rfakeroot", "-uc", "-us",])
		os.chdir(oldCwd)
		shutil.copy(
			glob.glob(os.path.join(sourcePath, "deb_dist/*.deb"))[0],
			path
		)

	def disable(self):
		self.active = False

		del self._modules
		del self._metadata

def init(moduleManager):
	return DebianPackagerModule(moduleManager)
