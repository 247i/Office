/*
	Copyright 2011-2012, Marten de Vries

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

var compose = function (word) {
	"use strict";
	var text, i, obligatorySet;

	if (word.length === 0) {
		return "";
	}
	if (word.length === 1) {
		return word[0].join(", ");
	}
	text = "";
	for (i = 0; i < word.length; i += 1) {
		obligatorySet = word[i];
		text += [
			i + 1,
			". ",
			obligatorySet.join(", "),
			" "
		].join("");
	}
	return text.trim();
};
