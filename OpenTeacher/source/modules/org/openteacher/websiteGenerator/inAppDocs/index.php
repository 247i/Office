<?php
	$lang = $_SERVER['HTTP_ACCEPT_LANGUAGE'];
	$filename = basename($lang) . ".html";
	if (file_exists($filename)) {
		require($filename);
	} else {
		require("en.html");
	};
?>
