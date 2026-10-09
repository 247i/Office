#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2012, Marten de Vries
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

class TestCase(unittest.TestCase):
	def setUp(self):
		#some test data
		#self.tests[0] -> everything wrong
		#self.tests[2] -> everything right
		self.tests = [
		  {
			 "finished":True,
			 "results":[
				{
				   "itemId":0,
				   "active":{
					  "start":"2011-08-24T15:09:25.944141",
					  "end":"2011-08-24T15:09:27.146226"
				   },
				   "result":"wrong"
				},
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:09:27.673549",
					  "end":"2011-08-24T15:09:28.144691"
				   },
				   "result":"wrong"
				},
				{
				   "itemId":2,
				   "active":{
					  "start":"2011-08-24T15:09:28.491800",
					  "end":"2011-08-24T15:09:28.904997"
				   },
				   "result":"wrong"
				},
				{
				   "itemId":3,
				   "active":{
					  "start":"2011-08-24T15:09:29.201219",
					  "end":"2011-08-24T15:09:29.432250"
				   },
				   "result":"wrong"
				},
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:09:29.673220",
					  "end":"2011-08-24T15:09:30.792912"
				   },
				   "result":"wrong"
				}
			 ],
			 "pauses":[

			 ]
		  },
		  {
			 "finished":True,
			 "results":[
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:10:02.299261",
					  "end":"2011-08-24T15:10:03.977188"
				   },
				   "result":"wrong"
				},
				{
				   "itemId":2,
				   "active":{
					  "start":"2011-08-24T15:10:04.952568",
					  "end":"2011-08-24T15:10:03.977188"
				   },
				   "result":"wrong"
				},
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:10:04.961008",
					  "end":"2011-08-24T15:10:05.361158"
				   },
				   "result":"right"
				},
				{
				   "itemId":0,
				   "active":{
					  "start":"2011-08-24T15:10:05.680522",
					  "end":"2011-08-24T15:10:05.361158"
				   },
				   "result":"right"
				},
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:10:05.687530",
					  "end":"2011-08-24T15:10:06.401639"
				   },
				   "result":"right"
				},
				{
				   "itemId":0,
				   "active":{
					  "start":"2011-08-24T15:10:07.409116",
					  "end":"2011-08-24T15:10:06.401639"
				   },
				   "result":"right"
				},
				{
				   "itemId":2,
				   "active":{
					  "start":"2011-08-24T15:10:07.410956",
					  "end":"2011-08-24T15:10:07.953038"
				   },
				   "result":"wrong"
				},
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:10:08.401110",
					  "end":"2011-08-24T15:10:07.953038"
				   },
				   "result":"wrong"
				},
				{
				   "itemId":2,
				   "active":{
					  "start":"2011-08-24T15:10:08.403379",
					  "end":"2011-08-24T15:10:08.865068"
				   },
				   "result":"right"
				},
				{
				   "itemId":0,
				   "active":{
					  "start":"2011-08-24T15:10:09.185520",
					  "end":"2011-08-24T15:10:08.865068"
				   },
				   "result":"right"
				},
				{
				   "itemId":2,
				   "active":{
					  "start":"2011-08-24T15:10:09.187343",
					  "end":"2011-08-24T15:10:09.601458"
				   },
				   "result":"right"
				},
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:10:09.913626",
					  "end":"2011-08-24T15:10:09.601458"
				   },
				   "result":"right"
				},
				{
				   "itemId":2,
				   "active":{
					  "start":"2011-08-24T15:10:09.915555",
					  "end":"2011-08-24T15:10:10.801324"
				   },
				   "result":"right"
				},
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:10:11.145461",
					  "end":"2011-08-24T15:10:10.801324"
				   },
				   "result":"right"
				},
				{
				   "itemId":2,
				   "active":{
					  "start":"2011-08-24T15:10:11.147436",
					  "end":"2011-08-24T15:10:11.657522"
				   },
				   "result":"right"
				},
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:10:11.993991",
					  "end":"2011-08-24T15:10:11.657522"
				   },
				   "result":"right"
				},
				{
				   "itemId":2,
				   "active":{
					  "start":"2011-08-24T15:10:11.996046",
					  "end":"2011-08-24T15:10:12.354332"
				   },
				   "result":"wrong"
				},
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:10:12.832351",
					  "end":"2011-08-24T15:10:12.354332"
				   },
				   "result":"wrong"
				},
				{
				   "itemId":2,
				   "active":{
					  "start":"2011-08-24T15:10:12.834965",
					  "end":"2011-08-24T15:10:13.249458"
				   },
				   "result":"right"
				},
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:10:13.593326",
					  "end":"2011-08-24T15:10:13.249458"
				   },
				   "result":"right"
				},
				{
				   "itemId":2,
				   "active":{
					  "start":"2011-08-24T15:10:13.595555",
					  "end":"2011-08-24T15:10:13.905424"
				   },
				   "result":"right"
				},
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:10:14.169514",
					  "end":"2011-08-24T15:10:13.905424"
				   },
				   "result":"right"
				},
				{
				   "itemId":2,
				   "active":{
					  "start":"2011-08-24T15:10:14.171479",
					  "end":"2011-08-24T15:10:14.489749"
				   },
				   "result":"right"
				},
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:10:14.832392",
					  "end":"2011-08-24T15:10:14.489749"
				   },
				   "result":"right"
				},
				{
				   "itemId":2,
				   "active":{
					  "start":"2011-08-24T15:10:14.834724",
					  "end":"2011-08-24T15:10:15.218156"
				   },
				   "result":"right"
				},
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:10:15.505983",
					  "end":"2011-08-24T15:10:15.218156"
				   },
				   "result":"right"
				},
				{
				   "itemId":2,
				   "active":{
					  "start":"2011-08-24T15:10:15.507872",
					  "end":"2011-08-24T15:10:15.817086"
				   },
				   "result":"right"
				},
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:10:16.042107",
					  "end":"2011-08-24T15:10:15.817086"
				   },
				   "result":"right"
				},
				{
				   "itemId":2,
				   "active":{
					  "start":"2011-08-24T15:10:16.044186",
					  "end":"2011-08-24T15:10:16.281451"
				   },
				   "result":"right"
				},
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:10:16.553626",
					  "end":"2011-08-24T15:10:16.281451"
				   },
				   "result":"right"
				},
				{
				   "itemId":2,
				   "active":{
					  "start":"2011-08-24T15:10:16.555542",
					  "end":"2011-08-24T15:10:16.785355"
				   },
				   "result":"right"
				},
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:10:17.025174",
					  "end":"2011-08-24T15:10:16.785355"
				   },
				   "result":"right"
				},
				{
				   "itemId":2,
				   "active":{
					  "start":"2011-08-24T15:10:17.029441",
					  "end":"2011-08-24T15:10:17.241304"
				   },
				   "result":"right"
				},
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:10:17.449294",
					  "end":"2011-08-24T15:10:17.241304"
				   },
				   "result":"right"
				},
				{
				   "itemId":2,
				   "active":{
					  "start":"2011-08-24T15:10:17.451118",
					  "end":"2011-08-24T15:10:17.657334"
				   },
				   "result":"right"
				},
				{
				   "itemId":3,
				   "active":{
					  "start":"2011-08-24T15:10:17.832469",
					  "end":"2011-08-24T15:10:17.657334"
				   },
				   "result":"right"
				},
				{
				   "itemId":3,
				   "active":{
					  "start":"2011-08-24T15:10:17.834993",
					  "end":"2011-08-24T15:10:18.009024"
				   },
				   "result":"right"
				},
				{
				   "itemId":3,
				   "active":{
					  "start":"2011-08-24T15:10:18.185291",
					  "end":"2011-08-24T15:10:18.009024"
				   },
				   "result":"right"
				}
			 ],
			 "pauses":[

			 ]
		  },
		  {
			 "finished":True,
			 "results":[
				{
				   "itemId":0,
				   "active":{
					  "start":"2011-08-24T15:14:19.065182",
					  "end":"2011-08-24T15:14:19.891656"
				   },
				   "result":"right"
				},
				{
				   "itemId":1,
				   "active":{
					  "start":"2011-08-24T15:14:20.300313",
					  "end":"2011-08-24T15:14:20.731603"
				   },
				   "result":"right"
				},
				{
				   "itemId":2,
				   "active":{
					  "start":"2011-08-24T15:14:21.124117",
					  "end":"2011-08-24T15:14:21.539749"
				   },
				   "result":"right"
				},
				{
				   "itemId":3,
				   "active":{
					  "start":"2011-08-24T15:14:21.859836",
					  "end":"2011-08-24T15:14:22.300199"
				   },
				   "result":"right"
				}
			 ],
			 "pauses":[

			 ]
		  }
	   ]

	def testCalculateNote(self):
		for mod in self._mm.mods("active", type="noteCalculator"):
			note1 = mod.calculateNote(self.tests[0])
			note2 = mod.calculateNote(self.tests[1])
			note3 = mod.calculateNote(self.tests[2])

			#see comment above test data
			self.assertNotEquals(note1, note3)

			#should be a non empty string
			self.assertIsInstance(note1, basestring, msg=mod)
			self.assertIsInstance(note2, basestring, msg=mod)
			self.assertIsInstance(note3, basestring, msg=mod)
			self.assertTrue(note1, msg=mod)
			self.assertTrue(note2, msg=mod)
			self.assertTrue(note3, msg=mod)

	def testCalculateAverageNote(self):
		for mod in self._mm.mods("active", type="noteCalculator"):
			note = mod.calculateAverageNote(self.tests)

			#should be a non-empty string.
			self.assertIsInstance(note, basestring, msg=mod)
			self.assertTrue(note, msg=mod)

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="noteCalculator"),
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
