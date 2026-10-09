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

import datetime
import dateutil
import weakref

def installQtClasses():
	global Graph, ProgressViewer

	class Graph(QtGui.QFrame):
		def __init__(self, test, *args, **kwargs):
			"""Raises KeyError if 'test' doesn't contain time info."""

			super(Graph, self).__init__(*args, **kwargs)
			
			self._test = test

			self.setSizePolicy(
				QtGui.QSizePolicy.Expanding,
				QtGui.QSizePolicy.MinimumExpanding
			)
			
			self.setFrameStyle(QtGui.QFrame.StyledPanel)
			self.setFrameShadow(QtGui.QFrame.Sunken)

			self.start = self._test["results"][0]["active"]["start"]
			self.end = self._test["results"][-1]["active"]["end"]
			self._totalSeconds = dateutil.total_seconds(self.end - self.start)

		@property
		def _amountOfUniqueItems(self):
			ids = set()
			for result in self._test["results"]:
				ids.add(result["itemId"])
			return len(ids)

		def event(self, event, *args, **kwargs):
			if event.type() == QtCore.QEvent.ToolTip:
				second = event.x() / self._secondsPerPixel
				moment = self.start + datetime.timedelta(seconds=second)
				for pause in self._test["pauses"]:
					if pause["start"] < moment and pause["end"] > moment:
						text = _("Pause")
						break
				try:
					text
				except NameError:
					for result in self._test["results"]:
						if result["active"]["start"] < moment and result["active"]["end"] > moment:
							text = _("Thinking")
				try:
					text
				except NameError:
					text = _("Answering")
				QtGui.QToolTip.showText(
					event.globalPos(),
					text,
				)
				return True
			return super(Graph, self).event(event, *args, **kwargs)

		def _paintItem(self, p, item):
			x = dateutil.total_seconds(item["start"] - self.start) * self._secondsPerPixel
			width = dateutil.total_seconds(item["end"] - item["start"]) * self._secondsPerPixel

			p.drawRect(x, 0, width, self._h)

		def paintEvent(self, event, *args, **kwargs):
			p = QtGui.QPainter()
			p.begin(self)
			
			p.setPen(QtCore.Qt.NoPen)

			w = self.width()
			self._h = self.height()

			try:
				#float, because one pixel might be more than one second.
				#When int was used, secondsPerPixel could become 0 showing
				#nothing in that case.
				self._secondsPerPixel = float(w) / self._totalSeconds
			except ZeroDivisionError:
				self._secondsPerPixel = 0
			colors = {}
			baseColor = self.palette().highlight().color()
			steps = 0
			colorDifference = (255 - baseColor.lightness()) / (self._amountOfUniqueItems +1)#+1 so it doesn't become 0
			for result in self._test["results"]:
				try:
					p.setBrush(QtGui.QBrush(colors[result["itemId"]]))
				except KeyError:
					color = QtGui.QColor(baseColor)
					hsl = list(color.getHsl())
					hsl[2] = hsl[2] + colorDifference * steps
					color.setHsl(*hsl)

					steps += 1

					colors[result["itemId"]] = QtGui.QBrush(color)
					p.setBrush(colors[result["itemId"]])

				if "active" in result:
					self._paintItem(p, result["active"])

			p.setBrush(self.palette().dark())
			for pause in self._test.get("pauses", []):
				self._paintItem(p, pause)

			p.setBrush(QtGui.QBrush())

			p.end()
			super(Graph, self).paintEvent(event, *args, **kwargs)

		def sizeHint(self):
			return QtCore.QSize(200, 30)

	class ProgressViewer(QtGui.QWidget):
		def __init__(self, test, *args, **kwargs):
			"""Raises KeyError if 'test' doesn't contain time info."""

			super(ProgressViewer, self).__init__(*args, **kwargs)

			self.graph = Graph(test)
			format = "%X"
			firstTime = QtGui.QLabel(self.graph.start.strftime(format))
			lastTime = QtGui.QLabel(self.graph.end.strftime(format))
			
			horLayout = QtGui.QHBoxLayout()
			horLayout.addWidget(firstTime)
			horLayout.addStretch()
			horLayout.addWidget(lastTime)
			
			mainLayout = QtGui.QVBoxLayout()
			mainLayout.addLayout(horLayout)
			mainLayout.addWidget(self.graph)
			
			self.setLayout(mainLayout)

class ProgressViewerModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(ProgressViewerModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "progressViewer"

		self.requires = (
			self._mm.mods(type="ui"),
		)
		self.filesWithTranslations = ("progressViewer.py",)

	def createProgressViewer(self, *args, **kwargs):
		pv = ProgressViewer(*args, **kwargs)
		self._progressViewers.add(weakref.ref(pv))
		return pv

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		installQtClasses()

		self._modules = set(self._mm.mods(type="modules")).pop()
		self._progressViewers = set()

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

	def _retranslate(self):
		#Translations
		global _
		global ngettext

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)

	def disable(self):
		self.active = False

		del self._modules
		del self._progressViewers

def init(moduleManager):
	return ProgressViewerModule(moduleManager)
