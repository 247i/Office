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

import tempfile
import os
import atexit
import shutil
import subprocess
import glob

class SourceSaverModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(SourceSaverModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "sourceSaver"

		atexit.register(self._cleanup)
		self._dirs = set()

	def enable(self):
		self.active = True

	def _cleanup(self):
		for dir in self._dirs:
			shutil.rmtree(dir)

	def _gatherSource(self):
		print "Please keep in mind that the source export may contain text in the language that OpenTeacher currently uses. If you're building an official package, you should make sure OpenTeacher is running in English, first. (It might currently, this warning isn't a check but just shown always.)\n"
		#e.g. /tmp/uuid-here
		copyBase = tempfile.mkdtemp()
		self._dirs.add(copyBase)

		#e.g. /programming_dir/openteacher
		moduleBase = os.path.abspath(os.path.dirname(__file__))
		while not moduleBase.endswith("modules"):
			moduleBase = os.path.normpath(os.path.join(moduleBase, ".."))
		originalBase = os.path.normpath(os.path.join(moduleBase, ".."))

		#make /tmp/uuid-here/modules
		os.mkdir(os.path.join(copyBase, "modules"))
		#copy python/cython files from the original base dir to
		#/tmp/uuid-here
		for f in os.listdir(originalBase):
			originalPath = os.path.join(originalBase, f)
			copyPath = os.path.join(copyBase, f)

			isPyMod = (
				os.path.isfile(originalPath) and
				(
					f.endswith(".py") or
					f.endswith(".pyx")
				)
			)
			isPyPackage = os.path.isfile(os.path.join(originalPath, "__init__.py"))

			if isPyMod:
				shutil.copy(originalPath, copyPath)
			elif isPyPackage:
				shutil.copytree(originalPath, copyPath)

		#copy all modules available in self._mm.mods
		for mod in self._mm.mods:
			dir = os.path.dirname(mod.__class__.__file__)
			commonLen = len(os.path.commonprefix([moduleBase, dir]))
			dest = os.path.join(
				copyBase,
				"modules",
				dir[commonLen:].strip(os.sep)
			)
			shutil.copytree(dir, dest, ignore=shutil.ignore_patterns("*.pyc", "*~"))
		return copyBase

	def saveSourceWithCExtensions(self):
		copyBase = self._gatherSource()

		#compile cython (.pyx) files into c extension code
		for path in glob.iglob(os.path.join(copyBase, "*.pyx")):
			subprocess.check_call(["cython", path])
		return copyBase

	def saveSource(self):
		copyBase = self._gatherSource()
		for path in glob.iglob(os.path.join(copyBase, "*.pyx")):
			os.rename(path, os.path.splitext(path)[0] + ".py")

		return copyBase

	def disable(self):
		self.active = False

def init(moduleManager):
	return SourceSaverModule(moduleManager)
