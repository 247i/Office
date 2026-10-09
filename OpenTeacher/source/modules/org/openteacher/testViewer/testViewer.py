#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2009-2013, Marten de Vries
#	Copyright 2008-2011, Milan Boers
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
import contextlib

def installQtClasses():
	global TestModel, TestViewer

	class TestModel(QtCore.QAbstractTableModel):
		def __init__(self, list, test, testTable, *args, **kwargs):
			super(TestModel, self).__init__(*args, **kwargs)

			self._list = list
			self._test = test

			self._testTable = testTable

		def headerData(self, section, orientation, role):
			if role != QtCore.Qt.DisplayRole:
				return
			if orientation == QtCore.Qt.Horizontal:
				return self._testTable.header[section]
			else:
				return section + 1

		def data(self, index, role):
			if not index.isValid():
				return
			
			if isinstance(self._testTable.data(index.row(), index.column()), bool):
				# Boolean
				if role == QtCore.Qt.CheckStateRole:
					return self._testTable.data(index.row(), index.column())
			else:
				# Non-Boolean
				if role == QtCore.Qt.DisplayRole:
					return self._testTable.data(index.row(), index.column())

		def rowCount(self, parent):
			return len(self._test["results"])

		def columnCount(self, parent):
			return len(self._testTable.header)

	class TestViewer(QtGui.QSplitter):
		def __init__(self, list, test, testTable, calculateNote, progressWidget, *args, **kwargs):
			super(TestViewer, self).__init__(QtCore.Qt.Vertical, *args, **kwargs)

			self._test = test
			self._testTable = testTable

			self._calculateNote = calculateNote

			#Vertical splitter
			tableView = QtGui.QTableView()
			testModel = TestModel(list, test, testTable)
			tableView.setModel(testModel)

			self.totalThinkingTimeLabel = QtGui.QLabel()
			vertSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
			vertSplitter.addWidget(self.totalThinkingTimeLabel)
			vertSplitter.addWidget(tableView)

			#Horizontal splitter
			factsLayout = QtGui.QVBoxLayout()
			self.completedLabel = QtGui.QLabel()
			self.noteLabel = QtGui.QLabel()
			factsLayout.addWidget(self.noteLabel, 0, QtCore.Qt.AlignTop)
			with contextlib.ignored(AttributeError):
				for fact in self._testTable.funFacts:
					if fact[1] is None:
						label = QtGui.QLabel("%s<br />-" % fact[0])
					else:
						label = QtGui.QLabel("%s<br /><span style=\"font-size: 14px\">%s</span>" % (fact[0], fact[1]))
					factsLayout.addWidget(label, 0, QtCore.Qt.AlignTop)

			factsLayout.addWidget(self.completedLabel)
			factsLayout.addStretch()
			
			factsWidget = QtGui.QWidget()
			factsWidget.setLayout(factsLayout)
			
			horSplitter = QtGui.QSplitter()
			horSplitter.addWidget(vertSplitter)
			horSplitter.addWidget(factsWidget)

			#Main splitter
			self.addWidget(horSplitter)
			if progressWidget:
				self.addWidget(progressWidget)

		def retranslate(self):
			self.setWindowTitle(_("Results"))

			if self._calculateNote:
				html = "<br /><span style=\"font-size: 40px\">%s</span>"
				self.noteLabel.setText(_("Note:") + html % self._calculateNote(self._test))
			else:
				self.noteLabel.setText("")

			try:
				completedText = _("yes") if self._test["finished"] else _("no")
			except KeyError:
				self.completedLabel.setText("")
			else:
				self.completedLabel.setText(_("Completed: %s") % completedText)

			seconds = int(round(self._totalThinkingTime))
			if seconds < 180:
				#< 3 minutes
				self.totalThinkingTimeLabel.setText(ngettext(
					"Total thinking time: %s second",
					"Total thinking time: %s seconds",
					seconds
				) % seconds)
			else:
				#> 3 minutes
				minutes = int(round(seconds / 60.0))
				self.totalThinkingTimeLabel.setText(
					_("Total thinking time: %s minutes") % minutes
				)

		@property
		def _totalThinkingTime(self):
			totalThinkingTime = datetime.timedelta()
			for result in self._test["results"]:
				if "active" in result:
					totalThinkingTime += result["active"]["end"] - result["active"]["start"]
			return dateutil.total_seconds(totalThinkingTime)

class TestViewerModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestViewerModule, self).__init__(*args, **kwargs)

		self._mm = moduleManager
		self.type = "testViewer"
		self.requires = (
			self._mm.mods(type="ui"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
			self._mm.mods(type="noteCalculatorChooser"),
			self._mm.mods(type="testType"),
			self._mm.mods(type="progressViewer"),
		)
		self.filesWithTranslations = ("testViewer.py",)

	def createTestViewer(self, list, dataType, test):
		"""This creates a widget that gives an overview of the passed in
		   `test`. Test should be inside `list["tests"]` and `list`
		   should be passed in. `dataType` should be the data type of
		   `list`.

		"""
		testTable = self._modules.default("active", type="testType", dataType=dataType)
		testTable.updateList(list, test)

		try:
			calculateNote = self._modules.default(
				"active",
				type="noteCalculatorChooser"
			).noteCalculator.calculateNote
		except IndexError:
			calculateNote = None

		try:
			progressWidget = self._modules.default(
				"active",
				type="progressViewer"
			).createProgressViewer(test)
		except (IndexError, KeyError):
			#IndexError: self._modules.default if the mod isn't there.
			#KeyError: a progress widget needs time info which might
			#not be there.
			progressWidget = None

		tv = TestViewer(list, test, testTable, calculateNote, progressWidget)
		self._testViewers.add(weakref.ref(tv))
		self._retranslate()

		return tv

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		installQtClasses()

		self._modules = set(self._mm.mods(type="modules")).pop()

		self._testViewers = set()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()
		self.active = True

	def _retranslate(self):
		global _, ngettext
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda x, y, n: x if n == 1 else y
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)
		for tv in self._testViewers:
			r = tv()
			if r is not None:
				r.retranslate()

	def disable(self):
		self.active = False

		del self._testViewers
		del self._modules

def init(moduleManager):
	return TestViewerModule(moduleManager)
