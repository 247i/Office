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

import unittest
import StringIO
import sys
import tempfile
import os
import shutil

MODES = ("all", "cli")

class TestCase(unittest.TestCase):
	"""Some pretty basic tests for the cli module. For now, this only
	   tests the default cases. Not much, but better than nothing.

	"""
	def _test(self, command):
		for mod in self._mm.mods("active", type="cli"):
			out = StringIO.StringIO()
			sys.stdout = out
			sys.stderr = out
			try:
				mod.run(["testSuite"] + command.split())
			except SystemExit, e:
				if e.code:
					#info can be useful. sys.stderr isn't reset at this
					#point, so send to the real one.
					print >> sys.__stderr__, out.getvalue()
					raise
			finally:
				sys.stdout = sys.__stdout__
				sys.stderr = sys.__stderr__
			yield out.getvalue()

	def testVersion(self):
		"""+v"""

		for result in self._test("+v"):
			self.assertTrue(result)

	def testAuthors(self):
		"""authors"""

		for result in self._test("authors"):
			self.assertTrue(result)

	def testHelp(self):
		"""Test the most import help commands. practise-word-list not
		   because it depends on urwid which this test suite shouldn't
		   depend on in my opinion.

		"""
		for command in ["+h", "convert +h", "reverse-list +h", "view-word-list +h", "new-word-list +h", "ocr-word-list +h", "merge +h", "authors +h"]:
			for result in self._test(command):
				self.assertTrue(result)

	def testMerge(self):
		"""merge outFile.otwd fileOne.otwd fileOne.otwd"""
		if self.mode not in MODES:
			self.skipTest("Write IO is too heavy for this test mode")
		inputFile = self._mm.resourcePath("testfile.otwd")
		fd, outputFile = tempfile.mkstemp(".otwd")
		os.close(fd)
		#file shouldn't exist
		os.remove(outputFile)
		for result in self._test("merge %s %s %s" % (outputFile, inputFile, inputFile)):
			os.remove(outputFile)

	def testOcrWordList(self):
		"""ocr-word-list inputFile.png outputFile"""
		if self.mode not in MODES:
			self.skipTest("Write IO is too heavy for this test mode")

		inputFile = self._mm.resourcePath("ocr.png")

		fd, outputFile = tempfile.mkstemp(".otwd")
		#file shouldn't exist yet.
		os.close(fd)
		os.remove(outputFile)
		for result in self._test("ocr-word-list %s %s" % (inputFile, outputFile)):
			#removing should succeed...
			os.remove(outputFile)

	def testNewWordList(self):
		"""new-word-list +t title +q questionLang +a answerLang
		   outputFile inputFile

		"""
		if self.mode not in MODES:
			self.skipTest("Write IO is too heavy for this test mode")

		fd, inputFile = tempfile.mkstemp()
		os.close(fd)
		with open(inputFile, "w") as f:
			f.write("een = one\ntwee = two\n drie = three")

		try:
			fd, outputFile = tempfile.mkstemp(".otwd")
			os.close(fd)
			#file shouldn't exist yet.
			os.remove(outputFile)
			for result in self._test("new-word-list +t a +q b +a c %s %s" % (outputFile, inputFile)):
				os.remove(outputFile)
		finally:
			os.remove(inputFile)

	def testViewWordList(self):
		"""view-word-list +p [list/title/question-lang/answer-lang]
		   filename

		"""
		for commandPart in ["list", "title", "question-lang", "answer-lang"]:
			command = "view-word-list %s +p " % self._mm.resourcePath("testfile.otwd") + commandPart
			for result in self._test(command):
				#all fields are filled, so all should give output.
				self.assertTrue(result)

	def testReverseList(self):
		"""reverse-list input-file output-file"""

		if self.mode not in MODES:
			self.skipTest("Write IO is too heavy for this test mode")

		fd, outputFile = tempfile.mkstemp(".ot")
		#file shouldn't be there, it's created by the command itself
		os.close(fd)
		os.remove(outputFile)

		files = (
			self._mm.resourcePath("testfile.otwd"),
			outputFile
		)
		for result in self._test("reverse-list %s %s" % files):
			os.remove(outputFile)

	def testConvertList(self):
		"""convert +f html testfile.otwd"""
		#not literally because we may not assume the module's dir is
		#writable.

		if self.mode not in MODES:
			self.skipTest("Write IO is too heavy for this test mode")

		fd, inFile = tempfile.mkstemp(".otwd")
		os.close(fd)
		shutil.copy(self._mm.resourcePath("testfile.otwd"), inFile)

		try:
			outFile = os.path.splitext(inFile)[0] + ".html"
			for result in self._test("convert +f html " + inFile):
				os.remove(outFile)
		finally:
			os.remove(inFile)

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="cli"),
		)

	def enable(self):
		self.TestCase = TestCase
		self.TestCase._mm = self._mm
		self.active = True

	def disable(self):
		self.active = False
		del self.TestCase

def init(moduleManager):
	return TestModule(moduleManager)
