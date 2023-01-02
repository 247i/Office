
======================================================================
LibreOffice 7.4 Beni Oku
======================================================================


Bu beni oku dosyasının güncel hali için https://git.libreoffice.org/core/tree/master/README.md adresine bakın.

Bu dosya LibreOffice yazılımı hakkında önemli bilgileri içermektedir. Kuruluma başlamadan önce bu bilgileri çok dikkatli şekilde okunanız önerilir.

LibreOffice topluluğu bu ürünün geliştirilmesinden sorumludur ve sizi bir topluluk üyesi olarak katkı vermeye davet eder. Eğer yeni bir kullanıcıysanız, LibreOffice projesi ve etrafındaki topluluklar hakkında birçok bilgi edinebileceğiniz LibreOffice sitesini ziyaret edebilirsiniz. https://www.libreoffice.org/ adresini ziyaret ediniz.

LibreOffice Gerçekten Her Kullanıcı İçin Ücretsiz mi?
----------------------------------------------------------------------

LibreOffice herkes tarafından özgürce kullanıma açıktır. LibreOffice'in bu kopyasını alıp dilediğiniz kadar bilgisayara kurabilirsiniz ve dilediğiniz amaçla (ticari, kamu, kamu yönetimi veya eğitim amaçlı) kullanabilirsiniz. Daha fazla bilgi için LibreOffice indirme paketi ile gelen lisans metnine göz atın.

LibreOffice Neden Her Kullanıcı İçin Ücretsiz?
----------------------------------------------------------------------

LibreOffice'in bu kopyasını ücret ödemeden kullabilirsiniz, çünkü bireysel katkıcılar ve ticari sponsorlar tasarladılar, geliştirdiler, test ettiler, yerelleştirdiler, belgelediler, desteklediler, pazarladılar ve LibreOffice'i bu günlere, dünyanın önde gelen Açık Kaynak Kodlu ofis yazılımı haline getirmek için pek çok şekilde yardımcı oldular.

Çalışmaları takdir ediyorsanız ve LibreOffice'in gelecekte de herkesin kullanımına açık olmasından emin olmak istiyorsanız, lütfen katkı vermeyi düşünün - Detaylar için https://www.documentfoundation.org/contribution/ adresini ziyaret ediniz. Herkes bir şekilde katkı verebilir.

----------------------------------------------------------------------
Kurulum Notları
----------------------------------------------------------------------

LibreOffice tam işlevselliği için güncel bir Java Çalıştırma Ortamına (JRE) ihtiyaç duyar. JRE, LibreOffice kurulumunun bir parçası değildir, ayrıca kurulmalıdır.

Sistem Gereksinimleri
----------------------------------------------------------------------

* Microsoft Windows 7 SP1, 8, 8.1 Güncelleme (S14) veya 10

Not: Lütfen kurulum için yönetici haklarınızın olduğundan emin olun.

Microsoft Office dosya biçimleri için LibreOffice'i varsayılan program olarak kayıt ettirmek istiyorsanız, kurulum programında aşağıdaki komutları kullanabilirsiniz:

* REGISTER_ALL_MSO_TYPES=1 bütün Microsoft Office dosya biçimleri için LibreOffice'i öntanımlı uygulama olarak kaydedecektir.
* REGISTER_NO_MSO_TYPES=1 bütün Microsoft Office dosya biçimleri için LibreOffice'in öntanımlı uygulama olmasını kaldıracaktır.

Lütfen sisteminizin geçici dizininde yeterli boş alan olduğundan ve bu alana okuma-yazma-çalıştırma hakkınızın olduğundan emin olunuz. Kurulumu başlatmadan önce, çalışan tüm programlarınızı kapatınız.

LibreOffice'in Debian/Ubuntu tabanlı Linux sistemler için kurulumu
----------------------------------------------------------------------

Bir dil paketini kurmak için (LibreOffice yazılımının ABD İngilizce sürümünü kurduktan sonra), lütfen aşağıdaki Bir Dil Paketini Kurmak başlıklı bölümü okuyunuz.

İndirme arşivini açtığınızda içeriğin bir alt dizin içerisinde açılmış olduğunu göreceksiniz. Dosya yöneticisini açın ve dizini "LibreOffice_" ile başlayan ve sürüm numarası ve platform bilgisi içeren dizin ile değiştirin.

Bu dizin "DEBS" adında bir alt dizini içermektedir. Dizini "DEBS" ile değiştirin.

Dizine sağ tıklayarak ve "Uçbirimde Aç"ı seçiniz. Bir uçbirim penceresi açılacaktır. Uçbirimin komut satırına şu komutu giriniz (komutun çalışması için sizden yetkili kullanıcı parolanızı girmeniz istenecektir):

Aşağıdaki komutlar LibreOffice'i ve masaüstü tümleştirme paketlerini kuracak (Bu komutları yazmak yerine kopyalayarak terminal ekranına yapıştırabilirsiniz):

sudo dpkg -i *.deb

Kurulum işlemi tamamlandı, ve Uygulamalar/Ofis menüsünde bütün LibreOffice uygulamalarının simgelerini görebileceksiniz.

LibreOffice Fedora, openSUSE, Mandriva ve diğer Linux sistemlerde RPM paketleri kullanılarak yüklenir
----------------------------------------------------------------------

Bir dil paketini kurmak için (LibreOffice yazılımının ABD İngilizce sürümünü kurduktan sonra), lütfen aşağıdaki Bir Dil Paketini Kurmak başlıklı bölümü okuyunuz.

İndirme arşivini açtığınızda içeriğin bir alt dizin içerisinde açılmış olduğunu göreceksiniz. Dosya yöneticisini açın ve dizini "LibreOffice_" ile başlayan ve sürüm numarası ve platform bilgisi içeren dizin ile değiştirin.

Bu dizin "RPMS" adında bir alt dizini içermektedir. Dizini "RPMS" ile değiştirin.

Dizine sağ tıklayarak ve "Uçbirimde Aç"ı seçiniz. Bir uçbirim penceresi açılacaktır. Uçbirimin komut satırına şu komutu giriniz (komutun çalışması için sizden yetkili kullanıcı parolanızı girmeniz istenecektir):

Fedora tabanlı sistemler için: sudo dnf install *.rpm

Mandriva tabanlı sistemler için: sudo urpmi *.rpm

Diğer RPM tabanlı sistemler (openSuse, vb): rpm -Uvh *.rpm

Kurulum işlemi tamamlandı, ve Uygulamalar/Ofis menüsünde bütün LibreOffice uygulamalarının simgelerini görebileceksiniz.

Alternatif olarak, bir kullanıcı olarak kurulum yapmak için bu arşiv dizininde bulunan 'install' betiğini kullanabilirsiniz. Betik, bu kurulum için kendi profilini normal profiliniz olan LibreOffice profilinden ayrı olarak LibreOffice olarak ayarlayacak. Dikkat edin masaüstü menü ögesi veya masaüstü MIME kayıtları gibi sistem bütünleşik parçaları olarak kurulmayacak.

Linux Dağıtımları için Masaüstü Entegrasyonunu ilgilendiren Notlar yukarıdaki Kurulum Talimatlarında yer almamaktadır
----------------------------------------------------------------------

LibreOffice yukarıdaki özelleştirilmiş talimatlarda belirtilmeyen diğer Linux dağıtımlarına da kolayca kurulabilir. Karşılaşılabilecek temel fark masaüstü entegrasyonu olabilir.

RPMS (veya DEBS) dizini libreoffice7.4-freedesktop-menus-7.4.0.1-1.noarch.rpm (veya libreoffice7.4-debian-menus_7.4.0.1-1_all.deb) isimli bir paketi de içermektedir. Bu paket bütün Linux dağıtımları için Freedesktop.org gerekliliklerini/tavsiyelerini desteklenmes içindir.(https://en.wikipedia.org/wiki/Freedesktop.org) ve yukarıdaki talimatlar dışındaki diğer Linux dağıtımlarına kurulumu sağlamaktadır.

Bir Dil Paketi Kurmak
----------------------------------------------------------------------

Tercih ettiğiniz dil ve platformun dil paketini indirin. Dil paketlerini temel yükleme paketlerinin bulunduğu yerde bulabilirsiniz. İndirdiğiniz paketi bir dosya yöneticisinin yardımı ile herhangi bir klasöre çıkartın (örneğin masaüstü). LibreOffice uygulamalarının kapalı olduğundan emin olun (QuickStarter dahil).

Paketi çıkarttığınız klasöre geçin.

Şimdi dizini çıkarma işlemi sürecinde yaratılan dizin ile değiştirin. Örneğin, 32-bit Debian/Ubuntu tabanlı sistemin Fransızca dili paketi için dizin adı, LibreOffice_, artı bazı sürüm bilgisi, artı Linux_x86_langpack-deb_fr olacaktır.

Şimdi dizini kurulacak paketleri içeren dizin ile değiştirin. Debian/Ubuntu tabanlı sistemlerde, dizin DEBS olacaktır. Fedora, openSuse veya Mandriva sistemlerinde ise dizin RPMS olacaktır.

Nautilus dosya yöneticisinde dizine sağ tıklayarak "Terminalde aç" düğmesine tıklayın. Açılan terminal penceresinde, dil paketini yüklemek için komut girin (aşağıdaki komutların tümü ile kullanıcı adı ve parola girmeniz istenebilir):

Debian/Ubuntu tabanlı sistemler için: sudo dpkg -i *.deb

Fedora tabanlı sistemler için: su -c 'dnf install *.rpm'

Mandriva tabanlı sistemler için: sudo urpmi *.rpm

RPM kullanan diğer sistemler için (openSuse v.b.): rpm -Uvh *.rpm

Şimdi LibreOffice uygulamalarından birini çalıştırın, örneğin Writer. Araçlar menüsüne giderek Seçenekler yolunu izleyin. Seçenekler penceresinde "Dil Ayarları"na tıklayınız ve "Diller" üzerine tıklayınız. "Kullanıcı arayüzü" listesini açınız ve az önce kurduğunuz dili seçiniz. Eğer isterseniz aynı şeyi "Yerel ayarlar", "Varsayılan para birimi" ve "Belgeler için varsayılan diller" için de yapabilirsiniz.

Bu ayarları yaptıktan sonra, Tamam'a tıklayınız. Pencere kapanacaktır ve değişikliklerin ancak LibreOffice 'den çıkıp yeniden başlattığınızda(eğer Hızlı Başlatıcı çalışmışsa ondan da çıkmayı unutmayınız) aktif olacağını bildiren bir uyarı alacaksınız.

LibreOffice 'i bir sonraki başlatışınızda kurduğunuz dil ile başlayacaktır.

----------------------------------------------------------------------
Program Başlatma Sırasında Problemler
----------------------------------------------------------------------

LibreOffice ürününü başlatma güçlükleri (ör. uygulamalar kilitleniyor) ve ekran görüntüsüyle ilgili sorunlar genellikle grafik kartı sürücüsünden kaynaklanır.  Bu sorunlar meydana gelirse, lütfen grafik kartı sürücünüzü güncelleyin veya işletim sisteminizle birlikte verilen grafik sürücüsünü kullanmayı deneyin.

----------------------------------------------------------------------
Windows altında ALPS/Synaptics dizüstü touchpad
----------------------------------------------------------------------

Windows'da bir sürücü sorunu yüzünden LibreOffice belgelerinde kaydırma özelliğini kullanamadığınızda, ALPS/Synaptics touchpad ile kaydırma özelliğini kullanabilirsiniz.

Touchpad kaydırmayı etkinleştirmek için "C:\Program Files\Synaptics\SynTP\SynTPEnh.ini" yapılandırma dosyasına takip eden satırı ekleyin ve bilgisayarınızı yeniden başlatın:

[LibreOffice]

FC = "SALFRAME"

SF = 0x10000000

SF |= 0x00004000

Not: Yapılandırma dosyasının yeri Windows'un farklı sürümlerinde değişebilir.

----------------------------------------------------------------------
Kısayol Tuşları
----------------------------------------------------------------------

LibreOffice kısayollarının (kısayol birleşimleri) bir kısmı bazı işletim sistemlerinde kullanılamayabilir. Eğer LibreOffice içinde bazı kısayol birleşimleri LibreOffice Yardım belgesinde anlatıldığı gibi çalışmıyorsa, işletim sisteminin kullanmakta olduğu kısayolları kontrol edip çakışma olup olmadığını kontrol ediniz. Eğer böyle bir durum var ise çakışan kısayol atamalarını değiştirebilirsiniz. Bir alternatif olarak LibreOffice tuş atamasını da değiştirebilirsiniz. Bu konu hakkında daha fazla bilgi almak için LibreOffice Yardım belgelerine ya da işletim sisteminizin yardım belgelerine göz atınız.

----------------------------------------------------------------------
LibreOffice'den E-posta eki olarak gönderilen belgelerin gönderimi sırasında sorunlar oluştu
----------------------------------------------------------------------

Bir belgeyi 'Dosya - Gönder - Belgeyi E-posta Eki Olarak' veya 'Belgeyi PDF Eki Olarak' yoluyla gönderirken sorunlar ortaya çıkabilir (program çöküyor veya takılıyor). Bunun nedeni, bazı dosya sürümlerinde sorunlara neden olan Windows sistem dosyası "Mapi" (Mesajlaşma Uygulama Programlama Arayüzü) 'dir. Ne yazık ki, sorun belirli bir sürüm numarasına indirgenemez. Daha fazla bilgi için  https://www.microsoft.com  adresini ziyaret ederek Microsoft Bilgi Bankası'nda "mapi dll" yi arayın.

----------------------------------------------------------------------
Önemli Erişebilirlik Notları
----------------------------------------------------------------------

LibreOffice 'in erişilebilirlik özellikleri ile ilgili daha fazla bilgi için https://www.libreoffice.org/accessibility/ adresini ziyaret ediniz

----------------------------------------------------------------------
Kullanıcı Desteği
----------------------------------------------------------------------

Ana destek sayfası size LibreOffice için yardım konusunda birçok seçenek sunmaktadır. Sorunuz hali hazırda cevaplanmış bile olabilir - https://www.documentfoundation.org/nabble/ adresindeki Topluluk Forumlarını kontrol edebilir veya https://www.libreoffice.org/lists/users/ adresindeki 'users@libreoffice.org' e-posta liste arşivlerini tarayabilirsiniz. alternatif olarak sorularınızı users@libreoffice.org 'e gönderebilirsiniz. Bu listeye üye olmak istiyorsanız(e-postalarınıza yanıt almak için) users+subscribe@libreoffice.org 'a boş bir e-posya gönderiniz.

LibreOffice web sayfasındaki SSS bölümünü de kontrol edin.

----------------------------------------------------------------------
Hata Raporlama & Sorunlar
----------------------------------------------------------------------

Hataları bildirmek, izlemek ve çözüme kavuşturmak için hali hazırda kullandığımız sistem Bugzilla olup https://bugs.libreoffice.org/ adresinde bulunmaktadır. Tüm kullanıcıların kendi platformlarında ortaya çıkabilecek hataları bildirebileceklerini hatırlatmak ve bunu yapmalarını teşvik etmek isteriz. Hataların heves ve titizlikle bildirilmesi, kullanıcı topluluğunun LibreOffice ürününün sürekli geliştirilmesine ve iyileştirilmesine yapabilecekkleri en önemli katkılardan biridir.

----------------------------------------------------------------------
Katkıda Bulunmak
----------------------------------------------------------------------

LibreOffice Topluluğu, bu açık kaynak kodlu ve önemli projenin geliştirilmesindeki aktif katılımınızdan çok yararlanacaktır.

Bir kullanıcı olarak, yazılımımızın gelişim sürecinde hali hazırda çok önemlisiniz ve sizin topluluğumuzda uzun dönemli bir katkıcı olarak daha aktif görevler almanızı teşvik etmek istiyoruz. Lütfen bize katılın ve LibreOffice web sayfasını inceleyin.

Başlangıç
----------------------------------------------------------------------

Katkı vermek için izlenecek en iyi yol, bir veya birkaç e-posta listesine üye olarak bir müddet takılmak, ve yavaş yavaş e-posta arşivlerindeki başlıkları gezerek kendinizi LibreOffice'in kaynak kodlarını açtığı Kasım 2000 yılından bu yana tartışılan birçok başlığa aşina kılmaktır. Kendinizi uygun hissettiğinizde tek yapmanız gereken bize kendinizi tanıtan bir e-posta göndererek işin içine dalmanız. Eğer Açık Kaynak Projeler ile alakalıysanız Yapılacaklar Listemize bir göz atın ve yardım etmek istediğiniz bir şeyleri belirlemek için LibreOffice web sayfasını ziyaret edin.

Üye ol
----------------------------------------------------------------------

Burada üye olabileceğniz birkaç eposta listesi bulunmaktadır: https://www.libreoffice.org/get-help/mailing-lists/

* Haberler: announce@documentfoundation.org *tüm kullanıcılara önerilir* (hafif mesaj trafiği)
* Ana kullanıcı listesi: users@global.libreoffice.org *tartışmalarda yer almanın kolay yolu* (yoğun mesaj trafiği)
* Pazarlama projesi: marketing@global.libreoffice.org *geliştirmenin ötesinde* (yoğun mesaj trafiği)
* Genel geliştirici listesi: libreoffice@lists.freedesktop.org (yoğun mesaj trafiği)

Projelere katılın
----------------------------------------------------------------------

Sınırlı yazılım tasarım ve kodlama deneyiminiz olsa bile, bu önemli özgür yazılım projesine değerli katkılarınız olabilir!

Biz, yeni LibreOffice 7.4'la ile çalışmaktan hoşlanacağınızı ümit ediyoruz ve bize çevirimiçi olarak katılabilirsiniz.

LibreOffice Topluluğu

----------------------------------------------------------------------
Kullanılmış / Değiştirilmiş Kaynak Kodu
----------------------------------------------------------------------

Parça Telif Hakkı 1998, 1999 James Clark. Parça Telif Hakkı 1996, 1998 Netscape Communications Corporation.
