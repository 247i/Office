
======================================================================
LibreOffice 7.4:n LueMinut-tiedosto
======================================================================


Viimeisimmät päivitykset tähän readme-tiedostoon löytyvät osoitteesta https://git.libreoffice.org/core/tree/master/README.md

Tämä tiedosto sisältää tärkeää tietoa LibreOffice-ohjelmistosta. Sen huolellinen lukeminen ennen asennuksen aloittamista on suositeltavaa.

Tämän ohjelmiston kehittänyt LibreOffice-yhteisö haluaa kutsua myös sinut osallistumaan yhteisön toimintaan. Uutena käyttäjänä sinun olisi hyvä tutustua LibreOfficen sivustoon, josta löytyy paljon tietoa LibreOffice-projektista ja sen parissa toimivista yhteisöistä. Lisää tietoa löytyy osoitteesta https://fi.libreoffice.org/.

Onko LibreOffice todellakin maksuton kaikessa käytössä?
----------------------------------------------------------------------

LibreOffice on vapaasti käytettävissä maksutta kaikkiin tarkoituksiin, niin hallinnossa, yrityksissä, kouluissa kuin yksityisessä käytössäkin. Tämän kopion LibreOfficesta voi asentaa halutessaan useampaan kuin yhteen tietokoneeseen. Tarkemmat tiedot löytyvät LibreOfficen mukana tulevasta lisenssitekstistä.

Miksi LibreOffice on maksuton kaikessa käytössä?
----------------------------------------------------------------------

Tätä LibreOffice-ohjelmistoa voi käyttää maksutta, koska useat yksityiset henkilöt ja yritykset ovat suunnitelleet, kehittäneet, testanneet, kääntäneet, dokumentoineet, tukeneet ja markkinoineet ohjelmistoa tavoitteenaan tehdä siitä maailman johtava avoimen lähdekoodin toimisto-ohjelmisto. LibreOffice on tämän työn tulos.

Jos arvostat tätä työtä ja haluat auttaa LibreOfficea kehittymään jatkossakin, voit osallistua projektiin. Katso lisää tietoa osoitteesta https://www.documentfoundation.org/contribution/. Kaikki voivat osallistua jollakin tavalla.

----------------------------------------------------------------------
Huomioita asennuksesta
----------------------------------------------------------------------

LibreOffice vaatii eräiden toimintojen suorittamiseen ajantasaisen version Java-ajoympäristöstä (JRE). JRE ei kuulu LibreOfficen asennuspakettiin, se täytyy tarvittaessa asentaa erikseen.

Järjestelmävaatimukset
----------------------------------------------------------------------

* Microsoft Windows 7 SP1, 8, 8.1 Update (S14) tai 10

Asennusprosessi vaatii järjestelmänvalvojan käyttöoikeudet.

LibreOfficen rekisteröinti oletussovellukseksi Microsoft Office -tiedostomuodoille voidaan pakottaa tai estää seuraavilla asennusohjelman komentorivivalitsimilla:

* REGISTER_ALL_MSO_TYPES=1 pakottaa LibreOfficen rekisteröinnin oletussovellukseksi Microsoft Office -tiedostomuodoille.
* REGISTER_NO_MSO_TYPES=1 estää LibreOfficen rekisteröinnin oletussovellukseksi Microsoft Office -tiedostomuodoille.

Varmista, että järjestelmäsi väliaikaishakemistossa on riittävästi vapaata levytilaa ja että sinulla on siihen riittävät luku-, kirjoitus- ja suoritusoikeudet. Sulje kaikki muut ohjelmat ennen asennuksen aloittamista.

LibreOfficen asentaminen Debian- tai Ubuntu-pohjaisiin Linux-järjestelmiin
----------------------------------------------------------------------

Ohjeita kielipaketin asentamiseen amerikanenglanninkielisen LibreOffice-version päälle löytyy alempaa kappaleesta Kielipaketin asentaminen.

Kun purat ladatun asennuspaketin, sen sisältö puretaan omaan kansioonsa. Avaa tiedostonhallintaohjelma ja siirry kansioon, jonka nimen alussa on "LibreOffice_" ja versioon ja käyttöjärjestelmään liittyviä tietoja.

Tässä kansiossa on alikansio nimeltä "DEBS". Avaa tämä "DEBS"-kansio.

Napsauta hiiren oikealla painikkeella kansion sisällä ja valitse "Avaa päätteessä". Tämä avaa pääteikkunan. Anna pääteikkunassa seuraava komento (tämä voi vaatia käyttäjätunnukseesi liittyvän salasanan antamisen):

Seuraavat komennot asentavat LibreOfficen ja työpöytäintegraatiopaketit (voit kopioida ja liittää ne pääteikkunaan sen sijaan, että kirjoittaisit ne käsin):

sudo dpkg -i *.deb

Asennus on nyt valmis, ja LibreOfficen käynnistyskuvakkeet löytyvät työpöytäympäristösi Sovellukset/Toimisto-valikosta.

LibreOfficen asentaminen Fedoraan, openSUSEen, Mandrivaan ja muihin RPM-pohjaisiin Linux-järjestelmiin
----------------------------------------------------------------------

Ohjeita kielipaketin asentamisesta amerikanenglanninkieliseen LibreOfficen versioon löytyy alempaa kohdasta Kielipaketin asentaminen.

Kun purat ladatun asennuspaketin, sen sisältö puretaan omaan kansioonsa. Avaa tiedostonhallintaohjelma ja siirry kansioon, jonka nimen alussa on "LibreOffice_" ja versioon ja käyttöjärjestelmään liittyviä tietoja.

Tässä kansiossa on alikansio nimeltä "RPMS". Avaa RPMS-kansio.

Napsauta hiiren oikealla painikkeella kansion sisällä ja valitse "Avaa päätteessä". Tämä avaa pääteikkunan. Anna pääteikkunassa seuraava komento (tämä voi vaatia käyttäjätunnukseesi liittyvän salasanan antamisen):

Fedora-pohjaisissa järjestelmissä: sudo dnf install *.rpm

Mandriva-pohjaisissa järjestelmissä: sudo urpmi *.rpm

Muissa RPM-pohjaisissa järjestelmissä (openSUSE jne.): rpm -Uvh *.rpm

Asennus on nyt valmis, ja LibreOfficen käynnistyskuvakkeet löytyvät työpöytäympäristösi Sovellukset/Toimisto-valikosta.

Vaihtoehtoisesti voit käyttää 'install'-komentosarjaa, joka sijaitsee asennuspaketin pääkansiossa. Komentosarjan voi ajaa tavallisen käyttäjän oikeuksilla ja se asentaa LibreOfficen niin, että se käyttää erillistä asetuskansiota, joka ei ole sama kuin järjestelmänlaajuisesti asennetun LibreOfficen käyttämä asetuskansio. Huomaa, että tämä ei asenna järjestelmäintegraatioon liittyviä osia kuten käynnistysvalikkoon tulevia kuvakkeita tai MIME-tyyppien rekisteröintiä.

Työpöytäympäristöön integrointi muissa kuin aiemmin käsitellyissä Linux-jakeluissa
----------------------------------------------------------------------

LibreOfficen asentaminen muihin kuin tässä ohjeessa mainittuihin Linux-jakeluihin onnistuu tavallisesti samaan tapaan kuin Debian- tai Fedora-pohjaisiin järjestelmiin. Järjestelmien väliset erot liittyvät yleensä sovelluksen ja työpöytäympäristön väliseen integraatioon.

Kansio RPMS (tai DEBS) sisältää myös paketin nimeltä libreoffice7.4-freedesktop-menus-7.4.0.1-1.noarch.rpm (tai libreoffice7.4-debian-menus_7.4.0.1-1_all.deb, tai vastaavan). Tämä paketti soveltuu kaikille Linux-jakeluille, jotka tukevat Freedesktop.orgin määrityksiä (https://en.wikipedia.org/wiki/Freedesktop.org). Se on tarkoitettu sellaisia Linux-jakeluita varten, joille ei ollut ohjeita edellä.

Kielipaketin asentaminen
----------------------------------------------------------------------

Lataa käyttöjärjestelmäsi ja haluamasi kielen mukainen asennuspaketti. Ne löytyvät samasta paikasta kuin varsinainen asennuspakettikin. Pura kielipaketti johonkin kansioon (esimerkiksi työpöydälle). Varmista, että LibreOffice (myös sen pikakäynnistys) on kokonaan suljettu.

Siirry kansioon, johon purit lataamasi kielipaketin.

Siirry kansioon, joka syntyi, kun kielipaketti purettiin. Esimerkiksi suomenkielinen kielipaketti 32-bittisessä Debian- tai Ubuntu-järjestelmässä puretaan kansioon, jonka nimessä on "LibreOffice_,", versiotietoja ja "Linux_x86_langpack-deb_fi".

Siirry tämän jälkeen kansioon, jossa asennettavat kielipaketit sijaitsevat. Debian- ja Ubuntu-järjestelmissä kansion nimi on DEBS. Fedora-, openSuse- ja Mandriva-järjestelmissä kansion nimi on RPMS.

Napsauta tiedostonhallintaohjelmassa kansion sisällä hiiren oikealla painikkeella ja valitse "Avaa päätteessä". Pääteikkuna avautuu. Anna päätteeseen seuraava komento kielipaketin asentamiseksi (komennot voivat vaatia käyttäjätunnukseesi liittyvän salasanan antamisen):

Debian- ja Ubuntu-järjestelmissä: sudo dpkg -i *.deb

Fedora-pohjaisissa järjestelmissä: su -c 'dnf install *.rpm'

Mandriva-pohjaisissa järjestelmissä: sudo urpmi *.rpm

Muissa RPM-pohjaisissa järjestelmissä (openSUSE jne.): rpm -Uvh *.rpm

Käynnistä jokin LibreOffice-sovelluksista, esimerkiksi Writer. Mene Työkalut-valikkoon ja valitse Asetukset. Asetukset-valintaikkunassa valitse "Kieliasetukset" ja sen alta "Kielet". Valitse asentamasi kieli "Käyttöliittymä"-pudotusvalikosta. Voit samalla myös tarkistaa, että maa-asetus, oletusvaluutta ja asiakirjojen oletuskielet ovat sopivat.

Kun olet muuttanut asetuksia, napsauta "OK". Näet ilmoituksen, jossa pyydetään sulkemaan LibreOffice ja käynnistämään se uudelleen, jotta uudet kieliasetukset tulevat voimaan. Muista myös sulkea ja käynnistää pikakäynnistyssovellus, jos se on käytössä.

Kun seuraavan kerran käynnistät LibreOfficen, asentamasi kieli on käytössä.

----------------------------------------------------------------------
Ongelmat ohjelman käynnistyksessä
----------------------------------------------------------------------

Ongelmat LibreOfficen käynnistämisessä (esim. sovellukset jumittuvat), kuten myös grafiikkaongelmat johtuvat usein näytönohjaimen ajurista. Mikäli tällaisia ongelmia ilmenee, päivitä näytönohjaimen ajuri tai kokeile käyttää käyttöjärjestelmän mukana toimitettua näytönohjaimen ajuria.

----------------------------------------------------------------------
Kannettavien tietokoneiden ALPS/Synaptics-kosketuslevyt Windowsissa
----------------------------------------------------------------------

Windowsin ajuriongelmasta johtuen LibreOffice-asiakirjoja ei voi vierittää liu'uttamalla sormea ALPS/Synaptics-kosketuslevyllä.

Kosketuslevyvierityksen saa käyttöön lisäämällä seuraavat rivit asetustiedostoon "C:\Program Files\Synaptics\SynTP\SynTPEnh.ini" ja käynnistämällä tietokoneen uudelleen:

[LibreOffice]

FC = "SALFRAME"

SF = 0x10000000

SF |= 0x00004000

Asetustiedoston sijainti saattaa vaihdella Windowsin eri versioissa.

----------------------------------------------------------------------
Pikanäppäimet
----------------------------------------------------------------------

Vain sellaisia pikanäppäimiä (näppäinyhdistelmiä), joita käyttöjärjestelmä ei käytä, voidaan käyttää LibreOfficessa. Jos LibreOfficen näppäinyhdistelmä ei toimi niin kuin on kuvattu LibreOfficen käytönaikaisessa ohjeessa, tarkista, onko kyseinen näppäinyhdistelmä jo käyttöjärjestelmän omassa käytössä. Voit korjata ongelman vaihtamalla näppäinten sidoksia käyttöjärjestelmässä. Vaihtoehtoisesti voit muuttaa lähes minkä tahansa näppäinsidoksen LibreOfficessa. Aiheesta saa lisätietoja LibreOfficen käytönaikaisesta ohjeesta ja käyttöjärjestelmäsi käyttöohjeista.

----------------------------------------------------------------------
Asiakirjojen sähköpostilla LibreOfficesta lähettämiseen liittyvät ongelmat
----------------------------------------------------------------------

When sending a document via 'File - Send - Document as Email' or 'Document as PDF Attachment' problems might occur (program crashes or hangs). This is due to the Windows system file "Mapi" (Messaging Application Programming Interface) which causes problems in some file versions. Unfortunately, the problem cannot be narrowed down to a certain version number. For more information visit https://www.microsoft.com to search the Microsoft Knowledge Base for "mapi dll".

----------------------------------------------------------------------
Tärkeitä saavutettavuustyökaluja koskevia ohjeita
----------------------------------------------------------------------

Lisää tietoa LibreOfficen saavutettavuustoiminnoista löytyy osoitteesta https://www.libreoffice.org/accessibility/

----------------------------------------------------------------------
Käyttäjätuki
----------------------------------------------------------------------

Tukisivustomme tarjoaa erilaisia tukivaihtoehtoja LibreOfficelle. Kysymyksiisi voi löytyä vastaus myös englanninkieliseltä keskustelualueelta https://www.documentfoundation.org/nabble/ tai englanninkieliseltä tukilistalta 'users@libreoffice.org' osoitteessa https://www.libreoffice.org/lists/users/. Voit myös lähettää kysymyksesi sähköpostitse julkiselle tukipostituslistalle osoitteeseen users@libreoffice.org. Jos haluat saada sähköpostiisi kaikki tukilistalle tulevat viestit, lähetä tyhjä sähköpostiviesti osoitteeseen users+subscribe@libreoffice.org.

Katso myös usein kysytyt kysymykset LibreOfficen sivustolta.

----------------------------------------------------------------------
Virheistä ja ongelmista ilmoittaminen
----------------------------------------------------------------------

Järjestelmämme ohjelmistovirheiden (bugien) raportointiin, seurantaan ja ratkomiseen on tällä hetkellä Bugzilla, joka sijaitsee osoitteessa https://bugs.documentfoundation.org/. Toivomme kaikkien käyttäjien ilmoittavan kohtaamistaan virheistä. Virheistä ilmoittaminen on yksi tärkeimmistä tavoista, joilla käyttäjäyhteisö voi osallistua LibreOfficen kehittämiseen entistäkin paremmaksi.

----------------------------------------------------------------------
Osallistuminen
----------------------------------------------------------------------

LibreOffice-yhteisö olisi erittäin kiitollinen aktiivisesta osallistumisestasi tämän keskeisen avoimen lähdekoodin projektin kehitystyöhön.

Käyttäjänäkin olet jo arvokas osa ohjelmiston kehitysprosessia. Haluaisimme rohkaista käyttäjiämme aktiivisuuteen, ja kannustamme sinua toimimaan yhteisön hyväksi pitkäaikaisena jäsenenä. Lisää tietoa tavoista osallistua löytyy LibreOffice-sivustolta.

Miten aloittaa
----------------------------------------------------------------------

Paras tapa aloittaa yhteisön toimintaan osallistuminen on tilata yksi tai useampia postituslistoja, seurata niillä käytävää keskustelua jonkin aikaa ja vähitellen käyttää postituslistojen arkistoja tutustuaksesi keskustelunaiheisiin, joita on käsitelty sen jälkeen kun LibreOfficen lähdekoodi alun perin julkaistiin syksyllä 2000. Tämän jälkeen voit lähettää listalle viestin, jossa esittelet itsesi ja tarjoudut auttamaan. Jos tunnet jo avoimen lähdekoodin kehitysprojekteja, vilkaise LibreOffice-sivustolta, mitä tehtävää olisi tarjolla.

Postituslistojen tilaaminen
----------------------------------------------------------------------

Tässä on muutamia englanninkielisiä sähköpostilistoja, joille voit liittyä osoitteessa https://www.libreoffice.org/get-help/mailing-lists/

* Uutiset: announce@documentfoundation.org *Suositellaan kaikille käyttäjille* (vähäinen liikenne)
* Pääasiallinen keskustelulista käyttäjille: users@global.libreoffice.org *Helppo tapa tutustua keskusteluihin* (paljon liikennettä)
* Markkinointiprojekti: marketing@global.libreoffice.org *muusta kuin kehityksestä* (reilusti liikennettä)
* Yleinen lista koodaajille: libreoffice@lists.freedesktop.org (paljon liikennettä)

Projekteihin liittyminen
----------------------------------------------------------------------

Voit antaa oman merkittävän panoksesi tähän tärkeään avoimen lähdekoodin projektiin, vaikka kokemuksesi ohjelmistosuunnittelusta ja ohjelmoinnista olisikin vähäistä.

Toivomme, että viihdyt uuden LibreOffice 7.4:n parissa ja liityt joukkoomme verkossa.

LibreOffice-yhteisö

----------------------------------------------------------------------
Käytetty tai muokattu lähdekoodi
----------------------------------------------------------------------

Osat Copyright 1998, 1999 James Clark. Osat Copyright 1996, 1998 Netscape Communications Corporation.
