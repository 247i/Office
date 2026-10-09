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

class MimicryTypefaceConverterModule(object):
	"""Supported mimicry fonts:
	   - Greek
	   - TekniaGreek

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(MimicryTypefaceConverterModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "mimicryTypefaceConverter"

	def convert(self, font, text):
		"""If 'font' is a known mimicry font, all letters in 'text' are
		   converted into their unicode equivalent. Unknown letters just
		   remain the same.

		"""
		fontTable = {
			#Symbol font (Greek chars)
			"symbol": {
				#Source: http://en.wikipedia.org/wiki/Symbol_%28typeface%29#Font_comparison
				#lowercase
				u"a": u"α",
				u"b": u"β",
				u"g": u"γ",
				u"d": u"δ",
				u"e": u"ε",
				u"z": u"ζ",
				u"h": u"η",
				u"q": u"θ",
				u"i": u"ι",
				u"k": u"κ",
				u"l": u"λ",
				u"m": u"μ",
				u"n": u"ν",
				u"x": u"ξ",
				u"o": u"ο",
				u"p": u"π",
				u"r": u"ρ",
				u"V": u"ς",
				u"s": u"σ",
				"t": u"τ",
				u"u": u"υ",
				u"f": u"φ",
				u"c": u"χ",
				u"y": u"ψ",
				u"w": u"ω",

				#uppercase
				u"A": u"Α",
				u"B": u"Β",
				u"G": u"Γ",
				u"D": u"Δ",
				u"E": u"Ε",
				u"Z": u"Ζ",
				u"H": u"Η",
				u"Q": u"Θ",
				u"I": u"Ι",
				u"K": u"Κ",
				u"L": u"Λ",
				u"M": u"Μ",
				u"N": u"Ν",
				u"X": u"Ξ",
				u"O": u"Ο",
				u"P": u"Π",
				u"R": u"Ρ",
				u"S": u"Σ",
				u"T": u"Τ",
				u"U": u"Υ",
				u"F": u"Φ",
				u"C": u"Χ",
				u"Y": u"Ψ",
				u"W": u"Ω",
			},
		}
		#Greek font (as supplied by Teach2000)
		fontTable["greek"] = fontTable["symbol"]
		fontTable["greek"].update({
			u"j": u"ς",
			u"v": u"ᾳ",
			u"J": u"ῷ",
			u"V": u"ῃ",
		})
		#TekniaGreek. This might not be accurate, but better than
		#nothing...
		fontTable["tekniagreek"] = fontTable["greek"]

		font = font.lower()
		letterTable = fontTable.get(font, {})

		return "".join((letterTable.get(letter, letter) for letter in text))

	def enable(self):
		self.active = True

	def disable(self):
		self.active = False

def init(moduleManager):
	return MimicryTypefaceConverterModule(moduleManager)
