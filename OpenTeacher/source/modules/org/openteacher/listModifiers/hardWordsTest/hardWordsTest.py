#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2012, Marten de Vries
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

class HardWordsTestCase(unittest.TestCase):
	def testWordWithoutResults(self):
		wordList = {
			"items": [
				{
					"id": 0,
				},
			],
		}

		self._test(wordList, [0])

	def testMultipleTests(self):
		wordList = {
			"items": [
				{
					"id": 0,
				},
			],
			"tests": [
				[
					{
						"result": "right",
						"itemId": 0,
					},
					{
						"result": "wrong",
						"itemId": 0,
					},
					{
						"result": "right",
						"itemId": 0,
					},
				],
				[
					{
						"result": "wrong",
						"itemId": 0,
					},
					{
						"result": "wrong",
						"itemId": 0,
					},
				],
			]
		}

		self._test(wordList, [0])

	def testMultipleWords(self):
		wordList = {
			"items": [
				{
					"id": 0,
				},
				{
					"id": 1,
				},
			],
			"tests": [
				[
					{
						"result": "right",
						"itemId": 0,
					},
					{
						"result": "wrong",
						"itemId": 1,
					},
					{
						"result": "right",
						"itemId": 0,
					},
					{
						"result": "wrong",
						"itemId": 1,
					},
					{
						"result": "wrong",
						"itemId": 0,
					},
				],
			],
		}
		
		self._test(wordList, [1])

	def test50Percent(self):
		#it should be larger than 50%
		wordList = {
			"items": [
				{
					"id": 0,
				},
			],
			"tests": [
				[
					{
						"result": "right",
						"itemId": 0,
					},
					{
						"result": "wrong",
						"itemId": 0,
					},
				],
			],
		}
		self._test(wordList, [])

	def _test(self, input, output):
		for mod in self._mm.mods("active", type="listModifier", testName="hardWords"):
			indexes = mod.modifyList(range(len(input["items"])), input)
			self.assertEqual(indexes, output)

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.uses = (
			self._mm.mods(type="listModifier", testName="hardWords"),
		)

	def enable(self):
		self.TestCase = HardWordsTestCase
		self.TestCase._mm = self._mm
		self.active = True

	def disable(self):
		self.active = False
		del self.TestCase

def init(moduleManager):
	return TestModule(moduleManager)
