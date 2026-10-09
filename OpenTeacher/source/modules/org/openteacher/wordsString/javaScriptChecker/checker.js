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

var check = (function () {
	"use strict";
	var calculateDifference, arrayValuesEqual,
		checkSingleCompulsoryAnswerGiven,
		checkMultipleCompulsoryAnswersGiven;

	calculateDifference = function (a1, a2) {
		return a1.filter(function (item) {
			return a2.indexOf(item) === -1;
		});
	};

	arrayValuesEqual = function (a1, a2) {
		var i, index;

		//copy, it's going to be modified
		a1 = a1.slice();

		for (i = 0; i < a2.length; i += 1) {
			index = a1.indexOf(a2[i]);
			if (index === -1) {
				return false;
			}
			a1.splice(index, 1);
		}
		return a1.length === 0;
	};

	checkSingleCompulsoryAnswerGiven = function (givenAnswer, word) {
		var result, difference, compulsoryAnswer, oldDifference, i;

		result = {"result": "right"};
		difference = givenAnswer[0];
		for (i = 0; i < word.answers.length; i += 1) {
			compulsoryAnswer = word.answers[i];

			oldDifference = difference;
			difference = calculateDifference(difference, compulsoryAnswer);
			if (arrayValuesEqual(oldDifference, difference)) {
				result = {"result": "wrong"};
				break;
			}
		}
		if (result.result === "right" && difference.length !== 0) {
			result = {"result": "wrong"};
		}
		return result;
	};

	checkMultipleCompulsoryAnswersGiven = function (givenAnswer, word) {
		var result, compulsoryAnswerCount, compulsoryGivenAnswer, difference, i, j, compulsoryAnswer;

		result = {"result": "wrong"};
		compulsoryAnswerCount = 0;

		for (i = 0; i < givenAnswer.length; i += 1) {
			compulsoryGivenAnswer = givenAnswer[i];

			for (j = 0; j < word.answers.length; j += 1) {
				compulsoryAnswer = word.answers[j];

				difference = calculateDifference(compulsoryGivenAnswer, compulsoryAnswer);
				if (difference.length === 0) {
					compulsoryAnswerCount += 1;
				}
			}
		}
		if (compulsoryAnswerCount === word.answers.length) {
			result = {"result": "right"};
		}
		return result;
	};

	return function (givenAnswer, word) {
		var result;

		if (givenAnswer.length === 1) {
			result = checkSingleCompulsoryAnswerGiven(givenAnswer, word);
		} else {
			result = checkMultipleCompulsoryAnswersGiven(givenAnswer, word);
		}

		result.itemId = word.id;
		return result;
	};
}());
