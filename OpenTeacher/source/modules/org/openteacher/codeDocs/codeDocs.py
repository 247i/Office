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

# cherrypy, pygments, pyratemp & docutils.core are imported in enable()

import inspect
import os
import types
import mimetypes
import sys
import re
import tempfile

import __builtin__
BUILTIN_TYPES = [t for t in __builtin__.__dict__.itervalues() if isinstance(t, type)]

class ModulesHandler(object):
	def __init__(self, moduleManager, templates, buildModuleGraph, devDocsBaseDir, hue, *args, **kwargs):
		super(ModulesHandler, self).__init__(*args, **kwargs)

		self._mm = moduleManager
		self._mods = {}

		for mod in self._mm.mods:
			#get the path of the module
			path = os.path.dirname(mod.__class__.__file__)
			#make sure the path is relative to the modules root for easier recognition
			self._mods[self._pathToUrl(path)] = mod
		self._templates = templates
		self._buildModuleGraph = buildModuleGraph
		self._devDocsBaseDir = devDocsBaseDir
		self._hue = hue

		#use last formatter if it exists
		self._formatter = pygments.formatters.HtmlFormatter(**{
			"linenos": "table",
			"anchorlinenos": True,
			"lineanchors": self._pathToUrl(path),
		})

	def _pathToUrl(self, path):
		path = os.path.abspath(path)

		sourceBase = os.path.abspath(os.path.dirname(__file__))
		while not sourceBase.endswith("modules"):
			sourceBase = os.path.normpath(os.path.join(sourceBase, ".."))
		sourceBase = os.path.normpath(os.path.join(sourceBase, ".."))		

		if sourceBase != os.curdir:
			common = os.path.commonprefix([sourceBase, path])
			url = path[len(common) +1:]
			return url
		return path

	def _format(self, text):
		if text:
			return docutils.core.publish_parts(
				text.replace("\t", "").replace("   ", ""),
				writer_name="html",
				settings_overrides={"report_level": 5}
			)["html_body"]
		else:
			return text

	def module_graph_svg(self):
		cherrypy.response.headers["Content-Type"] = "image/svg+xml"
		try:
			fd, path = tempfile.mkstemp(".svg")
			os.close(fd)
			self._buildModuleGraph(path)
			with open(path) as f:
				return f.read()
		finally:
			os.remove(path)
	module_graph_svg.exposed = True

	def style_css(self):
		t = pyratemp.Template(filename=self._templates["style"])
		cherrypy.response.headers["Content-Type"] = "text/css"
		return t(**{
			"headerBackgroundColor": QtGui.QColor.fromHsv(self._hue, 41, 250).name(),
			"bodyBackgroundColor": QtGui.QColor.fromHsv(self._hue, 7, 253, 255).name(),
			"footerBackgroundColor": QtGui.QColor.fromHsv(self._hue, 30, 228).name(),
			"pygmentsStyle": self._formatter.get_style_defs('.highlight'),
		})

	style_css.exposed = True

	def resources(self, *args):
		path = "/".join(args)
		if path == "logo":
			path = self._templates["logo"]
		else:
			#construct the path
			path = os.path.normpath(
				os.path.join(self._templates["resources"], path)
			)
			#check if the path is valid (i.e. is in the resources
			#directory.)
			if not path.startswith(os.path.normpath(self._templates["resources"])):
				#404
				raise cherrypy.HTTPError(404)
		mimetype = mimetypes.guess_type(path, strict=False)[0]
		if mimetype:
			cherrypy.response.headers["Content-Type"] = mimetype
		try:
			return open(path).read()
		except IOError:
			#404
			raise cherrypy.HTTPError(404)
	resources.exposed = True

	def index(self):
		t = pyratemp.Template(filename=self._templates["modules"])
		return t(**{
			"mods": sorted(self._mods.keys())
		})
	index.exposed = True

	def priorities_html(self):
		profileMods = self._mm.mods("active", type="profileDescription")
		profiles = (profileMod.desc["name"] for profileMod in profileMods)
		profiles = ["default"] + sorted(profiles)

		mods = {}
		for mod in self._mm.mods("priorities"):
			mods[self._pathToUrl(os.path.dirname(mod.__class__.__file__))] = mod
		mods = sorted(mods.iteritems())

		t = pyratemp.Template(filename=self._templates["priorities"])
		return t(**{
			"mods": mods,
			"profiles": profiles,
		})
	priorities_html.exposed = True

	def _fixmePaths(self):
		#get base directory
		def upOne(p):
			return os.path.normpath(os.path.join(p, ".."))

		basePath = os.path.abspath(os.path.dirname(__file__))
		while not basePath.endswith("modules"):
			basePath = upOne(basePath)

		#get all paths
		paths = (
			os.path.join(root, file)
			for root, dirs, files in sorted(os.walk(basePath))
			for file in files
		)
		#and filter them
		return (
			p for p in paths
			if not (
				os.path.splitext(p)[1] in (".png", ".gif", ".bmp", ".ico", ".pyc", ".mo", ".psd", ".gpg", ".pem", ".sqlite3", ".rtf", ".po", ".pot")
				or p.endswith("~")
				or "jquery" in p
				or "admin_files" in p
				or "codeDocs" in p
				or "ircBot" in p
				or "words.txt" in p
				or "dev_tools.rst" in p
			)
		)

	def fixmes_html(self):
		rePattern = re.compile("fixme|todo", re.IGNORECASE)
		fixmes = []
		for fpath in self._fixmePaths():
			with open(fpath, "r") as f:
				lines = f.readlines()

			lines = [
				unicode(line, encoding="UTF-8", errors="replace")
				for line in lines
			]
			for i, line in enumerate(lines):
				match = rePattern.search(line)
				if not match:
					continue
				if i - 2 > 0:
					startNumber = i - 2
				else:
					startNumber = 0
				try:
					lines[i + 5]
				except IndexError:
					endNumber = len(lines)
				else:
					endNumber = i + 5
				relevantLines = lines[startNumber:endNumber]
				relevantCode = u"".join(relevantLines)

				try:
					lexer = pygments.lexers.get_lexer_for_filename(fpath)
				except pygments.util.ClassNotFound:
					lexer = pygments.lexers.TextLexer()
				formatter = pygments.formatters.HtmlFormatter()
				fixmes.append({
					"path": self._pathToUrl(unicode(fpath, sys.getfilesystemencoding())),
					"line_number": i + 1,
					"relevant_code": pygments.highlight(relevantCode, lexer, formatter),
				})

		t = pyratemp.Template(filename=self._templates["fixmes"])
		return t(**{
			"fixmes": fixmes,
		})
	fixmes_html.exposed = True

	def _isFunction(self, mod, x):
		try:
			obj = getattr(mod.__class__, x)
		except AttributeError:
			obj = getattr(mod, x)
		return isinstance(obj, types.MethodType)

	def _modsForRequirement(self, selectors):
		for selector in selectors:
			selectorResults = set()
			requiredMods = set(selector)
			for requiredMod in requiredMods:
				selectorResults.add((
					self._pathToUrl(os.path.dirname(requiredMod.__class__.__file__)),
					requiredMod.__class__.__name__
				))
			yield selectorResults

	def _renderRstPage(self, rstPath):
		with open(rstPath) as f:
			parts = docutils.core.publish_parts(
				f.read(),
				writer_name="html",
				settings_overrides={
					"report_level": 5,
					"initial_header_level": 2
				}
			)

		t = pyratemp.Template(filename=self._templates["dev_docs"])
		return t(**{
			"page": parts["fragment"],
			"title": parts["title"]
		})

	def dev_docs(self, *args):
		if not args:
			args = ["index.rst"]
		requestedPath = "/".join(args)
		requestedPath = os.path.normpath(requestedPath)
		if os.path.isabs(requestedPath) or requestedPath.startswith(os.pardir):
			#invalid path
			raise cherrypy.HTTPError(404)
		path = os.path.join(self._devDocsBaseDir, requestedPath)

		if not os.path.exists(path):
			raise cherrypy.HTTPError(404)

		if path.endswith(".rst"):
			return self._renderRstPage(path)
		else:
			return cherrypy.lib.static.serve_file(os.path.abspath(path))

		#if all else fails
		raise cherrypy.HTTPError(404)

	dev_docs.exposed = True

	def _propertyDocs(self, property):
		#first try if the class attribute has a doc string. This
		#catches e.g. @property-decorated function docstrings.
		try:
			return self._format(getattr(mod.__class__, property).__doc__)
		except:
			#all errors aren't important enough to fail for
			pass
		#then try to get the docstring of the object itself.
		try:
			propertyObj = getattr(mod, property)
		except:
			#errors aren't important enough to fail for.
			return
		if propertyObj.__class__ != type and propertyObj.__class__ in BUILTIN_TYPES:
			#docstring is uninteresting
			return
		try:
			propertyDocs[property] = self._format(propertyObj.__doc__)
		except AttributeError:
			#no docstring.
			return

	def _fileDataForMod(self, mod):
		for root, dirs, files in os.walk(os.path.dirname(mod.__class__.__file__)):
			for f in sorted(files):
				ext = os.path.splitext(f)[1]
				if ext not in [".html", ".py", ".js", ".css", ".po", ".pot"]:
					continue
				if "jquery" in f.lower():
					continue
				path = os.path.join(root, f)
				if os.path.getsize(path) > 1.0/4.0 * 1024 * 1024:
					#> 0.25MB
					continue

				code = open(path).read()

				lexer = pygments.lexers.get_lexer_for_filename(path)
				source = pygments.highlight(code, lexer, self._formatter)
				commonLength = len(os.path.commonprefix([
					path,
					os.path.dirname(mod.__class__.__file__)
				]))
				yield path[commonLength:], source

	def modules(self, *args):
		args = list(args)
		args[-1] = args[-1][:-len(".html")]
		try:
			mod = self._mods["modules/" + "/".join(args)]
		except KeyError:
			raise cherrypy.HTTPError(404)

		attrs = set(dir(mod))
		methods = set(func for func in attrs if self._isFunction(mod, func))
		properties = attrs - methods

		isPublic = lambda x: not x.startswith("_")
		methods = set(m for m in methods if isPublic(m))

		methodDocs = {}
		methodArgs = {}
		for method in methods:
			methodObj = getattr(mod, method)
			methodDocs[method] = self._format(methodObj.__doc__)
			methodArgs[method] = self._constructSignature(inspect.getargspec(methodObj))

		properties = set(p for p in properties if isPublic(p))

		#remove special properties
		properties -= set(["type", "uses", "requires", "priorities", "filesWithTranslations"])
		propertyDocs = dict(
			(p, self._propertyDocs(p))
			for p in properties
			if self._propertyDocs(p) is not None
		)

		#uses
		uses = self._modsForRequirement(getattr(mod, "uses", []))

		#requires
		requires = self._modsForRequirement(getattr(mod, "requires", []))

		fileData = self._fileDataForMod(mod)

		t = pyratemp.Template(filename=self._templates["module"])
		return t(**{
			"name": mod.__class__.__name__,
			"moddoc": self._format(mod.__doc__),
			"type": getattr(mod, "type", None),
			"uses": uses,
			"requires": requires,
			"methods": sorted(methods),
			"methodDocs": methodDocs,
			"methodArgs": methodArgs,
			"properties": sorted(properties),
			"propertyDocs": propertyDocs,
			"files": fileData,
		})
	modules.exposed = True

	def _constructSignature(self, data):
		try:
			args = reversed(data.args)
		except TypeError:
			args = []
		try:
			defaults = list(reversed(data.defaults))
		except TypeError:
			defaults = []

		result = []
		for i, arg in enumerate(args):
			try:
				result.insert(0, "%s=%s" % (arg, defaults[i]))
			except IndexError:
				result.insert(0, arg)
		if data.varargs:
			result.append("*" + data.varargs)
		if data.keywords:
			result.append("**" + data.keywords)
		return result

class CodeDocumentationModule(object):
	"""This module generates code documentation for OpenTeacher
	   automatically based on the actual code. When the server crashes,
	   you can see the error message by adding the 'debug' parameter.
	   (i.e. ``python openteacher.py -p code-documentation debug``).

	   This module generates the following documentation:

	   - Overview of all modules
	   - Overview of the methods and properties of the module classes,
	     including docstrings.
	   - Source listing (including syntax highlighting)
	   - The module map (showing all dependencies between modules)
	   - FIXMEs/TODOs overview

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(CodeDocumentationModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "codeDocumentationShower"

		self.requires = (
			self._mm.mods(type="metadata"),
			self._mm.mods(type="execute"),
			self._mm.mods(type="moduleGraphBuilder"),
			self._mm.mods(type="devDocs"),
			self._mm.mods(type="qtApp"),
		)
		self.uses = (
			self._mm.mods(type="profileDescription"),
		)
		self.priorities = {
			"code-documentation": 0,
			"default": -1,
		}

	def showDocumentation(self):
		metadata = self._modules.default("active", type="metadata").metadata

		buildModuleGraph = self._modules.default("active", type="moduleGraphBuilder").buildModuleGraph
		devDocsBaseDir = self._modules.default("active", type="devDocs").developerDocumentationBaseDirectory
		templates = {
			"modules": self._mm.resourcePath("templ/modules.html"),
			"priorities": self._mm.resourcePath("templ/priorities.html"),
			"fixmes": self._mm.resourcePath("templ/fixmes.html"),
			"module": self._mm.resourcePath("templ/module.html"),
			"dev_docs": self._mm.resourcePath("templ/dev_docs.html"),
			"resources": self._mm.resourcePath("resources"),
			"style": self._mm.resourcePath("templ/style.css"),
			"logo": metadata["iconPath"],
		}
		hue = metadata["mainColorHue"]
		root = ModulesHandler(self._mm, templates, buildModuleGraph, devDocsBaseDir, hue)

		cherrypy.config.update({
			"server.socket_host": "0.0.0.0",
			"environment": "production",
		})
		app = cherrypy.tree.mount(root)
		cherrypy.engine.start()
		print "Serving at http://localhost:8080/"
		print "Type 'quit' and press enter to stop the server"
		while True:
			try:
				if raw_input("> ").lower() in ("q", "quit"):
					break
			except KeyboardInterrupt:
				break
		cherrypy.engine.exit()

	def enable(self):
		global cherrypy, pygments, pyratemp, docutils, QtGui
		try:
			import cherrypy
			import pygments
			import pygments.lexers
			import pygments.formatters
			import pygments.util
			import pyratemp
			import docutils.core
			from PyQt4 import QtGui
		except ImportError:
			sys.stderr.write("For this developer module to work, you need to have cherrypy, pygments, pyratemp and docutils installed. And indirectly, pygraphviz.\n")
			return #leave disabled

		#enable syntax highlighting
		self._mm.import_("rst-directive")

		self._modules = set(self._mm.mods(type="modules")).pop()
		self._modules.default(type="execute").startRunning.handle(self.showDocumentation)

		self.active = True

	def disable(self):
		self.active = False

		global pyratemp
		del pyratemp
		del self._modules

def init(moduleManager):
	return CodeDocumentationModule(moduleManager)
