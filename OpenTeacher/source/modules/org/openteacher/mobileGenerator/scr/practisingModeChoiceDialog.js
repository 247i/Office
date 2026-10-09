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

/* global $: false, optionsDialog: false, gui: false */

var practisingModeChoiceDialog;

practisingModeChoiceDialog = (function () {
	"use strict";
	var onTypeAnswer, onThinkAnswer, setSetting;

	setSetting = function (mode) {
		localStorage.practisingMode = mode;
		optionsDialog.updatePractisingMode();
		gui.startLesson();
	};

	onThinkAnswer = function () {
		setSetting("think-answer");
	};

	onTypeAnswer = function () {
		setSetting("type-answer");
	};

	return {
		retranslate: function (_) {
			$("#practising-mode-choice-header").text(_("Practising mode choice"));
			$("#practising-mode-choice-label").text(_("Please choose the practising mode you want to use:"));
			$("#think-answer-button").text(_("Think answer"));
			$("#type-answer-button").text(_("Type answer"));
			$("#practising-mode-choice-explanation").text(_("If you ever want to change your choice, you can do so in the options dialog, which is accessable by clicking 'Menu' and then 'Options'."));
		},
		setupUi: function () {
			$("#think-answer-button").click(onThinkAnswer);
			$("#type-answer-button").click(onTypeAnswer);
		}
	};
}());
