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

/* global $: false, enterTab: false, teachTab: false, menuDialog: false,
          optionsDialog: false, copyrightInfoDialog: false,
          practisingModeChoiceDialog: false
*/

var gui, _;

gui = (function () {
	"use strict";
	var setupDone, main, doRetranslate, retranslate, startLesson,
		onDeviceReady, onMenuKeyDown;

	setupDone = false;

	doRetranslate = function (_) {
		//header menu
		//.ui-btn-text because it seems close to impossible to
		//refresh a button based on a <a>-tag...
		$(".menu-dialog-link .ui-btn-text").text(_("Menu"));

		//tabs
		$(".enter-page-link .ui-btn-text").text(_("Enter list"));
		$(".teach-page-link .ui-btn-text").text(_("Teach me!"));

		//retranslate all tabs & dialogs
		enterTab.retranslate(_);
		teachTab.retranslate(_);
		menuDialog.retranslate(_);
		optionsDialog.retranslate(_);
		copyrightInfoDialog.retranslate(_);
		practisingModeChoiceDialog.retranslate(_);

		try {
			$("button").button("refresh");
		} catch (e) {
			$("button").button();
		}
	};

	retranslate = function (callback) {
		if (typeof optionsDialog.getLanguage().url === "undefined") {
			//english, use a simple pass through function.
			_ = function (str) {
				return str;
			};
			doRetranslate(_);
			if (callback) {
				callback();
			}
		} else {
			//download the translation file
			$.get(optionsDialog.getLanguage().url, function (translations) {
				//use it for translating the ui.
				_ = function (str) {
					return translations[str] || str;
				};
				doRetranslate(_);
				if (callback) {
					callback();
				}
			});
		}
	};

	onDeviceReady = function () {
		//Connect buttons to functions
		$(document).on("menubutton", onMenuKeyDown);
	};

	onMenuKeyDown = function () {
		//Make the menu button on Android work
		$.mobile.changePage("#menu-dialog", "pop", false, true);
	};

	main = function () {
		//translate the GUI for the first time. Delay the other set
		//up things until that's done, because they might depend
		//on the translations.
		retranslate(function () {
			if (!setupDone) {
				//setup UI
				enterTab.setupUi();
				teachTab.setupUi();
				menuDialog.setupUi();
				copyrightInfoDialog.setupUi();
				practisingModeChoiceDialog.setupUi();

				//start with a new word list
				enterTab.newList();

				//make sure the options dialog is ready to be shown
				optionsDialog.setupSettings();

				//handle tab switching.
				$(".teach-page-link").click(startLesson);

				//this part of main() is supposed to only run once.
				setupDone = true;
			}
		});
	};

	startLesson = function () {
		var lesson;

		lesson = enterTab.toLesson();
		if (!lesson) {
			return false;
		}

		if (typeof localStorage.practisingMode === "undefined") {
			$.mobile.changePage("#practising-mode-choice-dialog");
		} else {
			$.mobile.changePage("#teach-page", {"transition": "none"});
			teachTab.doLesson(lesson);
		}

		//don't allow to follow the link the normal way, which
		//reloads the page.
		return false;
	};

	//setup for a local environment
	$.ajaxSetup({
		beforeSend: function (xhr) {
			if (xhr.overrideMimeType) {
				xhr.overrideMimeType("application/json");
			}
		}
	});

	/* OS matching themes */
	(function () {
		var ua, isIos, isAndroid;

		ua = navigator.userAgent.toLowerCase();
		isIos = !(ua.indexOf("ipod") === -1 && ua.indexOf("iphone") === -1 && ua.indexOf("ipad") === -1);
		isAndroid = ua.indexOf("android") !== -1;

		if (isIos) {
			//page transition
			$(document).on("mobileinit", function () {
				$.mobile.defaultPageTransition = "slide";
			});
			//add css
			$(function () {
				$("head").append("<link type='text/css' rel='stylesheet' href='css/themes/ios/styles.css' />");
			});
		}
		if (isAndroid) {
			//change default swatch to something looking good
			//in android
			$.mobile.page.prototype.options.contentTheme = "d";

			$(function () {
				//add css
				$("head").append("<link type='text/css' rel='stylesheet' href='css/themes/android/android-theme.css' />");

				//set theme class
				$("body").addClass("android");
			});
		}
	}());

	//initialization of pages (retranslating etc.)
	$(document).on("pageinit", main);

	//do what needs to be done after the device is ready
	$(document).on("deviceready", onDeviceReady);

	return {
		retranslate: retranslate,
		startLesson: startLesson
	};
}());
