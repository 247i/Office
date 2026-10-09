/*
	Copyright 2012, Marten de Vries

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

var parse = (function () {
	"use strict";
	var obligatoryRe, wordRe, reverseAndTrim, isEmpty;

	obligatoryRe = new RegExp(" \\.[0-9]+(?!\\\\)");
	wordRe = new RegExp("[,;](?!\\\\)");

	reverseAndTrim = function (i) {
		//reverse all words (the characters) back and trim them
		return i.split("").reverse().join("").trim();
	};

	isEmpty = function (i) {
		//remove empty words
		return i;
	};

	return function (text) {
		var obligatoryElements, result, i, obligatoryElement, words;

		//so we don't need negative lookback assertions :).
		text = text.split("").reverse().join("");

		obligatoryElements = text.split(obligatoryRe);
		//reverse order, reversing the text itself happens later on.
		obligatoryElements.reverse();

		result = [];
		for (i = 0; i < obligatoryElements.length; i += 1) {
			obligatoryElement = obligatoryElements[i];

			//split words
			words = obligatoryElement.split(wordRe);

			words = words.map(reverseAndTrim);
			words = words.filter(isEmpty);
			//revert the last unreversed thing: the order of the words
			words = words.reverse();

			if (words.length !== 0) {
				//add if non-empty
				result.push(words);
			}
		}

		return result;
	};
}());
