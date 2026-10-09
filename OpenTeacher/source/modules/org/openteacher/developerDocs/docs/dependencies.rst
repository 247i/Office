============
Dependencies
============

This page contains a list of dependencies needed when you want to run
every single bit of OpenTeacher. In practise, only a subset is required
since most of the dependencies below are only used when developing.
Also, OpenTeacher nicely disables parts of itself when dependencies are
missing. In other words, running it with e.g. only Python and PyQt4
works just fine.

Dependencies for using OpenTeacher
==================================

* python
* python-qt4
* python-qt4-phonon
* python-qt4-gl
* python-enchant
* python-chardet
* pyttsx (currently included)
* pyratemp (currently included)
* espeak
* tesseract-ocr or cuneiform

also (test server):

* python-django
* django-rest-framework

also (command line interface)

* python-urwid

also (gtk ui)

* python-gi (gobject-introspection)

and if we ever implement updates:

* gpg
* python-gnupg?

Dependencies for developing OpenTeacher
=======================================

* python-flask
* python-cherrypy3
* python-pygments
* python-docutils
* python-launchpadlib
* python-polib
* python-pygraphviz
* python-twisted
* python-faulthandler
* python-babel
* gettext
* cython

(deb build only & optional:)

* python-all-dev
* build-essential

(when building windows/mac packages only:)

* PyInstaller

Alternative runtimes
====================

This list of dependencies can give problems on alternative Python
runtimes. (We're currently targetting CPython 2.6 & 2.7)

Incompatible dependencies: PyPy
-------------------------------

* python-qt4
* python-qt4-phonon
* python-qt4-gl
* python-enchant
* python-pygraphviz
* python-faulthandler (although similar tools might exist)
* python-gi
* PyInstaller

unsure (but they probably work as they probably don't use C extensions):

* python-launchpadlib
* python-polib
* python-gnupg
* urwid

Incompatible dependencies: CPython 3.x
--------------------------------------

* pyttsx (no detectable effort ongoing)
* python-flask (but: 'https://github.com/mitsuhiko/flask/issues/587')
* python-launchpadlib (https://bugs.launchpad.net/launchpadlib/+bug/1060734)
* python-twisted (but: http://twistedmatrix.com/trac/milestone/Python-3.x & http://twistedmatrix.com/trac/wiki/Plan/Python3)
* python-babel (but: http://babel.edgewall.org/ticket/209)
* PyInstaller (but: http://www.pyinstaller.org/ticket/85)
