#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2012, Marten de Vries
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

import urllib2
import urllib
import json
import re
import logging
import contextlib

logger = logging.getLogger(__name__)

class StudyStackApi(object):
	def __init__(self, parse, *args, **kwargs):
		super(StudyStackApi, self).__init__(*args, **kwargs)

		self._parse = parse

	def _get(self, action, **kwargs):
		kwargs.update({
			"strict": "Y",
			"appId": "osrc5103",
		})
		url = "http://www.studystack.com/servlet/%s?%s" % (
			action,
			urllib.urlencode(kwargs)
		)
		data = urllib2.urlopen(url).read()
		#the JSON is escaped in an invalid way. This should fix it
		#(every slash other than in '\"' and '\\' is removed, conform
		#the JSON spec).
		data = re.sub(
			r'("[^"]*)\\([^"\\])',
			r'\1\2',
			data
		)
		return json.loads(data)

	def getCategories(self):
		categories = self._get("categoryListJson")
		return ((c["name"], c["id"]) for c in categories)

	def getLists(self, categoryId):
		stacks = self._get("categoryStackListJson", page=1, sortOrder="stars", categoryId=categoryId)
		stacks += self._get("categoryStackListJson", page=2, sortOrder="stars", categoryId=categoryId)
		return ((s["stackName"], s["id"]) for s in stacks)

	def getList(self, listId):
		stack = self._get("json", studyStackId=listId)
		items = []
		for i, row in enumerate(stack["data"]):
			items.append({
				"id": i,
				"questions": self._parse(row[0]),
				"answers": self._parse(row[1]),
			})
		return {
			"list": {
				"title": stack["name"],
				"items": items,
			},
			"resources": {},
		}

def installQtClasses():
	global AbstractSelectDialog, BookSelectDialog, CategorySelectDialog, ListSelectDialog, Model

	class Model(QtCore.QAbstractListModel):
		def __init__(self, choices, *args, **kwargs):
			"""Choices should be an iterable object of tuples of size two,
			   with in it first the text to display and second the value to
			   return.

			"""
			super(Model, self).__init__(*args, **kwargs)

			self._choices = list(choices)

		def rowCount(self, parent):
			return len(self._choices)

		def data(self, index, role):
			if not (index.isValid() and role == QtCore.Qt.DisplayRole):
				return

			return self._choices[index.row()][0]

		def getChoice(self, index):
			return self._choices[index.row()][1]

	class AbstractSelectDialog(QtGui.QDialog):
		def __init__(self, choices, *args, **kwargs):
			super(AbstractSelectDialog, self).__init__(*args, **kwargs)

			self.label = QtGui.QLabel()

			self._listView = QtGui.QListView()
			self._model = Model(choices)
			self._listView.setModel(self._model)
			if not self.singleOnly:
				self._listView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
			self._listView.doubleClicked.connect(self.accept)

			buttonBox = QtGui.QDialogButtonBox(
				QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok,
				parent=self
			)
			buttonBox.accepted.connect(self.accept)
			buttonBox.rejected.connect(self.reject)

			l = QtGui.QVBoxLayout()
			l.addWidget(self.label)
			l.addWidget(self._listView)
			l.addWidget(buttonBox)
			self.setLayout(l)

		@property
		def chosenItems(self):
			return [self._model.getChoice(i) for i in self._listView.selectedIndexes()]

	class CategorySelectDialog(AbstractSelectDialog):
		singleOnly = True
		def retranslate(self):
			self.setWindowTitle(_("Select category"))
			self.label.setText(_("Please select a category"))

	class ListSelectDialog(AbstractSelectDialog):
		singleOnly = False
		def retranslate(self):
			self.setWindowTitle(_("Select list"))
			self.label.setText(_("Please select a list"))

class StudyStackApiModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(StudyStackApiModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "studyStackApi"
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="buttonRegister"),
			self._mm.mods(type="wordsStringParser"),
			self._mm.mods(type="loaderGui"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("studyStackApi.py",)

		x = 600
		self.priorities = {
			"all": x,
			"selfstudy": x,
			"student@home": x,
			"student@school": x,
			"teacher": x,
			"words-only": x,
			"code-documentation": x,
			"test-suite": x,
			"default": -1,
		}

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		installQtClasses()

		self._modules = set(self._mm.mods(type="modules")).pop()
		self._uiModule = self._modules.default("active", type="ui")
		self._buttonRegister = self._modules.default("active", type="buttonRegister")

		self._activeDialogs = set()

		self._button = self._buttonRegister.registerButton("load-from-internet")
		self._button.clicked.handle(self._selectCategory)
		self._button.changePriority.send(self.priorities["all"])

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self._api = StudyStackApi(self._parse)

		self.active = True

	def _retranslate(self):
		global _
		global ngettext

		#Install translator
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)

		self._button.changeText.send(_("Import from studystack.com"))

		#Translate all active dialogs
		for dialog in self._activeDialogs:
			dialog.retranslate()
			dialog.tab.title = dialog.windowTitle()

	@property
	def _parse(self):
		return self._modules.default("active", type="wordsStringParser").parse

	def _showDialog(self, dialog):
		tab = self._uiModule.addCustomTab(dialog)
		tab.closeRequested.handle(tab.close)
		dialog.rejected.connect(tab.close)
		dialog.accepted.connect(tab.close)
		dialog.tab = tab
		self._activeDialogs.add(dialog)

		self._retranslate()
		dialog.finished.connect(lambda: self._activeDialogs.remove(dialog))

		return dialog

	def _selectCategory(self):
		with self._handlingWebErrors():
			d = self._showDialog(CategorySelectDialog(self._api.getCategories()))
			d.accepted.connect(lambda: self._selectList(d))

	def _selectList(self, dialog):
		categoryId = dialog.chosenItems[0]
		with self._handlingWebErrors():
			d = self._showDialog(ListSelectDialog(self._api.getLists(categoryId)))
			d.accepted.connect(lambda: self._loadSelectedLists(d))

	def _loadSelectedLists(self, dialog):
		with self._handlingWebErrors():
			for listId in dialog.chosenItems:
				list = self._api.getList(listId)
				try:
					self._loadList(list)
				except NotImplementedError:
					return

			#everything went well
			self._uiModule.statusViewer.show(_("The word list was imported from Study Stack successfully."))

	@contextlib.contextmanager
	def _handlingWebErrors(self):
		try:
			yield
		except urllib2.URLError, e:
			#for debugging purposes
			logger.debug(e, exc_info=True)
			QtGui.QMessageBox.warning(
				self._uiModule.qtParent,
				_("No Study Stack connection"),
				_("Study Stack didn't accept the connection. Are you sure that your internet connection works and http://www.studystack.com/ is online?")
			)

	def _loadList(self, list):
		self._modules.default("active", type="loaderGui").loadFromLesson("words", list)

	def disable(self):
		self.active = False

		self._buttonRegister.unregisterButton(self._button)

		del self._modules
		del self._uiModule
		del self._buttonRegister

		del self._activeDialogs
		del self._button
		del self._api

def init(moduleManager):
	return StudyStackApiModule(moduleManager)
