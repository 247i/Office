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

/*global Event */

var LessonType;

LessonType = function (list, indexes) {
	"use strict";
	var modifyItem, test, sendNext, appendTest;

	//give this object its events
	this.newItem = new Event();
	this.lessonDone = new Event();

	//set public properties
	this.askedItems = 0;
	this.totalItems = indexes.length;
	this.list = list;

	//and object-unique private data
	test = {
		results: [],
		finished: false,
		pauses: []
	};

	if (arguments.length === 3) {
		modifyItem = arguments[2];
	} else {
		modifyItem = function (item) {return item;};
	}

	appendTest = function () {
		if (typeof list.tests === "undefined") {
			list.tests = [];
		}
		if (typeof list.tests[list.tests.length - 1] === "undefined") {
			list.tests.push(test);
		} else if (list.tests[list.tests.length - 1] !== test) {
			list.tests.push(test);
		}
	};

	sendNext = function () {
		var i, item;

		i = indexes[this.askedItems];
		if (typeof i === "undefined") {
			//lesson end
			if (test.results.length !== 0) {
				test.finished = true;
				if (typeof list.tests === "undefined") {
					list.tests = [];
				}
			}
			this.lessonDone.send();
		} else {
			//normally in lesson
			item = list.items[i];
			this.newItem.send(modifyItem(item));
		}
	};

	this.correctLastAnswer = function (result) {
		test.results[test.results.length - 1] = result;
	};

	this.setResult = function (result) {
		//Add the test to the list (if it's not already there)
		appendTest();

		test.results.push(result);

		this.askedItems += 1;
		sendNext.call(this);
	};

	this.skip = function () {
		var index;

		//get the index
		index = indexes[this.askedItems];
		//remove it
		indexes.splice(this.askedItems, 1);
		//add it again at the end
		indexes.push(index);

		//and continue
		sendNext.call(this);
	};

	this.start = function () {
		sendNext.call(this);
	};

	this.addPause = function (pause) {
		test.pauses.push(pause);
	};
};
