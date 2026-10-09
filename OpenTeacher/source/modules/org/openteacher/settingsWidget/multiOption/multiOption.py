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

def installQtClasses():
	global MultiOptionListModel, SettingsWidget

	class MultiOptionListModel(QtCore.QAbstractListModel):
		def __init__(self, options, active, *args, **kwargs):
			super(MultiOptionListModel, self).__init__(*args, **kwargs)

			self.options = options
			self.active = set()
			for data in active:
				for label, secondData in options:
					if data == secondData:
						self.active.add((label, data))

		def rowCount(self, parent=None):
			return len(self.options)

		def data(self, index, role):
			if not index.isValid():
				return
			if role == QtCore.Qt.DisplayRole:
				return self.options[index.row()][0]
			elif role == QtCore.Qt.UserRole:
				return self.options[index.row()][1]
			elif role == QtCore.Qt.CheckStateRole:
				if self.options[index.row()] in self.active:
					return QtCore.Qt.Checked
				else:
					return QtCore.Qt.Unchecked

		def setData(self, index, value, role):
			if not index.isValid():
				return False
			if role == QtCore.Qt.CheckStateRole:
				option = self.options[index.row()]
				if value == QtCore.Qt.Checked:
					self.active.add(option)
				else:
					self.active.remove(option)
				self.dataChanged.emit(index, index)
				return True
			return False

		def flags(self, index):
			return (
				QtCore.Qt.ItemIsEnabled |
				QtCore.Qt.ItemIsSelectable |
				QtCore.Qt.ItemIsUserCheckable
			)

		@property
		def value(self):
			return [
				option[1]
				for option in self.options
				if option in self.active
			]

	class SettingsWidget(QtGui.QListView):
		def __init__(self, setting, *args, **kwargs):
			super(SettingsWidget, self).__init__(*args, **kwargs)

			self._setting = setting

			model = MultiOptionListModel(setting["options"], setting["value"])
			model.dataChanged.connect(self._valueChanged)
			self.setModel(model)

		def _valueChanged(self, topLeft, bottomRight):
			self._setting["value"] = self.model().value

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

		self.widgetType = "multiOption"
		self.active = True

	def disable(self):
		self.active = False

		del self.widgetType

def init(moduleManager):
	return SettingsWidgetModule(moduleManager)

if __name__ == "__main__":
	app = QtGui.QApplication([])
	sw = SettingsWidget({"value": [1], "options": [("a", 1), ("b", 2)]})
	sw.show()
	app.exec_()
