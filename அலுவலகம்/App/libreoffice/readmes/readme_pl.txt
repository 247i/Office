
======================================================================
Plik ReadMe programu LibreOffice 7.4
======================================================================


Aby uzyskać najnowsze aktualizacje tego pliku readme, odwiedź https://git.libreoffice.org/core/tree/master/README.md

Ten plik zawiera istotne informacje dotyczące oprogramowania LibreOffice. Przeczytaj go uważnie przed rozpoczęciem instalacji.

Społeczność LibreOffice jest odpowiedzialna za rozwój tego programu i chce byś stał się jednym z jej członków. Jeśli jesteś nowym użytkownikiem, odwiedź stronę LibreOffice na której znajdziesz informacje o projekcie LibreOffice oraz jego społeczności. Odwiedź http://www.libreoffice.org/.

Czy LibreOffice naprawdę jest bezpłatny dla wszystkich?
----------------------------------------------------------------------

Program LibreOffice jest bezpłatny dla wszystkich. Możesz używać tej kopii LibreOffice i instalować ją na tylu komputerach ilu tylko chcesz oraz używać jej w każdym celu (komercyjnym, rządowym, edukacyjnym i w instytucjach administracji publicznej). Więcej szczegółów można znaleźć w licencji dołączonej do pobranego LibreOffice.

Dlaczego program LibreOffice jest bezpłatny dla każdego?
----------------------------------------------------------------------

Możesz używać tej kopii LibreOffice bez ponoszenia żadnych opłat ponieważ wielu współpracowników i sponsorów go projektowało, tworzyło, testowało, opisywało, wspierało, reklamowało i pomagało na wiele innych sposobów. Dzięki temu LibreOffice jest tym czym jest dzisiaj - liderem wśród pakietów biurowych typu Open Source na świecie, do użytku w domu i w firmie.

Jeśli doceniasz ich trud i chcesz mieć pewność, że w przyszłości LibreOffice nadal będzie dostępny bezpłatnie, zastanów się nad dołączeniem do projektu – odwiedź https://www.documentfoundation.org/contribution/, aby dowiedzieć się więcej. Każdy może w jakiś sposób pomóc.

----------------------------------------------------------------------
Uwagi dotyczące instalacji
----------------------------------------------------------------------

LibreOffice wymaga najnowszej wersji środowiska Java Runtime Environment (JRE) dla pełnej funkcjonalności. JRE nie jest częścią pakietu instalacyjnego LibreOffice i powinien być zainstalowana oddzielnie.

Wymagania systemowe
----------------------------------------------------------------------

* Microsoft Windows 7 SP1, 8, 8.1 Update (S14) lub 10

Do przeprowadzenia instalacji potrzebne są uprawnienia administratora.

Rejestrację systemu LibreOffice jako domyślnej aplikacji do obsługi formatów Microsoft Office można wymusić lub wyłączyć, używając instalatora z następującymi przełącznikami wiersza poleceń:

* REGISTER_ALL_MSO_TYPES=1 zmusi rejestrację LibreOffice jako domyślną aplikację dla formatów Microsoft Office.
* REGISTER_NO_MSO_TYPES=1 wstrzyma rejestrację LibreOffice jako domyślną aplikację dla formatów Microsoft Office.

Należy upewnić się, że jest wystarczająca ilość wolnego miejsca w katalogu tymczasowym oraz, że zostały przyznane uprawnienia odczytu, zapisu i uruchomienia. Przed rozpoczęciem procesu instalacji należy zamknąć inne programy.

Instalacja LibreOffice w systemach Linux opartych na Debianie/Ubuntu
----------------------------------------------------------------------

Aby uzyskać instrukcje jak zainstalować pakiet językowy (po instalacji anglojęzycznej wersji LibreOffice), proszę zapoznać się z poniższą sekcją zatytułowaną Instalacja pakietu językowego.

Po rozpakowaniu pobranego archiwum jego zawartość pojawi się w nowym podkatalogu. Należy otworzyć menedżer plików i przejść do katalogu, którego nazwa rozpoczyna się od "LibreOffice_" i w dalszej części zawiera numer wersji i informację o dedykowanej platformie.

Ten katalog zawiera podkatalog o nazwie "DEBS". Zmień katalog na "DEBS".

Kliknij prawym przyciskiem myszy na katalogu i wybierz z menu "Otwórz w Terminalu". Okno terminala otworzy się. W wierszu poleceń należy wpisać następujące polecenie (zostaniesz zapytany o hasło użytkownika root zanim polecenie zostanie wykonane):

Następujące polecenie zainstaluje LibreOffice oraz pakiet integrujący go z pulpitem (zamiast wpisywać je ręcznie, możesz przekopiować polecenie do terminala):

sudo dpkg -i *.deb

Proces instalacji jest teraz ukończony a ikony wszystkich aplikacji LibreOffice powinny być widoczne w menu Programy/Biuro.

Instalacja LibreOffice dla Fedory, openSUSE, Mandrivy i innych dystrybucji Linuksa używających pakietów RPM
----------------------------------------------------------------------

Aby uzyskać instrukcje jak zainstalować pakiet językowy (po instalacji anglojęzycznej wersji LibreOffice), proszę zapoznać się z poniższą sekcją zatytułowaną Instalacja pakietu językowego.

Po rozpakowaniu pobranego archiwum jego zawartość pojawi się w nowym podkatalogu. Należy otworzyć menedżer plików i przejść do katalogu, którego nazwa rozpoczyna się od "LibreOffice_" i w dalszej części zawiera numer wersji i informację o dedykowanej platformie.

Ten katalog zawiera podkatalog nazwany "RPMS". Zmień katalog na "RPMS".

Kliknij prawym przyciskiem myszy na katalogu i wybierz z menu "Otwórz w Terminalu". Okno terminala otworzy się. W wierszu poleceń należy wpisać następujące polecenie (zostaniesz zapytany o hasło użytkownika root zanim polecenie zostanie wykonane):

W przypadku systemów bazujących na Fedorze: sudo dnf install *.rpm

Dla systemów opartych na dystrybucji Mandriva: sudo urpmi *.rpm

Dla innych systemów opartych na pakietach RPM (openSUSE, itp.): rpm -Uvh *.rpm

Proces instalacji jest teraz ukończony a ikony wszystkich aplikacji LibreOffice powinny być widoczne w menu Programy/Biuro.

Możesz również użyć skryptu 'install' umiejscowionego w najwyższym poziomie folderu archiwum, aby uruchomić instalację jako użytkownik. Skrypt skonfiguruje LibreOffice z własnym profilem, oddzielonym od twojego normalnego profilu LibreOffice. Zauważ, że to nie będzie instalacja elementów integrujących system, takich jak pozycje w menu pulpitu i wpisy w rejestrze MIME.

Uwagi odnośnie integracji z pulpitem dla dystrybucji Linuksa nie uwzględnionych w powyższej instrukcji instalacji
----------------------------------------------------------------------

Instalacja LibreOffice powinna być całkiem łatwa w dystrybucjach Linuksa, które pominięto w tej instrukcji instalacji. Jedyna widoczna różnica może mieć miejsce w integracji z pulpitem.

Katalog RPM (lub odpowiednio DEB) zawiera również pakiet o nazwie libreoffice7.4-freedesktop-menus-7.4.0.1-1.noarch.rpm (lub libreoffice7.4-debian-menus_7.4.0.1-1_all.deb). Jest on przeznaczony dla wszystkich dystrybucji Linuksa które wspierają specyfikacje/rekomendacje Freedesktop.org (https://en.wikipedia.org/wiki/Freedesktop.org) i nie zostały ujęte w niniejszej instrukcji.

Instalacja pakietu językowego
----------------------------------------------------------------------

Należy pobrać pakiet językowy dla odpowiedniego języka i platformy. Pakiety dostępne są w tym samym miejscu co główne archiwum instalacyjne. Za pomocą menedżera plików należy rozpakować pobrane archiwum do katalogu (np. na pulpit). Należy również upewnić się, że żaden z programów pakietu LibreOffice nie jest uruchomiony (łącznie z modułem szybkiego uruchamiania QuickStarter).

Należy przejść do katalogu, gdzie pobrany pakiet językowy został rozpakowany.

Po rozpakowaniu pakietu językowego należy przejść do katalogu który został utworzony. Na przykład, dla francuskiego pakietu językowego dla systemu Debian/Ubuntu 32-bit, nazwa katalogu rozpoczyna się od LibreOffice_ i w dalszej części zawiera numer wersji oraz Linux_x86_langpack-deb_fr.

Następnie udajemy się do katalogu zawierającego pakiety instalacyjne. Dla systemów opartych na dystrybucji Debian/Ubuntu, katalog ten nazywa się DEBS. Dla systemów Fedora, openSUSE i Mandriva katalog ten nazywa się RPMS.

Kliknij prawym przyciskiem myszy na katalogu i wybierz z menu "Otwórz w Terminalu". Okno terminala otworzy się. Aby zainstalować pakiet językowy, w wierszu poleceń należy wpisać następujące polecenie (zostaniesz zapytany o hasło użytkownika root zanim polecenie zostanie wykonane):

Dla systemów bazujących na Debianie/Ubuntu: sudo dpkg -i *.deb

W przypadku systemów bazujących na Fedorze: su -c 'dnf install *.rpm'

Dla systemów opartych na dystrybucji Mandriva: sudo urpmi *.rpm

Dla innych systemów używających RPM (openSUSE, etc.): rpm -Uvh *.rpm

Uruchom jeden z programów wchodzących w skład LibreOffice - na przykład Writer. Z menu Narzędzia wybierz Opcje. W oknie dialogowym Opcje aktywuj "Ustawienie językowe" i wybierz "Języki". Z listy dla "Interfejs użytkownika" wybierz nowo zainstalowany język. Można zrobić to samo dla "Ustawienia regionalne", "Waluta domyślna" i "Domyślny język dokumentów".

Po zmianie tych ustawień należy nacisnąć przycisk OK. Okno dialogowe zamknie się i zostanie wyświetlona informacja o tym, że dokonane zmiany odniosą skutek dopiero po ponownym uruchomieniu LibreOffice (pamiętaj o zakończeniu działania modułu szybkiego uruchamiania QuickStarter).

Zainstalowany i wybrany język będzie aktywny przy następnym uruchomieniu LibreOffice.

----------------------------------------------------------------------
Problemy podczas uruchamiania programu
----------------------------------------------------------------------

Problemy z uruchomieniem LibreOffice (np. zawieszanie się aplikacji) oraz problemy z wyświetlaniem ekranu są często spowodowane przez sterownik karty graficznej. Jeśli wystąpią te problemy, zaktualizuj sterownik karty graficznej lub spróbuj użyć sterownika karty graficznej dostarczonego z systemem operacyjnym.

----------------------------------------------------------------------
Tabliczki dotykowe w komputerach przenośnych ALPS/Synaptics w Windows
----------------------------------------------------------------------

Z powodu sterownika systemu Windows nie można przewijać dokumentów LibreOffice przesuwając palec po tabliczkach dotykowych komputerów przenoścnych ALPS/Synaptics.

Aby włączyć przewijanie, dodaj następujące linie do pliku konfiguracyjnego "C:\Program Files\Synaptics\SynTP\SynTPEnh.ini" i uruchom ponownie komputer:

[LibreOffice]

FC = "SALFRAME"

SF = 0x10000000

SF |= 0x00004000

Położenie pliku może się różnić w zależności od wersji systemu Windows.

----------------------------------------------------------------------
Skróty klawiaturowe
----------------------------------------------------------------------

W programie LibreOffice mogą być używane tylko te skróty klawiaturowe (kombinacje klawiszy), które nie są używane przez system operacyjny. Jeżeli skrót w programie LibreOffice nie działa w sposób opisany w pomocy LibreOffice, należy sprawdzić, czy nie jest on używany przez system operacyjny. Jeśli tak jest, możesz usunąć ten konflikt, zmieniając skróty używane przez system. Możesz również zmienić niemal każdy skrót używany w produkcie LibreOffice. Więcej informacji na ten temat znajduje się w pomocy do produktu LibreOffice oraz w dokumentacji używanego systemu operacyjnego.

----------------------------------------------------------------------
Problemy z wysyłaniem dokumentów jako e-maili z LibreOffice
----------------------------------------------------------------------

Podczas wysyłania dokumentu za pomocą opcji 'Plik - Wyślij - Dokument jako e-mail' lub 'Dokument jako załącznik PDF' mogą wystąpić problemy (awarie lub zawieszanie się programu). Jest to spowodowane plikiem systemowym Windows "Mapi" (Messaging Application Programming Interface), który powoduje problemy w niektórych wersjach plików. Niestety problemu nie można zawęzić do określonego numeru wersji. Aby uzyskać więcej informacji, odwiedź witrynę https://www.microsoft.com i wyszukaj "mapi dll" w bazie wiedzy Microsoft Knowledge Base.

----------------------------------------------------------------------
Ważne uwagi dotyczące dostępności
----------------------------------------------------------------------

Więcej informacji na temat dostępności w LibreOffice można znaleźć pod adresem https://www.libreoffice.org/accessibility/

----------------------------------------------------------------------
Wsparcie użytkownika
----------------------------------------------------------------------

Główna strona wsparcia Strona pomocy oferuje różne możliwości pomocy z LibreOffice. Możliwe, że odpowiedź na Twoje pytanie została już napisana - sprawdź Forum Społeczności pod adresem https://www.documentfoundation.org/nabble/ lub przeszukaj archiwum listy mailingowej 'users@libreoffice.org' pod adresem https://www.libreoffice.org/lists/users/. Możesz również wysłać swoje zapytanie na adres users@libreoffice.org. Jeśli chcesz subskrybować listę, wyślij pusty email na adres users+subscribe@libreoffice.org.

Sprawdź także sekcję FAQ na  stronie LibreOffice .

----------------------------------------------------------------------
Raport błędów & problemów
----------------------------------------------------------------------

BugZilla jest naszym systemem do raportowania, śledzenia i rozwiązywania błędów, dostępna pod adresem http://bugs.documentfoundation.org/. Zachęcamy wszystkich użytkowników do raportowania błędów, jakie mogę pojawić się na poszczególnych platformach. Energiczne raportowanie błędów jest jednym z najważniejszych działań, jakie społeczność użytkowników może wnieść do dalszego rozwoju i poprawyLibreOffice.

----------------------------------------------------------------------
Przyłącz się
----------------------------------------------------------------------

Społeczność LibreOffice odniosłaby wielką korzyść z Twojego aktywnego udziału w rozwoju tego ważnego projektu open source.

Jako użytkownik, jesteś już wartościową częścią procesu rozwojowego i chcielibyśmy zachęcić Cię do podjęcia bardziej aktywnej roli w długoterminowej współpracy ze społecznością. Odwiedź i sprawdź stronę z informacjami o możliwych sposobach współpracy pod adresem Strony LibreOffice.

Jak rozpocząć współpracę?
----------------------------------------------------------------------

Najlepszym sposobem na rozpoczęcie współpracy jest zapisanie się na jedną lub więcej list mailingowych, przeglądanie archiwum i stopniowe zapoznawanie się z tematami tam poruszonymi. Z racji, że kod źródłowy LibreOffice został wydany w Październiku 2000, zakres tematyczny list jest dość obszerny. Gdy będziesz już zdecydowany, jedyne co powinieneś zrobić to wysłać email w którym krótko przedstawisz by następnie wskoczyć na głęboką wodę. Jeśli projekty Open Source nie są Ci obce, sprawdź naszą listę TODO i zobacz czy jest tam coś przy czym chciałbyś pomóc. Więcej informacji pod adresem Strony LibreOffice/.

Zapisz się
----------------------------------------------------------------------

Poniżej znajduje się kilka list mailingowych na które możesz się zapisać pod adresemhttps://www.libreoffice.org/get-help/mailing-lists/

* Nowości: announce@documentfoundation.org *zalecana dla wszystkich* (mały ruch)
* Główna lista użytkowników: users@global.libreoffice.org *w łatwy sposób podpatrzysz dyskusję* (duży ruch)
* Marketing: marketing@global.libreoffice.org *poza programowaniem* (coraz większy ruch)
* Ogólna lista programistów: libreoffice@lists.freedesktop.org (duży ruch)

Dołączanie do jednego lub więcej projektów
----------------------------------------------------------------------

Możesz mieć znaczący wkład w ten ważny projekt open source, nawet jeśli masz niewielkie doświadczenie w projektowaniu i tworzeniu oprogramowania. Tak, właśnie Ty!

Mamy nadzieję, że jesteś zadowolonym użytkownikiem nowego LibreOffice 7.4 i przyłączysz się do nas w internecie.

Społeczność LibreOffice

----------------------------------------------------------------------
Użyty / zmodyfikowany kod źródłowy
----------------------------------------------------------------------

Częściowe prawa autorskie 1998, 1999 James Clark. Częściowe prawa autorskie 1996, 1998 Netscape Communications Corporation.
