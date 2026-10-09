// Switches to another page
function loadPage(pageName)
{
	// Make the light go to the right place
	selectedMenuItem = '#' + pageName.split('/')[0] + 'Link';
	lightMove(selectedMenuItem);
	
	$("#content").slideUp(200,function() {
		$("#content").load(pageName + '.html' + ' #content', function() {
			$("#content").slideDown(200);
			currentPage = pageName;
		});
	});
}

// Makes the buttons functional
$(document).ready(function() {
	$(document).on("click", ".aLink", function(event) {
		event.preventDefault();
		var rel = $(this).attr('rel');
		loadPage(rel);
	});
});
