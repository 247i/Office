
======================================================================
LibreOffice 7.4 PročitajMe
======================================================================


Pregledaj zadnje promjene ove readme-datoteke na https://git.libreoffice.org/core/tree/master/README.md

Ova datoteka sadrži bitne informacije o programskom paketu LibreOffice. Preporučujemo vam da pažljivo pročitate ove informacije prije pokretanja instalacije.

LibreOfficeova je zajednica odgovorna za razvoj ovoga proizvoda te poziva i tebe da postaneš članom zajednice. Ako si novi korisnik, posjeti LibreOfficeovu stranicu jer tamo možeš pronaći više informacija o LibreOfficeu i zajednicama oko ovoga projekta. Posjeti https://www.libreoffice.org/.

Je li LibreOffice stvarno besplatan za bilo kojeg korisnika?
----------------------------------------------------------------------

LibreOffice mogu slobodno koristiti svi. Ovu kopiju LibreOfficea možete instalirati na koliko god računala želite i koristiti u koju god svrhu želite (komercijalne, državne, administrativne i edukacijske). Za više informacija pogledajte tekst licence uklopljen u preuzetu inačicu LibreOfficea.

Zašto je LibreOffice besplatan za bilo kojeg korisnika?
----------------------------------------------------------------------

Ovu kopiju LibreOffice možete koristiti bez naplate jer su se pojedinci i korporativni sponzori udružili i dizajnirali, razvili, testirali, preveli, dokumentirali, podržali, reklamirali ili pomogli na druge načine u stvaranju današnje inačice LibreOffice paketa – vodećeg uredskog paketa otvorenog koda.

Smatrate da je trud zajednice hvale vrijedan i željeli biste pomoći da LibreOffice bude korisnicima dostupan i u dalekoj budućnosti, razmislite o tome da pridonesete projektu. Više informacija možete pronaći na https://www.documentfoundation.org/contribution/. Svatko može pomoći - na ovaj ili onaj način.

----------------------------------------------------------------------
Zabilješke o instalaciji
----------------------------------------------------------------------

LibreOffice zahtjeva noviju inačicu Java Runtime Environment (JRE) za potpunu funkcionalnost. JRE nije dio LibreOffice instalacijskog paketa i treba se instalirati odvojeno.

Zahtjevi prema sustavu
----------------------------------------------------------------------

* Microsoft Windows 7 SP1, 8, 8.1 Ažuriranje (S14) ili 10

Potrebna su vam administratorska prava za proces instalacije.

Registracija LibreOffice kao zadanog programa za upravljanje Microsoft Office formatima može se prsiliti ili onemogućiti korištenjem sljedećih naredbi u instalaciji:

* REGISTER_ALL_MSO_TYPES=1 će registrirati LibreOffice kao zadani program za Microsoft Office datoteke.
* REGISTER_NO_MSO_TYPES=1 će ukloniti registraciju LibreOffice kao zadanog programa za Microsoft Office datoteke.

Provjerite imate li dovoljno slobodne memorije u privremenoj mapi na vašem sustavu, te se uvjerite da su vam odobrena prava čitanja, pisanja i izvršavanja. Zatvorite sve druge programe prije pokretanja instalacije.

Instalacija LibreOffice na sustave bazirane na Debian/Ubuntu
----------------------------------------------------------------------

Za upute kako instalirati jezični paket (nakon instalacije engleske SAD LibreOffice inačice), pročitajte niže navedeni odjeljak naslovljen Instalacija jezičnog paketa.

Kada otpakirate preuzetu arhivu, vidjet ćete da je sadržaj raspoređen u podmapu. Preglednikom datoteka otvorite mapu čije ime počinje s „LibreOffice_” iza kojega slijedi broj inačice i neke informacije o platformi.

Ova mapa sadrži podmapu naziva „DEBS”. Promjenite mapu u „DEBS”.

Kliknite desnom tipkom miša u mapu i odaberite naredbu „Otvori u terminalu”. Otvorit će se prozor terminala. U naredbenom retku izvršite sljedeću naredbu (od Vas će biti zatražena root lozinka prije izvršenja naredbe):

Sljedeće će naredbe instalirati LibreOffice i pakete za integraciju s radnom površinom (možete ih samo kopirati i zalijepiti u terminal umjesto da ih pokušavate upisati):

sudo dpkg -i *.deb

Instalacijski proces je završen te biste trebali imati ikone svih LibreOffice modula u izborniku Programi/Ured.

Instalacija LibreOffice na Fodoru, openSUSE, Mandrivu i druge Linux sustave koristeći RPM pakete
----------------------------------------------------------------------

Za upute kako instalirati jezični paket (nakon instalacije engleske SAD LibreOffice inačice), pročitajte niže navedeni odjeljak naslovljen Instalacija jezičnog paketa.

Kada otpakirate preuzetu arhivu, vidjet ćete da je sadržaj raspoređen u podmapu. Preglednikom datoteka otvorite mapu čije ime počinje s „LibreOffice_” iza kojega slijedi broj inačice i neke informacije o platformi.

Ova mapa sadrži podmapu naziva „RPMS”. Promjenite mapu u „RPMS”.

Kliknite desnom tipkom miša u mapu i odaberite naredbu „Otvori u terminalu”. Otvorit će se prozor terminala. U naredbenom retku izvršite sljedeću naredbu (od Vas će biti zatražena root lozinka prije izvršenja naredbe):

Za sustave temeljene na Fedori: sudo dnf install *.rpm

Sustavi temeljeni na Mandriva: sudo urpmi *.rpm

Za ostale sustave bazirane na RPM (openSUSE, etc.): rpm -Uvh *.rpm

Instalacijski proces je završen te biste trebali imati ikone svih LibreOffice modula u izborniku Programi/Ured.

Alternativno, možete koristiti 'install' skriptu, koja se nalazi u vršnom direktoriju ove arhive kako biste napravili instalaciju kao korisnik. Skripta će postaviti vlastiti LibreOffice profil za ovu instalaciju, odvojeno od standardnog LibreOffice profila. Ovo neće instalirati dijelove sistemske integracije kao što su stavke izbornika radne površine i registracije MIME tipa radne površine.

Bilješke u vezi integracije u radnu površinu za Linux distribucije koje nisu naznačene u prethodnim uputstvima za instalaciju
----------------------------------------------------------------------

Trebalo bi biti moguće lako instalirati LibreOffice na druge Linux distribucije koje nisu pokrivene ovim uputstvima. Glavni dio u kojem se može naići na razlike je integracija sa radnom površinom.

RPMS (ili DEBS) mapa također sadrži paket s imenom libreoffice7.4-freedesktop-menus-7.4.0.1-1.noarch.rpm (ili libreoffice7.4-debian-menus_7.4.0.1-1_all.deb, ili sličnim). Ovo je paket za sve Linux distribucije koje podržavaju Freedesktop.org specifikacije/preporuke (https://en.wikipedia.org/wiki/Freedesktop.org) i dan je za instalaciju na ostale Linux distribucije koje nisu pokrivene u navedenim uputama.

Instalacija jezičnog paketa
----------------------------------------------------------------------

Preuzmite jezični paket vašeg željenog jezika i platforme. Paketi su dostupni na istom mjestu kao i glavna instalacijska arhiva. Iz upravitelja datotekama Nautilus, otpakirajte preuzetu arhivu u mapu (na primjer, radna površina). Provjerite jeste i isključili sve programe paketa LibreOffice (uključujući i Brzo pokretanje, ukoliko je pokrenut).

Otvorite mapu u kojoj je otpakiran preuzeti jezični paket.

Otvorite mapu koju ste stvorili tijekom raspakiravanja. Naprimjer, za francuski jezični paket za platformu baziranu na 32-bitnom Debian/Ubuntu sustavu, mapa će se zvati LibreOffice_, plus informacije o inačici, plus Linux_x86_langpack-deb_fr.

Sada otvorite mapu koja sadrži instalacijske pakete. Na Debian/Ubuntu baziranim sustavima, postojat će mapa DEBS. Na Fedori, openSUSE-u ili Mandrivi, postojat će mapa RPMS.

Iz upravljača za datoteke Nautilus, izvršite desni klik na mapu i odaberite naredbu „Otvori u terminalu”. U prozoru terminala, koji se upravo otvorio, izvršite naredbu za instaliranje jezičnog paketa (sa svim dolje napisanim naredbama, biti ćete upitani za upis lozinke korisnika root):

Za sustave bazirane na Debian/Ubuntu: sudo dpkg -i *.deb

Za Fedora temeljene sustave: su -c 'dnf install *.rpm'

Sustavi temeljeni na Mandriva: sudo urpmi *.rpm

Za ostale sustave koji koriste RPM (openSUSE, etc.): rpm -Uvh *.rpm

Sada pokrenite jedan od LibreOffice programa - na primjer Writer. Odaberite izbornik Alati i odaberite Mogućnosti. U dijaloškom okviru Mogućnosti kliknite na Jezične postavke te nakon toga na Jezici. Kliknite na padajući izbornik Korisničko sučelje te odaberite jezik koji ste instalirali. Ukoliko želite, izmijenite postavke u Lokalne postavke, Zadana valuta i Zadani jezici za dokumente.

Nakon prilagodbe ovih postavki, kliknite na 'U redu'. Dijaloški okvir će se zatvoriti i vidjet ćete poruku, da će vaše izmjene biti primjenjene tek nakon što izađete iz LibreOffice i ponovo ga pokrenete (nemojte zaboraviti isključiti Brzo pokretanje ukoliko je uključeno).

Sljedeći put kad pokrenete LibreOffice, pokrenuti će se jezik koj iste upravo instalirali.

----------------------------------------------------------------------
Problemi prilikom pokretanja programa
----------------------------------------------------------------------

Poteškoće s pokretanjem LibreOffice (npr. prekid programa) kao i problemi s ekranom često su uzrokovani upravljačkim programom grafičke kartice. Ako se ovi problemi pojave, aktualiziraj upravljački program grafičke kartice ili pokušaj koristiti grafički upravljački program tvog operacijskog sustava.

----------------------------------------------------------------------
ALPS/Synaptics dodirna ploča za prijenosna računala pod MS Windows
----------------------------------------------------------------------

Zbog problema s upravljačkim programom Windowsa, ne možete klizati kroz LibreOffice dokumente, kad pomićete prst preko taktilne ploče proizvođača ALPS/Synaptics.

Omogućite klizanje pomoću dodirne ploče, dodajući sljedeće retke u konfiguracijsku datoteku „C:\Program Files\Synaptics\SynTP\SynTPEnh.ini”, te ponovo pokrenite računalo:

[LibreOffice]

FC = "SALFRAME"

SF = 0x10000000

SF |= 0x00004000

Smještaj konfiguracijske datoteke može se razlikovati kod različitih inačica Windowsa.

----------------------------------------------------------------------
Prečice
----------------------------------------------------------------------

U LibreOfficeu se mogu koristiti samo tipkovničke kratice (kombinacije tipaka) koje ne koristi operativni sustav. Ako u LibreOfficeu kombinacija tipki ne radi kao što je opisano u LibreOffice Pomoći, provjerite ne koristi li već te kratice operativni sustav. Možete promjeniti kratice vašeg operativnog sustava kako biste ispravili ove konflikte. Uostalom, LibreOffice omogućuje promjenu gotovo svih tipkovničkih kratica. Radi više informacija pogledajte LibreOffice Pomoć ili Pomoć vašeg operativnog sustava.

----------------------------------------------------------------------
Problemi prilikom slanja dokumenata kao e-maila od LibreOffice
----------------------------------------------------------------------

Prilikom slanja dokumenta putem „Datoteka - Pošalji - Dokument kao e-mail” ili „Dokument kao PDF prilog” mogu se pojaviti problemi (program prekida rad ili ne radi). Uzrok tome je datoteka Windows sustava „Mapi” (Messaging Application Programming Interface) koja uzrokuje probleme u nekim verzijama datoteka. Nažalost, problem se ne može suziti na određeni broj verzije. Za daljnje informacije posjeti https://www.microsoft.com za pretraživanje Microsoftove baze znanja za „mapi dll”.

----------------------------------------------------------------------
Važne napomene o pristupačnosti
----------------------------------------------------------------------

Za više informacija o funkcijama za pristupačnost u LibreOffice, pogledajte na https://www.libreoffice.org/accessibility/

----------------------------------------------------------------------
Podrška korisnicima
----------------------------------------------------------------------

Glavna stranica za podršku nudi razne mogućnosti pomoći za LibreOffice. Za vaše pitanje možda već postoji odgovor – provjerite forum zajednice na https://www.documentfoundation.org/nabble/ ili pretražite arhivu pretplatničke liste „users@libreoffice.org” na https://www.libreoffice.org/lists/users/. Pitanja možete slati i na users@libreoffice.org. Želite li se prijaviti na pretplatničku listu kako biste dobili odgovore na e-poštu, pošaljite praznu e-poruku na users+subscribe@libreoffice.org.

Proverite FAQ odlomak na  LibreOffice web site-u.

----------------------------------------------------------------------
Prijavljivanje nedostataka i problema
----------------------------------------------------------------------

BugZilla je naš trenutačni sustav za prijavljivanje, praćenje i rješavanje grešaka host-ana je nahttps://bugs.documentfoundation.org/. Pozivamo sve korisnike da prijavljuju greške koje se mogu pojaviti na vašim platformama. Često prijavljivanje grešaka jedan je od najvažnijih doprinosa koji zajednica korisnika može napraviti za kontinuirani razvoj i napredak LibreOffice.

----------------------------------------------------------------------
Uključivanje u projekt
----------------------------------------------------------------------

LibreOffice zajednica može uvelike prosperirati vašim aktivnim doprinosom u razvoju ovog važnog open source projekta.

Kao korisnik, Vi ste već vrijedan član procesa razvijanja paketa i voljeli bismo vas potaknuti da se još aktivnije uključite i eventualno postanete dugoročni suradnik zajednice. Pridružite se i pogledajte stranicu doprinosa na  LibreOffice web site-u

Kako početi
----------------------------------------------------------------------

Želite li započeti pridonositi, najbolji je način pretplatiti se na jednu ili više pretplatničkih lista, neko vrijeme promatrati i kroz arhive se postupno upoznavati s temama aktualiziranima još otkako je objavljen izvorni kȏd LibreOffice u listopadu 2000. Kad se opustite, sve što trebate jest predstaviti se u poruci i – uključiti se. Ako ste upoznati s drugim projektima otvorenog koda, provjerite popis zadataka na LibreOffice web stranicama.

Pretplata
----------------------------------------------------------------------

Ovdje je nekoliko popisa skupnih e-poruka projekata na koje se možete prijaviti https://www.libreoffice.org/get-help/mailing-lists/

* Novosti: announce@documentfoundation.org *preporučeno svim korisnicima* (mali promet)
* Glavni korisnički popis primatelja: users@global.libreoffice.org *lagani način vrebanja rasprava* (veliki promet)
* Marketing projekt: marketing@global.libreoffice.org *iznad razvoja* (počinje imati veliki promet)
* Opći popis skupne e-pošte za razvijatelje: libreoffice@lists.freedesktop.org (velik promet)

Pridruživanje jednom ili više projekata
----------------------------------------------------------------------

I vi možete dati velik doprinos ovom važnom projektu otvorenog koda čak i ako imate malo iskustva u oblikovanju ili programiranju softvera. Da, vi!

Nadamo se da ste uživali u radu s novom LibreOffice 7.4 inačicom i da ćete nam se pridružiti na webu.

Zajednica LibreOffice

----------------------------------------------------------------------
Korišteni/promijenjeni izvorni kȏd
----------------------------------------------------------------------

Djelomično autorsko pravo 1998, 1999 James Clark. Djelomično autorsko pravo 1996, 1998 Netscape Communications Corporation.
