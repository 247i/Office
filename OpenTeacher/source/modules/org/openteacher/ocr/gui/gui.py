#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2013, Marten de Vries
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

import sys
import os
import tempfile
import contextlib

def installQtClasses():
	global OcrWizard

	class ImageView(QtGui.QGraphicsView):
		def __init__(self, *args, **kwargs):
			super(ImageView, self).__init__(*args, **kwargs)

			self.setScene(QtGui.QGraphicsScene())

			self._rect = self.scene().addRect(0.0, 0.0, 0.0, 0.0)
			self._rect.setZValue(1)
			self._imageItem = None

		def wheelEvent(self, event):
			factor = 1.2
			if event.delta() < 0:
				factor = 1.0 / factor
			self.scale(factor, factor)

		def updateImage(self, path):
			if self._imageItem:
				self.scene().removeItem(self._imageItem)
			self._imageItem = self.scene().addPixmap(QtGui.QPixmap(path))

		def getExcision(self):
			size = self._rect.rect().size().toSize()
			if size.isEmpty():
				raise ValueError("Empty selection")
			img = QtGui.QImage(size, QtGui.QImage.Format_ARGB32_Premultiplied)
			painter = QtGui.QPainter(img)
			self.scene().render(painter, QtCore.QRectF(), self._rect.rect())
			return img

		def updateRotation(self, value):
			if self._imageItem:
				self._imageItem.setRotation(value)

		def mousePressEvent(self, event):
			self._startPos = self.mapToScene(event.pos())

		def mouseReleaseEvent(self, event):
			newRect = QtCore.QRectF(
				self._startPos,
				self.mapToScene(QtCore.QPoint(event.pos()))
			).normalized()
			self._rect.setRect(newRect)

		mouseMoveEvent = mouseReleaseEvent

	class StartPage(QtGui.QWizardPage):
		def __init__(self, *args, **kwargs):
			super(StartPage, self).__init__(*args, **kwargs)

			self._label = QtGui.QLabel()
			self._label.setWordWrap(True)
			vbox = QtGui.QVBoxLayout()
			vbox.addWidget(self._label)
			self.setLayout(vbox)

		def retranslate(self):
			self.setTitle(_("Introduction"))
			self._label.setText(_("This wizard will guide you through the process of creating a word list from a scan or picture of a physical word list. Click 'Next' to start."))

	class SignalLabel(QtGui.QLabel):
		textChanged = QtCore.pyqtSignal()

		def setText(self, *args, **kwargs):
			result = super(SignalLabel, self).setText(*args, **kwargs)
			self.textChanged.emit()
			return result

	class ImageChoicePage(QtGui.QWizardPage):
		def __init__(self, *args, **kwargs):
			super(ImageChoicePage, self).__init__(*args, **kwargs)

			self._label = QtGui.QLabel()
			self._label.setWordWrap(True)

			self._chooseLocationButton = QtGui.QPushButton()
			self._chooseLocationButton.clicked.connect(self._chooseLocationClicked)

			self._locationLabelLabel = QtGui.QLabel()
			self._locationLabel = SignalLabel()
			self.registerField("path", self._locationLabel, "text", self._locationLabel.textChanged)

			vbox = QtGui.QVBoxLayout()
			vbox.addWidget(self._label)
			vbox.addWidget(self._chooseLocationButton)
			vbox.addWidget(self._locationLabelLabel)
			vbox.addWidget(self._locationLabel)
			self.setLayout(vbox)

		def retranslate(self):
			self.setTitle(_("Choose an image"))

			self._label.setText(_("Please choose the location of the scan or picture of the physical word list on your system below."))
			self._chooseLocationButton.setText(_("Click here to choose a location"))
			self._locationLabelLabel.setText(_("Location:"))

		def _chooseLocationClicked(self):
			extsList = map(unicode, QtGui.QImageReader.supportedImageFormats())
			exts = "*." + " *.".join(extsList)
			filter = _("Images ({extensions})".format(extensions=exts))
			path = QtGui.QFileDialog.getOpenFileName(self, filter=filter)
			if path:
				self._locationLabel.setText(path)
				self.completeChanged.emit()

		def isComplete(self):
			path = unicode(self._locationLabel.text())
			return os.path.exists(path.encode(sys.getfilesystemencoding()))

	class ImageEditPage(QtGui.QWizardPage):
		def __init__(self, *args, **kwargs):
			super(ImageEditPage, self).__init__(*args, **kwargs)

			self._label1 = QtGui.QLabel()
			self._label2 = QtGui.QLabel()
			self._label1.setWordWrap(True)
			self._label2.setWordWrap(True)
			self._view = ImageView()

			self._rotationSlider = QtGui.QSlider()
			self._rotationSlider.setOrientation(QtCore.Qt.Horizontal)
			self._rotationSlider.setMinimum(-180)
			self._rotationSlider.setMaximum(180)
			self._rotationSlider.valueChanged.connect(self._view.updateRotation)

			vbox = QtGui.QVBoxLayout()
			vbox.addWidget(self._label1)
			vbox.addWidget(self._rotationSlider)
			vbox.addWidget(self._label2)
			vbox.addWidget(self._view)
			self.setLayout(vbox)

		def initializePage(self):
			path = self.field("path").toString()
			self._view.updateImage(path)

		def retranslate(self):
			self.setTitle(_("Make image ready"))
			self._label1.setText(_("Please make sure the image is rotated completely upright with the rotation slider under this text:"))
			self._label2.setText(_("When the image is completely upright, make a selection on the image with the mouse with in the left top the first question to include and in the right bottom the last answer to include. Click 'Next' when done."))

		def getExcision(self):
			return self._view.getExcision()

	class OcrThread(QtCore.QThread):
		def __init__(self, loadWordList, img, *args, **kwargs):
			super(OcrThread, self).__init__(*args, **kwargs)

			self._loadWordList = loadWordList
			self._img = img

		def run(self):
			fd, imgPath = tempfile.mkstemp(".png")
			os.close(fd)
			self._img.save(imgPath)

			self.lesson = self._loadWordList(imgPath)

			os.remove(imgPath)

	class PreviewPage(QtGui.QWizardPage):
		def __init__(self, loadWordList, composeList, *args, **kwargs):
			super(PreviewPage, self).__init__(*args, **kwargs)

			self._loadWordList = loadWordList
			self._composeList = composeList

			self._label = QtGui.QLabel()
			self._label.setWordWrap(True)
			self._previewTextEdit = QtGui.QTextEdit()
			self._previewTextEdit.setReadOnly(True)

			vbox = QtGui.QVBoxLayout()
			vbox.addWidget(self._label)
			vbox.addWidget(self._previewTextEdit)
			self.setLayout(vbox)

		def initializePage(self):
			try:
				image = self.wizard().getExcision()
			except ValueError:
				QtGui.QMessageBox.critical(self, _("No selection was made"), _("No selection was made. Please try again."))
				#next event loop iteration, otherwise Qt messes up
				#completely (combining multiple pages).
				QtCore.QTimer.singleShot(0, self.wizard().back)
				return

			self._thread = OcrThread(self._loadWordList, image)
			self._thread.finished.connect(self._showPreview)
			self._thread.start()

			self._dialog = QtGui.QProgressDialog(self, QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowTitleHint)
			self._dialog.setWindowTitle(_("Recognizing word list..."))
			self._dialog.setLabelText(_("Recognizing word list..."))
			self._dialog.setCancelButton(None)
			self._dialog.setRange(0, 0)
			self._dialog.setModal(True)
			self._dialog.show()

		def _showPreview(self):
			self._dialog.hide()
			self.lesson = self._thread.lesson
			text = self._composeList(self.lesson)
			self._previewTextEdit.setText(text)

		def retranslate(self):
			self._label.setText(_("Down here, you can see a preview of the result. There will probably be some wrongly recognized words in there, but the structure of the word list should be recognizable. If not, click 'Back' and try again. Otherwise, click 'Finish'."))
			self.setTitle(_("Result preview"))

	class OcrWizard(QtGui.QWizard):
		def __init__(self, loadWordList, composeList, *args, **kwargs):
			super(OcrWizard, self).__init__(*args, **kwargs)

			self._imageEditPage = ImageEditPage()
			self._previewPage = PreviewPage(loadWordList, composeList)
			self._pages = [
				StartPage(),
				ImageChoicePage(),
				self._imageEditPage,
				self._previewPage,
			]

			for page in self._pages:
				self.addPage(page)

			self.setWizardStyle(QtGui.QWizard.ClassicStyle)

		def getExcision(self):
			return self._imageEditPage.getExcision()

		def getLesson(self):
			return self._previewPage.lesson

		def retranslate(self):
			for page in self._pages:
				page.retranslate()

class OcrGuiModule(object):
	"""Provides a wizard that assists the user in loading a word list
	   from a picture or scan of a real-world word list. (E.g. out of a
	   book). The actual logic is in the ocrWordListLoader module,
	   although some work around that (making the image ready) is done
	   by this module.

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(OcrGuiModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "ocrGui"
		self.requires = (
			self._mm.mods(type="ui"),
			self._mm.mods(type="ocrWordListLoader"),
			self._mm.mods(type="buttonRegister"),
			self._mm.mods(type="wordListStringComposer"),
			self._mm.mods(type="loaderGui"),
		)
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.priorities = {
			"all": 975,
		}
		self.filesWithTranslations = ("gui.py",)

	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		installQtClasses()

		self._modules = next(iter(self._mm.mods(type="modules")))

		self._button = self._modules.default("active", type="buttonRegister").registerButton("create")
		self._button.clicked.handle(self._startWizard)
		self._button.changePriority.send(self.priorities["all"])
		self._button.changeSize.send("small")

		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

	_uiModule = property(lambda self: self._modules.default("active", type="ui"))
	_loadWordList = property(lambda self: self._modules.default("active", type="ocrWordListLoader").loadWordList)
	_composeList = property(lambda self: self._modules.default("active", type="wordListStringComposer").composeList)
	_loadFromLesson = property(lambda self: self._modules.default("active", type="loaderGui").loadFromLesson)

	def _startWizard(self):
		self._wizard = OcrWizard(self._loadWordList, self._composeList)

		tab = self._uiModule.addCustomTab(self._wizard)
		tab.closeRequested.handle(self._wizard.reject)
		self._wizard.tab = tab

		self._retranslate()
		self._wizard.finished.connect(tab.close)
		self._wizard.accepted.connect(self._loadResultiveLesson)

	def _loadResultiveLesson(self):
		lesson = self._wizard.getLesson()
		with contextlib.ignored(NotImplementedError):
			self._loadFromLesson("words", lesson)

	def _retranslate(self):
		global _, ngettext
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)

		self._button.changeText.send(_("Create words lesson from a scan or picture"))
		if hasattr(self, "_wizard"):
			self._wizard.retranslate()
			self._wizard.setWindowTitle(_("Words lesson from picture"))
			self._wizard.tab.title = self._wizard.windowTitle()

	def disable(self):
		self.active = False

		del self._modules
		del self._button

		if hasattr(self, "_wizard"):
			del self._pages

def init(moduleManager):
	return OcrGuiModule(moduleManager)
