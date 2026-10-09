#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011, Milan Boers
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

import os
import weakref
import contextlib

class DummyLesson(object):
	pass

def installQtClasses():
	global EnterItemListModel, EnterItemList, EnterWidget

	class EnterItemListModel(QtCore.QAbstractListModel):
		"""The model for the list widget with media items (this construction
		   because without model Qt produces a bug)

		"""
		def __init__(self,list,*args,**kwargs):
			super(EnterItemListModel, self).__init__(*args, **kwargs)
			self.update(list)

		def update(self,list):
			self.beginResetModel()
			self.listData = [item["name"] for item in list["items"]]
			self.endResetModel()

		def rowCount(self,parent):
			return len(self.listData)

		def data(self,index,role):
			if index.isValid() and role == QtCore.Qt.DisplayRole:
				return self.listData[index.row()]

	class EnterItemList(QtGui.QListView):
		"""The list widget with media items"""

		def __init__(self,enterWidget,*args,**kwargs):
			super(EnterItemList, self).__init__(*args, **kwargs)

			self.enterWidget = enterWidget

			self.lm = EnterItemListModel(enterWidget.list,self)
			self.setModel(self.lm)
			self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

		def update(self):
			self.lm.update(self.enterWidget.list)

		def selectionChanged(self,current,previous):
			self.setRightActiveItem()

		def setRightActiveItem(self):
			if len(self.enterWidget.list["items"]) > 0:
				self.enterWidget.setActiveItem(self.enterWidget.list["items"][self.currentIndex().row()])

	class EnterWidget(QtGui.QSplitter):
		"""The enter tab"""

		def __init__(self,*args, **kwargs):
			super(EnterWidget, self).__init__(*args, **kwargs)
			self.list = {
				"items": list(),
				"tests": list()
			}
			self.lesson = DummyLesson()
			self.activeitem = {
				"id": int(),
				"remote": False,
				"filename": unicode(),
				"name": unicode(),
				"question": unicode(),
				"answer": unicode()
			}

			self.titlel = QtGui.QLabel()
			self.titleTextBox = QtGui.QLineEdit()
			self.titleTextBox.textChanged.connect(self.changeTitle)
			leftTop = QtGui.QHBoxLayout()
			leftTop.addWidget(self.titlel)
			leftTop.addWidget(self.titleTextBox)

			self.enterItemList = EnterItemList(self)

			self.removeButton = QtGui.QPushButton()
			self.removeButton.clicked.connect(self.removeItem)
			self.addLocalButton = QtGui.QPushButton()
			self.addLocalButton.clicked.connect(self.addLocalItems)
			self.addRemoteButton = QtGui.QPushButton()
			self.addRemoteButton.clicked.connect(self.addRemoteItems)

			leftBottom = QtGui.QHBoxLayout()
			leftBottom.addWidget(self.removeButton)
			leftBottom.addWidget(self.addLocalButton)
			leftBottom.addWidget(self.addRemoteButton)

			left = QtGui.QVBoxLayout()
			left. addLayout(leftTop)
			left.addWidget(self.enterItemList)
			left.addLayout(leftBottom)
			leftW = QtGui.QWidget()
			leftW.setLayout(left)

			self.mediaDisplay = base._modules.default("active", type="mediaDisplay").createDisplay(autoplay=False)

			self.namel = QtGui.QLabel()

			self.enterName = QtGui.QLineEdit()
			self.enterName.textEdited.connect(self.changeName)
			self.enterName.setEnabled(False)

			self.questionl = QtGui.QLabel()

			self.enterQuestion = QtGui.QLineEdit()
			self.enterQuestion.textEdited.connect(self.changeQuestion)
			self.enterQuestion.setEnabled(False)

			self.answerl = QtGui.QLabel()

			self.enterAnswer = QtGui.QLineEdit()
			self.enterAnswer.textEdited.connect(self.changeAnswer)
			self.enterAnswer.setEnabled(False)

			desceditL = QtGui.QVBoxLayout()
			desceditL.addWidget(self.namel)
			desceditL.addWidget(self.enterName)
			desceditL.addWidget(self.questionl)
			desceditL.addWidget(self.enterQuestion)
			desceditL.addWidget(self.answerl)
			desceditL.addWidget(self.enterAnswer)

			desceditW = QtGui.QWidget()
			desceditW.setLayout(desceditL)

			rightSplitter = QtGui.QSplitter(2)
			rightSplitter.addWidget(self.mediaDisplay)
			rightSplitter.addWidget(desceditW)

			right = QtGui.QVBoxLayout()
			right.addWidget(rightSplitter)
			rightW = QtGui.QWidget()
			rightW.setLayout(right)

			splitter = QtGui.QSplitter(self)
			splitter.addWidget(leftW)
			splitter.addWidget(rightW)

			layout = QtGui.QHBoxLayout()
			layout.addWidget(splitter)

			self.setLayout(layout)
			self.retranslate()

		def retranslate(self):
			self.titlel.setText(_("Title:"))

			self.removeButton.setText(_("Remove"))
			self.addLocalButton.setText(_("Add local media"))
			self.addRemoteButton.setText(_("Add remote media"))

			self.namel.setText(_("Name:"))
			self.questionl.setText(_("Question:"))
			self.answerl.setText(_("Answer:"))

		def addLocalItems(self):
			"""Add items from the local disk to the list"""

			extensions = []
			for module in base._modules.sort("active", type="mediaType"):
				with contextlib.ignored(AttributeError):
					#AttributeError: no extensions
					extensions.extend(module.extensions)

			extensionsStr = "("
			for extension in extensions:
				extensionsStr += "*" + extension + " "
			extensionsStr += ")"

			filenames = QtGui.QFileDialog.getOpenFileNames(
				self,
				_(_("Select file(s)")),
				QtCore.QDir.homePath(),
				_("Media") + " " + extensionsStr
			)
			for filename in filenames:
				self.addItem(unicode(filename), remote=False)

		def addRemoteItems(self):
			"""Add items from the internet to the list"""

			sitenames = []
			for module in base._modules.sort("active", type="mediaType"):
				with contextlib.ignored(AttributeError):
					#AttributeError: No name
					sitenames.extend(module.remoteNames)

			sitenamesStr = ""
			for sitename in sitenames:
				sitenamesStr += sitename + ", "
			sitenamesStr = sitenamesStr[:-2]

			url, dialog = QtGui.QInputDialog.getText(
				self,
				_("File URL"),
				_("Enter the URL of your website or media item.\nSupported video sites: ") + sitenamesStr + "."
			)
			if dialog:
				self.addItem(str(url), remote=True)

		def updateWidgets(self):
			"""Updates all the widgets if the list has changed"""

			self.enterItemList.update()
			self.titleTextBox.setText(self.list.get("title", u""))
			self.setActiveItem(self.activeitem)

		def addItem(self,filename,remote=False,name=None,question=None,answer=None):
			"""Add an item to the list"""

			# Check if file is supported
			for module in base._modules.sort("active", type="mediaType"):
				if module.supports(filename):
					item = {
						"id": int(),
						"remote": remote,
						"filename": unicode(filename),
						"name": unicode(name),
						"question": unicode(),
						"answer": unicode()
					}
					# Set id
					try:
						item["id"] = self.list["items"][-1]["id"] +1
					except IndexError:
						item["id"] = 0

					if name:
						item["name"] = name
					else:
						if remote == False:
							item["name"] = os.path.basename(filename)
						else:
							item["name"] = filename
					if question:
						item["question"] = question
					if answer:
						item["answer"] = answer

					self.list["items"].append(item)
					self.lesson.changed = True
					self.updateWidgets()
					break
			else:
				QtGui.QMessageBox.critical(
					self,
					_("Unsupported file type"),
					_("This type of file is not supported:\n") + filename
				)

		def removeItem(self):
			"""Remove an item from the list"""

			if self.activeitem in self.list["items"]:
				self.list["items"].remove(self.activeitem)
				self.updateWidgets()
				self.mediaDisplay.clear()
				self.enterName.setText("")
				self.enterName.setEnabled(False)
				self.enterQuestion.setText("")
				self.enterQuestion.setEnabled(False)
				self.enterAnswer.setText("")
				self.enterAnswer.setEnabled(False)
				self.enterItemList.setRightActiveItem()

		def setActiveItem(self,item):
			"""Change the active item"""

			self.enterName.setEnabled(True)
			self.enterName.setText(item["name"])
			self.enterQuestion.setEnabled(True)
			self.enterQuestion.setText(item["question"])
			self.enterAnswer.setEnabled(True)
			self.enterAnswer.setText(item["answer"])
			if item["filename"] != self.activeitem["filename"]:
				self.mediaDisplay.showMedia(item["filename"], item["remote"], False)
			self.activeitem = item

		def changeTitle(self, text):
			"""Change the title of the media list"""

			text = unicode(text)
			if self.list.get("title", u"") != text:
				self.list["title"] = text
				self.lesson.changed = True

		def changeName(self):
			"""Change the name of the active item"""

			if self.activeitem["name"] != unicode(self.enterName.text()):
				self.activeitem["name"] = unicode(self.enterName.text())
				self.updateWidgets()
				self.lesson.changed = True

		def changeQuestion(self):
			"""Change the question of the active item"""

			if self.activeitem["question"] != unicode(self.enterQuestion.text()):
				self.activeitem["question"] = unicode(self.enterQuestion.text())
				self.lesson.changed = True

		def changeAnswer(self):
			"""Change the description of the active item"""

			if self.activeitem["answer"] != unicode(self.enterAnswer.text()):
				self.activeitem["answer"] = unicode(self.enterAnswer.text())
				self.lesson.changed = True

class MediaEntererModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(MediaEntererModule, self).__init__(*args, **kwargs)

		global base
		base = self

		self._mm = moduleManager

		self.type = "mediaEnterer"
		self.priorities = {
			"default": 510,
		}

		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.requires = (
			self._mm.mods(type="mediaDisplay"),
			self._mm.mods(type="ui"),
		)
		self.filesWithTranslations = ("media.py",)

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		installQtClasses()

		self._modules = set(self._mm.mods(type="modules")).pop()

		self._widgets = set()

		#setup translation
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

	def _retranslate(self):
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

		for ref in self._widgets:
			widget = ref()
			if widget is not None:
				widget.retranslate()

	def disable(self):
		self.active = False

		del self._modules
		del self._widgets

	def createMediaEnterer(self):
		ew = EnterWidget()
		self._widgets.add(weakref.ref(ew))
		return ew

def init(moduleManager):
	return MediaEntererModule(moduleManager)
