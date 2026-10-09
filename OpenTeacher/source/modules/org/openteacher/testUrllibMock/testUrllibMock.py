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

import urllib2
import StringIO
import logging

logger = logging.getLogger(__name__)

class MockOpener(object):
	def addheaders(self, headers):
		pass

	def open(self, request):
		if request.get_method() == "HEAD":
			return StringIO.StringIO()

		if request.get_full_url() == "http://www.wrts.nl/api/lists":
			return StringIO.StringIO('<?xml version="1.0" encoding="UTF-8"?><list-index />')

class TestUrllibMockModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestUrllibMockModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.priorities = {
			"test-suite": 0,
			"default": -1,
		}

	def _mockedUrlopen(self, url):
		logger.debug("url: %s" % url)
		if url.startswith("http://www.studystack.com/servlet/categoryListJson"):
			result = "[]"
		elif url.startswith("http://vocatrain.com/api/select_categories.php") or url.startswith("http://woordjesleren.nl/api/select_categories.php"):
			result = '<?xml version="1.0" encoding="UTF-8"?><woordjesleren version="1"><categories></categories></woordjesleren>'
		logger.debug("response: %s" % result)

		return StringIO.StringIO(result)

	def _mockedBuildOpener(self):
		return MockOpener()

	def enable(self):
		self._defaultUrlopen = urllib2.urlopen
		self._defaultBuildOpener = urllib2.build_opener

		urllib2.urlopen = self._mockedUrlopen
		urllib2.build_opener = self._mockedBuildOpener

		self.active = True

	def disable(self):
		self.active = False

		urllib2.urlopen = self._defaultUrlopen
		urllib2.build_opener = self._defaultBuildOpener

		del self._defaultUrlopen
		del self._defaultBuildOpener

def init(moduleManager):
	return TestUrllibMockModule(moduleManager)
