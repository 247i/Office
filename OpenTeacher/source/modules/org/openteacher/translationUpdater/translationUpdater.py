#! /usr/bin/env python
# -*- coding: utf-8 -*-

#	Copyright 2012, Marten de Vries
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
import glob
import subprocess

class TranslationUpdaterModule(object):
	def __init__(self, moduleManager, *args, **kwargs):
		super(TranslationUpdaterModule, self).__init__(*args, **kwargs)
		self._mm = moduleManager

		self.type = "translation-updater"

		self.priorities = {
			"update-translations": 0,
			"default": -1,
		}
		self.requires = (
			self._mm.mods(type="metadata"),
			self._mm.mods(type="execute"),
		)

	def _run(self):
		#save the cwd for later use
		startdir = os.getcwd()

		for m in self._mm.mods:
			#generate some handy vars
			path = os.path.dirname(m.__class__.__file__)
			tpath = os.path.join(path, "translations")

			#check if all the requirements for automatic translation
			#updates are there, and read the values of these
			#requirements (filename & var value). Otherwise continue.
			hasTranslations = os.path.isdir(tpath)
			if not hasTranslations:
				continue
			try:
				potpath = glob.glob(os.path.join(tpath, "*.pot")).pop()
			except IndexError:
				continue
			try:
				files = m.filesWithTranslations
			except AttributeError:
				print "WARNING: %s doesn't specify files to translate. Passing over." % path
				continue
			#adjust potpath to be relative to 'path'
			potname = os.path.basename(potpath)
			newpotpath = os.path.join("translations", potname)
			#change cwd to path
			os.chdir(path)
			#generate the xgettext comment, that extracts strings from
			#source code.
			cmd = "xgettext --keyword=tr --force-po --add-comments=TRANSLATORS --from-code=UTF-8 --language=Python --package-name=%s --package-version=%s --msgid-bugs-address=%s --output=%s %s" % (
				self._metadata["name"],
				self._metadata["version"],
				self._metadata["email"],
				newpotpath,
				" ".join(files)
			)
			subprocess.check_call(cmd.split(" "))

			nulldevice = open(os.devnull, "w")
			for pofile in glob.glob(os.path.join("translations", "*.po")):
				#Update all .po files
				cmd = "msgmerge --update %s %s" % (pofile, newpotpath)
				subprocess.check_call(cmd.split(" "), stderr=nulldevice)
				mofile = os.path.splitext(pofile)[0] + ".mo"
				#Update all .mo files
				cmd = "msgfmt --output %s %s" % (mofile, pofile)
				subprocess.check_call(cmd.split(" "))
			#reset for the next round/last time, since the module
			#manager and this module depend on the startdir as
			#reference location.
			os.chdir(startdir)

			print "Updated translations of: %s" % path

	def enable(self):
		self._modules = set(self._mm.mods(type="modules")).pop()
		self._metadata = self._modules.default("active", type="metadata").metadata

		self._execute = self._modules.default(type="execute")
		self._execute.startRunning.handle(self._run)

		self.active = True

	def disable(self):
		self.active = False
		del self._modules
		del self._metadata
		del self._execute

def init(moduleManager):
	return TranslationUpdaterModule(moduleManager)
