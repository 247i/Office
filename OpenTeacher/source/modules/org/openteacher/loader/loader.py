#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2013, Marten de Vries
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

import os
import sys

class Everything(object):
	def __contains__(self, item):
		return True

class LoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(LoaderModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "loader"

		self.uses = (
			self._mm.mods(type="lesson"),
			self._mm.mods(type="load"),
			self._mm.mods(type="recentlyOpened"),
		)

	@property
	def _supportedFileTypes(self):
		types = set()
		for lesson in self._mm.mods("active", type="lesson"):
			try:
				types.add(lesson.dataType)
			except AttributeError:
				pass
		return types

	@property
	def usableExtensions(self):
		"""Returns a alphabetically sorted list of tuples. The tuples
		   have this form: (file_format_name, ext). For example:
		   ("OpenTeaching words file", "otwd"). The list includes all
		   extensions that can be loaded with the modules currently in
		   use by OpenTeacher

		"""
		exts = set()

		#Collect exts the loader modules support, if there is a gui
		#module for the type(s) they can provide
		for module in self._modules.sort("active", type="load"):
			for ext, fileTypes in module.loads.iteritems():
				for fileType in fileTypes:
					if fileType in self._supportedFileTypes:
						exts.add((ext, module.name))
		return sorted(exts)

	@property
	def openSupport(self):
		"""Tells if there's a chance that calling load() will succeed
		   (and not fail with a NotImplementedError)

		"""
		return len(self.usableExtensions) != 0

	@property
	def _addToRecentlyOpened(self):
		try:
			recentlyOpenedModule = self._modules.default("active", type="recentlyOpened")
		except IndexError:
			return
		return recentlyOpenedModule.add

	def load(self, path):
		""""Opens the file at ``path`` in the GUI."""

		if isinstance(path, unicode):
			#recently opened case
			path = path.encode(sys.getfilesystemencoding())

		type, lessonData = self.loadToLesson(path, self._supportedFileTypes)

		if self._addToRecentlyOpened:
			# Add to recently opened
			self._addToRecentlyOpened(**{
				"label": lessonData["list"].get("title", "") or os.path.basename(path),
				"args": {},
				"kwargs": {"path": unicode(path, sys.getfilesystemencoding())},
				"method": "load",
				"moduleArgsSelectors": ["active"],
				"moduleKwargsSelectors": {"type": "loader"},
			})

		self.loadFromLesson(type, lessonData)

	def loadToLesson(self, path, dataTypes=None):
		"""Loads the file in ``path`` and returns a tuple containing
		   ``(dataType, lessonData)`` or raises NotImplementedError if
		   that is impossible. When a list is passed to ``dataTypes``,
		   it only loads the file if it can do so returning lessonData
		   of one of the dataTypes in the list. By default, it returns
		   lessonData of any type.

		"""
		if dataTypes is None:
			dataTypes = Everything()
		for loadModule in self._modules.sort("active", type="load"):
			fileType = loadModule.getFileTypeOf(path)
			if fileType is not None and fileType in dataTypes:
				return fileType, loadModule.load(path)
		raise NotImplementedError()

	def loadFromLesson(self, dataType, lessonData):
		"""Tries to show ``lessonData`` of type ``type`` in a GUI
		   lesson.

		"""
		loaders = [
			loader
			for loader in self._modules.sort("active", type="lesson")
			if loader.dataType == dataType
		]
		if not loaders:
			raise NotImplementedError()
		loader = loaders[0]
		lesson = loader.createLesson()
		lesson.list = lessonData["list"]
		lesson.resources = lessonData["resources"]
		if "changed" in lessonData:
			lesson.changed = lessonData["changed"]

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()

		self.active = True

	def disable(self):
		self.active = False

		del self._modules

def init(moduleManager):
	return LoaderModule(moduleManager)

