
======================================================================
LibreOffice 7.4 Lleime
======================================================================


For the latest updates to this readme file, see https://git.libreoffice.org/core/tree/master/README.md

Esti ficheru contien información importante tocante al software LibreOffice. S'encamienta lleer con atención esta información enantes d'aniciar la instalación.

La comunidá de LibreOffice ye responsable del desendolcu d'esti productu, y convídate a que consideres participar como miembru de la comunidá. Si yes un usuariu nuevu pues visitar el sitiu de LibreOffice, nel que podrás atopar una bayura d'información sobro'l proyeutu LibreOffice y les comunidaes qu'esisten alredor. Visita  http://www.libreoffice.org/.

¿LibreOffice ye llibre daveres pa cualquier usuariu?
----------------------------------------------------------------------

Toos puen usar LibreOffice con llibertá. Pues coyer esta copia de LibreOffice ya instalalu en tantos ordenadores como quieras, y usalu con cualesquier propósitu que quieras (incluyíu l'usu comercial, gubernativu, n'alministración pública o educativu). Pa más detalles mira nel testu de la llicencia incluyíu nesta descarga de LibreOffice.

¿Por qué LibreOffice ye llibre pa cualquier usuariu?
----------------------------------------------------------------------

Pues usar de baldre esta copia de LibreOffice porque les persones que collaboren y les empreses patrocinadores diseñaron, desendolcaron, probaron, tornaron, documentaron, dieron asistencia, ficieron publicidá y ayudaron de munches maneres pa que LibreOffice pudiera ser lo que ye anguaño - el líder mundial en software de productividá de códigu abierto pa casa y pa la oficina.

Si aprecies la so xera y te prestaría asegurar que LibreOffice siga disponible a llargu plazu, considerae facer una contribución al proyeutu - para más detalles visita https://www.documentfoundation.org/contribution/. Tol mundu pué collaborar de dalguna manera.

----------------------------------------------------------------------
Notes sobre la instalación
----------------------------------------------------------------------

LibreOffice requier una versión nueva de Java Runtime Environment (JRE) pa funcionar de mou completu. JRE nun ye parte del paquete d'instalación de LibreOffice, tien d'instalase aparte.

Requisitos del sistema
----------------------------------------------------------------------

* Microsoft Windows 7 SP1, 8, 8.1 Update (S14) o 10

Atalanta que pa executar el procesu d'instalación necesites permisos d'alministrador.

Se pue forzar o torgar el rexistru de LibreOffice como aplicación predeterminada pa los formatos de Microsoft Office usando los siguientes parámetros na llinia de comandos del instalador:

* REGISTER_ALL_MSO_TYPES=1 forzará'l rexistru de LibreOffice como aplicación predeterminada pa los formatos de Microsoft Office.
* REGISTER_NO_MSO_TYPES=1 torgará'l rexistru de LibreOffice como aplicación predeterminada pa los formatos de Microsoft Office.

Asegurate de tener espaciu bastante nel direutoriu temporal del sistema, y tamién de tener los permisos d'accesu necesarios pa llectura, escritura y execución n'él. Zarra tolos demás programes antes de principiar col procesu d'instalación.

Instalación de LibreOffice en sistemes Linux basaos en Debian/Ubuntu
----------------------------------------------------------------------

Pa más instrucciones sobre como instalar un paquete d'idioma (dempués de tener instalada la versión n'inglés de los EE.XX. de LibreOffice), llea más abaxo la seición titulada Instalación d'un paquete d'idioma.

Cuando desempaquete l'archivu descargáu, verá que'l conteníu se descomprimió nun subdireutoriu. Abra una ventana del alministrador de ficheros y cambia de direutoriu al que comienza con «LibreOffice_», siguío pol númberu de versión y dalguna información de la plataforma.

Esti direutoriu contien un subdireutoriu nomáu «DEBS». Cambia de direutoriu a «DEBS».

Calque col botón drechu dientro del direutoriu y escueya «Abrir nun terminal». S'abrirá una ventana de terminal. Na llinia de comandu, escriba'l comandu siguiente (va pidise escribir la contraseña del usuariu root enantes d'executar el comandu):

Los comandos siguientes instalarán LibreOffice y los paquetes pa la integración nel escritoriu (pue simplemente copialos y pegalos na pantalla del terminal meyor qu'intentar escribilos):

sudo dpkg -i *.deb

Agora ta completu'l procesu d'instalación, y habríes de tener los iconos de toles aplicaciones de LibreOffice nel menú d'escritoriu Aplicaciones/Oficina.

Instalación de LibreOffice en Fedora, openSuse, Mandriva y otros sistemes Linux qu'usen paquetes RPM
----------------------------------------------------------------------

Pa más instrucciones sobre como instalar un paquete d'idioma (dempués de tener instalada la versión n'inglés de los EE.XX. de LibreOffice), llea más abaxo la seición titulada Instalación d'un paquete d'idioma.

Cuando desempaquete l'archivu descargáu, verá que'l conteníu se descomprimió nun subdireutoriu. Abra una ventana del alministrador de ficheros y cambie de direutoriu al que comienza con «LibreOffice_», siguío pol númberu de versión y dalguna información de la plataforma.

Esti direutoriu contien un subdireutoriu nomáu «RPMS». Cambiar de direutoriu a «RPMS».

Calque col botón drechu dientro del direutoriu y escueya «Abrir nun terminal». S'abrirá una ventana de terminal. Na llinia de comandu, escriba'l comandu siguiente (va pidise escribir la contraseña del usuariu root enantes d'executar el comandu):

For Fedora-based systems: sudo dnf install *.rpm

Pa los sistemes basaos en Mandriva: sudo urpmi *.rpm

Pa otros sistemes basaos en RPM (openSuse, etc.): rpm -Uvh *.rpm

Agora ta completu'l procesu d'instalación, y habríes de tener los iconos de toles aplicaciones de LibreOffice nel menú d'escritoriu Aplicaciones/Oficina.

Alternativamente, pue utilizar el script «install», que s'alcuentra nel direutoriu de nivel superior d'esti archivu pa facer una instalación d'usuariu. El script configurará LibreOffice pa que tenga un perfil propiu nesta instalación, separáu del so perfil normal de LibreOffice. Tenga en cuenta qu'esto nun instalará les partes d'integración col sistema, tales como los menús del escritoriu y los rexistros de tipos MIME del escritoriu.

Notes tocante a la integración nel Escritoriu de distribuciones de Linux nun mencionaes nes anteriores instrucciones d'instalación
----------------------------------------------------------------------

Tendría de poder instalase de mou fácil LibreOffice n'otres distribuciones de Linux que nun se traten de manera específica nestes instrucciones d'instalación. El principal aspeutu nel que pueden apaecer diferencies ye no que cinca a la integración col escritoriu.

El direutoriu de RPM (ou DEB, según correspuenda) tamién contién un paquete llamáu libreoffice7.4-freedesktop-menus-7.4.0.1-1.noarch.rpm (o libreoffice7.4-debian-menus_7.4.0.1-1_all.deb, respeutivamente, o asemeyao). Esti ye un paquete pa toles distribuciones de Linux qu'almiten les especificaciones/recomendaciones de Freedesktop.org (https://en.wikipedia.org/wiki/Freedesktop.org), y úfrese pa permitir la instalación n'otres distribuciones de Linux que nun tán cubiertes poles anteriores instrucciones .

Instalar un paquete d'idioma
----------------------------------------------------------------------

Descarga'l paquete d'idioma pal idioma y plataforma que quieras. Tan disponibles nel mesmu llugar que'l archivu principal d'instalación. Dende'l alministrador de ficheros Nautilus, estrái l'archivu descargáu en dalgún direutoriu (por casu, nel escritoriu). Tienes d'asegurate de que colasti de toles aplicaciones de LibreOffice (incluyíu QuickStarter, si tuviera executándose).

Cambia al direutoriu nel qu'estraxisti el paquete d'idioma descargáu.

Agora cambie al direutoriu que se creó nel procesu d'estraición. Por exemplu, pal paquete n'idioma asturianu d'un sistema de 32 bits basáu en Debian/Ubuntu, el direutoriu llámase LibreOffice_, más información de la versión, más Linux_x86_langpack-deb_ast.

Agora, cambie al direutoriu que contién los paquetes pa instalar. Nos sistemes basaos en Debian o Ubuntu, el direutoriu ye DEBS. Nos sistemes Fedora, openSuse o Mandriva, el direutoriu llámase RPMS.

Dende'l xestor de ficheros Nautilus, calque col botón drechu nel direutoriu y escueya'l comandu «Abrir nun terminal». Na ventana del terminal que vien d'abrir, execute'l comandu pa instalar el paquete d'idioma (con tolos comandos darréu, va pidir qu'escriba la contraseña del usuariu root):

Pa los sistemes basaos en Debian o Ubuntu: sudo dpkg -i *.deb

For Fedora-based systems: su -c 'dnf install *.rpm'

Pa los sistemes basaos en Mandriva: sudo urpmi *.rpm

Pa otros sistemes qu'usen RPM (openSuse, etc.): rpm -Uvh *.rpm

Execute agora una de les aplicaciones de LibreOffice - Writer, por casu. Entre nel menú Ferramientes y escueya Opciones. Nel cuadru de diálogu Opciones, calque en «Configuración de llingua» y, darréu, en «Llingües». Estenderexe la llista «Interfaz d'usuariu» y seleicione l'idioma que vien d'instalar. Si quier, faiga lo mesmo cola «Configuración llocal», la «Moneda predeterminada» y la «Llingua predeterminada pa los documentos».

Dempués d'axustar eses preferencies, calque Aceutar. Se zarrará'l cuadru de diálogu, y verá un mensaxe informativu diciendo que los cambeos namái s'activarán dempués de zarrar LibreOffice y volver a executalu (recuerde zarrar tamién QuickStarter si tuviera executandose).

La siguiente vez qu'executes LibreOffice, s'aniciará col idioma que vienes d'instalar.

----------------------------------------------------------------------
Problemes al aniciar el programa
----------------------------------------------------------------------

Difficulties starting LibreOffice (e.g. applications hang) as well as problems with the screen display are often caused by the graphics card driver. If these problems occur, please update your graphics card driver or try using the graphics driver delivered with your operating system.

----------------------------------------------------------------------
Paneles táctiles de portátiles ALPS/Synaptics en Windows
----------------------------------------------------------------------

Por un problema col controlador de Windows, nun pue movese pelos documentos de LibreOffice cuando eslice'l deu per un panel táctil ALPS/Synaptics.

Pa poder desplazase usando'l touchpad, amiesta les siguientes llinies al ficheru de configuración "C:\Program Files\Synaptics\SynTP\SynTPEnh.ini" y reanicia l'equipu:

[LibreOffice]

FC = "SALFRAME"

SF = 0x10000000

SF |= 0x00004000

La llocalización del ficheru de configuración puede camudar dependiendo de les estremaes versiones de Windows.

----------------------------------------------------------------------
Combinación de tecles
----------------------------------------------------------------------

En LibreOffice sólo pueden usase les tecles d'atayu (combinaciones de tecles) que nun use'l sistema operativu. Si una combinación de tecles de LibreOffice nun funciona como se describe na ayuda de LibreOffice, comprueba si esi atayu yá lu usa'l sistema operativu. Pa iguar estos problemes, pues camudar les tecles asignaes pol sistema operativu. Tamién, pues camudar casi cualesquier asignación de tecles en LibreOffice. Si quies más información, consulta la ayuda de LibreOffice o la documentación d'ayuda del sistema operativu.

----------------------------------------------------------------------
Problems When Sending Documents as Emails From LibreOffice
----------------------------------------------------------------------

When sending a document via 'File - Send - Document as Email' or 'Document as PDF Attachment' problems might occur (program crashes or hangs). This is due to the Windows system file "Mapi" (Messaging Application Programming Interface) which causes problems in some file versions. Unfortunately, the problem cannot be narrowed down to a certain version number. For more information visit https://www.microsoft.com to search the Microsoft Knowledge Base for "mapi dll".

----------------------------------------------------------------------
Notes d'Acesibilidá Importantes
----------------------------------------------------------------------

Pa más información sobro les carauterístiques d'accesibilidá de LibreOffice visita https://www.libreoffice.org/accessibility/

----------------------------------------------------------------------
Asistencia al usuariu
----------------------------------------------------------------------

La páxina principal d'asistencia ufre delles posibilidaes d' ayuda pa LibreOffice. Seique la to entruga yá se contestó - consulta'l foru de la comunidá en https://www.documentfoundation.org/nabble/ o busca nos archivos de la llista de corréu «users@libreoffice.org» en https://www.libreoffice.org/lists/users/ . Tamién pues unviar les tos entrugues a users@libreoffice.org. Si quies suscribite a la llista (pa recibir respuestes per corréu) manda un corréu electrónicu en blancu a: users+subscribe@libreoffice.org.

Consulta tamién la sección d'Entrugues Más Frecuentes del sitiu web de LibreOffice.

----------------------------------------------------------------------
Reportar errores & problemes
----------------------------------------------------------------------

Our system for reporting, tracking and solving bugs is currently Bugzilla, hosted at https://bugs.documentfoundation.org/. We encourage all users to feel entitled and welcome to report bugs that may arise on your particular platform. Energetic reporting of bugs is one of the most important contributions that the user community can make to the ongoing development and improvement of LibreOffice.

----------------------------------------------------------------------
Implicase
----------------------------------------------------------------------

La Comunidá de LibreOffice podría beneficiase asgaya de la to participación activa nel desendolcu d'esti importante proyeutu de software abiertu.

As a user, you are already a valuable part of the suite's development process and we would like to encourage you to take an even more active role with a view to being a long-term contributor to the community. Please join and check out the contributing page at the LibreOffice website.

Cómo entamar
----------------------------------------------------------------------

The best way to start contributing is to subscribe to one or more of the mailing lists, lurk for a while, and gradually use the mail archives to familiarize yourself with many of the topics covered since the LibreOffice source code was released back in October 2000. When you're comfortable, all you need to do is send an email self-introduction and jump right in. If you are familiar with Open Source Projects, check out our To-Dos list and see if there is anything you would like to help with at the LibreOffice website.

Soscribi
----------------------------------------------------------------------

Here are a few of the mailing lists to which you can subscribe at https://www.libreoffice.org/get-help/mailing-lists/

* Noticies: announce@documentfoundation.org *s'encamienta pa tolos usuarios* (tráficu llixeru)
* Llista d'usuarios principal: users@global.libreoffice.org *mou fácil d'escucar los alderiques* (tráficu altu)
* Proyeutu de mercadoteunia: marketing@global.libreoffice.org *más alló del desendolcu* (tráficu mediu)
* Llista xeneral pal desendolcu: libreoffice@lists.freedesktop.org (tráficu intensu)

Xunise a un proyeutu o más
----------------------------------------------------------------------

Puedes faceer contribuciones pergrandes a esti proyeutu de códigu abiertu anque tengas poca esperiencia colos códigos o'l diseñu de software. ¡Sí, Tu!

Esperamos que te preste trabayar col nuevu LibreOffice 7.4 y que te xuntes con nós en llinia.

La comunidá de LibreOffice

----------------------------------------------------------------------
Códigu fonte usáu / camudáu
----------------------------------------------------------------------

Partes con Copyright 1998, 1999 de James Clark. Partes con Copyright 1996, 1998 Netscape Communications Corporation.
