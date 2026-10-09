#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2012-2013, Marten de Vries
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

import urllib2
import sys

class GetTranslationAuthorsModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(GetTranslationAuthorsModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "getTranslationAuthors"
		self.requires = (
			self._mm.mods(type="execute"),
		)
		self.priorities = {
			"get-translation-authors": 0,
			"default": -1,
		}

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._modules.default(type="execute").startRunning.handle(self._run)

		self.active = True

	def _translationFileLinks(self, lp):
		series = lp.projects["openteacher"].getSeries(name="3.x")
		for template in series.getTranslationTemplates():
			if not template.active:
				continue
			for translationFile in template.translation_files:
				yield translationFile.web_link + "/+details"
			print "processing template"

	def _personsForFile(self, link):
		print "downloading %s:" % link
		data = unicode(urllib2.urlopen(link).read(), encoding="UTF-8")
		doc = lxml.html.document_fromstring(data)
		language = doc.cssselect("span.sprite.language")[0].text_content()
		for person in doc.cssselect(".portlet ul li a.sprite.person"):
			yield person.get("href"), (language, person.text_content())

	def _run(self):
		global lxml
		try:
			from launchpadlib.launchpad import Launchpad
			import lxml.html
		except ImportError:
			sys.stderr.write("For this developer profile to work, you need launchpadlib and lxml to be installed.\n")
			return
		a = raw_input("Please only use this script if you want to update the openteacherAuthors module, since this script puts a lot of load on launchpad and your internet connection, and takes a lot of time to execute. Continue (y/n)? ")
		if a != "y":
			return

		lp = Launchpad.login_anonymously("Get OpenTeacher translators", "production", "~/.launchpadlib/cache/")
		links = self._translationFileLinks(lp)

		persons = dict(
			(href, info)
			for link in links
			for href, info in self._personsForFile(link)
		)

		print "\nResults:\n"

		for l, p in sorted(persons.values()):
			print '		r.add(a.registerAuthor(_("Translator (%%s)") %% "%s", u"%s"))' % (l, p)

	def disable(self):
		self.active = False

		del self._modules

def init(moduleManager):
	return GetTranslationAuthorsModule(moduleManager)
