# DC-DC Synchronous Buck Converter Design

Bu repository, MIT 6.622 tasarım projesi gereksinimlerinden yola çıkarak hazırlanmış bir **senkron buck converter** çalışmasını GitHub üzerinde okunabilir hale getirir. Proje; güç katı seçimi, frekans yerleşimi, küçük işaret modeli, PID/Type-3 kompanzasyon, op-amp ile gerçekleme ve LTspice doğrulamalarını tek bir teknik akışta toplar.

Tam teknik içerik README içinde özetlenmez; hesap adımları, denklemler, figürler ve benzetim ekran görüntüleri [docs/full-report.md](docs/full-report.md) içinde tutulur. Bu sayfa, projeye hızlı giriş ve güvenilir navigasyon noktasıdır.

## Hızlı Bağlantılar

| İçerik | Bağlantı |
|---|---|
| Tam teknik rapor | [docs/full-report.md](docs/full-report.md) |
| Dokümantasyon giriş sayfası | [docs/index.md](docs/index.md) |
| Doğrulama özeti | [docs/verification-summary.md](docs/verification-summary.md) |
| Kaynak bölüm / görsel haritası | [docs/source-map.md](docs/source-map.md) |
| Dönüşüm kalite raporu | [docs/TRANSFER_AUDIT.md](docs/TRANSFER_AUDIT.md) |
| Son kalite kontrol | [FINAL_QA.md](FINAL_QA.md) |
| Ana DOCX kaynak belge | [Birinci_donem_Buck_Converter_Serbest_Projesi.docx](Birinci_donem_Buck_Converter_Serbest_Projesi.docx) |
| Ana PDF rapor | [Birinci_donem_Buck_Converter_Serbest_Projesi.pdf](Birinci_donem_Buck_Converter_Serbest_Projesi.pdf) |
| LTspice çalışma klasörü | [LTspice_AveragedSwitchModelingSimulation/](LTspice_AveragedSwitchModelingSimulation/) |

## Tasarımın Kısa Tanımı

Tasarım hedefi, $24-36\,\text{V}$ giriş aralığından $14\,\text{V}$ regüle çıkış üreten ve yaklaşık $50-125\,\text{W}$ güç aralığında çalışan bir senkron alçaltıcı dönüştürücü kurmaktır. Çalışmada güç katı parametreleri kontrol tasarımından ayrı düşünülmez; $L$, $C$, ESR, anahtarlama frekansı, crossover hedefi ve kompanzasyon eğrisi birlikte ele alınır.

Kontrol tarafında sensör kazancı, control-to-output transfer fonksiyonu, uncompensated loop gain, lead/PD, lag/PI ve birleşik PID kompanzasyon adımları raporlanır. Nihai hedef yaklaşık $10\,\text{kHz}$ crossover ve yaklaşık $53-55^\circ$ phase margin ile pratik op-amp frekans kısıtını birlikte sağlamaktır.

## Temel Tasarım Spesifikasyonları

| Gereksinim | Hedef |
|---|---:|
| Giriş gerilimi | $24-36\,\text{V}$ |
| Giriş transient limiti | $44\,\text{V}$, en çok $1\,\text{ms}$ |
| Çıkış gücü | $50-125\,\text{W}$ |
| Statik çıkış gerilimi | $14\,\text{V}\pm3\%$ |
| Transient çıkış gerilimi | $14\,\text{V}\pm20\%$ |
| İzin verilen çıkış ripple | $100\,\text{mV}_{p-p}$ |
| İzin verilen giriş akımı ripple | $50\,\text{mA}_{p-p}$ |
| Minimum verim | $90\%$ |
| Ortam sıcaklığı | $-20^\circ\text{C}$ to $+50^\circ\text{C}$ |

## Öne Çıkan Teknik Seçimler

| Alan | Seçim / Sonuç |
|---|---|
| Anahtarlama frekansı | $f_s=100\,\text{kHz}$ |
| Crossover hedefi | Yaklaşık $10\,\text{kHz}$ |
| Referans gerilimi | $V_{ref}=1.8\,\text{V}$ |
| PWM ramp genliği | $V_m=4\,\text{V}$ |
| Sensör kazancı | $H\approx0.12857$ |
| Bobin | Yaklaşık $49.42\,\mu\text{H}$ |
| Çıkış sığacı | $82\,\mu\text{F}$ |
| Sığaç ESR | $19.39\,\text{m}\Omega$ |
| Sensor divider | $R_3=12.8\,\text{k}\Omega$, $R_5=87.2\,\text{k}\Omega$ |
| Compensator elemanları | $R_2=100\,\text{k}\Omega$, $R_1=21\,\text{k}\Omega$, $R_4=2.4\,\text{k}\Omega$, $C_2=1.59\,\text{nF}$, $C_4=2.2\,\text{nF}$ |

## Verification Özeti

| Kontrol | Raporlanan sonuç | Durum |
|---|---:|---|
| Çıkış gücü | Yaklaşık $49.5957-124.1839\,\text{W}$ | Geçti |
| Statik çıkış hatası | Yaklaşık $1.30\%$ | Geçti |
| Transient sapma | Yaklaşık $\pm8.58\%$ | Geçti |
| Çıkış ripple | Yaklaşık $37.38\,\text{mV}_{p-p}$ | Geçti |
| Verim | Yaklaşık $97.78\%$ | Geçti |
| Giriş transient, giriş ripple, sıcaklık sweep | Hedef olarak listelendi; ayrı görsel doğrulama yok | Takip gerekiyor |

Ayrıntılı tablo ve kanıt linkleri için [docs/verification-summary.md](docs/verification-summary.md) dosyasına bakın.

## Teknik Akış

| Bölüm | İçerik |
|---|---|
| [Abstract](docs/full-report.md#abstract) | Projenin kapsamı ve amaç özeti |
| [1. Giriş](docs/full-report.md#giris) | Problem tanımı ve buck converter arka planı |
| [2. Güç ve kontrol tasarım yöntemi](docs/full-report.md#guc-ve-kontrol-tasariminda-izlenen-yontem) | Frekans seçimi, $C R_{ESR}$ ve $CL$ kısıtları |
| [3. Güç katı hesaplamaları](docs/full-report.md#guc-kati-hesaplamalari) | Duty-cycle, bobin, sığaç, ESR ve RMS akım hesapları |
| [4. Durum denklemleri](docs/full-report.md#cevirici-durum-denklemleri) | ESR etkisi ve genel dalga biçimleri |
| [5. Kontrolcü tasarımı](docs/full-report.md#kontrolcu-tasarimi) | Küçük işaret modeli, Bode analizleri, lead/lag/PID kompanzasyon |
| [6. Op-amp gerçekleme](docs/full-report.md#op-amp-devresi-gerceklemesi) | Sensor gain ve compensator devresi eleman değerleri |
| [7. Benzetim sonuçları](docs/full-report.md#benzetim-sonuclari) | LTspice doğrulama görselleri ve gereksinim karşılaştırmaları |
| [8. Projenin geleceği](docs/full-report.md#projenin-gelecegi) | LM5146, giriş filtresi ve sonraki iterasyon notları |
| [Kaynaklar ve ekler](docs/full-report.md#kaynaklar) | Kullanılan kaynaklar, sığaç datasheet kesiti ve devre genel görünümü |

## Görsel Kanıtlar

**Sistem block diagramı**

![Sistem block diagramı](docs/assets/docx-media/media/image15.png)

**Nihai açık çevrim Bode diyagramı**

![Nihai açık çevrim Bode diyagramı](docs/assets/docx-media/media/image27.png)

**Transient çıkış davranışı**

![Transient çıkış gerilimi ve yük akımı](docs/assets/docx-media/media/image45.png)

**Çıkış ripple ölçümü**

![Çıkış ripple ölçümü](docs/assets/docx-media/media/image46.png)

## Simülasyon Dosyaları

LTspice kaynakları ve sonuç dosyaları [LTspice_AveragedSwitchModelingSimulation/](LTspice_AveragedSwitchModelingSimulation/) altında korunur. Buck converter çalışması için özellikle şu dosyalar önemlidir:

| Dosya | Rol |
|---|---|
| [SyncBuck_switching_CL.asc](LTspice_AveragedSwitchModelingSimulation/SyncBuck_switching_CL.asc) | Kapalı çevrim anahtarlamalı senkron buck devresi |
| [SyncBuck_average_CL.asc](LTspice_AveragedSwitchModelingSimulation/SyncBuck_average_CL.asc) | Ortalama model kapalı çevrim kontrol doğrulaması |
| [SyncBuck_average_fresponses.asc](LTspice_AveragedSwitchModelingSimulation/SyncBuck_average_fresponses.asc) | Frekans cevabı / loop-gain çalışmaları |
| [SyncBuck_average_parameters.asc](LTspice_AveragedSwitchModelingSimulation/SyncBuck_average_parameters.asc) | Parametre tabanlı ortalama model |
| [SyncBuck_average_Zout.asc](LTspice_AveragedSwitchModelingSimulation/SyncBuck_average_Zout.asc) | Çıkış empedansı çalışması |
| [PID_compensator.asc](LTspice_AveragedSwitchModelingSimulation/PID_compensator.asc) | PID/Type-3 compensator denemeleri |
| [average.lib](LTspice_AveragedSwitchModelingSimulation/average.lib) | Ortalama model kütüphanesi |
| [switching.lib](LTspice_AveragedSwitchModelingSimulation/switching.lib) | Anahtarlamalı model kütüphanesi |

Bu klasörde boost, flyback ve SEPIC eğitim örnekleri de vardır; ana proje kanıtı olarak buck isimli dosyalar ve raporda gömülü simülasyon görselleri esas alınır.

Not: `LTspice_AveragedSwitchModelingSimulation/SyncBuck_switching_CL.raw` yaklaşık 523 MB olduğu için GitHub repo commit’ine alınmadı. Dosya yerelde korunur; gerekirse harici bulut depolama veya GitHub Release asset olarak ayrıca paylaşılmalıdır.

## Kaynak ve Asset Yapısı

| Path | Açıklama |
|---|---|
| [docs/assets/docx-media/media/](docs/assets/docx-media/media/) | DOCX içinden çıkarılan ve rapora bağlanan medya |
| [docs/assets/docx-media/raw/](docs/assets/docx-media/raw/) | Ham DOCX medya kopyaları |
| [docs/originals/](docs/originals/) | Referans için kopyalanmış DOCX/PDF kaynakları |
| [images/readme/](images/readme/) | Önceki README için temiz adlandırılmış görseller; korunuyor |
| [images/docx_extracted/](images/docx_extracted/) | Eski kısmi DOCX medya çıkarımı; karşılaştırma için korunuyor |
| [orijinal ekran görüntüleri](ekran%20gor%C3%BCnt%C3%BCleri/) | Kaynak simülasyon ekran görüntüleri |
| [G5_mit6_622_s23_designproj.pdf](G5_mit6_622_s23_designproj.pdf) | MIT 6.622 proje şartnamesi |
| [G32_lm5146-q1.pdf](G32_lm5146-q1.pdf) | LM5146-Q1 datasheet |
| [G31_Robert_Erikson_fundamentals-of-power-electronics-3n_2020.pdf](G31_Robert_Erikson_fundamentals-of-power-electronics-3n_2020.pdf) | Power electronics reference/source material |

Üçüncü taraf PDF/TXT dosyaları repoda teknik referans materyali olarak durur; dağıtım/lisans uygunluğu ayrıca kontrol edilmelidir.

## Kapsam Notu

Bu çalışma birinci iterasyon niteliğindedir. Ana başarı kriterleri output-side regülasyon, ripple, transient davranış, verim ve kontrol tasarımıdır. Giriş transient dayanımı, giriş akımı ripple ve sıcaklık sweep gereksinimleri raporda hedef olarak listelenmiştir; ancak ayrı görsel doğrulamayla kapatılmamıştır. Bu açık noktalar [docs/verification-summary.md](docs/verification-summary.md) ve [docs/source-map.md](docs/source-map.md) içinde takip edilir.

## Source of Truth

Çelişki durumunda öncelik sırası:

1. [Birinci_donem_Buck_Converter_Serbest_Projesi.docx](Birinci_donem_Buck_Converter_Serbest_Projesi.docx)
2. Yereldeki görseller, simülasyon ekran görüntüleri ve LTspice dosyaları
3. Mevcut README ve yardımcı dokümantasyon

README bir landing page’dir; teknik kararlar için [docs/full-report.md](docs/full-report.md) ve kaynak DOCX esas alınmalıdır.
