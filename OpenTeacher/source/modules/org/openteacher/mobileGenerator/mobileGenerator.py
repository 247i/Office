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

import shutil
import sys
import os
import json
import urllib2
import urllib

class MobileGeneratorModule(object):
	"""Generates the HTML of OpenTeacher Mobile as a command line
	   profile. Includes an option to compress the JavaScript and CSS
	   via web services. (So in that case, a network connection is
	   required.)

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(MobileGeneratorModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "mobileGenerator"

		self.requires = [
			self._mm.mods(type="execute"),
			self._mm.mods(type="friendlyTranslationNames"),
			self._mm.mods(type="metadata"),
		]
		self._logicModTypes = [
			#wordsString
			"wordsStringComposer",

			#wordListString
			"wordListStringParser",
			"wordListStringComposer",

			#inputTypingLogic
			"inputTypingLogic",

			#else
			"javaScriptLessonType",
		]
		for type in self._logicModTypes:
			self.requires.append(self._mm.mods("javaScriptImplementation", type=type))
		self.requires = tuple(self.requires)

		self.priorities = {
			"default": -1,
			"generate-mobile": 0,
		}
		self.filesWithTranslations = ("scr/gui.js",)

	def enable(self):
		global QtCore, QtGui
		global pyratemp
		global polib
		try:
			import pyratemp
			import polib
			from PyQt4 import QtCore, QtGui
		except ImportError:
			sys.stderr.write("For this developer profile to work, you need pyratemp, polib and PyQt4 (QtCore & QtGui) to be installed.\n")
			return #remain disabled
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._modules.default(type="execute").startRunning.handle(self._run)

		self.active = True

	@property
	def languages(self, cache={}):
		if "languages" not in cache:
			cache["languages"] = self._modules.default("active", type="friendlyTranslationNames").friendlyNames
		return cache["languages"]

	def _buildSplash(self, width, height, iconPath):
		#build splash.png
		image = QtGui.QImage(width, height, QtGui.QImage.Format_ARGB32)
		painter = QtGui.QPainter(image)

		#it currently is 128x128, but this way a new future icon render/
		#new icon won't mess up this code.
		icon = QtGui.QImage(iconPath).scaled(128, 128)
		painter.setBrush(QtGui.QColor(209, 233, 250))
		painter.drawRect(0, 0, image.width(), image.height())

		#horizontally centered, vertically at 1/4
		painter.drawImage(QtCore.QPointF(
			(image.width() - icon.width()) / 2.0,
			image.height() / 4.0,
		), icon)

		#text, at 2/3
		painter.setFont(QtGui.QFont("Ubuntu", 32))
		painter.drawText(QtCore.QRectF(
			0,
			image.height() / 3.0 * 2.0, image.width(),
			image.height() / 3.0
		), QtCore.Qt.AlignHCenter, "OpenTeacher")

		painter.end()
		return image

	def _getSavePathAndMinify(self):
		#get path to save to
		try:
			path = sys.argv[1]
			minify = True if sys.argv[2] == "true" else False
		except IndexError:
			print >> sys.stderr, "Please specify a path to save the mobile site to and 'true' if you want to minify as last command line arguments. (e.g. -p generate-mobile mobile-debug false)"
			return
		#ask if overwrite
		if os.path.isdir(path):
			confirm = raw_input("There is already a directory at '%s'. Do you want to remove it and continue (y/n). " % path)
			if confirm != "y":
				return
			shutil.rmtree(path)
		return path, minify

	def _copyCss(self, path, minify):
		#copy css
		shutil.copytree(self._mm.resourcePath("css"), os.path.join(path, "css"))
		if minify:
			#minify
			for root, dirs, files in os.walk(os.path.join(path, "css")):
				for file in files:
					csspath = os.path.join(root, file)
					if not csspath.endswith(".css"):
						continue
					with open(csspath, "r") as g:
						data = g.read()
					minifiedData = urllib2.urlopen("http://reducisaurus.appspot.com/css", urllib.urlencode({
						"file": data,
					})).read()
					with open(csspath, "w") as f:
						f.write(minifiedData)

	def _generateTranslationFiles(self, path):
		#generate translation json files from po files
		translationIndex = {}

		os.mkdir(os.path.join(path, "translations"))
		for poname in os.listdir(self._mm.resourcePath("translations")):
			data = {}
			if not poname.endswith(".po"):
				continue
			popath = os.path.join(self._mm.resourcePath("translations"), poname)
			po = polib.pofile(popath)
			for entry in po.translated_entries():
				data[entry.msgid] = entry.msgstr

			lang = poname[:-len(".po")]
			jsonname = lang.replace("_", "-") + ".json"
			translationIndex[lang] = {
				"url": os.path.join("translations", jsonname),
				"name": self.languages[lang],
			}

			with open(os.path.join(path, "translations", jsonname), "w") as f:
				json.dump(data, f, separators=(",", ":"), encoding="UTF-8")

		translationIndex["en"] = {"name": self.languages["C"]}
		with open(os.path.join(path, "translations", "index.js"), "w") as f:
			data = json.dumps(translationIndex, separators=(",", ":"), encoding="UTF-8")
			f.write("var translationIndex=%s;" % data)

	def _buildLogicCode(self):
		#generate logic javascript
		logic = u""
		for type in self._logicModTypes:
			mod = self._modules.default("active", "javaScriptImplementation", type=type)
			#add to logic code var with an additional tab before every
			#line
			logic += "\n\n\n\t" + "\n".join(map(lambda s: "\t" + s, mod.code.split("\n"))).strip()
		logic = logic.strip()
		template = pyratemp.Template(filename=self._mm.resourcePath("logic.js.templ"))
		return template(code=logic)

	def _writeScripts(self, path, minify):
		logicCode = self._buildLogicCode()

		#copy scripts
		scripts = [
			#libs
			"jquery-1.8.2.js",
			"jquery.mobile-1.2.0.js",
			"taboverride.js",
			"jquery.taboverride.js",
			"jsdiff.js",
			#helper files
			"menuDialog.js",
			"copyrightInfoDialog.js",
			"optionsDialog.js",
			"enterTab.js",
			"teachTab.js",
			"practisingModeChoiceDialog.js",
			#main file
			"gui.js",
		]

		os.mkdir(os.path.join(path, "scr"))
		if minify:
			#combine scripts
			data = logicCode
			for script in scripts:
				data += unicode(open(os.path.join(self._mm.resourcePath("scr"), script)).read(), encoding="UTF-8")
			#minify
			minifiedData = urllib2.urlopen("http://closure-compiler.appspot.com/compile", urllib.urlencode({
				"compilation_level": "SIMPLE_OPTIMIZATIONS",
				"output_info": "compiled_code",
				"js_code": data.encode("UTF-8"),
			})).read()
			with open(os.path.join(path, "scr/js.js"), "w") as f:
				f.write(minifiedData)
			scripts = ["js.js"]
		else:
			#copy scripts
			for script in scripts:
				shutil.copy(
					os.path.join(self._mm.resourcePath("scr"), script),
					os.path.join(path, "scr", script)
				)
			with open(os.path.join(path, "scr", "logic.js"), "w") as f:
				f.write(logicCode)
			scripts.insert(0, "logic.js")
		return scripts

	def _writeHtml(self, path, scriptNames):
		#generate html
		headerTemplate = pyratemp.Template(filename=self._mm.resourcePath("header.html.templ"))

		template = pyratemp.Template(filename=self._mm.resourcePath("index.html.templ"))
		result = template(**{
			"scripts": scriptNames,
			"enterTabHeader": headerTemplate(titleHeader="<h1 id='enter-list-header'></h1>", tab="enter"),
			"teachTabHeader": headerTemplate(titleHeader="<h1 id='teach-me-header'></h1>", tab="teach"),
		})
		#write html to index.html
		with open(os.path.join(path, "index.html"), "w") as f:
			f.write(result)

	def _copyPhonegapConfig(self, path):
		#copy config.xml (phonegap config)
		shutil.copy(
			self._mm.resourcePath("config.xml"),
			os.path.join(path, "config.xml")
		)

	def _copyCopying(self, path):
		#copy COPYING
		shutil.copy(
			self._mm.resourcePath("COPYING.txt"),
			os.path.join(path, "COPYING.txt")
		)

	def _copyIcon(self, iconPath, path):
		#copy icon.png
		shutil.copy(
			iconPath,
			os.path.join(path, "icon.png")
		)

	def _writeSplash(self, iconPath, path):
		#splash screen
		self._buildSplash(320, 480, iconPath).save(
			os.path.join(path, "splash.png")
		)

	def _run(self):
		try:
			path, minify = self._getSavePathAndMinify()
		except TypeError:
			return

		self._copyCss(path, minify)
		self._generateTranslationFiles(path)
		scriptNames = self._writeScripts(path, minify)
		self._writeHtml(path, scriptNames)

		self._copyPhonegapConfig(path)
		self._copyCopying(path)

		#graphics
		iconPath = self._modules.default("active", type="metadata").metadata["iconPath"]
		self._copyIcon(iconPath, path)
		self._writeSplash(iconPath, path)

		print "Writing OpenTeacher mobile to '%s' is now done." % path

	def disable(self):
		self.active = False

		self._modules.default(type="execute").startRunning.unhandle(self._run)
		del self._modules

def init(moduleManager):
	return MobileGeneratorModule(moduleManager)
