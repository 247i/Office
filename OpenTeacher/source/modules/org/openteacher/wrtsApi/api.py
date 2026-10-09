#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2009-2012, Marten de Vries
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

import urllib2
import traceback
from etree import ElementTree

import xml.dom.minidom

class LoginError(ValueError):
	pass

class ConnectionError(IOError):
	pass

class NotEnoughMetadataError(ValueError):
	pass

class ShareNotFoundError(ValueError):
	pass

class RequestXml(xml.dom.minidom.Document):
	"""The RequestXml class is used to create xml understood by the WRTS-api. The
	   xml is used to send wordLists to WRTS."""
	def __init__(self, wordList, compose):
		xml.dom.minidom.Document.__init__(self)
		self.wordList = wordList

		self._compose = compose

	def createXml(self):
		l = self.wordList
		#Check if enough metadata is supplied, otherwise raise an error.
		if not (
			"title" in l and l["title"] and
			"questionLanguage" in l and l["questionLanguage"] and
			"answerLanguage" in l and l["answerLanguage"]
		):
			raise NotEnoughMetadataError()

		#create the root-element
		listDom = self.createElement("list")
		self.appendChild(listDom)

		#create a words-element
		wordsDom = self.createElement("words")
		listDom.appendChild(wordsDom)

		#append a title, question language, and answer language element
		titleDom = self.createElement("title")
		titleDom.appendChild(self.createTextNode(l["title"]))
		listDom.appendChild(titleDom)

		questionLanguageDom = self.createElement("lang-a")
		questionLanguageDom.appendChild(self.createTextNode(l["questionLanguage"]))
		listDom.appendChild(questionLanguageDom)

		answerLanguageDom = self.createElement("lang-b")
		answerLanguageDom.appendChild(self.createTextNode(l["answerLanguage"]))
		listDom.appendChild(answerLanguageDom)

		if "items" in l:
			for word in l["items"]:
				#create word-element
				wordDom = self.createElement("word")

				#append question
				questionWordDom = self.createElement("word-a")
				questionWordDom.appendChild(self.createTextNode(
					self._compose(word["questions"])
				))
				wordDom.appendChild(questionWordDom)

				#append answer (and second answer if one)
				answerWordDom = self.createElement("word-b")
				answerWordDom.appendChild(self.createTextNode(
					self._compose(word["answers"])
				))
				wordDom.appendChild(answerWordDom)

				#append word to wordsElement
				wordsDom.appendChild(wordDom)
		return self.toxml(encoding="UTF-8")

class WrtsConnection(object):
	"""This class is used to keep a connection with WRTS. It stores authenticationdata and offers some
	   methods which make it easy to get some data without the need of remembering the URL.

	   Methods:
		   login(email, password)
		   exportWordList(wordList)
		   importWordLIst(url)

		Properties:
			lists - gets all lists from the open account
			loggedIn - tells if the connection keeps valid (working) credentials of the user"""

	class HeadRequest(urllib2.Request):
		"""This class is used to let urllib2 perform a HEAD-request."""
		def get_method(self):
			return "HEAD"

	def __init__(self, parse, *args, **kwargs):
		super(WrtsConnection, self).__init__(*args, **kwargs)

		self._parse = parse
		self.loggedIn = False

	def logIn(self, email, password):
		"""Creates a connection to WRTS, with the authenticationdata inside it. Raises possibly a ConnectionError/LoginError"""

		#Create connection
		unencoded = u"%s:%s" % (email, password)
		#to UTF-8, because we need binary
		unencoded = str(unencoded.encode("utf-8"))
		encoded = unencoded.encode("base64").strip()

		self._opener = urllib2.build_opener()
		self._opener.addheaders = [("Authorization", "Basic %s" % encoded),
								   ("User-Agent", "OpenTeacher")]

		#Try loading the api; if not logged in it won't work, and raises a LoginError
		self._openUrl("http://www.wrts.nl/api", "HEAD")

	@property
	def listsParser(self):
		"""Get all wrts-lists; returns a WrtsListParser instance."""
		xml = self._openUrl("http://www.wrts.nl/api/lists")
		return ListsParser(xml)

	def shareListsParser(self, shareName):
		"""Get all wrts-lists on the share specified by url. Returns a
		   WrtsListParser instance.

		"""
		try:
			xml = self._openUrl("http://www.wrts.nl/api/shared/" + shareName, show404=True)
		except urllib2.HTTPError, e:
			#this can only be a 404 due to the self._openUrl design
			raise ShareNotFoundError(shareName)
		return ListsParser(xml)

	def exportWordList(self, wordList, compose):
		"""Exports a wordList to WRTS, fully automatic after your login. Throws LoginError/ConnectionError"""
		#Create the xml-document and set the wordlist
		requestXml = RequestXml(wordList, compose)

		#Send a POST request, with as body the xml
		self._openUrl("http://www.wrts.nl/api/lists", "POST", requestXml.createXml(), {"Content-Type": "application/xml"})

	def importWordList(self, url):
		"""Downloads a WRTS wordlist from URL and parses it into a WordList object. Throws LoginError/ConnectionError"""
		xmlStream = self._openUrl(url)
		wordListParser = WordListParser(self._parse, xmlStream)

		#return the wordList
		return wordListParser.list

	def _buildRequest(self, url, method, body, additionalHeaders):
		#If additionalHeaders not defined, they're set empty
		if not additionalHeaders:
			additionalHeaders = {}
		#Create a request object, lambda's so it's done lazily
		return {
			"HEAD": lambda: self.HeadRequest(url, headers=additionalHeaders),
			"GET": lambda: urllib2.Request(url, headers=additionalHeaders),
			"POST": lambda: urllib2.Request(url, body, additionalHeaders)
		}[method]()

	def _openUrl(self, url, method="GET", body=None, additionalHeaders=None, show404=False):
		"""Open an url, and return the response as a xml.dom.minidom.Document. Can raise a LoginError/ConnectionError"""

		request = self._buildRequest(url, method, body, additionalHeaders)

		#Send it
		try:
			response = self._opener.open(request)
		except urllib2.HTTPError, e:
			if show404 and e.code == 404:
				#if the user asks to get 404's, pass the error.
				raise
			if e.code == 401:
				#Not logged in
				self.loggedIn = False
				#Tell the user he/she isn't authorized.
				raise LoginError()
			else:
				#Unknown status (most likely an error): not logged in
				self.loggedIn = False

				#Show for debugging:
				traceback.print_exc()

				#But because it doesn't make sense to break the program for a WRTS error, show a nice error:
				raise ConnectionErrorError()
		except urllib2.URLError, e:
			#Something wrong with the connection
			self.loggedIn = False
			#show for debugging
			traceback.print_exc()
			#Show a nice error to the user.
			raise ConnectionError()

		#If no errors during request
		self.loggedIn = True

		if method == "HEAD":
			#HEAD never sends a body, so xml processing doesn't make sense.
			return

		return response

class ListsParser(object):
	"""This class parses a WRTS-API page: the lists-page. It can return the titles
	   of the lists as a python list with unicode strings, and it an get the url of the
	   corresponding wordList if you give the index of that title"""
	def __init__(self, xmlStream, *args, **kwargs):
		super(ListsParser, self).__init__(*args, **kwargs)

		self.root = ElementTree.parse(xmlStream).getroot()
		self.listsTree = self.root.findall(".//list")

	@property
	def lists(self):
		#Create a list to store the titles in.
		lists = []
		#Add titles to the earlier created list
		for listTree in self.listsTree:
			#Get the title (which can - too bad - be empty at WRTS)
			lists.append(listTree.findtext("title", u""))
		#Return the titles
		return lists

	def getWordListUrl(self, index):
		"""Gets the right node from the titleDom (selected by index),
		   gets the parentNode of it, which has an attribute 'href',
		   which is the needed url."""
		return self.listsTree[index].attrib["href"]

class WordListParser(object):
	"""This class parses a wordlist from the WRTS-API into a WordList-instance."""
	def __init__(self, parse, xmlStream, *args, **kwargs):
		super(WordListParser, self).__init__(*args, **kwargs)

		self._parse = parse
		self.root = ElementTree.parse(xmlStream).getroot()

	@property
	def list(self):
		#Create a new WordList instance
		wordList = {"items": []}

		#Read title, question subject and answer subject; sometimes the
		#element is empty, so the fallback u"" is needed.
		wordList["title"] = self.root.findtext("title", u"")
		wordList["questionLanguage"] = self.root.findtext("lang-a", u"")
		wordList["answerLanguage"] = self.root.findtext("lang-b", u"")

		#This counter is used to give each word a unique id
		counter = 0

		#Loop through the words in the xml
		for wordTree in self.root.findall("words/word"):
			#Create a Word-instance
			word = {}
			word["id"] = counter

			#Read the question, again keep in mind that null values are
			#possible, so again the u"" fallback. The question is parsed
			#by a wordsStringParser module.

			text = wordTree.findtext("word-a", u"")
			word["questions"] = self._parse(text)

			#Read the answer, again keep in mind that null values are
			#possible, so again the u"" fallback. The answer is parsed
			#by a wordsStringParser module.

			text = wordTree.findtext("word-b", u"")
			word["answers"] = self._parse(text)

			# Add the current edited word to the wordList instance
			wordList["items"].append(word)

			counter += 1

		#And finally, return the wordList
		return wordList
