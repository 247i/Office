// Calculates the light position
function lightPos(selector) {
	return $(selector).position().left + $(selector).width() / 2 - 10;
}

// Moves the light to a selector (must be id of a .menuLink)
function lightMove(selector) {
	$('#menuLight').stop().animate({'left': lightPos(selector) + 'px'});
}

$(document).ready(function() {
	// Make light visible and on right place
	$('#menuLight').show();
	$('#menuLight').css('left', lightPos('#indexLink') + 'px');
	
	// Hovering over menu items makes light move
	$('.menuLink').hover(function() {
		lightMove(this);
	}, function() {
		lightMove(selectedMenuItem);
	});
	
	// Resizing window needs to make light move along
	$(window).resize(function() {
		lightMove(selectedMenuItem);
	});
});