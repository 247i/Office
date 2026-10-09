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

/* global translationIndex: false, $: false, gui: false */

var optionsDialog;

optionsDialog = (function () {
	"use strict";

	var getLanguage, languageChanged, practisingModeChanged,
		updatePractisingMode;

	getLanguage = function () {
		if (typeof localStorage.language === "undefined") {
			//first time running
			if (translationIndex.hasOwnProperty(navigator.language)) {
				//first try the exact browser locale
				localStorage.language = navigator.language;
			} else if (translationIndex.hasOwnProperty(navigator.language.split("-")[0])) {
				//then the generic one
				localStorage.language = navigator.language.split("-")[0];
			} else {
				//if all else fails...
				localStorage.language = "en";
			}
		}
		return translationIndex[localStorage.language];
	};

	languageChanged = function () {
		localStorage.language = $("option:selected", this).val();
		gui.retranslate();
	};

	practisingModeChanged = function () {
		localStorage.practisingMode = $("option:selected", this).val();
	};

	updatePractisingMode = function () {
		if (typeof localStorage.practisingMode !== "undefined") {
			$("#practising-mode-select").val(localStorage.practisingMode);
		}
	};

	return {
		setupSettings: function () {
			var langCode, select;

			//language
			select = $("#language-select");

			//fill combobox
			for (langCode in translationIndex) {
				if (translationIndex.hasOwnProperty(langCode)) {
					select.append("<option value='" + langCode + "'>" + translationIndex[langCode].name + "</option>");
				}
			}

			//set current value
			//this makes sure localStorage.language is set
			getLanguage();
			//this sets the value.
			select.val(localStorage.language);

			//register handler
			select.change(languageChanged);

			//practising mode
			//set current value
			updatePractisingMode();
			//register handler
			$("#practising-mode-select").change(practisingModeChanged);
		},
		updatePractisingMode: updatePractisingMode,
		retranslate: function (_) {
			$("#options-header").text(_("Options"));
			$("#language-select-label").text(_("Language:"));

			$("#practising-mode-select-label").text(_("Practising mode:"));
			$("#think-answer-option").text(_("Think answer"));
			$("#type-answer-option").text(_("Type answer"));

			$("#copyright-info-link").text(_("Copyright info"));
		},
		getLanguage: getLanguage
	};
}());
