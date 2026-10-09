This folder contains Automator .workflow scripts to add most common PeaZip functions to the macOS Finder context menu, as service menu items.

To install a .workflow item, double-click on it.
To uninstall a .workflow item, follow system's instruction from context menu customization entry, or simply delete or move it from user's home folder ˜/Library/Services/ directory (which is hidden by default, as alternative to Finder it can be conveniently browsed using PeaZip).

It is recommended to make a copy of the .workflow items in order to keep a reference copy in case they are modified using Automator, or gets deleted installing/unistalling them.

The link "macOS service menus alias" in the root of macOS packages points to the folder with the same name in the installed peazip.app
To install peazip.app it is needed to apply correct attributes to it in the Terminal using following command
xattr -dr com.apple.quarantine /Applications/peazip.app
this action also results in applying correct attributes to the .workflow scripts, which is needed to be able to correctly install them as service menu items.
