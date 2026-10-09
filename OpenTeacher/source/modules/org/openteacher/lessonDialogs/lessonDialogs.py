#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2012, Milan Boers
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

class LessonDialogsModule(object):
	"""This module isn't retranslated, since it only has very short
	   lasting dialogs. It's not worth the effort.

	'"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(LessonDialogsModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager
		
		self.type = "lessonDialogs"
		
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.requires = (
			self._mm.mods(type="ui"),
		)
		self.filesWithTranslations = ("lessonDialogs.py",)
	
	def enable(self):
		global QtGui
		try:
			from PyQt4 import QtGui
		except ImportError:
			return
		self._modules = set(self._mm.mods(type="modules")).pop()

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

	def _retranslate(self):
		#setup translation
		global _, ngettext

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)

	def disable(self):
		self.active = False
		
		del self._modules

	def okToClose(self, parent=None):
		"""Returns True if the user wants to save first, otherwise
		   returns False.

		"""
		result = QtGui.QMessageBox.question(
			parent,
			_("Unsaved data"),
			_("There are unsaved items or results. Are you sure you want to close?"),
			QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
			QtGui.QMessageBox.No
		)
		return result == QtGui.QMessageBox.Yes

	def onTabChanged(self, fileTab, enterWidget, teachWidget, func=None):
		"""Does some checks and then decides if the tab may be left in
		   its new position, or if it's changed back. (This function
		   handles the changing.)

		"""
		if fileTab.currentTab == enterWidget:
			if teachWidget.inLesson:
				warningD = QtGui.QMessageBox()
				warningD.setIcon(QtGui.QMessageBox.Warning)
				warningD.setWindowTitle(_("Warning"))
				warningD.setStandardButtons(QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
				warningD.setText(_("Are you sure you want to go back to the enter tab? This will end your lesson!"))
				feedback = warningD.exec_()
				if feedback == QtGui.QMessageBox.Ok:
					teachWidget.stopLesson(showResults=False)
				else:
					fileTab.currentTab = teachWidget
		elif fileTab.currentTab == teachWidget:
			# If there are no words
			if not "items" in enterWidget.lesson.list or len(enterWidget.lesson.list["items"]) == 0:
				QtGui.QMessageBox.critical(
					teachWidget,
					_("Not enough items"),
					_("You need to add items to your test first")
				)
				fileTab.currentTab = enterWidget
			elif func is not None:
				#no problems doing the checks, so the lesson can start.
				#call the callback.
				func()

def init(moduleManager):
	return LessonDialogsModule(moduleManager)
