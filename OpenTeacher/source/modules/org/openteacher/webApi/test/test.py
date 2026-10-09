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
import tempfile
import os
import json
import sys

MODES = ("all", "web-api")

class TestCase(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		if not cls.mode in MODES:
			raise unittest.SkipTest("The current test isn't run because of the current mode.")
		#monkey patch the bcrypt module, gave the test suite a 9 second
		#speedup when this comment was written. Worth it.
		sys.modules["bcrypt"].hashpw = lambda password, salt_or_hash: password

		cls.clients = []
		for mod in cls._mm.mods("active", type="webApiServer"):
			mod.app.config["TESTING"] = True
			mod.app.config["KEYCHECK"] = False
			fd, mod.app.config["DATABASE"] = tempfile.mkstemp()
			os.close(fd)
			#make room for the database
			os.remove(mod.app.config["DATABASE"])

			client = mod.app.test_client()
			client.post("/users/", data={
				"apiKey": "whatever",
				"username": "test",
				"password": "test",
			})
			client.post("/users/", data={
				"apiKey": "whatever",
				"username": "secondtest",
				"password": "test",
			})
			cls.clients.append(client)

	@classmethod
	def tearDownClass(cls):
		for mod in cls._mm.mods("active", type="webApiServer"):
			os.remove(mod.app.config["DATABASE"])

	def testIndex(self):
		for client in self.clients:
			data = client.get("/").data
			self.assertIn("welcome", data)
			self.assertIn("version", data)
			self.assertIn("resources", data)

	def _auth(self, username, password):
		return {"Authorization": "Basic " + (username + ":" + password).encode("base64").strip()}

	def testShares(self):
		k = {"headers": self._auth("test", "test")}
		for client in self.clients:
			r = client.post("/lists/", data={
				"type": "words",
				"title": "1234",
				"items": "{}",
			}, **k)
			self.assertEqual(r.status_code, 200)

			r = client.post("/shares/", data={
				"name": "test share",
				"description": "description",
			}, **k)
			self.assertEqual(r.status_code, 200)

			url = json.loads(client.get("/shares/", **k).data)["result"][0]["url"]

			r = client.get(url)
			self.assertEqual(r.status_code, 200)
			self.assertIn("test share", r.data)

			r = client.put(url, data={
				"name": "test share edited",
				"description": "description edited",
			}, **k)
			self.assertEqual(r.status_code, 200)

			#url changed
			url = json.loads(client.get("/shares/", **k).data)["result"][0]["url"]
			listId = json.loads(client.get("/lists/", **k).data)["result"][0]["id"]

			r = client.post(url, data={
				"listId": listId,
			}, **k)
			self.assertEqual(r.status_code, 200)

			r = client.get(url)
			self.assertEqual(r.status_code, 200)
			sharedListUrl = json.loads(r.data)["result"]["lists"][0]["url"]

			r = client.get(sharedListUrl)
			self.assertEqual(r.status_code, 200)
			self.assertIn("1234", r.data)

			r = client.delete(sharedListUrl, **k)
			self.assertEqual(r.status_code, 200)

			r = client.delete(url, **k)
			self.assertEqual(r.status_code, 200)

	def testLists(self):
		k = {"headers": self._auth("test", "test")}
		k2 = {"headers": self._auth("secondtest", "test")}
		for client in self.clients:
			resp = client.get("/lists/", **k)
			self.assertEquals(resp.status_code, 200)
			self.assertEquals(json.loads(resp.data), {"result": []})

			resp2 = client.get("/lists/")
			self.assertEquals(resp2.status_code, 401)

			resp3 = client.post("/lists/", data={
				"type": "words",
				"title": "1234",
				"items": "{ }",
			}, **k)
			self.assertEquals(resp3.status_code, 200)

			resp4 = client.get("/lists/", **k)
			url = json.loads(resp4.data)["result"][0]["url"]

			resp5 = client.get(url, **k)
			self.assertEquals(resp5.status_code, 200)
			self.assertIn("{ }", resp5.data)

			resp6 = client.get(url)
			self.assertEquals(resp6.status_code, 401)

			resp7 = client.get(url, **k2)
			self.assertEquals(resp7.status_code, 404)

			resp8 = client.put(url)
			self.assertEquals(resp8.status_code, 401)

			resp9 = client.put(url, data={
				"type": "words",
				"title": "12345",
				"items": "{}",
			}, **k2)
			self.assertEquals(resp9.status_code, 404)

			resp10 = client.put(url, data={
				"type": "words",
				"title": "12345",
				"items": "{}",
			}, **k)
			self.assertEquals(resp10.status_code, 200)

			resp11 = client.delete(url, **k)
			self.assertEquals(resp11.status_code, 200)

	def testUsers(self):
		for client in self.clients:
			resp = client.post("/users/", data={
				#not actually tested, but we need to include one.
				"apiKey": "abcd",
				"username": "test1",
				"password": "test"
			})
			self.assertEquals(resp.status_code, 200)
			resp2 = client.post("/users/", data={
				"apiKey": "abcd",
				"username": "test1",
				"password": "test"
			})
			self.assertEquals(resp2.status_code, 403)

			resp3 = client.put("/users/test1", data={
				"username": "test2",
				"password": "testtest"
			}, headers=self._auth("test1", "test"))
			self.assertEquals(resp3.status_code, 200)

			resp4 = client.delete("/users/test2", headers=self._auth("test2", "testtest"))
			self.assertEquals(resp4.status_code, 200)

			resp5 = client.put("/users/test", data={
				"username": "a",
				"password": "b"
			})
			self.assertEquals(resp5.status_code, 401)

			resp55 = client.post("/users/", data={
				"apiKey": "whatever",
				"username": "other",
				"password": "test",
			})
			self.assertEquals(resp55.status_code, 200)

			resp6 = client.delete("/users/test", headers=self._auth("other", "test"))
			self.assertEquals(resp6.status_code, 404)

			resp7 = client.delete("/users/nonexisting", headers=self._auth("other", "test"))
			self.assertEquals(resp7.status_code, 404)

			resp8 = client.put("/users/nonexisting", headers=self._auth("other", "test"))
			self.assertEquals(resp8.status_code, 404)

class TestModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TestModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "test"
		self.requires = (
			self._mm.mods(type="webApiServer"),
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
