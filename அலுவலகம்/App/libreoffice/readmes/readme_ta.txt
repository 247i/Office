
======================================================================
LibreOffice 7.4 என்னைப்படி
======================================================================


For the latest updates to this readme file, see https://git.libreoffice.org/core/tree/master/README.md

இக்கோப்பு LibreOffice மென்பொருளைப் பற்றிய முக்கியத் தகவலைக் கொண்டுள்ளது. நிறுவலைத் தொடங்குமுன் இத்தகவலைக் கவனமாக வாசிக்கப் பரிந்துரைக்கப்படுகிறீர்கள்.

The LibreOffice community is responsible for the development of this product, and invites you to consider participating as a community member. If you are a new user, you can visit the LibreOffice site, where you will find lots of information about the LibreOffice project and the communities that exist around it. Go to https://www.libreoffice.org/.

உண்மையில் LibreOffice அனைவருக்கும் இலவசமா?
----------------------------------------------------------------------

LibreOffice யாவருக்கும் இலவசமாக வழங்கப்படும் மென்பொருளாகும். நீங்கள் LibreOffice இன் இந்தப் படியை எத்தை கணினியில் வேண்டுமானாலும் நிறுவலாம்; (வனிக, அரசாங்க, கல்வி உட்பட) அனைத்து தேவைக்கும் பயன்படுத்தலாம். மேலதிக தகவலுக்கு LibreOffice பதிவிறக்கத்துடன் வந்த உரிம உரையைப் பார்க்கவும்.

ஏன் LibreOffice அனைவருக்கும் இலவசம்?
----------------------------------------------------------------------

இந்த LibreOffice ஐ இலவசமாக வழங்க தனிநபர்களும் நிறுவனங்களும் இதனை வடிவமைத்து, மேம்படுத்தி, பரிசோதித்து, ஆவணப்படுத்தி, ஆதரவளித்து, சந்தைப்படுத்தி, இன்னும் பல வழிகளில் உதவியுள்ளனர். இன்று LibreOffice இல்லங்களுக்கும் அலுவலகங்களுக்குமான உலகின் தலைசிறந்த திறவூற்று உற்பத்தித்திறன் மென்பொருளாக விளங்குகிறது.

If you appreciate their efforts, and would like to ensure that LibreOffice continues to be available far into the future, please consider contributing to the project - see https://www.documentfoundation.org/contribution/ for details. Everyone can make a contribution of some kind.

----------------------------------------------------------------------
நிறுவுதல் குறிப்புகள்
----------------------------------------------------------------------

LibreOffice இன் முழு செயலம்சத்தையும் பெற சமீபத்திய Java இயங்குநேரச் சூழல் (JRE) பதிப்பு அவசியம். JRE LibreOffice நிறுவல் தொகுப்பின் பகுதியல்ல, அதை தனியாக நிறுவ வேண்டும்.

கட்டகத் தேவைகள்
----------------------------------------------------------------------

* Microsoft Windows 7 SP1, 8, 8.1 Update (S14) or 10

குறிப்பு: நிறுவல் செய்முறைக்கு நிர்வாகி உரிமைகள் தேவை என்பதைக் கவனத்தில் கொள்க.

மைக்ரோசாப்ட் ஓபிஸ் வடிவூட்டங்களுக்கு LibreOffice ஐ முன்னிருப்பு மென்பொருளாக பதிவுசெய்ய பின்வரும் நிறுவியுடனான கட்டளை வரி விசைகளைப் பயன்படுத்தி கட்டாயப்படுத்தலாம் அல்லது தடுக்கலாம்:

* REGISTER_ALL_MSO_TYPES=1 LibreOffice ஐ மைக்ரோசாப்ட் ஓபிஸ் வடிவூட்டங்களுக்கான முன்னிருப்பு பயன்பாடாகப் பதிவு செய்யக் கட்டாயப்படுத்தும்.
* REGISTER_NO_MSO_TYPES=1 LibreOffice ஐ மைக்ரோசாப்ட் ஓபிஸ் வடிவூட்டங்களுக்கான முன்னிருப்பு பயன்பாடாகப் பதிவு செய்வதைத் தடுக்கும்.

உங்கள் கணினியின் தற்காலிக அடைவில் போதுமான நினைவகம் இருப்பதையும், படிக்க, எழுத மற்றும் அணுகும் உரிமை உங்களுக்கு வழங்கப்பட்டுள்ளதையும் உறுதிசெய்து கொள்ளுங்கள். நிறுவலைத் தொடங்கும் முன், மற்ற நிரல்கள் அனைத்தையும் மூடி விடவும்.

டெபியன்/உபுண்டு அடிப்படையிலான லினக்ஸ் கணினியில் LibreOffice ஐ நிறுவுதல்
----------------------------------------------------------------------

ஒரு மொழிப் பொதியை எவ்வாறு நிறுவுவது என்ற அறிவுறுத்தல்களுக்கு (LibreOffice இன் அமெரிக்க ஆங்கிலப் பதிப்பை நிறுவியப்பின்), ஒரு மொழிப் பொதி நிறுவுதல் என்ற தலைப்புடைய பிரிவை கீழே வாசிக்கவும்.

பதிவிறக்கம் செய்த காப்பகக் கோப்பை நீங்கள் பிரிக்கும் போது, அதன் உள்ளடக்கம் ஒரு துணை கோப்பகத்தில் பிரித்து வைக்கப்படுவதைக் காண்பீர்கள். ஒரு கோப்பு நிர்வாகி சாளரத்தைத் திறந்து, கோப்பகத்தின் பெயரை "LibreOffice_" எனத் தொடங்கி, பதிப்பு எண்ணும் இயங்குதள தகவலும் கொண்டதாக முடியும்படி மாற்றுங்கள்.

இந்த அடைவு "DEBS" என்ற ஒரு துணையடைவைக் கொண்டுள்ளது. அடைவை "DEBS" அடைவுக்கு மாற்றுக.

அடைவினுள் சொடுக்கி "முனையத்தில் திற" தேர்வு செய்யவும். ஒரு முனைய சாளரம் திறக்கும். முனையத்தில் கட்டளை வரியில் இருந்து, பின்வரும் கட்டளையை (கட்டளையை செயல்படுத்தும் முன்னர், நீங்கள் உங்கள் மூல பயனர் கடவுச்சொல்லை உள்ளிட வேண்டும்) உள்ளிடவும்:

பின்வரும் கட்டளைகள் லிப்ரெஓபிஸ், பணிமேடை ஒருங்கிணைப்பு பொதிகளை நிறுவும் (இவற்றைத் தட்டச்சு செய்ய முயல்வதை விட அப்படியே நகலெடுத்து உங்கள் முனையத் திரையில் ஒட்டுவது நல்லது):

sudo dpkg -i *.deb

நிறுவல் இப்போது முடிந்துவிட்டது, ஆகவே, அனைத்து LibreOffice செயலிகளின் படவுருக்களும் உங்கள் பணிமேடையின் செயலிகள்/அலுவலகம் பட்டியலில் இருக்க வேண்டும்.

Fedora, openSUSE, Mandriva மற்றும் பிற Linux முறைமைகளில் RPM தொகுப்புகளைப் பயன்படுத்தி LibreOffice ஐ நிறுவுதல்
----------------------------------------------------------------------

ஒரு மொழிப் பொதியை எவ்வாறு நிறுவுவது என்ற அறிவுறுத்தல்களுக்கு (LibreOffice இன் அமெரிக்க ஆங்கிலப் பதிப்பை நிறுவியப்பின்), ஒரு மொழிப் பொதி நிறுவுதல் என்ற தலைப்புடைய பிரிவை கீழே வாசிக்கவும்.

பதிவிறக்கம் செய்த காப்பகக் கோப்பை நீங்கள் பிரிக்கும் போது, அதன் உள்ளடக்கம் ஒரு துணை கோப்பகத்தில் பிரித்து வைக்கப்படுவதைக் காண்பீர்கள். ஒரு கோப்பு நிர்வாகி சாளரத்தைத் திறந்து, கோப்பகத்தின் பெயரை "LibreOffice_" எனத் தொடங்கி, பதிப்பு எண்ணும் இயங்குதள தகவலும் கொண்டதாக முடியும்படி மாற்றுங்கள்.

இந்த அடைவு "RPMS" என்றொரு துணை அடைவைக் கொண்டுள்ளது. அடைவை "RPMS" அடைவாக மாற்றுக.

அடைவினுள் சொடுக்கி "முனையத்தில் திற" தேர்வு செய்யவும். ஒரு முனைய சாளரம் திறக்கும். முனையத்தில் கட்டளை வரியில் இருந்து, பின்வரும் கட்டளையை (கட்டளையை செயல்படுத்தும் முன்னர், நீங்கள் உங்கள் மூல பயனர் கடவுச்சொல்லை உள்ளிட வேண்டும்) உள்ளிடவும்:

For Fedora-based systems: sudo dnf install *.rpm

மாண்ரிவா அடிப்படையிலான கட்டகங்களுக்கு: sudo urpmi *.rpm

மற்ற RPM-அடிப்படையிலான முறைமைகளுக்கு (openSUSE போன்றவை): rpm -Uvh *.rpm

நிறுவல் இப்போது முடிந்துவிட்டது, ஆகவே, அனைத்து LibreOffice செயலிகளின் படவுருக்களும் உங்கள் பணிமேடையின் செயலிகள்/அலுவலகம் பட்டியலில் இருக்க வேண்டும்.

ஒரு பயனராக நிறுவ, இக்காப்பகத்தின் மேல் மட்டக் கோப்பகத்திலுள்ள 'நிறுவு' வரிவடிவத்தைக்கூட நீங்கள் பயன்படுத்தலாம். இந்த வரிவடிவம் அதன் தனிப்பட்ட விவரக்குறிப்பு இந்நிறுவலுக்கு இருப்பதற்காக LibreOffice ஐ அமைக்கும்; உங்கள் இயல்பான LibreOffice விவரக்குறிப்பிலிருந்து இது வேறுபட்டிருக்கும். பணிமேடை பட்டி உருப்படிகள், பணிமேடை MIME வகை பதிவுகள் போன்ற கட்டகத் தொகையீட்டின் பகுதிகளை இது நிறுவாது என்று கருத்தில் கொள்ளுங்கள்.

லினக்ஸ் விநியோகங்களுக்கான பணிபேடை ஒருமைப்பாடு பற்றிய குறிப்புகள் மேலுள்ள நிறுவல் வழிமுறையில் இடம்பெறவில்லை
----------------------------------------------------------------------

இந்த நிறுவல் வழிமுறைகளில் குறிப்பாக இடம்பெறாத இதர லினக்ஸ் விநியோகங்களில் LibreOffice ஐ நிறுவ எளிமையாக இருக்க வேண்டும். முக்கியமாக பணிமேடை ஒருமைப்பாட்டில்தான் வேறுபாடுகளைச் சந்திக்க முடியும்.

The RPMS (or DEBS, respectively) directory also contains a package named libreoffice7.4-freedesktop-menus-7.4.0.1-1.noarch.rpm (or libreoffice7.4-debian-menus_7.4.0.1-1_all.deb, respectively, or similar). This is a package for all Linux distributions that support the Freedesktop.org specifications/recommendations (https://en.wikipedia.org/wiki/Freedesktop.org), and is provided for installation on other Linux distributions not covered in the aforementioned instructions.

மொழிப் பொதி நிறுவப்படுகிறது
----------------------------------------------------------------------

உங்களுக்குப் பிடித்த மொழி, இயங்குதளம் இவற்றிற்கான மொழிப் பொதியைப் பதிவிறக்குங்கள். அவை முதன்மை நிறுவல் அவணகமுள்ள அதே இடத்திலிருந்து கிடைக்கின்றன. நௌடிலஸ் கோப்பு நிர்வாகியிலிருந்து பதிவிறக்கப்பட்ட ஆவணகத்தை ஓர் அடைவிற்கு (எ.கா. உங்கள் பணிமேடை) பிரித்தெடுங்கள். அனைத்து LibreOffice செயலிகளிலிருந்தும் (விரைவுத்தொடங்கி உட்பட) நீங்கள் வெளியேறிவிட்டதை உறுதிசெய்து கொள்ளவும்.

பதிவிறக்கிய மொழிப் பொதியை நீங்கள் பிரித்தெடுத்த‌ அடைவுக்கு அடைவை மாற்றவும்.

இப்போது பிரித்தெடுக்கும் போது உருவாக்கப்பட்ட கோப்பகத்திற்கு மாறவும். எடுத்துக்காட்டாக, ஒரு 32-பிட் Debian/Ubuntu-அடிப்படையிலான கணினிக்கான பிரெஞ்சு மொழித் தொகுப்புக்கு கோப்பகத்தின் பெயர் LibreOffice_, அத்துடன் பதிப்பு தகவல் மற்றும் Linux_x86_langpack-deb_fr போன்ற உரையைக் கொண்டிருக்கும்.

இப்போது நிறுவ வேண்டிய தொகுப்புகளைக் கொண்டுள்ள கோப்பகத்திற்கு மாறவும். Debian/Ubuntu-அடிப்படையிலான கணினிகளில் கோப்பகம் DEBS என்பதாகும். Fedora, openSUSE அல்லது Mandriva முறைமைகளில், கோப்பகம் RPMS ஆகும்.

நாட்டிலஸ் கோப்பு மேலாளரில், அடைவை வலம்-சொடுக்கி "முனையத்தில் திற" என்ற கட்டளையைத் தேர்ந்தெடுக்கவும். நீங்கள் சற்று முன்னர் திறந்த‌ முனையத்தில், மொழி பொதியை நிறுவும் கட்டளையை செயல்படுத்தவும் (கீழ்கண்ட‌ கட்டளைகள் அனைத்துக்கும், நீங்கள் மூல பயனர் கடவுச்சொல்லை உள்ளிட வேண்டி இருக்கலாம்):

டெபியன்/ உபுண்டு அடிப்படையிலான கட்டகங்களுக்கு: sudo dpkg -i *.deb

For Fedora-based systems: su -c 'dnf install *.rpm'

மாண்ரிவா அடிப்படையிலான கட்டகங்களுக்கு: sudo urpmi *.rpm

மற்ற RPM-பயன்படுத்தும் முறைமைகளுக்கு (openSUSE போன்றவை): rpm -Uvh *.rpm

இப்போது ஏதாவதொரு LibreOffice செயலியை -- எ.கா. ரைட்டர் -- தொடக்குங்கள். கருவிகள் பட்டிக்குச் சென்று விருப்பத்தேர்வை தேர்க. விருப்பத்தேர்வு உரையாடல் பெட்டியில், "மொழி அமைவுகள்" ஐச் சொடுக்கிய பின் "மொழிகள்" ஐச் சொடுக்குக. "பயனர் முகப்பு" பட்டியலைக் கீழிறக்கி, நீங்கள் சற்று முன்னர் நிறுவிய மொழியைத் தேர்க. நீங்கள் வேண்டினால், அதே செயலை "இட அமைவு", "முன்னிருப்பு நாணயம்", "ஆவண முன்னிருப்பு மொழிகள்" ஆகியவற்றிற்கும் செய்க.

அந்த அமைவுகளைச் சரிசெய்த பின், சரி ஐச் சொடுக்குக. உரையாடல் பெட்டி மூடும்; உங்கள் மாற்றங்கள் LibreOffice இலிருந்து (விரைவுத்தொடக்கி ஓடிக்கொண்டிருந்தால், அதிலிருந்தும்) வெளியேறி அதனை மீளத்தொடக்கிய பின்னர்தான் செயலாகும் என்ற ஒரு தகவலை நீங்கள் காண்பீர்கள்.

அடுத்த முறை நீங்கள் LibreOffice ஐத் தொடங்கும்போது, அது நீங்கள் சற்று முன்னர் நிறுவிய மொழியில் தொடங்கும்.

----------------------------------------------------------------------
நிரல் அமைவின் போது சிக்கல்
----------------------------------------------------------------------

Difficulties starting LibreOffice (e.g. applications hang) as well as problems with the screen display are often caused by the graphics card driver. If these problems occur, please update your graphics card driver or try using the graphics driver delivered with your operating system.

----------------------------------------------------------------------
விண்டோசிலுள்ள ALPS/Synaptics மடிகணினி தொடுதளங்கள்
----------------------------------------------------------------------

ஒரு விண்டோஸ் இயக்கியிலுள்ள சிக்கலால், உங்கள் விரலை ALPS/Synaptics தொடுதளத்தில் நகர்த்தி LibreOffice ஆவணங்களூடே உங்களால் உருண்டு செல்ல முடியாது.

தொடுதள உருளலை இயக்க, பின்வரும் வரிகளை "C:\Program Files\Synaptics\SynTP\SynTPEnh.ini" அமைவடிவாக்க கோப்பில் சேர்த்தபின் உங்கள் கணினியை மிளத்தொடங்குக:

[LibreOffice]

FC = "SALFRAME"

SF = 0x10000000

SF |= 0x00004000

குறிப்பு: அமைவடிவாக்க கோப்பின் இடம் விண்டோஸின் பதிப்பிற்கு ஏற்றபடி மாறலாம்.

----------------------------------------------------------------------
குறுக்கு விசைகள்
----------------------------------------------------------------------

இயங்குதளம் பயன்படுத்தாத குறுவிசைகளை (விசைச் சேர்க்கைகளை) மட்டுமே LibreOffice இல் பயன்படுத்த முடியும். LibreOffice  இல் ஏதேனும் விசைச் சேர்க்கைகள் LibreOffice உதவிக் கோப்பில் கூறியபடி வேலை செய்யவில்லை என்றால், முதலில் அதே விசைச்சேர்க்கைகள் இயங்குதளத்தில் பயனில் உள்ளதா என்பதைச் சோதிக்கவும். இத்தகைய முரண்களைச் சரிசெய்ய, உங்கள் இயங்குதளத்தின் விசைச் சேர்க்கைகளை நீங்கள் மாற்றலாம். அல்லது, LibreOffice இலுள்ள எந்த விசைச்சேர்க்கைகளையும் நீங்களே மாற்றலாம். இதைப்பற்றிய மேலதிக விபரங்களுக்கு, LibreOffice இன் உதவிக்கோப்பையோ உங்கள் இயங்குதளத்தின் உதவிக்கோப்பையோ வாசிக்கவும்.

----------------------------------------------------------------------
Problems When Sending Documents as Emails From LibreOffice
----------------------------------------------------------------------

When sending a document via 'File - Send - Document as Email' or 'Document as PDF Attachment' problems might occur (program crashes or hangs). This is due to the Windows system file "Mapi" (Messaging Application Programming Interface) which causes problems in some file versions. Unfortunately, the problem cannot be narrowed down to a certain version number. For more information visit https://www.microsoft.com to search the Microsoft Knowledge Base for "mapi dll".

----------------------------------------------------------------------
முக்கிய அனுகல் குறிப்புகள்
----------------------------------------------------------------------

For more information on the accessibility features in LibreOffice, see https://www.libreoffice.org/accessibility/

----------------------------------------------------------------------
பயனர் உதவி
----------------------------------------------------------------------

The main support page offers various possibilities for help with LibreOffice. Your question may have already been answered - check the Community Forum at https://www.documentfoundation.org/nabble/ or search the archives of the 'users@libreoffice.org' mailing list at https://www.libreoffice.org/lists/users/. Alternatively, you can send in your questions to users@libreoffice.org. If you like to subscribe to the list (to get email responses), send an empty mail to: users+subscribe@libreoffice.org.

Also check the FAQ section at the LibreOffice website.

----------------------------------------------------------------------
வழுக்கள் & சிக்கல்களின் அறிக்கையிடல்
----------------------------------------------------------------------

Our system for reporting, tracking and solving bugs is currently Bugzilla, hosted at https://bugs.documentfoundation.org/. We encourage all users to feel entitled and welcome to report bugs that may arise on your particular platform. Energetic reporting of bugs is one of the most important contributions that the user community can make to the ongoing development and improvement of LibreOffice.

----------------------------------------------------------------------
ஈடுபடுதல்
----------------------------------------------------------------------

LibreOffice சமூகம், நீங்கள் இந்த முக்கியமான திறவூற்று செயல்திட்டத்தில் ஆர்வமாக பங்கொவதன்வழி அதிகம் பயன்பெரும்.

As a user, you are already a valuable part of the suite's development process and we would like to encourage you to take an even more active role with a view to being a long-term contributor to the community. Please join and check out the contributing page at the LibreOffice website.

தொடங்குவது எப்படி
----------------------------------------------------------------------

The best way to start contributing is to subscribe to one or more of the mailing lists, lurk for a while, and gradually use the mail archives to familiarize yourself with many of the topics covered since the LibreOffice source code was released back in October 2000. When you're comfortable, all you need to do is send an email self-introduction and jump right in. If you are familiar with Open Source Projects, check out our To-Dos list and see if there is anything you would like to help with at the LibreOffice website.

குழுவிலிணை
----------------------------------------------------------------------

Here are a few of the mailing lists to which you can subscribe at https://www.libreoffice.org/get-help/mailing-lists/

* செய்திகள்: announce@documentfoundation.org *அனைத்து பயனர்களுக்கும் பரிந்துரைக்கப்படுகிறது* (குறைவான போக்குவரத்து)
* பிரதான பயனர் பட்டியல்: users@global.libreoffice.org *விவாதங்களில் நுழைய எளிய வழி* (அதிக போக்குவரத்துத் தடை)
* சந்தைப்படுத்தல் திட்டப்பணி: marketing@global.libreoffice.org *உருவாக்கத்திற்கும் அப்பால்* (பளுவாகிறது)
* பொது மேம்பாட்டாளர் பட்டியல்: libreoffice@lists.freedesktop.org (அதிக போக்குவரத்து)

ஒன்றுக்கு அல்லது அதற்கு மேற்பட்ட திட்டங்களில் இணைய
----------------------------------------------------------------------

குறைந்த மென்பொருள் வடிவாக்க, குறியாக்க அனுபவமே உங்களுக்கு இருந்தாலும், இந்த முக்கிய திறவூற்று செயல்திட்டதிற்கு மிகப்பெரிய பங்கை நீங்கள் அளிக்கலாம். ஆம், நீங்கள்தான்!

புதிய LibreOffice 7.4 உங்களுக்குப் பயனானதாக அமைந்திருக்குமெனவும் இணையத்தில் எங்கள் சமூகத்தில் இணைவீர்களெனவும் எதிர்பார்க்கிறோம்.

லிப்ரெஓபிஸ் சமூகம்

----------------------------------------------------------------------
பயன்படுத்திய / மாற்றியமைத்த மூலக் குறியீடு
----------------------------------------------------------------------

Portions Copyright 1998, 1999 James Clark. Portions Copyright 1996, 1998 Netscape Communications Corporation.
