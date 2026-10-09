#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2012, Cas Widdershoven
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

from PyQt4 import QtGui, QtCore

class HangmanGraphics(QtGui.QWidget):
	def __init__(self):
		super(HangmanGraphics, self).__init__()
		self.setMinimumSize(300, 200)
		self.mistakes = 0

	def paintEvent(self, e):
		self.qp = QtGui.QPainter()

		self.qp.begin(self)        
		self.initDraw()
		self.qp.end()
        
	def initDraw(self):
		pen = QtGui.QPen(QtCore.Qt.black, 2, QtCore.Qt.SolidLine)

		self.qp.setPen(pen)

		self.qp.drawLine(20, 190, 280, 190)
		self.qp.drawLine(60, 190, 60, 20)
		self.qp.drawLine(20, 190, 60, 150)
		self.qp.drawLine(100, 190, 60, 150)
		self.qp.drawLine(60, 20, 190, 20)
		self.qp.drawLine(60, 60, 100, 20)
		self.qp.drawLine(190, 20, 190, 40)

		if self.mistakes >= 1:
			self.qp.drawEllipse(178, 40, 24, 24)	
		if self.mistakes >= 2:
			self.qp.drawLine(190, 63, 190, 120)
		if self.mistakes >= 3:
			self.qp.drawLine(190, 120, 144, 166)
		if self.mistakes >= 4:
			self.qp.drawLine(190, 120, 236, 166)
		if self.mistakes >= 5:
			self.qp.drawLine(190, 63, 144, 109)
		if self.mistakes >= 6:
			self.qp.drawLine(190, 63, 236, 109)
			self.qp.drawLine(185, 47, 189, 51)
			self.qp.drawLine(185, 51, 189, 47)
			self.qp.drawLine(191, 51, 195, 47)
			self.qp.drawLine(191, 47, 195, 51)
			self.qp.drawLine(185, 56, 195, 56)
