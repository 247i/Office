#	Copyright 2011, Marten de Vries
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

from django.contrib.auth import authenticate

class HTTPBasicMiddleware(object):
	def process_request(self, request):
		if not request.META.has_key("HTTP_AUTHORIZATION"):
			return
		data = request.META["HTTP_AUTHORIZATION"].strip("Basic").strip()
		try:
			username, password = data.decode("base64").split(":")
		except: #just to be sure
			return
		user = authenticate(username=username, password=password)
		if user:
			request.user = user

	def process_response(self, request, response):
		if not request.user.id: #AnynoymousUser
			response["WWW-Authenticate"] = 'Basic realm="OpenTeacher test server"'
		return response
