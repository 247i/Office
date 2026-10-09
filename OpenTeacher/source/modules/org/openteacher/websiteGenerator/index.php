<?php
	function tryToRedirect($dir) {
		if (file_exists($dir)) {
			header("Location: $dir");
			exit();
		}
	}

	$langs = explode(",", $_SERVER['HTTP_ACCEPT_LANGUAGE']);

	foreach ($langs as $lang) {
		list($lang) = explode(";", $lang);
		list($lang, $area) = explode("-", $lang);

		if ($area) {
			tryToRedirect($lang . "_" . strtoupper($area));
		}
		tryToRedirect($lang);
	}
	tryToRedirect("en");
?>
