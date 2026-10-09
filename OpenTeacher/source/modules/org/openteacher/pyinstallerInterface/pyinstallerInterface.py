#! /usr/bin/env python
# -*- coding: utf-8 -*-

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

import platform
import tempfile
import atexit
import os
import shutil
import runpy
import sys

class PyinstallerInterfaceModule(object):
	"""This module freezes the current installation of OpenTeacher with
	   PyInstaller into an executable. For more on PyInstaller, see:

	   http://www.pyinstaller.org/

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(PyinstallerInterfaceModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "pyinstallerInterface"
		self.requires = (
			self._mm.mods(type="sourceSaver"),
			self._mm.mods(type="metadata")
		)
		self._tempPaths = set()
		atexit.register(self._cleanup)

	@property
	def _saveSource(self):
		return self._modules.default("active", type="sourceSaver").saveSource

	def build(self):
		path = tempfile.mkdtemp()
		self._tempPaths.add(path)
		for iconName in ["icon.ico", "icon.icns"]:
			shutil.copy(
				self._mm.resourcePath(iconName),
				os.path.join(path, iconName)
			)
		with open(os.path.join(path, "starter.py"), "w") as f:
			f.write("""
import sys
import os

if not sys.frozen:
	#import OT dependencies, so PyInstaller adds them to the build.
	#not required at runtime though, so that's why the if statement
	#above is here.
	from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork, phonon, QtScript, QtOpenGL
	import webbrowser
	import json
	import mimetypes
	import shutil
	import platform
	import atexit
	import urllib
	import urllib2
	import weakref
	import argparse
	import sqlite3
	import itertools
	import subprocess
	import zipfile
	import uuid
	import csv
	import code
	import xml.dom.minidom
	import docutils
	import chardet
	import contextlib
	import bisect
	import HTMLParser
	import traceback
	import collections
	import logging
	import runpy
	import enchant
	#windows only, so wrapped.
	try:
		import win32com
	except ImportError:
		pass
	from xml.etree import ElementTree

#filter the -psn argument passed by mac os x out.
sys.argv = [a for a in sys.argv if not a.startswith("-psn")]

sys.path.insert(0, os.path.join(os.path.dirname(sys.executable), 'source'))
sys.exit(__import__('openteacher').ModuleApplication().run())
			""")

		if platform.system() == "Darwin":
			icon = "icon.icns"
		else:
			icon = "icon.ico"

		#save so they can be restored later
		cwd = os.getcwd()
		os.chdir(path)
		argv = sys.argv
		#run pyinstaller
		pyinstallerPath = os.path.join(cwd, "pyinstaller-dev")
		sys.path.insert(0, pyinstallerPath)
		sys.argv = [
			"this is replaced by the runpy module anyway",
			"--windowed",
			"--name", str(self._metadata["name"].lower()),
			"--icon", icon,
			"starter.py",
		]
		runpy.run_path(os.path.join(pyinstallerPath, "pyinstaller.py"), run_name="__main__")
		#restore environment
		del sys.path[0]
		os.chdir(cwd)
		sys.argv = argv

		if platform.system() == "Darwin":
			resultPath = os.path.join(path, "dist", self._metadata["name"] + ".app")
		else:
			resultPath = os.path.join(path, "dist", self._metadata["name"].lower())

		#save source
		sourcePath = self._saveSource()

		#copy the source in
		if platform.system() == "Darwin":
			shutil.copytree(sourcePath, os.path.join(resultPath, "Contents/MacOS/source"))
		else:
			shutil.copytree(sourcePath, os.path.join(resultPath, "source"))

		self._copyInTesseractPortableExecutables(resultPath)

		return resultPath

	def _copyInTesseractPortableExecutables(self, resultPath):
		if platform.system() != "Windows":
			return
		#copy in the portable tesseract executables.
		tesseractDir = os.path.join(os.getcwd(), "tesseract-portable")
		for fileOrDir in os.listdir(tesseractDir):
			source = os.path.join(tesseractDir, fileOrDir)
			result = os.path.join(resultPath, fileOrDir)
			copy = shutil.copy if os.path.isfile(source) else shutil.copytree
			copy(source, result)

	def _cleanup(self):
		for path in self._tempPaths:
			shutil.rmtree(path)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._metadata = self._modules.default("active", type="metadata").metadata
		self.active = True

	def disable(self):
		self.active = False
		del self._modules
		del self._metadata

def init(moduleManager):
	return PyinstallerInterfaceModule(moduleManager)
