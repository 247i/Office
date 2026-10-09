#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2013, Marten de Vries
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
import datetime
import locale

class JMemorizeLessonLoaderModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(JMemorizeLessonLoaderModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "load"
		self.requires = (
			self._mm.mods(type="wordsStringParser"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)

	@property
	def _parse(self):
		return self._modules.default("active", type="wordsStringParser").parse

	def _parseDate(self, date):
		#change locale temporary; so strptime can do it's work the way
		#it should.
		locale.setlocale(locale.LC_ALL, "C")

		#do conversion
		dt = datetime.datetime.strptime(date, "%d-%b-%Y %H:%M:%S")

		#set locale back to make sure conflicts don't arise with other
		#modules depending on the locale.
		locale.resetlocale()

		return dt

	def getFileTypeOf(self, path):
		if path.endswith(".jml"):
			return "words"

	def load(self, path):
		#reference implementation:
		#http://jmemorize.svn.sourceforge.net/viewvc/jmemorize/trunk/jmemorize/src/jmemorize/core/io/XmlBuilder.java?view=markup
		try:
			with contextlib.closing(zipfile.ZipFile(path, "r")) as f:
				xmlFile = f.open("lesson.xml", "r")
		except (zipfile.BadZipfile, KeyError):
			xmlFile = open(path, "r")

		#crashes when the file structure is invalid.
		try:
			root = ElementTree.parse(xmlFile).getroot()
		finally:
			xmlFile.close()
		items = []
		for i, card in enumerate(root.findall(".//Card")):
			item = {
				"id": i,
				"questions": self._parse(card.get("Frontside") or u""),
				"answers": self._parse(card.get("Backside") or u""),
			}
			created = card.get("DateCreated")
			if created:
				item["created"] = self._parseDate(created)
			items.append(item)

		return {
			"resources": {},
			"list": {
				"items": sorted(items, key=lambda item: item.get("created")),
				"tests": [],
			},
		}

	def _retranslate(self):
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		#TRANSLATORS: This is one of the file formats OpenTeacher can
		#TRANSLATORS: read. See for more info:
		#TRANSLATORS: http://sourceforge.net/projects/jmemorize/
		self.name = _("jMemorize")

	def enable(self):
		self.loads = {"jml": ["words"]}
		self.mimetype = "application/x-jmemorizelesson"

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

def init(moduleManager):
	return JMemorizeLessonLoaderModule(moduleManager)
