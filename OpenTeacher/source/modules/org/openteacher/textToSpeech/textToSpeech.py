#! /usr/bin/env python
# -*- coding: utf-8 -*-

#    Copyright 2011, Milan Boers
#    Copyright 2011-2012, Marten de Vries
#
#    This file is part of OpenTeacher.
#
#    OpenTeacher is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    OpenTeacher is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with OpenTeacher.  If not, see <http://www.gnu.org/licenses/>.

import os
import threading
import sys
import contextlib

DEFAULT_SPEED = 120
MINIMAL_SPEED = 1

class SpeakThread(threading.Thread):
	def __init__(self, engine):
		super(SpeakThread, self).__init__()

		self.engine = engine

	def run(self):
		try:
			self.engine.runAndWait()
		except RuntimeError:
			pass

class TextToSpeech(object):
	def __init__(self, pyttsx):
		self.engine = pyttsx.init()

	def getVoices(self):
		feedback = []
		voices = self.engine.getProperty("voices")
		for voice in voices:
			feedback.append((voice.name, voice.id))
		return feedback

	def speak(self, text, rate=None, voiceid=None, thread=True):
		if not text:
			return
		# Set voice
		if voiceid:
			self.engine.setProperty('voice', voiceid)
		if rate:
			self.engine.setProperty('rate', rate)
		self.engine.say(text)

		st = SpeakThread(self.engine)
		if thread:
			st.start()
		else:
			#makes run() run in the current thread
			st.run()

class TextToSpeechModule(object):
	voiceid = None
	def __init__(self, mm):
		self._mm = mm

		self.type = "textToSpeech"
		self.uses = (
			self._mm.mods(type="translator"),
		)
		self.requires = (
			self._mm.mods(type="event"),
		)
		self.filesWithTranslations = ("textToSpeech.py",)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()

		try:
			import pyttsx
		except ImportError:
			return

		# Create text to speech engine
		try:
			self.tts = TextToSpeech(pyttsx)
		except (OSError, RuntimeError):
			return

		#load translator
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			pass
		else:
			translator.languageChanged.handle(self._retranslate)
		self._retranslate()

		settings = self._modules.default(type="settings")
		
		# Add settings
		self._ttsVoice = settings.registerSetting(**{
			"internal_name": "org.openteacher.textToSpeech.voice",
			"type": "option",
			"defaultValue": self.tts.getVoices()[0][1],
			"options": self.tts.getVoices(),
		})
		self._ttsSpeed = settings.registerSetting(**{
			"internal_name": "org.openteacher.textToSpeech.speed",
			"type": "number",
			"defaultValue": DEFAULT_SPEED,
			"minValue": MINIMAL_SPEED,
		})
		self._retranslate()

		# Create the say word event
		self.say = self._modules.default(type="event").createEvent()

		self.say.handle(self.newWord)

		self.active = True

	def _retranslate(self):
		#Translations
		try:
			translator = self._modules.default("active", type="translator")
		except IndexError:
			_, ngettext = unicode, lambda a, b, n: a if n == 1 else b
		else:
			_, ngettext = translator.gettextFunctions(
				self._mm.resourcePath("translations")
			)

		try:
			self._ttsVoice["name"] = _("Voice name (language)")
			self._ttsSpeed["name"] = _("Speed")

			categories = {
				"category": _("Pronounciation"),
				"subcategory": _("Voice"),
			}
			self._ttsVoice.update(categories)
			self._ttsSpeed.update(categories)
		except AttributeError:
			#first time retranslate
			pass

	def disable(self):
		del self._modules
		with contextlib.ignored(AttributeError):
			del self.tts
		with contextlib.ignored(AttributeError):
			del self.say
		with contextlib.ignored(AttributeError):
			del self._ttsVoice
		with contextlib.ignored(AttributeError):
			del self._ttsSpeed

		self.active = False
	
	def newWord(self, word, thread=True):
		# First voice as default/if none is selected
		voiceid = self.tts.getVoices()[0][1]
		# Get the selected voice
		if self._ttsVoice is not None:
			voiceid = self._ttsVoice["value"]
		# Get the selected speed
		speed = self._ttsSpeed["value"] or DEFAULT_SPEED
		# Pronounce
		self.tts.speak(word,speed,voiceid,thread)

def init(moduleManager):
	return TextToSpeechModule(moduleManager)
