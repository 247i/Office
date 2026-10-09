#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2013, Marten de Vries
#   Copyright 2011, Cas Widdershoven
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

from PyQt4 import QtCore, QtGui
import contextlib

class LoginDialog(QtGui.QDialog):
	def __init__(self, store, *args, **kwargs):
		super(LoginDialog, self).__init__(*args, **kwargs)

		self.emailTextBox = QtGui.QLineEdit()

		self.passwordTextBox = QtGui.QLineEdit()
		self.passwordTextBox.setEchoMode(QtGui.QLineEdit.Password)

		if store:
			self.saveCheckbox = QtGui.QCheckBox("", self)

		buttonBox = QtGui.QDialogButtonBox(
			QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok,
			parent=self
		)
		buttonBox.accepted.connect(self.accept)
		buttonBox.rejected.connect(self.reject)

		self.flayout = QtGui.QFormLayout()
		self.flayout.addRow("0", self.emailTextBox)
		self.flayout.addRow("1", self.passwordTextBox)
		if store:
			self.flayout.addRow(self.saveCheckbox)

		layout = QtGui.QVBoxLayout()
		layout.addLayout(self.flayout)
		layout.addStretch()
		layout.addWidget(buttonBox)

		self.setLayout(layout)

	@property
	def email(self):
		return unicode(self.emailTextBox.text())

	@property
	def password(self):
		return unicode(self.passwordTextBox.text())
		
	@property
	def saveCheck(self):
		try:
			return self.saveCheckbox.isChecked()
		except AttributeError:
			return False

	def retranslate(self):
		self.setWindowTitle(_("WRDS - login please:"))

		self.flayout.itemAt(0, QtGui.QFormLayout.LabelRole).widget().setText(
			_("Email:")
		)
		self.flayout.itemAt(1, QtGui.QFormLayout.LabelRole).widget().setText(
			_("Password:")
		)
		with contextlib.ignored(AttributeError):
			self.saveCheckbox.setText(_("Remember email address and password"))

class ReadOnlyStringListModel(QtGui.QStringListModel):
	def flags(self, index):
		return QtCore.QAbstractItemModel.flags(self, index)

class ListChoiceDialog(QtGui.QDialog):
	def __init__(self, list, parent=None):
		super(ListChoiceDialog, self).__init__(parent)

		self.listView = QtGui.QListView()
		listModel = ReadOnlyStringListModel(list)
		self.listView.setModel(listModel)
		self.listView.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
		self.listView.doubleClicked.connect(self.accept)

		buttonBox = QtGui.QDialogButtonBox(
			QtGui.QDialogButtonBox.Cancel | QtGui.QDialogButtonBox.Ok,
			parent=self
		)
		buttonBox.accepted.connect(self.accept)
		buttonBox.rejected.connect(self.reject)

		layout = QtGui.QVBoxLayout()
		layout.addWidget(self.listView)
		layout.addWidget(buttonBox)
		self.setLayout(layout)

	@property
	def selectedRowIndices(self):
		return [i.row() for i in self.listView.selectedIndexes()]

	def retranslate(self):
		self.setWindowTitle(_("WRDS - Please choose a list:"))

class UserListChoiceDialog(ListChoiceDialog):
	getFromShareClicked = QtCore.pyqtSignal([object])

	def __init__(self, *args, **kwargs):
		super(UserListChoiceDialog, self).__init__(*args, **kwargs)

		self._shareLabel = QtGui.QLabel()
		self._shareBox = QtGui.QLineEdit()
		self._getFromShareButton = QtGui.QPushButton()

		fromShareLayout = QtGui.QHBoxLayout()
		fromShareLayout.addWidget(self._shareLabel)
		fromShareLayout.addWidget(self._shareBox)
		fromShareLayout.addWidget(self._getFromShareButton)

		self.layout().insertLayout(0, fromShareLayout)

		self._getFromShareButton.clicked.connect(
			#lambda so we can pass the argument.
			lambda: self.getFromShareClicked.emit(self._shareBox.text())
		)

	def retranslate(self, *args, **kwargs):
		super(UserListChoiceDialog, self).retranslate(*args, **kwargs)

		self._shareLabel.setText(_("WRDS Share:"))
		#TRANSLATORS: please only translate the 'share-name' part here,
		#TRANSLATORS: unless you have a good reason to do something
		#TRANSLATORS: else, of course ;).
		self._shareBox.setText(_("share-name.wrts.nl"))
		self._getFromShareButton.setText(_("Get from share"))
