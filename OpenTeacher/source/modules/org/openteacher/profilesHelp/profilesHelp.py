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

import textwrap

class ProfilesHelpModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(ProfilesHelpModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "profilesHelp"
		self.uses = (
			self._mm.mods(type="profileDescription"),
		)
		self.requires = (
			self._mm.mods(type="execute"),
		)
		self.priorities = {
			"help": 0,
			"default": -1,
		}

	def run(self):
		simple = []
		advanced = []

		for mod in self._mm.mods("active", type="profileDescription"):
			if mod.desc["advanced"]:
				advanced.append(mod.desc)
			else:
				simple.append(mod.desc)

		def printProfileList(profiles):
			for profile in sorted(profiles, key=lambda p: p["name"]):
				text = "- {name}: {niceName}".format(**profile)
				print textwrap.fill(text, 80, subsequent_indent=3 * " ")

		print "Profile overview:"
		print ""
		print "User profiles"
		printProfileList(simple)
		print ""
		print "Developer profiles"
		printProfileList(advanced)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._modules.default(type="execute").startRunning.handle(self.run)

		self.active = True

	def disable(self):
		self.active = False

		del self._modules

def init(moduleManager):
	return ProfilesHelpModule(moduleManager)
