#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011, Milan Boers
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

import tempfile
import zipfile
import contextlib
import os
import shutil

class AnkiApkgLoaderModule(object):
	"""A pretty basic .apkg importer. For now it imports everything like
	   it is a words file, which might not always be the best way of
	   dealing with anki files. Also, it does nothing with the results
	   in the database. But, in the end, it might work fine for people
	   who want to switch. :)

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(AnkiApkgLoaderModule, self).__init__(*args, **kwargs)

		self.type = "load"
		self.priorities = {
			"default": 432,
		}
		self._mm = moduleManager
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.requires = (
			self._mm.mods(type="load", loads={"anki2": ["words"]}),
		)
		self.filesWithTranslations = ("apkg.py",)

	@property
	def _loadAnki2(self):
		return self._modules.default("active", type="load", loads={"anki2": ["words"]}).load

	def _stripTags(self, html):
		"""Thanks mmmdreg! See: http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python"""

		return re.sub("<[^<]+?>", "", html)

	def _retranslate(self):
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		#TRANSLATORS: This is one of the file formats OpenTeacher
		#TRANSLATORS: can read. It's named after the program that uses
		#TRANSLATORS: it. See http://ankisrs.net/ for more info on it.
		self.name = _("Anki 2.0")

	def enable(self):
		self.loads = {"apkg": ["words"]}
		self.mimetype = "application/x-apkg"

		self._modules = set(self._mm.mods(type="modules")).pop()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

	def disable(self):
		self.active = False

		del self.name
		del self.loads
		del self.mimetype

		del self._modules

	def getFileTypeOf(self, path):
		if path.endswith(".apkg"):
			return "words"

	def load(self, path):
		items = []
		try:
			fd, anki2Path = tempfile.mkstemp(".anki2")
			with contextlib.closing(zipfile.ZipFile(path)) as apkgZip:
				with open(anki2Path, "w") as anki2File:
					shutil.copyfileobj(apkgZip.open("collection.anki2"), anki2File)
			return self._loadAnki2(anki2Path)
		finally:
			os.close(fd)
			os.remove(anki2Path)

def init(moduleManager):
	return AnkiApkgLoaderModule(moduleManager)
