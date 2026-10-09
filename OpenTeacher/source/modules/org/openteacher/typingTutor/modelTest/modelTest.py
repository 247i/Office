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
import logging

logger = logging.getLogger(__name__)

TEST_USERNAME = "_modeltest"

class TestCase(unittest.TestCase):
	@property
	def models(self):
		return [m.model for m in self._mm.mods("active", type="typingTutorModel")]

	def setUp(self):
		for m in self.models:
			m.registerUser(TEST_USERNAME)

	def tearDown(self):
		for m in self.models:
			m.deregisterUser(TEST_USERNAME)

	def testRegisterUnregisterErrors(self):
		for m in self.models:
			with self.assertRaises(m.UsernameEmptyError):
				m.registerUser("")
			with self.assertRaises(m.UsernameTakenError):
				m.registerUser(TEST_USERNAME, "COLEMAK_LAYOUT")
			m.deregisterUser(TEST_USERNAME)
			with self.assertRaises(KeyError):
				m.deregisterUser(TEST_USERNAME)
			#for tearDown
			m.registerUser(TEST_USERNAME)

	def testUsernames(self):
		for m in self.models:
			self.assertIn(TEST_USERNAME, m.usernames)

	def _constructArgsForSession(self):
		argList = [
			None,
			(TEST_USERNAME, 20, 0),
			(TEST_USERNAME, 10, 3),
			(TEST_USERNAME, 30, 2),
			None,
			(TEST_USERNAME, 10, 0),
		]
		for i in range(50):
			argList.append((TEST_USERNAME, 10, 0))
		argList.append(None)
		argList.append((TEST_USERNAME, 5, 3))
		argList.append(None)
		for i in range(10):
			argList.append((TEST_USERNAME, 5, 0))
		return argList

	def _examineAmountOfMistakes(self, model, iteration):
		#the first iteration, no test results are known yet.
		if iteration == 0:
			with self.assertRaises(IndexError):
				model.amountOfMistakes(TEST_USERNAME)
		else:
			self.assertIsInstance(model.amountOfMistakes(TEST_USERNAME), int)

	def _examineInstruction(self, model):
		instruction = model.currentInstruction(TEST_USERNAME)
		logger.debug("INSTRUCTION: " + instruction)
		self.assertIsInstance(instruction, basestring)
		self.assertTrue(instruction)

	def _examineExercise(self, model):
		exercise = model.currentExercise(TEST_USERNAME)
		logger.debug("NEW EXERCISE: " + exercise)
		self.assertIsInstance(exercise, basestring)
		self.assertTrue(exercise)

	def _examineLayout(self, model):
		self.assertEqual(model.layout(TEST_USERNAME), model.QWERTY_LAYOUT)

	def _examineLevel(self, model):
		level = model.level(TEST_USERNAME)
		logger.debug("LEVEL: %s", level)
		self.assertIsInstance(level, int)
		self.assertTrue(level >= 0)

	def _examineMaxLevel(self, model):
		maxLevel = model.maxLevel(TEST_USERNAME)
		self.assertIsInstance(maxLevel, int)
		self.assertTrue(maxLevel >= 0)

	def _examineSpeed(self, model, iteration):
		if iteration == 0:
			with self.assertRaises(IndexError):
				model.speed(TEST_USERNAME)
		else:
			speed = model.speed(TEST_USERNAME)
			logger.debug("SPEED PREVIOUS EXERCISE: %s wpm", speed)
			self.assertIsInstance(speed, int)
			self.assertTrue(speed >= 0)

	def _examineTargetSpeed(self, model):
		targetSpeed = model.targetSpeed(TEST_USERNAME)
		self.assertIsInstance(targetSpeed, int)
		self.assertTrue(targetSpeed >= 0)

	def testSession(self):
		"""This test has some lines commented out which can be very
		   useful while debugging.

		"""
		argList = self._constructArgsForSession()

		for model in self.models:
			for iteration, args in enumerate(argList):
				if args:
					model.setResult(*args)

				self._examineAmountOfMistakes(model, iteration)
				self._examineInstruction(model)
				self._examineExercise(model)
				self._examineLayout(model)
				self._examineLevel(model)
				self._examineMaxLevel(model)
				self._examineSpeed(model, iteration)
				self._examineTargetSpeed(model)

				logger.debug("")

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="typingTutorModel"),
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
