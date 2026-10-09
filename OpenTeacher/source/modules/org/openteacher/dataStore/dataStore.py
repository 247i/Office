#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011, Marten de Vries
#	Copyright 2011-2012, Milan Boers
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
#	GNU Generatypel Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with OpenTeacher.  If not, see <http://www.gnu.org/licenses/>.

import json
import os
import atexit
import logging

logger = logging.getLogger(__name__)

class JSONShelve(dict):
	"""A dict-like object of which the keys and values are persistent.
	   Note that all keys need to be strings and that all values need
	   to be JSON serializable.

	"""
	def __init__(self, filepath, *args, **kwargs):
		super(JSONShelve, self).__init__(*args, **kwargs)

		self.filepath = filepath

		if os.path.exists(self.filepath):
			with open(self.filepath, "r") as fp:
				try:
					d = json.load(fp)
				except ValueError, e:
					#Catches both json.decoder.JSONDecodeError and
					#ValueError, see:
					#https://github.com/Yelp/mrjob/issues/544
					#
					#file corrupted. Print for debugging purposes, but
					#letting the whole program crash for a corrupt
					#settings file isn't done.
					logger.debug(e, exc_info=True)
					return
			# Copy dict to self
			self.update(d)

	def write(self):
		with open(self.filepath, "w") as fp:
			json.dump(self, fp)

class DataStoreModule(object):
	"""This module offers a data store, which allows data to be saved
	   persistently. The store is in the 'store' property and is dict-
	   like. Keep in mind it is JSON serialized to the hard disk, so
	   make sure everything you save inside is JSON serializable. Also
	   keep in mind, that all modules use the same store. So make sure
	   you don't claim generic names. We therefore strongly recommend
	   to use the 'reverse domain' strategy. So e.g.
	   com.example.modName.valueName as key.

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(DataStoreModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "dataStore"

		self._folderPath = self._getFolderPath()
		# Create folder path if not exists
		if not os.path.exists(self._folderPath):
			os.makedirs(self._folderPath)

		self.store = JSONShelve(os.path.join(self._folderPath, "store.json"))
		atexit.register(self.store.write)

		self.active = True

	def _getFolderPath(self):
		if os.name == "nt":
			return os.path.join(os.getenv("appdata"), "OpenTeacher")
		else:
			return os.path.join(os.path.expanduser("~"), ".openteacher")

def init(moduleManager):
	return DataStoreModule(moduleManager)
