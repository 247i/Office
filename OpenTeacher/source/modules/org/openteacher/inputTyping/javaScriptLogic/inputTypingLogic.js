/*
	Copyright 2013, Marten de Vries

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

/*global Event: false, compose: false, parse: false, check: false, _: false */
var InputTypingController;

InputTypingController = function () {
	"use strict";
	var AttributeError, ValueError, showingCorrection, installEvents,
		lessonType, lastWord, activity, enableUi, disableUi, onNewWord,
		assertLessonTypeSet, assertLessonActive,
		assertNotShowingCorrection, checkAnswerAndSaveResult,
		resultWrong, resultRight, tellLessonTypeAboutTheResult,
		lastResult, assertShowingCorrection, that;

	that = this;

	AttributeError = function (attr) {
		this.name = "AttributeError";
		this.message = "No such attribute: '" + attr + "'";
	};
	AttributeError.prototype = new Error();

	ValueError = function (msg) {
		this.name = "ValueError";
		this.message = msg;
	};
	ValueError.prototype = new Error();

	Object.defineProperty(this, "lessonType", {
		get: function () {
			return lessonType;
		},
		set: function (value) {
			try {
				lessonType.newItem.unhandle(onNewWord);
			} catch (error) {
				if (["KeyError", "TypeError"].indexOf(error.name) === -1) {
					throw error;
				}
			}
			if (showingCorrection) {
				that.correctionShowingDone();
			}
			lessonType = value;
			lessonType.newItem.handle(onNewWord);
			that.disableCorrectAnyway.send();
		}
	});

	installEvents = function () {
		that.clearInput = new Event();
		that.enableInput = new Event();
		that.disableInput = new Event();
		that.focusInput = new Event();

		that.showCorrection = new Event();
		that.hideCorrection = new Event();

		that.enableCheck = new Event();
		that.disableCheck = new Event();
		that.enableSkip = new Event();
		that.disableSkip = new Event();
		that.enableCorrectAnyway = new Event();
		that.disableCorrectAnyway = new Event();
	};

	onNewWord = function (word) {
		lastWord = word;

		activity = {start: new Date()};

		that.clearInput.send();
		that.focusInput.send();
	};

	enableUi = function () {
		that.enableCheck.send();
		that.enableSkip.send();
		that.enableInput.send();
	};

	disableUi = function () {
		that.disableCheck.send();
		that.disableSkip.send();
		that.disableInput.send();
	};

	this.checkTriggered = function (inputContent) {
		var result;

		assertLessonTypeSet();
		assertLessonActive();
		assertNotShowingCorrection();

		result = checkAnswerAndSaveResult(inputContent);
		if (result === "wrong") {
			resultWrong();
		} else {
			resultRight();
		}
	};

	assertLessonTypeSet = function () {
		if (typeof that.lessonType === "undefined") {
			throw new AttributeError("lessonType");
		}
	};

	assertLessonActive = function () {
		if (typeof lastWord === "undefined") {
			throw new ValueError("No lesson active");
		}
	};

	this.userIsTyping = function () {
		assertLessonTypeSet();
		assertLessonActive();
		assertNotShowingCorrection();

		activity.end = new Date();
	};

	resultWrong = function () {
		var correctAnswer;

		disableUi();
		that.enableCorrectAnyway.send();

		showingCorrection = true;
		correctAnswer = compose(lastWord.answers);
		that.showCorrection.send(correctAnswer);
	};

	resultRight = function () {
		that.disableCorrectAnyway.send();
		tellLessonTypeAboutTheResult();
	};

	checkAnswerAndSaveResult = function (userInput) {
		var givenAnswer;
		givenAnswer = parse(userInput);

		lastResult = check(givenAnswer, lastWord);
		lastResult.givenAnswer = userInput;
		return lastResult.result;
	};

	assertNotShowingCorrection = function () {
		if (showingCorrection) {
			throw new ValueError("Showing a correction -> calling this now makes no sense");
		}
	};

	tellLessonTypeAboutTheResult = function () {
		if (typeof activity.end === "undefined") {
			//assume now
			that.userIsTyping();
		}
		lastResult.active = activity;
		that.lessonType.setResult(lastResult);
	};

	this.correctionShowingDone = function () {
		assertShowingCorrection();
		showingCorrection = false;

		that.hideCorrection.send();
		tellLessonTypeAboutTheResult();
		enableUi();
	};

	assertShowingCorrection = function () {
		if (!showingCorrection) {
			throw new ValueError("Not showing a correction!");
		}
	};

	this.skipTriggered = function () {
		assertLessonTypeSet();
		assertLessonActive();
		assertNotShowingCorrection();

		that.lessonType.skip();
	};

	this.correctAnywayTriggered = function () {
		assertLessonTypeSet();
		assertLessonActive();

		if (showingCorrection) {
			that.correctionShowingDone();
		}
		lastResult.result = "right";
		lastResult.givenAnswer= _("Corrected: %s").replace("%s", lastResult.givenAnswer);

		that.lessonType.correctLastAnswer(lastResult);
		that.disableCorrectAnyway.send();
	};

	//setup object
	showingCorrection = false;
	installEvents();
};
