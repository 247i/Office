// Copyright 2010 The Closure Library Authors. Apache License, Version 2.0

dirname = function(path) {
	var i = path.lastIndexOf('/') + 1;
	var head = path.slice(0, i);
	//If the path isn't all forward slashes, trim the trailing slashes.
	if (!/^\/+$/.test(head)) {
		head = head.replace(/\/+$/, '');
	}
	return head;
};

$(document).ready(function() {
	$(document).on('click', '.linkToLinkHere', function() {
		$(this).hide();
		var url = dirname(window.location.href) + "/" + currentPage + ".html";
		$('#linkHere').text(url).show();

		return false;
	});
});
