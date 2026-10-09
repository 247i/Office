#! /usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright 2008-2011, Milan Boers
#    Copyright 2012, Marten de Vries
#
#    This file is part of OpenTeacher.
#
#    OpenTeacher is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    OpenTeacher is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with OpenTeacher.  If not, see <http://www.gnu.org/licenses/>.


import fnmatch

class MediaTypeModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(MediaTypeModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager
		
		self.phononControls = False
		
		self.type = "mediaType"
		self.remoteNames = ["Dailymotion"]
		self.priorities = {
			"default": 300,
		}

	def enable(self):
		global QtCore
		try:
			from PyQt4 import QtCore
		except ImportError:
			return
		self.active = True

	def disable(self):
		self.active = False
	
	def supports(self, path):
		if fnmatch.fnmatch(str(path), "*dailymotion.com/video/*"):
			return True
		else:
			return False
	
	def path(self, path, autoplay):
		# Dailymotion URL
		path = path.split("dailymotion.com/video/")[1]
		path = path.split("_")[0]
		path = "http://www.dailymotion.com/embed/video/" + path
		return path
	
	def showMedia(self, path, mediaDisplay, autoplay):
		if not mediaDisplay.noPhonon:
			# Stop any media playing
			mediaDisplay.videoPlayer.stop()
		# Set widget to web viewer
		mediaDisplay.setCurrentWidget(mediaDisplay.webviewer)
		# Set the URL
		mediaDisplay.webviewer.setUrl(QtCore.QUrl(path))

def init(moduleManager):
	return MediaTypeModule(moduleManager)
