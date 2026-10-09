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

import os

class UserDocumentationModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(UserDocumentationModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "userDocumentation"
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("getting-started.html",)

	@property
	def availableTranslations(self):
		"""All available languages in which the documentation is
		   translated. (English, the default, isn't included)

		"""
		paths = os.listdir(self._mm.resourcePath("translations"))
		return (os.path.splitext(p)[0] for p in paths if p.endswith(".po"))

	def getHtml(self, resourceUrl, lang=None):
		"""Returns the user documentation as an html snippet. All links
		   to resources (e.g. images) will be pointing to
		   ``resourceUrl``/resourceName. In other words, the caller
		   should make sure all files in ``self.resourcesPath`` are
		   available on the ``resourceUrl`` in some way.

		   The snippet will be in the language ``lang`` if available.
		   (``lang`` should be passable to the translator module.) If
		   lang is None, it will use the current language of
		   OpenTeacher.

		"""
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations"),
				lang
			)

		return self._template(**{
			"resourceUrl": resourceUrl,
			"tr": _,
		})

	def enable(self):
		try:
			import pyratemp
		except ImportError:
			#remain inactive
			return
		self._modules = next(iter(self._mm.mods(type="modules")))

		self.resourcesPath = self._mm.resourcePath("static")
		self._template = pyratemp.Template(filename=self._mm.resourcePath("getting-started.html"))

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self.resourcesPath
		del self._template

def init(moduleManager):
	return UserDocumentationModule(moduleManager)
