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

import subprocess
import os
import collections
import re

ComplexityResult = collections.namedtuple("ComplexityResult", "position complexity")

def pythonPaths(basePath):
	for root, dir, files in os.walk(basePath):
		for file in files:
			isNotAPythonFile = not file.endswith(".py")
			shouldNotBeChecked = (
				isNotAPythonFile or
				"pyinstaller" in root or
				"admin_files" in root or
				"pyttsx" in root or
				"collectionscompat.py" in file or
				"pyratemp" in file
			)
			if shouldNotBeChecked:
				continue
			yield os.path.join(root, file)

def complexityInfo(output):
	for line in output.split("\n"):
		if not line:
			continue
		result = ComplexityResult._make(eval(line))
		if not re.search(r"install.*Classes", result.position):
			yield result

def complexityForPaths(basePath):
	for path in pythonPaths(basePath):
		output = subprocess.check_output(["python", "-m", "mccabe", "--min=9", path]).strip()
		info = list(complexityInfo(output))
		if info:
			yield path, info

def main(basePath):
	def highestComplexity((path, results)):
		return max(r.complexity for r in results)

	for path, results in reversed(sorted(complexityForPaths(basePath), key=highestComplexity)):
		print path
		for result in reversed(sorted(results, key=lambda r: r.complexity)):
			print "Complexity:", result.complexity, "Position:", result.position
		print ""
