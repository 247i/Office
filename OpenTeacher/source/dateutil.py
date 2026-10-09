import warnings

def total_seconds(td):
	warnings.warn("When Python 2.6 support is dropped, switch to td.total_seconds()")

	return int(round((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / float(10**6)))
