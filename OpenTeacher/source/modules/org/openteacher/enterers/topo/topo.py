#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011, Milan Boers
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

import os
import weakref

class DummyLesson(object):
	pass

def installQtClasses():
	global EnterMapChooser, EnterPlaceByName, EnterPlacesWidget, EnterWidget

	class EnterPlacesWidget(QtGui.QListWidget):
		"""List widget of all the places"""

		def __init__(self, enterWidget, *args, **kwargs):
			super(EnterPlacesWidget, self).__init__(*args, **kwargs)
			
			self.enterWidget = enterWidget
		
		def update(self):
			self.clear()
			
			# Add all the places to the list
			for place in self.enterWidget.list["items"]:
				self.addItem(place["name"] + " (" + unicode(place["x"]) + "," + unicode(place["y"]) + ")")

	class EnterMapChooser(QtGui.QComboBox):
		"""The dropdown menu for choosing the map"""

		def __init__(self, parent, mapWidget, *args, **kwargs):
			super(EnterMapChooser, self).__init__(*args, **kwargs)
			
			self.mapWidget = mapWidget
			self.enterWidget = parent

			# Fill the MapChooser with the maps
			self._fillBox()
			# Change the map
			self._otherMap()

			self.activated.connect(self._otherMap)

			self.retranslate()

		def retranslate(self):
			#update the last combobox item
			self.removeItem(self.count() -1)
			self.addItem(_("From hard disk..."), unicode({}))

		def _fillBox(self):
			for module in base._modules.sort("active", type="map"):
				self.addItem(module.mapName, unicode({'mapName': module.mapName, 'mapPath': module.mapPath, 'knownPlaces': module.knownPlaces}))

			#the from harddisk item (retranslated)
			self.addItem("", unicode({}))
			
		def _otherMap(self):
			#custom map
			if self.currentMap == {}:
				def onSuccess(path):
					name = os.path.splitext(os.path.basename(path))[0]

					self.insertItem(0, name, unicode({'mapPath': path, 'knownPlaces': ''}))
					self.prevIndex += 1
					self.setCurrentIndex(0)
					#start the process over again.
					self._otherMap()
				def onError():
					self.setCurrentIndex(self.prevIndex)
				_fileDialogsMod = base._modules.default("active", type="fileDialogs")
				path = _fileDialogsMod.getLoadPath(
					onSuccess,
					QtCore.QDir.homePath(),
					[("gif", ""), ("jpg", ""), ("jpeg", ""), ("png", ""), ("bmp", ""), ("svg", "")],
					fileType=_("Images"),
					onError=onError,
				)
			#non-empty current map
			elif len(self.enterWidget.list["items"]) > 0:
				#Show warning
				warningD = QtGui.QMessageBox()
				warningD.setIcon(QtGui.QMessageBox.Warning)
				warningD.setWindowTitle(_("Warning"))
				warningD.setStandardButtons(QtGui.QMessageBox.Cancel | QtGui.QMessageBox.Ok)
				warningD.setText(_("Are you sure you want to use another map? This will remove all your places!"))
				feedback = warningD.exec_()
				if feedback != QtGui.QMessageBox.Ok:
					self.setCurrentIndex(self.prevIndex)
					return

				# Clear the entered items
				self.enterWidget.list = {
					"items": list(),
					"tests": list()
				}
				# Update the list
				self.enterWidget.currentPlaces.update()
				self.mapWidget.setMap(self.currentMap["mapPath"])
				self.enterWidget.addPlaceEdit.updateKnownPlaces(self.currentMap["knownPlaces"])
				self.prevIndex = self.currentIndex()
			#empty current map
			else:
				self.mapWidget.setMap(self.currentMap["mapPath"])
				self.enterWidget.addPlaceEdit.updateKnownPlaces(self.currentMap["knownPlaces"])
				self.prevIndex = self.currentIndex()

		@property
		def currentMap(self):
			return eval(unicode(self.itemData(self.currentIndex()).toString()))

	class EnterPlaceByName(QtGui.QLineEdit):
		"""The add-place-by-name edit"""

		def __init__(self, *args, **kwargs):
			super(EnterPlaceByName, self).__init__(*args, **kwargs)
		
		def _getNames(self, list):
			"""Gets list of names from the knownPlaces dict list"""

			return [name for item in list for name in item["names"]]

		def updateKnownPlaces(self, knownPlaces):
			"""Updates the list of names"""

			self.completer = QtGui.QCompleter(self._getNames(knownPlaces))
			self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
			self.setCompleter(self.completer)

	class EnterWidget(QtGui.QSplitter):
		"""The enter tab"""

		def __init__(self, *args, **kwargs):
			super(EnterWidget, self).__init__(*args, **kwargs)
			self.list = {
				"items": list(),
				"tests": list()
			}
			self.lesson = DummyLesson()
			
			#create the GUI
			self.addPlaceEdit = EnterPlaceByName()
			
			#left side
			leftSide = QtGui.QVBoxLayout()
			
			#left side - top
			self.mapLabel = QtGui.QLabel()
			
			#left side - middle
			self.enterMap = base._modules.default("active", type="topoMaps").getEnterMap(self)
			
			#left side - top
			self.mapChooser = EnterMapChooser(self, self.enterMap)

			chooseMap = QtGui.QHBoxLayout()
			chooseMap.addWidget(self.mapLabel)
			chooseMap.addWidget(self.mapChooser)
			
			#left side - bottom
			self.explanationLabel = QtGui.QLabel()
			self.explanationLabel.setWordWrap(True)

			#left side
			leftSide.addLayout(chooseMap)
			leftSide.addWidget(self.enterMap)
			leftSide.addWidget(self.explanationLabel)
			
			#right side
			rightSide = QtGui.QVBoxLayout()
			
			#right side - top
			self.placesLabel = QtGui.QLabel()
			self.placesLabel.setWordWrap(True)

			self.removePlaceButton = QtGui.QPushButton()
			self.removePlaceButton.clicked.connect(self.removePlace)
			
			rightTop = QtGui.QHBoxLayout()
			rightTop.addWidget(self.placesLabel)
			rightTop.addWidget(self.removePlaceButton)
			
			#right side - middle
			self.currentPlaces = EnterPlacesWidget(self)
			
			#right side - bottom
			addPlace = QtGui.QHBoxLayout()

			self.addPlaceName = QtGui.QLabel()
			self.addPlaceName.setWordWrap(True)
			self.addPlaceButton = QtGui.QPushButton()

			self.addPlaceButton.clicked.connect(lambda: self.addPlaceByName(self.addPlaceEdit.text()))
			self.addPlaceEdit.returnPressed.connect(lambda: self.addPlaceByName(self.addPlaceEdit.text()))

			addPlace.addWidget(self.addPlaceEdit)
			addPlace.addWidget(self.addPlaceButton)

			#right side
			rightSide.addLayout(rightTop)
			rightSide.addWidget(self.currentPlaces)
			rightSide.addWidget(self.addPlaceName)
			rightSide.addLayout(addPlace)

			#total layout
			leftSideWidget = QtGui.QWidget()
			leftSideWidget.setLayout(leftSide)
			rightSideWidget = QtGui.QWidget()
			rightSideWidget.setLayout(rightSide)

			self.addWidget(leftSideWidget)
			self.addWidget(rightSideWidget)

			self.retranslate()

		def retranslate(self):
			self.mapLabel.setText(_("Map:"))
			self.explanationLabel.setText(_("Add a place by doubleclicking it on the map"))
			self.placesLabel.setText(_("Places in your test"))
			self.removePlaceButton.setText(_("Remove selected place"))
			self.addPlaceName.setText(_("Add a place by name:"))
			self.addPlaceButton.setText(_("Add"))

			self.mapChooser.retranslate()

		def updateWidgets(self):
			"""Updates the widgets on the EnterWidget after the list of
			   places has changed

			"""
			self.enterMap.update()
			self.currentPlaces.update()

		def addPlace(self,place):
			"""Add a place to the list"""

			self.list["items"].append(place)
			self.lesson.changed = True
			self.updateWidgets()

		def addPlaceByName(self, name):
			"""Add a place by looking at the list of known places"""

			for placeDict in self.mapChooser.currentMap["knownPlaces"]:
				if name in placeDict["names"]:
					try:
						id = self.list["items"][-1]["id"] + 1
					except IndexError:
						id = 0
					self.list["items"].append({
						"name": unicode(name),
						"x": placeDict["x"],
						"y": placeDict["y"],
						"id": id
					})
					self.updateWidgets()
					return
			else:
				QtGui.QMessageBox(
					QtGui.QMessageBox.Warning,
					_("Place not found"),
					_("Sorry, this place is not in the list of known places. Please add it manually by doubleclicking on the right location in the map.")
				).exec_()

			self.addPlaceEdit.setText("")
			self.addPlaceEdit.setFocus()

			self.lesson.changed = True
			
		def removePlace(self):
			"""Remove a place from the list"""

			for placeItem in self.currentPlaces.selectedItems():
				for place in self.list["items"]:
					if placeItem.text() == unicode(place["name"] + " (" + unicode(place["x"]) + "," + unicode(place["y"]) + ")"):
						self.list["items"].remove(place)
				self.lesson.changed = True
			self.updateWidgets()

class TopoEntererModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TopoEntererModule, self).__init__(*args, **kwargs)
		
		global base
		base = self
		
		self._mm = moduleManager
		
		self.type = "topoEnterer"
		self.priorities = {
			"default": 640,
		}
		
		self.uses = (
			self._mm.mods(type="translator"),
			self._mm.mods(type="map"),
		)
		self.requires = (
			self._mm.mods(type="topoMaps"),
			self._mm.mods(type="fileDialogs"),
			self._mm.mods(type="ui"),
		)
		self.filesWithTranslations = ("topo.py",)
	
	def enable(self):
		global QtCore, QtGui
		try:
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return
		installQtClasses()

		self._modules = set(self._mm.mods(type="modules")).pop()
		self._widgets = set()

		#setup translation
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		self.active = True

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

		for ref in self._widgets:
			widget = ref()
			if widget is not None:
				widget.retranslate()
	
	def disable(self):
		self.active = False

		del self._modules
		del self._widgets
	
	def createTopoEnterer(self):
		ew = EnterWidget()
		self._widgets.add(weakref.ref(ew))
		return ew

def init(moduleManager):
	return TopoEntererModule(moduleManager)
