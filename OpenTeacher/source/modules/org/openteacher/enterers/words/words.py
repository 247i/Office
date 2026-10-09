#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2013, Marten de Vries
#	Copyright 2011, Cas Widdershoven
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

import datetime
import weakref
import contextlib

class EmptyLesson(object):
	def __init__(self, *args, **kwargs):
		super(EmptyLesson, self).__init__(*args, **kwargs)

		self.list = {}

def installQtClasses():
	global SpellingHighlighter, WordsTableView, WordsTableModel, EnterWidget

	class SpellingHighlighter(QtGui.QSyntaxHighlighter):
		_format = QtGui.QTextCharFormat()
		_format.setUnderlineColor(QtCore.Qt.red)
		_format.setUnderlineStyle(QtGui.QTextCharFormat.SpellCheckUnderline)

		def __init__(self, checkWord, splitWords, *args, **kwargs):
			super(SpellingHighlighter, self).__init__(*args, **kwargs)

			self._checkWord = checkWord
			self._splitWords = splitWords

		def highlightBlock(self, text):
			text = unicode(text)
			if text.endswith(u"…"):
				#might not be the best tokenization, but better than
				#what enchant can do in this situation...
				if u" " in text:
					text = text.rsplit(u" ", 1)[0]
				else:
					text = u""

			for word, pos in self._splitWords(text):
				if not self._checkWord(word):
					self.setFormat(pos, len(word), self._format)

	class WordsTableItemDelegate(QtGui.QStyledItemDelegate):
		"""A default delegate, with the difference that it installs an event
		   filter for some non-default keys. The equals key and return key
		   are, from the perspective of Qt, equal to the tab key. It
		   also allows callers to access the current editor via the
		   currentEditor property, and paints html when displaying.

		   Next to that, it offers spell checking. Set the
		   'checkQuestion' and 'checkAnswer' properties to a function
		   that checks one word before using this class because of that.

		"""
		def eventFilter(self, object, event):
			if (event.type() == QtCore.QEvent.KeyPress and event.key() in (QtCore.Qt.Key_Equal, QtCore.Qt.Key_Return)):
				event = QtGui.QKeyEvent(
					event.type(),
					QtCore.Qt.Key_Tab,
					event.modifiers(),
					event.text(),
					event.isAutoRepeat(),
					event.count()
				)
			return super(WordsTableItemDelegate, self).eventFilter(object, event)

		def paint(self, painter, option, index):
			self.initStyleOption(option, index)

			#set up document with syntax highlighting
			document = QtGui.QTextDocument()

			check = lambda item: True
			split = lambda words: []
			with contextlib.ignored(AttributeError):
				if index.column() == 0:
					check = self.checkQuestion
					split = self.splitQuestion
				elif index.column() == 1:
					check = self.checkAnswer
					split = self.splitAnswer
			SpellingHighlighter(check, split, document)

			#get elided text
			text = option.widget.fontMetrics().elidedText(option.text, option.textElideMode, option.rect.width() - document.documentMargin())
			#set elided text
			document.setHtml(text)

			#calculate place to start rendering
			yPos = option.rect.center().y() - option.widget.fontMetrics().height() / 2 - document.documentMargin()
			startPoint = QtCore.QPoint(option.rect.x(), yPos)

			#move to place to start rendering, render, and move back.
			painter.translate(startPoint)
			document.drawContents(painter)
			painter.translate(-startPoint)

		def createEditor(self, parent, option, index):
			self.currentEditor = super(WordsTableItemDelegate, self).createEditor(
				parent, option, index
			)
			return self.currentEditor

	class WordsTableView(QtGui.QTableView):
		def __init__(self, createChecker, *args, **kwargs):
			super(WordsTableView, self).__init__(*args, **kwargs)

			self._createChecker = createChecker

			self.setItemDelegate(WordsTableItemDelegate())
			self.setAlternatingRowColors(True)
			self.setSortingEnabled(True)

		def _questionLanguageChanged(self):
			try:
				lang = self.model().lesson.list["questionLanguage"]
			except KeyError:
				pass
			else:
				checker = self._createChecker(lang)
				self.itemDelegate().checkQuestion = checker.check
				self.itemDelegate().splitQuestion = checker.split
				self._wholeModelChanged()

		def _answerLanguageChanged(self):
			try:
				lang = self.model().lesson.list["answerLanguage"]
			except KeyError:
				pass
			else:
				checker = self._createChecker(lang)
				self.itemDelegate().checkAnswer = checker.check
				self.itemDelegate().splitAnswer = checker.split
				self._wholeModelChanged()

		def _wholeModelChanged(self):
			self.model().dataChanged.emit(
				self.model().index(0, 0),
				self.model().index(self.model().rowCount() -1, self.model().columnCount() -1)
			)

		def setModel(self, *args, **kwargs):
			with contextlib.ignored(AttributeError):
				#AttributeError: first time.
				self.model().modelReset.disconnect(self._modelReset)
				self.model().questionLanguageChanged.disconnect(self._questionLanguageChanged)
				self.model().answerLanguageChanged.disconnect(self._answerLanguageChanged)

			result = super(WordsTableView, self).setModel(*args, **kwargs)

			self.model().modelReset.connect(self._modelReset)
			self.model().questionLanguageChanged.connect(self._questionLanguageChanged)
			self.model().answerLanguageChanged.connect(self._answerLanguageChanged)

			#setting the model is 'resetting' too.
			self._modelReset()

			return result

		def _modelReset(self):
			self._questionLanguageChanged()
			self._answerLanguageChanged()

			#If the model is empty, let the user start editing
			#(model has always one starting row.)
			if self.model().rowCount() == 1:
				i = self.model().createIndex(0, 0)
				self.setCurrentIndex(i)
				self.edit(i)

		def moveCursor(self, cursorAction, modifiers):
			"""Reimplentation of moveCursor that makes sure that tab only
			   moves between the questions and answers column (so not the 
			   comment column). This way, inserting words is way faster.

			"""
			if cursorAction not in (QtGui.QAbstractItemView.MoveNext, QtGui.QAbstractItemView.MovePrevious):
				return super(WordsTableView, self).moveCursor(cursorAction, modifiers)
			if self.model().columnCount() == 0 or self.model().rowCount() == 0:
				return QtCore.QModelIndex()

			row = self.currentIndex().row()
			column = self.currentIndex().column()
			if cursorAction == QtGui.QAbstractItemView.MoveNext:
				column += 1
				if column > 1:
					column = 0
					row += 1
				if row > self.model().rowCount() -1:
					row = 0
			elif cursorAction == QtGui.QAbstractItemView.MovePrevious:
				column -= 1
				if column < 0:
					column = 1
					row -= 1
				if row < 0:
					row = self.model().rowCount() -1
			
			return self.model().index(row, column)

	class WordsTableModel(QtCore.QAbstractTableModel):
		questionLanguageChanged = QtCore.pyqtSignal()
		answerLanguageChanged = QtCore.pyqtSignal()
		QUESTIONS, ANSWERS, COMMENT, COMMENT_AFTER_ANSWERING = xrange(4)

		def __init__(self, compose, parse, *args, **kwargs):
			super(WordsTableModel, self).__init__(*args, **kwargs)

			self.updateLesson(EmptyLesson())
			self._compose = compose
			self._parse = parse
			self._headers = ["", "", "", ""]

		def retranslate(self):
			self._headers = [_("Questions"), _("Answers"), _("Comment"), _("Comment after answering")]

		def updateLesson(self, lesson):
			self.beginResetModel()
			self.lesson = lesson
			try:
				self.indexes = range(len(self.lesson.list["items"]))
			except KeyError:
				self.indexes = []
			self.endResetModel()

		def sort(self, column, order):
			items = self.lesson.list.get("items", [])
			if column == self.QUESTIONS:
				sortedItems = sorted(items, key=lambda word: word.get("questions", []))
			elif column == self.ANSWERS:
				sortedItems = sorted(items, key=lambda word: word.get("answers", []))
			elif column == self.COMMENT:
				sortedItems = sorted(items, key=lambda word: word.get("comment", u""))
			elif column == self.COMMENT_AFTER_ANSWERING:
				sortedItems = sorted(items, key=lambda word: word.get("commentAfterAnswering", u""))

			if order == QtCore.Qt.DescendingOrder:
				items.reverse()

			self.layoutAboutToBeChanged.emit()
			self.indexes = [self.lesson.list["items"].index(item) for item in items]
			self.layoutChanged.emit()

		def updateTitle(self, title):
			self.lesson.list["title"] = unicode(title)
			self.lesson.changed = True

		def updateQuestionLanguage(self, questionLanguage):
			self.lesson.list["questionLanguage"] = unicode(questionLanguage)
			self.questionLanguageChanged.emit()
			self.lesson.changed = True

		def updateAnswerLanguage(self, answerLanguage):
			self.lesson.list["answerLanguage"] = unicode(answerLanguage)
			self.answerLanguageChanged.emit()
			self.lesson.changed = True

		def headerData(self, section, orientation, role):
			if role != QtCore.Qt.DisplayRole:
				return
			if orientation == QtCore.Qt.Horizontal:
				return self._headers[section]
			elif orientation == QtCore.Qt.Vertical:
				return section +1

		def rowCount(self, parent=None):
			try:
				return len(self.lesson.list["items"]) +1
			except KeyError:
				return 1

		def columnCount(self, parent=None):
			return 4

		def data(self, index, role=QtCore.Qt.DisplayRole):
			if not (index.isValid() and
				role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole)):
				return
			try:
				listIndex = self.indexes[index.row()]
			except IndexError:
				return u"" #last (empty) row
			else:
				word = self.lesson.list["items"][listIndex]

				if index.column() == self.QUESTIONS:
					return self._compose(word.get("questions", []))
				elif index.column() == self.ANSWERS:
					return self._compose(word.get("answers", []))
				elif index.column() == self.COMMENT:
					return word.get("comment", u"")
				elif index.column() == self.COMMENT_AFTER_ANSWERING:
					return word.get("commentAfterAnswering", u"")

		def flags(self, index):
			return (
				QtCore.Qt.ItemIsEnabled |
				QtCore.Qt.ItemIsSelectable |
				QtCore.Qt.ItemIsEditable
			)

		def setData(self, index, value, role=QtCore.Qt.EditRole):
			if not (index.isValid() and role == QtCore.Qt.EditRole):
				return False
			#makes calling without a QVariant possible (more dynamic).
			value = QtCore.QVariant(value)
			#add 'items' key to the list if not there already, since setData needs it.
			if "items" not in self.lesson.list:
				self.lesson.list["items"] = []
			while True:
				#repeat because this does two things:
				#- add a row if needed
				#- enter the data in that row (and then break the loop)
				try:
					listIndex = self.indexes[index.row()]
				except IndexError:
					#insert row
					if not unicode(value.toString()):
						return False

					word = {"created": datetime.datetime.now()}
					try:
						word["id"] = self.lesson.list["items"][-1]["id"] +1
					except IndexError:
						word["id"] = 0
					self.beginInsertRows(
						QtCore.QModelIndex(),
						self.rowCount(),
						self.rowCount()
					)
					self.lesson.list["items"].append(word)
					self.indexes.append(self.lesson.list["items"].index(word))
					self.endInsertRows()
				else:
					#set data
					word = self.lesson.list["items"][listIndex]

					if index.column() == self.QUESTIONS:
						word["questions"] = self._parse(unicode(value.toString()))
					elif index.column() == self.ANSWERS:
						word["answers"] = self._parse(unicode(value.toString()))
					elif index.column() == self.COMMENT:
						word["comment"] = unicode(value.toString()).strip()
						if not len(word["comment"]):
							del word["comment"]
					elif index.column() == self.COMMENT_AFTER_ANSWERING:
						word["commentAfterAnswering"] = unicode(value.toString()).strip()
						if not len(word["commentAfterAnswering"]):
							del word["commentAfterAnswering"]
					break
			self.lesson.changed = True
			return True

		def removeRow(self, row, parent=QtCore.QModelIndex()):
			listIndex = self.indexes[row]
			self.beginRemoveRows(parent, row, row)
			del self.indexes[row]
			#update self.indexes
			for i in xrange(len(self.indexes)):
				if self.indexes[i] > listIndex:
					self.indexes[i] -= 1
			del self.lesson.list["items"][listIndex]
			self.endRemoveRows()

	class EnterWidget(QtGui.QSplitter):
		def __init__(self, createChecker, keyboardWidget, compose, parse, *args, **kwargs):
			super(EnterWidget, self).__init__(*args, **kwargs)

			#Initialize all widgets
			self._buildUi(createChecker, keyboardWidget)

			#Install the table model
			self._wordsTableModel = WordsTableModel(compose, parse)
			self._wordsTableView.setModel(self._wordsTableModel)

			self._connectSignals()

		@property
		def lesson(self):
			return self._wordsTableModel.lesson

		def updateLesson(self, lesson):
			self._wordsTableModel.updateLesson(lesson)
			self._titleTextBox.setText(lesson.list.get("title", u""))
			self._questionLanguageTextBox.setText(lesson.list.get("questionLanguage", u""))
			self._answerLanguageTextBox.setText(lesson.list.get("answerLanguage", u""))

		def removeSelectedRows(self):
			while True:
				try:
					i = self._wordsTableView.selectedIndexes()[0]
				except IndexError:
					break
				try:
					self._wordsTableModel.removeRow(i.row())
				except IndexError:
					#trying to remove the empty add row isn't going to work
					break

		def addLetter(self, letter):
			i = self._wordsTableView.currentIndex()
			if not i.isValid():
				return

			data = self._wordsTableModel.data(i) + letter
			self._wordsTableModel.setData(i, data)
			self._wordsTableView.edit(i)
			self._wordsTableView.itemDelegate().currentEditor.deselect()

		def _buildUi(self, createChecker, keyboardWidget):
			self._titleLabel = QtGui.QLabel()
			self._titleTextBox = QtGui.QLineEdit(self)
			self._questionLanguageTextBox = QtGui.QLineEdit(self)
			self._questionLanguageLabel = QtGui.QLabel()
			self._answerLanguageTextBox = QtGui.QLineEdit(self)
			self._answerLanguageLabel = QtGui.QLabel()
			self._wordsTableView = WordsTableView(createChecker)

			topLayout = QtGui.QGridLayout()
			topLayout.addWidget(self._titleLabel, 0, 0)
			topLayout.addWidget(self._titleTextBox, 0, 1)

			topLayout.addWidget(self._questionLanguageLabel, 1, 0)
			topLayout.addWidget(self._questionLanguageTextBox, 1, 1)

			topLayout.addWidget(self._answerLanguageLabel, 2, 0)
			topLayout.addWidget(self._answerLanguageTextBox, 2, 1)

			leftLayout = QtGui.QVBoxLayout()
			leftLayout.addLayout(topLayout)
			leftLayout.addWidget(self._wordsTableView)

			leftLayoutWidget = QtGui.QWidget()
			leftLayoutWidget.setLayout(leftLayout)

			if keyboardWidget is not None:
				self._keyboardWidget = keyboardWidget
			self._removeSelectedRowsButton = QtGui.QPushButton(self)
			shortcut = QtGui.QShortcut(QtGui.QKeySequence.Delete, self)
			shortcut.activated.connect(self._removeSelectedRowsButton.animateClick)

			rightLayout = QtGui.QVBoxLayout()
			with contextlib.ignored(AttributeError):
				rightLayout.addWidget(self._keyboardWidget)
			rightLayout.addWidget(self._removeSelectedRowsButton)

			rightLayoutWidget = QtGui.QWidget()
			rightLayoutWidget.setLayout(rightLayout)

			self.addWidget(leftLayoutWidget)
			self.addWidget(rightLayoutWidget)

			self.setStretchFactor(0, 255)
			self.setStretchFactor(1, 1)

		def retranslate(self):
			self._titleLabel.setText(_("Title:"))
			self._questionLanguageLabel.setText(_("Question language:"))
			self._answerLanguageLabel.setText(_("Answer language:"))
			self._removeSelectedRowsButton.setText(_("Remove selected row(s)"))
			
			self._wordsTableModel.retranslate()

		def _connectSignals(self):
			self._removeSelectedRowsButton.clicked.connect(
				self.removeSelectedRows
			)
			with contextlib.ignored(AttributeError):
				self._keyboardWidget.letterChosen.handle(self.addLetter)

			self._titleTextBox.textEdited.connect(
				self._wordsTableModel.updateTitle
			)
			self._questionLanguageTextBox.textEdited.connect(
				self._wordsTableModel.updateQuestionLanguage
			)
			self._answerLanguageTextBox.textEdited.connect(
				self._wordsTableModel.updateAnswerLanguage
			)

class WordsEntererModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(WordsEntererModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "wordsEnterer"
		self.priorities = {
			"default": 450,
		}
		self.uses = (
			self._mm.mods(type="translator"),
			self._mm.mods(type="spellChecker"),
			self._mm.mods(type="charsKeyboard"),
		)
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="wordsStringComposer"),
			self._mm.mods(type="wordsStringParser"),
		)
		self.filesWithTranslations = ("words.py",)

	@property
	def _charsKeyboard(self):
		try:
			return self._modules.default(
				"active",
				type="charsKeyboard"
			).createWidget()
		except IndexError:
			return

	@property
	def _compose(self):
		return self._modules.default(
			"active",
			type="wordsStringComposer"
		).compose

	@property
	def _parse(self):
		return self._modules.default(
			"active",
			type="wordsStringParser"
		).parse

	@property
	def _createChecker(self):
		try:
			return self._modules.default("active", type="spellChecker").createChecker
		except IndexError:
			class Fallback(object):
				def __init__(self, *args, **kwargs):
					pass
				def check(self, item):
					#'everything is a well spelled word'
					return True
				def split(self, words):
					#'no words in there'
					return []
			return Fallback

	def createWordsEnterer(self):
		ew = EnterWidget(
			self._createChecker,
			self._charsKeyboard,
			self._compose,
			self._parse
		)
		self._activeWidgets.add(weakref.ref(ew))
		self._retranslate()

		return ew

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		installQtClasses()

		self._modules = set(self._mm.mods(type="modules")).pop()
		self._activeWidgets = set()

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

		for widget in self._activeWidgets:
			r = widget()
			if r is not None:
				r.retranslate()

	def disable(self):
		self.active = False
		
		del self._modules
		del self._activeWidgets

def init(moduleManager):
	return WordsEntererModule(moduleManager)
