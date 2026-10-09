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

class WebApiServerRunnerModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(WebApiServerRunnerModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "webApiServerRunner"
		self.requires = (
			self._mm.mods(type="execute"),
			self._mm.mods(type="webApiServer"),
		)
		self.priorities = {
			"default": -1,
			"web-api-server": 0,
		}

	def _run(self):
		app = self._modules.default("active", type="webApiServer").app
		app.config["DATABASE"] = "database.sqlite3"
		app.config["RECAPTCHA_PUBLIC_KEY"] = "put a key here"
		app.config["RECAPTCHA_PRIVATE_KEY"] = "put a key here"
		app.run()

	def enable(self):
		self._modules = next(iter(self._mm.mods(type="modules")))
		self._modules.default(type="execute").startRunning.handle(self._run)

		self.active = True

	def disable(self):
		self.active = False

		del self._modules

def init(moduleManager):
	return WebApiServerRunnerModule(moduleManager)
