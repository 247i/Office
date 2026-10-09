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

class Printer(object):
	def __init__(self, module, dataType, lesson, printer, *args, **kwargs):
		super(Printer, self).__init__(*args, **kwargs)

		self.module = module
		self.dataType = dataType
		self.lesson = lesson
		self.printer = printer

	def print_(self):
		self.module.print_(self.dataType, self.lesson, self.printer)

class PrinterModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(PrinterModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "printer"
		self.uses = (
			self._mm.mods(type="print"),
		)
		self.requires = (
			self._mm.mods(type="lessonTracker"),
		)

	def print_(self, printer):
		dataType = self._lessonTracker.currentLesson.dataType
		printers = [
			Printer(module, dataType, self._lessonTracker.currentLesson, printer)
			for module in self._modules.sort("active", type="print")
			if dataType in module.prints
		]

		if not printers:
			raise NotImplementedError()

		printerWrapper = printers[0]
		#Print
		printerWrapper.print_()

	@property
	def printSupport(self):
		#Checks for printer modules, and if there is a gui module for
		#the data type(s) they can provide
		try:
			dataType = self._lessonTracker.currentLesson.dataType
		except AttributeError:
			return False
		return any(
			dataType in module.prints
			for module in self._mm.mods("active", type="print")
		)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._lessonTracker = self._modules.default("active", type="lessonTracker")

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self._lessonTracker

def init(moduleManager):
	return PrinterModule(moduleManager)
