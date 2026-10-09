$(document).ready(function() {
	// Preload the images
	var img1 = new Image();
	img1.src = 'images/windows-button-h.png';
	var img4 = new Image();
	img4.src = 'images/screens/3.0-windows-teach.png';
	var img6 = new Image();
	img6.src = 'images/screens/3.0-windows-topo.png';
	var img7 = new Image();
	img7.src = 'images/screens/3.0-windows-media.png';
	var img8 = new Image();
	img8.src = 'images/screens/3.0-ubuntu-enter.png';
	var img9 = new Image();
	img9.src = 'images/screens/2.-test-mac.png';
	
	$(document).on("mouseover", ".screenThumb", function(event) {
		var rel = $(this).attr('rel');
		if($('#screenshot').attr('src') != '../images/screens/' + rel + '.png')
		{
			$('#screenshot').fadeTo(100,0,function(){
				$('#screenshot').attr('src','../images/screens/' + rel + '.png');
				$('#screenshot').fadeTo(100,1);
			});
		}
	});
});