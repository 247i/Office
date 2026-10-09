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

import urllib2
import urllib
import contextlib
from etree import ElementTree
import logging

logger = logging.getLogger(__name__)

class VocatrainApi(object):
	"""Public properties:
	    - service. Should be either 'http://vocatrain.com/' or
	      'http://woordjesleren.nl/'. Don't change it while looking up
	      a list, since the id's that are passed to the lookup methods
	      aren't the same anymore after this chagnes.

	"""
	def __init__(self, parseList, *args, **kwargs):
		super(VocatrainApi, self).__init__(*args, **kwargs)

		self.service = "http://vocatrain.com/"
		self._parseList = parseList

	def _open(self, url, **kwargs):
		return urllib2.urlopen(url + "?" + urllib.urlencode(kwargs))

	def getCategories(self):
		fd = self._open(self.service + "api/select_categories.php")
		root = ElementTree.parse(fd).getroot()
		for category in root.findall(".//category"):
			yield (category.text, category.get("id"))

	def getBook(self, categoryId):
		fd = self._open(self.service + "api/select_books.php", category=categoryId)
		root = ElementTree.parse(fd).getroot()
		for book in root.findall(".//book"):
			yield (book.text, book.get("id"))

	def getLists(self, bookId):
		fd = self._open(self.service + "api/select_lists.php", book=bookId)
		root = ElementTree.parse(fd).getroot()
		for list in root.findall(".//list"):
			yield (list.text, list.get("id"))

	def getList(self, listId):
		fd = self._open(self.service + "api/select_list.php", list=listId)
		root = ElementTree.parse(fd).getroot()

		list = root.findtext("list")
		return self._parseList(list, parseLenient=True)

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
			self._listView.doubleClicked.connect(self.accept)
			if not self.singleOnly:
				self._listView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)

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

	class BookSelectDialog(AbstractSelectDialog):
		singleOnly = True
		def retranslate(self):
			self.setWindowTitle(_("Select book"))
			self.label.setText(_("Please select a book"))

	class ListSelectDialog(AbstractSelectDialog):
		singleOnly = False
		def retranslate(self):
			self.setWindowTitle(_("Select list"))
			self.label.setText(_("Please select a list"))

class VocatrainApiModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(VocatrainApiModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "vocatrainApi"
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="buttonRegister"),
			self._mm.mods(type="wordListStringParser"),
			self._mm.mods(type="loaderGui"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("vocatrainApi.py",)

		x = 644
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

		self._enButton = self._buttonRegister.registerButton("load-from-internet")
		self._enButton.clicked.handle(self.importFromVocatrain)
		self._enButton.changePriority.send(self.priorities["all"])

		self._nlButton = self._buttonRegister.registerButton("load-from-internet")
		self._nlButton.clicked.handle(self.importFromWoordjesleren)
		#+1 so it gets less priority than the vocatrain (english)
		#button.
		self._nlButton.changePriority.send(self.priorities["all"] + 1)

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

		#Install translator
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)

		self._enButton.changeText.send(_("Import from vocatrain.com"))
		self._nlButton.changeText.send(_("Import from woordjesleren.nl"))

		#Translate all active dialogs
		for dialog in self._activeDialogs:
			dialog.retranslate()
			dialog.tab.title = dialog.windowTitle()

	@property
	def _parseList(self):
		return self._modules.default("active", type="wordListStringParser").parseList

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

	def importFromVocatrain(self):
		self._selectCategory(VocatrainApi(self._parseList))

	def importFromWoordjesleren(self):
		api = VocatrainApi(self._parseList)
		api.service = "http://woordjesleren.nl/"

		self._selectCategory(api)

	def _selectCategory(self, api):
		with self._handlingWebErrors(api):
			d = self._showDialog(CategorySelectDialog(api.getCategories()))
			d.accepted.connect(lambda: self._selectBook(api, d))

	def _selectBook(self, api, dialog):
		categoryId = dialog.chosenItems[0]
		with self._handlingWebErrors(api):
			d = self._showDialog(BookSelectDialog(api.getBook(categoryId)))
			d.accepted.connect(lambda: self._selectList(api, d))

	def _selectList(self, api, dialog):
		bookId = dialog.chosenItems[0]
		with self._handlingWebErrors(api):
			d = self._showDialog(ListSelectDialog(api.getLists(bookId)))
			d.accepted.connect(lambda: self._loadSelectedList(api, d))

	def _loadSelectedList(self, api, dialog):
		with self._handlingWebErrors(api):
			for listId in dialog.chosenItems:
				list = api.getList(listId)
				try:
					self._loadList(list)
				except NotImplementedError:
					return

			#everything went well
			self._uiModule.statusViewer.show(_("The word list was imported from %s successfully.") % self._serviceNameForApi(api))

	def _serviceNameForApi(self, api):
		#[5:-1] to strip http:// and the final /
		serviceName = api.service[7:-1]

		return serviceName

	@contextlib.contextmanager
	def _handlingWebErrors(self, api):
		serviceName = self._serviceNameForApi(api)
		try:
			yield
		except urllib2.URLError, e:
			#for debugging purposes
			logger.debug(e, exc_info=True)
			QtGui.QMessageBox.warning(
				self._uiModule.qtParent,
				_("No %s connection") % serviceName,
				_("{serviceName} didn't accept the connection. Are you sure that your internet connection works and {serviceName} is online?").format(serviceName=serviceName)
			)

	def _loadList(self, lesson):
		self._modules.default("active", type="loaderGui").loadFromLesson("words", lesson)

	def disable(self):
		self.active = False

		self._buttonRegister.unregisterButton(self._enButton)
		self._buttonRegister.unregisterButton(self._nlButton)

		del self._modules
		del self._uiModule
		del self._buttonRegister

		del self._activeDialogs
		del self._enButton
		del self._nlButton

def init(moduleManager):
	return VocatrainApiModule(moduleManager)
