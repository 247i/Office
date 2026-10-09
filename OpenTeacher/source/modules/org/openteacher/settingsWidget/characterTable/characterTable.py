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

def installQtClasses():
	global Model, SettingsWidget

	class Model(QtCore.QAbstractTableModel):
		def __init__(self, data, *args, **kwargs):
			super(Model, self).__init__(*args, **kwargs)

			self.data = data

		def rowCount(self, parent):
			return len(self.data)

		def columnCount(self, parent):
			return len(self.data[0])

		def data(self, index, role):
			if not index.isValid() or role not in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
				return
			return self.data[index.row()][index.column()]

		def setData(self, index, value, role):
			if not index.isValid() or role != QtCore.Qt.EditRole:
				return False
			value = unicode(value.toString())
			if len(value) > 1 and not (len(value) == 2 and value[0] == "\\"):
				return False
			self.data[index.row()][index.column()] = value
			self.dataChanged.emit(index, index)
			return True

		def flags(self, index):
			flags = super(Model, self).flags(index)
			if index.isValid():
				flags = flags | QtCore.Qt.EditRole
			return flags

	class SettingsWidget(QtGui.QTableView):
		def __init__(self, setting, *args, **kwargs):
			super(SettingsWidget, self).__init__(*args, **kwargs)

			self._setting = setting

			model = Model(setting["value"])
			model.dataChanged.connect(self._resetValue)
			self.setModel(model)

			self.setAlternatingRowColors(True)
			self.resizeColumnsToContents()
			self.resizeRowsToContents()
			self.horizontalHeader().hide()
			self.verticalHeader().hide()

		def _resetValue(self):
			"""To make the settings callback get called"""
			self._setting["value"] = self.model().data

class SettingsWidgetModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(SettingsWidgetModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "settingsWidget"

		self.requires = (
			self._mm.mods(type="ui"),
		)

	def createWidget(self, *args, **kwargs):
		return SettingsWidget(*args, **kwargs)

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		installQtClasses()

		self.widgetType = "character_table"
		self.active = True

	def disable(self):
		self.active = False

		del self.widgetType

def init(moduleManager):
	return SettingsWidgetModule(moduleManager)
