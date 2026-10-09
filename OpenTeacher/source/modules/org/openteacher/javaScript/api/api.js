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

/*global $, localStorage, document */

var Api;

Api = (function() {
	"use strict";
	var actions, fallbackActions, getOfflineLists, getQueue, addToQueue, synchronize, processOneQueueItem;

	actions = {
		newList: function (data, callback) {
			$.post(
				"/api/lists/",
				data
			).fail(function (xhr) {
				//only connection errors should be retried later.
				if (xhr.status === 0) {
					addToQueue({command: "newList", args: [data]});
				}
			}).always(callback);
		},
		updateList: function (id, data, callback) {
			$.ajax(
				"/api/lists/" + id,
				{type: "PUT", data: data}
			).fail(function (xhr) {
				//only connection errors should be retried later.
				if (xhr.status === 0) {
					addToQueue({command: "updateList", args: [id, data]});
				}
			}).always(callback);
		},
		removeList: function (id, callback) {
			$.ajax(
				"/api/lists/" + id,
				{type: "DELETE"}
			).fail(function (xhr) {
				//only connection errors should be retried later.
				if (xhr.status === 0) {
					addToQueue({command: "removeList", args: [id]});
				}
			}).always(callback);
		}
	};

	fallbackActions = {
		newList: function (data) {
			this.push(data);
		},
		updateList: function (id, data) {
			var i;

			for (i = 0; i < this.length; i += 1) {
				if (this[i].id === id) {
					this[i] = data;
					this[i].id = id;
				}
			}
		},
		removeList: function (id) {
			var i;

			for (i = 0; i < this.length; i += 1) {
				if (this[i].id === id) {
					this.splice(i, 1);
					//compensate for the removing
					i -= 1;
				}
			}
		}
	};

	getOfflineLists = function () {
		return JSON.parse(localStorage.lists);
	};

	getQueue = function () {
		return JSON.parse(localStorage.queue);
	};

	addToQueue = function (desc) {
		var queue;

		queue = getQueue();
		queue.push(desc);
		localStorage.queue = JSON.stringify(queue);
	};

	processOneQueueItem = function (queue, onDone) {
		var item;

		item = queue.shift();
		if (typeof item === "undefined") {
			onDone();
			return;
		}
		//add callback
		item.args.push(function () {
			processOneQueueItem(queue, onDone);
		});
		actions[item.command].apply(null, item.args);
	};

	synchronize = function (callback) {
		var queue;

		queue = getQueue();
		localStorage.queue = "[]";

		processOneQueueItem(queue, callback);
	};

	localStorage.lists = localStorage.lists || "[]";
	localStorage.queue = localStorage.queue || "[]";

	$(document).on("online", function () {
		synchronize(function () {});
	});

	return {
		getLists: function (callback) {
			synchronize(function () {
				$.getJSON("/api/lists/", function (response) {
					localStorage.lists = JSON.stringify(response.result);
					callback(getOfflineLists());
				}).fail(function () {
					var i, item, lists, queue;

					//build an up-to-date, but surrogate, list.
					lists = getOfflineLists();
					queue = getQueue();
					for (i = 0; i < queue.length; i += 1) {
						item = queue[i];
						fallbackActions[item.command].apply(lists, item.args);
					}
					callback(lists);
				});
			});
		},
		setCredentials: function (username, password) {
			$.ajaxSetup({username: username, password: password});
		},
		newList: actions.newList,
		updateList: actions.updateList,
		removeList: actions.removeList
	};
}());
