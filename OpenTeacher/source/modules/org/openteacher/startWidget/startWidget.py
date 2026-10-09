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

import weakref
import contextlib

def installQtClasses():
	global ButtonsGroupBox, StartWidget, LargeStartWidgetButton

	class LargeStartWidgetButton(QtGui.QToolButton):
		def __init__(self, *args, **kwargs):
			super(LargeStartWidgetButton, self).__init__(*args, **kwargs)

			#the label that handles the word wrapping
			self._label = QtGui.QLabel(self)
			self._label.setWordWrap(True)
			self._label.setIndent(32)
			self._label.setMargin(10)
			self._label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

			#setup the button sizes etc. correctly
			self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
			self.setIconSize(QtCore.QSize(32, 32))
			self.setSizePolicy(
				QtGui.QSizePolicy.MinimumExpanding,
				QtGui.QSizePolicy.Fixed
			)
			self.setMinimumSize(70, 70)
			#width: unlimited (Qt default). Height: fixed
			self.setMaximumSize(16777215, 70)

		def resizeEvent(self, *args, **kwargs):
			#resize the label when the button resizes
			result = super(LargeStartWidgetButton, self).resizeEvent(*args, **kwargs)
			self._label.resize(self.size())
			return result

		def setText(self, text):
			#set the text on the label instead of the button
			self._label.setText(text)

	class SmallStartWidgetButton(QtGui.QToolButton):
		def __init__(self, *args, **kwargs):
			super(SmallStartWidgetButton, self).__init__(*args, **kwargs)

			self.setAutoRaise(True)
			self.setSizePolicy(
				QtGui.QSizePolicy.MinimumExpanding,
				QtGui.QSizePolicy.MinimumExpanding,
			)
			self.setIcon(QtGui.QCommandLinkButton().icon())
			self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

	class ButtonsGroupBox(QtGui.QGroupBox):
		def __init__(self, customButtons=None, *args, **kwargs):
			super(ButtonsGroupBox, self).__init__(*args, **kwargs)

			self._buttons = {}

			self._smallLayout = QtGui.QVBoxLayout()
			self._largeLayout = QtGui.QGridLayout()

			if not customButtons:
				customButtons = []
			self._customButtons = customButtons

			layout = QtGui.QVBoxLayout()
			layout.addLayout(self._largeLayout)
			layout.addLayout(self._smallLayout)
			self.setLayout(layout)

		@staticmethod
		def _emptyLayout(layout):
			while True:
				item = layout.takeAt(0)
				if not item:
					break
				if item.widget():
					item.widget().setParent(None)

		def _updateLayout(self):
			self._emptyLayout(self._largeLayout)
			self._emptyLayout(self._smallLayout)

			i = 0
			j = 0
			for button, desc in sorted(self._buttons.iteritems(), key=lambda data: data[1]["priority"]):
				if desc["size"] == "large":
					#make button
					qtButton = LargeStartWidgetButton()
					qtButton.setIcon(QtGui.QIcon(desc["icon"]))
					#insert into layout
					self._largeLayout.addWidget(qtButton, i, j)
					j += 1
					if j > 1:
						j = 0
						i += 1
				else:
					#make button
					qtButton = SmallStartWidgetButton()
					#insert into layout
					self._smallLayout.addWidget(qtButton)

				#do stuff common to buttons of both sizes
				qtButton.setText(desc["text"])
				#lambda to remove some qt argument. The second lambda so it
				#works as expected in a for-loop.
				qtButton.clicked.connect(
					(lambda button: lambda: button.clicked.send())(button)
				)

			for button in self._customButtons:
				self._smallLayout.addWidget(button)

		def addButton(self, button):
			self._buttons[button] = {
				"text": "",
				"icon": "",
				"priority": 0,
				"size": "large",
			}
			button.changeText.handle(lambda t: self._updateText(button, t))
			button.changeIcon.handle(lambda i: self._updateIcon(button, i))
			button.changePriority.handle(lambda p: self._updatePriority(button, p))
			button.changeSize.handle(lambda s: self._updateSize(button, s))
			self._updateLayout()

		def removeButton(self, button):
			del self._buttons[button]
			self._updateLayout()

		def _updateText(self, button, text):
			self._buttons[button]["text"] = text
			self._updateLayout()

		def _updateIcon(self, button, icon):
			self._buttons[button]["icon"] = icon
			self._updateLayout()

		def _updatePriority(self, button, priority):
			self._buttons[button]["priority"] = priority
			self._updateLayout()

		def _updateSize(self, button, size):
			self._buttons[button]["size"] = size
			self._updateLayout()

	class LoadFromInternetButton(SmallStartWidgetButton):
		def __init__(self, *args, **kwargs):
			super(LoadFromInternetButton, self).__init__(*args, **kwargs)

			self.setPopupMode(QtGui.QToolButton.InstantPopup)

			self._buttons = {}

		def addButton(self, button):
			self._buttons[button] = {
				"text": "",
				"priority": 0,
			}
			button.changeText.handle(lambda t: self._updateText(button, t))
			button.changePriority.handle(lambda p: self._updatePriority(button, p))
			self._updateMenu()

		def removeButton(self, button):
			del self._buttons[button]
			self._updateMenu()

		def _updateText(self, button, text):
			self._buttons[button]["text"] = text
			self._updateMenu()

		def _updatePriority(self, button, priority):
			self._buttons[button]["priority"] = priority
			self._updateMenu()

		def _updateMenu(self):
			menu = QtGui.QMenu()
			sortedButtons = sorted(
				self._buttons.iteritems(),
				key=lambda (button, desc): desc["priority"]
			)
			for button, desc in sortedButtons:
				action = menu.addAction(desc["text"])
				#first lambda to remove some qt argument. The second
				#lambda so it works as expected in the for loop.
				action.triggered.connect(
					(lambda button: lambda: button.clicked.send())(button)
				)
			self.setMenu(menu)

	class StartWidget(QtGui.QSplitter):
		def __init__(self, recentlyOpenedViewer, *args, **kwargs):
			super(StartWidget, self).__init__(*args, **kwargs)

			self.loadFromInternetButton = LoadFromInternetButton()

			self.createLessonGroupBox = ButtonsGroupBox()
			self.loadLessonGroupBox = ButtonsGroupBox([self.loadFromInternetButton])

			openLayout = QtGui.QVBoxLayout()
			openLayout.addWidget(self.createLessonGroupBox)
			openLayout.addWidget(self.loadLessonGroupBox)
			openLayout.addStretch()

			left = self.style().pixelMetric(QtGui.QStyle.PM_LayoutLeftMargin)
			openLayout.setContentsMargins(left, 0, 0, 0)

			openWidget = QtGui.QWidget(self)
			openWidget.setLayout(openLayout)

			self.addWidget(openWidget)

			self.setStretchFactor(0, 7)

			if recentlyOpenedViewer:
				recentlyOpenedLayout = QtGui.QVBoxLayout()

				right = self.style().pixelMetric(QtGui.QStyle.PM_LayoutRightMargin)
				recentlyOpenedLayout.addWidget(recentlyOpenedViewer)

				self.recentlyOpenedGroupBox = QtGui.QGroupBox()
				self.recentlyOpenedGroupBox.setLayout(recentlyOpenedLayout)

				self.addWidget(self.recentlyOpenedGroupBox)
				self.setStretchFactor(1, 2)

			self.retranslate()

		def retranslate(self):
			self.createLessonGroupBox.setTitle(_("Create lesson:"))
			self.loadLessonGroupBox.setTitle(_("Load lesson:"))
			self.loadFromInternetButton.setText(_("Load from the internet"))
			with contextlib.ignored(AttributeError):
				self.recentlyOpenedGroupBox.setTitle(_("Recently opened:"))

		def _widgetForButton(self, button):
			return {
				"create": self.createLessonGroupBox,
				"load": self.loadLessonGroupBox,
				"load-from-internet": self.loadFromInternetButton,
			}.get(button.category)

		def addButton(self, button):
			widget = self._widgetForButton(button)
			if widget:
				widget.addButton(button)

		def removeButton(self, button):
			widget = self._widgetForButton(button)
			if widget:
				widget.removeButton(button)

class StartWidgetModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(StartWidgetModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "startWidget"

		self.requires = (
			self._mm.mods(type="buttonRegister"),
		)
		self.uses = (
			self._mm.mods(type="recentlyOpenedViewer"),
			self._mm.mods(type="translator"),
		)
		self.filesWithTranslations = ("startWidget.py",)

	def createStartWidget(self):
		"""By calling this method, you need to be able to guarantee that
		   there's already a QApplication active. E.g. by depending on
		   'ui', or by being the module that manages the QApplication...

		"""
		try:
			recentlyOpenedViewer = self._modules.default(
				"active",
				type="recentlyOpenedViewer"
			).createViewer()
		except IndexError:
			recentlyOpenedViewer = None
		widget = StartWidget(recentlyOpenedViewer)

		self._register.addButton.handle(widget.addButton)
		self._register.removeButton.handle(widget.removeButton)

		self._activeWidgets.add(weakref.ref(widget))
		return widget

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

		for ref in self._activeWidgets:
			widget = ref()
			if widget is not None:
				widget.retranslate()

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		installQtClasses()

		self._modules = set(self._mm.mods(type="modules")).pop()
		self._register = self._modules.default("active", type="buttonRegister")

		self._activeWidgets = set()

		#load translator
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self._register
		del self._activeWidgets

def init(moduleManager):
	return StartWidgetModule(moduleManager)
