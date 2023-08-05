
======================================================================
LibreOffice 7.4 ReadMe
======================================================================


এই রীডমি নথিতে সাম্প্রতিকতম সংযোজনের জন্যে দেখুন https://git.libreoffice.org/core/tree/master/README.md

এ ফাইলে LibreOffice সফ্টওয়্যার সম্পর্কে গুরুত্বপূর্ণ তথ্য রয়েছে। ইনস্টলেশন শুরু করার পূর্বে এ তথ্য মনযোগ দিয়ে পড়ে নেয়ার জন্য আপনাকে সুপারিশ করা হচ্ছে।

LibreOffice পণ্যটি উন্নতির জন্য সম্প্রদায় দায়গ্রস্ত এবং আপনাকে এই সম্প্রদায়ে অংশগ্রহণ বিবেচনা করতে আবেদন জানায়। আপনি যদি নতুন ব্যবহারকারী হন, তাহলে আপনি LibreOffice  সাইট-এ যেতে পারেন, যেখানে আপনি LibreOffice প্রকল্প সম্পর্কে অনেক তথ্য এবং এর সংক্রান্ত সম্প্রদায়গুলির সম্পর্কে জানতে পারবেন। যান -  https://www.libreoffice.org/.

LibreOffice কি আসলেই যেকোন ব্যবহারকারীর জন্য মুক্ত?
----------------------------------------------------------------------

LibreOffice সবার বিনামূল্যে ব্যবহারের জন্য। আপনি LibreOffice এর একটি অনুলিপি নিয়ে যতসংখ্যাক খুশি ততসংখ্যক কম্পিউটারে ইনস্টল করতে পারেন এবং আপনার পছন্দনানুসারে যেকোনো ক্ষেত্রে (বাণিজ্যিক, সরকারী, লোকপ্রশাসন বা শিক্ষাক্ষেত্রে)ব্যবহার করতে পারেন। আরও বিস্তারিত তথ্যের জন্য LibreOffice ডাউনলোডের সাথে দেয়া লাইসেন্স টেক্সট প্যাকেজ দেখুন।

কেন LibreOffice যেকোন ব্যবহারকারীর জন্য মুক্ত?
----------------------------------------------------------------------

LibreOffice এর অনুলিপি আপনার বিনামূল্যে ব্যবহারের জন্য কারণ প্রত্যেক অবদানকারী এবং কর্পোরেট স্পনসর যারা নকশা,উন্নয়ন, পরীক্ষা, অনুবাদ, নথিবদ্ধকরণ, সমর্থন, প্রচার এরকম আরও অনেক কিছু করেছে জন্যই LibreOffice আজকের এই অবস্থায় এসেছে - ঘর এবং অফিসের জন্য বিশ্বের নেতৃত্বদানকারী ওপেন সোর্স সফ্টওয়্য়ার প্রোডাক্টিভিটি।

আপনি যদি এই প্রকল্পের সমাদর করেন এবং নিশ্চিত করতে চান যে LibreOffice সুদূর ভবিষ্যতেও উপলব্ধ থাকুক, অনুগ্রহ করে এই প্রকল্পে অবদান করুন - দেখুন https://www.documentfoundation.org/contribution/ বিশদভাবে জানতে, সবাই কোনো না কোনো ভাবে অবদান রাখতে পারেন।

----------------------------------------------------------------------
ইনস্টলেশনের ব্যাপারে নোট
----------------------------------------------------------------------

$ {PRODUCTNAME} এর একটি জাভা রানটাইম এনভায়রনমেন্টের (JRE) সাম্প্রতিক সংস্করণ প্রয়োজন সম্পূর্ণ কার্যকারিতা জন্য। JRE $ {PRODUCTNAME} ইনস্টলেশন প্যাকেজের অংশ নয়, সেটি আলাদাভাবে ইনস্টল করা উচিত।

সিস্টেমের আবশ্যকীয় বৈশিষ্ট্য
----------------------------------------------------------------------

* মাইক্রোসফট উইন্ডোস ৭ এস পি ১, ৮, ৮.১ আপডেট(এস১৪) বা ১০

অনুগ্রহ করে খেয়াল করুন ইনস্টলেশন প্রক্রিয়ার জন্য অ্যাডমিনিস্ট্রেটর অধিকার প্রয়োজন।

ইনস্টলারের নিম্নবর্ণিত কমান্ড লাইন সুইচগুলো ব্যবহার করে Microsoft Office ফরম্যাটের জন্য ডিফল্ট অ্যাপ্লিকেশন হিসেবে LibreOffice কে রেজিস্ট্রেশন করানো যায় বা বাদ দেয়া যায়।

* REGISTER_ALL_MSO_TYPES=1 মাইক্রোসফট অফিস ফরম্যাটের জন্য ডিফল্ট অ্যাপ্লিকেশন হিসাবে LibreOffice এর নিবন্ধন বাধ্যতামূলককরবে.
* REGISTER_NO_MSO_TYPES=1 মাইক্রোসফট অফিস ফরম্যাটের জন্য ডিফল্ট অ্যাপ্লিকেশন হিসাবে LibreOffice এর নিবন্ধীকরণ দমন করবে.

আপনার অস্থায়ী ডিরেক্টরি সিস্টেমে যথেষ্ট পরিমান মেমরি খালি আছে কিনা অনুগ্রহ করে তা নিশ্চিত করুন,এবং পড়া, লিখা ও চালানোর জন্য প্রবেশের অধিকার গ্রহণযোগ্য হবে তা নিশ্চিত করুন।  ইন্সটলেশন প্রক্রিয়া শুরু হওয়ার পূর্বেই বাকী সব প্রোগ্রাম বন্ধ করুন।

ডেবিয়ান/উবুন্টু ভিত্তিক লিনাক্স সিস্টেমের জন্য LibreOffice ইনস্টল প্রক্রিয়া
----------------------------------------------------------------------

একটি ভাষা প্যাক কীভাবে ইনস্টল করতে পারবেন তা জানতে (LibreOffice-এর US ইংরাজি সংস্করণ ইনস্টল করার পরে), একটি ভাষা প্যাক ইনস্টল করা বিষয়ক বিভাগটি অনুগ্রহ করে পড়ুন।

অাপনি যখন ডাউনলোড করা সংরক্ষণাগারের প্যাক খোলেন তখন, অাপনি দেখতে পাবেন যে তার বিষয়বস্তু একটি উপ-ডিরেক্টরিতে ডিকম্প্রেস হয়েছে। একটি ফাইল পরিচালক উইন্ডো খুলুন, এবং ডিরেক্টরি সেখানে পরিবর্তন করুন যা শুরু হচ্ছে "LibreOffice_", এবং থাকছে সংস্করণ নম্বর এবং প্ল্যাটফর্ম বিষয়ক কিছু তথ্য।

এই ডিরেক্টরিতে সাবডিরেক্টরি আছে যা "DEBS" নামে পরিচিত। ডিরেক্টরি "DEBS" এ পরিবর্তন করুন।

ডিরেক্টরির মধ্যে মাউসের ডান দিকের বাটহ সহযোগে ক্লিক করে  "টার্মিন্যালের মধ্যে খুলুন" বিকল্পটি নির্বাচন করুন। একটি টার্মিন্যাল উইন্ডো প্রদর্শন করা হলে। টার্মিন্যাল উইন্ডোর কমান্ড-লাইনে নিম্নলিখিত কমান্ডটি লিখুন (কমান্ড সঞ্চালনার পূর্বে, সিস্টেমের root ব্যবহারকারীর পাসওয়ার্ড লেখার অনুরোধ জানানো হবে):

নিম্নলিখিত কম্যান্ড LibreOffice এবং ডেস্কটপ একত্রিকরণ প্যাকেজ ইনস্টল করবে (অাপনি এখানে তাদের অনুলিপি করার থেকে টার্মিন্যালের স্ক্রিনে অনুলিপি করে লেপন করতে পারেন):

sudo dpkg -i *.deb

ইনস্টলেশন এখন সমাপ্ত এবং সকল LibreOfficeঅ্যাপ্লিকেশনের আইকনগুলি এখন অ্যাপ্লিকেশন-তালিকা/অফিস শীর্ষক মেনুর মধ্যে উপলব্ধ থাকবে।

RPM প্যাকেজ ব্যবহার করে Fedora, openSUSE, Mandriva এবং অন্যান্য Linux সিস্টেমে LibreOffice ইনস্টল করা।
----------------------------------------------------------------------

কোনো ভাষা প্যাক কীভাবে ইনস্টল করবেন তা জানতে (LibreOffice-এর US ইংরাজি সংস্করণ ইনস্টল করার পরে), অনুগ্রহ করে একটি ভাষা প্যাক ইনস্টল করুন লেখা বিভাগটি পড়ুন।

অাপনি ডাউনলোড করা সংরক্ষণাগার প্যাক থেকে খুললে, অাপনি লক্ষ্য করবেন যে বিষয়বস্তু একটি উপ-ডিরেক্টরিতে ডিকম্প্রেস হয়েছে। একটি ফাইল ম্যানেজার উইন্ডো খুলুন, এবং এমন একটি ডিরেক্টরিতে পরিবর্তন করুন যা শুরু হচ্ছে "LibreOffice_" দিয়ে, অার রয়েছে সংস্করণ সংখ্যা এবং প্ল্যাটফর্ম বিষয়ক কিছু তথ্য।

এই ডিরেক্টরিতে সাবডিরেক্টরি আছে যা "RPMS" নামে পরিচিত। ডিরেক্টরি "RPMS" এ পরিবর্তন করুন।

ডিরেক্টরির মধ্যে মাউসের ডান দিকের বাটহ সহযোগে ক্লিক করে  "টার্মিন্যালের মধ্যে খুলুন" বিকল্পটি নির্বাচন করুন। একটি টার্মিন্যাল উইন্ডো প্রদর্শন করা হলে। টার্মিন্যাল উইন্ডোর কমান্ড-লাইনে নিম্নলিখিত কমান্ডটি লিখুন (কমান্ড সঞ্চালনার পূর্বে, সিস্টেমের root ব্যবহারকারীর পাসওয়ার্ড লেখার অনুরোধ জানানো হবে):

For Fedora-based systems: sudo dnf install *.rpm

ম্যানড্রিভা ভিত্তিক সিস্টেমের জন্য: sudo urpmi *.rpm

অন্যান্য RPM-ভিত্তিক সিস্টেমের জন্য (openSUSE, ইত্যাদি): rpm -Uvh *.rpm

ইনস্টলেশন এখন সমাপ্ত এবং সকল LibreOfficeঅ্যাপ্লিকেশনের আইকনগুলি এখন অ্যাপ্লিকেশন-তালিকা/অফিস শীর্ষক মেনুর মধ্যে উপলব্ধ থাকবে।

বিকল্প ভাবে, একজন ব্যবহারকারী হিসাবে একটি ইনস্টলেশান করতে, অাপনি সবথেকে উপরের স্তরের ডিরেক্টরিতে অবস্থিত 'ইনস্টল' স্ক্রিপ্ট ব্যবহার করতে পারেন। স্ক্রিপ্ট LibreOffice সেট অাপ করবে যাতে এই ইনস্টলেশানের জন্য তার নিজস্ব প্রোফাইল থাকে, যা অাপনার সাধারণ LibreOffice প্রোফাইলের থেকে অালাদা হবে। মনে রাখবেন যে, এটি সিস্টেম একত্রিকরণ অংশ ইনস্টল করবে না যেমন ডেস্কটপ মেনু অাইটেম এবং ডেস্কটপ MIME ধরন নিবন্ধন।

লিনাক্স ডিস্ট্রিবিউশনের জন্য ডেস্কটপ ইন্টিগ্রেশন উপরোক্ত ইনস্টলেশন অনুসরণ করে না
----------------------------------------------------------------------

LibreOffice কে অন্যান্য লিনাক্স ডিস্ট্রিবিউশনে ইনস্টল করা সহজ হবে। ডেস্কটপ ইন্টিগ্রেশনে এসব পরিবর্তনগুলো প্রয়োগ হবে।

The RPMS (or DEBS, respectively) directory also contains a package named libreoffice7.4-freedesktop-menus-7.4.0.1-1.noarch.rpm (or libreoffice7.4-debian-menus_7.4.0.1-1_all.deb, respectively, or similar). This is a package for all Linux distributions that support the Freedesktop.org specifications/recommendations (https://en.wikipedia.org/wiki/Freedesktop.org), and is provided for installation on other Linux distributions not covered in the aforementioned instructions.

ভাষা প্যাক ইনস্টল করা হচ্ছে
----------------------------------------------------------------------

আপনার পছন্দনীয় ভাষা এবং প্লাটফরমের জন্য ভাষা প্যাকটি ডাউনলোড করুন। এটি মূল ইন্সটলেশন আর্কাইভের একই অবস্থানে বিদ্যমান। নটিলাস ফাইল ব্যবস্থাপক হতে, ডাউনলোডকৃত আর্কাইভকে ডিরেক্টরিতে (উদাহরণস্বরূপ-আপনার ডেস্কটপ) সম্প্রসারণ করুন। আপনি সব LibreOffice এপ্লিকেশন (যদি QuickStarter শুরু হয়, তবে এটি অন্তর্ভুক্ত হবে ) হতে প্রস্থান নিশ্চিত করুন।

ডাউনলোডকৃত ডিরেক্টরিটি যেখানে আনপ্যাক করেছেন সে ডিরেক্টরিতে ডিরেক্টরি পরিবর্তন করুন।

এখন ডিরেক্টরি সেই ডিরেক্টরিতে পরিবর্তন করুন যা নিষ্কাশন প্রক্রিয়ার সময়ে তৈরি করা হয়েছে। উদাহরণস্বরূপ, একটি 32-বিট Debian/Ubuntu-ভিত্তিক সিস্টেমের ক্ষেত্রে ফরাসি ভাষা প্যাকের জন্য, ডিরেক্টরির নাম দেওয়া হয় LibreOffice_, উপরন্তু কিছু সংস্করণ তথ্য, উপরন্তু Linux_x86_langpack-deb_fr

এখন ডিরেক্টরি সেই ডিরেক্টরিতে পরিবর্তন করুন যেখানে ইনস্টল করার প্যাকেজগুলি রয়েছে। Debian/Ubuntu-ভিত্তিক সিস্টেমে, DEBS হবে ডিরেক্টরি। Fedora, openSUSE বা Mandriva সিস্টেমে, ডিরেক্টরি হবে RPMS

নটিলাস ফাইল ব্যবস্থাপক হতে, ডিরেক্টরিতে ডান-ক্লিক করুন এবং "টার্মিনালে খোলা" কমান্ডটি নির্বাচন করুন। এইমাত্র উন্মুক্তকৃত টার্মিনাল উইন্ডোতে, ভাষা প্যাকটি ইনস্টল করতে কমান্ডটি কার্যকর করুন(নিম্নে বর্ণিত সব কমান্ডসহ, আপনাকে মূল ব্যবহারকারী পাসওয়ার্ডটি প্রবেশ করাতে হতে পারে)।

ডেবিয়ান/উবুন্টু ভিত্তিক সিস্টেমের জন্য: sudo dpkg -i *.deb

For Fedora-based systems: su -c 'dnf install *.rpm'

ম্যানড্রিভা ভিত্তিক সিস্টেমের জন্য: sudo urpmi *.rpm

অন্যান্য RPM-ব্যবহার করা সিস্টেমের জন্য (openSUSE, ইত্যাদি): rpm -Uvh *.rpm

LibreOffice এপ্লিকেশনটি শুরু করা হলো- উদাহরণস্বরূপ- রাইটার। টুলস্ মেনুতে গিয়ে অপশন নির্বাচন করুন। অপশনের সংলাপ বাক্সে, "ভাষা সেটিং" এ ক্লিক করুন তারপর ভাষায় ক্লিক করুন। "ব্যবহারকারী ইন্টারফেস" তালিকাটি ড্রপডাউন করুন এবং আপনার ইনস্টলকৃত ভাষাটি নির্বাচন করুন। "স্থানীয় সেটিং", "পূর্বনির্ধারিত মূদ্রা" এবং "ডকুমেন্টের জন্য পূর্বনির্ধারিত ভাষা" এও একই কাজ করতে পারেন।

এই সেটিংগুলো সমন্বিত করার পর, ঠিক আছে তে ক্লিক করুন। সংলাপ বাক্সটি বন্ধ হয়ে যাবে এবং একটি তথ্য বার্তা দেখতে পাবেন তাতে লিখা থাকবে LibreOffice প্রস্থান করে আবার  শুরু করলে ( মনে রাখবেন, যদি QuickStarter শুরু থাকে তবে তাও প্রস্থান করতে হবে) পরিবর্তনগুলো সক্রিয় হবে।

পরবর্তীতে LibreOffice চালালে, এটি আপনার ইনস্টলকৃত ভাষায় চালু হবে।

----------------------------------------------------------------------
প্রোগ্রাম শুরুর সময় ত্রুটি
----------------------------------------------------------------------

Difficulties starting LibreOffice (e.g. applications hang) as well as problems with the screen display are often caused by the graphics card driver. If these problems occur, please update your graphics card driver or try using the graphics driver delivered with your operating system.

----------------------------------------------------------------------
Windows ALPS/Synaptics নোটবই টাচপ্যাড
----------------------------------------------------------------------

একটি Windows ড্রাইভার বিষয়ের কারনে, ALPS/Synaptics টাচপ্যাডে আঙুল চালানোর সময় আপনি LibreOffice নথির মধ্যে স্ক্রল করতে পারবেন না।

টাচপ্যাড স্ক্রলিং সক্রিয় করতে, কনফিগারেশন ফাইলে নিচের লাইনটি যুক্ত করুন "C:\Program Files\Synaptics\SynTP\SynTPEnh.ini" , এবং কম্পিউটার রিটার্ট করুন:

[LibreOffice]

FC = "SALFRAME"

SF = 0x10000000

SF |= 0x00004000

কনফিগারেশন ফাইলের অবস্থান উইন্ডোজের সংস্করণ ভেদে ভিন্ন হয়।

----------------------------------------------------------------------
শর্টকাট কী
----------------------------------------------------------------------

Only shortcut keys (key combinations) not used by the operating system can be used in LibreOffice. If a key combination in LibreOffice does not work as described in the LibreOffice Help, check if that shortcut is already used by the operating system. To rectify such conflicts, you can change the keys assigned by your operating system. Alternatively, you can change almost any key assignment in LibreOffice. For more information on this topic, refer to the LibreOffice Help or the Help documentation of your operating system.

----------------------------------------------------------------------
Problems When Sending Documents as Emails From LibreOffice
----------------------------------------------------------------------

When sending a document via 'File - Send - Document as Email' or 'Document as PDF Attachment' problems might occur (program crashes or hangs). This is due to the Windows system file "Mapi" (Messaging Application Programming Interface) which causes problems in some file versions. Unfortunately, the problem cannot be narrowed down to a certain version number. For more information visit https://www.microsoft.com to search the Microsoft Knowledge Base for "mapi dll".

----------------------------------------------------------------------
জরুরি অ্যাক্সেসিবিলিটি নোট
----------------------------------------------------------------------

For more information on the accessibility features in LibreOffice, see https://www.libreoffice.org/accessibility/

----------------------------------------------------------------------
ব্যবহারকারী সহায়তা
----------------------------------------------------------------------

The main support page offers various possibilities for help with LibreOffice. Your question may have already been answered - check the Community Forum at https://www.documentfoundation.org/nabble/ or search the archives of the 'users@libreoffice.org' mailing list at https://www.libreoffice.org/lists/users/. Alternatively, you can send in your questions to users@libreoffice.org. If you like to subscribe to the list (to get email responses), send an empty mail to: users+subscribe@libreoffice.org.

Also check the FAQ section at the LibreOffice website.

----------------------------------------------------------------------
বাগ এবং ইস্যু রিপোর্টিং
----------------------------------------------------------------------

Our system for reporting, tracking and solving bugs is currently Bugzilla, hosted at https://bugs.documentfoundation.org/. We encourage all users to feel entitled and welcome to report bugs that may arise on your particular platform. Energetic reporting of bugs is one of the most important contributions that the user community can make to the ongoing development and improvement of LibreOffice.

----------------------------------------------------------------------
সংযুক্ত হোন
----------------------------------------------------------------------

LibreOffice কমিউনিটি এই জরুরী ওপেন সোর্স প্রোজেক্ট উন্নয়নে আপনার কার্যকর অংশগ্রহনে অত্যন্ত উপকৃত হবে।

As a user, you are already a valuable part of the suite's development process and we would like to encourage you to take an even more active role with a view to being a long-term contributor to the community. Please join and check out the contributing page at the LibreOffice website.

কিভাবে শুরু করতে হবে
----------------------------------------------------------------------

The best way to start contributing is to subscribe to one or more of the mailing lists, lurk for a while, and gradually use the mail archives to familiarize yourself with many of the topics covered since the LibreOffice source code was released back in October 2000. When you're comfortable, all you need to do is send an email self-introduction and jump right in. If you are familiar with Open Source Projects, check out our To-Dos list and see if there is anything you would like to help with at the LibreOffice website.

সাবস্ক্রাইব
----------------------------------------------------------------------

Here are a few of the mailing lists to which you can subscribe at https://www.libreoffice.org/get-help/mailing-lists/

* খবর: announce@documentfoundation.org *recommended to all users* (light traffic)
* ব্যবহারকারীদের প্রধান তালিকা: users@global.libreoffice.org *আড়ালে থেকে বিভিন্ন আলোচনা সম্পর্ক অবগত থাকার সহজ উপায়* (উচ্চ পরিমাণের ট্রাফিক)
* মার্কেটিং প্রজেক্ট: marketing@global.libreoffice.org *ডিভেলপমেন্ট ভিন্ন অন্যান্য তথ্য* (ট্রাফিক পরিমাণ বৃদ্ধি হচ্ছে)
* সাধারণ ডেভেলপার তালিকা: libreoffice@তালিকাs.freedesktop.org (heavy traffic)

এক বা একাধিক প্রোজেক্টে অংশগ্রহন করুন
----------------------------------------------------------------------

যদি আপনার খুব কম সফটওয়্যার ডিজাইন বা কোডিং অভিজ্ঞতা থাকে তাহলেও আপনি এই জরুরী মুক্ত সোর্স প্রোজেক্টে বড় অবদান রাখতে পারেন। হ্যাঁ, আপনি!

আশা করি আপনি নতুন LibreOffice 7.4 এর সাথে কাজ করে আনন্দ পাচ্ছেন এবং অনলাইনে আমাদের সাথে যুক্ত হবেন।

লিবার অফিস কমিউনিটি

----------------------------------------------------------------------
ব্যবহৃত / পরিবর্তিত সোর্স কোড
----------------------------------------------------------------------

Portions Copyright 1998, 1999 James Clark. Portions Copyright 1996, 1998 Netscape Communications Corporation.
