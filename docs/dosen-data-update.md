# Laporan Hasil Pencocokan Data Dosen (dosen.json vs Database)

Dokumen ini berisi hasil analisis perbandingan antara data hasil scraping (`dosen.json`) dan data master dosen yang ada di database (`siredo.db`).

## 1. Ringkasan Statistik

- **Total Record di Scrap (`dosen.json`)**: 78
- **Total Record Dosen di DB**: 86
- **Record Berhasil Dicocokkan (Matched)**: 75
- **Record Scrap Baru (Unmatched Scrap)**: 3
- **Record DB Tanpa Pasangan Scrap (Unmatched DB)**: 0

## 2. Rincian Data Cocok (Matched Records) & Usulan Penyesuaian

Tabel di bawah ini menampilkan perbandingan data dosen DB dengan data scrap yang cocok beserta perubahan data yang diusulkan:

| No | Nama DB | Nama Scrap | Metode Match | NIDN Lama -> Baru | Keahlian Baru | Status |
|---|---|---|---|---|---|---|
| 1 | Ahmad Hamim Thohari, S.S.T., M.T. | Ahmad Hamim Thohari, S.S.T., M.T. | Name Similarity (100%) | `-` -> `115143` | Software Development, Database, E-Government | READY TO UPDATE |
| 2 | Festy Winda Sari, S.Tr. Kom | Festy Winda Sari, S.Tr. Kom., M.Sc | Name Similarity (100%) | `-` -> `122288` | App Security, Web Security, Programming | READY TO UPDATE |
| 3 | Mir'atul Khusna Mufida, S.ST, M.Sc | Mir'atul Khusna Mufida, PhD. | Name Similarity (100%) | `-` -> `109057` | AI, Big Data Analytics, ITS | READY TO UPDATE |
| 4 | Yeni Rokhayati, S.Si., M.Sc | Yeni Rokhayati, S.Si., M.Sc | Name Similarity (100%) | `-` -> `112093` | Data Science | READY TO UPDATE |
| 5 | Happy Yugo Prasetiya, S.Sn., M.Sn | Happy Yugo Prasetiya, S.Sn., M.Sn | Name Similarity (100%) | `-` -> `112092` | Desain Komunikasi Visual, Animasi | READY TO UPDATE |
| 6 | Farouki Dinda Rassarandi, S.T., M.Eng | Ir. Farouki Dinda Rassarandi, S.T., M.Eng. | Name Similarity (100%) | `-` -> `118208` | Survei Terestris, Geoinformatika | READY TO UPDATE |
| 7 | Maidel Fani, S.Pd., M.Kom. | Maidel Fani, S.Pd., M.Kom. | Name Similarity (100%) | `-` -> `117192` | Ilmu Komputer | READY TO UPDATE |
| 8 | Supardianto, S.ST., M.Eng | Supardianto, M.Eng. | Name Similarity (100%) | `-` -> `113105` | Ilmu Komputer | READY TO UPDATE |
| 9 | Metta Santiputri, S.T., M.Sc, Ph.D | Metta Santiputri, S.T., M.Sc, Ph.D | Name Similarity (100%) | `-` -> `100017` | Software Engineering | READY TO UPDATE |
| 10 | Liony Lumombo, S.ST., M.IDes | Liony Lumombo, S.ST., M.IDes | Name Similarity (100%) | `-` -> `113118` | Game UI/UX Design, HCI | READY TO UPDATE |
| 11 | Andri Albertha Pratama, S.Tr. Kom., M.Sn | Andri Albertha Pratama, S.Tr.Kom., M.Sn | Name Similarity (100%) | `-` -> `211100` | Pengkajian Film | READY TO UPDATE |
| 12 | Ari Wibowo, ST., MT | Dr. Ari Wibowo, S.T., M.T. | Name Similarity (76%) | `-` -> `100012` | AI, Computer Vision, Autonomous System | READY TO UPDATE |
| 13 | Uuf Brajawidagda, S.T., M.T., Ph.D | Dr. Uuf Brajawidagda, S.T., M.T., Ph.D | Name Similarity (100%) | `-` -> `100015` | Sistem Informasi, E-Government | READY TO UPDATE |
| 14 | Hilda Widyastuti, S.T., M.T. | Hilda Widyastuti, S.T., M.T. | Name Similarity (100%) | `-` -> `102020` | Kecerdasan Buatan | READY TO UPDATE |
| 15 | Riwinoto, S.T., M.Kom | Riwinoto, ST,M.Kom | Name Similarity (84%) | `-` -> `103025` | Game, Simulasi, Teknologi Reality, Kewirausahaan | READY TO UPDATE |
| 16 | Andy Triwinarko, ST., MT., Ph.D | Andy Triwinarko, ST, M.T., Ph.D | Name Similarity (92%) | `-` -> `105038` | Telecommunication, Informatics | READY TO UPDATE |
| 17 | Evaliata Br. Sembiring, S.Kom., M.Cs | Evaliata Br. Sembiring, S.Kom., M.Cs | Name Similarity (100%) | `-` -> `106042` | Computer Science, Artificial Intelligence, Multimedia Content | READY TO UPDATE |
| 18 | Nur Cahyono Kushardianto, S.Si., M.T., M.Sc | Nur Cahyono Kushardianto,S.Si., M.T., M.Sc., Ph.D | Name Similarity (100%) | `-` -> `106044` | Jaringan Komputer, Teknologi Komunikasi, Machine Learning | READY TO UPDATE |
| 19 | Afdhol Dzikri, S.ST., M.T | Afdhol Dzikri, S.ST., M.T | Name Similarity (100%) | `-` -> `107048` | Computer Vision, Biometrik | READY TO UPDATE |
| 20 | Agus Fatulloh, S.T., M.T | Agus Fatulloh, S.T., M.T | Name Similarity (100%) | `-` -> `107051` | Computer Organization and Architecture, Operating System, Networking and Hardware Technology, Computer Engineering, Software Applications Development, Social Computing | READY TO UPDATE |
| 21 | Condra Antoni, SS., M.A | Condra Antoni,SS, M.A | Name Similarity (100%) | `-` -> `107054` | Linguistic | READY TO UPDATE |
| 22 | Mira Chandra Kirana, S.T., M.T | Mira Chandra Kirana, S.T., M.T | Name Similarity (100%) | `-` -> `109064` | Biomedical Engineering, Image Processing, Intelligent System | READY TO UPDATE |
| 23 | Gendhy Dwi Harlyan, S.Sn., M.Sn | Gendhy Dwi Harlyan, S.Sn.,M.Sn | Name Similarity (100%) | `-` -> `112086` | Audio Visual | READY TO UPDATE |
| 24 | Nur Zahrati Janah, S.Kom., M.Sc | Nur Zahrati Janah, S.Kom, M.Sc | Name Similarity (100%) | `-` -> `112087` | Software Development, Machine Learning, Image Processing | READY TO UPDATE |
| 25 | Dwi Ely Kurniawan, S.Pd., M.Kom | Ir. Dwi Ely Kurniawan, S.Pd., M.Kom | Name Similarity (100%) | `-` -> `112094` | Information System, Mobile Programming, Computer Network, Multimedia Learning | READY TO UPDATE |
| 26 | Maria, S.ST., M.Sn | Ir. Maria, S.ST., M.Sn., IPP | Name Similarity (71%) | `-` -> `113103` | Multimedia Technology, Animation | READY TO UPDATE |
| 27 | Selly Artaty Zega, S.ST., M.Sc | Ir. Selly Artaty Zega, S.ST., M.Sc | Name Similarity (100%) | `-` -> `113104` | Digital Media Technology | READY TO UPDATE |
| 28 | Sandi Prasetyaningsih, S.ST., M.Media | Sandi Prasetyaningsih, S.ST., M.Media | Name Similarity (100%) | `-` -> `113106` | Media dan Komunikasi | READY TO UPDATE |
| 29 | Sudra Irawan, S.Pd.Si., M.Sc | Ir. Sudra Irawan, S.Pd.Si., M.Sc., IPM. | Name Similarity (88%) | `-` -> `113110` | Geoscience, Geophysics, Hydro-oceanography, Geology, GIS | READY TO UPDATE |
| 30 | Sartikha, S. ST., M.Eng | Sartikha, S. ST., M.Eng | Name Similarity (100%) | `-` -> `113115` | Database Engineering, Software Engineering, Optimization | READY TO UPDATE |
| 31 | Arta Uly Siahaan, S.Pd, M.Pd | Arta Uly Siahaan, S.Pd, M.Pd | Name Similarity (100%) | `-` -> `114131` | Pendidikan Bahasa Inggris | READY TO UPDATE |
| 32 | Oktavianto Gustin, S.T., M.T | Ir. Oktavianto Gustin, S.T., M.T., IPM. | Name Similarity (89%) | `-` -> `115138` | GNSS, Remote Sensing, Engineering Survey | READY TO UPDATE |
| 33 | Nelmiawati, B.CS., M.Comp.Sc | Nelmiawati, B.CS., M.Comp.Sc | Name Similarity (100%) | `-` -> `115148` | Computer Network, Information Security, Computer Science | READY TO UPDATE |
| 34 | Muhammad Zainuddin Lubis, S.I.k, M.Si | Muhammad Zainuddin Lubis, S.I.k, M.Si | Name Similarity (100%) | `-` -> `116162` | Hydrographic Survey, Physical Oceanography, Underwater Acoustic, Marine GIS | READY TO UPDATE |
| 35 | Wenang Anurogo, S.Si., M.Sc. | Wenang Anurogo, S.Si., M.Sc. | Name Similarity (100%) | `-` -> `116163` | Computer Network, Information Security, Computer Science | READY TO UPDATE |
| 36 | Muchamad Fajri Amirul Nasrullah, S.ST., M.Sc | Muchamad Fajri Amirul Nasrullah, S.ST., M.Sc | Name Similarity (100%) | `-` -> `117173` | Video Coding, Video Effect, Mobile Application | READY TO UPDATE |
| 37 | Hamdani Arif, S.Pd., M.Sc | Hamdani Arif, S.Pd., M.Sc | Name Similarity (100%) | `-` -> `117175` | Networking, IoT | READY TO UPDATE |
| 38 | Luthfiya Ratna Sari, S.Si., M.T. | Ir. Luthfiya Ratna Sari, S.Si., M.T. | Name Similarity (100%) | `-` -> `117196` | Aplikasi Sistem Informasi Geografis, Penginderaan Jauh, Kartografi | READY TO UPDATE |
| 39 | Rina Yulius, S.Pd., M.Eng | Rina Yulius, S.Pd., M.Eng | Name Similarity (100%) | `-` -> `118199` | E-Learning, Human Computer Interaction, Gamification | READY TO UPDATE |
| 40 | Satriya Bayu Aji, S.S., M.Hum. | Satriya Bayu Aji, S.S., M.Hum. | Name Similarity (100%) | `-` -> `118201` | Bahasa Inggris | READY TO UPDATE |
| 41 | Siti Noor Chayati, S.T., M.Sc | Siti Noor Chayati, S.T., M.Sc | Name Similarity (100%) | `-` -> `118207` | Hydrographic Surveying | READY TO UPDATE |
| 42 | Agung Riyadi, S.Si., M.Kom | Agung Riyadi, S.Si., M.Kom | Name Similarity (100%) | `-` -> `119221` | Artificial Intelligence | READY TO UPDATE |
| 43 | Dodi Prima Resda, S.Pd., M.Kom | Dodi Prima Resda, S.Pd., M.Kom | Name Similarity (100%) | `-` -> `119222` | Teknik Informatika, Rekayasa Keamanan Siber | READY TO UPDATE |
| 44 | Fadli Suandi, S.T., M.Kom. | Fadli Suandi, S.T., M.Kom. | Name Similarity (100%) | `-` -> `119223` | Human Computer Interaction, Photography, Multimedia | READY TO UPDATE |
| 45 | Swono Sibagariang, S.Kom., M.Kom | Swono Sibagariang, S.Kom., M.Kom | Name Similarity (100%) | `-` -> `119224` | Software Development | READY TO UPDATE |
| 46 | Siskha Handayani, S.Si., M.Si | Siskha Handayani M.Si | Name Similarity (100%) | `-` -> `121246` | Matematika | READY TO UPDATE |
| 47 | Dwi Amalia Purnamasari, S.T., M.Cs | Dwi Amalia Purnamasari, S.T., M.Cs. | Name Similarity (100%) | `-` -> `121248` | Software Development, Supply Chain Management, Forecasting | READY TO UPDATE |
| 48 | Rini Amadia, S.Sn., M.Sn | Rini Amadia, S.Sn.,M.Sn | Name Similarity (100%) | `-` -> `122256` | Desain Komunikasi Visual | READY TO UPDATE |
| 49 | Aragani Timur Kanistren, S.Sn., M.Sn | Aragani Timur Kanistren. S.Sn ., M.Sn | Name Similarity (100%) | `-` -> `122258` | Naskah Produksi, Ide Kreatif, Broadcasting | READY TO UPDATE |
| 50 | Anis Rahmi, S.Tr. Kom., M.Sn | Anis Rahmi, S.Tr. Kom., M.Sn | Name Similarity (100%) | `-` -> `122259` | 2D Skeletal Animation, 3D Animation Workflow, Rigging, Lighting, Render & Compositing, Object-Oriented Computer Animation | READY TO UPDATE |
| 51 | Feby, M.Pd | Feby, S.Pd, M.Pd | Name Similarity (100%) | `-` -> `122270` | Bahasa Inggris | READY TO UPDATE |
| 52 | Ahmadi Irmansyah Lubis, S.kom., M.kom. | Ahmadi Irmansyah Lubis, S.Kom., M.Kom. | Name Similarity (100%) | `-` -> `122275` | Artificial Intelligence, Decision Support System, Machine Learning, Computer Science | READY TO UPDATE |
| 53 | Antoni Haikal, S.ST.,M.T | Antoni Haikal | Name Similarity (100%) | `-` -> `122276` | Application Security, Software Development, Offensive Security | READY TO UPDATE |
| 54 | Noper Ardi, S.Pd., M.Eng | Noper Ardi, S.Pd., M.Eng | Name Similarity (100%) | `-` -> `122277` | RPL, AI | READY TO UPDATE |
| 55 | Alena Uperiati, S.T, M.Cs | Alena Uperiati, S.T., M.Cs | Name Similarity (100%) | `-` -> `122279` | Machine Learning, Data Science, Software Development | READY TO UPDATE |
| 56 | Amirul Mu’minin, S.Ds., M.Ds. | Amirul Mu'minin, S.Ds, M.Ds. | Name Similarity (96%) | `-` -> `122280` | Desain Grafis, Game Desain, Visual Effect | READY TO UPDATE |
| 57 | Cahya Miranto, S.S.T., M.Tr.Kom. | Cahya Miranto, S.S.T, M.Tr.Kom | Name Similarity (100%) | `-` -> `122282` | Animasi 3D | READY TO UPDATE |
| 58 | Muhammad Idris S.Tr | Muhammad Idris, S.Tr., M.Tr.Kom | Name Similarity (84%) | `-` -> `122283` | Software Development, QA Software, Security | READY TO UPDATE |
| 59 | Ardiman Firmanda, S.S.T., M.Tr.Kom. | Ardiman Firmanda, S.S.T, M.Tr.Kom | Name Similarity (100%) | `-` -> `122284` | Musik | READY TO UPDATE |
| 60 | Chairoel Adam S.Ds., M.Sn. | Chairoel Adam, S. Ds., M. Sn. | Name Similarity (72%) | `-` -> `123298` | Penciptaan Seni | READY TO UPDATE |
| 61 | Suwarno, S.S., M.Pd | Suwarno, S.S., M.Pd | Name Similarity (100%) | `-` -> `124300` | Systemic Functional Linguistics, Computational Linguistics | READY TO UPDATE |
| 62 | Nursaimah Harhap | Nursaima Harahap, S.Pd, M.Hum | Name Similarity (93%) | `-` -> `124302` | Bahasa Inggris | READY TO UPDATE |
| 63 | Rusyda Nazhirha | Rusyda Nazhirah Yunus, S.S.,M.Si | Name Similarity (77%) | `-` -> `124307` | Linguistik Terapan, Wacana Digital, Teks Multimodal, Bahasa Indonesia | READY TO UPDATE |
| 64 | Berliansyah Ramadhan | Berliansyah Rumodhon, S.Pd.,M.Sn | Name Similarity (85%) | `-` -> `124313` | Musik | READY TO UPDATE |
| 65 | Luki Aswar M.Pd. | Luki Aswar, M.Pd. | Name Similarity (100%) | `-` -> `124316` | Pendidikan Bahasa Indonesia | READY TO UPDATE |
| 66 | Fendra Dwi R | Fendra Dwi Ramadhan, S.T., M.T. | Name Similarity (77%) | `-` -> `124326` | Remote Sensing, Geographical Information System (GIS), Geoinformatics, GNSS, Photogrammetry | READY TO UPDATE |
| 67 | Cyntia Lasmi | Cyntia Lasmi Andesti, S.Kom., M.Kom | Name Similarity (75%) | `-` -> `125331` | Artificial Intelligence, Data Mining | READY TO UPDATE |
| 68 | Arif Rahman, M.T | Arif Rahman, M.T | Name Similarity (100%) | `-` -> `125341` | Perencanaan Bangunan, AutoCad | READY TO UPDATE |
| 69 | Holong Marisi Simalango, M.Kom. | Holong Marisi Simalango, A.Md., S.T., M.Kom. | Name Similarity (90%) | `-` -> `125346` | Software Engineering, IoT, AI, Game Development | READY TO UPDATE |
| 70 | Kawan Pandiangan, S.Sn.,M.Sn | Kawan Pandiangan S.Sn.,M.Sn | Name Similarity (100%) | `-` -> `125350` | Music, Ethnomusicology, Performing Arts | READY TO UPDATE |
| 71 | Nadya Satya Handayani, M.Kom | Nadya Satya Handayani, S.Kom., M.Kom | Name Similarity (100%) | `-` -> `125351` | Biomedical, AI | READY TO UPDATE |
| 72 | Nur Israyani, S.T, M.T | Nur Israyani, S.T., M.T | Name Similarity (100%) | `-` -> `125352` | Geographical Information System (GIS) | READY TO UPDATE |
| 73 | Recy Harviani Zurwanty, S.Pd., M.Pd | Recy Harviani Zurwanty,S.Pd.,M.Pd | Name Similarity (100%) | `-` -> `125355` | Pendidikan Pancasila, Pendidikan Kewarganegaraan | READY TO UPDATE |
| 74 | Sri Rahayu, M.Pd | Sri Rahayu, M.Pd | Name Similarity (100%) | `-` -> `125359` | Pendidikan Pancasila, Pendidikan Kewarganegaraan (Civics Education) | READY TO UPDATE |
| 75 | Sukma Evadini, S.T., M.Kom | Sukma Evadini, S.T., M.Kom | Name Similarity (100%) | `-` -> `125360` | Data Mining, Expert System, Machine Learning | READY TO UPDATE |


## 3. Rincian Perubahan Field Per Dosen (Detail Inspection)

### 1. Ahmad Hamim Thohari, S.S.T., M.T.
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `115143`
- **Program Studi**: `Rekayasa Keamanan Siber` -> `Rekayasa Keamanan Siber`
- **Bidang Keahlian**: `Software Development, Database, E-Government` -> `Software Development, Database, E-Government`
- **Pendidikan**: `DIV Politeknik Negeri Batam - Teknologi Rekayasa Multimedia; S2 ITB - Teknik Informatika` -> `Sarjana Terapan (DIV) Politeknik Negeri Batam : Teknologi Rekayasa Multimedia, Magister (S2) Institut Teknologi Bandung : Teknik Informatika`

### 2. Festy Winda Sari, S.Tr. Kom
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `122288`
- **Program Studi**: `Rekayasa Keamanan Siber` -> `Rekayasa Keamanan Siber`
- **Bidang Keahlian**: `App Security, Web Security, Programming` -> `App Security, Web Security, Programming`
- **Pendidikan**: `DIII Politeknik Negeri Batam - Teknik Informatika; DIV Politeknik Negeri Batam - Multimedia dan Jaringan; S2 Swansea University - Cyber Security` -> `Diploma (DIII) Teknik Informatika Politeknik Negeri Batam, Sarjana Terapan (DIV) Multimedia dan Jaringan Politeknik Negeri Batam, Magister (S2) Cyber Security Swansea University`

### 3. Mir'atul Khusna Mufida, S.ST, M.Sc
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `109057`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `AI, Big Data Analytics, ITS` -> `AI, Big Data Analytics, ITS`
- **Pendidikan**: `DIV ITS - Teknologi Informasi; S2 Universite Grenoble Alpes - Informatique; S3 Universite Polytechnique Hauts de France` -> `Sarjana Terapan (DIV) Institut Teknologi Sepuluh Nopember : Teknologi Informasi, Magister (S2) Universite Grenoble Alpes : Informatique, Doktor (S3) Universite Polytechnique Hauts de France (UPHF)`

### 4. Yeni Rokhayati, S.Si., M.Sc
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `112093`
- **Program Studi**: `Teknik Informatika` -> `Teknik Informatika`
- **Bidang Keahlian**: `Data Science` -> `Data Science`
- **Pendidikan**: `S1 Universitas Riau - Matematika; S2 Universiti Malaysia Terengganu - Sains Matematik` -> `Sarjana (S1) Universitas Riau : Matematika, Magister (S2) Universiti Malaysia Terengganu : Sains Matematik`

### 5. Happy Yugo Prasetiya, S.Sn., M.Sn
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `112092`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Desain Komunikasi Visual, Animasi` -> `Desain Komunikasi Visual, Animasi`
- **Pendidikan**: `S1 Universitas Negeri Malang - Desain Komunikasi Visual; S2 ISI Yogyakarta - Pengkajian Seni DKV` -> `Sarjana (S1) Universitas Negeri Malang : Desain Komunikasi Visual, Magister (S2) ISI Yogyakarta : Pengkajian Seni Desain Komunikasi Visual`

### 6. Farouki Dinda Rassarandi, S.T., M.Eng
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `118208`
- **Program Studi**: `Teknologi Geomatika` -> `Teknologi Geomatika`
- **Bidang Keahlian**: `Survei Terestris, Geoinformatika` -> `Survei Terestris, Geoinformatika`
- **Pendidikan**: `S1 ITN Malang - Teknik Geodesi; S2 UGM - Teknologi Geomatika; PSPPI Politeknik Negeri Batam` -> `Sarjana (S1) Institut Teknologi Nasional (ITN) Malang : Teknik Geodesi, Magister (S2) Universitas Gadjah Mada (UGM) : Teknologi Geomatika, PSPPI Politeknik Negeri Batam`

### 7. Maidel Fani, S.Pd., M.Kom.
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `117192`
- **Program Studi**: `Rekayasa Keamanan Siber` -> `Rekayasa Keamanan Siber`
- **Bidang Keahlian**: `Ilmu Komputer` -> `Ilmu Komputer`
- **Pendidikan**: `S1 STAIN Bukittinggi - Pendidikan Teknik Informatika dan Komputer; S2 Universitas Putra Indonesia YPTK Padang - Ilmu Komputer` -> `Sarjana (S1) STAIN Bukit Tinggi : Pendidikan Teknik Informatika dan Komputer, Magister (S2) Universitas Putra Indonesia YPTK Padang : Ilmu Komputer`

### 8. Supardianto, S.ST., M.Eng
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `113105`
- **Program Studi**: `Teknologi Rekayasa Perangkat Lunak` -> `Teknologi Rekayasa Perangkat Lunak`
- **Bidang Keahlian**: `Ilmu Komputer` -> `Ilmu Komputer`
- **Pendidikan**: `S1 ITB - Teknik Media Digital; S2 UGM - Teknologi Informasi` -> `Sarjana (S1) Institut Teknologi Bandung : Teknik Media Digital, Magister (S2) Universitas Gadjah Mada : Teknologi Informasi`

### 9. Metta Santiputri, S.T., M.Sc, Ph.D
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `100017`
- **Program Studi**: `Teknik Komputer` -> `Teknik Komputer`
- **Bidang Keahlian**: `Software Engineering` -> `Software Engineering`
- **Pendidikan**: `S1 ITB - Teknik Informatika; S2 University of Twente - Computer Science; S3 University of Wollongong - Computer Science` -> `Sarjana (S1) Institut Teknologi Bandung : Teknik Informatika, Magister (S2) University of Twente : Computer Science, Doktor (S3) University of Wollongong : Computer Science`

### 10. Liony Lumombo, S.ST., M.IDes
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `113118`
- **Program Studi**: `Teknologi Permainan` -> `Teknologi Permainan`
- **Bidang Keahlian**: `Game UI/UX Design, HCI` -> `Game UI/UX Design, HCI`
- **Pendidikan**: `DIV ITB - Animation; S2 The University of Queensland - Interaction Design` -> `Sarjana Terapan (DIV) Institut Teknologi Bandung : Animation, Magister (S2) The University of Queensland : Master of Interaction Design`

### 11. Andri Albertha Pratama, S.Tr. Kom., M.Sn
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `211100`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Pengkajian Film` -> `Pengkajian Film`
- **Pendidikan**: `DIV Politeknik Negeri Batam - Teknik Multimedia dan Jaringan; S2 ISI Surakarta` -> `Sarjana Terapan (DIV) Politeknik Negeri Batam : Teknik Multimedia dan Jaringan, Magister (S2) Institut Seni Indonesia Surakarta`

### 12. Ari Wibowo, ST., MT
- **Metode Match**: Name Similarity (76%)
- **NIDN**: `` -> `100012`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `AI, Computer Vision, Autonomous System` -> `AI, Computer Vision, Autonomous System`
- **Pendidikan**: `S1 ITB - Teknik Informatika; S2 ITB - Informatika; S3 ITB - Teknik Elektro Informatika` -> `Sarjana (S1) Institut Teknologi Bandung : Teknik Informatika, Magister (S2) Institut Teknologi Bandung : Informatika, Doktor (S3) Institut Teknologi Bandung : Teknik Elektro Informatika`

### 13. Uuf Brajawidagda, S.T., M.T., Ph.D
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `100015`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Sistem Informasi, E-Government` -> `Sistem Informasi, E-Government`
- **Pendidikan**: `S1 ITB - Teknik Industri; S2 ITB - Teknik Informatika; S3 University of Wollongong - Computer Science` -> `Sarjana (S1) Institut Teknologi Bandung : Teknik Industri, Magister (S2) Institut Teknologi Bandung : Teknik Informatika, Doktor (S3) University of Wollongong : Computer Science`

### 14. Hilda Widyastuti, S.T., M.T.
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `102020`
- **Program Studi**: `Teknik Informatika` -> `Teknik Informatika`
- **Bidang Keahlian**: `Kecerdasan Buatan` -> `Kecerdasan Buatan`
- **Pendidikan**: `S1 ITB - Teknik Informatika; S2 ITB - Informatika` -> `Sarjana (S1) Institut Teknologi Bandung : Teknik Informatika, Magister (S2) Institut Teknologi Bandung : Informatika`

### 15. Riwinoto, S.T., M.Kom
- **Metode Match**: Name Similarity (84%)
- **NIDN**: `` -> `103025`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Game, Simulasi, Teknologi Reality, Kewirausahaan` -> `Game, Simulasi, Teknologi Reality, Kewirausahaan`
- **Pendidikan**: `S1 ITB - Teknik Informatika; S2 Universitas Indonesia - Ilmu Komputer` -> `Sarjana (S1) Institut Teknologi Bandung : Teknik Informatika, Magister (S2) Universitas Indonesia : Ilmu Komputer`

### 16. Andy Triwinarko, ST., MT., Ph.D
- **Metode Match**: Name Similarity (92%)
- **NIDN**: `` -> `105038`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Telecommunication, Informatics` -> `Telecommunication, Informatics`
- **Pendidikan**: `S1 ITB - Teknik Informatika; S2 Universitas Indonesia - Teknik Elektro; S3 Universite Polytechnique Hauts-de-France - Electronique` -> `Sarjana (S1) Institut Teknologi Bandung : Teknik Informatika, Magister (S2) Universitas Indonesia : Teknik Elektro, Doktor (S3) Universit Polytechnique Hauts-de-France : Electronique`

### 17. Evaliata Br. Sembiring, S.Kom., M.Cs
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `106042`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Computer Science, Artificial Intelligence, Multimedia Content` -> `Computer Science, Artificial Intelligence, Multimedia Content`
- **Pendidikan**: `S1 Univ Katholik St Thomas Sumatera Utara - Teknik Informatika; S2 UGM - Ilmu Komputer` -> `Sarjana (S1) Univ Katholik St Thomas Sumatera Utara : Teknik Informatika, Magister (S2) Universitas Gadjah Mada : Ilmu Komputer`

### 18. Nur Cahyono Kushardianto, S.Si., M.T., M.Sc
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `106044`
- **Program Studi**: `Teknik Komputer` -> `Teknik Komputer`
- **Bidang Keahlian**: `Jaringan Komputer, Teknologi Komunikasi, Machine Learning` -> `Jaringan Komputer, Teknologi Komunikasi, Machine Learning`
- **Pendidikan**: `S1 ITB - Matematika; S2 Universitas Indonesia - Jaringan Informasi dan Multimedia; S2 Universite de Valenciennes - Communication Systems Engineering; S3 Universite Polytechnique ...` -> `Sarjana (S1) Institut Teknologi Bandung : Matematika, Magister (S2) Universitas Indonesia : Jaringan Informasi dan Multimedia, Magister (S2) Universite de Valenciennes et du Hainaut-Cambresis : Communication Systems Engineering, Doktor (S3) Universite Polytechnique Hauts-de-France : Electronics`

### 19. Afdhol Dzikri, S.ST., M.T
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `107048`
- **Program Studi**: `Teknik Informatika` -> `Teknik Informatika`
- **Bidang Keahlian**: `Computer Vision, Biometrik` -> `Computer Vision, Biometrik`
- **Pendidikan**: `DIV PENS - Teknologi Informasi; S2 ITS - Jaringan Cerdas Multimedia, Teknik Elektro` -> `Sarjana Terapan (DIV) PENS : Teknologi Informasi, Magister (S2) Institut Teknologi Sepuluh Nopember : Jaringan Cerdas Multimedia, Teknik Elektro`

### 20. Agus Fatulloh, S.T., M.T
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `107051`
- **Program Studi**: `Rekayasa Keamanan Siber` -> `Rekayasa Keamanan Siber`
- **Bidang Keahlian**: `Computer Organization and Architecture, Operating System, Networking, Hardware Technology, Software Development, Social Computing` -> `Computer Organization and Architecture, Operating System, Networking and Hardware Technology, Computer Engineering, Software Applications Development, Social Computing`
- **Pendidikan**: `S1 STST Indonesia Bandung - Teknik Informatika; S2 ITB - Teknik Elektro` -> `Sarjana (S1) Sekolah Tinggi Sains dan Teknologi Indonesia Bandung : Teknik Informatika, Magister (S2) Institut Teknologi Bandung : Teknik Elektro`

### 21. Condra Antoni, SS., M.A
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `107054`
- **Program Studi**: `Teknik Informatika` -> `Teknik Informatika`
- **Bidang Keahlian**: `Linguistic` -> `Linguistic`
- **Pendidikan**: `S1 Universitas Andalas - Sastra Inggris; S2 Radboud University - Linguistic` -> `Sarjana (S1) Universitas Andalas : Sastra Inggris, Magister (S2) Radboud University : Linguistic`

### 22. Mira Chandra Kirana, S.T., M.T
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `109064`
- **Program Studi**: `Teknik Informatika` -> `Teknik Informatika`
- **Bidang Keahlian**: `Biomedical Engineering, Image Processing, Intelligent System` -> `Biomedical Engineering, Image Processing, Intelligent System`
- **Pendidikan**: `S1 ITS - Teknik Elektro; S2 ITS - Teknik Elektro` -> `Sarjana (S1) Institut Teknologi Sepuluh Nopember : Teknik Elektro, Magister (S2) Institut Teknologi Sepuluh Nopember : Teknik Elektro`

### 23. Gendhy Dwi Harlyan, S.Sn., M.Sn
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `112086`
- **Program Studi**: `Animasi` -> `Animasi`
- **Bidang Keahlian**: `Audio Visual` -> `Audio Visual`
- **Pendidikan**: `S1 Universitas Negeri Malang - Desain Komunikasi Visual; S2 Institut Kesenian Jakarta - Pengkajian Seni` -> `Sarjana (S1) Universitas Negeri Malang : Desain Komunikasi Visual, Magister (S2) Institut Kesenian Jakarta : Pengkajian Seni`

### 24. Nur Zahrati Janah, S.Kom., M.Sc
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `112087`
- **Program Studi**: `Teknik Informatika` -> `Teknik Informatika`
- **Bidang Keahlian**: `Software Development, Machine Learning, Image Processing` -> `Software Development, Machine Learning, Image Processing`
- **Pendidikan**: `S1 Universitas Gadjah Mada - Ilmu Komputer; S2 Universiti Teknologi PETRONAS - Information Technology` -> `Sarjana (S1) Universitas Gajah Mada : Ilmu Komputer, Magister (S2) Universiti Teknologi PETRONAS, Malaysia : Information Technology`

### 25. Dwi Ely Kurniawan, S.Pd., M.Kom
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `112094`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Information System, Mobile Programming, Computer Network, Multimedia Learning` -> `Information System, Mobile Programming, Computer Network, Multimedia Learning`
- **Pendidikan**: `S1 Universitas Pendidikan Indonesia - Pendidikan Ilmu Komputer; S2 Universitas Diponegoro - Sistem Informasi; PSPPI Politeknik Negeri Batam` -> `Sarjana (S1) Universitas Pendidikan Indonesia : Pendidikan Ilmu Komputer, Magister (S2) Universitas Diponegoro : Sistem Informasi, PSPPI Politeknik Negeri Batam`

### 26. Maria, S.ST., M.Sn
- **Metode Match**: Name Similarity (71%)
- **NIDN**: `` -> `113103`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Multimedia Technology and Animation` -> `Multimedia Technology, Animation`
- **Pendidikan**: `DIV ITB - Teknologi Media Digital; S2 Institut Seni Indonesia - Tata Kelola Seni` -> `Sarjana Terapan (DIV) Institut Teknologi Bandung : Teknologi Media Digital, Magister (S2) Institut Seni Indonesia : Tata Kelola Seni`

### 27. Selly Artaty Zega, S.ST., M.Sc
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `113104`
- **Program Studi**: `Animasi` -> `Animasi`
- **Bidang Keahlian**: `Digital Media Technology` -> `Digital Media Technology`
- **Pendidikan**: `DIV ITB - Desain Komunikasi Visual Animasi; S2 Nanyang Technological University` -> `Sarjana Terapan (DIV) Institut Teknologi Bandung : Desain Komunikasi Visual - Animasi, Magister (S2) Nanyang Technological University`

### 28. Sandi Prasetyaningsih, S.ST., M.Media
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `113106`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Media dan Komunikasi` -> `Media dan Komunikasi`
- **Pendidikan**: `DIV ITB - Desain Komunikasi Visual Animasi; S2 RMIT University - Master of Media` -> `Sarjana Terapan (DIV) Institut Teknologi Bandung : Desain Komunikasi Visual - Animasi, Magister (S2) RMIT University : Master of Media`

### 29. Sudra Irawan, S.Pd.Si., M.Sc
- **Metode Match**: Name Similarity (88%)
- **NIDN**: `` -> `113110`
- **Program Studi**: `Teknologi Geomatika` -> `Teknologi Geomatika`
- **Bidang Keahlian**: `Geoscience, Geophysics, Hydro-oceanography, Geology, GIS` -> `Geoscience, Geophysics, Hydro-oceanography, Geology, GIS`
- **Pendidikan**: `S1 Universitas Negeri Yogyakarta - Pendidikan Fisika; S2 Universitas Gadjah Mada - Fisika` -> `Sarjana (S1) Universitas Negeri Yogyakarta : Pendidikan Fisika, Magister (S2) Universitas Gadjah Mada : Fisika`

### 30. Sartikha, S. ST., M.Eng
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `113115`
- **Program Studi**: `Teknik Informatika` -> `Teknik Informatika`
- **Bidang Keahlian**: `Database Engineering, Software Engineering, Optimization` -> `Database Engineering, Software Engineering, Optimization`
- **Pendidikan**: `DIV ITB - Teknik Media Digital; S2 Universitas Gadjah Mada - Teknologi Informasi` -> `Sarjana Terapan (DIV) Institut Teknologi Bandung : Teknik Media Digital, Magister (S2) Universitas Gadjah Mada : Teknologi Informasi`

### 31. Arta Uly Siahaan, S.Pd, M.Pd
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `114131`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Pendidikan Bahasa Inggris` -> `Pendidikan Bahasa Inggris`
- **Pendidikan**: `S1 Univ HKBP Nommensen - Pendidikan Bahasa Inggris; S2 Universitas Negeri Malang - Pendidikan Bahasa Inggris` -> `Sarjana (S1) Univ HKBP Nommensen : Pendidikan Bahasa Inggris, Magister (S2) Universitas Negeri Malang : Pendidikan Bahasa Inggris`

### 32. Oktavianto Gustin, S.T., M.T
- **Metode Match**: Name Similarity (89%)
- **NIDN**: `` -> `115138`
- **Program Studi**: `Teknologi Geomatika` -> `Teknologi Geomatika`
- **Bidang Keahlian**: `GNSS, Remote Sensing, Engineering Survey` -> `GNSS, Remote Sensing, Engineering Survey`
- **Pendidikan**: `S1 ITS - Teknologi Geomatika; S2 ITS - Teknologi Geomatika; PSPPI ITB` -> `Sarjana (S1) Institut Teknologi Sepuluh Nopember Surabaya : Teknologi Geomatika, Magister (S2) Institut Teknologi Sepuluh Nopember Surabaya : Teknologi Geomatika, PSPPI Institut Teknologi Bandung`

### 33. Nelmiawati, B.CS., M.Comp.Sc
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `115148`
- **Program Studi**: `Rekayasa Keamanan Siber` -> `Rekayasa Keamanan Siber`
- **Bidang Keahlian**: `Computer Network, Information Security, Computer Science` -> `Computer Network, Information Security, Computer Science`
- **Pendidikan**: `S1 Universiti Teknologi Malaysia - Computer Network and Security; S2 Universiti Teknologi Malaysia - Information Security` -> `Sarjana (S1) Universiti Teknologi Malaysia : Computer Network and Security, Magister (S2) Universiti Teknologi Malaysia : Information Security`

### 34. Muhammad Zainuddin Lubis, S.I.k, M.Si
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `116162`
- **Program Studi**: `Teknologi Geomatika` -> `Teknologi Geomatika`
- **Bidang Keahlian**: `Hydrographic Survey, Physical Oceanography, Underwater Acoustic, Marine GIS` -> `Hydrographic Survey, Physical Oceanography, Underwater Acoustic, Marine GIS`
- **Pendidikan**: `S1 IPB University - Ilmu dan Teknologi Kelautan; S2 IPB University - Teknologi Kelautan` -> `Sarjana (S1) IPB University : Ilmu dan Teknologi Kelautan, Magister (S2) IPB University : Teknologi Kelautan`

### 35. Wenang Anurogo, S.Si., M.Sc.
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `116163`
- **Program Studi**: `Teknologi Geomatika` -> `Teknologi Geomatika`
- **Bidang Keahlian**: `Computer Network, Information Security, Computer Science` -> `Computer Network, Information Security, Computer Science`
- **Pendidikan**: `S1 Universitas Gadjah Mada - Geografi/Kartografi dan Penginderaan Jauh; S2 Universitas Gadjah Mada - Magister Pengelolaan Pesisir dan DAS` -> `Sarjana (S1) Universitas Gadjah Mada : Geografi/Kartografi dan Penginderaan Jauh, Magister (S2) Gadjah Mada : Geografi/Magister Pengelolaan Pesisir dan Daerah Aliran Sungai (MPPDAS)`

### 36. Muchamad Fajri Amirul Nasrullah, S.ST., M.Sc
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `117173`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Video Coding, Video Effect, Mobile Application` -> `Video Coding, Video Effect, Mobile Application`
- **Pendidikan**: `DIV Politeknik Elektronik Negeri Surabaya - Teknik Telekomunikasi; S2 National Taipei University of Technology - Electrical Engineering and Computer Science` -> `Sarjana Terapan (DIV) Politeknik Elektronik Negeri Surabaya : Teknik Telekomunikasi, Magister (S2) National Taipei University Of Technology : Electrical Engineering and Computer Science`

### 37. Hamdani Arif, S.Pd., M.Sc
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `117175`
- **Program Studi**: `Rekayasa Keamanan Siber` -> `Rekayasa Keamanan Siber`
- **Bidang Keahlian**: `Networking, IoT` -> `Networking, IoT`
- **Pendidikan**: `S1 Universitas Negeri Malang - Teknik Informatika; S2 Chang Gung University - Computer Science & Information Engineering` -> `Sarjana (S1) Univ. Negeri Malang : Teknik Informatika, Magister (S2) Chang Gung University : Computer Science & Information Engineering`

### 38. Luthfiya Ratna Sari, S.Si., M.T.
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `117196`
- **Program Studi**: `Teknologi Geomatika` -> `Teknologi Geomatika`
- **Bidang Keahlian**: `Aplikasi Sistem Informasi Geografis, Penginderaan Jauh, Kartografi` -> `Aplikasi Sistem Informasi Geografis, Penginderaan Jauh, Kartografi`
- **Pendidikan**: `S1 Universitas Gadjah Mada - Kartografi dan Penginderaan Jauh; S2 ITB - Teknik Geodesi dan Geomatika; PSPPI Politeknik Negeri Batam` -> `Sarjana (S1) Universitas Gadjah Mada : Kartografi dan Penginderaan Jauh, Magister (S2) Institut Teknologi Bandung : Teknik Geodesi dan Geomatika, PSPPI Politeknik Negeri Batam`

### 39. Rina Yulius, S.Pd., M.Eng
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `118199`
- **Program Studi**: `Teknik Informatika` -> `Teknik Informatika`
- **Bidang Keahlian**: `E-Learning, Human Computer Interaction, Gamification` -> `E-Learning, Human Computer Interaction, Gamification`
- **Pendidikan**: `S1 Universitas Negeri Padang - Pendidikan Teknik Informatika dan Komputer; S2 Universitas Gadjah Mada - Teknik Elektro` -> `Sarjana (S1) Universitas Negeri Padang : Pendidikan Teknik Informatika dan Komputer, Magister (S2) Universitas Gajah Mada : Teknik Elektro`

### 40. Satriya Bayu Aji, S.S., M.Hum.
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `118201`
- **Program Studi**: `Teknologi Geomatika` -> `Teknologi Geomatika`
- **Bidang Keahlian**: `Bahasa Inggris` -> `Bahasa Inggris`
- **Pendidikan**: `S1 Universitas Terbuka - Sastra Inggris (Penerjemahan); S2 Universitas Sebelas Maret - Ilmu Linguistik` -> `Sarjana (S1) Universitas Terbuka : Sastra Inggris Bidang Minat Penerjemahan, Magister (S2) Universitas Sebelas Maret : Ilmu Linguistik`

### 41. Siti Noor Chayati, S.T., M.Sc
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `118207`
- **Program Studi**: `Teknologi Geomatika` -> `Teknologi Geomatika`
- **Bidang Keahlian**: `Hydrographic Surveying` -> `Hydrographic Surveying`
- **Pendidikan**: `S1 Universitas Gadjah Mada - Teknik Geodesi; S2 University College London - Hydrographic Surveying` -> `Sarjana (S1) Universitas Gadjah Mada : Teknik Geodesi, Magister (S2) University College London : Hydrographic Surveying`

### 42. Agung Riyadi, S.Si., M.Kom
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `119221`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Artificial Intelligence` -> `Artificial Intelligence`
- **Pendidikan**: `S1 Universitas Negeri Jakarta - Fisika; S2 Universitas Budi Luhur - Ilmu Komputer` -> `Sarjana (S1) Universitas Negeri Jakarta : Fisika, Magister (S2) Universitas Budiluhur : Ilmu Komputer`

### 43. Dodi Prima Resda, S.Pd., M.Kom
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `119222`
- **Program Studi**: `Rekayasa Keamanan Siber` -> `Rekayasa Keamanan Siber`
- **Bidang Keahlian**: `Teknik Informatika, Rekayasa Keamanan Siber` -> `Teknik Informatika, Rekayasa Keamanan Siber`
- **Pendidikan**: `S1 Universitas Negeri Padang - Pendidikan Teknik Elektro; S2 Universitas Putra Indonesia YPTK - Teknik Informatika` -> `Sarjana (S1) Universitas Negeri Padang : Pendidikan Teknik Elektro, Magister (S2) Universitas Putra Indonesia YPTK : Teknik Informatika`

### 44. Fadli Suandi, S.T., M.Kom.
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `119223`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Human Computer Interaction, Photography, Multimedia` -> `Human Computer Interaction, Photography, Multimedia`
- **Pendidikan**: `S1 UIN Sultan Syarif Kasim - Teknik Informatika; S2 Universitas Islam Indonesia - Teknik Informatika` -> `Sarjana (S1) Universitas Islam Negeri Sultan Syarif Kasim : Teknik Informatika, Magister (S2) Universitas Islam Indonesia : Teknik Informatika`

### 45. Swono Sibagariang, S.Kom., M.Kom
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `119224`
- **Program Studi**: `Teknik Informatika` -> `Teknik Informatika`
- **Bidang Keahlian**: `Software Development` -> `Software Development`
- **Pendidikan**: `S1 Univ Katolik Santo Thomas Sumatera Utara - Teknik Informatika; S2 Universitas Sumatera Utara - Ilmu dan Teknologi` -> `Sarjana (S1) Univ Khatolik Santo Thomas Sumatera Utara : Teknik Informatika, Magister (S2) Universitas Sumatera Utara : Ilmu dan Teknologi`

### 46. Siskha Handayani, S.Si., M.Si
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `121246`
- **Program Studi**: `Teknik Informatika` -> `Teknik Informatika`
- **Bidang Keahlian**: `Matematika` -> `Matematika`
- **Pendidikan**: `S1 Universitas Andalas - Matematika; S2 Universitas Andalas - Matematika` -> `Sarjana (S1) Universitas Andalas : Matematika, Magister (S2) Universitas Andalas : Matematika`

### 47. Dwi Amalia Purnamasari, S.T., M.Cs
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `121248`
- **Program Studi**: `Teknik Informatika` -> `Teknik Informatika`
- **Bidang Keahlian**: `Software Development, Supply Chain Management, Forecasting` -> `Software Development, Supply Chain Management, Forecasting`
- **Pendidikan**: `S1 Universitas Maritim Raja Ali Haji - Teknik Informatika; S2 Universitas Gadjah Mada - Ilmu Komputer` -> `Sarjana (S1) Universitas Maritim Raja Ali Haji : Teknik Informatika, Magister (S2) Universitas Gadjah Mada : Ilmu Komputer`

### 48. Rini Amadia, S.Sn., M.Sn
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `122256`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Desain Komunikasi Visual` -> `Desain Komunikasi Visual`
- **Pendidikan**: `S1 Institut Seni Indonesia Padangpanjang; S2 Institut Seni Indonesia Padangpanjang` -> `Sarjana (S1) Institut Seni Indonesia Padangpanjang, Magister (S2) Institut Seni Indonesia Padangpanjang`

### 49. Aragani Timur Kanistren, S.Sn., M.Sn
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `122258`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Naskah Produksi, Ide Kreatif, Broadcasting` -> `Naskah Produksi, Ide Kreatif, Broadcasting`
- **Pendidikan**: `S1 Institut Seni Indonesia - Fakultas Seni Media Rekam (Televisi); S2 ISI Yogyakarta - Videografi` -> `Sarjana (S1) Institut Seni Indonesia : Fakultas Seni Media Rekam, Jurusan Televisi, Magister (S2) Pascasarjana ISI Yogyakarta : Fakultas Seni Media Rekam, Jurusan Videografi`

### 50. Anis Rahmi, S.Tr. Kom., M.Sn
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `122259`
- **Program Studi**: `Animasi` -> `Animasi`
- **Bidang Keahlian**: `2D Skeletal Animation, 3D Animation Workflow (Rigging, Lighting, Render, Compositing), Object-oriented Computer Animation` -> `2D Skeletal Animation, 3D Animation Workflow, Rigging, Lighting, Render & Compositing, Object-Oriented Computer Animation`
- **Pendidikan**: `DIV Politeknik Negeri Batam - Teknik Multimedia dan Jaringan; S2 ISI Yogyakarta - Animasi` -> `Sarjana Terapan (DIV) Politeknik Negeri Batam : Teknik Multimedia dan Jaringan, Magister (S2) Institut Seni Indonesia Yogyakarta : Penciptaan Seni Media Rekam (Animasi)`

### 51. Feby, M.Pd
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `122270`
- **Program Studi**: `Animasi` -> `Animasi`
- **Bidang Keahlian**: `Bahasa Inggris` -> `Bahasa Inggris`
- **Pendidikan**: `S1 Universitas Bung Hatta - Pendidikan Bahasa Inggris; S2 Universitas Negeri Padang - Pendidikan Bahasa Inggris` -> `Sarjana (S1) Universitas Bung Hatta : Pendidikan Bahasa Inggris, Magister (S2) Universitas Negeri Padang : Pendidikan Bahasa Inggris`

### 52. Ahmadi Irmansyah Lubis, S.kom., M.kom.
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `122275`
- **Program Studi**: `Teknologi Rekayasa Perangkat Lunak` -> `Teknologi Rekayasa Perangkat Lunak`
- **Bidang Keahlian**: `Artificial Intelligence, Decision Support System, Machine Learning, Computer Science` -> `Artificial Intelligence, Decision Support System, Machine Learning, Computer Science`
- **Pendidikan**: `S1 Universitas Sumatera Utara - Teknologi Informasi; S2 Universitas Sumatera Utara - Teknik Informatika` -> `Sarjana (S1) Universitas Sumatera Utara : Teknologi Informasi, Magister (S2) Universitas Sumatera Utara : Teknik Informatika`

### 53. Antoni Haikal, S.ST.,M.T
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `122276`
- **Program Studi**: `Rekayasa Keamanan Siber` -> `Rekayasa Keamanan Siber`
- **Bidang Keahlian**: `Application Security, Software Development, Offensive Security` -> `Application Security, Software Development, Offensive Security`
- **Pendidikan**: `D4 Institut Teknologi Bandung; S2 Institut Teknologi Bandung - Elektro` -> `Sarjana Terapan (D4) Institut Teknologi Bandung, Magister (S2) Institut Teknologi Bandung : Elektro`

### 54. Noper Ardi, S.Pd., M.Eng
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `122277`
- **Program Studi**: `Teknologi Rekayasa Perangkat Lunak` -> `Teknologi Rekayasa Perangkat Lunak`
- **Bidang Keahlian**: `RPL, AI` -> `RPL, AI`
- **Pendidikan**: `S1 Universitas Negeri Padang - Pendidikan Teknik Informatika dan Komputer; S2 Universitas Gadjah Mada - Teknologi Informasi` -> `Sarjana (S1) Universitas Negeri Padang : Pendidikan Teknik Informatika dan Komputer, Magister (S2) Universitas Gadjah Mada : Teknologi Informasi`

### 55. Alena Uperiati, S.T, M.Cs
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `122279`
- **Program Studi**: `Teknologi Rekayasa Perangkat Lunak` -> `Teknologi Rekayasa Perangkat Lunak`
- **Bidang Keahlian**: `Machine Learning, Data Science, Software Development` -> `Machine Learning, Data Science, Software Development`
- **Pendidikan**: `S1 Universitas Maritim Raja Ali Haji - Teknik Informatika; S2 Universitas Gadjah Mada - Ilmu Komputer` -> `Sarjana (S1) Universitas Maritim Raja Ali Haji : Teknik Informatika, Magister (S2) Universitas Gadjah Mada : Ilmu Komputer`

### 56. Amirul Mu’minin, S.Ds., M.Ds.
- **Metode Match**: Name Similarity (96%)
- **NIDN**: `` -> `122280`
- **Program Studi**: `Animasi` -> `Animasi`
- **Bidang Keahlian**: `Desain Grafis, Game Design, Visual Effect` -> `Desain Grafis, Game Desain, Visual Effect`
- **Pendidikan**: `S1 Universitas Negeri Makassar - Desain Komunikasi Visual; S2 Institut Teknologi Bandung - Magister Desain` -> `Sarjana (S1) Universitas Negeri Makassar : Desain Komunikasi Visual, Magister (S2) Institut Teknologi Bandung : Magister Desain`

### 57. Cahya Miranto, S.S.T., M.Tr.Kom.
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `122282`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Animasi 3D` -> `Animasi 3D`
- **Pendidikan**: `DIV Politeknik Negeri Batam - Multimedia & Jaringan; S2 PENS - Teknik Informatika dan Komputer` -> `Sarjana Terapan (DIV) Politeknik Negeri Batam : Multimedia & Jaringan, Magister (S2) PENS : Teknik Informatika dan Komputer`

### 58. Muhammad Idris S.Tr
- **Metode Match**: Name Similarity (84%)
- **NIDN**: `` -> `122283`
- **Program Studi**: `Teknik Informatika` -> `Teknik Informatika`
- **Bidang Keahlian**: `Software Development, QA Software, Web Security` -> `Software Development, QA Software, Security`
- **Pendidikan**: `DIV Politeknik Negeri Batam - Multimedia & Jaringan; S2 PENS - Teknik Informatika dan Komputer` -> `Sarjana Terapan (DIV) Politeknik Negeri Batam : Multimedia & Jaringan, Magister (S2) PENS : Teknik Informatika dan Komputer`

### 59. Ardiman Firmanda, S.S.T., M.Tr.Kom.
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `122284`
- **Program Studi**: `Teknologi Permainan` -> `Teknologi Permainan`
- **Bidang Keahlian**: `Musik` -> `Musik`
- **Pendidikan**: `DIV Politeknik Negeri Batam - Multimedia & Jaringan; S2 PENS - Teknik Informatika dan Komputer` -> `Sarjana Terapan (DIV) Politeknik Negeri Batam : Multimedia & Jaringan, Magister (S2) PENS : Teknik Informatika dan Komputer`

### 60. Chairoel Adam S.Ds., M.Sn.
- **Metode Match**: Name Similarity (72%)
- **NIDN**: `` -> `123298`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Penciptaan Seni, Desain Komunikasi Visual` -> `Penciptaan Seni`
- **Pendidikan**: `S1 Universitas Negeri Padang - Desain Komunikasi Visual; S2 Institut Seni Indonesia Yogyakarta - Penciptaan Seni` -> `Sarjana (S1) Universitas Negeri Padang : Desain Komunikasi Visual, Magister (S2) Institut Seni Indonesia Yogyakarta : Penciptaan Seni`

### 61. Suwarno, S.S., M.Pd
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `124300`
- **Program Studi**: `Teknologi Rekayasa Perangkat Lunak` -> `Teknik Rekayasa Perangkat Lunak`
- **Bidang Keahlian**: `Systemic Functional Linguistics, Computational Linguistics` -> `Systemic Functional Linguistics, Computational Linguistics`
- **Pendidikan**: `S1 Universitas Putera Batam; S2 Universitas Negeri Yogyakarta` -> `Sarjana (S1) Universitas Putera Batam, Magister (S2) Universitas Negeri Yogyakarta`

### 62. Nursaimah Harhap
- **Metode Match**: Name Similarity (93%)
- **NIDN**: `` -> `124302`
- **Program Studi**: `Teknologi Permainan` -> `Teknologi Permainan`
- **Bidang Keahlian**: `Bahasa Inggris` -> `Bahasa Inggris`
- **Pendidikan**: `S1 Universitas Graha Nusantara - Pendidikan Bahasa Inggris; S2 Universitas Negeri Medan - Linguistik Terapan Bahasa Inggris` -> `Sarjana (S1) Universitas Graha Nusantara : Pendidikan Bahasa Inggris, Magister (S2) Universitas Negeri Medan : Linguistik Terapan Bahasa Inggris`

### 63. Rusyda Nazhirha
- **Metode Match**: Name Similarity (77%)
- **NIDN**: `` -> `124307`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Linguistik Terapan, Wacana Digital, Teks Multimodal, Bahasa Indonesia` -> `Linguistik Terapan, Wacana Digital, Teks Multimodal, Bahasa Indonesia`
- **Pendidikan**: `S1 Universitas Negeri Medan - Sastra Indonesia; S2 Universitas Sumatera Utara - Linguistik` -> `Sarjana (S1) Universitas Negeri Medan : Sastra Indonesia, Magister (S2) Universitas Sumatera Utara : Linguistik`

### 64. Berliansyah Ramadhan
- **Metode Match**: Name Similarity (85%)
- **NIDN**: `` -> `124313`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Musik` -> `Musik`
- **Pendidikan**: `S1 Universitas PGRI Palembang - Pendidikan Sendratasik; S2 Institut Seni Indonesia Padangpanjang - Pengkajian dan Penciptaan Seni` -> `Sarjana (S1) Universitas PGRI Palembang : Pendidikan Sendratasik, Magister (S2) Institut Seni Indonesia Padangpanjang : Pengkajian dan Penciptaan Seni`

### 65. Luki Aswar M.Pd.
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `124316`
- **Program Studi**: `Teknik Informatika` -> `Teknik Informatika`
- **Bidang Keahlian**: `Pendidikan Bahasa Indonesia` -> `Pendidikan Bahasa Indonesia`
- **Pendidikan**: `S1 Universitas Riau - Pendidikan Bahasa dan Sastra Indonesia; S2 Universitas Negeri Padang - Pendidikan Bahasa dan Sastra Indonesia` -> `Sarjana (S1) Universitas Riau : Pendidikan Bahasa dan Sastra Indonesia, Magister (S2) Universitas Negeri Padang : Pendidikan Bahasa dan Sastra Indonesia`

### 66. Fendra Dwi R
- **Metode Match**: Name Similarity (77%)
- **NIDN**: `` -> `124326`
- **Program Studi**: `Teknologi Geomatika` -> `Teknologi Geomatika`
- **Bidang Keahlian**: `Remote Sensing, GIS, Geoinformatics, GNSS, Photogrammetry` -> `Remote Sensing, Geographical Information System (GIS), Geoinformatics, GNSS, Photogrammetry`
- **Pendidikan**: `S1 Institut Teknologi Sepuluh Nopember - Teknik Geomatika; S2 Institut Teknologi Sepuluh Nopember - Teknik Geomatika` -> `Sarjana (S1) Institut Teknologi Sepuluh Nopember : Teknik Geomatika, Magister (S2) Institut Teknologi Sepuluh Nopember : Teknik Geomatika`

### 67. Cyntia Lasmi
- **Metode Match**: Name Similarity (75%)
- **NIDN**: `` -> `125331`
- **Program Studi**: `Teknik Informatika` -> `Teknik Informatika`
- **Bidang Keahlian**: `Artificial Intelligence, Data Mining` -> `Artificial Intelligence, Data Mining`
- **Pendidikan**: `S1 Universitas Putra Indonesia YPTK Padang - Teknik Informatika; S2 Universitas Putra Indonesia YPTK Padang - Teknik Informatika` -> `Sarjana (S1) Universitas Putra Indonesia 'YPTK' Padang : Teknik Informatika, Magister (S2) Universitas Putra Indonesia 'YPTK' Padang : Teknik Informatika`

### 68. Arif Rahman, M.T
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `125341`
- **Program Studi**: `Teknik Informatika` -> `Teknik Informatika`
- **Bidang Keahlian**: `Perencanaan Bangunan, AutoCAD` -> `Perencanaan Bangunan, AutoCad`
- **Pendidikan**: `S1 Universitas Negeri Padang - Teknik Sipil; S2 Universitas Andalas - Teknik Sipil` -> `Sarjana (S1) Universitas Negeri Padang : Teknik Sipil, Magister (S2) Universitas Andalas : Teknik Sipil`

### 69. Holong Marisi Simalango, M.Kom.
- **Metode Match**: Name Similarity (90%)
- **NIDN**: `` -> `125346`
- **Program Studi**: `Teknologi Rekayasa Perangkat Lunak` -> `Teknologi Rekayasa Perangkat Lunak`
- **Bidang Keahlian**: `Software Engineering, IoT, AI, Game Development` -> `Software Engineering, IoT, AI, Game Development`
- **Pendidikan**: `DIII Politeknik Pos Indonesia; S1 STMIK LIKMI; S2 STMIK LIKMI` -> `Diploma (DIII) Politeknik Pos Indonesia, Sarjana (S1) STMIK LIKMIK, Magister (S2) STMIK LIKMI`

### 70. Kawan Pandiangan, S.Sn.,M.Sn
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `125350`
- **Program Studi**: `Teknologi Rekayasa Multimedia` -> `Teknologi Rekayasa Multimedia`
- **Bidang Keahlian**: `Music, Ethnomusicology, Performing Arts` -> `Music, Ethnomusicology, Performing Arts`
- **Pendidikan**: `S1 Universitas Sumatera Utara - Etnomusikologi; S2 Universitas Sumatera Utara - Penciptaan dan Pengkajian Seni` -> `Sarjana (S1) Universitas Sumatera Utara : Etnomusikologi, Magister (S2) Universitas Sumatera Utara : Penciptaan dan Pengkajian Seni`

### 71. Nadya Satya Handayani, M.Kom
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `125351`
- **Program Studi**: `Teknik Informatika` -> `Teknik Informatika`
- **Bidang Keahlian**: `Biomedical, Artificial Intelligence` -> `Biomedical, AI`
- **Pendidikan**: `S1 STMIK Amik Riau - Teknik Informatika; S2 Universitas Islam Indonesia - Informatika` -> `Sarjana (S1) STMIK Amik Riau : Teknik Informatika, Magister (S2) Universitas Islam Indonesia : Informatika`

### 72. Nur Israyani, S.T, M.T
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `125352`
- **Program Studi**: `Teknologi Geomatika` -> `Teknologi Geomatika`
- **Bidang Keahlian**: `Geographical Information System (GIS)` -> `Geographical Information System (GIS)`
- **Pendidikan**: `S1 Universitas Muslim Indonesia - Teknik Sipil; S2 Universitas Hasanuddin - Teknik Sipil` -> `Sarjana (S1) Universitas Muslim Indonesia : Teknik Sipil, Magister (S2) Universitas Hasanuddin : Teknik Sipil`

### 73. Recy Harviani Zurwanty, S.Pd., M.Pd
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `125355`
- **Program Studi**: `Teknologi Rekayasa Perangkat Lunak` -> `Teknologi Rekayasa Perangkat Lunak`
- **Bidang Keahlian**: `Pendidikan Pancasila, Pendidikan Kewarganegaraan` -> `Pendidikan Pancasila, Pendidikan Kewarganegaraan`
- **Pendidikan**: `S1 Universitas Negeri Padang - Pendidikan Pancasila dan Kewarganegaraan; S2 Universitas Negeri Padang - Pendidikan Pancasila dan Kewarganegaraan` -> `Sarjana (S1) Universitas Negeri Padang : Pendidikan Pancasila dan Kewarganegaraan, Magister (S2) Universitas Negeri Padang : Pendidikan Pancasila dan Kewarganegaraan`

### 74. Sri Rahayu, M.Pd
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `125359`
- **Program Studi**: `Teknologi Rekayasa Perangkat Lunak` -> `Teknologi Rekayasa Perangkat Lunak`
- **Bidang Keahlian**: `Pendidikan Pancasila, Pendidikan Kewarganegaraan` -> `Pendidikan Pancasila, Pendidikan Kewarganegaraan (Civics Education)`
- **Pendidikan**: `S1 Universitas Pendidikan Indonesia - Pendidikan Pancasila dan Kewarganegaraan; S2 Universitas Pendidikan Indonesia - Pendidikan Kewarganegaraan` -> `Sarjana (S1) Universitas Pendidikan Indonesia : Pendidikan Pancasila dan Kewarganegaraan, Magister (S2) Universitas Pendidikan Indonesia : Pendidikan Kewarganegaraan`

### 75. Sukma Evadini, S.T., M.Kom
- **Metode Match**: Name Similarity (100%)
- **NIDN**: `` -> `125360`
- **Program Studi**: `Teknologi Rekayasa Perangkat Lunak` -> `Teknologi Rekayasa Perangkat Lunak`
- **Bidang Keahlian**: `Data Mining, Machine Learning, Computer Graphics, Expert System` -> `Data Mining, Expert System, Machine Learning`
- **Pendidikan**: `S1 Universitas Indonesia - Ilmu Komputer; S2 Universitas Indonesia - Ilmu Komputer` -> `Sarjana (S1) Universitas Islam Negeri Sultan Syarif Kasim Riau : Teknik Informatika, Magister (S2) Universitas Putra Indonesia YPTK Padang : Teknik Informatika`

## 4. Data Scrap Baru (Belum ada di DB)

Berikut data dosen baru dari hasil scrap yang dapat di-insert ke DB:

| No | Nama | NIDN | Program Studi | Bidang Spesialis |
|---|---|---|---|---|
| 1 | Riki, S.Tr., M.F.A | 124329 | Animasi | Animasi, Illustrasi |
| 2 | Yusuf Rizky Nur C. S. Sn. M.A | 123289 | Teknologi Rekayasa Multimedia | Seni Musik, Etnomusikologi, Budaya, Composer & Arrangement Musik |
| 3 | Ummul Fitri Afifah, S.Kom.,M.MSI. | 125330 | Teknik Informatika | IT Governance, AI |
