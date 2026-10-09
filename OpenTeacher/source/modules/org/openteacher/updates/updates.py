#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011, 2013 Marten de Vries
#	Copyright 2012, Milan Boers
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

import urllib
import urllib2
import json
import datetime
import zipfile
import os

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

class UpdatesModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(UpdatesModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "updates"
		self.requires = (
			self._mm.mods(type="metadata"),
			self._mm.mods(type="dataStore"),
			self._mm.mods(type="gpg"),
		)

	@staticmethod
	def _download(link, filename):
		urllib.urlretrieve(link, filename)

	def _downloadUpdates(self):
		"""Raises IOError and ValueError"""
		self._download(self._metadata["updatesUrl"], self._mm.resourcePath("updates.json"))
		asc = urllib2.urlopen(self._metadata["updatesSignatureUrl"])
		verified = self._gpg.verify_file(asc, open(self._mm.resourcePath("updates.json")))
		if verified != 0:
			raise ValueError("No valid signature!")

	@property
	def updates(self):
		if self._updatesCache is not None:
			return self._updatesCache
		try:
			lastUpdate = datetime.datetime.strptime(
				self._dataStore["org.openteacher.updates.lastUpdate"],
				DATETIME_FORMAT
			)
		except KeyError:
			lastUpdate = datetime.datetime.min
		self._downloadUpdates()
		updates = json.load(open(self._mm.resourcePath("updates.json")))
		for i in xrange(len(updates)):
			updates[i]["timestamp"] = datetime.datetime.strptime(
				updates[i]["timestamp"],
				DATETIME_FORMAT
			)
		result = filter(lambda x: x["timestamp"] > lastUpdate, updates)
		self._updatesCache = result
		return result

	def _installUpdate(self, link, signature):
		"""Raises IOError and ValueError"""
		self._download(link, self._mm.resourcePath("update.zip"))
		asc = urllib2.urlopen(signature)
		verified = self._gpg.verify_file(asc, open(self._mm.resourcePath("update.zip")))
		if verified != 0:
			raise ValueError("No valid signature!")

		updatesZip = zipfile.ZipFile(self._mm.resourcePath("update.zip"), "r")
		for item in updatesZip.namelist():
			#check if it doesn't stay inside the module dir
			if os.path.normpath(item).startswith(os.pardir):
				#Help, the OT Maintainers have gone mad! This is
				#malware! :P
				#
				#skip this update...
				return
		#'all-clear'
		updatesZip.extractall(self._mm.modulesPath)
		os.remove(self._mm.resourcePath("update.zip"))

	def update(self):
		for update in self.updates:
			self._installUpdate(update["link"], update["signature"])
			self._dataStore["org.openteacher.updates.lastUpdate"] = datetime.datetime.strftime(
				update["timestamp"],
				DATETIME_FORMAT
			)
		#Done installing updates, inform caller to restart in order for the changes to take effect.
		raise SystemExit("Updates installed, please restart.")

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._metadata = self._modules.default("active", type="metadata").metadata
		self._dataStore = self._modules.default(type="dataStore").store
		self._gpg = self._modules.default("active", type="gpg").gpg
		self._updatesCache = None

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self._metadata
		del self._dataStore
		del self._gpg
		del self._updatesCache

def init(moduleManager):
	return UpdatesModule(moduleManager)
