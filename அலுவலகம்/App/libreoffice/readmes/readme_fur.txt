
======================================================================
File leimi di LibreOffice 7.4
======================================================================


Par consultâ i ultins inzornaments a chest file leimi, bute un voli su https://git.libreoffice.org/core/tree/master/README.md

Chest file al conten informazions impuartantis sul program LibreOffice. Prime di scomençâ la instalazion, us conseìn di lei une vore ben chestis informazions.

La comunitât di LibreOffice e je responsabile dal disvilup di chest prodot e us invide a considerâ la vuestre partecipazion come membris de comunitât. Se si è gnûfs utents, al è pussibil visitâ il sît di LibreOffice, dulà che o cjatarês tantis informazions sul progjet LibreOffice e lis comunitâts che i stan tor ator. Visitait la direzion https://www.libreoffice.org.

Isal LibreOffice pardabon libar par ducj?
----------------------------------------------------------------------

Ducj a son libars di doprâ LibreOffice. Tu puedis cjapâ cheste copie di LibreOffice e instalâle su ducj i computer che tu âs voie e doprâlu par cualsisei finalitât che si desidere (includude chê comerciâl, governative, di aministrazion publiche e educative). Par vê plui detais viodêt il test de licence includude in cheste copie di LibreOffice.

Parcè isal LibreOffice libar par ducj?
----------------------------------------------------------------------

Si pues doprâ cheste copie di LibreOffice cence paiâ nuie par vie che colaboradôrs individuâi e aziendis patrocinantis a àn progjetât, svilupât, provât, tradot, documentât, supuartât, publicizât e judât in tantis altris manieris par rindi LibreOffice ce che al è vuê: il software di produtivitât a codiç viert (open source) prin tal mont, pe cjase e pal ufici.

Se o preseais i lôr sfuarçs e o desiderais che LibreOffice al continuedi a jessi disponibil intai agns che a vignaran, considerait di contribuî al progjet: consultait https://www.documentfoundation.org/contribution/ pai detais. Ducj a puedin contribuî in cualchi maniere.

----------------------------------------------------------------------
Notis pe instalazion
----------------------------------------------------------------------

Par podê funzionâ in maniere complete LibreOffice al à bisugne di une version resinte di Java Runtime Environment (JRE). JRE nol fâs part dal pachet di instalazion di LibreOffice e al scugne jessi instalât in maniere separade.

Recuisîts di sisteme
----------------------------------------------------------------------

* Microsoft Windows 7 SP1, 8, 8.1 Inzornament (S14) o 10

Viôt che a coventin i dirits di aministradôr pal procès di instalazion.

Si pues sfuarçâ o evitâ che LibreOffice si regjistri tant che aplicazion predefinide pai formâts di Microsoft Office doprant, cul instaladôr, lis opzions a rie di comant chi sot:

* REGISTER_ALL_MSO_TYPES=1 al sfuarçarà la regjistrazion di LibreOffice come aplicazion predefinide pai formâts di Microsoft Office.
* REGISTER_NO_MSO_TYPES=1 al disabilitarà la regjistrazion di LibreOffice come aplicazion predefinide pai formâts di Microsoft Office.

Sigurâitsi che al sedi vonde spazi libar te cartele temporanie dal vuestri sisteme e di vê i dirits di leture, scriture e esecuzion. Prime di inviâ il procès di instalazion sierait ducj chei altris programs.

Instalazion di LibreOffice sui sistemis Linux basâts su Debian/Ubuntu
----------------------------------------------------------------------

PAr savê ce mût instalâ un pachet di lenghe (dopo vê instalât la version inglese merecane di LibreOffice), lei la sezion chi sot intitulade “Instalâ un pachet di lenghe”.

Cuant che tu disimpachetis l'archivi discjariât, tu viodarâs che i contignûts a vegnin tirâts fûr intune sot-cartele. Vierç un barcon dal gjestôr di file e jentre te cartele che e scomence par “LibreOffice_”, seguide dal numar di version e cualchi informazion de plateforme.

Cheste cartele e conten une sot-cartele clamade “DEBS”. Jentre te cartele “DEBS”.

Fâs clic-diestri dentri de cartele e sielç “Vierç tal terminâl”. Un barcon dal terminâl si vierzarà. De rie di comant dal barcon, scrîf chest comant (par eseguî il comant, ti si domandarà di inserî la password di root):

I comants chi sot a instalaran LebreOffice e i pachets di integrazion cul scritori (si pues ancje dome copiâju e tacâju jenfri de videade dal terminâl, pitost che scriviju):

sudo dpkg -i *.deb

Il procès di instalazion al è cumò completât, e tu varessis di vê lis iconis par dutis lis aplicazions di LibreOffice tal menù Aplicazions/Ufici dal to scritori.

Instalazion di LibreOffice su sistemis Linux Fedora, openSUSE, Mandriva e altris, che a doprin i pachets RPM
----------------------------------------------------------------------

Par vê istruzions su ce mût instalâ un pachet di lenghe (dopo vê instalât la version inglese-merecane di LibreOffice), lei la sezion chi sot intitulade "Instalâ un pachet di lenghe".

Cuant che tu decomprimis l'archivi discjariât, tu viodarâs che il so contignût al è stât decomprimût intune sot-cartele. Vierç il to gjestôr di file e va te cartele che e tache par "LibreOffice_" cun daûr il numar de version e cualchi informazions in merit ae plateforme.

Cheste cartele e conten une sot-cartele clamade "RPMS". Va inte cartele "RPMS".

Fâs clic cul pulsant diestri dal mouse dentri te cartele e sielç "Vierç tal terminâl". Si vierzarà un barcon di terminâl. De rie di comant dal barcon, scrîf chest comant (par eseguî il comant, al vignarà domandât di scrivi la password di aministradôr):

For Fedora-based systems: sudo dnf install *.rpm

Pai sistemis basâts su Mandriva: sudo urpmi *.rpm

Pai altris sistemis basâts su RPM (openSUSE e vie indenant): rpm -Uvh *.rpm

Il procès di instalazion al è cumò completâte tu varessis di vê lis iconis par dutis lis aplicazions di LibreOffice tal menù Aplicazions/Ufici dal to scritori.

In alternative, par eseguî une instalazion a nivel di utent, tu puedis doprâ il script 'install', che si cjate te cartele superiôr di chest archivi. Il script al configurarà LibreOffice in mût di vê un so propri profîl par cheste instalazion, separât dal to normâl profîl di LibreOffice. Ten iniments che cheste operazion no instalarà lis parts pe integrazion cul scritori, come i elements dal menù e lis regjistrazions dai gjenars MIME.

Osservazions in merit ae integrazion cul scritori pes distribuzions Linux no tratadis tes istruzions di instalazion precedentis
----------------------------------------------------------------------

Nol varès di jessi dificil instalâ LibreOffice su altris distribuzions Linux no includudis in chestis istruzions di instalazion. Lis diferencis principâls che si podaressin intivâ a stan te integrazion cul scritori.

La cartele RPMS (o DEBS, secont il câs) e conten ancje un pachet clamât libreoffice7.4-freedesktop-menus-7.4.0.1-1.noarch.rpm (o libreoffice7.4-debian-menus_7.4.0.1-1_all.deb, secont il câs, o similâr). Chest al è un pachet par dutis lis distribuzions Linux che a supuartin lis specifichis/racomandazions di Freedesktop.org (https://en.wikipedia.org/wiki/Freedesktop.org), e al ven furnît pes instalazions su altris distribuzions di Linux no tratadis intes istruzions menzonadis in precedence.

Instalâ un pachet di lenghe
----------------------------------------------------------------------

Discjarie il pachet de lenghe che ti interesse secont de to plateforme. A son disponibii te stesse posizion dal archivi di instalazion principâl. Dal gjestôr di file Nautilus, tire fûr i file dal archivi discjariât intune cartele (par esempli il to scritori). Siguriti di sei jessût di dutis lis aplicazions di LibreOffice (includût il "QuickStart" l'inizi rapit, se inviât).

Va te cartele dulà che tu âs estrat il pachet di lenghe discjariât.

Cumò va te cartele creade intal procès di estrazion. Par esempli, pal pachet di lenghe furlane par un sisteme a 32-bit basât su Debian/Ubuntu, la cartele si clamarà LibreOffice_, plui cualchi informazion di version, plui Linux_x86_langpack-deb_fur.

Cumò va te cartele che e conten i pachets di instalâ. Tai sistemis basâts su Debian/Ubuntu, la cartele e sarà DEBS. Tai sistemis Fedora, openSUSE o Mandriva e sarà RPMS.

Dal gjestôr di file Nautilus, fâs clic diestri inte cartele e sielç il comant "Vierç tal terminâl". Tal barcon dal terminâl apene viert eseguìs il comant par instalâ il pachet di lenghe (e podarès vignî domandade la password dal aministradôr par ducj i comants chi sot):

Pai sistemis basâts su Debian/Ubuntu: sudo dpkg -i *.deb

For Fedora-based systems: su -c 'dnf install *.rpm'

Pai sistemis basâts su Mandriva: sudo urpmi *.rpm

Pai altris sistemis che a doprin RPM (openSUSE e vie indenant): rpm -Uvh *.rpm

Cumò invie une aplicazion di LibreOffice - Writer, par esempli. Va tal menù Struments e sielç Opzions. Tal barcon di dialic des opzions, fâs clic su "Impostazions de lenghe", daspò su "Lenghis". Te liste "Interface utent" selezione la lenghe apene instalade. Tu puedis fâ la stesse robe pe "Impostazion locâl", la "Valude predefinide" e lis "Lenghis predefinidis pai documents".

Dopo vê justât chês impostazions, fâs clic su Va ben. Il barcon si sierarà e al vignarà fûr un messaç di informazion che ti vise che lis modifichis a vignaran aplicadis dome daspò vê sierât e tornât a inviâ LibreOffice (visiti di sierâ ancje il QuickStart, l'inizi rapit, se inviât).

La prossime volte che tu inviarâs LibreOffice, al vignarà fûr te lenghe apene instalade.

----------------------------------------------------------------------
Problemis tal inviâ il program
----------------------------------------------------------------------

Difficulties starting LibreOffice (e.g. applications hang) as well as problems with the screen display are often caused by the graphics card driver. If these problems occur, please update your graphics card driver or try using the graphics driver delivered with your operating system.

----------------------------------------------------------------------
Touchpad di portatil ALPS/Synaptics in MS Windows
----------------------------------------------------------------------

Par vie di un probleme cul driver di Windows, nol è pussibil doprâ la funzion di scoriment dal touchpad ALPS/Synaptics tai documents di LibreOffice.

Par abilitâ il scoriment dal touchpad, zonte chestis riis al file di configurazion "C:\Program Files\Synaptics\SynTP\SynTPEnh.ini" e torne invie il computer:

[LibreOffice]

FC = "SALFRAME"

SF = 0x10000000

SF |= 0x00004000

La posizion dal file di configurazion e pues variâ su versions diferentis di Windows.

----------------------------------------------------------------------
Tascj pes scurtis
----------------------------------------------------------------------

In LibreOffice si puedin doprâ dome i tascj-scurte (cumbinazion di tascj) che no son za doprâts dal sisteme operatîf. Tal câs che une cumbinazion di tascj di LibreOffice no funzionedi come descrite intal jutori di LibreOffice, controle che chê scurte no sedi za doprade dal sisteme operatîf. Par risolvi chescj conflits, tu puedis cambiâ i tascj assegnâts dal to sisteme operatîf. In alternative, tu puedis cambiâ cuasi dutis lis assegnazions di tascj in LibreOffice. Par vê plui informazions in merit, fâs riferiment al jutori di LibreOffice o ae documentazion dal to sisteme operatîf.

----------------------------------------------------------------------
Problems When Sending Documents as Emails From LibreOffice
----------------------------------------------------------------------

When sending a document via 'File - Send - Document as Email' or 'Document as PDF Attachment' problems might occur (program crashes or hangs). This is due to the Windows system file "Mapi" (Messaging Application Programming Interface) which causes problems in some file versions. Unfortunately, the problem cannot be narrowed down to a certain version number. For more information visit https://www.microsoft.com to search the Microsoft Knowledge Base for "mapi dll".

----------------------------------------------------------------------
Avîs impuartants pe acessibilitât
----------------------------------------------------------------------

Par vê plui informazions su lis carateristichis di acès facilitât in LibreOffice, consulte https://www.libreoffice.org/accessibility/

----------------------------------------------------------------------
Supuart utents
----------------------------------------------------------------------

La pagjine di supuart principâl e ufrìs variis soluzions di assistence par LibreOffice. La tô domande e podarès bielza  vê vût rispueste: controle il forum de comunitât ae direzion http://www.documentfoundation.org/nabble/ o cîr tai archivis de mailing list 'users@fur.libreoffice.org' in http://www.libreoffice.org/lists/users/. In alternative, tu puedis inviâ lis tôs domandis a users@libreoffice.org. Se tu ti vûs iscrivi ae liste (par otignî rispuestis), invie un messaç vueit ae direzion: users+subscribe@fur.libreoffice.org.

Controle ancje la sezion FAQ sul sît web di LibreOffice.

----------------------------------------------------------------------
Segnalazion di erôrs e problemis
----------------------------------------------------------------------

Pal moment il nestri sisteme pe segnalazion, par tignî di voli e par risolvi i erôrs al è Bugzilla, ospitât su https://bugs.documentfoundation.org/. O invidìn ducj i utents a segnalâ i erôrs cjatâts te lôr specifiche plateforme. Un sisteme di segnalazions vivarose al è un dai contribûts plui impuartants che la comunitât di utents e pues dâ pal disvilup e il miorament futûr di LibreOffice.

----------------------------------------------------------------------
Ce mût colaborâ
----------------------------------------------------------------------

La comunitât di LibreOffice e zove une vore de vuestre partecipazion ative intal disvilup di chest impuartant progjet a codiç viert (open source).

Come utent, tu sês za une part impuartante dal procès di svilup de suite, e nus plasarès sburtâti a cjapâ in caric un rôl plui atîf, cul obietîf di deventâ un colaboradôr a lunc tiermin de comunitât. Tu nus puedis contatâ e unîti a nô ae pagjine dai contribûts sul sît web di LibreOffice.

Ce mût scomençâ
----------------------------------------------------------------------

La miôr maniere par tacâ a contribuî al progjet al è chel di iscrivisi a une o plui mailing list, lei par par un pôc di timp lis discussions e tacâ a lei i archivis par cjapâ convidence cui tancj argoments tratâts dal lontan Otubar 2000, date de prime publicazion dal codiç sorzint di LibreOffice. Al moment just, dut ce che ti varâs di fâ al sarà inviâ une e-mail par presentâti e butâti tal grum! Se tu âs za colaborât a altris progjets a codiç viert (open source), controle la liste des robis di fâ (To-Do) e scuvierç tal sît web di LibreOffice se al è alc che ti spire par judâ.

Iscriviti
----------------------------------------------------------------------

Chi si à cualchi mailing list che a chês tu ti puedis iscrivi inte pagjine https://www.libreoffice.org/get-help/mailing-lists/

* Gnovis: announce@documentfoundation.org *conseade par ducj i utents* (pôc trafic)
* Liste dai utents principâl: users@global.libreoffice.org *metodi sempliç par fâ la pueste su lis discussions* (trafic penç)
* Progjet di comercializazion: marketing@global.libreoffice.org *in diplui al disvilup* (trafic in aument)
* Liste gjenerâl pai disvilupadôrs: libreoffice@lists.freedesktop.org (trafic penç)

Unîsi a un o plui progjets
----------------------------------------------------------------------

Tu puedis dâ contribûts impuartants, a chest grant progjet a codiç viert, ancje se no si à grandis esperiencis di progjetazion o programazion di software. Nuie pôre!

O sperin che tu gjoldedis a lavorâ cul gnûf LibreOffice 7.4 e che tu partecipedis ae nestre comunitât online.

La comunitât di LibreOffice

----------------------------------------------------------------------
Codiç sorzint doprât / modificât
----------------------------------------------------------------------

Parts cun dirits di autôr 1998, 1999 James Clark. Parts cun dirits di autôr 1996, 1998 Netscape Communications Corporation.
