#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2012, Milan Boers
#	Copyright 2012-2013, Marten de Vries
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

import contextlib

def installQtClasses():
	global EnterMap, EnterMapScene, Map, TeachPictureMap, TeachPictureScene, TeachPlaceOnMap

	class Map(QtGui.QGraphicsView):
		"""Abstract class for the map widgets"""

		def __init__(self,*args, **kwargs):
			super(Map, self).__init__(*args, **kwargs)
			
			module = base._modules.default(type="settings")
			if base._openGlSetting["value"]:
				self.setViewport(QtOpenGL.QGLWidget())
		
		def setMap(self, map):
			self._setPicture(map)
		
		def _setPicture(self,picture):
			# Create a new scene
			self.scene = QtGui.QGraphicsScene()
			# Set the pixmap of the scene
			self.pixmap = QtGui.QPixmap(picture)
			self.scene.addPixmap(self.pixmap)
			# Set the scene
			self.setScene(self.scene)
		
		def wheelEvent(self,wheelevent):
			# Scrolling makes it zoom
			if wheelevent.delta() > 0:
				self.scale(1.1,1.1)
			else:
				self.scale(0.9,0.9)

	class TeachPlaceOnMap(QtGui.QGraphicsRectItem):
		"""A place on the map for the inverted order"""

		def __init__(self, place, *args, **kwargs):
			super(TeachPlaceOnMap, self).__init__(*args, **kwargs)
			
			width = 10
			height = 10
			
			self.setRect(place["x"] - width / 2, place["y"] - height / 2, width, height)
			self.setBrush(QtGui.QBrush(QtGui.QColor("red")))
			
			self.place = place

	class EnterMapScene(QtGui.QGraphicsScene):
		"""The graphics scene of the map where you enter"""

		def __init__(self, enterMap, *args, **kwargs):
			super(EnterMapScene, self).__init__(*args, **kwargs)
			
			self.enterMap = enterMap
		
		def mouseDoubleClickEvent(self,gsme):
			# Get coordinates
			x = gsme.lastScenePos().x()
			y = gsme.lastScenePos().y()
			# If its in the map
			if x > 0 and y > 0:
				# Ask for the name
				name = QtGui.QInputDialog.getText(self.enterMap, _("Name for this place"), _("What's this place's name?"))
				if unicode(name[1]) and unicode(name[0]).strip() != u"":
					# Make the place
					place = {
						"id": int(),
						"name": unicode(name[0]),
						"x": int(x),
						"y": int(y)
					}
					# Set id
					try:
						place["id"] = self.enterMap.enterWidget.list["items"][-1]["id"] + 1
					except IndexError:
						place["id"] = 0
					# And add the place
					self.enterMap.enterWidget.addPlace(place)

	class EnterMap(Map):
		"""The map on the enter tab"""

		def __init__(self, enterWidget, *args, **kwargs):
			super(EnterMap, self).__init__(*args, **kwargs)
			# Make it scrollable and draggable
			self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
			
			self.enterWidget = enterWidget
			
			self.placesList = []
			self.placesGroup = QtGui.QGraphicsItemGroup()
		
		def _setPicture(self, filepath):
			"""Override base class _setPicture with one that uses an
			   EnterMapScene instead of QGraphicsScene

			"""
			# Create a new scene
			self.scene = EnterMapScene(self)
			# Set the pixmap of the scene
			self.pixmap = QtGui.QPixmap(filepath)
			self.scene.addPixmap(self.pixmap)
			# Set the scene
			self.setScene(self.scene)
		
		def update(self):
			# Remove previous items
			for item in self.placesList:
				with contextlib.ignored(RuntimeError):
					#RuntimeError: Object already removed
					self.scene.removeItem(item)
			
			# Remove all previous items
			self.placesList = []
			
			# Add all the places
			for place in self.enterWidget.list["items"]:
				# Make the little rectangle
				rect = QtGui.QGraphicsRectItem(place["x"],place["y"],6,6)
				rect.setBrush(QtGui.QBrush(QtGui.QColor("red")))
				# Place the rectangle in the list of items
				self.placesList.append(rect)
				
				# Make the shadow of the text
				shadow = QtGui.QGraphicsTextItem(place["name"])
				shadow.setFont(QtGui.QFont("sans-serif",15,75))
				shadow.setPos(place["x"]+2,place["y"]+2)
				shadow.setDefaultTextColor(QtGui.QColor("black"))
				shadow.setOpacity(0.5)
				# Place the shadow in the list of items
				self.placesList.append(shadow)
				
				item = QtGui.QGraphicsTextItem(place["name"])
				item.setFont(QtGui.QFont("sans-serif",15,75))
				item.setPos(place["x"],place["y"])
				item.setDefaultTextColor(QtGui.QColor("red"))
				# Place the text in the list of items
				self.placesList.append(item)
			
			# Place the list of items on the map
			self.placesGroup = self.scene.createItemGroup(self.placesList)
		
		def getScreenshot(self):
			image = QtGui.QImage(self.scene.width(), self.scene.height(), QtGui.QImage.Format_RGB32)
			image.fill(QtGui.QColor(QtCore.Qt.white).rgb())
			painter = QtGui.QPainter(image)
			self.scene.render(painter)
			painter.end()
			return image

	class TeachPictureScene(QtGui.QGraphicsScene):
		"""Scene for the TeachPictureMap"""

		def __init__(self, pictureMap, *args, **kwargs):
			super(TeachPictureScene, self).__init__(*args, **kwargs)
			
			self.pictureMap = pictureMap
		
		def mouseReleaseEvent(self, event):
			# Clicked a place
			clickedObject = self.itemAt(event.lastScenePos().x(), event.lastScenePos().y())
			if clickedObject.__class__ == TeachPlaceOnMap:
				self.pictureMap.teachWidget.lesson.checkAnswer(clickedObject.place)

	class TeachPictureMap(Map):
		"""The map on the teach tab"""

		def __init__(self, teachWidget, *args, **kwargs):
			super(TeachPictureMap, self).__init__(*args, **kwargs)
			
			self.teachWidget = teachWidget
			
			# Not interactive
			self.interactive = False
			# Make sure everything is redrawn every time
			self.setViewportUpdateMode(0)
		
		def setArrow(self, x, y):
			"""Sets the arrow on the map to the right position"""

			self.centerOn(x-15,y-50)
			self.crosshair.setPos(x-15,y-50)
		
		def removeArrow(self):
			"""Removes the arrow"""

			self.scene.removeItem(self.crosshair)

		def _setPicture(self,picture):
			"""Overriding the base class _setPicture method with one using the TeachPictureScene"""

			# Create a new scene
			self.scene = TeachPictureScene(self)
			# Set the pixmap of the scene
			self.pixmap = QtGui.QPixmap(picture)
			self.scene.addPixmap(self.pixmap)
			# Set the scene
			self.setScene(self.scene)
		
		def showPlaceRects(self):
			"""Shows all the places without names"""

			placesList = []
			
			for place in self.teachWidget.places["items"]:
				# Make the little rectangle
				rect = TeachPlaceOnMap(place)
				# Place the rectangle in the list of items
				placesList.append(rect)
			
			self.placesGroup = self.scene.createItemGroup(placesList)
		
		def hidePlaceRects(self):
			with contextlib.ignored(AttributeError):
				for item in self.placesList:
					self.removeItem(item)
		
		def setInteractive(self, val):
			if val:
				self.showPlaceRects()
				# Interactive
				self.interactive = True
				# Scrollbars
				self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
				self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
				self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
			else:
				self.hidePlaceRects()
				# Not interactive
				self.interactive = False
				# No scrollbars
				self.setDragMode(QtGui.QGraphicsView.NoDrag)
				self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
				self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
				# Arrow
				crosshairPixmap = QtGui.QPixmap(base._mm.resourcePath("resources/crosshair.png"))
				self.crosshair = QtGui.QGraphicsPixmapItem(crosshairPixmap)
				
				self.scene.addItem(self.crosshair)

class TopoMapsModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TopoMapsModule, self).__init__(*args, **kwargs)
		
		global base
		base = self
		
		self._mm = moduleManager
		
		self.type = "topoMaps"
		self.priorities = {
			"default": 416,
		}

		self.requires = (
			self._mm.mods(type="ui"),
		)
		
		self.uses = (
			self._mm.mods(type="translator"),
			self._mm.mods(type="settings"),
		)
		self.filesWithTranslations = ("topoMaps.py",)
	
	def enable(self):
		global QtCore, QtGui, QtOpenGL
		try:
			from PyQt4 import QtCore, QtGui, QtOpenGL
		except ImportError:
			return
		installQtClasses()

		self._modules = set(self._mm.mods(type="modules")).pop()

		# Add settings
		try:
			self._settings = self._modules.default(type="settings")
		except IndexError, e:
			self._openGlSetting = {"value": False}
		else:
			self._openGlSetting = self._settings.registerSetting(**{
				"internal_name": "org.openteacher.lessons.topo.opengl",
				"type": "boolean",
				"defaultValue": False,
				"advanced": True,
			})

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
		#install _ and ngettext
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

		self._openGlSetting.update({
			"name": _("OpenGL rendering"),
			"category": _("Lesson"),
			"subcategory": _("Topography"),
		})

	def disable(self):
		self.active = False

		del self._modules
		if hasattr(self, "_settings"):
			del self._settings
		del self._openGlSetting

	def getEnterMap(self, enterWidget):
		return EnterMap(enterWidget)
	
	def getTeachMap(self, teachWidget):
		return TeachPictureMap(teachWidget)

def init(moduleManager):
	return TopoMapsModule(moduleManager)
