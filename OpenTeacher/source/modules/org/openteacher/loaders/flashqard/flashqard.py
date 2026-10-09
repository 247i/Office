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
import re
import datetime

class FlashQardLoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(FlashQardLoaderModule, self).__init__(*args, **kwargs)
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
		self.filesWithTranslations = ("flashqard.py",)

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
		#TRANSLATORS: http://flashqard-project.org/
		self.name = _("Flashqard")

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.mimetype = "application/x-flashqard"
		self.loads = {"fq": ["words"]}

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self.name
		del self.loads
		del self.mimetype

	def getFileTypeOf(self, path):
		if path.endswith(".fq"):
			return "words"

	def _stripTags(self, html):
		"""Thanks mmmdreg! See: http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python"""

		return re.sub("<[^<]+?>", "", html)

	def load(self, path):
		"""Loads .fq (FlashQard) files. Based on file format inspection.
		   (even though source code is available, see
		   http://flashqard-project.org/download.php)

		"""
		with open(path, "r") as f:
			root = ElementTree.parse(f).getroot()

		list = {
			"items": [],
			"title": root.find("box").get("name"),
		}

		for i, itemTree in enumerate(root.findall(".//card")):
			questions = self._stripTags(itemTree.findtext("frontsidedocument/html"))
			answers = self._stripTags(itemTree.findtext("backsidedocument/html"))
			created = itemTree.findtext("statistics/dateCreated")
			list["items"].append({
				"id": i,
				"questions": self._parse(questions),
				"answers": self._parse(answers),
				"comment": self._stripTags(itemTree.findtext("comments")),
				"created": datetime.datetime.strptime(created, "%d.%m.%Y")
			})

		return {
			"resources": {},
			"list": list,
		}

def init(moduleManager):
	return FlashQardLoaderModule(moduleManager)
