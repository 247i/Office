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

import sys
import os
import datetime
import subprocess
import glob

class SourceWithSetupSaverModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(SourceWithSetupSaverModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "sourceWithSetupSaver"
		self.requires = (
			self._mm.mods(type="metadata"),
			self._mm.mods(type="sourceSaver"),
			self._mm.mods(type="translator"),
		)
		self.uses = (
			self._mm.mods(type="profileDescription"),
			self._mm.mods(type="authors"),
			self._mm.mods(type="load"),
			self._mm.mods(type="dataTypeIcons"),
		)
		self.filesWithTranslations = ("manpage.templ",)

	def _moveIntoPythonPackage(self):
		os.mkdir(self._packagePath)

		#move into python package
		for item in os.listdir(self._sourcePath):
			if item != self._packageName:
				os.rename(
					os.path.join(self._sourcePath, item),
					os.path.join(self._packagePath, item)
				)

		#write __init__.py
		open(os.path.join(self._packagePath, "__init__.py"), "a").close()

	def _findPackageData(self):
		#find all files for package_data
		modulePath = os.path.join(self._packagePath, "modules")
		def getDifference(root):
			return root[len(os.path.commonprefix([self._packagePath, root])) +1:]

		for root, dirs, files in os.walk(modulePath):
			if len(files) == 0:
				continue
			root = getDifference(root)
			for file in files:
				yield os.path.join(root, file)

	def _findMimetypes(self):
		for mod in self._modules.sort("active", type="load"):
			if not hasattr(mod, "mimetype"):
				continue
			for ext in mod.loads.keys():
				yield ext, mod.name, mod.mimetype

	def _findImagePaths(self, mimetypes):
		imagePaths = {}
		for ext, name, mimetype in mimetypes:
			imagePaths[mimetype] = "linux/" + mimetype.replace("/", "-") + ".png"
		return imagePaths

	def _buildStartupScript(self):
		#bin/package
		os.mkdir(os.path.join(self._sourcePath, "bin"))
		with open(os.path.join(self._sourcePath, "bin", self._packageName), "w") as f:
			templ = pyratemp.Template(filename=self._mm.resourcePath("runner.templ"))
			#ascii since the file doesn't have a encoding directive
			f.write(templ(name=self._packageName).encode("ascii"))

	def _buildDesktopFile(self, linuxDir, mimetypes):
		#linux/package.desktop
		with open(os.path.join(linuxDir, self._packageName + ".desktop"), "w") as f:
			templ = pyratemp.Template(filename=self._mm.resourcePath("desktop.templ"))

			mimetypeList = sorted(set((m[2] for m in mimetypes)))
			f.write(templ(package=self._packageName, mimetypes=";".join(mimetypeList), **self._metadata).encode("UTF-8"))

	def _makeLinuxDir(self):
		path = os.path.join(self._sourcePath, "linux")
		os.mkdir(path)
		return path

	def _buildMenuFile(self, linuxDir):
		#linux/package.menu
		with open(os.path.join(linuxDir, self._packageName), "w") as f:
			templ = pyratemp.Template(filename=self._mm.resourcePath("menu.templ"))
			f.write(templ(package=self._packageName, **self._metadata).encode("UTF-8"))

	def _buildManPages(self, linuxDir):
		#english man page
		self._buildManPage(linuxDir, "C")
		#other languages
		translator = self._modules.default("active", type="translator")
		for file in glob.glob(self._mm.resourcePath("translations/*.mo")):
			lang = os.path.splitext(os.path.basename(file))[0]
			self._buildManPage(linuxDir, lang)

	def _buildMimetypeFile(self, linuxDir, mimetypes):
		#linux/package.xml
		with open(os.path.join(linuxDir, self._packageName + ".xml"), "w") as f:
			templ = pyratemp.Template(filename=self._mm.resourcePath("mimetypes.xml"))
			f.write(templ(data=mimetypes).encode("UTF-8"))

	def _getLogoAsQImage(self):
		return QtGui.QImage(self._metadata["iconPath"])

	def _buildPngIcon(self, linuxDir, qImage):
		#generate png icon
		image128 = qImage.scaled(128, 128, QtCore.Qt.KeepAspectRatio)
		image128.save(os.path.join(self._sourcePath, os.path.join(linuxDir, self._packageName + ".png")))

	def _buildXpmIcon(self, linuxDir, qImage):
		#generate openteacher.xpm
		image32 = qImage.scaled(32, 32, QtCore.Qt.KeepAspectRatio)
		image32.save(os.path.join(linuxDir, self._packageName + ".xpm"))

	def _buildFileIcons(self, imagePaths, qImage):
		#generate file icons

		for mimeType, imagePath in imagePaths.iteritems():
			copy = qImage.scaled(128, 128, QtCore.Qt.KeepAspectRatio)
			otherImage = self._findSubIcon({
				"application/x-openteachingwords": "words",
				"application/x-openteachingtopography": "topo",
				"application/x-openteachingmedia": "media",
			}.get(mimeType))
			if not otherImage.isNull():
				otherImage = otherImage.scaled(64, 64, QtCore.Qt.KeepAspectRatio)

			p = QtGui.QPainter(copy)
			p.drawImage(64, 64, otherImage)
			p.end()

			copy.save(os.path.join(self._sourcePath, imagePath))

	def _findSubIcon(self, type):
		try:
			return QtGui.QImage(self._modules.default("active", type="dataTypeIcons").findIcon(type))
		except (KeyError, IndexError):
			return QtGui.QImage()

	def _buildLinuxFilesCopying(self, linuxDir):
		#make a COPYING file in place for the generated files
		with open(os.path.join(linuxDir, "COPYING"), "w") as f:
			f.write("application-x-openteachingwords.png, application-x-openteachingtopo.png and application-x-openteachingmedia.png are based on the files words.png, topo.png and media.png of which the licenses are described elsewhere in this package.\n")

	def _findCExtensions(self):
		#gather extensions to compile
		for f in os.listdir(self._packagePath):
			if f.endswith(".c"):
				yield os.path.splitext(f)[0], f

	def _findPackages(self):
		yield self._packageName

		for root, dirs, files in os.walk(self._packagePath):
			if root == self._packagePath:
				continue
			relativeName = os.path.relpath(root, self._packagePath)
			if "__init__.py" in files:
				yield self._packageName + "." + relativeName.replace(os.sep, ".")

	def _buildSetupPy(self, imagePaths):
		packageData = self._findPackageData()
		exts = self._findCExtensions()
		packages = self._findPackages()

		data = self._metadata.copy()
		data.update({
			"packageName": self._packageName,
			"packages": packages,
			"package_data": packageData,
			"image_paths": repr(imagePaths.values()),
			"extensions": exts,
		})

		#setup.py
		with open(os.path.join(self._sourcePath, "setup.py"), "w") as f:
			templ = pyratemp.Template(filename=self._mm.resourcePath("setup.py.templ"))
			f.write(templ(**data).encode("UTF-8"))

	def _addSetupAndOtherFiles(self):
		#set main path variables
		self._packageName = os.path.basename(sys.argv[0])
		if self._packageName.endswith(".py"):
			self._packageName = self._packageName[:-3]
		self._packagePath = os.path.join(self._sourcePath, self._packageName)

		self._moveIntoPythonPackage()
		self._buildStartupScript()

		linuxDir = self._makeLinuxDir()
		self._buildMenuFile(linuxDir)
		self._buildLinuxFilesCopying(linuxDir)
		self._buildManPages(linuxDir)

		qIcon = self._getLogoAsQImage()
		self._buildPngIcon(linuxDir, qIcon)
		self._buildXpmIcon(linuxDir, qIcon)

		mimetypes = list(self._findMimetypes())
		self._buildMimetypeFile(linuxDir, mimetypes)
		self._buildDesktopFile(linuxDir, mimetypes)

		imagePaths = self._findImagePaths(mimetypes)
		self._buildFileIcons(imagePaths, qIcon)

		self._buildSetupPy(imagePaths)

	def saveSourceWithCExtensions(self):
		self._sourcePath = self._sourceSaver.saveSourceWithCExtensions()
		self._addSetupAndOtherFiles()
		return self._sourcePath

	def saveSource(self):
		self._sourcePath = self._sourceSaver.saveSource()
		self._addSetupAndOtherFiles()
		return self._sourcePath

	_sourceSaver = property(lambda self: self._modules.default("active", type="sourceSaver"))

	def _buildManPage(self, linuxDir, lang):
		translator = self._modules.default("active", type="translator")
		#temporarily switch the application language
		oldLanguage = translator.language
		translator.language = lang

		rstPath = os.path.join(linuxDir, "manpage.rst")
		with open(rstPath, "w") as f:
			_, ngettext = translator.gettextFunctions(self._mm.resourcePath("translations"))

			templ = pyratemp.Template(filename=self._mm.resourcePath("manpage.templ"))
			authors = self._modules.default("active", type="authors").registeredAuthors
			profileMods = self._modules.sort("active", type="profileDescription")
			args = {
				"package": self._packageName,
				"now": datetime.datetime.now(),
				#someone may appear in multiple categories, so set.
				"otAuthors": set([a[1] for a in authors]),
				"profiles": [m.desc for m in profileMods],
				"tr": _,
				#constructs a valid restructured text title.
				"titleify": lambda title: title + "\n" + (len(title) + 1) * "="
			}
			args.update(self._metadata)
			f.write(templ(**args).encode("UTF-8"))

		if lang == "C":
			manName = self._packageName + ".1"
		else:
			manName = self._packageName + "." + lang + ".1"
		subprocess.check_call(["rst2man", rstPath, os.path.join(linuxDir, manName)])
		os.remove(rstPath)

		#restore the default application language again.
		translator.language = oldLanguage

	def enable(self):
		global pyratemp
		global QtCore, QtGui
		try:
			import pyratemp
			from PyQt4 import QtCore, QtGui
		except ImportError:
			return #fail silently: stay inactive
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._metadata = self._modules.default("active", type="metadata").metadata

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self._metadata

def init(moduleManager):
	return SourceWithSetupSaverModule(moduleManager)
