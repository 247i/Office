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

/*global compose: false */
var composeList;

composeList = (function () {
	"use strict";
	var escape, equalsRe, tabRe;

	equalsRe = new RegExp("[^\\\\](=)");
	tabRe = new RegExp("[^\\\\](\t)");

	escape = function (data) {
		var i;

		//(+ 1 because we want the '=', not the thing that isn't a
		//slash)
		i = data.search(equalsRe) + 1;
		if (i) {
			//+ 1 here to make sure the '=' isn't double included.
			data = data.slice(0, i) + "\\=" + data.slice(i + 1);
		}
		//same for tab
		i = data.search(tabRe) + 1;
		if (i) {
			data = data.slice(0, i) + "\\\t" + data.slice(i + 1);
		}
		return data;
	};

	return function (container) {
		var items, result, i, questions, answers;

		items = container.list.items || [];
		result = "";
		for (i = 0; i < items.length; i += 1) {
			questions = compose(items[i].questions || []);
			answers = compose(items[i].answers || []);
			result += escape(questions) + " = " + escape(answers) + "\n";
		}
		if (!result) {
			return "\n";
		}
		return result;
	};
}());
