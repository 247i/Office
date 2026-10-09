PeaZip is a natively portable standalone application, requiring none or minimal installation on the target system.

This is an advantage when it's desired to have a portable application to just unpack and run, or when a library freeze is desired and shared libraries should not be furtherly changed (i.e. on some production system), or when it's desired to have a single application with almost identical look and feel and features in an environment with mixed systems or desktop managers.

One obvious shortcoming of this approach is natively scarce system integration on target environments, which is addressed by Linux installers using same methods here explained in order to automatically integrate out-of-the box the application in different distributions.

With following instructions you can easily integrate PeaZip with Gnome, KDE, and other DE following Freedesktop guidelines.


1 INSTALL PEAZIP

1A Install a PeaZip installable package, or

1B Extract PeaZip portable to the desired path (i.e. in /opt, or in user's home subpath) and link peazip binary in the binaries folder most suited for your system i.e. /bin, /sbin, /usr/bin, /usr/local/bin [you will need root unless you have a ~/bin folder configured in user's home]
If you can not or want not to link peazip in binaries folder, you can edit the script files here provided using the absolute path of peazip binary instead of "peazip" directory.


2 SYSTEM INTEGRATION

App list, open with, and context menu can be customised using .desktop files provided in this folder: 
- peazip.desktop file provides standard system integration to main application; it is automatically installed with PeaZip installable packages
- additional-desktop-files contains other alternative .desktop files for direct access to specific fuctions (extraction, archiving, force open as archive...) even to DE non supporting .desktop file Actions

Desired .desktop file(s) needs to be copied to /usr/share/applications or /usr/local/share/applications (system-wide) ~/.local/share/applications/ (user-specific)

Icon .png file(s) needs to be copied to /usr/share/icons or /usr/local/share/icons (system-wide) ~/.local/share/icons/ (user-specific)
More icon files are available in (peazip)/res/share/icons directory.
The icons of the app can be modified if desired, and the .desktop files can be edited to use a different icon.

Please note those locations may be different in some distributions and desktop environments, or could have been further configured differently by user's choice [you will need root to write to system-wide directories].

Notes for specific Desktop Environments:

2a) Gnome, Mate, Cinnamon (old), Budgie

Some versions may have been configured to use */pixmaps instad of */icons path.

Gnome-derived DE generally allows to customise CONTEXT MENU, use the scripts in 'Nautilus-scripts' directory.
Copy 'PeaZip' folder (or individual scripts you prefer) from the 'Nautilus-scripts' directory to:
Gnome 2 ~/.gnome2/nautilus-scripts 
Gnome 3 and 4 ~/.local/share/nautilus/scripts
Make sure "Allow executing file as program" or "Is executable" permission is set for the Nautilus scripts.

A sh script is available in 'Nautilus-scripts' directory to help installation of PeaZip context menu entries for the current user.

2b) Cinnamon (new)

To customise the CONTEXT MENU, copy desired Nemo-actions in
~/.local/share/nemo/actions
"Allow executing file as program" or "Is executable" permission may be needed to enable the entries.

A sh script is available in 'Nemo-actions' directory to help installation of PeaZip context menu entries for the current user.

2c) KDE

Some versions of KDE may have been configured to use (kde directory)/share/applications/kde instead of standard paths.
The (kde directory) is specified in $KDEDIR in environment variable and can be overridden by $KDEDIRS.

To customise CONTEXT MENU use Service menus .desktop files from KDE(version) subfolders in 'KDE-servicemenus' directory.
Copy .desktop files from KDE(version) subfolders into, usually:
KDE 3 (kde directory)/share/apps/konqueror/servicemenus (kde directry usually being /opt/kde3)
KDE 4 /usr/share/kde4/services/ServiceMenus
KDE 5 (prior 5.85) /usr/share/kservices5/ServiceMenus or ~/.local/share/kservices5/ServiceMenus
KDE 5 and KDE 6 /usr/share/kio/servicemenus or ~/.local/share/kio/servicemenus
"Allow executing file as program" or "Is executable" permission may be needed to be set for the .desktop files in context menu.

A sh script is available in 'KDE-servicemenus' directory to help installation of PeaZip context menu entries for the current user.

2c) Xfce, LXDE 

Copy peazip.desktop file or other .desktop files to standard locations specified at point 2).
For Xfce, Xfdesktop 4.5 or higher is required


3) FLATPAK AND OTHER SANDBOXED / CONTAINERIZED PACKAGE MANAGERS

If installation takes place in a sanboxed / containerized environment, adapt paragraph 2) instructions starting from the virtual root path created by the package manager for the application.

In example, for PeaZip Flatpak, all Desktop Environment integration paths suggested in paragraph 2) will be replicated starting from the directory
~/.var/app/io.github.peazip.PeaZip/
which is the root directory of the sandboxed environment creted by Flatpak for PeaZip app.

Invoking PeaZip in such environment will then requires some changes:

Exec=peazip 
strings can be replaced with 
Exec=flatpak run --fileforwarding io.github.peazip.PeaZip

and %* parameters can be replaced with @@ '$basedir/$*' @@

Refer to package manager's documentation for more details about how the sandboxed paths are managed, and translated in actual paths for the host system.

If system's environment variables (e.g. cursor size and theme) are not correctly passed to the containerized application for any reason, tools like Flatseal can help troubleshooting and fixing the issue.


4) OPTIONAL CUSTOMISATION

.desktop files can be modified to implement functions described "Customisation and scripting" chapter of PeaZip help file.

Also, .desktop files can be edited to translate text, replace icons, and implement different features as described in Freedesktop specification documentation https://specifications.freedesktop.org/desktop-entry-spec/latest/
