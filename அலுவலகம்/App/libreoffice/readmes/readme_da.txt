
======================================================================
LibreOffice 7.4 ReadMe
======================================================================


Se de seneste opdateringer af denne readme-fil påhttps://git.libreoffice.org/core/tree/master/README.md

Denne fil indeholder vigtige oplysninger om programmet LibreOffice. Du anbefales at læse indholdet inden du begynder at installere.

LibreOffice-fællesskabet er ansvarlig for udviklingen af dette produkt og indbyder dig til overveje at deltage som medlem. Hvis du er ny bruger, kan du besøge LibreOffice-stedet, hvor du vil finde masser af information om LibreOffice-projektet og de fællesskaber, der findes omkring de. Gå til https://www.libreoffice.org

Er LibreOffice virkelig gratis for alle brugere?
----------------------------------------------------------------------

LibreOffice er gratis at bruge for alle. Du må installere denne kopi af LibreOffice på så mange computere, du har lyst til og bruge det til ethvert formål, herunder også professionelt og til uddannelse. For yderligere detaljer kan du læse licensteksten, som du har fået sammen med LibreOffice.

Hvorfor er LibreOffice gratis at bruge for alle?
----------------------------------------------------------------------

Du kan gratis bruge denne kopi af LibreOffice fordi individuelle bidragsydere og kommercielle sponsorer har udviklet, testet, oversat, dokumenteret, støttet og på mange andre måder hjulpet med at gøre LibreOffice til det det er i dag: Verdens ledende open source kontorprogram til hjemmet og arbejdet.

Hvis du sætter pris på den indsats, der bliver gjort af de frivillige, og du vil gerne være med til at sikre ,at LibreOffice også fremover vil være tilgængelig, så overvej at blive bidragsyder - se http://www.documentfoundation.org/contribution/ for oplysninger. Alle kan bidrage med noget. Der er meget andet end programmering, der skal gøres.

----------------------------------------------------------------------
Bemærkninger vedrørende installation
----------------------------------------------------------------------

LibreOffice kræver en nyere version af Java Runtime Environment (JRE) for at opnå fuld funktionalitet. JRE er ikke en del af installationspakken for LibreOffice og skal derfor installeres separat.

Systemkrav
----------------------------------------------------------------------

* Microsoft Windows 7 SP1, 8, 8.1 Update (S14) eller 10

Bemærk: Du skal have administratorrettigheder for at kunne installere programmet.

Registrering af LibreOffice som standardprogram for Microsoft Office-formater kan påtvinges eller undertrykkes ved at bruge følgende kommandolinjeparametre med installationsprogrammet:

* REGISTER_ALL_MSO_TYPES = 1 vil gennemtvinge registrering af LibreOffice som standardprogram for Microsoft Office formater.
* REGISTER_NO_MSO_TYPES = 1 vil undertrykke registrering af LibreOffice som standardprogram for Microsoft Office formater.

Du bør sikre dig, at du har tilstrækkelig fri hukommelse i den midlertidige mappe på dit system. Vær også sikker på, der er tildelt læse-, skrive- og køre-rettigheder for mappen. Luk alle andre programmer før du fortsætter med installationen.

Installation af LibreOffice på Debian/Ubuntu-baserede Linux systemer
----------------------------------------------------------------------

For instruktioner om hvorledes en sprogpakke installeres (efter installation af US English versionen af LibreOffice), læs venligst afsnittet nedenfor, betegnet Installation af en sprogpakke.

Når du udpakker den downloadede pakke, vil du se at indholdet er udpakket til et underbibliotek. Brug dit filhåndteringssystem (f.eks. stifinder) til at skifte til den underfolder der starter med "LibreOffice_" efterfulgt af versionsnummer og platformsinformation.

Denne mappe indeholder en undermappe der hedder "DEBS". Skift mappe til mappen "DEBS".

Højreklik inden i mappen og vælg "Åbn i terminal". Et terminalvindue vises. Fra kommandolinjen i terminalvinduet, skriv de følgende kommandoer (du vil blive spurgt om superbruger/administrator kodeordet før kommandoerne udføres):

Følgende kommando vil installere LibreOffice og skrivebordsintegrationen (du kan med fordel kopiere kommandoen ind i vinduet frem for at indtaste manuelt):

sudo dpkg -i *.deb

Installationen er nu fuldført og alle ikonerne til applikationerne i LibreOffice bør være i din computers programmenu under "Kontor".

Installation af LibreOffice på Fedora, openSUSE, Mandriva og andre Linuxsystemer ved hjælp af RPM-pakker
----------------------------------------------------------------------

For instruktioner om, hvordan du installerer en sprogpakke (efter at have installeret US English versionen af LibreOffice), bedes du læse afsnittet Installation af en sprogpakke.

Når du udpakker det hentede arkiv vil du se, at indholdet er blevet udpakket til en undermappe. Åbn et filhåndteringsvindue, og skift til mappen, der starter med "LibreOffice_", efterfulgt af versionsnummeret og information om platformen.

Denne mappe indeholder en undermappe med navnet "RPMS". Skift mappe til mappen "RPMS".

Højreklik inden i mappen og vælg "Åbn i terminal". Et terminalvindue vises. Fra kommandolinjen i terminalvinduet, skriv de følgende kommandoer (du vil blive spurgt om superbruger/administrator adgangskoden før kommandoerne udføres):

For Fedora-baserede systemer: sudo dnf install *.rpm

For Mandriva-baserede systemer: su urpmi *.rpm

For andre RPM-baserede systemer (openSUSE m. fl.): rpm -Uvh *.rpm

Installationen er nu fuldført og alle ikonerne til applikationerne i LibreOffice bør være i din computers programmenu under "Kontor".

Alternativt kan du bruge skriptet 'install', der findes i det øverste mappeniveau af dette arkiv, for at udføre en installation som en bruger. Skriptet vil opsætte LibreOffice, så det får sin egen profil for denne installation, adskilt fra din normale LibreOffice-profil. Bemærk at det ikke vil installere delene til systemintegration, såsom skrivebordets menuelementer og registreringer af MIME-typer for skrivebordet.

Bemærkninger angående skrivebordsintegration for Linuxdistributioner, som ikke er dækket af ovenstående instruktioner
----------------------------------------------------------------------

Det kan let lade sig gøre at installere LibreOffice på andre Linuxdistributioner, end de der er beskrevet i installationsvejledningerne. Den store forskel ligger i skrivebordsintegrationen.

Katalogerne RPMS (eller DEBS, henholdsvis) indeholder også en pakke kaldet libreoffice7.4-freedesktop-menus-7.4.0.1-1.noarch.rpm (eller libreoffice7.4-debian-menus_7.4.0.1-1_all.deb, henholdsvis, eller lignende). Der en pakke til alle Linux-distributioner, som understøtter Freedesktop.org,s specifikationer/anbefalinger (https://en.wikipedia.org/wiki/Freedesktop.org), og stilles til rådighed for installation til på andre Linux-distributioner, der ikke er dækket i de førnævnte instruktioner.

Installere en sprogpakke
----------------------------------------------------------------------

Download den relevante sprogpakke for det ønskede sprog og platform. De er tilgængelige fra samme sted, som du hentede programinstallationen. Fra Nautilus skal du udpakke det hentede arkiv til en folder (f.eks. en folder på skrivebordet). Vær helt sikker på at du har stoppet alle LibreOfficeprogrammer, herunder også kvikstart.

Skift til den mappe, som du udpakkede den hentede sprogpakke til.

Åbn nu den mappe som blev oprettet ved udpakningsprocessen. F.eks. er mappen ved dansk sprogpakke for et 32-bit Debian/Ubuntu-baseret system navngivet som LibreOffice_ efterfulgt af versionsinformationer og Linux_x86_langpack-deb_da.

Skift nu til det katalog, der indeholder pakkerne, som skal installeres. På Debian/Ubuntu systemer vil kataloget hedde DEBS. På Fedora, Suse og Mandriva vil kataloget hedde RPMS.

Fra Nautilus filhåndtering, højreklik på mappen og vælg "Åbn i terminal". I terminalvinduet som du netop har åbnet skal du eksekvere kommandoen som installerer sprogpakken (med samtlige kommandoer herunder kan du blive spurgt om din root-adgangskode):

For Debian/Ubuntu-baserede systemer: sudo dpkg -i *.deb

For Fedora-baserede systemer: su -c 'dnf install *.rpm'

For Mandriva-baserede systemer: su urpmi *.rpm

For andre RPM-baserede systemer (Suse, etc.): rpm -Uvh *.rpm

Start nu et af LibreOffice programmerne, f.eks. Writer. Brug nu menuen Funktioner og vælg Indstillinger. I dialogen Indstillinger skal du vælge Sprogindstillinger og derefter Sprog. Åbn rullelisten Brugergrænseflade og vælg det sprog du netop har installeret. Hvis du ønsker at vælge en anden placering, vælg da også fra rullelisten Lokalitetsindstillinger, Standard valuta og Standardsprog for dokumenter.

Efter at have foretaget disse indstillinger, klik på OK. Dialogboksen vil nu lukke, og du vil få en besked om, at dine ændringer først træder i kraft, når du afslutter LibreOffice og starter det igen (Husk også at afslut Hurtig Start hvis den kører).

Næste gang du starter LibreOffice, vil programmet starte op i det sprog, du installerede.

----------------------------------------------------------------------
Problemer under programstart
----------------------------------------------------------------------

Vanskeligheder med at starte  LibreOffice (for eksempel at programmet hænger) så vel som problemer med visning på skærmen skyldes ofte grafikkortets driver. Hvis disse problemer opstår, skal du opdatere dit grafikkort eller prøve at bruge den grafikkort-driver, der blev leveret med dit operativsystem.

----------------------------------------------------------------------
ALPS/Synaptics-pegeplade til bærbare i Windows
----------------------------------------------------------------------

På grund af driverproblemer i Windows kan du ikke rulle igennem LibreOffice-dokumenter, når du trækker din finger over en ALPS/Synaptics-pegeplade.

For at aktivere pegepladerulning skal du føje følgende linjer til konfigurationsfilen "C:\Programmer\Synaptics\SynTP\SynTPEnh.ini" og genstarte din computer:

[LibreOffice]

FC = "SALFRAME"

SF = 0x10000000

SF |= 0x00004000

Bemærk: Placeringen af konfigurationsfilen kan variere mellem forskellige versioner af Windows.

----------------------------------------------------------------------
Genvejstaster
----------------------------------------------------------------------

Kun genvejstaster (tastekombinationer), der ikke allerede anvendes af operativsystemet, kan benyttes i LibreOffice. Hvis en kombination i LibreOffice ikke virker som beskrevet i LibreOffice Hjælp, skal du undersøge, om genvejen allerede anvendes af operativsystemet. For at rette op på et sådant sammenfald kan du ændre operativsystemets tastetildeling. Du kan også ændre næsten enhver tastetildeling i LibreOffice. Læs mere i LibreOffice Hjælp eller operativsystemets dokumentation for yderligere oplysninger.

----------------------------------------------------------------------
Problemer ved afsendelse af dokumenter som e-mails fra $ {PRODUCTNAME}
----------------------------------------------------------------------

Når du sender et dokument via ‘Filer – Send –  E-maildokument’ eller ‘E-mail som PDF…’, kan der opstå problemer (programmet bryder ned eller hænger). Det skyldes Windows-systemfilen “Mapi” (Messaging Application Programming Interface), som afstedkommer problemer i nogle filversioner. Desværre kan problemet ikke indkrænkes til et bestemt versionsnummer. Find flere oplysninger ved at besøge https://www.microsoft.com og søge i Microsoft Knowledge Base efter "mapi dll“.

----------------------------------------------------------------------
Vigtige tilgængelighedsnoter
----------------------------------------------------------------------

Se mere information om tilgængeligheds-funktioner i LibreOffice på https://www.libreoffice.org/accessibility/

----------------------------------------------------------------------
Brugerhjælp
----------------------------------------------------------------------

Supportsiden https://www.libreoffice.org/get-help/community-support/ giver forskellige mulighed for hjælp til LibreOffice. Dit spørgsmål er måske allerede blevet besvaret -- check fællesskabet forum påhttps://www.documentfoundation.org/nabble/ eller søg i arkivet for postlisten 'users@libreoffice.org' på https://www.libreoffice.org/lists/users/. du kan også sende dine spørgsmål til users@libreoffice.org. Hvis du gerne vil abonnere på listen (så du får svar pr. e-mail, sender du en tom mail til: users+subscribe@libreoffice.org.

Check også FAQ/OSS-afsnittet på LibreOffices websted.

----------------------------------------------------------------------
Rapportering af fejl & mangler
----------------------------------------------------------------------

Vores system til fejlhåndtering er BugZilla på https://bugs.documentfoundation.org/. Vi opfordrer alle brugere til at føle sig berettigede og velkomne til rapportere fejl, som måtte opstå på din særlige platform. Energisk indrapportering af fejl er et af de vigtigste bidrag, som fællesskabet kan yde til det fortløbende arbejde med at forbedre LibreOffice.

----------------------------------------------------------------------
Deltag
----------------------------------------------------------------------

Fællesskabet bag LibreOffice vil få stor glæde af din aktive deltagelse i udviklingen af dette vigtige 'fri software'-projekt.

Som bruger er du allerede en vigtig del af programpakkens udviklingsproces, og vi vil gerne opmuntre dig til at tage en mere aktiv rolle med udsigten til at blive langsigtet bidragyder i fællesskabet. Meld dig til og tag et kig på siden bidrags-siden på LibreOffice's webside.

Sådan kommer du igang
----------------------------------------------------------------------

Den bedste måde at starte deltagelse på, er ved at tilmelde sig en eller flere postlister og så følge med i snakken for en tid. Begynd også gradvist at kigge i postarkivet for at gøre dig bekendt med flere af de emner, der er blevet omtalt siden LibreOffice-kildekoden blev frigivet tilbage i oktober 2000. Når du føler dig godt hjemme, skal du blot sende en kort introduktion af dig selv til den eller de relevante liste(r) og gå i gang. Hvis du er bekendt med, hvordan open source-projekter fungerer, kan du kigge på vores opgaveliste og se, om der er noget, du har lyst til at hjælpe med: LibreOffice's websted.

Abonner
----------------------------------------------------------------------

Her er nogle få af de post-lister, du kan abonnere på:https://www.libreoffice.org/get-help/mailing-lists/

* Nyheder: announce@documentfoundation.org *anbefales til alle brugere* (let trafik)
* Brugerspørgsmål: users@global.libreoffice.org *let måde at komme ind i sagerne på* (meget trafik)
* Marketingprojektet: marketing@global.libreoffice.org *ikke om programmering* (mere og mere trafik)
* Overordnet liste for udviklere: libreoffice@lists.freedesktop.org (meget trafik)

Tilslutte sig til et eller flere projekter
----------------------------------------------------------------------

Du kan give betydelige bidrag til dette vigtige 'åben software'-projekt, selvom du har begrænset erfaring med programmering og systemudvikling. Ja, dig!

Vi håber, at du får stor fornøjelse med at bruge den nye LibreOffice 7.4, samt at du vil tilmelde dig projektet online.

Fællesskabet bag LibreOffice

----------------------------------------------------------------------
Anvendt/ændret kildetekst
----------------------------------------------------------------------

Delvis ophavsret 1998, 1999 James Clark. Delvis ophavsret 1996, 1998 Netscape Communications Corporation.
