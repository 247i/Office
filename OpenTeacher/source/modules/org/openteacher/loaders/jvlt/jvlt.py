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

from etree import ElementTree
import zipfile
import contextlib

class JvltLoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(JvltLoaderModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "load"
		self.priorities = {
			"default": 756,
		}
		
		self.requires = (
			self._mm.mods(type="wordsStringParser"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("jvlt.py",)

	@property
	def _parse(self):
		return self._modules.default("active", type="wordsStringParser").parse

	def _retranslate(self):
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		#TRANSLATORS: This is the name of a file type OpenTeacher can
		#TRANSLATORS: read. It's named after the program with the same
		#TRANSLATORS: name. For more info on the program, see:
		#TRANSLATORS: http://jvlt.sourceforge.net/
		self.name = _("jVLT")

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.mimetype = "application/x-jvlt"
		self.loads = {"jvlt": ["words"]}

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self.name
		del self.loads
		del self.mimetype

	def getFileTypeOf(self, path):
		if path.endswith(".jvlt"):
			return "words"

	def load(self, path):
		"""Documentation: http://jvlt.sourceforge.net/download.html
		   (at the bottom)

		"""
		with contextlib.closing(zipfile.ZipFile(path)) as jvltZip:
			root = ElementTree.parse(jvltZip.open("dict.xml")).getroot()

		list = {"items": []}

		for i, itemTree in enumerate(root.findall(".//entry")):
			list["items"].append({
				"id": i,
				"questions": self._parse(itemTree.findtext("orth") or u""),
				"answers": self._parse(itemTree.findtext("sense/trans") or u""),
				"comment": u", ".join([pron.text for pron in itemTree.findall("pron")]),
			})

		return {
			"resources": {},
			"list": list,
		}

def init(moduleManager):
	return JvltLoaderModule(moduleManager)
