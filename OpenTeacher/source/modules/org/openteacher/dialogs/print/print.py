#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2013, Marten de Vries
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

class PrintDialogModule(object):
	"""The print dialog."""

	def __init__(self, moduleManager, *args, **kwargs):
		super(PrintDialogModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "printDialog"

		self.requires = (
			self._mm.mods(type="ui"),
		)

	def getConfiguredPrinter(self):
		"""Returns a completely configured QPrinter, or None when the
		   user cancels the configuration dialog.

		"""
		printer = QtGui.QPrinter()

		printDialog = QtGui.QPrintDialog(printer)
		result = printDialog.exec_()
		if not result:
			return
		return printer

	def enable(self):
		global QtGui
		try:
			from PyQt4 import QtGui
		except ImportError:
			#remain inactive
			return
		self.active = True

	def disable(self):
		self.active = False

def init(moduleManager):
	return PrintDialogModule(moduleManager)
