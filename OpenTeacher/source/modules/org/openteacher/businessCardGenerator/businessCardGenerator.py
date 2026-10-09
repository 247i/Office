#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2012, Cas Widdershoven
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

import sys

class BusinessCardGeneratorModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(BusinessCardGeneratorModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "businessCardGenerator"
		self.requires = (
			self._mm.mods(type="backgroundImageGenerator"),
			self._mm.mods(type="ui"),
			self._mm.mods(type="execute"),
		)
		self.priorities = {
			"default": -1,
			"generate-business-card": 0,
		}

	def _run(self):
		try:
			path = sys.argv[1]
		except IndexError:
			print >> sys.stderr, "Please specify a path where the business card image can be saved as last command line argument (ending in .png)."
			return
		w = 640
		h = 320
		extraTopMargin = 40
		margin = 35

		img = QtGui.QImage(w, h, QtGui.QImage.Format_ARGB32_Premultiplied)
		img.fill(QtCore.Qt.white)
		painter = QtGui.QPainter(img)

		#draw background
		background = self._generateBackground()
		background = background.scaledToWidth(w, QtCore.Qt.SmoothTransformation)

		painter.drawImage(0, 0, background)

		#draw text
		painter.translate(0, extraTopMargin)

		color = QtGui.QColor("#3B4D55")

		doc = QtGui.QTextDocument()
		doc.setDocumentMargin(margin)
		doc.setDefaultStyleSheet("""
			div {
				font-family: Verdana;
				font-size: 17pt;
				color: %s;
			}
		""" % color.name())

		doc.setHtml("""
			<div>
				<strong style='font-size: 19pt;'>OpenTeacher</strong><br />
				Free open source exam training software<br /><br />

				Get it here:<br />
				http://openteacher.org/<br /><br />

				Or contact us at:<br />
				info@openteacher.org
			</div>
		""")
		doc.setTextWidth(w)
		doc.drawContents(painter)

		painter.end()
		img.save(path)

	@property
	def _generateBackground(self):
		return self._modules.default("active", type="backgroundImageGenerator").generate

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		self._modules = next(iter(self._mm.mods(type="modules")))
		self._modules.default("active", type="execute").startRunning.handle(self._run)

		self.active = True

	def disable(self):
		self.active = False

		del self._modules

def init(moduleManager):
	return BusinessCardGeneratorModule(moduleManager)
