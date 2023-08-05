
======================================================================
LibreOffice 7.4 Pročitaj Me
======================================================================


For the latest updates to this readme file, see https://git.libreoffice.org/core/tree/master/README.md

Ova datoteka sadrži važne informacije o softveru LibreOffice. Preporučeno je da pročitate pažljivo ove informacije prije početka instalacije.

The LibreOffice community is responsible for the development of this product, and invites you to consider participating as a community member. If you are a new user, you can visit the LibreOffice site, where you will find lots of information about the LibreOffice project and the communities that exist around it. Go to https://www.libreoffice.org/.

Da li je LibreOffice stvarno besplatan za sve?
----------------------------------------------------------------------

LibreOffice je slobodan za sve. Kopiju paketa LibreOffice možete da instalirate na neograničeno računara i koristite na bilo koji način (uključujući komercijalnu upotrebu i upotrebu u javnoj upravi i obrazovanju). Za više informacija pogledajte licencu upakovanu sa instalacijom paketa LibreOffice.

Zašto je LibreOffice besplatan za sve?
----------------------------------------------------------------------

Možete da koristite kopiju paketa LibreOffice slobodno i besplatno jer su pojedinačni saradnici i partneri projekta dizajnirali, razvili, testirali, preveli, dokumentovali, podržali i pomogli na mnoge druge načine kako bi paket LibreOffice načinili onim što je danas — vodeći svjetski slobodni kancelarijski softver za dom i kancelariju.

If you appreciate their efforts, and would like to ensure that LibreOffice continues to be available far into the future, please consider contributing to the project - see https://www.documentfoundation.org/contribution/ for details. Everyone can make a contribution of some kind.

----------------------------------------------------------------------
Bilješke o instalaciji
----------------------------------------------------------------------

LibreOffice  zahtijeva noviju verziju Java Runtime Environment (JRE) da bi u potpunosti funkcionisao. JRE nije dio instalacijskog paketa LibreOffice , stoga je potrebna odvojena instalacija.

Sistemski zahtjevi
----------------------------------------------------------------------

* Microsoft Windows 7 SP1, 8, 8.1 Update (S14) or 10

Napominjemo da su prava administratora potrebna za instalacijski proces.

Registracija LibreOffice kao podrazumijevane aplikacije za Microsoft Office formate može biti forsirana ili prevaziđena sljedećim parametrima komandne linije unutar instalacije:

* REGISTER_ALL_MSO_TYPES=1 će nametnuti registraciju LibreOffice kao podrazumijevane aplikacije za Microsoft Office formate.
* REGISTER_NO_MSO_TYPES=1 će zanemariti registraciju LibreOffice kao podrazumijevane aplikacije za Microsoft Office formate.

Postarajte se da imate dovoljno raspoložive memorije u privremenom direktoriju na vašem sistemu i da su dozvoljene privilegije za čitanje, upisivanje i izvršavanje. Zatvorite sve programe prije početka procesa instalacije.

Instalacija kancelarijskog paketa LibreOffice na Debian/Ubuntu Linux distribucijama
----------------------------------------------------------------------

Za informacije kako instalirati jezični paket ( nakon instaliranja US English verzije paketa LibreOffice ),molimo pročitajte tekst ispod, pod naslovom Instaliranje Jezičnog Paketa.

Kada raspakujete preuzetu arhivu, vidjet ćete da je sadržaj raspakovan u pod-direktorij. Otvorite prozor za pomoć sa fajlovima, i promijenite direktorij tako da se njegov sadržaj može pokrenuti pomoću "LibreOffice..." , nakon čega slijedi broj verzije i neke informacije o platformi.

Direktorijum sadrži pod-direktorijum sa nazivom "DEBS". Pređite unutar "DEBS"direktorija.

U direktorijumu kliknite desnim klikom i izaberite "Otvori u terminalu". Otvoriće se prozor terminala. Iz komandne linije terminala unesite sljedeću naredbu (da bi se naredba izvršila morate unijeti lozinku root korisnika):

Sljedeće naredbe će instalirati LibreOffice i integracione pakete radne površine (možete ih samo kopirati i zalijepiti na zaslonu terminala, umjesto da ih tipkate):

sudo dpkg -i *.deb

Proces instalacije je sada završen i trebalo bi da sve ikone aplikacija paketa LibreOffice budu dostupne u meniju Aplikacije/Ured.

Instalacija paketa  LibreOffice za Fedora, openSUSE, Mandriva i druge Linux sisteme koji koriste RPM pakete
----------------------------------------------------------------------

Za informacije kako instalirati jezični paket (nakon instaliranja US English verzije paketa LibreOffice), molimo pročitajte tekst ispod pod naslovom Instaliranje jezičkog paketa.

Kada raspakujete preuzetu arhivu, vidjet ćete da je sadržaj raspakovan u pod-direktorij. Otvorite prozor za pomoć sa fajlovima i promijenite direktorij tako da se njegov sadržaj može pokrenuti pomoću "LibreOffice_" , nakon čega slijedi broj verzije i neke informacije o platformi.

Ovaj direktorij sadrži pod-direktorij sa imenom "RPMS". Premjestite se u direktorijum "RPMS".

U direktorijumu kliknite desnim klikom i izaberite "Otvori u terminalu". Otvoriće se prozor terminala. Iz komandne linije terminala unesite sljedeću naredbu (da bi se naredba izvršila morate unijeti lozinku root korisnika):

For Fedora-based systems: sudo dnf install *.rpm

Za sisteme zasnovane na Mandriva distribuciji: sudo urpmi *.rpm

Za ostale sisteme zasnovane na RPM distribuciji (openSUSE, itd.): rpm -Uvh *.rpm

Proces instalacije je sada završen i trebalo bi da sve ikone aplikacija paketa LibreOffice budu dostupne u meniju Aplikacije/Ured.

Alternativno, možete koristiti 'Install' skriptu, koja se nalazi u toplevel direktoriju ove arhive da biste izveli  instalaciju kao korisnik. Skripta će postaviti LibreOffice tako da ima ​vlastiti profil za ovu instalaciju, odvojeno od vašeg regularnog LibreOffice profila. Imajte na umu da to neće instalirati dijelove sistemske integracije, kao što su stavke menija ekrana i registracije tipa MIME ekrana.

Bilješke namijenjene integraciji u radno okruženje za distribucije Linuxa koje nisu obuhvaćene dosadašnjim instrukcijama
----------------------------------------------------------------------

Moguće je jednostavno instalirati paket LibreOffice i na drugim Linux distribucijama koje nisu obuhvaćene u ovom priručniku za instalaciju. Glavne razlike se mogu javiti oko integracije za radno okruženje.

The RPMS (or DEBS, respectively) directory also contains a package named libreoffice7.4-freedesktop-menus-7.4.0.1-1.noarch.rpm (or libreoffice7.4-debian-menus_7.4.0.1-1_all.deb, respectively, or similar). This is a package for all Linux distributions that support the Freedesktop.org specifications/recommendations (https://en.wikipedia.org/wiki/Freedesktop.org), and is provided for installation on other Linux distributions not covered in the aforementioned instructions.

Instalacija jezičkog paketa
----------------------------------------------------------------------

Preuzmite jezički paket za željeni jezik i platformu. Dostupni su sa iste lokacije, kao i glavna instalaciona arhiva. Iz Nautilus upravnika datoteka otpakujte preuzetu arhivu u direktorijum (na primer, Radna površ). Proverite da ste zatvorili sve programe paketa LibreOffice (uključujući i Brzi pokretač u sistemskoj kaseti, ukoliko je pokrenut).

Premjestite se u direktorij gdje ste raspakovali preuzeti jezički paket.

Sada se premjestite u direktorijum koji je stvoren tokom procesa raspakivanja. Na primjer, za francuski jezički paket za 32-bitni Debian/Ubuntu-bazirane sisteme, direktorij se zove LibreOffice_, plus neke informacije o verziji, plus Linux_x86_langpack-deb_fr.

Sada se premjestite u direktorij koji sadrži pakete za instalaciju. Na Debian/Ubuntu-baziranim sistemima, direktorij će biti DEBS. Na Fedora, openSUSE ili Mandriva sistemima, direktorij će biti RPMS.

Iz Nautilus upravnika datoteka, kliknite desnim klikom na direktorij i izaberite opciju "Otvori u terminalu". U prozoru Terminala izvršite komandu za instaliranje jezičkog paketa (pomoću svih navedenih komandi; sistem će od vas vjerovatno tražiti da unesete lozinku root korisnika):

Za sisteme zasnovane na Debian/Ubuntu distribuciji: sudo dpkg -i *.deb

For Fedora-based systems: su -c 'dnf install *.rpm'

Za sisteme zasnovane na Mandriva distribuciji: sudo urpmi *.rpm

Za ostale sisteme koji koriste RPM pakete (openSUSE itd.): rpm -Uvh *.rpm

Pokrenite jednu od LibreOffice aplikacija - na primjer Writer. Idite na meni Alati i izaberite Opcije. U dijalogu za podešavanja kliknite na "Jezičke postavke" i potom na "Jezici". Iz padajuće liste "Korisnički interfejs" odaberite jezik koji ste upravo instalirali. Ukoliko želite možete uraditi isto za "Lokalne postavke", "Podrazumijevana valuta" i "Jezici za dokumente".

Nakon prilagođavanja tih podešavanja, kliknite na OK. Dijaloški prozor će se zatvoriti, a prikazaće se poruka koja kaže da će unete promene biti aktivne nakon ponovnog pokretanja LibreOfficea (takođe morate zaustaviti i Brzi pokretač ukoliko je pokrenut).

Kada naredni put pokrenete LibreOffice, biće preveden na jezik koji ste predhodno instalirali.

----------------------------------------------------------------------
Problemi prilikom pokretanja
----------------------------------------------------------------------

Difficulties starting LibreOffice (e.g. applications hang) as well as problems with the screen display are often caused by the graphics card driver. If these problems occur, please update your graphics card driver or try using the graphics driver delivered with your operating system.

----------------------------------------------------------------------
ALPS/Synaptics dodirna ploča za laptope pod MS Windows-om
----------------------------------------------------------------------

Zbog problema sa drajverom Windows-a, ne možete pomicati LibreOffice dokumente kada vučete prst preko dodirne ploče proizvođača ALPS/Synaptics.

Za uključivanje pomicanja pomoću dodirne ploče, dodajte sljedeće redove u konfiguracijsku datoteku "C:\Program Files\Synaptics\SynTP\SynTPEnh.ini", te restartujte računar:

[LibreOffice]

FC = "SALFRAME"

SF = 0x10000000

SF |= 0x00004000

Lokacija kofiguracijske datoteke može biti različita na različitim verzijama Windows-a.

----------------------------------------------------------------------
Kratice
----------------------------------------------------------------------

Only shortcut keys (key combinations) not used by the operating system can be used in LibreOffice. If a key combination in LibreOffice does not work as described in the LibreOffice Help, check if that shortcut is already used by the operating system. To rectify such conflicts, you can change the keys assigned by your operating system. Alternatively, you can change almost any key assignment in LibreOffice. For more information on this topic, refer to the LibreOffice Help or the Help documentation of your operating system.

----------------------------------------------------------------------
Problems When Sending Documents as Emails From LibreOffice
----------------------------------------------------------------------

When sending a document via 'File - Send - Document as Email' or 'Document as PDF Attachment' problems might occur (program crashes or hangs). This is due to the Windows system file "Mapi" (Messaging Application Programming Interface) which causes problems in some file versions. Unfortunately, the problem cannot be narrowed down to a certain version number. For more information visit https://www.microsoft.com to search the Microsoft Knowledge Base for "mapi dll".

----------------------------------------------------------------------
Važne napomene o pristupačnosti
----------------------------------------------------------------------

For more information on the accessibility features in LibreOffice, see https://www.libreoffice.org/accessibility/

----------------------------------------------------------------------
Podrška korisnicima
----------------------------------------------------------------------

The main support page offers various possibilities for help with LibreOffice. Your question may have already been answered - check the Community Forum at https://www.documentfoundation.org/nabble/ or search the archives of the 'users@libreoffice.org' mailing list at https://www.libreoffice.org/lists/users/. Alternatively, you can send in your questions to users@libreoffice.org. If you like to subscribe to the list (to get email responses), send an empty mail to: users+subscribe@libreoffice.org.

Also check the FAQ section at the LibreOffice website.

----------------------------------------------------------------------
Prijavite greške i probleme
----------------------------------------------------------------------

Our system for reporting, tracking and solving bugs is currently Bugzilla, hosted at https://bugs.documentfoundation.org/. We encourage all users to feel entitled and welcome to report bugs that may arise on your particular platform. Energetic reporting of bugs is one of the most important contributions that the user community can make to the ongoing development and improvement of LibreOffice.

----------------------------------------------------------------------
Uključite se u rad
----------------------------------------------------------------------

LibreOffice zajednica će imati puno koristi od vašeg aktivnog učestvovanja u razvijanju ovog važnog projekta otvorenog koda.

As a user, you are already a valuable part of the suite's development process and we would like to encourage you to take an even more active role with a view to being a long-term contributor to the community. Please join and check out the contributing page at the LibreOffice website.

Kako početi
----------------------------------------------------------------------

The best way to start contributing is to subscribe to one or more of the mailing lists, lurk for a while, and gradually use the mail archives to familiarize yourself with many of the topics covered since the LibreOffice source code was released back in October 2000. When you're comfortable, all you need to do is send an email self-introduction and jump right in. If you are familiar with Open Source Projects, check out our To-Dos list and see if there is anything you would like to help with at the LibreOffice website.

Pretplati se
----------------------------------------------------------------------

Here are a few of the mailing lists to which you can subscribe at https://www.libreoffice.org/get-help/mailing-lists/

* Vijesti: announce@documentfoundation.org *preopručeno za sve korisnike* (slab promet)
* Glavni popis korisnika: users@global.libreoffice.org*jednostavan način da pripazite na diskusije*(prilikom zagušenja)
* Marketing projekt: marketing@global.libreoffice.org *u razvoju* (getting heavy)
* Opšta razvojna lista: libreoffice@lists.freedesktop.org (veliki promet)

Priključivanje jednom ili više projekata
----------------------------------------------------------------------

Možete dati vaš doprinos ovom važnom projektu otvorenog koda čak iako je vaše iskustvo u dizajniranju softvera ograničeno. Da, vi!

Nadamo se da ćete uživati u radu sa novim LibreOffice 7.4 i da ćete nam se pridružiti online.

LibreOffice zajednica

----------------------------------------------------------------------
Korišten / izmijenjen izvorni kod
----------------------------------------------------------------------

Djelomična autorska prava 1998, 1999 James Clark. Portions Copyright 1996, 1998 Netscape Communications Corporation.
