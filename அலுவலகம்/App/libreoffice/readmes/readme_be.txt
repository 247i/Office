
======================================================================
LibreOffice 7.4 ReadMe
======================================================================


For the latest updates to this readme file, see https://git.libreoffice.org/core/tree/master/README.md

This file contains important information about the LibreOffice software. You are recommended to read this information very carefully before starting installation.

The LibreOffice community is responsible for the development of this product, and invites you to consider participating as a community member. If you are a new user, you can visit the LibreOffice site, where you will find lots of information about the LibreOffice project and the communities that exist around it. Go to https://www.libreoffice.org/.

Is LibreOffice Really Free for Any User?
----------------------------------------------------------------------

LibreOffice is free for use by everybody. You may take this copy of LibreOffice and install it on as many computers as you like, and use it for any purpose you like (including commercial, government, public administration and educational use). For further details see the license text packaged with this LibreOffice download.

Чаму LibreOffice бясплатны для ўсіх карыстальнікаў?
----------------------------------------------------------------------

You can use this copy of LibreOffice free of charge because individual contributors and corporate sponsors have designed, developed, tested, translated, documented, supported, marketed, and helped in many other ways to make LibreOffice what it is today - the world's leading Open Source productivity software for home and office.

If you appreciate their efforts, and would like to ensure that LibreOffice continues to be available far into the future, please consider contributing to the project - see https://www.documentfoundation.org/contribution/ for details. Everyone can make a contribution of some kind.

----------------------------------------------------------------------
Заўвагі па ўстаноўцы
----------------------------------------------------------------------

Для поўнай функцыянальнасці LibreOffice патрабуе наяўнасці Java Runtime Environment (JRE) сучаснай версіі. У інсталяцыйны пакет LibreOffice гэтае асяроддзе не ўваходзіць і павінна ставіцца асобна.

Патрабаванні да сістэмы
----------------------------------------------------------------------

* Microsoft Windows 7 SP1, 8, 8.1 Update (S14) or 10

Увага: для ўстаноўкі патрабуюцца паўнамоцтвы адміністратара.

Registration of LibreOffice as default application for Microsoft Office formats can be forced or suppressed by using the following command line switches with the installer:

* REGISTER_ALL_MSO_TYPES=1 прымусіць рэгістрацыю LibreOffice як прадвызначанай праграмы для фарматаў Microsoft Office.
* REGISTER_NO_MSO_TYPES=1 забароніць рэгістрацыю LibreOffice як прадвызначанай праграмы для фарматаў Microsoft Office.

Пераканайцеся, што ў вашай сістэме дастаткова вольнай прасторы ў тымчасовым каталогу, і што ўстаноўлены правы на чытанне, запіс і выкананне. Закрыйце ўсе іншыя праграмы перад пачаткам устанаўлення.

Устаноўка LibreOffice на Linux-сістэмах, заснаваных на Debian/Ubuntu
----------------------------------------------------------------------

For instructions on how to install a language pack (after having installed the US English version of LibreOffice), please read the section below entitled Installing a Language Pack.

When you unpack the downloaded archive, you will see that the contents have been decompressed into a sub-directory. Open a file manager window, and change directory to the one starting with "LibreOffice_", followed by the version number and some platform information.

This directory contains a subdirectory called "DEBS". Change directory to the "DEBS" directory.

Націсніце правую кнопку мышы ў каталогу і выберыце "Адкрыць у тэрмінале". Адкрыецца акно тэрмінала. У камандным радку тэрмінала ўвядзіце наступную каманду (перш чым каманда будзе выканана, вам будзе прапанавана ўвесці пароль карыстальніка root):

The following commands will install LibreOffice and the desktop integration packages (you may just copy and paste them into the terminal screen rather than trying to type them):

sudo dpkg -i *.deb

Цяпер працэс устанаўлення скончаны, і ў сістэмным меню Праграмы/Офіс мусяць з'явіцца значкі для запуску праграм LibreOffice.

Устаноўка LibreOffice на Linux-сістэмах, якія выкарыстоўваюць RPM-пакункі, такіх як Fedora, openSUSE, Mandriva і іншыя
----------------------------------------------------------------------

For instructions on how to install a language pack (after having installed the US English version of LibreOffice), please read the section below entitled Installing a Language Pack.

When you unpack the downloaded archive, you will see that the contents have been decompressed into a sub-directory. Open a file manager window, and change directory to the one starting with "LibreOffice_", followed by the version number and some platform information.

This directory contains a subdirectory called "RPMS". Change directory to the "RPMS" directory.

Націсніце правую кнопку мышы ў каталогу і выберыце "Адкрыць у тэрмінале". Адкрыецца акно тэрмінала. У камандным радку тэрмінала ўвядзіце наступную каманду (перш чым каманда будзе выканана, вам будзе прапанавана ўвесці пароль карыстальніка root):

For Fedora-based systems: sudo dnf install *.rpm

Для сістэм тыпу Mandriva: sudo urpmi *.rpm

Для рэшты сістэм з RPM (openSUSE і інш.): rpm -Uvh *.rpm

Цяпер працэс устанаўлення скончаны, і ў сістэмным меню Праграмы/Офіс мусяць з'явіцца значкі для запуску праграм LibreOffice.

Alternatively, you can use the 'install' script, located in the toplevel directory of this archive to perform an installation as a user. The script will set up LibreOffice to have its own profile for this installation, separated from your normal LibreOffice profile. Note that this will not install the system integration parts such as desktop menu items and desktop MIME type registrations.

Notes Concerning Desktop Integration for Linux Distributions Not Covered in the Above Installation Instructions
----------------------------------------------------------------------

It should be easily possible to install LibreOffice on other Linux distributions not specifically covered in these installation instructions. The main aspect for which differences might be encountered is desktop integration.

The RPMS (or DEBS, respectively) directory also contains a package named libreoffice7.4-freedesktop-menus-7.4.0.1-1.noarch.rpm (or libreoffice7.4-debian-menus_7.4.0.1-1_all.deb, respectively, or similar). This is a package for all Linux distributions that support the Freedesktop.org specifications/recommendations (https://en.wikipedia.org/wiki/Freedesktop.org), and is provided for installation on other Linux distributions not covered in the aforementioned instructions.

Installing a Language Pack
----------------------------------------------------------------------

Download the language pack for your desired language and platform. They are available from the same location as the main installation archive. From the Nautilus file manager, extract the downloaded archive into a directory (your desktop, for instance). Ensure that you have exited all LibreOffice applications (including the QuickStarter, if it is started).

Перайдзіце ў каталог, у які вы распакавалі ваш атрыманы моўны пакунак.

Now change directory to the directory that was created during the extraction process. For instance, for the French language pack for a 32-bit Debian/Ubuntu-based system, the directory is named LibreOffice_, plus some version information, plus Linux_x86_langpack-deb_fr.

Now change directory to the directory that contains the packages to install. On Debian/Ubuntu-based systems, the directory will be DEBS. On Fedora, openSUSE or Mandriva systems, the directory will be RPMS.

From the Nautilus file manager, right-click in the directory and choose the command "Open in terminal". In the terminal window you just opened, execute the command to install the language pack (with all of the commands below, you may be prompted to enter your root user's password):

Для Debian/Ubuntu-падобных сістэм: sudo dpkg -i *.deb

For Fedora-based systems: su -c 'dnf install *.rpm'

Для сістэм тыпу Mandriva: sudo urpmi *.rpm

Для рэшты сістэм з RPM (openSUSE і інш.): rpm -Uvh *.rpm

Цяпер запусціце адну з праграм  LibreOffice, напрыклад, Writer. Перайдзіце ў меню Прылады - Настаўленні. У дыялогавым акне Настаўленні раскрыйце "Моўныя настаўленні", а потым націсніце "Мовы". У выпадальным спісе "Карыстальніцкі інтэрфейс" выберыце толькі што ўстаноўленую мову. Калі трэба, зрабіце тое самае для "Настаўленні мясцовасці", "Прадвызначаная валюта" і "Прадвызначаныя мовы для дакументаў".

Пасля ўстанаўлення гэтых параметраў націсніце ОК. Дыялог закрыецца і вы пабачыце паведамленне, што вашы змяненні набудуць моц пасля выхаду з LibreOffice і наступнага запуску (не забудзьце таксама выйсці з QuickStarter, калі ён запушчаны).

Наступным разам LibreOffice запусціцца з толькі што ўстаноўленай мовай.

----------------------------------------------------------------------
Праблемы пры пуску праграмы
----------------------------------------------------------------------

Difficulties starting LibreOffice (e.g. applications hang) as well as problems with the screen display are often caused by the graphics card driver. If these problems occur, please update your graphics card driver or try using the graphics driver delivered with your operating system.

----------------------------------------------------------------------
Сенсарныя панэлі мабільных камп'ютараў ALPS/Synaptics у Windows
----------------------------------------------------------------------

Вы не можаце пракручваць дакументы у LibreOffice, водзячы пальцам па сенсарных панэлях ('тачпадах') ALPS/Synaptics, таму што ў іх драйверах для сістэмы Windows ёсць праблемы.

Каб адключыць пракручванне з дапамогай тачпаду, дадайце наступныя радкі ў канфігурацыйны файл "C:\Program Files\Synaptics\SynTP\SynTPEnh.ini" і перазапусціце камп'ютар:

[LibreOffice]

FC = "SALFRAME"

SF = 0x10000000

SF |= 0x00004000

The location of the configuration file might vary on different versions of Windows.

----------------------------------------------------------------------
Клавішавыя скароты
----------------------------------------------------------------------

Толькі тыя клавіятурныя скароты (спалучэнні клавіш), што не выкарыстоўваюцца аперацыйнай сістэмай, могуць быць выкарыстаны ў LibreOffice. Калі спалучэнне клавіш у LibreOffice не працуе так, яка апісана ў даведцы LibreOffice, праверце, ці не выкарыстаны ўжо гэтыя скароты аперацыйнай сістэмай. Каб развязаць падобныя канфлікты, вы можаце змяніць спалучэнні, вызначаныя вашай аперацыйнай сістэмай. Як варыянт, вы можаце змяніць амаль кожны скарот у LibreOffice. Каб атрымаць больш інфармацыі па гэтай тэме, звярніцеся да даведкі LibreOffice ці да даведкі аперацыйнай сістэмы.

----------------------------------------------------------------------
Problems When Sending Documents as Emails From LibreOffice
----------------------------------------------------------------------

When sending a document via 'File - Send - Document as Email' or 'Document as PDF Attachment' problems might occur (program crashes or hangs). This is due to the Windows system file "Mapi" (Messaging Application Programming Interface) which causes problems in some file versions. Unfortunately, the problem cannot be narrowed down to a certain version number. For more information visit https://www.microsoft.com to search the Microsoft Knowledge Base for "mapi dll".

----------------------------------------------------------------------
Важныя заўвагі да падтрымкі асоб з абмежаванымі здольнасцямі
----------------------------------------------------------------------

For more information on the accessibility features in LibreOffice, see https://www.libreoffice.org/accessibility/

----------------------------------------------------------------------
Падтрымка карыстальнікаў
----------------------------------------------------------------------

The main support page offers various possibilities for help with LibreOffice. Your question may have already been answered - check the Community Forum at https://www.documentfoundation.org/nabble/ or search the archives of the 'users@libreoffice.org' mailing list at https://www.libreoffice.org/lists/users/. Alternatively, you can send in your questions to users@libreoffice.org. If you like to subscribe to the list (to get email responses), send an empty mail to: users+subscribe@libreoffice.org.

Also check the FAQ section at the LibreOffice website.

----------------------------------------------------------------------
Паведамленні пра памылкі & пажаданні
----------------------------------------------------------------------

Our system for reporting, tracking and solving bugs is currently Bugzilla, hosted at https://bugs.documentfoundation.org/. We encourage all users to feel entitled and welcome to report bugs that may arise on your particular platform. Energetic reporting of bugs is one of the most important contributions that the user community can make to the ongoing development and improvement of LibreOffice.

----------------------------------------------------------------------
Getting Involved
----------------------------------------------------------------------

Супольнасць LibreOffice вельмі скарыстала б з вашага актыўнага ўдзелу ў распрацоўцы гэтага важнага праекту адкрытых праграм.

As a user, you are already a valuable part of the suite's development process and we would like to encourage you to take an even more active role with a view to being a long-term contributor to the community. Please join and check out the contributing page at the LibreOffice website.

Як пачынаць
----------------------------------------------------------------------

The best way to start contributing is to subscribe to one or more of the mailing lists, lurk for a while, and gradually use the mail archives to familiarize yourself with many of the topics covered since the LibreOffice source code was released back in October 2000. When you're comfortable, all you need to do is send an email self-introduction and jump right in. If you are familiar with Open Source Projects, check out our To-Dos list and see if there is anything you would like to help with at the LibreOffice website.

Падпісацца
----------------------------------------------------------------------

Here are a few of the mailing lists to which you can subscribe at https://www.libreoffice.org/get-help/mailing-lists/

* Навіны: announce@documentfoundation.org *рэкамендуецца ўсім карыстальнікам* (малы трафік)
* Галоўная рассылка для карыстальнікаў: users@global.libreoffice.org *сачыць за абмеркаваннямі проста* (вялікі трафік)
* Праект маркетынгу: marketing@global.libreoffice.org *па-за распрацоўкай* (трафік пачынае рабіцца вялікім)
* Агульны спіс распрацоўшчыкаў: libreoffice@lists.freedesktop.org (вялікі трафік)

Далучыцца да аднаго ці некалькіх праектаў
----------------------------------------------------------------------

Вы можаце зрабіць важны ўклад у гэты праект адкрытага праграмнага забеспячэння, нават калі ваш досвед распрацоўкі ці кадавання праграм малы. Так, вы!

Спадзяёмся, што вам спадабаецца праца з новым LibreOffice 7.4, і што вы далучыцеся да нас у Сеціве.

Супольнасць LibreOffice

----------------------------------------------------------------------
Выкарыстаны/зменены выточны код
----------------------------------------------------------------------

Portions Copyright 1998, 1999 James Clark. Portions Copyright 1996, 1998 Netscape Communications Corporation.
