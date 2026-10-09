// Sets some useful os-dependent variables
var ua = navigator.userAgent.toLowerCase();

if(ua.indexOf('fedora') !== -1 || ua.indexOf('redhat') !== -1) {
	os = 'fedora';
	osStr = 'Fedora/Redhat (.rpm)';
} else if(ua.indexOf('linux') !== -1) {
	os = 'ubuntu';
	osStr = 'Ubuntu (.deb)';
} else if(ua.indexOf('mac') !== -1) {
	os = 'osx';
	osStr = 'Mac OS X 10.7 (Experimental)';
} else {
	os = 'windows';
	osStr = 'Windows';
}