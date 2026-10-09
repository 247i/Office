/*
	Copyright 2012, Marten de Vries

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

var Event;

Event = function () {
	"use strict";
	var handlers, KeyError;

	handlers = [];
	KeyError = function (key) {
		this.name = "KeyError";
		this.message = "No such key: " + key;
	};
	KeyError.prototype = new Error();

	this.handle = function (handler) {
		var index;

		index = handlers.indexOf(handler);
		if (index === -1) {
			handlers.push(handler);
		}
	};

	this.unhandle = function (handler) {
		var index;

		index = handlers.indexOf(handler);
		if (index !== -1) {
			handlers.splice(index, 1);
		} else {
			throw new KeyError(handler);
		}
	};

	this.send = function () {
		var i, handler, handlersCopy;

		//copy so the handlers iterated through don't change while
		//sending the event.
		handlersCopy = handlers.slice();
		for (i = 0; i < handlersCopy.length; i += 1) {
			handler = handlersCopy[i];
			handler.apply(this, arguments);
		}
	};
};
