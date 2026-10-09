#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2012-2013, Marten de Vries
#	Copyright 2012, Milan Boers
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

#ATTENTION: fixmes/todos in this module won't be shown in the overview,
#since the word 'fixme' is used multiple times for other reasons.

from twisted.words.protocols import irc
from twisted.internet import protocol, reactor, ssl

from launchpadlib import launchpad
import re
import urllib2
import urllib

class OpenTeacherBot(irc.IRCClient):
	sessionKey = None
	
	factoids = {
		".downloads": "http://openteacher.org/download.html",
		".sf": "http://sourceforge.net/projects/openteacher",
		".stats": "http://sourceforge.net/projects/openteacher/files/stats",
		".lp": "https://launchpad.net/openteacher",
		".blueprints": "https://blueprints.launchpad.net/openteacher",
		".code": "https://code.launchpad.net/openteacher",
		".bugs": "https://bugs.launchpad.net/openteacher",
		".answers": "https://answers.launchpad.net/openteacher",
		".translations": "https://translations.launchpad.net/openteacher",
		".website": "http://openteacher.org/",
		".about": "http://openteacher.org/about.html",
		".documentation": "http://openteacher.org/documentation.html",
		".codedocs": "http://vps.marten-de-vries.nl/openteacher-code-documentation/",
		".contribute": "http://openteacher.org/contribute.html",
		".forum": "http://forum.ubuntu-nl.org/etalage/openteacher-overhoorprogramma-voor-linux/new/#new",
		".ogd": "http://opengamedesigner.org/",
		".ogd-lp": "https://launchpad.net/opengamedesigner",
		".twitter": "http://twitter.com/#!/openteacher",
		".facebook": "http://www.facebook.com/OpenTeacher",
		".hyves": "http://openteacher.hyves.nl/",
		".ohloh": "http://www.ohloh.net/p/openteacher",
		".mailarchive": "https://lists.launchpad.net/openteachermaintainers/",
		".paste": "http://paste.ubuntu.com/",
		".etherpad": "http://openetherpad.org/",
		".testsuite": "http://vps.marten-de-vries.nl/openteacher-test-suite-log.txt",
		".ogd-testsuite": "http://vps.marten-de-vries.nl/opengamedesigner-test-suite-log.txt",
		".jfl": "https://launchpad.net/justforlearning/",
		".jfl-demo": "http://vps.marten-de-vries.nl/justforlearning/",
		".ot-mobile": "http://web.openteacher.org/mobile/",
		".ot-test-coverage": "http://vps.marten-de-vries.nl/openteacher-test-coverage/",
		".ogd-test-coverage": "http://vps.marten-de-vries.nl/opengamedesigner-test-coverage/",
		".vps": "http://vps.marten-de-vries.nl/",
		".priorities": "http://vps.marten-de-vries.nl/openteacher-code-documentation/priorities.html",
		".fixmes": "http://vps.marten-de-vries.nl/openteacher-code-documentation/fixmes.html",
		".modulemap": "http://vps.marten-de-vries.nl/openteacher-code-documentation/module_graph.svg",
		".peps": "http://www.python.org/dev/peps/",
		".api": "http://web.openteacher.org/api/",
		".profiling-results": "http://vps.marten-de-vries.nl/openteacher-profiling-results/",
		".website-preview": "http://vps.marten-de-vries.nl/openteacher-website-preview/",
		".developer-documentation": "http://vps.marten-de-vries.nl/openteacher-code-documentation/dev_docs/",
		".code-complexity": "http://vps.marten-de-vries.nl/openteacher-code-complexity.txt",
		".dependencies": "http://vps.marten-de-vries.nl/openteacher-code-documentation/dev_docs/dependencies.rst",
		".bitesize": "https://bugs.launchpad.net/openteacher/+bugs?field.tag=bitesize"
	}
	factoids[".launchpad"] = factoids[".lp"]
	factoids[".download"] = factoids[".downloads"]
	factoids[".homepage"] = factoids[".website"]
	factoids[".codedocumentation"] = factoids[".codedocs"]
	factoids[".code-documentation"] = factoids[".codedocs"]
	factoids[".code-docs"] = factoids[".codedocs"]
	factoids[".forumtopic"] = factoids[".forum"]
	factoids[".mailinglist"] = factoids[".mailarchive"]
	factoids[".pastebin"] = factoids[".paste"]
	factoids[".test-suite"] = factoids[".testsuite"]
	factoids[".tests"] = factoids[".testsuite"]
	factoids[".ogd-test-suite"] = factoids[".ogd-testsuite"]
	factoids[".ogd-tests"] = factoids[".ogd-testsuite"]
	factoids[".openteacher-mobile"] = factoids[".ot-mobile"]
	factoids[".mobile"] = factoids[".ot-mobile"]
	factoids[".ot-coverage"] = factoids[".ot-test-coverage"]
	factoids[".ogd-coverage"] = factoids[".ogd-test-coverage"]
	factoids[".coverage"] = factoids[".ot-test-coverage"]
	factoids[".fixme"] = factoids[".fixmes"]
	factoids[".todos"] = factoids[".fixmes"]
	factoids[".todo"] = factoids[".fixmes"]
	factoids[".priority"] = factoids[".priorities"]
	factoids[".module-map"] = factoids[".modulemap"]
	factoids[".modulegraph"] = factoids[".modulemap"]
	factoids[".module-graph"] = factoids[".modulemap"]
	factoids[".profile"] = factoids[".profiling-results"]
	factoids[".profiling"] = factoids[".profiling-results"]
	factoids[".cProfile"] = factoids[".profiling-results"]
	factoids[".performance"] = factoids[".profiling-results"]
	factoids[".website-dev"] = factoids[".website-preview"]
	factoids[".dev-docs"] = factoids[".developer-documentation"]
	factoids[".devdocs"] = factoids[".developer-documentation"]
	factoids[".developer-docs"] = factoids[".developer-documentation"]
	factoids[".dev-documentation"] = factoids[".developer-documentation"]
	factoids[".wiki"] = factoids[".developer-documentation"]
	factoids[".complexity"] = factoids[".code-complexity"]
	factoids[".cyclomatic-complexity"] = factoids[".code-complexity"]
	factoids[".mccabe"] = factoids[".code-complexity"]
	factoids[".requirements"] = factoids[".dependencies"]
	factoids[".simplebugs"] = factoids[".bitesize"]
	factoids[".bitesizebugs"] = factoids[".bitesize"]

	@property
	def nickname(self):
		return self.factory.nickname

	@property
	def password(self):
		return self.factory.password

	@property
	def realname(self):
		return self.factory.realname

	def signedOn(self):
		print "Signed on. Now getting key and joining channels."
		
		self._setSessionKey()
		
		for channel in self.factory.channels:
			self.join(channel)

	def joined(self, channel):
		print "Joined %s." % (channel,)

	def _setSessionKey(self):
		# Get a session key from appspot
		shellSite = urllib2.urlopen("http://shell.appspot.com/")
		
		regex = re.compile(r'<input type="hidden" name="session" value="(.*)" />')

		for line in shellSite:
			m = regex.search(line)
			if m != None:
				self.sessionKey = m.group(1)
				return True
		return False

	def _buildBugResponse(self, msg, user):
		#bugs
		match = re.search("(?:bugs? ?/?|#|lp:)([0-9]+)", msg)
		if match:
			number = match.group(1)
			bug = self.factory.launchpad.bugs[number]
			if bug:
				try:
					task = bug.bug_tasks[0] #should not crash, but to be sure
				except IndexError:
					pass
				else:
					return "bug #%s: %s (status: %s, importance: %s) - %s" % (
						bug.id,
						bug.title,
						task.status,
						task.importance,
						bug.web_link
					)

	def _buildBranchResponse(self, msg, user):
		#branches
		match = re.search("lp:[^ ]*(?=[^,.?!])[^ ]", msg)
		if match:
			branch = self.factory.launchpad.branches.getByUrl(url=match.group(0))
			if branch:
				text = "branch %s (status: %s, %s revisions) - %s" % (
					branch.bzr_identity,
					branch.lifecycle_status,
					branch.revision_count,
					branch.web_link,
				)
				return text

	def _buildPyModResponse(self, msg, user):
		if msg.startswith(".pymod "):
			mod = msg.split(" ")[1]
			url = u"http://docs.python.org/library/%s.html" % mod
			try:
				urllib2.urlopen(url)
			except urllib2.HTTPError:
				return u"Can't find documentation for that module."
			else:
				return url

	def _buildGoogleResponse(self, msg, user):
		if msg.startswith(".google "):
			q = msg.split(" ", 1)[1]
			q = urllib.quote_plus(q)
			return u"http://google.com/search?q=%s" % q

	def _buildQtResponse(self, msg, user):
		if msg.startswith(".qt "):
			cls = msg.split(" ")[1]
			url = u"http://qt-project.org/doc/qt-4.8/%s.html" % cls
			try:
				urllib2.urlopen(url)
			except urllib2.HTTPError:
				return u"Can't find documentation for that class."
			else:
				return url

	def _buildAnswerResponse(self, msg, user):
		if msg.startswith(".answer ") or msg.startswith(".ask ") or msg.startswith(".question "):
			q = msg.split(" ", 1)[1].replace(self.nickname, "")
			q = urllib.quote_plus(q)
			return u"http://www.wolframalpha.com/input/?i=%s" % q

	def _buildPythonResponse(self, msg, user):
		#python evaluation
		if msg.startswith(".py "):
			statement = msg[4:]

			data = urllib.urlencode({
				"statement": statement,
				"session": self.sessionKey,
			})
			data = unicode(urllib2.urlopen("http://shell.appspot.com/shell.do?" + data).read(), encoding="UTF-8")
			result = data.strip().split("\n")[-1]
			if len(result) > 350:
				result = result[len(result) - 350:]
			return result

	def _buildPythonResetResponse(self, msg, user):
		#reset python shell
		if msg == ".reset" and user in self.factory.admins:
			if self._setSessionKey():
				return u"I've been reset."
			else:
				return u"Could not reset. Is appspot down?"

	def _buildPepResponse(self, msg, user):
		if msg.startswith(".pep "):
			try:
				number = int(msg.split(" ", 1)[1].replace(self.nickname, ""))
			except ValueError:
				return u"Couldn't parse pep number."
			else:
				url = u"http://www.python.org/dev/peps/pep-%04d/" % number
				try:
					urllib2.urlopen(url)
				except urllib2.HTTPError:
					return u"No pep found for that number."
				else:
					return url

	def _buildQuitResponse(self, msg, user):
		#quit client
		if msg == ".quit" and user in self.factory.admins:
			self.factory.timeToQuit = True
			self.quit()

	def _buildBlueprintResponse(self, msg, user):
		#blueprints
		match = re.search("(?:specs?[ /]+|blueprints? )([^ ,.?!/]+)", msg)
		if match:
			spec = self.factory.launchpad.projects["openteacher"].getSpecification(name=match.group(1))
			if spec:
				return u"blueprint %s: %s (def. status: %s, impl. status: %s, priority: %s) - %s" % (
					spec.name,
					spec.title,
					spec.definition_status,
					spec.implementation_status,
					spec.priority,
					spec.web_link,
				)

	def _buildFactoidResponse(self, msg, user):
		#factoids
		#sorted on key so the longest factoid keys are tried first.
		#Needed in this situation: .codedocumentation while there's a
		#factoid .code.
		for key, factoid in reversed(sorted(self.factoids.iteritems(), key=lambda t: len(t[0]))):
			if key in msg:
				return factoid

	def privmsg(self, user, channel, msg):
		print "%s: %s: %s" % (user.split("!")[0], channel, msg)
		target = channel if channel in self.factory.channels else user.split("!")[0]

		builders = [
			self._buildAnswerResponse,
			self._buildBlueprintResponse,
			self._buildBranchResponse,
			self._buildBugResponse,
			self._buildFactoidResponse,
			self._buildGoogleResponse,
			self._buildPepResponse,
			self._buildPyModResponse,
			self._buildPythonResetResponse,
			self._buildPythonResponse,
			self._buildQtResponse,
			self._buildQuitResponse,
		]

		for buildResponse in builders:
			resp = buildResponse(msg, user)
			if resp is not None:
				#found a message
				break
		else:
			#no message found
			return

		#send the message
		self.msg(target, resp.encode("UTF-8"))

class OpenTeacherBotFactory(protocol.ClientFactory):
	protocol = OpenTeacherBot

	def __init__(self, channels, nickname, realname, password, admins):
		self.channels = channels
		self.nickname = nickname
		self.realname = realname
		self.password = password
		self.admins = admins

		self.timeToQuit = False

		self.launchpad = launchpad.Launchpad.login_anonymously("OpenTeacher bot", "production", "~/.config/launchpadlib", version="devel")

	def clientConnectionLost(self, connector, reason):
		if not self.timeToQuit:
			print "Lost connection: %s. Trying to reconnect." % (reason,)
			connector.connect()

	def clientConnectionFailed(self, connector, reason):
		print "Connection failed: %s, Trying to reconnect." % (reason,)
		connector.connect()

def run():
	print """For a nice quit, first tell the bot to .quit
on irc. Then press ctrl+c here.\n"""

	config = {
		"channels": [
			"##PyTest",
		],
		"nickname": "OTbot-dev",
		"realname": "http://openteacher.org/",
		"password": None,
		"admins": [
			"CasW!~cas@unaffiliated/casw",
			"commandoline!~commandol@ubuntu/member/commandoline",
			"lordnoid!~lordnoid@53537359.cm-6-4b.dynamic.ziggo.nl",
		]
	}
	reactor.connectSSL('irc.freenode.net', 7000, OpenTeacherBotFactory(**config), ssl.ClientContextFactory())
	reactor.run()

if __name__ == "__main__":
	run()
