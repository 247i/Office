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

import unittest
import glob
import os
import contextlib

MODES = ("all", "load")

class TestCase(unittest.TestCase):
	def setUp(self):
		self._files = glob.glob(self._mm.resourcePath("testFiles") + "/*")

	def _modsForFile(self, file):
		if os.path.basename(file) in ("netherlands.png", "COPYING",):
			#files that aren't loadable
			return set()
		if file.endswith(".xml"):
			#Special case for abbyy since it doesn't have a mimetype
			loadMods = set(self._mm.mods("active", type="load", loads={"xml": ["words"]}))
		elif file.endswith(".csv"):
			#same for csv
			loadMods = set(self._mm.mods("active", type="load", loads={"csv": ["words"]}))
		elif file.endswith(".db"):
			#same for sqlite .db
			loadMods = set(self._mm.mods("active", type="load", loads={"db": ["words"]}))
		elif file.endswith("gnuVocabTrain.txt"):
			#gnuVocabTrain .txt
			loadMods = set(self._mm.mods("active", type="load", format="gnuVocabTrain"))
		elif file.endswith("vtrain.txt"):
			#vTrain .txt
			loadMods = set(self._mm.mods("active", type="load", format="vtrain"))
		else:
			mimetype = os.path.basename(file).split(".")[0].replace("_", "/")
			loadMods = set(self._mm.mods("active", type="load", mimetype=mimetype))
			self.assertTrue(loadMods, msg="No loader fount for mimetype: %s" % mimetype)
		return loadMods

	def _loadFiles(self, results=[]):
		if self.mode not in MODES:
			self.skipTest("Not running in one of these modes: " + ", ".join(MODES))
			#don't run the tests.
			return []
		if not results:
			#only load when not yet in cache.
			for file in self._files:
				loadMods = self._modsForFile(file)
				for mod in loadMods:
					result = mod.load(file)
					result["file"] = file
					result["mod"] = mod
					results.append(result)

		return results

	def testGetFileTypeOf(self):
		for file in self._files:
			loadMods = self._modsForFile(file)
			for mod in loadMods:
				try:
					#feel free to extend with new lesson types
					self.assertIn(mod.getFileTypeOf(file), ["words", "topo", "media"])
				except AssertionError:
					print file, mod
					raise

	def testHasAttrs(self):
		for mod in self._mm.mods("active", type="load"):
			self.assertTrue(mod.getFileTypeOf)
			self.assertTrue(mod.load)
			self.assertTrue(mod.name)
			for type, ext in mod.loads.iteritems():
				self.assertTrue(type)
				self.assertTrue(ext)
			with contextlib.ignored(AttributeError):
				#optional. But not empty
				self.assertTrue(mod.mimetype)

	def testHasItems(self):
		results = self._loadFiles()

		for data in results:
			try:
				self.assertTrue(data["list"]["items"])
			except AssertionError:
				print data["mod"], data["file"]
				raise

	def testItemHasUniqueId(self):
		results = self._loadFiles()

		for data in results:
			ids = set()
			for item in data["list"]["items"]:
				self.assertNotIn(item["id"], ids)
				ids.add(item["id"])

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="load"),
		)

	def enable(self):
		self.TestCase = TestCase
		self.TestCase._mm = self._mm
		self.active = True

	def disable(self):
		self.active = False
		del self.TestCase

def init(moduleManager):
	return TestModule(moduleManager)
