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

/* global $: false, logic: false */

var enterTab;

enterTab = (function () {
	"use strict";
	var closePopup, newText;

	closePopup = function () {
		$("#missing-separator-popup").popup("close");
	};

	return {
		newList: function () {
			//keyup so jqm adjusts the textarea size.
			$("#list-textarea").val(newText).keyup();
		},
		setupUi: function () {
			$("#list-textarea").tabOverride();
			$("#missing-separator-ok-button").click(closePopup);
		},
		retranslate: function (_) {
			$("#enter-list-header").text(_("Enter list"));
			$("#word-list-label").text(_("Word list:"));
			newText = _("Welcome = Welkom\nto = bij\nOpenTeacher mobile = OpenTeacher mobile\n");

			$("#missing-separator-header").text(_("Error"));
			$("#missing-separator-title").text(_("Missing equals sign or tab"));
			$("#missing-separator-msg").text(_("Please make sure every line contains an '='-sign or tab between the questions and answers."));
			$("#missing-separator-ok-button").text(_("Ok"));
		},
		fromLesson: function (lesson) {
			var text;

			text = logic.composeList(lesson);
			$("#list-textarea").val(text);
		},
		toLesson: function () {
			var text, lesson;

			text = $("#list-textarea").val();

			try {
				lesson = logic.parseList(text);
			} catch (exc) {
				if (exc.name === "SeparatorError") {
					$("#missing-separator-popup").popup("open");
					return false;
				}
				throw exc;
			}
			return lesson;
		}
	};
}());
