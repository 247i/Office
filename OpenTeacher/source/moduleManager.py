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

import sys
import os
import imp
import moduleFilterer

class ModuleManager(object):
	"""This class manages modules. It loads them from a directory when
	   they meet the requirements for being a module, and it offers a
	   few functions to the initialized modules, like getting resource
	   paths and handling imports in the module directory.

	"""
	def __init__(self, modulesPath, *args, **kwargs):
		super(ModuleManager, self).__init__(*args, **kwargs)

		self.modulesPath = modulesPath
		self._references = set()

		self._loadModules()

	@staticmethod
	def _callerOfCallerPath():
		callerFile = sys._getframe(2).f_code.co_filename
		return os.path.dirname(callerFile)

	@classmethod
	def resourcePath(cls, resource):
		return os.path.join(cls._callerOfCallerPath(), resource)

	@property
	def mods(self):
		return moduleFilterer.ModuleFilterer(self._modules)

	def importFrom(self, path, moduleName):
		fp, pathname, description = imp.find_module(moduleName, [path])

		try:
			#import the module
			module = imp.load_module(moduleName, fp, pathname, description)
			#remove the module from the python cache, to avoid
			#namespace clashes
			del sys.modules[moduleName]
			#but keep our own reference, otherwise the module namespace
			#will probably be garbage collected.
			self._references.add(module)
			return module
		finally:
			fp.close()

	def import_(self, moduleName):
		return self.importFrom(self._callerOfCallerPath(), moduleName)

	def _loadModules(self):
		self._modules = set()

		for root, dirs, files in os.walk(self.modulesPath):
			name = os.path.split(root)[1]
			valid = (
				name + ".py" in files and
				#os.sep so names like random_.py are allowed.
				not os.sep + "_" in root
			)
			if valid:
				container = self.importFrom(root, name)
				module = container.init(self)
				#To compensate for the missing __module__ attribute of
				#the class Python has when importing normally.
				path = os.path.join(root, name + ".py")
				module.__class__.__file__ = os.path.abspath(path)
				self._modules.add(module)
