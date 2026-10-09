#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2012, Marten de Vries
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

def getGraph():
	class Graph(QtGui.QWidget):
		BAR_SIZE = 50
		SPACING = 20
		FONT_MARGIN = 5

		def __init__(self, notes, *args, **kwargs):
			super(Graph, self).__init__(*args, **kwargs)

			self._notes = notes

			self.setSizePolicy(
				QtGui.QSizePolicy.MinimumExpanding,
				QtGui.QSizePolicy.Minimum
			)

		def sizeHint(self):
			w = len(self._notes) * self.BAR_SIZE + len(self._notes) * self.SPACING
			h = self.fontMetrics().height() + 2 * self.FONT_MARGIN
			return QtCore.QSize(w, h)

		def paintEvent(self, e):
			h = self.height()
			w = self.width()

			p = QtGui.QPainter()
			p.begin(self)

			#draw the bars
			p.setBrush(self.palette().highlight())

			horPos = int(round(self.SPACING / 2.0))
			for note in self._notes:
				barHeight = int(round(note / 100.0 * h))
				p.setPen(QtCore.Qt.NoPen)
				p.drawRect(horPos, h, self.BAR_SIZE, -barHeight)
				p.setPen(QtGui.QPen(self.palette().highlightedText()))
				text = "%s%%" % note
				y = h - self.FONT_MARGIN
				#center on the bar
				x = horPos + self.BAR_SIZE / 2.0 - self.fontMetrics().width(text) / 2.0
				p.drawText(x, y, text)
				horPos += self.BAR_SIZE + self.SPACING

			p.end()
	return Graph

def getPercentNotesViewer():
	class PercentNotesViewer(QtGui.QScrollArea):
		def __init__(self, notes, *args, **kwargs):
			super(PercentNotesViewer, self).__init__(*args, **kwargs)

			self.setFrameStyle(QtGui.QFrame.NoFrame)

			graph = Graph(notes)
			self.setWidget(graph)

		def resizeEvent(self, *args, **kwargs):
			graphHeight = self.viewport().height()
			self.widget().resize(self.widget().width(), graphHeight)

			super(PercentNotesViewer, self).resizeEvent(*args, **kwargs)
	return PercentNotesViewer

class PercentNotesViewerModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(PercentNotesViewerModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "percentNotesViewer"
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="percentsCalculator"),
		)

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		global Graph, PercentNotesViewer
		Graph = getGraph()
		PercentNotesViewer = getPercentNotesViewer()

		self._modules = set(self._mm.mods(type="modules")).pop()

		self.active = True

	def _percentNotesFor(self, tests):
		calculatePercents = self._modules.default(
			"active",
			type="percentsCalculator"
		).calculatePercents
		return map(calculatePercents, tests)

	def createPercentNotesViewer(self, tests, *args, **kwargs):
		return PercentNotesViewer(self._percentNotesFor(tests), *args, **kwargs)

	def disable(self):
		self.active = False

		del self._modules

def init(moduleManager):
	return PercentNotesViewerModule(moduleManager)
