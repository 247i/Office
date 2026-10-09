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

import argparse
import sys
import glob
import os

class DummyLesson(object):
	def __init__(self, lessonDict, *args, **kwargs):
		super(DummyLesson, self).__init__(*args, **kwargs)

		self.list = lessonDict["list"]
		self.resources = lessonDict["resources"]

def getEnterEdit(Event):
	class EnterEdit(urwid.Edit):
		def __init__(self, *args, **kwargs):
			super(EnterEdit, self).__init__(*args, **kwargs)

			self.enterPressed = Event()

		def keypress(self, size, key):
			if key == "enter":
				self.enterPressed.send()
			else:
				return super(EnterEdit, self).keypress(size, key)

	return EnterEdit

class PractisingInterface(object):
	"""A command line interface for practising words, using the urwid
	   toolkit.

	"""
	def __init__(self, createController, lessonType, *args, **kwargs):
		super(PractisingInterface, self).__init__(*args, **kwargs)

		self._controller = createController()
		self._controller.lessonType = lessonType
		self._connectToEvents()
		self._setupUi()

	def _connectToEvents(self):
		self._controller.clearInput.handle(self._clearInput)
		self._controller.showCorrection.handle(self._showCorrection)
		self._controller.hideCorrection.handle(self._hideCorrection)

	def _setupUi(self):
		#setup main UI
		self._txt = urwid.Text(u"")
		self._edit = EnterEdit("ANSWER: ")
		self._edit.enterPressed.handle(self._onCheck)
		urwid.connect_signal(self._edit, "change", lambda x, y: self._controller.userIsTyping)

		checkButton = urwid.Button("Check", lambda button: self._onCheck())
		skipButton = urwid.Button("Skip", lambda button: self._controller.skipTriggered())

		divider = urwid.Divider()
		quitButton = urwid.Button("Quit", lambda button: self.quit())

		widgets = [self._txt, self._edit, divider, checkButton, skipButton, divider, quitButton]
		listBox = urwid.ListBox(widgets)
		adapter = urwid.BoxAdapter(listBox, len(widgets))
		self._mainFiller = urwid.Filler(adapter, "middle")

		#setup correction dialog
		self._correctionTxt = urwid.Text(u"")
		self._correctionFiller = urwid.Filler(self._correctionTxt, "middle")

		self._loop = urwid.MainLoop(self._mainFiller)

	def _clearInput(self):
		self._edit.edit_text = ""

	def _showCorrection(self, correctAnswer):
		self._loop.widget = self._correctionFiller
		self._correctionTxt.set_text(u"WRONG ANSWER. IT SHOULD HAVE BEEN: %s" % correctAnswer)
		self._loop.set_alarm_in(3, lambda x, y:self._controller.correctionShowingDone())

	def _hideCorrection(self):
		self._loop.widget = self._mainFiller

	def run(self):
		self._controller.lessonType.start()
		self._loop.run()

	def _onCheck(self):
		self._controller.checkTriggered(self._edit.edit_text)

	def quit(self):
		raise urwid.ExitMainLoop()

	def setNextItem(self, question):
		self._txt.set_text("QUESTION: %s" % question)

class CommandLineInterfaceModule(object):
	"""This module provides a command line interface to a lot of
	   OpenTeacher's functions, including list management, list
	   practising, OCR, and viewing some program metadata.

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(CommandLineInterfaceModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "cli"
		self.requires = (
			self._mm.mods(type="execute"),
			self._mm.mods(type="metadata"),
			self._mm.mods(type="wordListStringComposer"),
			self._mm.mods(type="wordListStringParser"),
			self._mm.mods(type="lessonType"),
			self._mm.mods(type="event"),
			self._mm.mods(type="inputTypingLogic"),
			self._mm.mods(type="wordsStringComposer"),
			self._mm.mods(type="authors"),
			self._mm.mods(type="loader"),
		)
		self.uses = (
			self._mm.mods(type="save"),
			self._mm.mods(type="reverser"),
			self._mm.mods(type="ocrWordListLoader"),
		)
		self.priorities = {
			"cli": 0,
			"default": 960,
		}

	def _saveExts(self):
		yielded = set()
		for mod in self._modules.sort("active", type="save"):
			for exts in sorted(mod.saves.itervalues()):
				for ext in sorted(exts):
					if ext not in yielded:
						yielded.add(ext)
						yield ext

	def _load(self, path):
		return self._modules.default("active", type="loader").loadToLesson(path)

	def _expandPaths(self, paths):
		newPaths = []
		for selector in paths:
			newPaths.extend(glob.iglob(selector))
		return newPaths

	def _reverseList(self, args):
		type, lesson = self._load(args["input-file"])
		if not lesson:
			print >> sys.stderr, "Couldn't load file '%s', not reversing." % args["input-file"]
			return

		try:
			self._modules.default("active", type="reverser", dataType=type).reverse(lesson["list"])
		except IndexError:
			print >> sys.stderr, "Couldn't reverse the file '%s'." % args["input-file"]
			return

		self._save(type, lesson, args["output-file"])

	def _merge(self, args):
		baseType, baseLesson = self._load(args["base-file"])
		if not baseLesson:
			print >> sys.stderr, "Couldn't load the base file ('%s'). Not doing the merge." % args["base-file"]
			return
		try:
			merge = self._modules.default("active", type="merger", dataType=baseType).merge
		except IndexError:
			print >> sys.stderr, "Can't merge this type of files. Stopping."
			return

		for inputFile in args["other-files"]:
			type, lesson = self._load(inputFile)
			if not lesson:
				print >> sys.stderr, "Couldn't load the file '%s'. Not doing the merge." % inputFile
				return
			if type != baseType:
				print >> sys.stderr, "The type of the base file ('%s') and the input file '%s' ('%s') aren't equal. Not doing the merge." % (baseType, inputFile, type)
				return
			baseLesson = merge(baseLesson, lesson)

		self._save(baseType, baseLesson, args["output-file"])

	def _convert(self, args):
		inputPaths = self._expandPaths(args["input-files"])
		outputFormat = args["output_format"]

		for inputPath in inputPaths:
			#loading
			type, lesson = self._load(inputPath)
			if not lesson:
				print >> sys.stderr, "Couldn't load file '%s', not converting." % inputPath
				#next file
				continue

			done = False
			outputPath = os.path.splitext(inputPath)[0] + "." + outputFormat
			if os.path.exists(outputPath):
				print >> sys.stderr, "The file '{outfile}' already exists, so '{infile}' can't be converted.".format(outfile=outputPath, infile=inputPath)
				#next file
				continue

			for mod in self._modules.sort("active", type="save"):
				for modType, exts in mod.saves.iteritems():
					if modType == type and outputFormat in exts:
						mod.save(type, DummyLesson(lesson), outputPath)
						done = True
						break
				if done:
					break
			else:
				print >> sys.stderr, "Couldn't save file '{infile}' in the '{format}' format, not converting.".format(infile=inputPath, format=outputFormat)
				#next file. Not strictly necessary, but just in case more code's added later...
				continue
			print "Converted file '{infile}' to '{outfile}'.".format(infile=inputPath, outfile=outputPath)
		print "Done."

	def _viewWordList(self, args):
		inputPaths = self._expandPaths(args["input-files"])
		for inputPath in inputPaths:
			type, lesson = self._load(inputPath)
			if type != "words":
				print >> sys.stderr, "File '%s' isn't a word list." % inputPath
				continue
			if not lesson:
				print >> sys.stderr, "Couldn't load file %s, not showing." % inputPath
				continue
			#lambda's for lazy loading. Handy for the compose case which
			#is a lot more likely to crash than the others + is
			#relatively slow. JS implementation only currently...
			print {
				"title": lambda: lesson["list"]["title"],
				"question-lang": lambda: lesson["list"]["questionLanguage"],
				"answer-lang": lambda: lesson["list"]["answerLanguage"],
				"list": lambda: self._composeWordList(lesson),
			}[args["part"]]()

	def _newWordList(self, args):
		if args["input-file"] == "-":
			inputFile = sys.stdin
		else:
			inputFile = open(args["input-file"], "r")
		data = unicode(inputFile.read(), sys.stdin.encoding or "UTF-8")

		lesson = self._parseWordList(data)

		if args["title"]:
			lesson["list"]["title"] = unicode(args["title"], encoding=sys.stdin.encoding or "UTF-8")
		if args["question_lang"]:
			lesson["list"]["questionLanguage"] = unicode(args["question_lang"], encoding=sys.stdin.encoding or "UTF-8")
		if args["answer_lang"]:
			lesson["list"]["answerLanguage"] = unicode(args["answer_lang"], encoding=sys.stdin.encoding or "UTF-8")

		self._save("words", lesson, args["output-file"])

	def _ocrWordList(self, args):
		loadWordList = self._modules.default("active", type="ocrWordListLoader").loadWordList
		lesson = loadWordList(args["input-file"])
		self._save("words", lesson, args["output-file"])

	def _save(self, type, lesson, path):
		#also strip the dot.
		ext = os.path.splitext(path)[1][1:]

		if os.path.isfile(path):
			print >> sys.stderr, "Output file already exists. Not saving."
			return

		for mod in self._modules.sort("active", type="save"):
			if not ext in mod.saves.get(type, []):
				continue
			mod.save("words", DummyLesson(lesson), path)
			print "Done."
			break
		else:
			print >> sys.stderr, "Couldn't save your input to '%s'." % path

	@property
	def _lessonTypes(self):
		return [
			mod.name.encode(sys.stdin.encoding or "UTF-8")
			for mod in self._modules.sort("active", type="lessonType")
		]

	def _authors(self, args):
		authors = self._modules.default("active", type="authors").registeredAuthors
		if args["category"] is not None:
			authors = filter(lambda (c, n): c == args["category"], authors)
		output = []
		lastCategory = None
		for category, name in sorted(authors):
			if lastCategory is not None and lastCategory != category:
				output.append("")
			lastCategory = category
			output.append("%s: %s" % (name, category))
		print "\n".join(output)

	def _practiseWordList(self, args):
		inputFile = args["file"]

		type, lesson = self._load(inputFile)
		if type != "words":
			print >> sys.stderr, "File '%s' isn't a word file" % inputFile
		if not lesson:
			print >> sys.stderr, "The '%s' file can't be loaded." % inputFile

		lessonTypeMod = self._modules.default("active", type="lessonType", name=args["lesson_type"])
		lessonType = lessonTypeMod.createLessonType(lesson["list"], range(len(lesson["list"]["items"])))

		typingInputLogicMod = self._modules.default("active", type="inputTypingLogic")
		self._ui = PractisingInterface(typingInputLogicMod.createController, lessonType)

		lessonType.newItem.handle(self._setNextItem)
		lessonType.lessonDone.handle(self._ui.quit)
		self._ui.run()

	def _setNextItem(self, word):
		question = self._compose(word["questions"])
		self._ui.setNextItem(question)

	def run(self, argList=None):
		"""Runs the command line interface. Called by this module itself
		   indirectly when in the 'cli' profile. Otherwise, you can call
		   it with an optional argList. (defaults to sys.argv)

		"""
		if argList is None:
			argList = sys.argv

		#import urwid only here. That's because it's a relatively heavy
		#dependency that's only required in a few special cases
		global urwid, EnterEdit, Event
		try:
			import urwid
		except ImportError:
			urwid = None
		else:
			Event = self._modules.default("active", type="event").createEvent
			EnterEdit = getEnterEdit(Event)

		#setup parser: using + instead of - to distinguish from the
		#execute module's argparse. (the one providing the -p arg).
		parser = argparse.ArgumentParser(**{
			"prog": argList[0] + " -p cli",
			"prefix_chars": "+",
		})

		#--version
		version = self._metadata["name"] + " " + self._metadata["version"]
		parser.add_argument("+v", "++version", action="version", version=version)

		subparsers = parser.add_subparsers()
		self._buildSubparsers(subparsers)

		args = parser.parse_args(argList[1:])
		if not set(vars(args)) - set(["func"]):
			parser.print_usage()
			return
		args.func(vars(args))

	def _buildSubparsers(self, subparsers):
		#shows authors
		authors = subparsers.add_parser("authors", help="show OpenTeacher's authors", prefix_chars="+")
		authors.add_argument("+c", "++category", help="only show authors in the specified category")
		authors.set_defaults(func=self._authors)

		loadingPossible = bool(set(self._mm.mods("active", type="loader")))
		savingPossible = bool(set(self._mm.mods("active", type="save")))
		wordListOcrPossible = bool(set(self._mm.mods("active", type="ocrWordListLoader")))

		#if at least one saver and loader available:
		if loadingPossible and savingPossible:
			#convert
			convert = subparsers.add_parser("convert", help="convert word, topo and media files", prefix_chars="+")
			convert.add_argument("+f", "++output-format", help="output format", default="otwd", choices=list(self._saveExts()))
			convert.add_argument("input-files", nargs="+", help="input files")
			convert.set_defaults(func=self._convert)

			#merge
			merge = subparsers.add_parser("merge", help="merge files of the same file type", prefix_chars="+")
			merge.add_argument("output-file", help="output file")
			merge.add_argument("base-file", help="base file")
			merge.add_argument("other-files", help="files to merge with base file into output file", nargs="+")
			merge.set_defaults(func=self._merge)

			#reverse list
			reverseList = subparsers.add_parser("reverse-list", help="reverse list", prefix_chars="+")
			reverseList.add_argument("input-file", help="input files")
			reverseList.add_argument("output-file", help="output file")
			reverseList.set_defaults(func=self._reverseList)

		#if at least a loader is available.
		if loadingPossible:
			#view-word-list
			viewWordList = subparsers.add_parser("view-word-list", help="show a word list", prefix_chars="+")
			viewWordList.add_argument("input-files", nargs="+", help="input files")
			viewWordList.add_argument("+p", "++part", choices=["list", "title", "question-lang", "answer-lang"], default="list")
			viewWordList.set_defaults(func=self._viewWordList)

		#saver & ocrWordListLoader required
		if savingPossible and wordListOcrPossible:
			#ocr-word-list
			ocrWordList = subparsers.add_parser("ocr-word-list", help="load a word list from a scan or photo", prefix_chars="+")
			ocrWordList.add_argument("input-file", help="input file")
			ocrWordList.add_argument("output-file", help="output file")
			ocrWordList.set_defaults(func=self._ocrWordList)

		#if at least a saver is available
		if savingPossible:
			#new-word-list
			newWordList = subparsers.add_parser("new-word-list", help="make a new word list", prefix_chars="+")
			newWordList.add_argument("output-file", help="output file")
			newWordList.add_argument("input-file", help="input file (default: stdin)", nargs="?", default="-")
			newWordList.add_argument("+t", "++title")
			newWordList.add_argument("+q", "++question-lang")
			newWordList.add_argument("+a", "++answer-lang")
			newWordList.set_defaults(func=self._newWordList)

		#if curses framework used for practising and at least one loader
		#is available.
		if urwid and loadingPossible:
			#practise-word-list
			practiseWordList = subparsers.add_parser("practise-word-list", help="practise a word list", prefix_chars="+")
			practiseWordList.add_argument("file", help="the file to practise")
			practiseWordList.add_argument("+l", "++lesson-type", choices=self._lessonTypes, default=self._lessonTypes[0])
			practiseWordList.set_defaults(func=self._practiseWordList)

	def enable(self):
		self._modules = next(iter(self._mm.mods(type="modules")))
		if self._modules.profile == "cli":
			self._modules.default("active", type="execute").startRunning.handle(self.run)

		self._metadata = self._modules.default("active", type="metadata").metadata
		self._composeWordList = self._modules.default("active", type="wordListStringComposer").composeList
		self._parseWordList = self._modules.default("active", type="wordListStringParser").parseList
		self._compose = self._modules.default("active", type="wordsStringComposer").compose

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self._metadata
		del self._composeWordList
		del self._parseWordList
		del self._compose

def init(moduleManager):
	return CommandLineInterfaceModule(moduleManager)
