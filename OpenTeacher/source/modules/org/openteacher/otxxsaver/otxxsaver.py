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

import superjson
import zipfile
import contextlib

class OtxxSaverModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(OtxxSaverModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "otxxSaver"
		self.requires = (
			self._mm.mods(type="metadata"),
		)

	def save(self, lesson, path, resourceFilenames={}, zipCompression=zipfile.ZIP_DEFLATED):
		list = {"file-format-version": self._version}
		list.update(lesson.list)
		with contextlib.closing(zipfile.ZipFile(path, "w", zipCompression)) as otxxzip:
			otxxzip.writestr("list.json", superjson.dumps(
				list, #the list to save
				separators=(',',':'), #compact encoding
				default=self._serialize #serialize datetime
			))
			for resourceKey, filename in resourceFilenames.iteritems():
				otxxzip.write(lesson.resources[resourceKey], filename)

		lesson.path = path
		lesson.changed = False

	@property
	def _version(self):
		return self._modules.default("active", type="metadata").metadata["version"]

	def _serialize(self, obj):
		try:
			return obj.strftime("%Y-%m-%dT%H:%M:%S.%f")
		except AttributeError:
			raise TypeError("The type '%s' isn't JSON serializable." % obj.__class__)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self.active = True

	def disable(self):
		self.active = False
		del self._modules

def init(moduleManager):
	return OtxxSaverModule(moduleManager)
