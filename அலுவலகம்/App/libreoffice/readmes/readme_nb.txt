
======================================================================
LibreOffice 7.4 Om
======================================================================


For den seneste oppdateringen tildenne  readme filen, se https://git.libreoffice.org/core/tree/master/README.md

Denne filen inneholder viktig informasjon om LibreOffice. Det anbefales at man leser denne informasjonen nøye før installasjon.

Miljøet rundt LibreOffice er ansvarlig for utviklingen av dette produktet og inviterer deg til å bli en del av samarbeidet som bidragsyter. Hvis du er en ny bruker, kan du besøke nettstedet til LibreOffice. Der vil du finne masse informasjon om prosjektet LibreOffice og miljøet som eksisterer rundt det. Besøkhttp://www.libreoffice.org/.

Er LibreOffice virkelig gratis for alle?
----------------------------------------------------------------------

LibreOffice er gratis å bruke for alle. Du kan installere dette eksemplaret av LibreOffice på så mange datamaskiner du vil, og bruke det til hva du vil (gjelder også bruk i det offentlige, i næringslivet og innen utdanning). Du kan lese mer om vilkårene i lisensteksten som følger med denne nedlastingen av LibreOffice.

Hvorfor er LibreOffice gratis for alle?
----------------------------------------------------------------------

Denne kopien av LibreOffice kan brukes gratis fordi individuelle bidragsytere og bedriftssponsorer har laget, utviklet, testet, oversatt, dokumentert, støttet, markedsført og hjulpet til på mange andre måter for å gjøre LibreOffice til det er i dag – verdens ledende Åpen kildekode-produktivitetgruppevare for hjem og kontor.

Hvis du verdsetter innsatsen deres og vil sørge for at LibreOffice fortsetter å være tilgjengelig langt inn i fremtiden, kan du vurdere å bidra til prosjektet. For nærmere informasjon:http://www.documentfoundation.org/contribution/. Alle kan bidra med noe.

----------------------------------------------------------------------
Merknader om installasjon
----------------------------------------------------------------------

LibreOffice krever en nyere versjon av Java (JRE) for å kunne ta i bruk alle funksjoner. JRE er ikke en del av installasjonspakken for LibreOffice og må derfor installeres separat.

Systemkrav
----------------------------------------------------------------------

* Microsoft Windows 7 SP1, 8, 8.1 Update (S14) eller 10

Administratorrettigheter kreves for å installere programmet.

Du kan angi at LibreOffice skal brukes som standardprogram når du åpner filer fra Microsoft Office-programmer. Under installasjonen kan du gjøre dette ved å bruke følgende kommandolinjevalg:

* REGISTER_ALL_MSO_TYPES=1 gjør LibreOffice til standardprogrammet for Microsoft Office-formater.
* REGISTER_NO_MSO_TYPES=1 forhindrer LibreOffice i å bli standardprogrammet for Microsoft Office-formater.

Kontroller at det er nok tilgjengelig plass i mappen for midlertidige filer i operativsystemet og at du har lese-, skrive- og kjørerettigheter i denne mappen. Lukk alle andre program før du starter installasjonen.

Installasjon av LibreOffice på Debian/Ubuntu-baserte Linux-systemer
----------------------------------------------------------------------

Les avsnittet med navnet «Installasjon av en språkpakke» nedenfor for å se hvordan du kan installere en lokal språkpakke (etter å ha installert US-engelsk-versjonen av LibreOffice).

Når du pakker ut nedlastingen vil du se at innholdet er fordelt på undermapper. Åpne filbehandleren og bytt til undermapen kalt «LibreOffice» etterfulgt av versjonsnummeret og informasjon om hvilken plattform installasjonen er laget for.

Denne mappen inneholder en undermappe kalt «DEBS». Bytt til denne mappen.

Høyreklikk i mappen og velg «Åpne i terminal». Et terminalvindu vises. Fra kommandolinjen i terminalvinduet, skriv den følgende kommandoen (du vil bli spurt om å oppgi passordet til superbruker/administrator før kjøring av kommandoen):

Denne kommandoen vil installere LibreOffice og skrivebordsintegrasjonen. (Det enkleste er å  kopiere og lime inn kommandoen i vinduet i stedet for å skrive den inn manuelt):

sudo dpkg -i *.deb

Installasjonprosessen er nå fullført, og ikoner for alle programmer i LibreOffice skal være tilgjengelige i skrivebordets program-/kontormeny.

Installasjon av LibreOffice på Fedora, openSUSE, Mageia og andre Linux-system ved hjelp av RPM-pakker.
----------------------------------------------------------------------

Les avsnittet med navnet «Installasjon av en språkpakke» nedenfor for å se hvordan du kan installere en lokal språkpakke (etter å ha installert US-engelsk-versjonen av LibreOffice).

Når du pakker ut nedlastingen vil du se at innholdet er fordelt på undermapper. Åpne filbehandleren og bytt til undermappen kalt «LibreOffice» etterfulgt av versjonsnummeret og informasjon om hvilken plattform installasjonen er laget for.

Denne mappen inneholder en undermappe kalt «RPMS». Bytt til denne mappen.

Høyreklikk i mappen og velg «Åpne i terminal». Et terminalvindu vises. Fra kommandolinjen i terminalvinduet, skriv den følgende kommandoen (du vil bli spurt om å oppgi passordet til superbruker/administrator før kjøring av kommandoen):

For Fedora-baserte systemer: sudo dnf install *.rpm

For Mageia-baserte systemer: su -c urpmi *.rpm

For andre RPM-baserte system (openSUSE osv.): rpm -Uvh *.rpm

Installasjonprosessen er nå fullført, og ikoner for alle programmer i LibreOffice skal være tilgjengelige i skrivebordets program-/kontormeny.

Alternativt kan du bruke skriptet «install» fra den øverste mappen i dette arkivet for å installere programmet som en bruker. Skriptet vil sette opp en egen profil for denne installasjonen av LibreOffice, adskilt fra den normale LibreOffice-profilen. Vær klar over at dette ikke vil installere komponentene for systemintegrasjon, slik menyoppføringer og MIME-typer.

Merknader for skrivebordintegrasjon i Linux-distribusjoner som ikke ble dekket i installasjonveiledningen over
----------------------------------------------------------------------

Det er forholdsvis enkelt å installere LibreOffice på andre Linux-distribusjoner som ikke dekkes i installasjonveiledningen. Integrasjonen av programvaren på skrivebordet kan variere.

Mappen RPMS (eller eventuelt DEBS) inneholder også en pakke kalt libreoffice7.4-freedesktop-menus-7.4.noarch.rpm(or libreoffice7.4-debian-menus_7.4.0.1-1_all.deb, respectively eller lignende). Dette er en pakke for alle Linux-distribusjoner som støtter spesifikasjonene/anbefalingene til Freedesktop.org (http://en.wikipedia.org/wiki/Freedesktop.org) og er gjort tilgjengelig for installasjon på Linux-distribusjoner som ikke er dekket av de foregående instruksjonene.

Installasjon av en språkpakke
----------------------------------------------------------------------

Last ned språkpakken for det ønskede språket og plattform. De er tilgjengelige fra det samme stedet som standardinstallasjonen. Fra filbehandleren, pakk ut den nedlastede arkivet i en mappe (for eksempel skrivebordet). Sørg for at du har avsluttet alle programmer i LibreOffice (inkludert hurtigstarteren, hvis påslått.)

Bytt til mappen der den nedlastede språkpakken ble pakket ut.

Åpne mappen som ble opprettet under utpakkingen. For eksempel vil mappen med norsk språkpakke for et 32 bit Debian/Ubuntu-basert system ha navnet LibreOffice_ med versjonsnummer og Linux_x86_langpack-deb_nb.

Bytt til mappen som inneholder pakkene som skal installeres. På Debian/Ubuntu-baserte systemer vil mappen hete DEBS. På Fedora-, openSUSE- og Mageia-baserte systemer vil mappen hete RPMS.

Fra filebehandleren, høyreklikk i mappen og velg kommandoen «Åpne i terminal». I terminalvinduet, kjør kommandoen for å installere språkpakkene (kommandoene under vil kanskje kreve passordet til superbruker):

For Debian/Ubuntu-baserte systemer: sudo dpkg -i *.deb

For Fedora-baserte systemer: su -c 'dnf install *.rpm'

For Mageia-baserte systemer: su -c urpmi *.rpm

For andre RPM-baserte systemer (openSUSE, osv.): rpm -Uvh *.rpm

Start opp et av programmene i LibreOffice, for eksempel Writer. Gå til menyen «Verktøy» og velg «Innstillinger». I dialogvinduet «Innstillinger», trykk på «Språkinnstillinger» og velg «Språk». Velg listen i rullegardinmenyen «Brukergrensesnittet» og språket som ble installert. Hvis ønskelig, gjør det samme med «Lokale innstillinger», «Standard valuta» og «Standardspråk for dokumenter».

Etter å ha justert innstillingene, trykk på OK. Dialogvinduet vil lukkes og en melding om at innstillingene vil tre i bruk ved neste oppstart av LibreOffice vises. Start programmet på nytt (husk også å lukke hurtigstart.)

Neste gang LibreOffice starter, vil det starte i språket du nettopp installerte.

----------------------------------------------------------------------
Problem ved programoppstart
----------------------------------------------------------------------

Vanskeligheter med å starte LibreOffice (f.eks. at Apper henger) samt problemer med skjermvisningen skyldes ofte grafikkortdriveren. Hvis disse problemene oppstår, må du oppdatere grafikkortdriveren eller prøve å bruke grafikkdriveren som fulgte med operativsystemet.

----------------------------------------------------------------------
ALPS/Synaptics-styreplater i Windows
----------------------------------------------------------------------

På grunn av en driverfeil kan du ikke rulle i et LibreOffice-dokument når du bruker en styreplate fra ALPS/Synaptics.

For å kunne rulle med en styreplate, legg inn følgende linjer i oppsettfilen C:\Program Files\Synaptics\SynTP\SynTPEnh.ini og start datamaskinen på nytt:

[LibreOffice]

FC = "SALFRAME"

SF = 0x10000000

SF |= 0x00004000

Merknad: Plasseringen av oppsettsfilen kan variere på ulike versjoner av Windows.

----------------------------------------------------------------------
Hurtigtaster
----------------------------------------------------------------------

Bare hurtigtaster (tastekombinasjoner) som ikke blir brukt i operativsystemet kan brukes i LibreOffice. Dersom en tastekombinasjon i LibreOffice ikke virker som det står i hjelpetekstene til LibreOffice, se om hurtigtasten allerede er i bruk av operativsystemet. For å løse slike konflikter kan du endre tastetilordningene i operativsystemet ditt. Du kan også endre nesten alle tastekombinasjonene i LibreOffice. For mer informasjon om dette emnet, se hjelpen i LibreOffice eller dokumentasjonen for operativsystemet ditt.

----------------------------------------------------------------------
Problemer når du sender dokumenter som e-post fra LibreOffice
----------------------------------------------------------------------

Når du sender et dokument via 'Fil - Send - Dokument som E-Post' eller 'Dokument som PDF Vedlegg', kan det oppstå problemer (program krasjer eller henger seg). Dette skyldes Windows-systemfilen "Mapi" (Messaging Application Programming Interface) som forårsaker problemer i noen filversjoner. Dessverre kan ikke problemet begrenses til et bestemt versjonsnummer. For mer informasjon besøk 1  https: //www.microsoft.com2  for å søke i Microsoft Knowledge Base etter "folder dll".

----------------------------------------------------------------------
Viktig informasjon om tilgjengelighet
----------------------------------------------------------------------

For mer informasjon om tilgjengelighetstøtten i LibreOffice, sehttp://www.libreoffice.org/accessibility/

----------------------------------------------------------------------
Brukerstøtte
----------------------------------------------------------------------

Hovedsiden for brukerstøtte http://www.libreoffice.org/support, tilbyr en rekke muligheter med tanke på brukerstøtte for LibreOffice. Ditt spørsmål har kanskje allerede blitt besvart - kontroller forumet på http://www.documentfoundation.org/nabble/ eller søk i arkivet til e-postlisten «users@libreoffice.org» på http://www.libreoffice.org/lists/users/. Alternativt, kan du sende dine spørsmål til users@libreoffice.org. Hvis du vil abonnere på listen (for å få tilbakemeldinger på e-post), send en tom e-post til: users+subscribe@libreoffice.org.

Se også FAQ på the LibreOffice website.

----------------------------------------------------------------------
Rapporter inn feil & problemer
----------------------------------------------------------------------

Systemet for rapportering, sporing og løsning av feil er for øyeblikket BugZilla, påhttps://buhttps://bugs.documentfoundation.org. Vi oppfordrer alle brukere som føler seg forpliktet, til å rapportere feil som måtte dukke opp på deres spesifikke plattform. Aktiv feilrapportering er et av de mest verdifulle bidragene brukermiljøet kommer med i forhold til den pågående utviklingen og forbedringen av LibreOffice.

----------------------------------------------------------------------
Bli involvert
----------------------------------------------------------------------

LibreOffice-miljøet vil ha stor hjelp av at du deltar aktivt i utviklingen av dette viktige fri programvare-prosjektet.

Som bruker, er du allerede en verdifull del av programvarens utviklingsprosess og vi vil oppmuntre deg til å ta en mer aktiv rolle som bidragsyter i miljøet. Bli med og les mer på siden for bidragsytere http://www.libreoffi ce.org/contribution/

Hvordan komme i gang
----------------------------------------------------------------------

Hvis du ønsker å bidra, anbefaler vi å starte med ett abonnement på en eller flere av e-postlistene. Følg med en stund og ta gradvis i bruk e-postarkivene for å gjøre deg kjent med mange av temaene som er dekket siden kildekoden til LibreOffice ble gjort tilgjengelig i oktober 2000. Når du føler deg klar, trenger du kun å sende en e-post der du introduserer deg selv og hopper i det. Hvis du allerede er kjent med Åpen kildekode-prosjekter, kan du ta en titt på listen med oppgaver http://www.libreoffice.org/develop/ og se om det er noe du kan hjelpe til med.

Abonner
----------------------------------------------------------------------

Her er noen av epostlistene man kan abonnere på http://www.libreoffice.org/contribution/

* Nyheter: announce@documentfoundation.org *anbefales for alle brukere* (liten trafikk)
* Hovedliste for brukere: users@libreoffice.org *enkelt å følge med på diskusjoner* (mye trafikk)
* Markedsføringprosjekt: marketing@libreoffice.org *utover utvikling* (begynner å bli belastet)
* Generell utviklerliste: libreoffice@lists.freedesktop.org (høy trafikk)

Bli medlem av et eller flere prosjekter
----------------------------------------------------------------------

Du kan gjøre mye for prosjektet selv om du ikke har noe erfaring med programvareutvikling og programmering. Ja, du ja!

Vi håper du har glede av å arbeide med LibreOffice 7.4 og at vi snart møter deg på nettet.

LibreOffice-miljøet

----------------------------------------------------------------------
Brukt/endret kildekode
----------------------------------------------------------------------

Deler med opphavsrett 1998, 1999 tilhørende Jack Clark. Deler med opphavsrett 1996, 1996 Netscape Communications Corporation.
