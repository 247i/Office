$(document).ready(function() {
	// Set download button
	$('#osStr').html('for ' + osStr);
	$('#downloadButton').css('background-image', 'url(../images/downloadbuttons/' + os + '-button.png');
	// On mouseover
	$(document).on('mouseover mouseleave', "#downloadButton", function(event){
		var buttonImage;
		if (event.type == 'mouseover') {
			buttonImage = 'url(../images/downloadbuttons/' + os + '-button-h.png)';
			$(this).css('background-image', buttonImage);
		}
		else
		{
			buttonImage = 'url(../images/downloadbuttons/' + os + '-button.png)';
			$(this).css('background-image', buttonImage);
		}
	});
	// On click
	$(document).on('click', '#toTheDownloadPage', function(event) {
		event.preventDefault();
		loadPage('download');
	});
});
