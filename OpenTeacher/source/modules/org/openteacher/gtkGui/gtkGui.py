#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2013, Marten  de Vries
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

def installGtkClasses():
	global EnterWindow, TeachWindow

	class EnterWindow(Gtk.Window):
		def __init__(self, Event, *args, **kwargs):
			super(EnterWindow, self).__init__(*args, **kwargs)

			edit = Gtk.TextView()
			self._textBuffer = edit.get_buffer()
			self._textBuffer.set_text("een = one\ntwee = two\ndrie = three\n")

			self.lessonStartRequested = Event()
			button = Gtk.Button(label="Start lesson")
			button.connect("clicked", self.on_button_clicked)

			box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
			box.pack_start(edit, expand=True, fill=True, padding=0)
			box.pack_start(button, expand=False, fill=True, padding=0)

			self.add(box)
			self.resize(400, 300)

		def on_button_clicked(self, widget):
			text = self._textBuffer.get_text(self._textBuffer.get_start_iter(), self._textBuffer.get_end_iter(), True).decode("UTF-8")
			self.lessonStartRequested.send(text)

	class TeachWindow(Gtk.Window):
		def __init__(self, createLessonType, createEvent, compose, createController, *args, **kwargs):
			super(TeachWindow, self).__init__(*args, **kwargs)

			self._createLessonType = createLessonType
			self._compose = compose

			self.lessonDone = createEvent()

			self._build_ui()
			self._controller = createController()

			#connect buttons
			self._checkButton.connect("clicked", self.on_check_clicked)
			self._skipButton.connect("clicked", self._controller.skipTriggered)
			self._correctAnywayButton.connect("clicked", self._controller.correctAnywayTriggered)

			#handle events
			self._controller.clearInput.handle(lambda: self._inputEntry.set_text(""))
			self._controller.enableInput.handle(lambda: self._inputEntry.set_editable(True))
			self._controller.disableInput.handle(lambda: self._inputEntry.set_editable(False))
			self._controller.focusInput.handle(self._inputEntry.grab_focus)

			self._controller.showCorrection.handle(self.show_correction)
			self._controller.hideCorrection.handle(lambda: self._correctionLabel.set_text(""))

			self._controller.enableCheck.handle(lambda: self._checkButton.set_sensitive(True))
			self._controller.disableCheck.handle(lambda: self._checkButton.set_sensitive(False))
			self._controller.enableSkip.handle(lambda: self._skipButton.set_sensitive(True))
			self._controller.disableSkip.handle(lambda: self._skipButton.set_sensitive(False))
			self._controller.enableCorrectAnyway.handle(lambda: self._correctAnywayButton.set_sensitive(True))
			self._controller.disableCorrectAnyway.handle(lambda: self._correctAnywayButton.set_sensitive(False))

		def on_check_clicked(self, widget):
			self._controller.checkTriggered(self._inputEntry.get_text().decode("UTF-8"))

		def show_correction(self, correction):
			self._correctionLabel.set_text(correction)

			GLib.timeout_add(2000, self.correction_showing_done)

		def correction_showing_done(self):
			self._controller.correctionShowingDone()
			#don't call this one again.
			return False

		def _build_ui(self):
			self._questionLabel = Gtk.Label()
			self._correctionLabel = Gtk.Label()
			self._inputEntry = Gtk.Entry()
			self._checkButton = Gtk.Button(label="Check")
			self._skipButton = Gtk.Button(label="Skip")
			self._correctAnywayButton = Gtk.Button(label="Correct anyway")

			box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
			box.pack_start(self._questionLabel, expand=False, fill=True, padding=0)
			box.pack_start(self._correctionLabel, expand=False, fill=True, padding=0)
			box.pack_start(self._inputEntry, expand=False, fill=True, padding=0)
			box.pack_start(self._checkButton, expand=False, fill=True, padding=0)
			box.pack_start(self._skipButton, expand=False, fill=True, padding=0)
			box.pack_start(self._correctAnywayButton, expand=False, fill=True, padding=0)

			self.add(box)
			self.resize(400, 300)

		def startLesson(self, lessonData):
			lessonList = lessonData["list"]
			indexes = range(len(lessonList["items"]))
			lessonType = self._createLessonType(lessonList, indexes)

			self._controller.lessonType = lessonType
			lessonType.newItem.handle(self._newItem)
			lessonType.lessonDone.handle(self.lessonDone.send)
			lessonType.start()

			self.show()

		def _newItem(self, item):
			questions = self._compose(item.get("questions", []))
			self._questionLabel.set_text(questions)

class GtkGui(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(GtkGui, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "gtkGui"
		self.priorities = {
			"default": -1,
			"gtk": 0,
		}
		self.requires = (
			self._mm.mods(type="execute"),
			self._mm.mods(type="wordListStringParser"),
			self._mm.mods(type="wordListStringComposer"),
			self._mm.mods(type="lessonType"),
			self._mm.mods(type="inputTypingLogic"),
		)

	def _run(self):		
		self._enterWin = EnterWindow(self._createEvent)
		self._enterWin.connect("delete-event", Gtk.main_quit)
		self._enterWin.lessonStartRequested.handle(self._startLesson)
		self._enterWin.show_all()

		self._teachWin = TeachWindow(self._createLessonType, self._createEvent, self._compose, self._createController)
		self._teachWin.connect("delete-event", Gtk.main_quit)
		self._teachWin.lessonDone.handle(self._backToEntering)
		self._teachWin.show_all()
		self._teachWin.hide()

		Gtk.main()

	def _startLesson(self, data):
		self._enterWin.hide()

		lessonData = self._modules.default("active", type="wordListStringParser").parseList(data)
		self._teachWin.startLesson(lessonData)

	def _backToEntering(self):
		self._teachWin.hide()
		self._enterWin.show()

	def enable(self):
		global Gtk, GLib
		try:
			from gi.repository import Gtk, GLib
		except ImportError:
			return
		installGtkClasses()

		self._modules = next(iter(self._mm.mods(type="modules")))
		self._modules.default("active", type="execute").startRunning.handle(self._run)

		self._createEvent = self._modules.default("active", type="event").createEvent
		self._createLessonType = self._modules.default("active", type="lessonType").createLessonType
		self._createController = self._modules.default("active", type="inputTypingLogic").createController
		self._compose = self._modules.default("active", type="wordsStringComposer").compose

		self.active = True

	def disable(self):
		self.active = False

		self._modules.default("active", type="execute").startRunning.unhandle(self._run)
		del self._modules
		del self._createEvent
		del self._createLessonType
		del self._createController
		del self._compose

def init(moduleManager):
	return GtkGui(moduleManager)
