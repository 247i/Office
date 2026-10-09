
======================================================================
LibreOffice 25.8 Citește-mă
======================================================================


Pentru cele mai recente actualizări ale acestui fișier readme (citește-mă), consultă https://git.libreoffice.org/core/tree/master/README.md

Acest fișier conține informații importante despre aplicația LibreOffice. Se recomandă să citiți cu atenție aceste informații înainte de a începe instalarea.

Comunitatea LibreOffice este responsabilă pentru dezvoltarea acestui produs și vă invită să luați în considerare participarea în calitate de membru al comunității. Dacă sunteți un utilizator nou, puteți vizita site-ul web LibreOffice, unde veți găsi o mulțime de informații despre proiectul LibreOffice și comunitățile care există în jurul acestuia. Accesați https://www.libreoffice.org/.

Aplicația LibreOffice este într-adevăr gratuită pentru orice utilizator?
----------------------------------------------------------------------

Utilizarea LibreOffice este gratuită pentru toată lumea. Puteți lua și instala această copie a LibreOffice pe oricâte computere doriți și o puteți utiliza în orice scop doriti (inclusiv comercial, guvern, administrație publică și învățământ). Pentru mai multe detalii, după descărcare vedeți fișierul text care conține licența aplicației LibreOffice.

De ce aplicația LibreOffice este gratuită pentru orice utilizator?
----------------------------------------------------------------------

Puteți folosi gratuit această copie a LibreOffice, deoarece contribuitorii individuali și sponsorii corporativi au proiectat, dezvoltat, testat, tradus, sprijinit, comercializat și au ajutat în multe alte feluri pentru ca aplicația LibreOffice să fie ceea ce este astăzi – lider mondial în software-ul Open Source pentru casă și birou.

Dacă apreciați eforturile lor și doriți să vă asigurați că LibreOffice continuă să fie disponibil departe în viitor, vă rugăm să luați în considerare contribuția la proiect - consultați https://www.documentfoundation.org/contribution/ pentru detalii. Oricine poate aduce o contribuție de un fel.

----------------------------------------------------------------------
Note despre instalare
----------------------------------------------------------------------

LibreOffice necesită o versiune recentă a Mediului de Rulare Java (JRE) pentru a funcționa la capacitate maximă.JRE nu face parte din pachetul de instalare al LibreOffice, el ar trebui instalat separat.

Descărcare
----------------------------------------------------------------------

* Microsoft Windows 10 sau mai nou

Pentru instalare aveți nevoie de drepturi de administrator.

Înregistrarea LibreOffice drept aplicație implicită pentru formatele Microsoft Office poate fi forțată sau suprimată folosind următoarele opțiuni în linia de comandă la lansarea asistentului de instalare:

* REGISTER_ALL_MSO_TYPES=1 va seta pentru formatele Microsoft Office ca program implicit, programul LibreOffice.
* REGISTER_NO_MSO_TYPES=1 nu va seta pentru formatele Microsoft Office ca program implicit, programul LibreOffice.

Asigurați-vă că aveți suficient spațiu liber în directorul temporar al sistemului dvs., și că ați citit drepturile de acces. Închideți toate celelalte programe înainte de a începe procesul de instalare.

Instalarea LibreOffice pe sistemele de operarea bazate pe Linux: Debian/Ubuntu
----------------------------------------------------------------------

Pentru instrucțiuni privind instalarea pachetelor de limbă (după ce aveți deja instalată LibreOffice în limba US English), citiți secțiunea de mai jos cu titlul Instalarea pachetelor de limbă.

Atunci când despachetezi arhiva descărcată, vei vedea că respectivul conținut a fost decomprimat într-un subdirector. Deschide o fereastră de gestionare a fișierelor și schimbă directorul în cel care începe cu „LibreOffice_”, urmat de numărul versiunii și câteva informații despre platformă.

Acest director conține un subdirector numit "Debs". Comută la directorul "Debs".

Faceți clic dreapta in director și alegeți opțiunea "Open in Terminal". Se va deschide o fereastră terminal. Din linia de comandă a ferestrei terminal, introduceți următoarea comandă (vi se va cere să introduceți parola dvs. de utilizator root înainte de a se executa comanda):

Următoarele comenzi vor instala LibreOffice și pachetele de integrare desktop (le poți copia și lipi în ecranul terminalului în loc să încerci să le tastezi):

sudo dpkg -i *.deb

Procesul de instalare este acum încheiat și ar trebui să aveți iconițe pentru a vizualiza toate aplicațiile LibreOffice în meniul Aplicațiile desktop-ului / Office.

Instalarea LibreOffice pe Fedora, openSUSE, Mandriva și alte sisteme Linux folosind pachete RPM
----------------------------------------------------------------------

Pentru instrucțiuni privind instalarea pachetelor de limbă (după ce aveți deja instalată LibreOffice în limba US English), citiți secțiunea de mai jos cu titlul Instalarea pachetelor de limbă.

Atunci când despachetezi arhiva descărcată, vei vedea că respectivul conținut a fost decomprimat într-un subdirector. Deschide o fereastră de gestionare a fișierelor și schimbă directorul în cel care începe cu „LibreOffice_”, urmat de numărul versiunii și câteva informații despre platformă.

Acest director conține un subdirector numit "RPMS". Schimbă la directorul "RPMS".

Faceți clic dreapta in director și alegeți opțiunea "Open in Terminal". Se va deschide o fereastră terminal. Din linia de comandă a ferestrei terminal, introduceți următoarea comandă (vi se va cere să introduceți parola dvs. de utilizator root înainte de a se executa comanda):

Pentru sistemele bazate pe Fedora: sudo dnf install *.rpm

Pentru sistemele bazate pe Mandriva:  sudo urpmi *.rpm

Pentru alte sisteme bazate pe RPM (openSUSE, etc.): rpm -Uvh *.rpm

Procesul de instalare este acum încheiat și ar trebui să aveți iconițe pentru a vizualiza toate aplicațiile LibreOffice în meniul Aplicațiile desktop-ului / Office.

Ca alternativă folosiți scriptul „install”, găsit la nivelul superior al arhivei pentru instalare ca utilizator. Scriptul setează în așa fel instalarea lui LibreOffice ca să creeze profil distinct față de instalarea normală. Nu uitați că această instalare nu va instala integrarea în sistemul de operare, ca iconițele desktop, sau nu setează tipurile de fișiere MIME.

Note privind integrarea Desktop pentru distribuții Linux nu sunt cuprinse în instrucțiunile de instalare de mai sus
----------------------------------------------------------------------

Instalarea LibreOffice pe alte distribuții de Linux nespecificate în aceste instrucțiuni de instalare ar trebui să fie simplă. Ar putea să apară diferențe la integrarea desktop.

Directorul RPMS (sau respectiv DEBS) conține și un pachet numit libreoffice25.8-freedesktop-menus-25.8.0.1-1.noarch.rpm (sau respectiv libreoffice25.8-debian-menus_25.8.0.1-1_all.deb sau similar). Acesta este un pachet pentru toate distribuțiile Linux care acceptă specificațiile/recomandările Freedesktop.org (https://en.wikipedia.org/wiki/Freedesktop.org) și este furnizat pentru instalare pe alte distribuții Linux care nu sunt acoperite de instrucțiunile menționate anterior.

Instalarea unui Pachet Lingvistic
----------------------------------------------------------------------

Descărcați pachetul lingvistic pentru limba și platforma dorită. Acestea sunt disponibile în aceeași locație unde se găsește și arhiva pentru instalarea aplicației. Din managerul de fișiere Nautilus, extrageți arhiva descărcată într-un director (în desktop, de exemplu). Asigurați-vă că ați ieșit din toate aplicațiile LibreOffice (inclusiv Quickstarter, în cazul în care este pornit).

Schimbați directorul la directorul în care ați extras pachetul lingvistic descărcat.

Acum schimbă directorul în directorul care a fost creat în timpul procesului de extragere. De exemplu, pentru pachetul lingvistic francez pentru un sistem bazat pe Debian/Ubuntu pe 32 de biți, directorul este denumit LibreOffice_, plus câteva informații despre versiune, plus Linux_x86_langpack-deb_fr.

Acum schimbați directorul către cel care conține pachetele pentru instalare. Pe sistemele bazate pe Debian/Ubuntu, directorul va fi DEBS. Pentru sistemele Fedora, openSUSE sau Mandriva, acesta va fi RPMS.

Din managerul de fișiere Nautilus, faceți clic dreapta în director și alegeți comanda "Open in terminal". În fereastra de terminal pe care tocmai ați deschis-o, executați comanda pentru instalarea pachetul lingvistic (cu toate comenzile de mai jos - e posibil să vi se solicite introducerea parolei dvs. de utilizator root):

Pentru Debian / sisteme de operare bazate pe Ubuntu: sudo dpkg -i *.deb

Pentru sistemele bazate pe Fedora: su -c 'dnf install *.rpm'

Pentru sistemele bazate pe Mandriva:  sudo urpmi *.rpm

Pentru celelalte sisteme care utilizează RPM (openSUSE, etc.): rpm -Uvh *.rpm

Acum pornește una dintre aplicațiile LibreOffice - de exemplu, Writer. Accesează meniul Instrumente și alegeți Opțiuni. În caseta de dialog Opțiuni, dă clic pe „Limbi și setări regionale”, apoi pe „General”. Derulează lista „Interfața utilizatorului” și selectează limba pe care tocmai ai instalat-o. Dacă vrei, fă același lucru pentru „Setări regionale”, „Monedă implicită” și „Limbi implicite pentru documente”.

După ajustarea acestor setări, dați clic pe OK. Caseta de dialog se va închide și veți vedea un mesaj de informare care vă anunță că modificările vor fi activate numai după ce închideți și reporniți LibreOffice (nu uitați să închideți și Quickstarter în cazul în care acesta este pornit).

Data viitoare când porniți LibreOffice, acesta va porni în limba pe care tocmai ați instalat-o.

----------------------------------------------------------------------
Probleme în timpul pornirii programului
----------------------------------------------------------------------

Dificultățile la pornirea LibreOffice (de exemplu, blocarea aplicațiilor), precum și problemele de afișare pe ecran sunt adesea cauzate de driverul plăcii grafice (plăcii video). Dacă apar aceste probleme, te rugăm să actualizezi driverul plăcii grafice (plăcii video) sau să încerci să folosești driverul grafic livrat împreună cu sistemul de operare.

----------------------------------------------------------------------
Touchpad-uri ALPS/Synaptics notebook în Windows
----------------------------------------------------------------------

Datorită unei probleme cu driverul Windows, nu puteți derula prin documentele LibreOffice când glisați degetul pe un touchpad ALPS/Synaptics.

Pentru a permite derularea touchpad, adaugați următoarele linii "C:\Program Files\Synaptics\SynTP\SynTPEnh.ini" la fișierul de configurare, și reporniți computerul:

[LibreOffice]

FC = "SALFRAME"

SF = 0x10000000

SF |= 0x00004000

Locația fișierului de configurare ar putea varia pe diferite versiuni de Windows.

----------------------------------------------------------------------
Comenzi rapide de la tastatură
----------------------------------------------------------------------

Doar comenzile rapide (combinațiile de taste) care nu sunt folosite de către sistemul de operare pot fi utilizate în LibreOffice. Dacă o combinație de taste în LibreOffice nu funcționează așa cum este descris în ajutorul LibreOffice, verificați dacă această comandă rapidă este deja utilizată de către sistemul de operare. Pentru a remedia astfel de conflicte, puteți schimba tastele atribuite de sistemul de operare. Alternativ, aveți posibilitatea să modificați aproape orice atribuire a tastei în LibreOffice. Pentru mai multe informații despre acest subiect, consultați ajutorul LibreOffice sau documentația ajutor al sistemului de operare.

----------------------------------------------------------------------
Probleme la trimiterea documentelor ca e-mailuri de la LibreOffice
----------------------------------------------------------------------

La trimiterea unui document prin „Fișier - Trimitere - E-mail document” sau „Fișier - Trimitere - E-mail ca PDF”, pot apărea probleme (blocări ale programului). Acest lucru se datorează fișierului de sistem Windows „Mapi” (Messaging Application Programming Interface), care cauzează probleme în anumite versiuni de fișiere. Din păcate, problema nu poate fi limitată la un anumit număr de versiune. Pentru mai multe informații, vizitează https://www.microsoft.com pentru a căuta în baza de cunoștințe Microsoft „mapi dll”.

----------------------------------------------------------------------
Note importante de acces
----------------------------------------------------------------------

Pentru mai multe informații despre funcțiile de accesibilitate din LibreOffice, consultă https://www.libreoffice.org/accessibility/

----------------------------------------------------------------------
Asistență utilizator
----------------------------------------------------------------------

Pagina principală de asistență oferă diverse posibilități de ajutor cu LibreOffice. Este posibil ca întrebarea ta. să fi primit deja răspuns - consultă Forumul Comunității la https://ask.libreoffice.org/ sau căutați în arhivele listei de discuții „users@libreoffice.org” la https://www.libreoffice.org/lists/users/. În mod alternativ, poți trimite întrebările tale la users@libreoffice.org. Dacă dorești să te abonezi la listă (pentru a primi răspunsuri prin e-mail), trimite un e-mail gol la: users+subscribe@libreoffice.org.

Consultă și secțiunea Întrebări frecvente de pe site-ul web LibreOffice.

----------------------------------------------------------------------
Raportarea unor bug-uri și probleme
----------------------------------------------------------------------

Sistemul nostru de raportare, urmărire și rezolvare a erorilor este în prezent Bugzilla, găzduit la https://bugs.documentfoundation.org/. Încurajăm toți utilizatorii să se simtă îndreptățiți și bineveniți în a raporta erori care pot apărea pe platforma pe care rulează programul. Raportarea energică a erorilor este una dintre cele mai importante contribuții pe care comunitatea de utilizatori le poate aduce la dezvoltarea și îmbunătățirea continuă a LibreOffice.

----------------------------------------------------------------------
Cum vă puteți implica
----------------------------------------------------------------------

Comunitatea LibreOffice ar avea foarte mult de câștigat din participarea ta activă la dezvoltarea acestui important proiect cu sursă deschisă.

În calitate de utilizator, sunteți deja o parte valoroasă a procesului de dezvoltare a suitei și am dori să vă încurajăm să vă asumați un rol și mai activ pentru a fi un contribuitor pe termen lung al comunității. Vă rugăm să vă alăturați și să consultați pagina de contribuție de pe site-ul web LibreOffice.

Cum să începeți
----------------------------------------------------------------------

Cea mai bună modalitate de a începe contribuția este abonarea la una sau mai multe dintre listele de corespondență, urmărirea lor o vreme și folosirea treptată a arhivelor de e-mail pentru a familiarizarea cu multe dintre subiectele acoperite de când codul sursă LibreOffice a fost lansat în Octombrie 2000. Când vă simțiți confortabil, tot ce trebuie să faceți este să trimiteți un e-mail de auto-introducere și să intrați imediat. Dacă sunteți familiarizat cu proiectele Open Source, verificați lista noastră de lucruri de făcut și vedeți dacă există ceva la site-ul web LibreOffice cu care doriți să ajutați.

Subscrie
----------------------------------------------------------------------

Aici sunt câteva dintre listele de discuții la care te poți abona la https://www.libreoffice.org/get-help/mailing-lists/

* Noutăți: announce@documentfoundation.org *recomandat tuturor utilizatorilor* (trafic ușor)
* Lista principală de discuții (în limba engleză): users@global.libreoffice.org (trafic intenes)
* Proiect marketing: marketing@global.libreoffice.org
* Lista generală a dezvoltatorilor: libreoffice@lists.freedesktop.org (trafic intens)

Colaborarea la unul sau la mai multe Proiecte
----------------------------------------------------------------------

Poți aduce contribuții importante la acest proiect open source chiar și dacă ai experiență limitată în proiectare software sau în scriere de cod. Da, tu!

Sperăm că vă face plăcere să lucrați cu noul LibreOffice 25.8 și că ni vă veți alătura online.

Comunitatea LibreOffice

----------------------------------------------------------------------
Cod sursă folosit / modificat
----------------------------------------------------------------------

Unele porțiuni Copyright 1998, 1999 James Clark. Unele porțiuni Copyright 1996, 1998 Netscape Communications Corporation.
