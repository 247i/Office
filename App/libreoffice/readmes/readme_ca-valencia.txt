
======================================================================
Llegiu-me del LibreOffice 7.4
======================================================================


Visiteu https://git.libreoffice.org/core/tree/master/README.md per a obtindre la versió més recent d'aquest fitxer.

Aquest fitxer conté informació important sobre el LibreOffice. Es recomana que llegiu aquesta informació atentament abans de començar la instal·lació.

La comunitat del LibreOffice és responsable del desenvolupament d'aquest producte, i vos convida a considerar participar com a membre de la comunitat. Si sou un usuari nou, podeu visitar el lloc web del LibreOffice, on hi trobareu molta informació sobre el projecte LibreOffice i les comunitats que existeixen al seu voltant. Aneu a https://www.libreoffice.org/.

El LibreOffice realment és gratuït per a tots els usuaris?
----------------------------------------------------------------------

Tothom pot utilitzar el LibreOffice gratuïtament. Podeu instal·lar aquesta còpia del LibreOffice en tants ordinadors com vulgueu i utilitzar-lo per a qualsevol propòsit (inclosos propòsits comercials, governamentals, d'administració pública i d'usos educatius). Podeu obtindre més detalls al text de llicència que s'inclou dins del paquet del LibreOffice.

Per què el LibreOffice és gratuït per a qualsevol usuari?
----------------------------------------------------------------------

Podeu utilitzar aquesta còpia del LibreOffice gratuïtament perquè col·laboradors individuals i patrocinadors corporatius han dissenyat, desenvolupat, provat, traduït, documentat, mantingut, promocionat i ajudat de moltes altres maneres per fer del LibreOffice allò que és hui: el líder mundial en programari lliure ofimàtic per a usuaris domèstics i d'oficina.

Si aprecieu l'esforç i voleu que el LibreOffice seguïsca estant disponible en el futur, considereu la possibilitat de contribuir al projecte. Visiteu https://www.documentfoundation.org/contribution/ per a obtindre més detalls. Tothom pot contribuir-hi d'alguna manera.

----------------------------------------------------------------------
Notes d'instal·lació
----------------------------------------------------------------------

El LibreOffice necessita una versió actualitzada de l'entorn d'execució de Java (JRE) per a poder proporcionar tota la seua funcionalitat. El JRE no forma part del paquet d'instal·lació del LibreOffice i s'ha d'instal·lar per separat.

Requeriments del sistema
----------------------------------------------------------------------

* Microsoft Windows 7 SP1, 8, 8.1 Update (S14) o 10

Tingueu en compte que cal tindre drets d'administrador per al procés d'instal·lació.

El registre del LibreOffice com a aplicació per defecte per als formats del Microsoft Office es pot forçar o suprimir mitjançant les següents opcions de línia d'ordres de l'instal·lador:

* REGISTER_ALL_MSO_TYPES=1 forçarà el registre del LibreOffice com a aplicació per defecte per als formats del Microsoft Office.
* REGISTER_NO_MSO_TYPES=1 suprimirà el registre del LibreOffice com a aplicació per defecte per als formats del Microsoft Office.

Assegureu-vos que teniu prou espai disponible al directori temporal del sistema i comproveu que teniu accés de lectura, escriptura i execució. Tanqueu tots els altres programes abans d'iniciar el procés d'instal·lació.

Instal·lació del LibreOffice en sistemes Linux basats en Debian/Ubuntu
----------------------------------------------------------------------

Per a les instruccions de com instal·lar un paquet de llengua (després d'haver instal·lat la versió en anglés EUA del LibreOffice), llegiu la secció següent titulada «Instal·lació d'un paquet de llengua».

En descomprimir el fitxer baixat, veureu que els continguts es descomprimeixen en un subdirectori. Obriu una finestra del gestor de fitxers i canvieu el directori actual al que comença per «LibreOffice_», tot seguit pel número de versió i informació sobre la plataforma.

Aquest directori conté un subdirectori anomenat "DEBS". Canvieu el directori actual pel directori "DEBS".

Feu clic amb el botó secundari sobre el directori i seleccioneu «Obri en el Terminal». S'obrirà una finestra de terminal. Des de la línia d'ordes de la finestra de terminal, introduïu la següent orde (se vos preguntarà la contrasenya d'administrador abans d'executar-se):

Les ordres següents instal·laran el LibreOffice i els paquets d'integració amb l'escriptori (podeu copiar-les i apegar-les en una finestra del terminal en comptes de teclejar-les):

sudo dpkg -i *.deb

El procés d'instal·lació s'ha completat i heu de tindre les icones de totes les aplicacions del LibreOffice en el vostre menú d'escriptori d'Aplicacions/Ofimàtica.

Instal·lació del LibreOffice a Fedora, openSUSE, Mandriva i altres distribucions que utilitzen paquets RPM
----------------------------------------------------------------------

Per a les instruccions de com instal·lar un paquet de llengua (després d'haver instal·lat la versió en anglés EUA del LibreOffice), llegiu la secció següent titulada «Instal·lació d'un paquet de llengua».

En descomprimir el fitxer baixat, veureu que els continguts es descomprimeixen en un subdirectori. Obriu una finestra del gestor de fitxers i canvieu el directori actual al que comença per «LibreOffice_», tot seguit pel número de versió i informació sobre la plataforma.

Aquest directori conté un subdirectori anomenat "RPMS". Canvieu el directori actual pel directori "RPMS".

Feu clic amb el botó secundari sobre el directori i seleccioneu «Obri en el Terminal». S'obrirà una finestra de terminal. Des de la línia d'ordes de la finestra de terminal, introduïu la següent orde (se vos preguntarà la contrasenya d'administrador abans d'executar-se):

Per a sistemes basats en Fedora: sudo dnf install *.rpm

Per a sistemes basats en Mandriva: sudo urpmi *.rpm

Per a altres sistemes que utilitzen RPM (openSUSE, etc.): rpm -Uvh *.rpm

El procés d'instal·lació s'ha completat i heu de tindre les icones de totes les aplicacions del LibreOffice en el vostre menú d'escriptori d'Aplicacions/Ofimàtica.

Alternativament, podeu usar l'script «install» ubicat al nivell superior del directori d'aquest arxiu per a fer una instal·lació com a usuari. L'script configurarà el LibreOffice per a tindre el seu propi perfil, separat del perfil normal del LibreOffice. Noteu que això no instal·larà la integració amb el sistema operatiu, com ara els elements del menú d'escriptori o els registres del tipus MIME.

Notes referents a la integració amb l'escriptori de les distribucions no mencionades en les instruccions anteriors
----------------------------------------------------------------------

Hauria de ser possible instal·lar fàcilment el LibreOffice en altres distribucions que no estan cobertes en aquestes instruccions. Les diferències principals seran en la integració amb l'escriptori.

El directori RPMS (o DEBS, respectivament) també conté un paquet anomenat libreoffice7.4-freedesktop-menus-7.4.0.1-1.noarch.rpm (o libreoffice7.4-debian-menus_7.4.0.1-1_all.deb, respectivament, o similar). Aquest paquet és per a totes les distribucions de Linux que implementen les especificacions o recomanacions de Freedesktop (https://ca.wikipedia.org/wiki/Freedesktop.org), i es proporciona per a permetre la instal·lació en distribucions Linux que no estan mencionades en les instruccions.

Instal·lació d'un paquet de llengua
----------------------------------------------------------------------

Baixeu el paquet corresponent a la vostra llengua i plataforma. Aquests es troben disponibles en el mateix lloc que el fitxer d'instal·lació principal. Des del gestor de fitxers Nautilus, descomprimiu el fitxer baixat a un directori (el vostre escriptori, per exemple). Assegureu-vos també que heu eixit de totes les aplicacions del LibreOffice (inclòs l'inici ràpid, si està executant-se).

Canvieu de directori cap al directori on heu baixat el paquet de llengua.

Ara canvieu el directori actual pel directori que s'ha creat durant el procés d'extracció. Per exemple, per al codi de llengua catalana per als sistema Debian/Ubuntu de 32 bits, el directori s'anomena LibreOffice_, més informació sobre la versió, més Linux_x86_langpack-deb_ca.

Ara canvieu el directori actual pel directori que conté els paquets per instal·lar. En un sistema basat en Debian/Ubuntu el directori serà DEBS. En Fedora, openSUSE o Mandriva, el directori serà RPMS.

Des del gestor de fitxers Nautilus, feu clic amb el botó secundari sobre el directori i seleccioneu «Obri en el Terminal». S'obrirà una finestra de terminal. Des de la línia d'ordes de la finestra de terminal, introduïu la següent orde (se vos preguntarà la contrasenya d'administrador abans d'executar-se):

Per a sistemes basats en Debian/Ubuntu: sudo dpkg -i *.deb

Per a sistemes basats en Fedora: su -c 'dnf install *.rpm'

Per a sistemes basats en Mandriva: sudo urpmi *.rpm

Per a altres sistemes que utilitzen RPM (openSUSE, etc.): rpm -Uvh *.rpm

Ara inicieu una de les aplicacions del LibreOffice, per exemple el Writer. Aneu al menú d'Eines i seleccioneu Opcions. Al quadre de diàleg Opcions, feu clic a «Configuració de la llengua» i a «Llengües». A la llista desplegable «Interfície d'usuari», seleccioneu la llengua que heu instal·lat. Si voleu també podeu fer el mateix amb «Configuració local», «Moneda per defecte» i «Llengües per defecte per als documents».

Després d'ajustar aquests paràmetres, feu clic a «D'acord». El quadre de diàleg es tancarà i podreu veure un missatge d'informació que us informa que els canvis només s'activaran després d'eixir del LibreOffice i executar-lo una altra vegada (recordeu-vos també d'eixir de l'inici ràpid, si està activat).

La pròxima vegada que reinicieu el LibreOffice, s'iniciarà amb la llengua que heu instal·lat.

----------------------------------------------------------------------
Problemes en iniciar el programa
----------------------------------------------------------------------

Difficulties starting LibreOffice (e.g. applications hang) as well as problems with the screen display are often caused by the graphics card driver. If these problems occur, please update your graphics card driver or try using the graphics driver delivered with your operating system.

----------------------------------------------------------------------
Ratolins tàctils ALPS/Synaptics de portàtils al Windows
----------------------------------------------------------------------

A causa d'un problema amb el controlador del Windows, no us podeu desplaçar a través de documents del LibreOffice en arrossegar el dit per un ratolí tàctil ALPS/Synaptics.

Per a habilitar el desplaçament amb el ratolí tàctil, afegiu les línies següents al fitxer de configuració "C:\Program Files\Synaptics\SynTP\SynTPEnh.ini"  i reinicieu l'ordinador:

[LibreOffice]

FC = "SALFRAME"

SF = 0x10000000

SF |= 0x00004000

La ubicació del fitxer de configuració pot variar en diferents versions del Windows.

----------------------------------------------------------------------
Tecles de drecera
----------------------------------------------------------------------

Només les tecles de drecera (combinacions de tecles) que no s'utilitzen en el sistema operatiu es poden utilitzar al LibreOffice. Si una combinació de tecles al LibreOffice no funciona tal com diu l'ajuda del LibreOffice, comproveu que no la utilitze ja el sistema operatiu. Per a resoldre aquests conflictes, podeu canviar les assignacions de tecles del sistema operatiu. Alternativament, podeu canviar gairebé qualsevol assignació de tecles a LibreOffice. Per a més informació, vegeu l'ajuda del LibreOffice o del sistema operatiu.

----------------------------------------------------------------------
Problemes en enviar documents com a correus electrònics des del LibreOffice
----------------------------------------------------------------------

Quan s'envia un document via «Fitxer ▸ Envia ▸ Document com a correu electrònic» o «Document com a adjunt PDF» es poden produir problemes (el programa falla o es penja).  Això es deu al fitxer del sistema de Windows «Mapi» (Messaging Application Programming Interface) que causa problemes en algunes versions de fitxers.  Lamentablement, el problema no es pot reduir a un determinat número de versió.  Per a més informació visiteu https://www.microsoft.com per a cercar la base de coneixement de Microsoft per «mapi dll».

----------------------------------------------------------------------
Notes importants quant a l'accessibilitat
----------------------------------------------------------------------

Per a més informació sobre les característiques d'accessibilitat del LibreOffice, visiteu https://www.libreoffice.org/accessibility/

----------------------------------------------------------------------
Assistència a l'usuari
----------------------------------------------------------------------

La pàgina principal d'assistència ofereix diferents maneres d'obtindre ajuda per al LibreOffice. La vostra pregunta ja s'ha contestat. Comproveu-ho en el fòrum comunitari a https://www.documentfoundation.org/nabble/ o cerqueu en els arxius de la llista de correu 'users@libreoffice.org' a https://www.libreoffice.org/lists/users/. Com a alternativa podeu enviar les vostres preguntes a users@libreoffice.org. Si vos voleu subscriure a aquesta llista (per a obtindre les respostes via correu electrònic) envieu un missatge en blanc a: users+subscribe@libreoffice.org.

Consulteu també la secció de preguntes més freqüents en el lloc web del LibreOffice.

----------------------------------------------------------------------
Notificació d'errors i problemes
----------------------------------------------------------------------

El nostre sistema actual per a reportar, seguir i resoldre errors és el Bugzilla, que es troba a https://bugs.documentfoundation.org/. Volem que tots els usuaris reportin errors que troben a la seua plataforma particular. Reportar errors és una de les contribucions més importants que la comunitat pot fer per a millorar el desenvolupament del LibreOffice.

----------------------------------------------------------------------
Com col·laborar
----------------------------------------------------------------------

La comunitat del LibreOffice es pot beneficiar en gran mesura de la vostra participació activa en el desenvolupament d'aquest important projecte de codi font obert.

Com a usuari ja sou ara mateix una part important del procés de desenvolupament i ens agradaria encoratjar-vos a tindre un paper encara més actiu tot sent un col·laborador a llarg termini de la comunitat. Uniu-vos a nosaltres i visiteu la pàgina al lloc web del LibreOffice.

Com començar
----------------------------------------------------------------------

La millor manera de començar a col·laborar-hi és subscriure-vos a una o més llistes de correu, llegir els missatges durant un temps i utilitzar gradualment els arxius de correu per a familiaritzar-vos amb els diversos temes que s'hi tracten des que es va alliberar el codi del LibreOffice l'octubre de 2000. Quan vos trobeu còmode, tot el que heu de fer és enviar un missatge de presentació i començar a treballar. Si teniu experiència amb altres projectes de programari lliure, consulteu la llista de coses per fer i mireu si hi ha res on voldríeu ajudar en el lloc web del LibreOffice.

Subscriviu-vos
----------------------------------------------------------------------

Ací teniu algunes de les llistes de correu a les quals vos podeu subscriure des de https://www.libreoffice.org/get-help/mailing-lists/

* Notícies: announce@documentfoundation.org *recomanada per a tots els usuaris* (poc trànsit)
* Llista d'usuaris principal: users@global.libreoffice.org *la manera fàcil d'assabentar-se dels temes que es debaten* (molt de trànsit)
* Projecte de màrqueting: marketing@global.libreoffice.org *més enllà del desenvolupament* (trànsit en augment)
* Llista general de desenvolupament: libreoffice@lists.freedesktop.org (molt de trànsit)

Apuntar-se a un o més projectes
----------------------------------------------------------------------

Podeu fer contribucions importants a aquest gran projecte de codi font obert fins i tot si la vostra experiència en programació i disseny de programari és limitada. No ho dubteu!

Esperem que gaudiu treballant amb el nou LibreOffice 7.4 i que us uniu a nosaltres en línia.

La comunitat LibreOffice

----------------------------------------------------------------------
Codi font utilitzat / modificat
----------------------------------------------------------------------

Parts amb copyright 1998, 1999 James Clark. Parts amb copyright 1996, 1998 Netscape Communications Corporation.
