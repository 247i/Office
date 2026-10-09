#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2011-2012, Marten de Vries
#
#	This file is part of OpenTeacher.
#
#	OpenTeacher is free software: you can redistribute it and/or modify
#	it under the terms of the GNU Affero General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	OpenTeacher is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU Affero General Public License for more details.
#
#	You should have received a copy of the GNU Affero General Public License
#	along with OpenTeacher.  If not, see <http://www.gnu.org/licenses/>.

import cherrypy

import os
import sys
import django.core.handlers.wsgi

def main():
	path = os.path.join(os.path.dirname(__file__))
	sys.path.insert(0, path)
	sys.path.insert(0, os.path.join(path, "ot_testserver"))
	os.environ["DJANGO_SETTINGS_MODULE"] = "settings"

	cherrypy.config.update({
		"server.ssl_certificate": os.path.join(path, "cert.pem"),
		"server.ssl_private_key": os.path.join(path, "privatekey.pem"),
		"server.socket_port": 8080,
		"server.socket_host": "0.0.0.0",
		"environment": "production",
	})

	cherrypy.tree.graft(django.core.handlers.wsgi.WSGIHandler(), "/")
	cherrypy.tree.mount(None, os.path.join(path, "/static/admin"), {"/": {
			"tools.staticdir.on": True,
			"tools.staticdir.dir": os.path.abspath(os.path.join(path, "admin_files")),
		}
	})

	cherrypy.engine.start()
	print "Serving at https://localhost:8080/"
	print "Type 'quit' and press enter to stop the server"
	while True:
		try:
			if raw_input("> ") in ("q", "Q", "quit", "Quit"):
				break
		except KeyboardInterrupt:
			break
	cherrypy.engine.exit()

if __name__ == "__main__":
	main()
