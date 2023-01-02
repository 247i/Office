
======================================================================
LibreOffice 7.4 አንብቡኝ
======================================================================


For the latest updates to this readme file, see https://git.libreoffice.org/core/tree/master/README.md

ይህ ፋይል አስፈላጊ መረጃ ይዟል ስለ LibreOffice ሶፍትዌር ፡ ሶፍትዌሩን ከመግጠምዎ በፊት ይህን መረጃ በጥንቃቄ እንዲያነቡ ይመከራሉ

የ LibreOffice ሕብረተሰቡ ሀላፊነት ነው ይህን እቃ ማበልጸግ: እና እንደ ሕብረተሰቡ እንዲሳተፉ እናሳስባለን: አዲስ ተጠቃሚ ከሆኑ ይህን ይጎብኙ የ LibreOffice ድህረ ገጽ: በርካታ መረጃ ያገኛሉ: ስለ የ LibreOffice እቅድ እና ዙሪያውን ስላሉ ሕብረተሰቦች: ይህን ይጎብኙ የ https://www.libreoffice.org/.

ይህ LibreOffice በእርግጥ ነፃ ነው ለማንኛውም ተጠቃሚ?
----------------------------------------------------------------------

LibreOffice is free for use by everybody. You may take this copy of LibreOffice and install it on as many computers as you like, and use it for any purpose you like (including commercial, government, public administration and educational use). For further details see the license text packaged with this LibreOffice download.

ለምን ይህ LibreOffice ለሁሉም ተጠቃሚ ነፃ ሆነ?
----------------------------------------------------------------------

You can use this copy of LibreOffice free of charge because individual contributors and corporate sponsors have designed, developed, tested, translated, documented, supported, marketed, and helped in many other ways to make LibreOffice what it is today - the world's leading Open Source productivity software for home and office.

If you appreciate their efforts, and would like to ensure that LibreOffice continues to be available far into the future, please consider contributing to the project - see https://www.documentfoundation.org/contribution/ for details. Everyone can make a contribution of some kind.

----------------------------------------------------------------------
ማስታወሻ ስለ አገጣጠሙ
----------------------------------------------------------------------

LibreOffice requires a recent version of Java Runtime Environment (JRE) for full functionality. JRE is not part of the LibreOffice installation package, it should be installed separately.

የሚያስፈልገው የስርአት አይነት
----------------------------------------------------------------------

* Microsoft Windows 7 SP1, 8, 8.1 Update (S14) or 10

እባክዎን ይጠንቀቁ የ አስተዳዳሪ መብት ፍቃድ ያስፈልጋል የ መግጠሚያውን ሂደት ለማስኬድ

ምዝገባ ለ LibreOffice እንደ ነባር መተግበሪያ ለ Microsoft Office አቀራረብ ማስገደድ ይቻላል ወይንም መጫን የሚቀጥለውን ትእዛዝ መስመር መቀየሪያ በ መግጠሚያው በ መጠቀም:

* REGISTER_ALL_MSO_TYPES=1 will force registration of LibreOffice as default application for Microsoft Office formats.
* REGISTER_NO_MSO_TYPES=1 will suppress registration of LibreOffice as default application for Microsoft Office formats.

እባክዎን እርግጠኛ ይሁኑ በቂ ነፃ ማስታወሻ በ ጊዚያዊ ዳይሬክቶሪ በ እርስዎ ኮምፒዩተር ውስጥ እንዳለ: እና እባክዎን እርግጠኛ ይሁኑ የ ማንበብ: የ መጻፍ: እና የ ማስኬድ መብት እንደ ተሰጠ: ሁሉንም ሌሎች ፕሮግራሞች ይዝጉ የ መግጠሚያ ሂደት ከ መጀመርዎ በፊት

Installation of LibreOffice on Debian/Ubuntu-based Linux systems
----------------------------------------------------------------------

For instructions on how to install a language pack (after having installed the US English version of LibreOffice), please read the section below entitled Installing a Language Pack.

When you unpack the downloaded archive, you will see that the contents have been decompressed into a sub-directory. Open a file manager window, and change directory to the one starting with "LibreOffice_", followed by the version number and some platform information.

This directory contains a subdirectory called "DEBS". Change directory to the "DEBS" directory.

Right-click within the directory and choose "Open in Terminal". A terminal window will open. From the command line of the terminal window, enter the following command (you will be prompted to enter your root user's password before the command will execute):

The following commands will install LibreOffice and the desktop integration packages (you may just copy and paste them into the terminal screen rather than trying to type them):

sudo dpkg -i *.deb

የመግጠሙ ሂደት ተጠናቋል: በ ዴስክቶፕ ላይ ምልክቶች ይፈጠራሉ LibreOffice ለሁሉም የቢሮ ዝርዝር/መተግበሪያዎች

Installation of LibreOffice on Fedora, openSUSE, Mandriva and other Linux systems using RPM packages
----------------------------------------------------------------------

For instructions on how to install a language pack (after having installed the US English version of LibreOffice), please read the section below entitled Installing a Language Pack.

When you unpack the downloaded archive, you will see that the contents have been decompressed into a sub-directory. Open a file manager window, and change directory to the one starting with "LibreOffice_", followed by the version number and some platform information.

This directory contains a subdirectory called "RPMS". Change directory to the "RPMS" directory.

Right-click within the directory and choose "Open in Terminal". A terminal window will open. From the command line of the terminal window, enter the following command (you will be prompted to enter your root user's password before the command will execute):

For Fedora-based systems: sudo dnf install *.rpm

For Mandriva-based systems: sudo urpmi *.rpm

For other RPM-based systems (openSUSE, etc.): rpm -Uvh *.rpm

የ መግጠሙ ሂደት ተጠናቋል: በዴስክቶፕ ላይ ምልክቶች ይፈጠራሉ LibreOffice ለሁሉም የቢሮ ዝርዝር/መተግበሪያዎች

Alternatively, you can use the 'install' script, located in the toplevel directory of this archive to perform an installation as a user. The script will set up LibreOffice to have its own profile for this installation, separated from your normal LibreOffice profile. Note that this will not install the system integration parts such as desktop menu items and desktop MIME type registrations.

ማስታወሻዎች የ ዴስክቶፕ ማዋሀጃ ለ ሊነክስ ስርጭቶች በ ላይኛው መግጠሚያ መመሪያዎች አይሸፈንም
----------------------------------------------------------------------

It should be easily possible to install LibreOffice on other Linux distributions not specifically covered in these installation instructions. The main aspect for which differences might be encountered is desktop integration.

The RPMS (or DEBS, respectively) directory also contains a package named libreoffice7.4-freedesktop-menus-7.4.0.1-1.noarch.rpm (or libreoffice7.4-debian-menus_7.4.0.1-1_all.deb, respectively, or similar). This is a package for all Linux distributions that support the Freedesktop.org specifications/recommendations (https://en.wikipedia.org/wiki/Freedesktop.org), and is provided for installation on other Linux distributions not covered in the aforementioned instructions.

የ ቋንቋ ጥቅል በ መግጠም ላይ
----------------------------------------------------------------------

Download the language pack for your desired language and platform. They are available from the same location as the main installation archive. From the Nautilus file manager, extract the downloaded archive into a directory (your desktop, for instance). Ensure that you have exited all LibreOffice applications (including the QuickStarter, if it is started).

Change directory to the directory in which you extracted your downloaded language pack.

Now change directory to the directory that was created during the extraction process. For instance, for the French language pack for a 32-bit Debian/Ubuntu-based system, the directory is named LibreOffice_, plus some version information, plus Linux_x86_langpack-deb_fr.

Now change directory to the directory that contains the packages to install. On Debian/Ubuntu-based systems, the directory will be DEBS. On Fedora, openSUSE or Mandriva systems, the directory will be RPMS.

From the Nautilus file manager, right-click in the directory and choose the command "Open in terminal". In the terminal window you just opened, execute the command to install the language pack (with all of the commands below, you may be prompted to enter your root user's password):

For Debian/Ubuntu-based systems: sudo dpkg -i *.deb

For Fedora-based systems: su -c 'dnf install *.rpm'

For Mandriva-based systems: sudo urpmi *.rpm

For other RPM-using systems (openSUSE, etc.): rpm -Uvh *.rpm

አሁን ይጀምሩ አንድ LibreOffice መተግባሪያ - መጻፊያ: ለምሳሌ: ይሂዱ ወደ እቃዎች ዝርዝር እና ይምረጡ ምርጫዎች: በ ምርጫዎች ንግግር ሳጥን ውስጥ: ይጫኑ በ "ቋንቋ ማሰናጃዎች" ላይ እና ከዛ ይጫኑ በ "ቋንቋዎች" ወደ ታች በሚዘረገፍ ላይ: በ "ተጠቃሚ ገጽታ" ዝርዝር ውስጥ እና ቋንቋ ይምረጡ እርስዎ የ ገጠሙትን: እርስዎ ከ ፈለጉ: ተመሳሳይ ይፈጽሙ ለ "ቋንቋ ማሰናጃ": የ "ነባር ገንዘብ": እና የ "ነባር ቋንቋዎች ለ ሰነዶች":

After adjusting those settings, click on OK. The dialog box will close, and you will see an information message telling you that your changes will only be activated after you exit LibreOffice and start it again (remember to also exit the QuickStarter if it is started).

The next time you start LibreOffice, it will start in the language you just installed.

----------------------------------------------------------------------
ፕሮግራሙ ሲጀምር ችግር ተፈጥሯል
----------------------------------------------------------------------

Difficulties starting LibreOffice (e.g. applications hang) as well as problems with the screen display are often caused by the graphics card driver. If these problems occur, please update your graphics card driver or try using the graphics driver delivered with your operating system.

----------------------------------------------------------------------
ALPS/Synaptics notebook touchpads in Windows
----------------------------------------------------------------------

Due to a Windows driver issue, you cannot scroll through LibreOffice documents when you slide your finger across an ALPS/Synaptics touchpad.

To enable touchpad scrolling, add the following lines to the "C:\Program Files\Synaptics\SynTP\SynTPEnh.ini" configuration file, and restart your computer:

[LibreOffice]

FC = "SALFRAME"

SF = 0x10000000

SF |= 0x00004000

የ ማሰናጃ ፋይል አካባቢሊለያይ ይችላል በ ተለያየ እትም መስኮት ውስጥ

----------------------------------------------------------------------
አቋራጭ ቁልፎች
----------------------------------------------------------------------

አቋራጭ ቁልፎች ብቻ (ቁልፍ ማጣመሪያ) በ መስሪያ ስርአቱ ላይ ያልተጠቀሙትን መጠቀም ይችላሉ በ LibreOffice. የ ቁልፍ ማጣመሪያ በ LibreOffice እንደ ተገለጸው አይሰራም በ LibreOffice እርዳታ: የ አቋራጭ ቁልፉን በ ቅድሚያ የ መስሪያ ስርአቱ እንዳልተጠቀመበት ይመርምሩ: ይህን ችግር ለማስወገድ: እርስዎ መቀየር ይችላሉ የ ቁልፍ ጥምረትን በ መስሪያ ስርአት ውስጥ: በ አማራጭ: እርስዎ ማንኛውንም የ ተመደበ ቁልፍ መቀየር ይችላሉ: በ LibreOffice. ለ በለጠ መረጃ ስለዚህ ጉዳይ: ይህን ያመሳክሩ የ LibreOffice እርዳታ: የ እርዳታ ሰነድ በ እርስዎ የ መስሪያ ስርአት ውስጥ

----------------------------------------------------------------------
Problems When Sending Documents as Emails From LibreOffice
----------------------------------------------------------------------

When sending a document via 'File - Send - Document as Email' or 'Document as PDF Attachment' problems might occur (program crashes or hangs). This is due to the Windows system file "Mapi" (Messaging Application Programming Interface) which causes problems in some file versions. Unfortunately, the problem cannot be narrowed down to a certain version number. For more information visit https://www.microsoft.com to search the Microsoft Knowledge Base for "mapi dll".

----------------------------------------------------------------------
አስፈላጊ መድረሻ ማስታወሻዎች
----------------------------------------------------------------------

For more information on the accessibility features in LibreOffice, see https://www.libreoffice.org/accessibility/

----------------------------------------------------------------------
የ ተጠቃሚ ድጋፍ
----------------------------------------------------------------------

The main support page offers various possibilities for help with LibreOffice. Your question may have already been answered - check the Community Forum at https://www.documentfoundation.org/nabble/ or search the archives of the 'users@libreoffice.org' mailing list at https://www.libreoffice.org/lists/users/. Alternatively, you can send in your questions to users@libreoffice.org. If you like to subscribe to the list (to get email responses), send an empty mail to: users+subscribe@libreoffice.org.

Also check the FAQ section at the LibreOffice website.

----------------------------------------------------------------------
ችግር መግለጫ በ መላክ ላይ & ችግሮች
----------------------------------------------------------------------

Our system for reporting, tracking and solving bugs is currently Bugzilla, hosted at https://bugs.documentfoundation.org/. We encourage all users to feel entitled and welcome to report bugs that may arise on your particular platform. Energetic reporting of bugs is one of the most important contributions that the user community can make to the ongoing development and improvement of LibreOffice.

----------------------------------------------------------------------
ይሳተፉ
----------------------------------------------------------------------

The LibreOffice Community would very much benefit from your active participation in the development of this important open source project.

As a user, you are already a valuable part of the suite's development process and we would like to encourage you to take an even more active role with a view to being a long-term contributor to the community. Please join and check out the contributing page at the LibreOffice website.

እንዴት ልጀምር
----------------------------------------------------------------------

The best way to start contributing is to subscribe to one or more of the mailing lists, lurk for a while, and gradually use the mail archives to familiarize yourself with many of the topics covered since the LibreOffice source code was released back in October 2000. When you're comfortable, all you need to do is send an email self-introduction and jump right in. If you are familiar with Open Source Projects, check out our To-Dos list and see if there is anything you would like to help with at the LibreOffice website.

ማህበርተኛ
----------------------------------------------------------------------

Here are a few of the mailing lists to which you can subscribe at https://www.libreoffice.org/get-help/mailing-lists/

* ዜናዎች : announce@documentfoundation.org *ለሁሉም ተጠቃሚዎች የሚመከር * (ቀላል መንገድ)
* የ ዋናው ተጠቃሚ ዝርዝር: users@global.libreoffice.org *easy way to lurk on discussions* (heavy traffic)
* Marketing project: marketing@global.libreoffice.org *beyond development* (getting heavy)
* ባጠቃላይ የ አበልጻጊዎች ዝርዝር: libreoffice@lists.freedesktop.org (heavy traffic)

Joining one or more Projects
----------------------------------------------------------------------

You can make major contributions to this important open source project even if you have limited software design or coding experience. Yes, you!

እኛ ተስፋ እናደርጋለን እርስዎ እንደሚደሰቱበት በ አዲሱ LibreOffice 7.4 እና በ መስመር ላይ ያግኙን

የ LibreOffice ሕብረተሰብ

----------------------------------------------------------------------
የ ተጠቀሙት / የ ተሻሻለ የ ኮድ ምንጭ
----------------------------------------------------------------------

Portions Copyright 1998, 1999 James Clark. Portions Copyright 1996, 1998 Netscape Communications Corporation.
