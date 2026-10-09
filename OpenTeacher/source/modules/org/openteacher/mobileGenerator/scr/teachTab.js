/*
	Copyright 2012-2013, Marten de Vries
	Copyright 2012, Milan Boers

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

/* global $: false, JsDiff: false, logic: false */

var teachTab;

teachTab = (function () {
	"use strict";

	var lessonDone, newItem, sliderToProgressBar, lessonType,
		currentItem, calculateNote,	noteMessage, backToEnterTab,
		onViewAnswer, onRight, onWrong, focusAtNewItem,
		showCorrection, hideCorrection, controller;

	showCorrection = function (correction) {
		var correctionLabel, answerBox, diff, diffText, i;

		correctionLabel = $("#correction-label");
		answerBox = $("#answer-box");

		diff = JsDiff.diffChars(answerBox.val(), correction);
		if (diff.length > 4) {
			//differs too much
			correctionLabel.html(correction);
		} else {
			//diff is close enough, show it.
			diffText = "";
			for (i = 0; i < diff.length; i += 1) {
				if (diff[i].added) {
					diffText += "<span style='color: green; text-decoration: underline;'>" + diff[i].value + "</span>";
				} else if (diff[i].removed) {
					diffText += "<span style='color: red; text-decoration: underline;'>" + diff[i].value + "</span>";
				} else {
					diffText += diff[i].value;
				}
			}
			correctionLabel.html(diffText);
		}
		answerBox.hide();
		correctionLabel.show().fadeOut(4000, function () {
			controller.correctionShowingDone();
		});
	};

	hideCorrection = function () {
		$("#correction-label").stop().hide();
		$("#answer-box").show();
	};

	calculateNote = function (test) {
		var good, total, i, result;

		good = 0;
		total = test.results.length;
		for (i = 0; i < test.results.length; i += 1) {
			result = test.results[i];
			if (result.result === "right") {
				good += 1;
			}
		}
		return Math.round(good / total * 100).toString() + "%";
	};

	lessonDone = function () {
		var test, note;

		test = lessonType.list.tests[lessonType.list.tests.length - 1];
		note = calculateNote(test);

		//free lesson objects
		lessonType = undefined;
		currentItem = undefined;

		//show results
		$("#result-msg").text(noteMessage.replace("%s", note));
		$.mobile.changePage($("#result-dialog"));
	};

	focusAtNewItem = function () {
		//focus to input box/the button when jqm is fully set up.
		window.setTimeout(function () {
			if (localStorage.practisingMode === "type-answer") {
				$("#answer-box").focus();
			} else {
				$("#view-answer-button").focus();
			}
		}, 0);
	};

	newItem = function (item) {
		var slider;

		currentItem = item;

		//set question
		$("#question-label").text(logic.compose(item.questions));

		//show/hide the right 'think answer'-controls
		$("#thinking-controls").show();
		$("#answering-controls").hide();

		//update progress bar
		slider = $("#progress-bar");
		slider.attr("max", lessonType.totalItems);
		slider.val(lessonType.askedItems);
		try {
			slider.slider("refresh");
		} catch (e) {}
	};

	sliderToProgressBar = function () {
		//It's a hack. But it works. Brilliantly.
		$("#progress-bar")
			.hide()

			.siblings(".ui-slider")
			.css("margin", 6)
			.width("99%")
			.off("vmousedown")

			.children(".ui-slider-handle")
			.hide()

			.siblings(".ui-slider-bg")
			.css("cursor", "auto");
	};

	backToEnterTab = function () {
		$.mobile.changePage($("#enter-page"));
	};
	$(document).on("pageinit", sliderToProgressBar);

	onViewAnswer = function () {
		var answers;

		answers = logic.compose(currentItem.answers);
		$("#translation-label").text(answers);

		$("#thinking-controls").hide();
		$("#answering-controls").show();
	};

	onRight = function () {
		lessonType.setResult({"result": "right"});
	};

	onWrong = function () {
		lessonType.setResult({"result": "wrong"});
	};

	return {
		setupUi: function () {
			var checkAnswer;
			controller = new logic.InputTypingController();

			//bind to controller events
			controller.clearInput.handle(function () {
				$("#answer-box").val("");
			});
			controller.enableInput.handle(function () {
				$("#answer-box").textinput("enable");
			});
			controller.disableInput.handle(function () {
				$("#answer-box").textinput("disable");
			});
			controller.focusInput.handle(function () {
				//we might need to focus the 'show answer'-button
				//instead.
				focusAtNewItem();
			});

			controller.showCorrection.handle(showCorrection);
			controller.hideCorrection.handle(hideCorrection);

			controller.enableCheck.handle(function () {
				$("#check-button").button("enable");
			});
			controller.disableCheck.handle(function () {
				$("#check-button").button("disable");
			});
			controller.enableSkip.handle(function () {
				$(".skip-button").button("enable");
			});
			controller.disableSkip.handle(function () {
				$(".skip-button").button("disable");
			});
			controller.enableCorrectAnyway.handle(function () {
				$("#correct-anyway-button").button("enable");
			});
			controller.disableCorrectAnyway.handle(function () {
				$("#correct-anyway-button").button("disable");
			});

			//make sure user actions are sent to the controller
			checkAnswer = function () {
				controller.checkTriggered($("#answer-box").val());
			};
			$("#check-button").click(checkAnswer);
			$("#teach-page").keydown(function (event) {
				if (event.which === 13) {
					//enter key
					if (localStorage.practisingMode === "type-answer") {
						checkAnswer();
					} else {
						$("#view-answer-button").click();
					}
				}
			});
			$("#correct-anyway-button").click(controller.correctAnywayTriggered);
			$(".skip-button").click(controller.skipTriggered);
			$("#answer-box").change(controller.userIsTyping);

			$("#view-answer-button").click(onViewAnswer);
			$("#i-was-right-button").click(onRight);
			$("#i-was-wrong-button").click(onWrong);

			$("#result-ok-button").click(backToEnterTab);
		},

		retranslate: function (_) {
			//ui itself
			$("#teach-me-header").text(_("Teach me!"));
			$("#question-label-label").text(_("Question:"));
			$("#answer-box-label").text(_("Answer:"));
			$("#check-button").text(_("Check!"));
			$(".skip-button").text(_("Skip"));
			$("#correct-anyway-button").text(_("Correct anyway"));
			$("#think-answer-explanation").text(_("Think about the answer, and press the 'View answer' button when you're done."));
			$("#view-answer-button").text(_("View answer"));
			$("#translation-label-label").text(_("Translation:"));
			$("#i-was-right-button").text(_("I was right"));
			$("#i-was-wrong-button").text(_("I was wrong"));

			//result popup
			$("#result-header").text(_("Test completed!"));
			$("#result-title").text(_("Test completed!"));
			$("#result-ok-button").text(_("Ok"));
			noteMessage = _("Your note: %s");
		},

		doLesson: function (lesson) {
			var i, indexes;

			if (typeof localStorage.practisingMode === "undefined") {
				$.mobile.changePage("#practising-mode-choice-dialog");
				return;
			}

			indexes = [];
			for (i = 0; i < lesson.list.items.length; i += 1) {
				indexes.push(i);
			}

			lessonType = new logic.LessonType(lesson.list, indexes);
			lessonType.newItem.handle(newItem);
			lessonType.lessonDone.handle(lessonDone);
			controller.lessonType = lessonType;
			lessonType.start();

			if (localStorage.practisingMode === "type-answer") {
				$("#think-answer-practising-mode").hide();
				$("#type-answer-practising-mode").show();
			} else {
				$("#think-answer-practising-mode").show();
				$("#type-answer-practising-mode").hide();
			}
		}
	};
}());
