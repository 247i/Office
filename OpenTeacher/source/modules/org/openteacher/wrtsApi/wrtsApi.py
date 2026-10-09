#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2012-2013, Marten de Vries
#	Copyright 2011, Cas Widdershoven
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

import contextlib
import logging
import functools

logger = logging.getLogger(__name__)

class WrtsApiModule(object):
	def __init__(self, moduleManager):
		super(WrtsApiModule, self).__init__()
		self._mm = moduleManager

		self.type = "wrtsApi"
		self.uses = (
			self._mm.mods(type="translator"),
			self._mm.mods(type="settings"),
		)
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="buttonRegister"),
			self._mm.mods(type="loaderGui"),
			self._mm.mods(type="lessonTracker"),
			self._mm.mods(type="wordsStringComposer"),
			self._mm.mods(type="wordsStringParser"),
		)
		x = 508
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
		self.filesWithTranslations = ("wrtsApi.py", "ui.py")

	def _updateMenuItems(self):
		lesson = self._lessonTracker.currentLesson
		canExport = bool(lesson) and lesson.dataType == "words"
		self._action.enabled = canExport

	def enable(self):
		global QtGui
		try:
			from PyQt4 import QtGui
		except ImportError:
			return
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._uiModule = self._modules.default("active", type="ui")
		self._lessonTracker = self._modules.default("active", type="lessonTracker")
		self._activeDialogs = set()

		self._ui = self._mm.import_("ui")
		self._api = self._mm.import_("api")

		self._button = self._modules.default("active", type="buttonRegister").registerButton("load-from-internet")
		self._button.clicked.handle(self.importFromWrts)
		self._button.changePriority.send(self.priorities["all"])

		self._action = self._uiModule.fileMenu.addAction(self.priorities["all"])
		self._action.triggered.handle(self.exportToWrts)

		self._lessonTracker.lessonChanged.handle(self._updateMenuItems)
		self._updateMenuItems()

		try:
			self._settings = self._modules.default(type="settings")
		except IndexError:
			self._emailSetting = {
				"value": u"",
			}
			self._passwordSetting = {
				"value": u"",
			}
			self._storeEnabled = False
		else:
			self._emailSetting = self._settings.registerSetting(**{
				"internal_name": "org.openteacher.wrtsApi.email",
				"type": "short_text",
				"defaultValue": u"",
			})
			self._passwordSetting = self._settings.registerSetting(**{
				"internal_name": "org.openteacher.wrtsApi.password",
				"type": "password",
				"defaultValue": u"",
			})
			self._storeEnabled = True

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		parse = self._modules.default(
			"active",
			type="wordsStringParser"
		).parse
		self._wrtsConnection = self._api.WrtsConnection(parse)

		self.active = True

	def disable(self):
		self.active = False

		self._action.remove()

		self._lessonTracker.lessonChanged.unhandle(self._updateMenuItems)

		del self._modules
		del self._uiModule
		del self._lessonTracker
		del self._activeDialogs
		del self._ui
		del self._api
		del self._button
		del self._settings
		del self._emailSetting
		del self._passwordSetting
		del self._wrtsConnection
		del self._storeEnabled
		del self._action

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
		self._ui._, self._ui.ngettext = _, ngettext

		#Translate button + menu action
		self._button.changeText.send(_("Import from WRDS"))
		self._action.text = _("Export to WRDS")

		#Translate settings
		self._emailSetting["name"] = _("Email")
		self._passwordSetting["name"] = _("Password")
		categories = {
			"category": _("Input and output"),
			"subcategory": _("WRDS Login credentials"),
		}
		self._emailSetting.update(categories)
		self._passwordSetting.update(categories)

		#Translate all active dialogs
		for dialog in self._activeDialogs:
			dialog.retranslate()
			dialog.tab.title = dialog.windowTitle()

	def _invalidLogin(self):
		QtGui.QMessageBox.warning(
			self._uiModule.qtParent,
			_("Invalid login credentials"),
			_("WRDS didn't accept the login credentials. Are you sure you entered your e-mail and password correctly?")
		)

	def _noConnection(self):
		QtGui.QMessageBox.warning(
			self._uiModule.qtParent,
			_("No WRDS connection"),
			_("WRDS didn't accept the connection. Are you sure that your internet connection works and WRDS is online?")
		)

	def _loginToWrts(self, success, forceLogin=False):
		"""Calls the `success` callback when logging in succeded,
		   otherwise it calls nothing.

		"""
		email = self._emailSetting["value"]
		password = self._passwordSetting["value"]

		blankCredentials = not (email and password)

		if forceLogin or blankCredentials:
			ld = self._showDialog(self._ui.LoginDialog(
				self._storeEnabled,
				self._uiModule.qtParent
			), previousTabOnClose=True)

			ld.accepted.connect(lambda: self._checkLoginFromDialog(ld, success))
		else:
			self._checkLogin(email, password, success, retry=True)

	def _checkLoginFromDialog(self, dialog, success):
		if dialog.saveCheck:
			self._emailSetting["value"] = dialog.email
			self._passwordSetting["value"] = dialog.password

		email, password = dialog.email, dialog.password

		self._checkLogin(email, password, success, retry=False)

	def _checkLogin(self, email, password, success, retry):
		try:
			self._wrtsConnection.logIn(email, password)
		except self._api.LoginError:
			if retry:
				self._loginToWrts(success, forceLogin=True)
			else:
				self._invalidLogin()
		except self._api.ConnectionError:
			self._noConnection()
		else:
			success()

	def _requires_login(f):
		@functools.wraps(f)
		def wrapper(self, *args, **kwargs):
			self._loginToWrts(success=lambda: f(self, *args, **kwargs))
		return wrapper

	@contextlib.contextmanager
	def _handlingWebErrors(self):
		try:
			yield
		except self._api.LoginError, e:
			logger.debug(e, exc_info=True)
			self._invalidLogin()
		except self._api.ConnectionError, e:
			logger.debug(e, exc_info=True)
			self._noConnection()

	@_requires_login
	def exportToWrts(self):
		lesson = self._lessonTracker.currentLesson

		with self._handlingWebErrors():
			try:
				self._wrtsConnection.exportWordList(
					lesson.list,
					self._modules.default("active", type="wordsStringComposer").compose
				)
			except self._api.NotEnoughMetadataError:
				QtGui.QMessageBox.warning(
					self._uiModule.qtParent,
					_("No word list metadata given."),
					_("Please fill in the wordlist title, question language and answer language first. Then try again.")
				)
				return

			self._uiModule.statusViewer.show(_("Word list succesfully exported to WRDS."))

	@_requires_login
	def importFromWrts(self):
		ldc = self._showDialog(self._ui.UserListChoiceDialog(
			self._wrtsConnection.listsParser.lists,
			self._uiModule.qtParent
		))

		ldc.getFromShareClicked.connect(ldc.reject)
		ldc.getFromShareClicked.connect(self._importFromWrtsShare)

		ldc.accepted.connect(lambda: self._doActualImport(
			self._wrtsConnection.listsParser,
			ldc.selectedRowIndices
		))

	def _showDialog(self, d, *args, **kwargs):
		self._activeDialogs.add(d)

		tab = self._uiModule.addCustomTab(d, *args, **kwargs)
		tab.closeRequested.handle(tab.close)
		d.finished.connect(tab.close)
		d.tab = tab

		self._retranslate()

		d.finished.connect(lambda: self._activeDialogs.remove(d))

		return d

	def _importFromWrtsShare(self, url):
		#from QString
		url = unicode(url)
		if url.endswith(".wrts.nl"):
			url = url[:-len(".wrts.nl")]
		url.strip("/")
		try:
			parser = self._wrtsConnection.shareListsParser(url)
		except self._api.ShareNotFoundError, e:
			QtGui.QMessageBox.critical(
				self._uiModule.qtParent,
				_("Can't find the share"),
				_("Can't find the share you requested. ('%s') Are you sure it exists?" % unicode(e))
			)
			return

		lcd = self._showDialog(self._ui.ListChoiceDialog(
			parser.lists,
			self._uiModule.qtParent
		))
		lcd.accepted.connect(
			lambda: self._doActualImport(parser, lcd.selectedRowIndices)
		)

	def _doActualImport(self, parser, selectedRowIndices):
		if len(selectedRowIndices) == 0:
			#No list selected, report.
			QtGui.QMessageBox.warning(
				self._uiModule.qtParent,
				_("No list selected"),
				_("No list was selected. Please try again.")
			)
			return

		with self._handlingWebErrors():
			for index in selectedRowIndices:
				listUrl = parser.getWordListUrl(index)
				list = self._wrtsConnection.importWordList(listUrl)

				loaderGui = self._modules.default("active", type="loaderGui")
				try:
					loaderGui.loadFromLesson("words", {
						"list": list,
						"resources": {},
					})
				except NotImplementedError:
					return

			#if everything went well
			self._uiModule.statusViewer.show(_("The word list was imported from WRDS successfully."))

def init(moduleManager):
	return WrtsApiModule(moduleManager)
