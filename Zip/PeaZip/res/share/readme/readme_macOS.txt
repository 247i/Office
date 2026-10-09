HOW TO INSTALL PEAZIP ON MACOS

1) Open PeaZip's DMG and drop peazip.app in Applications directory
2) Open Terminal, paste and run the following command:

xattr -dr com.apple.quarantine /Applications/peazip.app

Running the aforementioned xattr command is needed to remove the "quarantine" attribute which is automatically applied by Safari to unsigned app packages downloaded from the web; otherwise running PeaZip will result in one of the following error messages:

"peazip.app is damaged and can’t be opened"
"peazip.app cannot be opened because the developer cannot be verified" 


OPTIONAL: MACOS SERVICE MENUS

The link "macOS service menus alias" in the package root contains Automator .workflow service menu scripts for quickly sending the items selected in Finder to main PeaZip functions, in example add to archive, extract, extract here, open file or folder with PeaZip, etc.

The link points to the folder with the same name in the installed peazip.app, in 
/Applications/peazip.app/Contents/Resources/share/batch/macOS service menus/
So, applying the correct attributes to the app with xattr (as explained in the previous point) also applies the attributes to those items, allowing them to be correctly installed.

To install a .workflow item, double-click on it.
To uninstall a .workflow item, follow system's instruction from context menu customization entry or simply delete or move it from user's home folder ˜/Library/Services/ directory (which is hidden by default, as alternative to Finder it can be conveniently browsed with PeaZip).


OPTIONAL: CUSTOMIZE APP ICON

The icon displayed while running the app is hardcoded at compile time, it can be changed with Lazarus IDE from Project Options (applies globally to all forms) or changing the icon for each form.
The icon displayed in the dock (while app is not running), in Launcher, and in Finder can be customized replacing the app icon (i.e. from Get Info) with one of the .icns files provided in /Applications/peazip.app/Contents/Resources/share/icons folder inside peazip.app (rightclick the app and select "show content" in Finder).


MORE INFORMATION

PeaZip is available built for aarch64 and Intel architectures on https://peazip.github.io/peazip-macos.html
The application's binaries are not signed by a registered Apple developer account: M1 version is simply ad-hoc signed, Intel version is not signed.
M1 SoC can run bot aarch64 (native) and Intel (using Rosetta 2 emulation layer), Intel-based Macintosh systems can only run Intel version.

PeaZip sources https://peazip.github.io/peazip-sources.html can be built with Lazarus for macOS, sources are tested for Cocoa widget set.
To manually select the target architecture open main menu, Project > Project Options, Configuration and Target, set Darwin as destination OS, and aarch64 as destination CPU family if compiling for machines with M1 Apple Silicon chip, or x86_64 if compiling for Intel-based Apple machines.