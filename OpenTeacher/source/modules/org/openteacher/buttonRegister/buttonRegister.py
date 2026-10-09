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

class Button(object):
	"""Represents a Button. UI modules should draw a button and handle
	   the events so they're updated on changes. User modules use it
	   as an abstract way of changing the buttons, by sending the change
	   events with arguments. Note that the UI can't always respect all
	   the values passed in via the events. That's up to the UI
	   implementation.

	   Properties:

	   - category (read-only)

	   Events:

	   - clicked() -> gui to user
	   - changeText(text) -> user to gui
	   - changeIcon(icon_path) -> user to gui
	   - changeSize(size) -> user to gui
	     size is a string: either 'small' or 'large'.
	   - changePriority(priority) -> user to gui
	     piority is a number; 0 is high, inifinity low.

	"""
	def __init__(self, category, createEvent, *args, **kwargs):
		"""category must be either 'create', 'load' or
		   'load-from-internet'.

		"""
		super(Button, self).__init__(*args, **kwargs)

		self.category = category

		self.clicked = createEvent()
		self.changeText = createEvent()
		self.changeIcon = createEvent()
		self.changePriority = createEvent()
		self.changeSize = createEvent()

class ButtonRegisterModule(object):
	"""Module that provides a register of all 'buttons', a way for
	   features to present themselves to the user next to the menus.

	   UI's keep track of all registered an unregistered buttons by
	   handling the ``addButton`` and ``removeButton`` events. They get
	   passed the same kind of object as the caller of
	   ``registerButton`` gets back.

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(ButtonRegisterModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "buttonRegister"

		self.requires = (
			self._mm.mods(type="event"),
		)

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._createEvent = self._modules.default(type="event").createEvent
		self.addButton = self._createEvent()
		self.removeButton = self._createEvent()

		self.active = True

	def disable(self):
		self.active = False

		del self._modules
		del self._createEvent
		del self.addButton
		del self.removeButton

	def registerButton(self, category):
		"""Creates a new Button object, and tells the world (mostly the
		   gui modules) it has been created. It returns the resulting
		   object to the user. `category` can be everything in theory,
		   if you want your button to be shown using a string with value
		   'load', 'load-from-internet' or 'create' is a good idea.

			Returns an object, the docstring of that objects is:

		"""
		b = Button(category, self._createEvent)
		self.addButton.send(b)
		return b
	registerButton.__doc__ += Button.__doc__

	def unregisterButton(self, b):
		"""Tell 'the world' the button `b` isn't in use anymore. User
		   responsibility to call this on disable.

		"""
		self.removeButton.send(b)

def init(moduleManager):
	return ButtonRegisterModule(moduleManager)
