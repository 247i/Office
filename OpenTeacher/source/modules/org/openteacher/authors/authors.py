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

import collections

class AuthorsModule(object):
	"""This module keeps track of the authors of OpenTeacher. Every
	   installed module can use it to add authors itself. This way, it's
	   possible to also give credit to third party module authors. Just
	   call the `registerAuthor` method.

	   If you're writing a module which depends on other OT modules and
	   shows credits in some way, this module is the ideal data source.
	   Give the `registeredAuthors` property a look.

	"""
	def __init__(self, moduleManager, *args, **kwargs):
		super(AuthorsModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "authors"

	def registerAuthor(self, category, name):
		"""Registers author `name` for his/her work in `category`. Both
		   arguments should be convertible with `unicode()`.

		   Returns a function which, when called, removes the author
		   again from the list. Handy if you want to retranslate the
		   category for example.

		"""
		data = (unicode(category), unicode(name))
		self._authors.update((data,))
		return lambda: self._authors.subtract((data,))

	@property
	def registeredAuthors(self):
		"""Returns an iterable type which contains `(category, name)`
		   tuples of authors. You're free to modify the data type you
		   get, it won't damage this module.

			Tuple attribute description:
		   `category`: the type of work this author was involved in.
		   `name`: the name of the author.

		   Both are guaranteed to be unicode strings. All authors are
		   only listed once, no matter if they were or were not added
		   multiple times.

		"""
		return set((a for a in self._authors if self._authors[a] > 0))

	def enable(self):
		self._authors = collections.Counter()

		self.active = True

	def disable(self):
		self.active = False

		del self._authors

def init(moduleManager):
	return AuthorsModule(moduleManager)
