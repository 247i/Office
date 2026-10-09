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

class SettingDict(dict):
	def __init__(self, value, executeCallback, addedNow, *args, **kwargs):
		super(SettingDict, self).__init__(value, *args, **kwargs)

		self._executeCallback = executeCallback
		self._addedNow = addedNow

	def __setitem__(self, name, value):
		super(SettingDict, self).__setitem__(name, value)
		if name == "value" and self.has_key("callback"):
			self._executeCallback(self["callback"])

class SettingsModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(SettingsModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "settings"
		self.requires = (
			self._mm.mods(type="dataStore"),
		)

	def initialize(self):
		"""Connects to data store, should be called before doing
		   anything else but only once in each program run. Normally,
		   that's handled by the execute module.

		"""
		self._modules = set(self._mm.mods(type="modules")).pop()
		store = set(self._mm.mods(type="dataStore")).pop().store
		
		try:
			self._settings = store["org.openteacher.settings.settings"]
		except KeyError:
			self._settings = store["org.openteacher.settings.settings"] = {}

		#replace the dicts by SettingDicts
		for key, value in self._settings.iteritems():
			#False because it was added in a previous session
			self._settings[key] = SettingDict(value, self._executeCallback, addedNow=False)

		self.active = True

	def registerSetting(self, internal_name, **setting):
		"""Adds a setting. internal_name should be unique and describe
		   what the setting contains, we **strongly recommmend** to use the
		   'reverse domain' naming	strategy because of the first property.
		   (E.g. ``com.example.moduleName.settingName``).

		   The other arguments, describing the setting, should be:

		   * name,
		   * type="short_text",
		    * boolean
		    * short_text
		    * long_text
		    * number
		    * password
		    * option
		    * multiOption
		    * language
		    * profile
		    ... are available.
		   * defaultValue
		   * minValue=None
		   * maxValue=None
		   * category=None
		   * subcategory=None
		   * advanced=False
		   * callback=None

		   The callback option should have this format::

		    {
		        "args": ("active",),
		        "kwargs": {"type": "callback"},
		        "method": "callbackMethod",
		    }

		   Where args and kwargs are the same as in the following:
		   ``self._mm.mods(*args, **kwargs)``

		   The following argument should be included when type="option" or type="multiOption":

		   * options=[]
		    * options should have this format: ``("label", data)``

		   This method returns a setting dict with the same properties as
		   described above, with the difference that defaultValue is
		   missing and that the 'value' key is added containing the actual
		   current value of the setting. You're free to modify the object,
		   as long as its values are valid.

		   When a setting argument isn't given (e.g. category), then it
		   also isn't in the setting dict that is returned, so for the
		   non-obligatory ones (the one with default values above) check
		   for a ``KeyError`` and if there is one, threat it like the default
		   value is the current data.

		   If a callback is added, it's called when the value is changed
		   automatically by this module.

		"""
		if internal_name in self._settings:
			#copy the value
			setting["value"] = self._settings[internal_name]["value"]
		else:
			#use the default value
			setting["value"] = setting.pop("defaultValue")
		#wrap it, True because it's added now
		wrappedSetting = SettingDict(setting, self._executeCallback, addedNow=True)
		#store
		self._settings[internal_name] = wrappedSetting

		return wrappedSetting
	
	def setting(self, internal_name):
		"""Method to return a setting from the internal name."""

		return self._settings[internal_name]

	@property
	def registeredSettings(self):
		"""Returns a list of all registered settings. The way to access
		   the settings if you are providing a settings dialog/other
		   interface like that.

		"""
		#only settings registered this session
		return [
			setting
			for setting in self._settings.values()
			if getattr(setting, "_addedNow", False)
		]

	def _executeCallback(self, callback):
		obj = self._modules.default(*callback["args"], **callback["kwargs"])
		getattr(obj, callback["method"])() #execute

def init(moduleManager):
	return SettingsModule(moduleManager)
