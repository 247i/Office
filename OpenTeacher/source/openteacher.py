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

import os
import sys

MODULES_PATH = os.path.join(os.path.dirname(__file__), "modules")

class ModuleApplication(object):
	def run(self):
		#simplify json importing
		try:
			sys.modules["json"] = __import__("simplejson")
		except ImportError:
			sys.modules["json"] = __import__("json")
		#simplify unittest importing
		if sys.version < "2.7":
			sys.modules["unittest"] = __import__("unittest2")
		else:
			sys.modules["unittest"] = __import__("unittest")

		import moduleManager

		mm = moduleManager.ModuleManager(MODULES_PATH)

		#check if there's only one execute module
		mods = set(mm.mods(type="execute"))
		if len(mods) != 1:
			raise ValueError("There has to be exactly one execute module installed.")
		#start that module
		mods.pop().execute()
		#nothing crashed, so exit code's 0.
		return 0

if __name__ == "__main__":
	try:
		import pyximport
	except ImportError:
		pass
	else:
		pyximport.install()

	app = ModuleApplication()
	sys.exit(app.run())
