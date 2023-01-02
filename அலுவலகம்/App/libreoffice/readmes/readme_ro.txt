
======================================================================
LibreOffice 7.4 Citește-mă
======================================================================


For the latest updates to this readme file, see https://git.libreoffice.org/core/tree/master/README.md

Acest fișier conține informații importante despre aplicația LibreOffice. Se recomandă să citiți cu atenție aceste informații înainte de a începe instalarea.

Comunitatea LibreOffice este responsabilă pentru dezvoltarea acestui produs și vă invită să luați în considerare participarea în calitate de membru al comunității. Dacă sunteți un utilizator nou, puteți vizita site-ul web LibreOffice, unde veți găsi o mulțime de informații despre proiectul LibreOffice și comunitățile care există în jurul acestuia. Accesați https://www.libreoffice.org/.

Aplicația LibreOffice este într-adevăr gratuită pentru orice utilizator?
----------------------------------------------------------------------

Utilizarea LibreOffice este gratuită pentru toată lumea. Puteți lua și instala această copie a LibreOffice pe oricâte computere doriți și o puteți utiliza în orice scop doriti (inclusiv comercial, guvern, administrație publică și învățământ). Pentru mai multe detalii, după descărcare vedeți fișierul text care conține licența aplicației LibreOffice.

De ce aplicația LibreOffice este gratuită pentru orice utilizator?
----------------------------------------------------------------------

Puteți folosi gratuit această copie a LibreOffice, deoarece contribuitorii individuali și sponsorii corporativi au proiectat, dezvoltat, testat, tradus, sprijinit, comercializat și au ajutat în multe alte feluri pentru ca aplicația LibreOffice să fie ceea ce este astăzi - lider mondial în software-ul Open Source pentru casă și birou.

If you appreciate their efforts, and would like to ensure that LibreOffice continues to be available far into the future, please consider contributing to the project - see https://www.documentfoundation.org/contribution/ for details. Everyone can make a contribution of some kind.

----------------------------------------------------------------------
Note despre instalare
----------------------------------------------------------------------

LibreOffice necesită o versiune recentă a Mediului de Rulare Java (JRE) pentru a funcționa la capacitate maximă.JRE nu face parte din pachetul de instalare al LibreOffice, el ar trebui instalat separat.

Descărcare
----------------------------------------------------------------------

* Microsoft Windows 7 SP1, 8, 8.1 Update (S14) or 10

Pentru instalare aveți nevoie de drepturi de administrator.

Înregistrarea LibreOffice drept aplicație implicită pentru formatele Microsoft Office poate fi forțată sau suprimată folosind următoarele opțiuni în linia de comandă la lansarea asistentului de instalare:

* REGISTER_ALL_MSO_TYPES=1 va seta pentru formatele Microsoft Office ca program implicit, programul LibreOffice.
* REGISTER_NO_MSO_TYPES=1 nu va seta pentru formatele Microsoft Office ca program implicit, programul LibreOffice.

Asigurați-vă că aveți suficient spațiu liber în directorul temporar al sistemului dvs., și că ați citit drepturile de acces. Închideți toate celelalte programe înainte de a începe procesul de instalare.

Instalarea LibreOffice pe sistemele de operarea bazate pe Linux: Debian/Ubuntu
----------------------------------------------------------------------

Pentru instrucțiuni privind instalarea pachetelor de limbă (după ce aveți deja instalată LibreOffice în limba US English), citiți secțiunea de mai jos cu titlul Instalarea pachetelor de limbă.

La despachetarea arhivei descărcate, veți observa conținutul decomprimat într-un subdirector. Deschideți o fereastră a gestionarului de fișiere și schimbați directorul cu cel care începe cu „LibreOffice_”, urmat de numărul versiunii și câteva informații despre platformă.

Acest director conține un subdirector numit "Debs". Comută la directorul "Debs".

Faceți clic dreapta in director și alegeți opțiunea "Open in Terminal". Se va deschide o fereastră terminal. Din linia de comandă a ferestrei terminal, introduceți următoarea comandă (vi se va cere să introduceți parola dvs. de utilizator root înainte de a se executa comanda):

Comenzile următoare instalează LibreOffice și pachetele de integrare în mediul desktop (copiați și inserați această comandă într-un terminal, în loc să introduceți comanda manual):

sudo dpkg -i *.deb

Procesul de instalare este acum încheiat și ar trebui să aveți iconițe pentru a vizualiza toate aplicațiile LibreOffice în meniul Aplicațiile desktop-ului / Office.

Instalarea LibreOffice pe Fedora, openSUSE, Mandriva și alte sisteme Linux folosind pachete RPM
----------------------------------------------------------------------

Pentru instrucțiuni privind instalarea pachetelor de limbă (după ce aveți deja instalată LibreOffice în limba US English), citiți secțiunea de mai jos cu titlul Instalarea pachetelor de limbă.

La despachetarea arhivei descărcate, veți observa conținutul decomprimat într-un subdirector. Deschideți o fereastră a gestionarului de fișiere și schimbați directorul cu cel care începe cu „LibreOffice_”, urmat de numărul versiunii și câteva informații despre platformă.

Acest director conține un subdirector numit "RPMS". Schimbă la directorul "RPMS".

Faceți clic dreapta in director și alegeți opțiunea "Open in Terminal". Se va deschide o fereastră terminal. Din linia de comandă a ferestrei terminal, introduceți următoarea comandă (vi se va cere să introduceți parola dvs. de utilizator root înainte de a se executa comanda):

For Fedora-based systems: sudo dnf install *.rpm

Pentru sistemele bazate pe Mandriva:  sudo urpmi *.rpm

Pentru alte sisteme bazate pe RPM (openSUSE, etc.): rpm -Uvh *.rpm

Procesul de instalare este acum încheiat și ar trebui să aveți iconițe pentru a vizualiza toate aplicațiile LibreOffice în meniul Aplicațiile desktop-ului / Office.

Ca alternativă folosiți scriptul „install”, găsit la nivelul superior al arhivei pentru instalare ca utilizator. Scriptul setează în așa fel instalarea lui LibreOffice ca să creeze profil distinct față de instalarea normală. Nu uitați că această instalare nu va instala integrarea în sistemul de operare, ca iconițele desktop, sau nu setează tipurile de fișiere MIME.

Note privind integrarea Desktop pentru distribuții Linux nu sunt cuprinse în instrucțiunile de instalare de mai sus
----------------------------------------------------------------------

Instalarea LibreOffice pe alte distribuții de Linux nespecificate în aceste instrucțiuni de instalare ar trebui să fie simplă. Ar putea să apară diferențe la integrarea desktop.

The RPMS (or DEBS, respectively) directory also contains a package named libreoffice7.4-freedesktop-menus-7.4.0.1-1.noarch.rpm (or libreoffice7.4-debian-menus_7.4.0.1-1_all.deb, respectively, or similar). This is a package for all Linux distributions that support the Freedesktop.org specifications/recommendations (https://en.wikipedia.org/wiki/Freedesktop.org), and is provided for installation on other Linux distributions not covered in the aforementioned instructions.

Instalarea unui Pachet Lingvistic
----------------------------------------------------------------------

Descărcați pachetul lingvistic pentru limba și platforma dorită. Acestea sunt disponibile în aceeași locație unde se găsește și arhiva pentru instalarea aplicației. Din managerul de fișiere Nautilus, extrageți arhiva descărcată într-un director (în desktop, de exemplu). Asigurați-vă că ați ieșit din toate aplicațiile LibreOffice (inclusiv Quickstarter, în cazul în care este pornit).

Schimbați directorul la directorul în care ați extras pachetul lingvistic descărcat.

Acum intrați în directorul care a fost creat în timpul procesului de extracție. De exemplu, pentru pachetul de limbă română pentru un sistem 32-bit bazat pe Debian/Ubuntu, directorul se numește LibreOffice_(versiune)_Linux_x86_langpack-deb_ro.

Acum schimbați directorul către cel care conține pachetele pentru instalare. Pe sistemele bazate pe Debian/Ubuntu, directorul va fi DEBS. Pentru sistemele Fedora, openSUSE sau Mandriva, acesta va fi RPMS.

Din managerul de fișiere Nautilus, faceți clic dreapta în director și alegeți comanda "Open in terminal". În fereastra de terminal pe care tocmai ați deschis-o, executați comanda pentru instalarea pachetul lingvistic (cu toate comenzile de mai jos - e posibil să vi se solicite introducerea parolei dvs. de utilizator root):

Pentru Debian / sisteme de operare bazate pe Ubuntu: sudo dpkg -i *.deb

For Fedora-based systems: su -c 'dnf install *.rpm'

Pentru sistemele bazate pe Mandriva:  sudo urpmi *.rpm

Pentru celelalte sisteme care utilizează RPM (openSUSE, etc.): rpm -Uvh *.rpm

Acum rulați una dintre aplicatiile LibreOffice - Writer, de exemplu. Din meniul Tools/Instrumente alegeti Options/Opțiuni. În caseta de dialog Opțiuni, faceți clic pe "Language Settings/Setări lingvistice" și apoi faceți clic pe "Limbi". Din lista derulantă "interfață utilizator" selectați limba pe care tocmai ați instalat-o. Dacă doriți, puteți face acelasi lucru pentru "Setări Locale", "Moneda implicită", și "Limbi implicite pentru documente".

După ajustarea acestor setări, dați clic pe OK. Caseta de dialog se va închide și veți vedea un mesaj de informare care vă anunță că modificările vor fi activate numai după ce închideți și reporniți LibreOffice (nu uitați să închideți și Quickstarter în cazul în care acesta este pornit).

Data viitoare când porniți LibreOffice, acesta va porni în limba pe care tocmai ați instalat-o.

----------------------------------------------------------------------
Probleme în timpul pornirii programului
----------------------------------------------------------------------

Difficulties starting LibreOffice (e.g. applications hang) as well as problems with the screen display are often caused by the graphics card driver. If these problems occur, please update your graphics card driver or try using the graphics driver delivered with your operating system.

----------------------------------------------------------------------
Touchpad-uri ALPS/Synaptics notebook în Windows
----------------------------------------------------------------------

Datorită unei probleme cu driverul Windows, nu puteți derula documente LibreOffice alunecînd cu degetul peste un touchpad ALPS/Synaptics.

Pentru a permite derularea touchpad, adaugați următoarele linii "C:\Program Files\Synaptics\SynTP\SynTPEnh.ini" la fișierul de configurare, și reporniți computerul:

[LibreOffice]

FC = "SALFRAME"

SF = 0x10000000

SF |= 0x00004000

Locația fișierului de configurare ar putea varia pe diferite versiuni de Windows.

----------------------------------------------------------------------
Taste rapide
----------------------------------------------------------------------

Doar comenzile rapide (combinațiile de taste) care nu sunt folosite de către sistemul de operare pot fi utilizate în LibreOffice. Dacă o combinație de taste în LibreOffice nu funcționează așa cum este descris în ajutorul LibreOffice, verificați dacă această comandă rapidă este deja utilizată de către sistemul de operare. Pentru a remedia astfel de conflicte, puteți schimba tastele atribuite de sistemul de operare. Alternativ, aveți posibilitatea să modificați aproape orice atribuire a tastei în LibreOffice. Pentru mai multe informații despre acest subiect, consultați ajutorul LibreOffice sau documentația ajutor al sistemului de operare.

----------------------------------------------------------------------
Problems When Sending Documents as Emails From LibreOffice
----------------------------------------------------------------------

When sending a document via 'File - Send - Document as Email' or 'Document as PDF Attachment' problems might occur (program crashes or hangs). This is due to the Windows system file "Mapi" (Messaging Application Programming Interface) which causes problems in some file versions. Unfortunately, the problem cannot be narrowed down to a certain version number. For more information visit https://www.microsoft.com to search the Microsoft Knowledge Base for "mapi dll".

----------------------------------------------------------------------
Note importante de acces
----------------------------------------------------------------------

For more information on the accessibility features in LibreOffice, see https://www.libreoffice.org/accessibility/

----------------------------------------------------------------------
Asistență utilizator
----------------------------------------------------------------------

Pagina principală de asistență oferă diverse posibilități de ajutor pentru LibreOffice. Este posibil ca întrebarea dumneavoastră să fi primit deja răspuns – verificați forumul comunității la https://www.documentfoundation.org/nabble/ sau căutați arhivele listei de corespondență 'users@libreoffice.org' la https://www.libreoffice.org/lists/users/. Alternativ, puteți trimite întrebările la adresa de e-mail users@libreoffice.org. Dacă doriți să vă abonați la listă (pentru a primi răspunsuri prin e-mail), trimiteți un e-mail gol la: users+subscribe@libreoffice.org.

Also check the FAQ section at the LibreOffice website.

----------------------------------------------------------------------
Raportarea unor bug-uri și probleme
----------------------------------------------------------------------

Sistemul nostru de raportare, urmărire și rezolvare a erorilor este în prezent Bugzilla, găzduit la https://bugs.documentfoundation.org/. Încurajăm toți utilizatorii să se simtă îndreptățiți și bineveniți în a raporta erori care pot apărea pe platforma pe care rulează programul. Raportarea energică a erorilor este una dintre cele mai importante contribuții pe care comunitatea de utilizatori le poate aduce la dezvoltarea și îmbunătățirea continuă a LibreOffice.

----------------------------------------------------------------------
Cum vă puteți implica
----------------------------------------------------------------------

Comunitatea LibreOffice ar avea foarte mult de câștigat din participarea dumneavoastră activă la dezvoltarea acestui important proiect cu sursă deschisă.

În calitate de utilizator, sunteți deja o parte valoroasă a procesului de dezvoltare a suitei și am dori să vă încurajăm să vă asumați un rol și mai activ pentru a fi un contribuitor pe termen lung al comunității. Vă rugăm să vă alăturați și să consultați pagina de contribuție de pe site-ul web LibreOffice.

Cum să începeți
----------------------------------------------------------------------

Cea mai bună modalitate de a începe contribuția este abonarea la una sau mai multe dintre listele de corespondență, urmărirea lor o vreme și folosirea treptată a arhivelor de e-mail pentru a familiarizarea cu multe dintre subiectele acoperite de când codul sursă LibreOffice a fost lansat în Octombrie 2000. Când vă simțiți confortabil, tot ce trebuie să faceți este să trimiteți un e-mail de auto-introducere și să intrați imediat. Dacă sunteți familiarizat cu proiectele Open Source, verificați lista noastră de lucruri de făcut și vedeți dacă există ceva la site-ul web LibreOffice cu care doriți să ajutați.

Subscrie
----------------------------------------------------------------------

Here are a few of the mailing lists to which you can subscribe at https://www.libreoffice.org/get-help/mailing-lists/

* Noutăți: announce@documentfoundation.org *recomandat tuturor utilizatorilor* (trafic ușor)
* Lista principală de discuții (în limba engleză): users@global.libreoffice.org (trafic intenes)
* Proiect marketing: marketing@global.libreoffice.org
* Lista generală a dezvoltatorilor: libreoffice@lists.freedesktop.org (trafic intens)

Colaborarea la unul sau la mai multe Proiecte
----------------------------------------------------------------------

Puteți aduce contribuții importante la acest proiect open source chiar și dacă aveți experiență limitată în proiectarea software sau în scrierea de cod. Da, dumneavoastră!

Sperăm că vă face plăcere să lucrați cu noul LibreOffice 7.4 și că ni vă veți alătura online.

Comunitatea LibreOffice

----------------------------------------------------------------------
Cod sursă folosit / modificat
----------------------------------------------------------------------

Unele porțiuni Copyright 1998, 1999 James Clark. Unele porțiuni Copyright 1996, 1998 Netscape Communications Corporation.
