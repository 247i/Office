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
import itertools

class CheckCall(object):
	def __init__(self, *args, **kwargs):
		super(CheckCall, self).__init__(*args, **kwargs)

		self.reset()

	def __call__(self, *args, **kwargs):
		self.called = True
		self.args = args
		self.kwargs = kwargs

	def reset(self):
		self.called = False
		self.args = ()
		self.kwargs = {}

class UiEnablerWatcher(object):
	def __init__(self, controller, *args, **kwargs):
		super(UiEnablerWatcher, self).__init__(*args, **kwargs)

		self._onEnableCheck = CheckCall()
		controller.enableCheck.handle(self._onEnableCheck)
		self._onEnableSkip = CheckCall()
		controller.enableSkip.handle(self._onEnableSkip)
		self._onEnableInput = CheckCall()
		controller.enableInput.handle(self._onEnableInput)

	def assertUiHasBeenEnabled(self):
		assert self._onEnableCheck.called
		assert self._onEnableSkip.called
		assert self._onEnableInput.called

class UiDisablerWatcher(object):
	def __init__(self, controller, *args, **kwargs):
		super(UiDisablerWatcher, self).__init__(*args, **kwargs)

		self._onDisableCheck = CheckCall()
		controller.disableCheck.handle(self._onDisableCheck)
		self._onDisableSkip = CheckCall()
		controller.disableSkip.handle(self._onDisableSkip)
		self._onDisableInput = CheckCall()
		controller.disableInput.handle(self._onDisableInput)

	def assertUiHasBeenDisabled(self):
		assert self._onDisableCheck.called
		assert self._onDisableSkip.called
		assert self._onDisableInput.called

class TestCase(unittest.TestCase):
	@property
	def _list(self):
		return {
			"tests": [],
			"items": [
				{
					"id": 0,
					"questions": [["een"]],
					"answers": [["one"]],
				},
				{
					"id": 1,
					"questions": [["twee"]],
					"answers": [["two"]],
				},
			],
		}

	def setUp(self):
		self._lessonTypeMod = next(iter(self._mm.mods("active", type="lessonType", testName="allOnce")))

	@property
	def _lessonType(self):
		return self._lessonTypeMod.createLessonType(self._list, [0, 1])

	@property
	def _lessonType2(self):
		return self._lessonTypeMod.createLessonType(self._list, [1])

	def _getControllers(self):
		for c in self._getControllersWithoutLessonType():
			c.lessonType = self._lessonType
			yield c

	def _getControllersWithoutLessonType(self):
		for mod in itertools.chain(
			self._mm.mods("active", type="inputTypingLogic"),
			self._mm.mods("active", type="jsInputTypingLogic"),
		):
			yield mod.createController()

	def testCallingMethodsWithoutLessonType(self):
		for controller in self._getControllersWithoutLessonType():
			with self.assertRaises(AttributeError):
				controller.checkTriggered("shouldn't matter")
			with self.assertRaises(AttributeError):
				controller.correctAnywayTriggered()
			with self.assertRaises(AttributeError):
				controller.skipTriggered()
			with self.assertRaises(AttributeError):
				controller.userIsTyping()

	def testCallingMethodsWithoutStartingLesson(self):
		for controller in self._getControllers():
			with self.assertRaises(ValueError):
				controller.checkTriggered("whatever")
			with self.assertRaises(ValueError):
				controller.correctAnywayTriggered()
			with self.assertRaises(ValueError):
				controller.skipTriggered()
			with self.assertRaises(ValueError):
				controller.userIsTyping()

	def testSettingOtherLessonTypeWhileShowingACorrection(self):
		for controller in self._getControllers():
			self._makeUnusedControllerShowACorrection(controller)

			uiWatcher = UiEnablerWatcher(controller)
			onHideCorrection = CheckCall()
			controller.hideCorrection.handle(onHideCorrection)

			controller.lessonType = self._lessonType2

			self.assertTrue(onHideCorrection.called)
			uiWatcher.assertUiHasBeenEnabled()

			#start again to test if everything was cleaned up properly
			controller.lessonType.start()

	def _makeUnusedControllerShowACorrection(self, controller):
		onShowCorrection = CheckCall()
		controller.showCorrection.handle(onShowCorrection)
		onHideCorrection = CheckCall()
		controller.hideCorrection.handle(onHideCorrection)
		uiWatcher = UiDisablerWatcher(controller)

		controller.lessonType.start()
		controller.checkTriggered(u"a wrong answer")

		self.assertTrue(onShowCorrection.called)
		self.assertEqual(onShowCorrection.args, (u"one",))
		self.assertFalse(onHideCorrection.called)
		uiWatcher.assertUiHasBeenDisabled()

	def testMethodsWhileShowingCorrection(self):
		for controller in self._getControllers():
			self._makeUnusedControllerShowACorrection(controller)

			with self.assertRaises(ValueError):
				controller.checkTriggered(u"this answer doesn't matter")
			with self.assertRaises(ValueError):
				controller.skipTriggered()
			with self.assertRaises(ValueError):
				controller.userIsTyping()

	def testCorrectAnywayWhileShowingCorrection(self):
		for controller in self._getControllers():
			self._makeUnusedControllerShowACorrection(controller)

			onHideCorrection = CheckCall()
			controller.hideCorrection.handle(onHideCorrection)

			uiWatcher = UiEnablerWatcher(controller)

			controller.correctAnywayTriggered()
			self.assertTrue(onHideCorrection.called)
			uiWatcher.assertUiHasBeenEnabled()

	def testSkip(self):
		for controller in self._getControllers():
			onNewItem = CheckCall()
			controller.lessonType.newItem.handle(onNewItem)

			controller.lessonType.start()
			self.assertEqual((self._list["items"][0],), onNewItem.args)
			controller.skipTriggered()
			self.assertEqual((self._list["items"][1],), onNewItem.args)

	def testCompleteLesson(self):
		for controller in self._getControllers():
			controller.lessonType.start()
			#right answer both times
			controller.checkTriggered(u"one")
			controller.checkTriggered(u"two")

	def testCallingCorrectionShowingDoneWhileNoCorrectionIsShown(self):
		for controller in self._getControllers():
			controller.lessonType.start()
			with self.assertRaises(ValueError):
				controller.correctionShowingDone()

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="inputTypingLogic"),
			self._mm.mods(type="lessonType", testName="allOnce"),
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
