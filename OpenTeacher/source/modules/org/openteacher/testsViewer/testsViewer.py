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

import weakref
import contextlib

def installQtClasses():
	global DetailsWidget, NotesWidget, TestViewerWidget, TestsModel, TestsViewer, TestsViewerWidget

	class TestsModel(QtCore.QAbstractTableModel):
		DATE, NOTE, COMPLETED = xrange(3)

		def __init__(self, calculateNote, *args, **kwargs):
			super(TestsModel, self).__init__(*args, **kwargs)

			self._calculateNote = calculateNote
			self._list = {
				"tests": [],
				"items": [],
			}
			self._headers = ["", "", ""]

		def headerData(self, section, orientation, role):
			if role != QtCore.Qt.DisplayRole:
				return
			if orientation == QtCore.Qt.Horizontal:
				return self._headers[section]
			else:
				return section + 1

		def retranslate(self):
			self._headers = [
				_("Date"),
				_("Note"),
				_("Completed"),
			]

		def data(self, index, role):
			if not index.isValid():
				return
			test = self._list["tests"][index.row()]
			if role == QtCore.Qt.DisplayRole:
				if index.column() == self.DATE:
					try:
						return test["results"][0]["active"]["start"].date().isoformat()
					except (IndexError, KeyError):
						return u""
				elif index.column() == self.NOTE:
					return self._calculateNote(test)
			elif role == QtCore.Qt.CheckStateRole and index.column() == self.COMPLETED:
				#guess it's there.
				try:
					return test["finished"]
				except KeyError:
					return

		def testFor(self, index):
			if index.isValid():
				return self._list["tests"][index.row()]

		def rowCount(self, parent):
			try:
				return len(self._list["tests"])
			except KeyError:
				return 0

		def columnCount(self, parent):
			return 3

		def _getList(self):
			return self._list

		def _setList(self, list):
			self.beginResetModel()
			self._list = list
			self.reset()

		list = property(_getList, _setList)

	class NotesWidget(QtGui.QWidget):
		def __init__(self, noteCalculator, calculatePercents, *args, **kwargs):
			super(NotesWidget, self).__init__(*args, **kwargs)

			self._noteCalculator = noteCalculator
			self._calculatePercents = calculatePercents

			self.highestLabel = QtGui.QLabel()
			self.averageLabel = QtGui.QLabel()
			self.lowestLabel = QtGui.QLabel()

			self.layout = QtGui.QFormLayout()
			self.layout.addRow(QtGui.QLabel(), self.highestLabel)
			self.layout.addRow(QtGui.QLabel(), self.averageLabel)
			self.layout.addRow(QtGui.QLabel(), self.lowestLabel)

			self.setLayout(self.layout)

		def retranslate(self):
			self.layout.labelForField(self.highestLabel).setText(
				_("Highest note:")
			)
			self.layout.labelForField(self.averageLabel).setText(
				_("Average note:")
			)
			self.layout.labelForField(self.lowestLabel).setText(
				_("Lowest note:")
			)

		def updateList(self, list):
			try:
				percents = map(self._calculatePercents, list["tests"])
			except KeyError:
				percents = []
			try:
				maxTest = list["tests"][percents.index(max(percents))]
				self.highestLabel.setText(self._noteCalculator.calculateNote(maxTest))
			except (KeyError, ValueError):
				#TRANSLATORS: This is meant as 'here would normally
				#stand a note, but not today.' If '-' isn't
				#appropriate in you language for that, please replace.
				#Otherwise, just copy the original.
				self.highestLabel.setText(_("-"))
			try:
				minTest = list["tests"][percents.index(min(percents))]
				self.lowestLabel.setText(self._noteCalculator.calculateNote(minTest))
			except (KeyError, ValueError):
				self.lowestLabel.setText(_("-"))
			try:
				average = self._noteCalculator.calculateAverageNote(list["tests"])
			except (ZeroDivisionError, KeyError):
				average = _("-")
			self.averageLabel.setText(unicode(average))

	class DetailsWidget(QtGui.QWidget):
		def __init__(self, testTypes, *args, **kwargs):
			super(DetailsWidget, self).__init__(*args, **kwargs)

			self._testTypes = testTypes

			self.labels = []
			self.layout = QtGui.QFormLayout()

			self.setLayout(self.layout)

		def updateList(self, list, dataType):
			for module in self._testTypes:
				if module.dataType == dataType and hasattr(module, "properties"):
					# Only if there are any properties in this module
					# If the labels were not made yet, make them
					if len(self.labels) == 0:
						for property in module.properties:
							label = QtGui.QLabel(property[0])
							label.setWordWrap(True)
							self.layout.addRow(property[0], label)
							label.setText(list.get(property[1], _("-")))
							self.labels.append(label)
					# Else, update them
					else:
						i = 0
						for property in module.properties:
							self.labels[i].setText(list.get(property[1], _("-")))
							i += 1
					break

	class TestsViewerWidget(QtGui.QSplitter):
		testActivated = QtCore.pyqtSignal([object, object, object])

		def __init__(self, testTypes, noteCalculator, calculatePercents, createPercentNoteViewer=None, *args, **kwargs):
			super(TestsViewerWidget, self).__init__(QtCore.Qt.Vertical, *args, **kwargs)

			self._createPercentNotesViewer = createPercentNoteViewer

			self.testsModel = TestsModel(noteCalculator.calculateNote)
			testsView = QtGui.QTableView()
			testsView.setModel(self.testsModel)
			testsView.doubleClicked.connect(self.showTest)
			self.notesWidget = NotesWidget(noteCalculator, calculatePercents)
			self.detailsWidget = DetailsWidget(testTypes)

			horSplitter = QtGui.QSplitter()
			horSplitter.addWidget(testsView)
			horSplitter.addWidget(self.notesWidget)

			self.addWidget(self.detailsWidget)
			self.addWidget(horSplitter)

		def showTest(self, index):
			list = self.testsModel.list
			dataType = self.testsModel.dataType
			test = self.testsModel.testFor(index)
			
			self.testActivated.emit(list, dataType, test)

		def updateList(self, list, dataType):
			self.testsModel.list = list
			self.testsModel.dataType = dataType
			self.notesWidget.updateList(list)
			self.detailsWidget.updateList(list, dataType)
			with contextlib.ignored(AttributeError):
				self.percentNotesViewer.hide()
			try:
				self.percentNotesViewer = self._createPercentNotesViewer(list["tests"])
			except (TypeError, KeyError):
				pass
			else:
				self.addWidget(self.percentNotesViewer)

		def retranslate(self):
			self.notesWidget.retranslate()
			self.testsModel.retranslate()

	class TestViewerWidget(QtGui.QWidget):
		backActivated = QtCore.pyqtSignal()

		def __init__(self, createTestViewer, list, dataType, test, *args, **kwargs):
			super(TestViewerWidget, self).__init__(*args, **kwargs)

			self.backButton = QtGui.QPushButton("")
			self.backButton.clicked.connect(self.backActivated.emit)

			testViewer = createTestViewer(list, dataType, test)

			layout = QtGui.QVBoxLayout()
			layout.addWidget(testViewer)
			layout.addWidget(self.backButton)
			self.setLayout(layout)

		def retranslate(self):
			self.backButton.setText(_("Back"))

	class TestsViewer(QtGui.QStackedWidget):
		def __init__(self, testTypes, noteCalculator, calculatePercents, createTestViewer, createPercentNotesViewer=None,  *args, **kwargs):
			super(TestsViewer, self).__init__(*args, **kwargs)

			self._createTestViewer = createTestViewer

			self.testsViewerWidget = TestsViewerWidget(testTypes, noteCalculator, calculatePercents, createPercentNotesViewer)
			self.testsViewerWidget.testActivated.connect(self.showList)
			self.addWidget(self.testsViewerWidget)

		def showList(self, list, dataType, test):
			testViewer = TestViewerWidget(self._createTestViewer, list, dataType, test)
			testViewer.backActivated.connect(self.showTests)
			self.addWidget(testViewer)
			self.setCurrentWidget(testViewer)
			self.retranslate()

		def showTests(self):
			self.setCurrentWidget(self.testsViewerWidget)

		def updateList(self, list, dataType):
			self.testsViewerWidget.updateList(list, dataType)

		def retranslate(self):
			for i in range(self.count()):
				self.widget(i).retranslate()

class TestsViewerModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestsViewerModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "testsViewer"
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="noteCalculatorChooser"),
			self._mm.mods(type="testViewer"),
		)
		self.uses = (
			self._mm.mods(type="percentNoteViewer"),
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("testsViewer.py",)

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		installQtClasses()

		self._modules = set(self._mm.mods(type="modules")).pop()

		self._testsViewers = set()
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()
		self.active = True

	def disable(self):
		self.active = False
		
		del self._modules
		del self._testsViewers

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
		for tv in self._testsViewers:
			r = tv() #check weak reference
			if r is not None:
				r.retranslate()

	def createTestsViewer(self):
		testTypes = self._mm.mods("active", type="testType")
		noteCalculator = self._modules.default(
			"active",
			type="noteCalculatorChooser"
		).noteCalculator
		calculatePercents = self._modules.default(
			"active",
			type="percentsCalculator"
		).calculatePercents
		createTestViewer = self._modules.default(
			"active",
			type="testViewer"
		).createTestViewer
		try:
			createPercentNotesViewer = self._modules.default(
				"active",
				type="percentNotesViewer"
			).createPercentNotesViewer
		except IndexError:
			createPercentNotesViewer = None

		tv = TestsViewer(testTypes, noteCalculator, calculatePercents, createTestViewer, createPercentNotesViewer)
		#Weak reference so gc can still get into action
		self._testsViewers.add(weakref.ref(tv))
		self._retranslate()
		return tv

def init(moduleManager):
	return TestsViewerModule(moduleManager)
