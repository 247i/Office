#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2013, Marten de Vries
#	Copyright 2011, Milan Boers
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

class MediaHtmlGeneratorModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(MediaHtmlGeneratorModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "mediaHtmlGenerator"

	def generate(self, lesson, name="", margin="0"):
		templatePath = self._mm.resourcePath("template.html")
		t = pyratemp.Template(filename=templatePath)
		return t(**{
			"list": lesson.list,
			"name": name,
			"margin": margin,
		})

	def enable(self):
		global pyratemp
		try:
			import pyratemp
		except ImportError:
			return #remain inactive

		self.active = True

	def disable(self):
		self.active = False

def init(moduleManager):
	return MediaHtmlGeneratorModule(moduleManager)
