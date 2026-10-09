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

/* global $: false */

var copyrightInfoDialog;

copyrightInfoDialog = {
	retranslate: function (_) {
		"use strict";

		$("#copyright-info-header").text(_("Copyright info"));
	},
	setupUi: function () {
		"use strict";

		$("#copyright-info-text")
			.load("COPYING.txt")
			.css("overflow", "auto");
	}
};
