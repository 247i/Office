#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2009-2011, Marten de Vries
#	Copyright 2008-2011, Milan Boers
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

class GreekModule(object):
	"""Keeps a list of all greek characters in table format in the
	   'data' attribute, and the (translated) term 'Greek' in the
	   name attribute.

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(GreekModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "chars"
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("greek.py",)
		self.priorities = {
			"default": 160,
		}

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.data = (
			(u"α", u"Α", u"β", u"Β", u"γ", u"Γ"),
			(u"δ", u"Δ", u"ε", u"Ε", u"ζ", u"Ζ"),
			(u"η", u"Η", u"θ", u"Θ", u"ι", u"Ι"),
			(u"κ", u"Κ", u"λ", u"Λ", u"μ", u"Μ"),
			(u"ν", u"Ν", u"ξ", u"Ξ", u"ο", u"Ο"),
			(u"π", u"Π", u"ρ", u"Ρ", u"σ", u"Σ"),
			(u"ς", u"τ", u"Τ", u"υ", u"Υ", u"φ"),
			(u"Φ", u"χ", u"Χ", u"ψ", u"Ψ", u"ω"),
			(u"Ω", u"῾", u"᾿", u"", u"", u""),
		)
		self.active = True

	def _retranslate(self):
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		self.name = _("Greek")

	def disable(self):
		self.active = False

		del self._modules
		del self.name
		del self.data

def init(moduleManager):
	return GreekModule(moduleManager)
