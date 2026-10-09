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

import os
import unittest
import logging
import moduleManager

logger = logging.getLogger(__name__)

MODES = ("all", "moduleManager")

class TestCase(unittest.TestCase):
	"""Tries to enable() and disable() all modules with different
	   amounts of modules in uses enabled. Checks if modules reset their
	   state on disable(). This segfaults sometimes, but it shouldn't
	   give any other errors. (And if anyone manages to remove the
	   segfault, that would be very welcome!)

	"""
	def setUp(self):
		if not self.mode in MODES:
			self.skipTest("Too heavy for this test mode.")
		self._mm = moduleManager.ModuleManager(self._masterModuleManager.modulesPath)

	def _enableIncludingDependenciesIfNotActive(self, mod, minimalDependencies):
		#the fast exit so the recursiveness isn't forever
		if getattr(mod, "active", False):
			return True, []
		return self._enableIncludingDependencies(mod, minimalDependencies)

	def _enableIncludingDependencies(self, mod, minimalDependencies):
		success, enabledMods = self._enableDependencies(mod, minimalDependencies)
		if not success:
			return False, enabledMods

		#enable
		if hasattr(mod, "enable"):
			logger.debug("enabling " + mod.__class__.__file__)
			mod.enable()
		enabled = getattr(mod, "active", False)
		if enabled:
			enabledMods.append(mod)
		return enabled, enabledMods

	def _enableDependencies(self, mod, minimalDependencies):
		enabledMods = []

		for selector in getattr(mod, "requires", []):
			success, enabledMods = self._enableDependencySelector(selector, minimalDependencies, enabledMods)
			if not success:
				#fast exit
				return False, enabledMods

		if not minimalDependencies:
			for selector in getattr(mod, "uses", []):
				success, enabledMods = self._enableDependencySelector(selector, minimalDependencies, enabledMods)
		return True, enabledMods

	def _enableDependencySelector(self, selector, minimalDependencies, enabledMods):
		success = False
		for requirement in selector:
			subSuccess, otherMods = self._enableIncludingDependenciesIfNotActive(requirement, minimalDependencies)
			enabledMods.extend(otherMods)
			if subSuccess:
				success = True
				if minimalDependencies:
					#dependencies met for this selector, stop trying
					break
		#dependencies couldn't be satisfied
		return success, enabledMods

	def _disableDependencyTree(self, mods):
		for mod in reversed(mods):
			if hasattr(mod, "disable"):
				logger.debug("disabling " + mod.__class__.__file__)
				mod.disable()

	def _fakeExecuteModule(self):
		#initialize settings (normally they're used by the execute
		#module)
		next(iter(self._mm.mods(type="settings"))).initialize()

		#inject an alternative execute module into the module system,
		#because we can't use the real one. (Every module capable of
		#doing that registers at startRunning.)
		class ExecuteMod(object):
			type = "execute"
			active = True
			startRunning = next(iter(self._mm.mods(type="event"))).createEvent()
			__file__ = os.path.join(self._mm.modulesPath, "org/openteacher/execute/execute.py")
		self._mm._modules.remove(next(iter(self._mm.mods(type="execute"))))
		self._mm._modules.add(ExecuteMod())
		#Set a profile. The execute module does that normally.
		next(iter(self._mm.mods(type="modules"))).profile = "default"

	def _removeGtkModule(self):
		"""Removes the GTK module from the module manager, because that
		   one can't be enabled at the same time with Qt. Normally the
		   profiles take care of that, but this tests circumvents the
		   profiles.

		"""
		theMod = next(iter(self._mm.mods(type="gtkGui")))
		self._mm._modules.remove(theMod)

	def _doTest(self, minimalDependencies):
		self._fakeExecuteModule()
		self._removeGtkModule()

		for mod in self._mm.mods:
			startVars = set(vars(mod).keys()) - set(["active"])
			success, enabledMods = self._enableIncludingDependenciesIfNotActive(mod, minimalDependencies)
			self._disableDependencyTree(enabledMods)
			endVars = set(vars(mod).keys()) - set(["active"])
			try:
				self.assertEqual(startVars, endVars)
			except AssertionError: # pragma: no cover
				print mod
				raise
			logger.debug("")

	def testMinimalDependencies(self):
		self._doTest(True)

	def testWithFullDependencies(self):
		self._doTest(False)

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"

	def enable(self):
		self.TestCase = TestCase
		self.TestCase._masterModuleManager = self._mm
		self.active = True

	def disable(self):
		self.active = False
		del self.TestCase

def init(moduleManager):
	return TestModule(moduleManager)
