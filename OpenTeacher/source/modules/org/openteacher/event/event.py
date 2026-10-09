#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011, Marten de Vries
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

class Event(object):
	def __init__(self, *args, **kwargs):
		super(Event, self).__init__(*args, **kwargs)

		self._handlers = set()

	def handle(self, handler):
		self._handlers.add(handler)

	def unhandle(self, handler):
		self._handlers.remove(handler)

	def send(self, *args, **kwargs):
		for handler in self._handlers.copy():
			handler(*args, **kwargs)

class EventModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(EventModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "event"
		#The event module doesn't have to be enabled.
		self.active = True

	@staticmethod
	def createEvent(*args, **kwargs):
		"""Builds an event; an object similar to a PyQt4 signal but then
		   implemented in pure Python and differently named methods to
		   distinguish it from a signal. Methods are:

		   - ``handle(func)``; adds a handler
		   - ``unhandle(func)``; removes a handler
		   - ``send(*args, **kwargs)``; calls all handlers with the
		     arguments passed to itself. No calling order is guaranteed.

		"""
		return Event(*args, **kwargs)

def init(moduleManager):
	return EventModule(moduleManager)
