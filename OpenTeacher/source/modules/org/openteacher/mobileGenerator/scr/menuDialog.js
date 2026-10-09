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

/* global $: false, enterTab: false */

var menuDialog;

menuDialog = (function () {
	"use strict";

	var newList, askWhichListToLoad, loadList, askSaveName,
		saveList, getLessons, saveLessons, askWhichListToRemove,
		removeList;

	getLessons = function () {
		return JSON.parse(localStorage.lessons || "{}");
	};

	saveLessons = function (lessons) {
		localStorage.lessons = JSON.stringify(lessons);
	};

	newList = function () {
		$.mobile.changePage($("#enter-page"));
		enterTab.newList();
	};

	removeList = function (name) {
		var lessons;

		lessons = getLessons();
		delete lessons[name];
		saveLessons(lessons);

		history.go(-2);
	};

	askWhichListToRemove = function () {
		var html, lists, name, listView;

		html = "";

		//fill the list view again with newly retrieved lists.
		lists = getLessons();
		for (name in lists) {
			if (lists.hasOwnProperty(name)) {
				html += "<li><a href='#'>" + name + "</a></li>";
			}
		}

		listView = $("#remove-listview");
		listView.html(html);
		try {
			listView.listview("refresh");
		} catch (e) {}
		$.mobile.changePage($("#remove-dialog"));
	};

	loadList = function (name) {
		var lesson;

		//load the associated lesson
		lesson = getLessons()[name];
		//and load that lesson into the enter tab
		enterTab.fromLesson(lesson);
		//then, switch to the enter tab.
		$.mobile.changePage($("#enter-page"));
	};

	askWhichListToLoad = function () {
		var html, lists, name, listView;

		html = "";

		//fill the list view again with newly retrieved lists.
		lists = getLessons();
		for (name in lists) {
			if (lists.hasOwnProperty(name)) {
				html += "<li><a href='#'>" + name + "</a></li>";
			}
		}

		listView = $("#load-listview");
		listView.html(html);
		try {
			listView.listview("refresh");
		} catch (e) {}
		$.mobile.changePage($("#load-dialog"));
	};

	askSaveName = function () {
		$.mobile.changePage($("#save-dialog"));
	};

	saveList = function (force) {
		var lessons, nameBox, name, lesson;

		nameBox = $("#save-name-box");
		name = nameBox.val();

		lessons = getLessons();

		if (lessons.hasOwnProperty(name) && !force) {
			//ask if the user wants to overwrite
			$("#overwrite-popup").popup("open");
			return;
		}
		//clean name box
		nameBox.val("");

		//do saving
		lesson = enterTab.toLesson();
		if (lesson) {
			lessons[name] = lesson;
			saveLessons(lessons);
		}

		//update ui
		history.go(-2);
	};
	return {
		setupUi: function () {
			$("#new-list-button").click(newList);
			$("#load-list-button").click(askWhichListToLoad);
			$("#save-list-button").click(askSaveName);
			$("#remove-list-button").click(askWhichListToRemove);

			$("#save-done-button").click(function () {
				saveList(false);
			});
			$("#overwrite-yes-button").click(function () {
				saveList(true);
			});
			$("#overwrite-no-button").click(askSaveName);

			//for all 'a's in #load-listview, so also ones added
			//later on.
			$("#load-listview").on("click", "a", function () {
				loadList($(this).text());
			});
			//same for remove
			$("#remove-listview").on("click", "a", function () {
				removeList($(this).text());
			});
		},
		retranslate: function (_) {
			//base dialog
			$("#menu-header").text(_("Menu"));
			$("#new-list-button").text(_("New list"));
			$("#load-list-button").text(_("Load list"));
			$("#save-list-button").text(_("Save list"));
			$("#remove-list-button").text(_("Remove list"));
			$("#options-button .ui-btn-text").text(_("Options"));

			//save dialog (& overwrite popup)
			$("#save-header").text(_("Save list"));
			$("#save-explanation").text(_("Please choose a name for the current list, so it can be saved."));
			$("#save-name-box-label").text(_("Name:"));
			$("#save-done-button").text(_("Done"));

			$("#overwrite-header").text(_("Warning"));
			$("#overwrite-title").text(_("There is already a list named like that."));
			$("#overwrite-msg").text(_("If you continue, it will be overwritten. Continue?"));
			$("#overwrite-yes-button").text(_("Yes"));
			$("#overwrite-no-button").text(_("No"));

			//load dialog
			$("#load-header").text(_("Load list"));
			$("#load-explanation").text(_("Please choose the list you want to load."));
			$("#load-listview").attr("data-filter-placeholder", _("Filter lists..."));

			//remove dialog
			$("#remove-header").text(_("Remove list"));
			$("#remove-explanation").text(_('Please choose the list you want to remove.'));
			$("#remove-listview").attr("data-filter-placeholder", _("Filter lists..."));
		}
	};
}());
