#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2013, Marten de Vries
#	Copyright 2008-2011, Roel Huybrechts
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

#pyratemp, QtCore & QtGui imported in enable()
import random
import weakref

def installQtClasses():
	global AboutDialog

	class AboutTextLabel(QtGui.QLabel):
		def __init__(self, metadata, templatePath, *args, **kwargs):
			super(AboutTextLabel, self).__init__(*args, **kwargs)

			self._metadata = metadata
			self._templatePath = templatePath

			self.setOpenExternalLinks(True)
			self.setAlignment(QtCore.Qt.AlignCenter)

		def retranslate(self):
			t = pyratemp.Template(open(self._templatePath).read())
			data = self._metadata.copy()
			data.update({
				"websiteText": _("Project website"),
			})
			self.setText(t(**data))

	class AboutImageLabel(QtGui.QLabel):
		def __init__(self, metadata, *args, **kwargs):
			super(AboutImageLabel, self).__init__(*args, **kwargs)

			self.setPixmap(QtGui.QPixmap(metadata["comicPath"]))
			self.setAlignment(QtCore.Qt.AlignCenter)

	class AboutWidget(QtGui.QWidget):
		"""The about page (shows some metadata)."""

		def __init__(self, metadata, templatePath, *args, **kwargs):
			super(AboutWidget, self).__init__(*args, **kwargs)

			imageLabel = AboutImageLabel(metadata)
			self.textLabel = AboutTextLabel(metadata, templatePath)

			layout = QtGui.QVBoxLayout()
			layout.addStretch()
			layout.addWidget(imageLabel)
			layout.addStretch()
			layout.addWidget(self.textLabel)
			layout.addStretch()
			self.setLayout(layout)

		def retranslate(self):
			self.textLabel.retranslate()

	class ShortLicenseWidget(QtGui.QWidget):
		def __init__(self, metadata, *args, **kwargs):
			super(ShortLicenseWidget, self).__init__(*args, **kwargs)

			label = QtGui.QLabel()
			label.setText(metadata["licenseIntro"])
			self.fullLicenseButton = QtGui.QPushButton()

			vbox = QtGui.QVBoxLayout()
			vbox.addWidget(label)
			vbox.addWidget(self.fullLicenseButton)
			
			self.layout = QtGui.QHBoxLayout()
			self.layout.addStretch()
			self.layout.addLayout(vbox)
			self.layout.addStretch()
			self.setLayout(self.layout)

		def retranslate(self):
			self.fullLicenseButton.setText(_("Full license text"))

	class LongLicenseWidget(QtGui.QTextEdit):
		def __init__(self, metadata, *args, **kwargs):
			super(LongLicenseWidget, self).__init__(*args, **kwargs)

			self.setReadOnly(True)
			self.setText(metadata["license"])

	class LicenseWidget(QtGui.QStackedWidget):
		"""The license page. Can show both the short copyright notice,
		   and the full license.

		"""
		def __init__(self, metadata, *args, **kwargs):
			super(LicenseWidget, self).__init__(*args, **kwargs)

			self.shortLicenseWidget = ShortLicenseWidget(metadata)
			self.longLicenseWidget = LongLicenseWidget(metadata)

			self.shortLicenseWidget.fullLicenseButton.clicked.connect(self.showFullLicense)

			self.addWidget(self.shortLicenseWidget)
			self.addWidget(self.longLicenseWidget)

		def retranslate(self):
			self.shortLicenseWidget.retranslate()

		def showFullLicense(self):
			self.setCurrentIndex(1) #longLicenseWidget

	class PersonWidget(QtGui.QWidget):
		def __init__(self, *args, **kwargs):
			super(PersonWidget, self).__init__(*args, **kwargs)

			self.taskLabel = QtGui.QLabel("")
			self.taskLabel.setStyleSheet("font-size:24pt;")
			self.nameLabel = QtGui.QLabel("")
			self.nameLabel.setStyleSheet("font-size:36pt;")

			#to prevent flash of unstyled content
			palette = QtGui.QPalette()
			color = palette.windowText().color()
			color.setAlpha(0)
			palette.setColor(QtGui.QPalette.WindowText, color)

			self.taskLabel.setPalette(palette)
			self.nameLabel.setPalette(palette)

			self.taskLabel.setAlignment(QtCore.Qt.AlignCenter)
			self.nameLabel.setAlignment(QtCore.Qt.AlignCenter)

			self.layout = QtGui.QVBoxLayout()
			self.layout.addWidget(self.taskLabel)
			self.layout.addStretch()
			self.layout.addWidget(self.nameLabel)
			self.setLayout(self.layout)

		def update(self, task, name):
			self.taskLabel.setText(task)
			self.nameLabel.setText(name)

		def fade(self, step):
			if step <= 255:
				alpha = step
			elif step > 765:
				alpha = 1020 - step
			else:
				return

			palette = QtGui.QPalette()
			color = palette.windowText().color()
			color.setAlpha(alpha)
			palette.setColor(QtGui.QPalette.WindowText, color)

			self.taskLabel.setPalette(palette)
			self.nameLabel.setPalette(palette)

	class AuthorsWidget(QtGui.QWidget):
		"""The authors widget. Displays all authors of OpenTeacher with
		   a fade animation.

		"""
		def __init__(self, authors, *args, **kwargs):
			super(AuthorsWidget, self).__init__(*args, **kwargs)
			
			if len(authors) == 0:
				self.authors = None
			else:
				self.backupAuthors = list(authors)
				self.authors = []

			self.personWidget = PersonWidget()
			self.launchpadLabel = QtGui.QLabel()
			self.launchpadLabel.setAlignment(QtCore.Qt.AlignCenter)

			self.layout = QtGui.QVBoxLayout()
			self.layout.addWidget(self.personWidget)
			self.layout.addStretch()
			self.layout.addWidget(self.launchpadLabel)
			self.setLayout(self.layout)

			self.animationActive = False

		def retranslate(self):
			self.launchpadLabel.setText(
				_("Thanks to all Launchpad contributors!")
			)

		def startAnimation(self):
			self.nextAuthor()
			timeLine = QtCore.QTimeLine(5000, self)
			#4x 255; 2x for the alpha gradients, 2x for a pause
			timeLine.setFrameRange(0, 1020)
			timeLine.frameChanged.connect(self.personWidget.fade)
			timeLine.finished.connect(self.startAnimation)
			timeLine.start()
			self.animationActive = True

		def nextAuthor(self):
			if self.authors is None:
				return
			try:
				self.personWidget.update(*self.authors.pop())
			except IndexError:
				self.authors = self.backupAuthors[:]
				random.shuffle(self.authors)
				self.nextAuthor()

	class AboutDialog(QtGui.QTabWidget):
		"""The about dialog, consists of an about page, a license page
		   and an authors page.

		"""
		def __init__(self, authors, metadata, templatePath, *args, **kwargs):
			super(AboutDialog, self).__init__(*args, **kwargs)

			self.setTabPosition(QtGui.QTabWidget.South)
			self.setDocumentMode(True)

			self.aboutWidget = AboutWidget(metadata, templatePath)
			self.licenseWidget = LicenseWidget(metadata)
			self.authorsWidget = AuthorsWidget(authors)

			self.addTab(self.aboutWidget, "")
			self.addTab(self.licenseWidget, "")
			self.addTab(self.authorsWidget, "")

			self.currentChanged.connect(self.startAnimation)

		def retranslate(self):
			self.setWindowTitle(_("About"))
			self.setTabText(0, _("About"))
			self.setTabText(1, _("License"))
			self.setTabText(2, _("Authors"))

			self.aboutWidget.retranslate()
			self.licenseWidget.retranslate()
			self.authorsWidget.retranslate()

		def startAnimation(self):
			if self.currentWidget() == self.authorsWidget and not self.authorsWidget.animationActive:
				self.authorsWidget.startAnimation()

class AboutDialogModule(object):
	"""Provides the about dialog."""

	def __init__(self, moduleManager, *args, **kwargs):
		super(AboutDialogModule, self).__init__(*args, **kwargs)

		self._mm = moduleManager
		self.type = "about"

		self.requires = (
			self._mm.mods(type="ui"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
			self._mm.mods(type="authors"),
		)
		self.filesWithTranslations = ("about.py",)

	def show(self):
		try:
			module = self._modules.default("active", type="authors")
		except IndexError:
			authors = set()
		else:
			authors = module.registeredAuthors
		metadata = self._modules.default("active", type="metadata").metadata
		templatePath = self._mm.resourcePath("about.html")
		dialog = AboutDialog(authors, metadata, templatePath)
		self._activeDialogs.add(weakref.ref(dialog))

		tab = self._modules.default("active", type="ui").addCustomTab(dialog)
		dialog.tab = tab
		tab.closeRequested.handle(tab.close)

		self._retranslate()

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
		for ref in self._activeDialogs:
			dialog = ref()
			if dialog is not None:
				dialog.retranslate()
				dialog.tab.title = dialog.windowTitle()

	def enable(self):
		global pyratemp
		global QtCore, QtGui
		try:
			import pyratemp
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return #remain inactive
		installQtClasses()

		self._modules = set(self._mm.mods(type="modules")).pop()
		self._activeDialogs = set()

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
		del self._activeDialogs

def init(moduleManager):
	return AboutDialogModule(moduleManager)
