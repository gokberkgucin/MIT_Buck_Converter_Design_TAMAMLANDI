# Documentation Index

Bu sayfa, repo içindeki uzun teknik rapora ve destek dosyalarına düzenli giriş noktasıdır. README hızlı landing page olarak kalır; ayrıntılı teknik içerik [full-report.md](full-report.md) içinde tutulur.

## Ana Dokümanlar

| Doküman | İçerik |
|---|---|
| [full-report.md](full-report.md) | Kaynak DOCX’ten taşınan tam teknik rapor |
| [verification-summary.md](verification-summary.md) | Tasarım gereksinimleri ve benzetim sonuçlarının kısa karşılaştırması |
| [source-map.md](source-map.md) | DOCX bölümleri, repo karşılıkları ve görsel kullanım haritası |
| [TRANSFER_AUDIT.md](TRANSFER_AUDIT.md) | DOCX aktarım hattının kalite/audit çıktısı |
| [../FINAL_QA.md](../FINAL_QA.md) | Landing page, docs ve link kalite kontrolü |
| [../REPO_AUDIT.md](../REPO_AUDIT.md) | Başlangıç repo audit notları |
| [../MIGRATION_PLAN.md](../MIGRATION_PLAN.md) | Dönüşüm planı ve source-of-truth kararı |

## Okuma Sırası

1. [Abstract](full-report.md#abstract)
2. [Güç ve kontrol tasarımında izlenen yöntem](full-report.md#guc-ve-kontrol-tasariminda-izlenen-yontem)
3. [Güç katı hesaplamaları](full-report.md#guc-kati-hesaplamalari)
4. [Kontrolcü tasarımı](full-report.md#kontrolcu-tasarimi)
5. [Op-amp devresi gerçekleştirmesi](full-report.md#op-amp-devresi-gerceklemesi)
6. [Benzetim sonuçları](full-report.md#benzetim-sonuclari)
7. [Verification summary](verification-summary.md)

## Rapor Bölümleri

| Bölüm | Bağlantı |
|---|---|
| Kapak / giriş | [full-report.md#kapak](full-report.md#kapak) |
| Abstract | [full-report.md#abstract](full-report.md#abstract) |
| İçindekiler | [full-report.md#icindekiler](full-report.md#icindekiler) |
| 1. Giriş | [full-report.md#giris](full-report.md#giris) |
| 2. Güç ve kontrol tasarım yöntemi | [full-report.md#guc-ve-kontrol-tasariminda-izlenen-yontem](full-report.md#guc-ve-kontrol-tasariminda-izlenen-yontem) |
| 3. Güç katı hesaplamaları | [full-report.md#guc-kati-hesaplamalari](full-report.md#guc-kati-hesaplamalari) |
| 4. Çevirici durum denklemleri | [full-report.md#cevirici-durum-denklemleri](full-report.md#cevirici-durum-denklemleri) |
| 5. Kontrolcü tasarımı | [full-report.md#kontrolcu-tasarimi](full-report.md#kontrolcu-tasarimi) |
| 6. Op-amp devresi gerçekleştirmesi | [full-report.md#op-amp-devresi-gerceklemesi](full-report.md#op-amp-devresi-gerceklemesi) |
| 7. Benzetim sonuçları | [full-report.md#benzetim-sonuclari](full-report.md#benzetim-sonuclari) |
| 8. Projenin geleceği | [full-report.md#projenin-gelecegi](full-report.md#projenin-gelecegi) |
| Kaynaklar | [full-report.md#kaynaklar](full-report.md#kaynaklar) |
| Ekler | [full-report.md#ekler](full-report.md#ekler) |

## Verification Kısayolları

| Kanıt | Bağlantı |
|---|---|
| Güç aralığı: yaklaşık $49.6-124.2\,\text{W}$ | [Şekil 7.1/7.2](full-report.md#cikis-gucu) |
| Statik çıkış gerilimi | [Şekil 7.3](full-report.md#fig-static-output) |
| Transient sapma: yaklaşık $\pm8.58\%$ | [Şekil 7.4](full-report.md#fig-transient-output) |
| Çıkış ripple: yaklaşık $37.38\,\text{mV}_{p-p}$ | [Şekil 7.5](full-report.md#fig-output-ripple) |
| Verim: yaklaşık $97.78\%$ | [Şekil 7.6/7.7](full-report.md#fig-eff-36v) |

## Görsel ve Kaynak Klasörleri

| Path | Açıklama |
|---|---|
| [assets/docx-media/media/](assets/docx-media/media/) | Rapor içinde kullanılan temiz medya seti |
| [assets/docx-media/raw/](assets/docx-media/raw/) | DOCX içinden çıkarılan ham medya |
| [originals/](originals/) | Kaynak DOCX/PDF kopyaları |
| [../images/readme/](../images/readme/) | Eski README görsel seti; karşılaştırma ve yeniden kullanım için korunuyor |
| [../images/docx_extracted/](../images/docx_extracted/) | Eski kısmi DOCX medya çıkarımı |
| [../ekran gorüntüleri/](../ekran%20gor%C3%BCnt%C3%BCleri/) | Orijinal simülasyon ekran görüntüleri |

## LTspice

Ana simülasyon klasörü: [../LTspice_AveragedSwitchModelingSimulation/](../LTspice_AveragedSwitchModelingSimulation/)

Öne çıkan buck converter dosyaları:

- [SyncBuck_switching_CL.asc](../LTspice_AveragedSwitchModelingSimulation/SyncBuck_switching_CL.asc)
- [SyncBuck_average_CL.asc](../LTspice_AveragedSwitchModelingSimulation/SyncBuck_average_CL.asc)
- [SyncBuck_average_fresponses.asc](../LTspice_AveragedSwitchModelingSimulation/SyncBuck_average_fresponses.asc)
- [SyncBuck_average_parameters.asc](../LTspice_AveragedSwitchModelingSimulation/SyncBuck_average_parameters.asc)
- [SyncBuck_average_Zout.asc](../LTspice_AveragedSwitchModelingSimulation/SyncBuck_average_Zout.asc)
- [PID_compensator.asc](../LTspice_AveragedSwitchModelingSimulation/PID_compensator.asc)

## Kaynak Orijinaller

| Kaynak | Bağlantı |
|---|---|
| Ana DOCX | [../Birinci_donem_Buck_Converter_Serbest_Projesi.docx](../Birinci_donem_Buck_Converter_Serbest_Projesi.docx) |
| Ana PDF | [../Birinci_donem_Buck_Converter_Serbest_Projesi.pdf](../Birinci_donem_Buck_Converter_Serbest_Projesi.pdf) |
| Docs içindeki DOCX kopyası | [originals/birinci-donem-buck-converter-serbest-projesi.docx](originals/birinci-donem-buck-converter-serbest-projesi.docx) |
| Docs içindeki PDF kopyası | [originals/birinci-donem-buck-converter-serbest-projesi.pdf](originals/birinci-donem-buck-converter-serbest-projesi.pdf) |
| MIT proje şartnamesi | [../G5_mit6_622_s23_designproj.pdf](../G5_mit6_622_s23_designproj.pdf) |
| LM5146-Q1 datasheet | [../G32_lm5146-q1.pdf](../G32_lm5146-q1.pdf) |

## Kalan Manuel Takip

Input voltage transient, input current ripple ve sıcaklık sweep gereksinimleri hedef olarak korunmuştur; kaynak raporda bunları ayrı dalga şekliyle kapatan kanıt bulunmadığı için takip gerektirir. Çok küçük `image12.png`, `image13.png`, `image30.png`, `image32.png`, `image33.png` medya nesneleri görünür teknik figür gibi durmadığından ana akışa gömülmemiştir.
