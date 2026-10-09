#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2012-2013, Marten de Vries
#	Copyright 2011, Milan Boers
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

import zipfile
import tempfile
import datetime
import atexit
import datetime
import os
import shutil
import json
import contextlib

class OtxxLoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(OtxxLoaderModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "otxxLoader"

		atexit.register(self._cleanupTempPaths)

	def _stringsToDatetimes(self, list):
		if not "tests" in list:
			return list
		for test in list["tests"]:
			for result in test["results"]:
				if "active" not in result:
					continue
				result["active"]["start"] = self.stringToDatetime(result["active"]["start"])
				result["active"]["end"] = self.stringToDatetime(result["active"]["end"])

		return list

	def stringToDatetime(self, string):
		return datetime.datetime.strptime(
			string,
			"%Y-%m-%dT%H:%M:%S.%f"
		)

	def load(self, path, resourceFilenames={}):
		with contextlib.closing(zipfile.ZipFile(path, "r")) as zipFile:
			listFile = zipFile.open("list.json")
			list = json.load(listFile)
			list = self._stringsToDatetimes(list)

			resources = {}
			for resourceKey, filename in resourceFilenames.iteritems():
				tf = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1])
				path2 = tf.name
				
				self._tempPaths.add(path2)
				with contextlib.ignored(KeyError):
					#KeyError: the file might not be in the zip. That's
					#not important enough to break on. It happens when
					#importing .ottp files created with OT < 3.2 e.g.
					resourceFile = zipFile.open(filename)
					
					shutil.copyfileobj(resourceFile, tf)
					tf.close()
					
					resources[resourceKey] = path2

		return {
			"resources": resources,
			"list": list,
		}

	def _cleanupTempPaths(self):
		if hasattr(self, "_tempPaths"):
			for path in self._tempPaths:
				os.remove(path)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._tempPaths = set()

		self.active = True

	def disable(self):
		self.active = False

		self._cleanupTempPaths()
		del self._modules
		del self._tempPaths

def init(moduleManager):
	return OtxxLoaderModule(moduleManager)
