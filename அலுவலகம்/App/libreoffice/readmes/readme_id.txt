
======================================================================
BacaSaya LibreOffice 7.4
======================================================================


Untuk pembaruan terakhir dari berkas readme ini, lihat https://git.libreoffice.org/core/tree/master/README.md

Berkas ini memuat informasi penting tentang perangkat lunak LibreOffice. Anda disarankan untuk membaca informasi ini secara hati-hati sebelum memulai pemasangan.

Komunitas LibreOffice bertanggung jawab atas pengembangan produk ini dan mengundang Anda untuk mempertimbangkan ikut serta sebagai anggota komunitas. Bila Anda adalah pengguna baru, Anda dapat mengunjungi situs LibreOffice, di mana Anda akan temukan banyak informasi tentang projek LibreOffice dan komunitas yang ada disekitarnya. Pergilah ke  https://www.libreoffice.org/.

Apakah LibreOffice Benar-benar Bebas untuk Siapa Saja?
----------------------------------------------------------------------

LibreOffice bebas digunakan oleh semua orang. Anda boleh membawa salinan LibreOffice dan memasangnya pada sebanyak komputer yang Anda suka, dan memakainya untuk keperluan apapun yang Anda suka (termasuk komersil, pemerintahan, administrasi publik, dan pendidikan). Untuk rincian lebih lanjut lihatlah teks lisensi yang dikemas dengan unduhan LibreOffice ini.

Kenapa LibreOffice Bebas untuk Semua Pengguna?
----------------------------------------------------------------------

Anda dapat memakai salinan LibreOffice ini secara gratis karena kontributor individu dan sponso korporat telah merancang, mengembangkan, menguji, menerjemahkan, mendokumentasikan, mendukung, memasarkan, dan membantu dalam banyak cara lain untuk membuat LibreOffice seperti hari ini - perangkat lunak produktivitas Open Source, bagi rumah dan kantor, yang paling unggul di dunia.

Bila Anda menghargai upaya mereka, dan ingin memastikan bahwa LibreOffice terus tersedia sampai jauh di masa mendatang, mohon pertimbangkan menyumbang ke projek - lihat https://www.documentfoundation.org/contribution/ untuk rinciannya. Setiap orang dapat memberikan kontribusi jenis tertentu.

----------------------------------------------------------------------
Catatan Pemasangan
----------------------------------------------------------------------

LibreOffice memerlukan Java Runtime Environment (JRE) versi cukup baru agar berfungsi secara penuh. JRE bukan bagian dari paket pemasangan LibreOffice, melainkan mesti dipasang secara terpisah.

Keperluan Sistem
----------------------------------------------------------------------

* Microsoft Windows 7 SP1, 8, 8.1 Update (S14), atau 10

Mohon perhatikan bahwa hak akses administrator diperlukan untuk proses pemasangan program.

Registrasi LibreOffice sebagai aplikasi utama untuk format Microsoft Office dapat dipaksa atau dibebaskan dengan menggunakan perintah baris berikut pada installer:

* REGISTER_ALL_MSO_TYPES=1 akan memaksa registrasi dari LibreOffice sebagai aplikasi baku bagi format Microsoft Office.
* REGISTER_NO_MSO_TYPES=1 akan mencegah registrasi dari LibreOffice sebagai aplikasi baku bagi format Microsoft Office.

Mohon pastikan bahwa Anda memiliki memori bebas yang cukup dalam direktori temporer pada sistem Anda, dan pastikan bahwa hak akses baca, tulis, dan jalankan telah diberikan. Tutup semua program lain sebelum memulai proses pemasangan.

Pemasangan LibreOffice pada sistem Linux berbasis Debian/Ubuntu
----------------------------------------------------------------------

Untuk petunjuk tentang bagaimana memasang suatu paket bahasa (setelah memasang versi Inggris AS dari LibreOffice), silakan baca seksi di bawah yang berjudul Memasang suatu Paket Bahasa.

Ketika Anda membongkar arsip yang diunduh, Anda akan melihat bahwa isinya telah diawamampatkan ke dalam subdirektori. Buka suatu jendela manajer berkas, dan ubah direktori ke satu yang diawali dengan "LibreOffice_", diikuti dengan nomor versi dan suatu informasi platform.

Direktori ini memuat suatu subdirektori bernama "DEBS". Pindahlah ke direktori "DEBS".

Klik kanan dalam direktori dan pilih "Buka dalam Terminal". Suatu jendela terminal akan terbuka. Dari baris perintah di jendela terminal, masukkan perintah berikut (Anda akan diminta memasukkan sandi pengguna root sebelum perintah dijalankan):

Perintah berikut akan memasang LibreOffice dan paket integrasi desktop (Anda boleh sekedar menyalin dan menempel mereka ke dalam suatu layar terminal daripada mencoba mengetikkannya):

sudo dpkg -i *.deb

Proses pemasangan kini komplit, dan Anda mestinya telah memiliki ikon bagi semua aplikasi LibreOffice pada menu desktop Aplikasi/Perkantoran.

Pemasangan LibreOffice pada Fedora, openSUSE, Mandriva, dan sistem Linux lain memakai paket RPM
----------------------------------------------------------------------

Untuk petunjuk tentang bagaimana memasang suatu paket bahasa (setelah memasang versi Inggris AS dari LibreOffice), silakan baca seksi di bawah yang berjudul Memasang suatu Paket Bahasa.

Ketika Anda membongkar arsip yang diunduh, Anda akan melihat bahwa isinya telah diawamampatkan ke dalam subdirektori. Buka suatu jendela manajer berkas, dan ubah direktori ke satu yang diawali dengan "LibreOffice_", diikuti dengan nomor versi dan suatu informasi platform.

Direktori ini memuat suatu subdirektori bernama "RPMS". Pindahlah ke direktori "RPMS".

Klik kanan dalam direktori dan pilih "Buka dalam Terminal". Suatu jendela terminal akan terbuka. Dari baris perintah di jendela terminal, masukkan perintah berikut (Anda akan diminta memasukkan sandi pengguna root sebelum perintah dijalankan):

Untuk sistem berbasis Fedora: sudo dnf install *.rpm

Untuk sistem berbasis Mandriva: sudo urpmi *.rpm

Untuk sistem berbasis RPM lainnya (openSUSE, dsb.): rpm -Uvh *.rpm

Proses pemasangan kini komplit, dan Anda mestinya telah memiliki ikon bagi semua aplikasi LibreOffice pada menu desktop Aplikasi/Perkantoran.

Sebagai alternatif, Anda dapat memakai skrip 'install', terletak di direktori puncak arsip ini untuk melakukan pemasangan sebagai pengguna. Skrip tersebut akan menyiapkan LibreOffice agar memiliki profilnya sendiri bagi pemasangan ini, terpisah dari profil LibreOffice normal Anda. Perhatikan bahwa ini tidak akan memasang bagian integrasi sistem seperti butir menu desktop dan registrasi jenis MIME desktop.

Catatan Menyangkut Integrasi Desktop Bagi Distribusi Linux Yang Tak Tercakup Dalam Instruksi Pemasangan Di Atas
----------------------------------------------------------------------

Mestinya cukup mudah untuk memasang LibreOffice pada distribusi Linux lain yang tidak secara spesifik dicakup dalam instruksi pemasangan ini. Aspek utama tempat mungkin terjadinya perbedaan adalah integrasi desktop.

Direktori RPMS (atau DEBS) juga memuat suatu paket bernama libreoffice7.4-freedesktop-menus-7.4.0.1-1.noarch.rpm (atau libreoffice7.4-debian-menus_7.4.0.1-1_all.deb, atau yang serupa). Ini adalah paket bagi semua distribusi Linux yang mendukung spesifikasi/rekomendasi Freedesktop.org (https://en.wikipedia.org/wiki/Freedesktop.org), dan disediakan untuk pemasangan pada distribusi Linux lain yang tidak dicakup oleh instruksi terdahulu.

Memasang suatu Pak Bahasa
----------------------------------------------------------------------

Unduh pak bahasa bagi platform dan bahasa yang Anda inginkan. Mereka tersedia di lokasi yang sama dengan arsip pemasangan utama. Dari manajer berkas Nautilus, ekstraklah arsip yang diunduh ke suatu direktori (misalnya, desktop Anda). Pastikan bahwa Anda telah keluar dari semua aplikasi LibreOffice (termasuk QuickStarter, bila dijalankan).

Berpindahlah ke direktori tempat Anda mengekstrak pak bahasa yang Anda unduh.

Sekarang ubah direktori ke direktori yang dibuat selama proses ekstraksi. Sebagai contoh, bagi paket bahasa Perancis untuk sistem 32-bit berbasis Debian/Ubuntu, direktori dinamai LibreOffice_, ditambah dengan informasi versi, tambah Linux_x86_langpack-deb_fr.

Kini ubah direktori ke direktori yang memuat paket yang akan dipasang. Pada sistem berbasis Debian/Ubuntu, direktori itu adalah DEBS. Pada sistem Fedora, openSUSE, atau Mandriva, direktorinya adalah RPMS.

Dari manajer berkas Nautilus, klik kanan pada direktori dan pilih perintah "Buka dalam terminal". Dalam jendela terminal yang baru Anda buka, jalankan perintah untuk memasang pak bahasa (dengan semua perintah di bawah, Anda mungkin diminta memasukkan sandi pengguna root):

Untuk sistem berbasis Debian/Ubuntu: sudo dpkg -i *.deb

Untuk sistem berbasis Fedora: su -c 'dnf install *.rpm'

Untuk sistem berbasis Mandriva: sudo urpmi *.rpm

Untuk sistem yang memakai RPM lainnya (openSUSE, dll.): rpm -Uvh *.rpm

Kini jalankan satu dari aplikasi LibreOffice - Writer misalnya. Pergi ke menu Perkakas dan pilih Pilihan. Pada kotak dialog Pilihan, klik "Pengaturan Bahasa", lalu klik pada "Bahasa". Jatuhkan senarai "Antar muka pengguna" dan pilih bahasa yang baru Anda pasang. Bila Anda inginkan, lakukan hal yang sama bagi "Pengaturan lokal", "Mata uang baku", dan "Bahasa baku bagi dokumen".

Setelah menata pengaturan tersebut, klik OK. Kotak dialog akan ditutup, dan Anda akan melihat pesan informasi yang menyatakan bahwa perubahan Anda hanya akan diaktifkan setelah Anda keluar dari LibreOffice dan memulainya lagi (ingat juga untuk keluar dari QuickStarter bila itu dijalankan).

Kali berikut Anda memulai LibreOffice, itu akan dimulai dalam bahasa yang baru Anda pasang.

----------------------------------------------------------------------
Masalah Selama Menjalankan Program
----------------------------------------------------------------------

Kesulitan memulai LibreOffice (misalnya aplikasi hang) serta masalah dengan tampilan layar sering kali disebabkan oleh penggerak kartu grafis. Jika masalah ini terjadi, perbarui penggerak kartu grafis Anda atau coba gunakan penggerak grafis yang disertakan dengan sistem operasi Anda.

----------------------------------------------------------------------
ALPS/laptop pedal-sentuh Synaptics pada Windows
----------------------------------------------------------------------

Berkenaan dengan isu penggerak Windows, Anda tak dapat menggulir dokumen LibreOffice saat Anda menggeser jari pada pedal-sentuh ALPS/Synaptics.

Untuk mengaktifkan pengguliran melalui pedal-sentuh, tambah baris berikut pada berkas konfigurasi "C:\Program Files\Synaptics\SynTP\SynTPEnh.ini", dan nyalakan ulang komputer Anda:

[LibreOffice]

FC = "SALFRAME"

SF = 0x10000000

SF |= 0x00004000

Catatan: Lokasi dari berkas konfigurasi dapat beragam pada versi Windows yang berbeda.

----------------------------------------------------------------------
Tombol Pintas
----------------------------------------------------------------------

Hanya tombol pintas (kombinasi tombol) yang tidak digunakan oleh sistem operasi yang dapat digunakan pada LibreOffice. Bila kombinasi tombol pada LibreOffice tidak bekerja seperti yang diuraikan pada Bantuan LibreOffice, periksalah apakah pintas tersebut sudah digunakan oleh sistem operasi. Untuk memperbaiki konflik seperti itu, Anda bisa mengganti tombol yang diatur oleh sistem operasi. Sebagai alternatif, Anda bisa mengubah hampir semua penugasan tombol pada LibreOffice. Untuk informasi lebih lanjut tentang topik ini, rujuklah Bantuan LibreOffice atau dokumentasi Bantuan sistem operasi Anda.

----------------------------------------------------------------------
Masalah Saat Mengirim Dokumen sebagai Surel Dari LibreOffice
----------------------------------------------------------------------

Saat mengirin dokumen via 'Berkas - Kirim - Dokumen sebagai Surel' atau 'Dokumen sebagai Lampiran PDF' beberapa masalah mungkin terjadi (program yang bentrok atau tersangkut). Ini adalah masalah pada berkas sistem "Mapi" (Messaging Application Programming Interface) Windows yang menyebabkan masalah pada beberapa versi berkas. Sayangnya, masalah ini tidak dapat dipersempit ke nomor versi tertentu. Untuk informasi lebih lanjut, kunjungi https://www.microsoft.com untuk mencari Microsoft Knowledge Base bagi "mapi dll".

----------------------------------------------------------------------
Catatan Penting Aksesibilitas
----------------------------------------------------------------------

Untuk informasi lebih tentang fitur aksesabilitas dalam LibreOffice, lihat  https://www.libreoffice.org/accessibility/

----------------------------------------------------------------------
Dukungan Pengguna
----------------------------------------------------------------------

Halaman dukungan utama menawarkan berbagai kemungkinan mendapatkan bantuan tentang LibreOffice. Pertanyaan Anda mungkin telah terjawab - periksa Forum Komunitas di https://www.documentfoundation.org/nabble/ atau cari pada arsip milis 'users@libreoffice.org' di https://www.libreoffice.org/lists/users/. Sebagai alternatif, Anda dapat mengirim pertanyaan Anda ke users@libreoffice.org. Bila Anda mau berlangganan ke milis (untuk memperoleh balasan surel), kirim surat kosong ke: users+subscribe@libreoffice.org.

Periksa juga bagian FAQ pada situs web LibreOffice.

----------------------------------------------------------------------
Melaporkan Kutu & Masalah
----------------------------------------------------------------------

Sistem kami untuk melaporkan, melacak, dan memecahkan kutu kini adalah BugZilla, dihosting di https://bugs.documentfoundation.org/. Kami anjurkan semua pengguna untuk merasa berhak dan disambut untuk melaporkan kutu yang mungkin muncul pada platform Anda. Pelaporan kutu yang bersemangat adalah salah satu sumbangan terpenting dari komunitas pengguna yang dapat diberikan bagi pengembangan dan perbaikan berkelanjutan dari LibreOffice.

----------------------------------------------------------------------
Ikut Terlibat
----------------------------------------------------------------------

Komunitas LibreOffice akan memperoleh banyak keuntungan dari partisipasi aktif Anda dalam pengembangan proyek kode sumber terbuka ini.

Sebagai seorang pengguna, Anda telah menjadi suatu bagian berharga dari proses pengembangan kumpulan aplikasi ini dan kami mendorong Anda untuk ikut berperan lebih aktif menjadi kontributor jangka panjang ke komunitas. Silakan bergabung dan periksa halaman kontribusi di situs web LibreOffice

Bagaimana Memulai
----------------------------------------------------------------------

Cara terbaik untuk memulai berkontribusi adalah dengan berlangganan ke satu atau lebih milis, untuk sementara menjadi pemerhati, dan secara bertahap menggunakan arsip surel untuk membiasakan diri Anda dengan banyaknya topik yang dicakup semenjak kode sumber LibreOffice dirilis pada Oktober 2000. Saat Anda sudah merasa nyaman, yang Anda butuhkan adalah mengirim surel perkenalan diri dan langsung terlibat. Kalau Anda sudah terbiasa dengan Projek Open Source, periksa senarai tugas kami dan periksa apakah ada yang ingin Anda bantu di situs web LibreOffice.

Mendaftar
----------------------------------------------------------------------

Berikut adalah beberapa milis yang dapat Anda ikuti pada https://www.libreoffice.org/get-help/mailing-lists/

* Berita: announce@documentfoundation.org *disarankan bagi semua pengguna* (lalu lintas ringan)
* Milis pengguna utama: users@global.libreoffice.org *cara mudah memantau diskusi* (lalu lintas ramai)
* Projek pemasaran: marketing@global.libreoffice.org *di luar pengembangan* (semakin ramai)
* Milis umum pengembang: libreoffice@lists.freedesktop.org (lalu lintas padat)

Bergabung ke satu Projek atau lebih
----------------------------------------------------------------------

Anda bisa memberikan kontribusi besar untuk proyek kode sumber terbuka ini, meski Anda sendiri adalah orang dengan pengalaman desain peranti lunak atau koding yang terbatas. Ya, Anda bisa!

Kami harap Anda menikmati bekerja dengan LibreOffice 7.4 yang baru ini dan akan bergabung secara daring bersama kami.

Komunitas LibreOffice

----------------------------------------------------------------------
Penggunaan / Pengubahan Kode Sumber
----------------------------------------------------------------------

Sebagian Hak Cipta 1998, 1999 James Clark. Sebagian Hak Cipta 1996, 1998 Netscape Communications Corporation.
