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

import math
import random

def installQtClasses():
	global KeyboardWidget

	class KeyboardWidget(QtGui.QWidget):
		"""An onscreen keyboard view. Make sure you call
		   setKeyboardLayout() before showing the widget (otherwise
		   you'll see nothing.)

		"""
		#15 per row
		SIZE_MAP = [
			#tuples: (start_position, relative_size, finger_number)
			[(0, 1, 1), (1, 1, 1), (2, 1, 2), (3, 1, 3), (4, 1, 4), (5, 1, 4), (6, 1, 7), (7, 1, 7), (8, 1, 8), (9, 1, 9), (10, 1, 10), (11, 1, 10), (12, 1, 10), (13, 2, 10)],
			[(0, 1.5, 1), (1.5, 1, 1), (2.5, 1, 2), (3.5, 1, 3), (4.5, 1, 4), (5.5, 1, 4), (6.5, 1, 7), (7.5, 1, 7), (8.5, 1, 8), (9.5, 1, 9), (10.5, 1, 10), (11.5, 1, 10), (12.5, 1, 10), (13.5, 1.5, 10)],
			[(0, 2, 1), (2, 1, 1), (3, 1, 2), (4, 1, 3), (5, 1, 4), (6, 1, 4), (7, 1, 7), (8, 1, 7), (9, 1, 8), (10, 1, 9), (11, 1, 10), (12, 1, 10), (13, 1, 10), (14, 1, 10)],
			[(0, 1.5, 1), (1.5, 1, 1), (2.5, 1, 1), (3.5, 1, 2), (4.5, 1, 3), (5.5, 1, 4), (6.5, 1, 4), (7.5, 1, 7), (8.5, 1, 7), (9.5, 1, 8), (10.5, 1, 9), (11.5, 1, 10), (12.5, 2.5, 10)],
			[(1.5, 12, (5, 6))],
		]

		_golden_ratio_conjugate = 1.6180339887498948482

		def __init__(self, *args, **kwargs):
			super(KeyboardWidget, self).__init__(*args, **kwargs)

			self._currentKey = None
			self._wrongKey = None
			self.setSizePolicy(
				QtGui.QSizePolicy.Expanding,
				QtGui.QSizePolicy.Expanding
			)
			self._h = random.random()
			self._cache = {}
			self._layout = None

		def _colorForFinger(self, finger):
			if finger == (5, 6):
				#I like a non-colored space bar
				return QtCore.Qt.lightGray
			if not finger in self._cache:
				self._cache[finger] = self._nextColor()
			return self._cache[finger]

		def _nextColor(self):
			#calculates a new color, as distinctive from the others as possible
			#credits: http://martin.ankerl.com/2009/12/09/how-to-create-random-colors-programmatically/
			self._h = (self._h + self._golden_ratio_conjugate) % 1
			return QtGui.QColor.fromHsvF(self._h, 0.3, 0.9)

		def paintEvent(self, event):
			if not self._layout:
				#not ready for drawing.
				return
			#make the keyboard as large as possible, but don't let it
			#be partly drawn outside the visible widget area.
			widthCellSize = int(math.floor(self.width() / 15.0)) -1
			heightCellSize = int(math.floor(self.height() / 5.0)) -1
			cellSize = min(widthCellSize, heightCellSize)

			p = QtGui.QPainter()
			p.begin(self)

			for rowNumber, row in enumerate(self.SIZE_MAP):
				y = rowNumber * cellSize
				height = cellSize
				for columnNumber, column in enumerate(row):
					x = cellSize * column[0]
					width = cellSize * column[1]
					finger = column[2]
					text = self._layout[rowNumber][columnNumber]

					#set key background color
					p.setBrush(self._colorForFinger(finger))
					if text == self._currentKey:
						p.setBrush(QtCore.Qt.black)
					elif text == self._wrongKey:
						p.setBrush(QtCore.Qt.red)

					#draw the key background
					p.drawRect(x, y, width, height)

					#if this is the enter key we're drawing, remove the
					#line which separates the two parts of it now the
					#last part of it is drawn.
					if rowNumber +1 == 3 and columnNumber == len(row) -1:
						p.setPen(self._colorForFinger(finger))
						#x + 1 because it looks better
						p.drawLine(x + 1, y, x + width, y)
						p.setPen(QtGui.QPen())

					#reset the background color
					p.setBrush(QtGui.QBrush())
					if text in (self._currentKey, self._wrongKey):
						#set the text color
						p.setPen(QtCore.Qt.white)
					#draw the text onto the key
					p.drawText(QtCore.QRect(x, y, width, height), QtCore.Qt.AlignCenter, text)
					#reset the text color to the default
					p.setPen(QtGui.QPen())

			p.end()

		def setCurrentKey(self, key):
			self._currentKey = key
			self.update()

		def setWrongKey(self, key):
			self._wrongKey = key
			self.update()

		def sizeHint(self):
			return QtCore.QSize(500, 210)

		def setKeyboardLayout(self, layout):
			self._layout = layout
			self.update()

class TypingTutorKeyboardModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TypingTutorKeyboardModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "typingTutorKeyboard"
		self.requires = (
			self._mm.mods(type="ui"),
		)

	def createKeyboardWidget(self, *args, **kwargs):
		return KeyboardWidget(*args, **kwargs)

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return

		installQtClasses()

		self.active = True

	def disable(self):
		self.active = False

def init(moduleManager):
	return TypingTutorKeyboardModule(moduleManager)
