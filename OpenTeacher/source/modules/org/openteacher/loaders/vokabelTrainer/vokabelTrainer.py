#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2012, Marten de Vries
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

class VokabelTrainerLoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(VokabelTrainerLoaderModule, self).__init__(*args, **kwargs)
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
		self.filesWithTranslations = ("vokabelTrainer.py",)

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
		#TRANSLATORS: http://www.vt-online.net/ueberblick/ (german)
		self.name = _("Vokabel Trainer")

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.mimetype = "application/x-vokabeltrainer"
		self.loads = {"vtl3": ["words"]}

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self.name
		del self.loads
		del self.mimetype

	def getFileTypeOf(self, path):
		if path.endswith(".vtl3"):
			return "words"

	def load(self, path):
		with open(path, "r") as f:
			root = ElementTree.parse(f).getroot()

		list = {
			"items": [],
		}

		for i, itemTree in enumerate(root.findall("Vokabeldatensatz/Datensatz")):
			word = {
				"id": i,
				"questions": [],
				"answers": [],
			}
			comments = []
			for question in itemTree.findall("Vokabeln/string"):
				word["questions"].append((question.text,))
			for answer in itemTree.findall("Vokabeln/string"):
				word["answers"].append((answer.text,))
			for comment in itemTree.findall("Kommentare/string"):
				comments.append((comment.text))
			if comments:
				word["comment"] = u"; ".join(comments)

			list["items"].append(word)

		return {
			"resources": {},
			"list": list,
		}

def init(moduleManager):
	return VokabelTrainerLoaderModule(moduleManager)
