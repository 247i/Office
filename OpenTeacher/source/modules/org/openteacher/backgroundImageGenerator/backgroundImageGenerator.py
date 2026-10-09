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

class BackgroundImageGeneratorModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(BackgroundImageGeneratorModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "backgroundImageGenerator"
		self.requires = (
			self._mm.mods(type="metadata"),
			self._mm.mods(type="ui"),
		)

	def generate(self):
		"""Generate the body background, which includes:
		    - a rounded lighter area, on which the content is shown
		    - the logo
		    - the application name

		"""
		#set some values
		width = 1000
		height = 5000
		sideMargin = 27
		topMargin = 64

		xRadius = 9
		yRadius = xRadius * 0.7
		topLineY = 94

		logoTopX = 6
		logoSize = 107

		textXStart = 124
		textYBaseline = 58

		#determine colors
		textColor = QtGui.QColor.fromHsv(self._hue, 119, 47)
		gradientTopColor = QtGui.QColor.fromHsv(self._hue, 7, 253)
		gradientBottomColor = QtGui.QColor.fromHsv(self._hue, 12, 243)

		#create image
		img = QtGui.QImage(width, height, QtGui.QImage.Format_ARGB32_Premultiplied)
		img.fill(QtCore.Qt.transparent)

		gradient = QtGui.QLinearGradient(0, 0, 0, height)
		gradient.setColorAt(0, gradientTopColor)
		gradient.setColorAt(1, gradientBottomColor)

		font = QtGui.QFont("Verdana", 37)
		font.setWeight(55)
		font.setLetterSpacing(QtGui.QFont.PercentageSpacing, 95)

		smallFont = QtGui.QFont(font)
		smallFont.setPointSize(smallFont.pointSize() - 8)

		painter = QtGui.QPainter(img)
		painter.setPen(self.lineColor)
		painter.setBrush(gradient)
		painter.drawRoundedRect(
			sideMargin,
			topMargin,
			width - sideMargin * 2,
			height,
			xRadius,
			yRadius
		)
		painter.drawLine(
			sideMargin,
			topLineY,
			width - sideMargin,
			topLineY
		)
		painter.drawImage(
			QtCore.QPoint(logoTopX, 0),
			QtGui.QImage(self._logo).scaledToHeight(logoSize, QtCore.Qt.SmoothTransformation)
		)

		textPen = QtGui.QColor(textColor)
		textPen.setAlpha(200)
		painter.setPen(textPen)
		painter.setFont(font)
		textXPos = textXStart
		painter.drawText(textXPos, textYBaseline, "O")
		textXPos += QtGui.QFontMetrics(font).width("O")
		painter.setFont(smallFont)
		painter.drawText(textXPos, textYBaseline, "PEN")
		textXPos += QtGui.QFontMetrics(smallFont).width("PEN")
		painter.setFont(font)
		painter.drawText(textXPos, textYBaseline, "T")
		textXPos += QtGui.QFontMetrics(font).width("T")
		painter.setFont(smallFont)
		painter.drawText(textXPos, textYBaseline, "EACHER")
		painter.end()

		return img

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		modules = next(iter(self._mm.mods(type="modules")))
		metadata = modules.default("active", type="metadata").metadata
		self._hue = metadata["mainColorHue"]
		self._logo = metadata["iconPath"]

		self.lineColor = QtGui.QColor.fromHsv(self._hue, 28, 186)

		self.active = True

	def disable(self):
		self.active = False

		del self._hue
		del self._logo
		del self.lineColor

def init(moduleManager):
	return BackgroundImageGeneratorModule(moduleManager)
