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

import code
import sys
import os
import contextlib
import __builtin__

BANNER_TEMPL = """Welcome to the {appname} {appversion} interactive Python shell!

The module manager is in the 'mm' variable. For your convenience, we 
also added the 'modules' module in the 'modules' variable so you can
start experimenting with modules right away. Have fun!"""

class ShellModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(ShellModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "shell"
		self.priorities = {
			"default": -1,
			"shell": 0
		}
		self.requires = (
			self._mm.mods(type="execute"),
			self._mm.mods(type="metadata"),
		)

	def _run(self):
		#tab completion & history file
		try:
			import readline
		except ImportError:
			pass
		else:
			import rlcompleter
			readline.parse_and_bind("tab: complete")

			histfile = os.path.join(os.path.expanduser("~"), ".pyhist")
			try:
				readline.read_history_file(histfile)
			except IOError:
				pass

		#setup banner & local variables
		banner = BANNER_TEMPL.format(**{
			"appname": self._metadata["name"],
			"appversion": self._metadata["version"],
		})
		self._patch()
		args = {
			"banner": banner,
			"local": {
				"mm": self._mm,
				"modules": self._modules,
			}
		}
		try:
			code.interact(**args)
		except SystemExit:
			#exit the OpenTeacher way.
			print "Have a nice day!"

		#save tab completion history file
		with contextlib.ignored(NameError):
			readline.write_history_file(histfile)

	def _patch(self):
		def f(s):
			d = {}
			for c in (65, 97):
				for i in range(26):
					d[chr(i+c)] = chr((i+13) % 26 + c)

			return "".join([d.get(c, c) for c in s])

		realImport = __builtin__.__import__
		def myImport(name, *args, **kwargs):
			firstTime = f("guvf") not in sys.modules
			result = realImport(name, *args, **kwargs)
			if name == f("guvf") and firstTime:
				print f("Clguba zbqhyrf ner pbby, BcraGrnpure zbqhyrf ner orggre!")
			return result
		__builtin__.__import__ = myImport

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._metadata = self._modules.default(type="metadata").metadata
		self._execute = self._modules.default(type="execute")
		self._execute.startRunning.handle(self._run)

		self.active = True

	def disable(self):
		self.active = False
		del self._modules
		del self._metadata
		del self._execute

def init(moduleManager):
	return ShellModule(moduleManager)
