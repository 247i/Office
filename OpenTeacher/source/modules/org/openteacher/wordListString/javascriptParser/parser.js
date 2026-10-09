/*
	Copyright 2012-2013, Marten de Vries

	This file is part of OpenTeacher.

	OpenTeacher is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	OpenTeacher is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with OpenTeacher.  If not, see <http://www.gnu.org/licenses/>.
*/

/*global parse: false */

var parseList = (function() {
	"use strict";

	var SeparatorError, re, splitLine, parseLine;

	SeparatorError = function (message) {
		this.name = "SeparatorError";
		this.message = message;
	};
	SeparatorError.prototype = new Error();
	SeparatorError.prototype.constructor = SeparatorError;

	//the '\\\\' part matches exactly 1 '\' due to both JS and regex
	//escaping...
	re = new RegExp("[^\\\\][=\t]");

	splitLine = function (line) {
		var firstOccurenceIndex;

		if (["\t", "="].indexOf(line[0]) !== -1) {
			//if first character is \t or =, run special logic because
			//the regex handler down here can't cope with that.
			return {
				questionText: "",
				answerText: line.slice(1)
			};
		} else {
			firstOccurenceIndex = line.search(re);
			if (firstOccurenceIndex === -1) {
				throw new SeparatorError("Missing equals sign or tab");
			}
			return {
				questionText: line.slice(0, firstOccurenceIndex + 1),
				answerText: line.slice(firstOccurenceIndex + 2)
			};
		}
	};

	parseLine = function (line, id, createdDate) {
		var splittedLine;

		if (line.trim() === "") {
			return;
		}

		splittedLine = splitLine(line);

		return {
			id: id,
			created: createdDate,
			questions: parse(splittedLine.questionText),
			answers: parse(splittedLine.answerText)
		};
	};

	var parseList = function (string, parseLenient) {
		var list, now, counter, lines, i, word;

		list = {
			items: [],
			tests: []
		};
		now = new Date();
		counter = 0;

		lines = string.split("\n");
		for (i = 0; i < lines.length; i += 1) {
			try {
				word = parseLine(lines[i], counter, now);
			} catch (e) {
				if (parseLenient) {
					continue;
				} else {
					throw e;
				}
			}
			if (word) {
				list.items.push(word);
				counter += 1;
			}
		}
		return {
			"resources": {},
			"list": list
		};
	};

	return parseList;
}());
