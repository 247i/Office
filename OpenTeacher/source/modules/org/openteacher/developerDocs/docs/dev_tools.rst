=================
Development tools
=================

There are a number of tools that come in handy when developing
OpenTeacher. We have tools that provide documentation, tools that make
testing easier, tools that automatically package OpenTeacher, and tools
that automate tasks that you'd otherwise to do by hand. They're mostly
built into OpenTeacher itself as a custom profile. They're described
below.

.. figure:: tools.jpg
   :width: 400px
   :figwidth: 400px
   :align: right

   Tools make developing for OpenTeacher a lot easier.

.. contents:: `Contents:`

Tools that provide information
==============================

python openteacher.py -p code-documentation
-------------------------------------------
This is where you're currently looking at: it starts a web server that
provides all kinds of documentation. It shows info on the interfaces of
modules, has a module map that shows dependencies between modules and
also contains the developer documentation. Next to that, there's a page
that lists all FIXME's and TODO's in OpenTeacher.

python openteacher.py -p module-graph
-------------------------------------
Builds the module map that's also shown in the code documentation. In
most cases using the code documentation is easier, but maybe this comes
in handy sometime...

python openteacher.py -p code-complexity
------------------------------
Calculates the McCabe code complexity for (almost) every function in the
OpenTeacher source tree. If it's higher than a certain threshold
(configurable inside the script), then it shows the function name. Handy
heuristic to see which code could use some refactoring. Or just to
monitor how the code complexity evolves over time.

Tools that help with testing
============================

python openteacher.py -p cli
----------------------------
Although the command line interface is made for users, it's often handy
as a fast way of testing code you're developing, since you don't have to
issue UI commands for that. It mostly describes it functionality itself.
(Via the ++help (or +h) option you can pass in a lot of situations.)

python openteacher.py -p shell
------------------------------
Starts an interactive python shell with a module manager with all
modules loaded. Handy for quickly experimenting a bit with some module.

python openteacher.py -p test-suite
-----------------------------------
Runs the test suite. You need to specify an argument that specifies
which tests to run exactly. Handy values are 'fast' (runs all tests that
take no significant time, which are most, and 'all', which takes some
time but runs every single test.)

Tools that handle packaging
===========================

python openteacher.py -p package-arch
-------------------------------------
Packages the currently running OT instance into an Arch Linux package.
(A .tar.xz file.) Works on Arch only.

python openteacher.py -p package-debian
---------------------------------------
This command takes the current installation and builds a debian package
out of it. Requires a Debian or Debian-based (like Ubuntu) system.

python openteacher.py -p package-mac
------------------------------------
Generates a Mac .app directory out of the currently running instance.
Converts the Python code into executables, so there are no other
dependencies. Works on a Mac only.

python openteacher.py -p package-rpm
------------------------------------
Builds an .rpm package build on the current running instance of
OpenTeacher. Recommended to run this on the OS that this .rpm targets.

python openteacher.py -p package-source
---------------------------------------
Packages the source of this installation into a zip file.

python openteacher.py -p package-source-with-setup
--------------------------------------------------
Packages the source of this installation into a tarball, and includes a
setup.py file. Next to that, man pages, a .desktop and a menu file are
included. Handy as a base for packaging for linux distributions. (In
fact, most of the other package-* commands for linux distros use this
behind the screen.)

python openteacher.py -p package-windows-msi
---------------------------------------------
Generates a Windows executable and an Microsoft Installer (.msi) file
that can be used to install it. Windows only.

python openteacher.py -p package-windows-portable
-------------------------------------------------
Packages the current installation into a Windows .exe and some other
files and zips those. Works on Windows only.

Tools that automate certain repeating tasks
===========================================

python openteacher.py -p get-translation-authors
------------------------------------------------
Gathers a list of all translators of OpenTeacher in Launchpad. You can
copy its output code straight into the openteacherAuthors_ module's
code.

.. _openteacherAuthors: ../modules/org/openteacher/openteacherAuthors.html

python openteacher.py -p update-rosetta-priorities
--------------------------------------------------
Updates the translation priorities of OpenTeacher on Launchpad. Handy
since we have a separate translation template (.pot file) for every
module. Priorities are based on the amount of modules that depend on the
module the priority is determined for, and some manual corrections.

python openteacher.py -p update-translations
--------------------------------------------
Updates all .po and .pot files in the source tree. Also generates .mo
files. This makes sure new translations are added, and that translations
made in launchpad and exported from there are actually used.

python openteacher.py -p generate-language-code-guesser-table
-------------------------------------------------------------
Generates the dict used by the languageCodeGuesser_ module based on data
that's in the babel module. This isn't done at runtime, because it's too
slow. You can just paste the output into the file 'tables.py' of the
languageCodeGuesser_ module.

.. _languageCodeGuesser: ../modules/org/openteacher/languageCodeGuesser.html
