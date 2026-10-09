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

class ForeignKnownModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(ForeignKnownModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "itemModifier"
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("foreignKnown.py",)

	def modifyItem(self, item):
		#modify in place, because the caller is responsible for passing
		#a copy of item.
		item["questions"], item["answers"] = item.get("answers", []), item.get("questions", [])
		return item

	def enable(self):
		self.dataType = "words"

		self._modules = set(self._mm.mods(type="modules")).pop()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)

		#TRANSLATORS: This is an option. When checked, OT asks the
		#TRANSLATORS: answers and expects from you to give the
		#TRANSLATORS: corresponding questions.
		self.name = _("Ask foreign - known")
		self.active = True

	def disable(self):
		self.active = False

		del self.dataType
		del self._modules
		del self.name

def init(moduleManager):
	return ForeignKnownModule(moduleManager)
