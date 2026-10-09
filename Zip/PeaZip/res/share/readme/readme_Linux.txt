HOW TO INSTALL PEAZIP ON LINUX

PeaZip is available as pre-built packages on https://peazip.github.io/peazip-linux.html
Packages are built for aarch64 and x86_64, targeting GTK2 and Qt6 widgetsets (experimental GTK3-alpha available for evaluation and debugging purpose), packed as DEB, RPM, and as Portable packages not requiring installation.

HINT: running peazip binary in the console provides more feedback in case of problems running the application, i.e. missing dependencies.

Pre-built packages does not cover all possible combinations of architecture, widgetset, and package format, and are not targeting any specific Linux distribution/version.
Consequently, it is recommended to search for specific installers on your own distro or package manager repositories, and to require inclusion of PeaZip to maintainers of said repositories if a PeaZip package is missing (or outdated) in the repository.

As alternative:
- PeaZip is available as Flatpak on https://flathub.org/apps/io.github.peazip.PeaZip (Qt6, both for aarch64 and x86_64), or
- PeaZip can be built from sources https://peazip.github.io/peazip-sources.html


QT VERSION

Qt6 packages provides libQt6Pas.so which may be required on some machines to run the Qt version of PeaZip.
The binary, or equivalent to libQt6Pas.so, must be installed in /usr/local/lib or equivalent directory, such as /usr/lib. 
You can get up to date libQt6Pas.so using distribution-specific tools, i.e. apt-get install package:architecture, or copying the file manually and running ldconfig.


OPTIONAL: SYSTEM INTEGRATION

To integrate PeaZip in context menus and app launchers of Gnome, KDE, and other DE, please refer to the sample .desktop files in (peazip)/res/share/batch/freedesktop_integration directory, and documentation in readme_freedesktop_integration.txt file in same directory.


MORE INFORMATION

PeaZip sources https://peazip.github.io/peazip-sources.html can be built with Lazarus for Linux.
To add or remove .lpk (Lazarus Packages) dependencies from sources use main menu > Project > Project Inspector.
To manually select the target architecture (i.e. aarch64, x86_64) open main menu, Project > Project Options, Configuration and Target.
To manually set the target widgetset (i.e. GTK2, GTK3, Qt5, Qt6) open main menu, Project > Project Options, Configuration and Target and click "Select other widgetset".
To compile from console, and to build packages, please refer to the readme.txt file in the source package.