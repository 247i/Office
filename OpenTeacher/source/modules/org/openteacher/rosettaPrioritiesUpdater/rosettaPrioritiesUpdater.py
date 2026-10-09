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

import os
import glob

class RosettaPrioritiesUpdaterModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(RosettaPrioritiesUpdaterModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "rosettaPrioritiesUpdater"

		self.priorities = {
			"default": -1,
			"update-rosetta-priorities": 0,
		}
		self.requires = (
			self._mm.mods(type="execute"),
		)

	def _getMod(self, template):
		mapping = {}
		for mod in self._mm.mods:
			modRoot = os.path.dirname(mod.__class__.__file__)
			potPathGlob = os.path.join(modRoot, "translations", "*.pot")
			potPath = glob.glob(potPathGlob)
			if potPath:
				potName = os.path.splitext(os.path.basename(potPath[0]))[0].lower()
				mapping[potName] = mod
				if "_" in potName:
					#second possibility
					mapping[potName.replace("_", "-")] = mod

		return mapping[template]

	def _adjustedPriority(self, mod, priority):
		if mod in self._mm.mods(type="friendlyTranslationNames"):
			#this just needs to be on the top of the list.
			priority = 10000

		priorityCorrectionsForKeyword = {
			"lesson": 50,
			"enterer": 40,
			"teacher": 30,
			"profiledescription": -40,
			"loader": -30,
			"saver": -30,
			"notecalculator": -70,
			"uicontroller": 50,
			"mobilegenerator": 15,
		}
		for keyword, priorityCorrection in priorityCorrectionsForKeyword.iteritems():
			if keyword in mod.__class__.__file__.lower():
				priority += priorityCorrection
		return priority

	def _run(self):
		answer = raw_input("This updates the priorities of the translations of OpenTeacher on Launchpad. If you're not in the ~openteachermaintainers team, continuing will probably crash or do nothing. Continue? (y/n) ")
		if answer.lower() not in ("y", "yes", "yep"):
			return
		lp = launchpadlib.launchpad.Launchpad.login_with("OpenTeacher Rosetta priorities updater", "production")

		priorities = set()

		for template in lp.projects["openteacher"].translation_focus.getTranslationTemplates():
			if not template.active:
				continue
			try:
				mod = self._getMod(template.name)
			except KeyError:
				print "Couldn't find a module for: %s" % template.name
				continue

			priority = self._modPriority(mod)
			priority = self._adjustedPriority(mod, priority)

			priorities.add((priority, template))

		for priority, template in sorted(priorities):
			print "Setting %s to %s" % (template.name, priority)
			template.priority = priority
			template.lp_save()
		exit()

	def _modPriority(self, mod, cache={}):
		#caching to speed things up a bit. It's needed.
		if mod not in cache:
			#start priority
			priority = 1
			#add the priorities of all mods depending on this one
			for otherMod in self._mm.mods:
				for selector in getattr(otherMod, "requires", []):
					if mod in selector:
						priority += self._modPriority(otherMod)
				for selector in getattr(otherMod, "uses", []):
					if mod in selector:
						priority += int(round(0.75 * self._modPriority(otherMod)))
			cache[mod] = priority
		return cache[mod]

	def enable(self):
		self._modules = next(iter(self._mm.mods(type="modules")))

		global launchpadlib
		try:
			import launchpadlib.launchpad
		except ImportError:
			#remain inactive
			return

		self._modules.default("active", type="execute").startRunning.handle(self._run)

		self.active = True

	def disable(self):
		self.active = False

		self._modules.default("active", type="execute").startRunning.unhandle(self._run)
		del self._modules

def init(moduleManager):
	return RosettaPrioritiesUpdaterModule(moduleManager)
