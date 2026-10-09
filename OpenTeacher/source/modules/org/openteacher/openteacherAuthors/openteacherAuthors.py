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

class OpenTeacherAuthorsModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(OpenTeacherAuthorsModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "openteacherAuthors"
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.requires = (
			self._mm.mods(type="authors"),
		)
		self.filesWithTranslations = ("openteacherAuthors.py",)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()

		self._authors = self._modules.default("active", type="authors")
		self._removers = set()

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

	def _retranslate(self):
		#setup translation
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)

		a = self._authors
		r = self._removers

		for remove in self._removers.copy():
			#remove all authors with the wrong translated roles
			remove()
			self._removers.remove(remove)

		#Add all the contributors. With their newly translated role

		#Core development team
		r.add(a.registerAuthor(_("Core developer"), u"Milan Boers"))
		r.add(a.registerAuthor(_("Core developer"), u"Cas Widdershoven"))
		r.add(a.registerAuthor(_("Core developer"), u"Marten de Vries"))

		#Patches
		r.add(a.registerAuthor(_("Patches contributor"), u"Roel Huybrechts"))
		r.add(a.registerAuthor(_("Patches contributor"), u"David D Lowe"))

		#Packaging
		r.add(a.registerAuthor(_("Debian/Ubuntu packager"), u"Charlie Smotherman"))

		#Artwork
		r.add(a.registerAuthor(_("Artwork"), u"Yordi de Graaf"))
		r.add(a.registerAuthor(_("Artwork"), u"Oxygen icon theme"))
		r.add(a.registerAuthor(_("Topography maps"), u"Wikimedia Commons"))

		#IRC channel spammers
		r.add(a.registerAuthor(_("Chat channel spammer"), u"Stefan de Vries"))

		#Bug hunters
		r.add(a.registerAuthor(_("Bug hunter"), u"Michael Tel"))

		#Translators
		#This section can be auto-generated with the following command:
		#python openteacher.py -p get-translation-authors
		r.add(a.registerAuthor(_("Translator (%s)") % "Afrikaans", u"computergeoffrey"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Arabic", u"Aminos Amigos"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Arabic", u"El Achèche ANIS"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Arabic", u"Slim KSOURI"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Brazilian Portuguese", u"Adriano Steffler"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Brazilian Portuguese", u"Marcelo Thomaz"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Brazilian Portuguese", u"Rubens Bueno"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Chinese (Simplified)", u"Ricardo Conde"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Chinese (Simplified)", u"Wang Dianjin"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Chinese (Simplified)", u"adam liu"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Chinese (Traditional)", u"Louie Chen"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Czech", u"Jakub Šnapka"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Czech", u"Jan Havran"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Czech", u"Jan Žárský"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Czech", u"Pavol_Ondercin"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Dutch", u"Cas Widdershoven"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Dutch", u"Michael Tel"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Dutch", u"Willem Sonke"))
		r.add(a.registerAuthor(_("Translator (%s)") % "English (Australia)", u"Joel Pickett"))
		r.add(a.registerAuthor(_("Translator (%s)") % "English (United Kingdom)", u"Andi Chandler"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Esperanto", u"Michael Moroni"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Finnish", u"Teemu Paavola"))
		r.add(a.registerAuthor(_("Translator (%s)") % "French", u"EmmanuelLeNormand"))
		r.add(a.registerAuthor(_("Translator (%s)") % "French", u"Flames_in_Paradise"))
		r.add(a.registerAuthor(_("Translator (%s)") % "French", u"Florent (LSc)"))
		r.add(a.registerAuthor(_("Translator (%s)") % "French", u"Glyca"))
		r.add(a.registerAuthor(_("Translator (%s)") % "French", u"Hélion du Mas des Bourboux"))
		r.add(a.registerAuthor(_("Translator (%s)") % "French", u"Kcchouette"))
		r.add(a.registerAuthor(_("Translator (%s)") % "French", u"Messer Kevin"))
		r.add(a.registerAuthor(_("Translator (%s)") % "French", u"Pierre Slamich"))
		r.add(a.registerAuthor(_("Translator (%s)") % "French", u"SOMDA Sâaviel Constant"))
		r.add(a.registerAuthor(_("Translator (%s)") % "French", u"SarahSlean"))
		r.add(a.registerAuthor(_("Translator (%s)") % "French", u"Stanislas Michalak"))
		r.add(a.registerAuthor(_("Translator (%s)") % "French", u"Sylvie Gallet"))
		r.add(a.registerAuthor(_("Translator (%s)") % "French", u"YannUbuntu"))
		r.add(a.registerAuthor(_("Translator (%s)") % "French", u"c3d"))
		r.add(a.registerAuthor(_("Translator (%s)") % "French", u"pou"))
		r.add(a.registerAuthor(_("Translator (%s)") % "French", u"ymadec"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Frisian", u"Marten de Vries"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Galician", u"Miguel Anxo Bouzada"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Galician", u"Xosé"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Galician", u"ghas"))
		r.add(a.registerAuthor(_("Translator (%s)") % "German", u"Alexander Haack"))
		r.add(a.registerAuthor(_("Translator (%s)") % "German", u"Daniel Winzen"))
		r.add(a.registerAuthor(_("Translator (%s)") % "German", u"Dennis Baudys"))
		r.add(a.registerAuthor(_("Translator (%s)") % "German", u"Hans Schmidt"))
		r.add(a.registerAuthor(_("Translator (%s)") % "German", u"Jonatan Zeidler"))
		r.add(a.registerAuthor(_("Translator (%s)") % "German", u"Macedon"))
		r.add(a.registerAuthor(_("Translator (%s)") % "German", u"Maximilian Mühlbauer"))
		r.add(a.registerAuthor(_("Translator (%s)") % "German", u"Phillip Sz"))
		r.add(a.registerAuthor(_("Translator (%s)") % "German", u"Raffael Menke"))
		r.add(a.registerAuthor(_("Translator (%s)") % "German", u"Simon Schütte"))
		r.add(a.registerAuthor(_("Translator (%s)") % "German", u"Tim O."))
		r.add(a.registerAuthor(_("Translator (%s)") % "German", u"dagmalina"))
		r.add(a.registerAuthor(_("Translator (%s)") % "German", u"dubst3pp4"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Greek", u"Basilis Thomopoulos"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Greek", u"Yannis Kaskamanidis"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Greek", u"Yannis Kaskamanidis"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Greek", u"nask00s"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Hungarian", u"Molnár Krisztián"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Hungarian", u"Richard Somlói"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Italian", u"Guybrush88"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Italian", u"Leonardo Corato"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Italian", u"Pierdomenico"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Japanese", u"LeeAnna Kobayashi"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Polish", u"Michał Kudela"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Polish", u"pp/bs"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Russian", u"AleXanDeR_G"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Russian", u"Dasha"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Russian", u"Egor Bushmelyov"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Russian", u"Nkolay Parukhin"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Russian", u"facepalm"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Sinhalese", u"Mohamed Rizmi"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Sinhalese", u"Sameera Nelson"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Sinhalese", u"පසිඳු කාවින්ද"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Slovak", u"Alexander Suchan"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Spanish", u"A. Byrne"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Spanish", u"Adolfo Jayme Barrientos"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Spanish", u"Aiguanachein"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Spanish", u"Alfredo Hernández"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Spanish", u"Eduardo Alberto Calvo"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Spanish", u"Hector A. Mantellini"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Spanish", u"Javier Blanco"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Spanish", u"Mariano Noguera"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Spanish", u"Miguel A. Alvarado V."))
		r.add(a.registerAuthor(_("Translator (%s)") % "Spanish", u"Rose"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Spanish", u"Shaun Mallette"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Spanish", u"Ubuntu"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Spanish", u"Victor Rodriguez Cavaliere"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Spanish", u"Yury Jajitzky"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Spanish", u"emerling"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Spanish", u"gustavoreyes"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Turkish", u"kodadiirem"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Turkish", u"oldumulenone"))
		r.add(a.registerAuthor(_("Translator (%s)") % "Turkish", u"zeugma"))

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self._authors
		del self._removers

def init(moduleManager):
	return OpenTeacherAuthorsModule(moduleManager)
