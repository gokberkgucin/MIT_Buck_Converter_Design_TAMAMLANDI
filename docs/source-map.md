# Source Map

Bu dosya, kaynak DOCX belgesindeki ana bölümlerin repo içindeki Markdown karşılıklarını ve kullanılan görselleri izlemek için oluşturuldu.

## Bölüm Haritası

| Kaynak DOCX bölümü | Repo karşılığı | Durum |
|---|---|---|
| Kapak / onay sayfaları | `docs/full-report.md#kapak` | Aktarıldı |
| ABSTRACT | `docs/full-report.md#abstract` | Aktarıldı |
| İÇİNDEKİLER | `docs/full-report.md#icindekiler` | GitHub uyumlu tıklanabilir TOC olarak yeniden kuruldu |
| 1. GİRİŞ | `docs/full-report.md#giris` | Aktarıldı |
| 1.1 Çalışmanın Amacı ve Kapsamı | `docs/full-report.md#calismanin-amaci-ve-kapsami` | Aktarıldı |
| 1.2 Buck Converter Nedir? | `docs/full-report.md#buck-converter-nedir` | Aktarıldı |
| 2. Güç ve Kontrol Tasarımında İzlenen Yöntem | `docs/full-report.md#guc-ve-kontrol-tasariminda-izlenen-yontem` | Aktarıldı |
| 2.1 Frekans Seçim Kuralları ve Hesaplamalar | `docs/full-report.md#frekans-secim-kurallari-ve-hesaplamalar` | Aktarıldı |
| 2.2 Hesaplamalarda Kullanılacak Parametreler | `docs/full-report.md#hesaplamalarda-kullanilacak-parametreler` | Aktarıldı |
| 3. Güç Katı Hesaplamaları | `docs/full-report.md#guc-kati-hesaplamalari` | Aktarıldı |
| 4. Çevirici Durum Denklemleri | `docs/full-report.md#cevirici-durum-denklemleri` | Aktarıldı |
| 4.1 ESR Etkisi | `docs/full-report.md#esr-etkisi` | Aktarıldı |
| 4.2 Genel Dalga-Biçimleri | `docs/full-report.md#genel-dalga-bicimleri` | Aktarıldı |
| 5. Kontrolcü Tasarımı | `docs/full-report.md#kontrolcu-tasarimi` | Aktarıldı ve denklem temizliği yapıldı |
| 6. Op-Amp Devresi Gerçeklemesi | `docs/full-report.md#op-amp-devresi-gerceklemesi` | Aktarıldı ve denklem temizliği yapıldı |
| 7. Benzetim Sonuçları | `docs/full-report.md#benzetim-sonuclari` | Aktarıldı ve doğrulama tablosu güçlendirildi |
| 8. PROJENIN GELECEĞİ | `docs/full-report.md#projenin-gelecegi` | Aktarıldı |
| KAYNAKLAR | `docs/full-report.md#kaynaklar` | Temiz referans formatına dönüştürüldü |
| EKLER | `docs/full-report.md#ekler` | Aktarıldı |
| EK-1. Sığaç Verisayfası | `docs/full-report.md#ek-1-sigac-verisayfasi` | Aktarıldı |
| EK-2. Genel görünüm | `docs/full-report.md#ek-2-genel-gorunum` | Aktarıldı |

## Görsel Kullanım Haritası

| Görsel | Kullanıldığı yer | İçerik |
|---|---|---|
| `docs/assets/full-report/power-stage/image01-type-3-compensator-frequency-relations.png` | Bölüm 2.1 | Type-3 compensator frekans ilişkileri |
| `docs/assets/full-report/power-stage/image02-frequency-ordering.png` | Bölüm 2.1 | Frekans sıralaması |
| `docs/assets/full-report/power-stage/image03-updated-power-stage-calculation-flow.png` | Bölüm 3.2 | Güç katı hesap akışı/devre görseli |
| `docs/assets/full-report/power-stage/image04-duty-cycle-36v-ltspice-check.jpeg` | Bölüm 3.3 | 36 V duty-cycle kontrolü |
| `docs/assets/full-report/power-stage/image05-duty-cycle-24v-ltspice-check.png` | Bölüm 3.3 | 24 V duty-cycle kontrolü |
| `docs/assets/full-report/state-equations/image06-buck-converter-state-equations.png` | Bölüm 4 | Durum denklemleri |
| `docs/assets/full-report/state-equations/image07-esr-effect-output-voltage.png` | Bölüm 4.1 | ESR etkisi |
| `docs/assets/full-report/state-equations/image08-current-voltage-general-waveforms.png` | Bölüm 4.1 | Genel akım/gerilim dalga biçimleri |
| `docs/assets/full-report/state-equations/image09-waveform-label-small-signal.png` | Bölüm 4.2 | Dalga biçimi etiket görseli |
| `docs/assets/full-report/state-equations/image10-waveform-equation-label.png` | Bölüm 4.2 | Dalga biçimi denklem/etiket görseli |
| `docs/assets/full-report/state-equations/image11-buck-converter-general-waveforms.png` | Bölüm 4.2 | Buck converter genel dalga biçimleri |
| `docs/assets/full-report/state-equations/image12-decorative-small-media-12.png` | Bölüm 4.2 | Kaynak DOCX küçük medya nesnesi; eksiksiz aktarım için ölçeklenerek bağlandı |
| `docs/assets/full-report/state-equations/image13-decorative-small-media-13.png` | Bölüm 4.2 | Kaynak DOCX küçük medya nesnesi; eksiksiz aktarım için ölçeklenerek bağlandı |
| `docs/assets/full-report/controller/image14-controller-design-transition-diagram.png` | Bölüm 5 | Kontrolcü tasarımı giriş diyagramı |
| `docs/assets/full-report/controller/image15-system-block-diagram.png` | Bölüm 5.1 | Sistem block diagramı |
| `docs/assets/full-report/controller/image16-closed-loop-expression-1.png` | Bölüm 5.1 | Kapalı çevrim ifade ilişkisi |
| `docs/assets/full-report/controller/image17-closed-loop-expression-2.png` | Bölüm 5.1 | Kapalı çevrim ifade ilişkisi |
| `docs/assets/full-report/controller/image18-open-loop-transfer-function-block-expression.png` | Bölüm 5.3 | Açık çevrim transfer fonksiyonu |
| `docs/assets/full-report/controller/image19-uncompensated-loop-gain-expression.png` | Bölüm 5.3 | Uncompensated loop gain ifadesi |
| `docs/assets/full-report/controller/image20-uncompensated-loop-gain-bode.png` | Bölüm 5.3 | Uncompensated Bode diyagramı |
| `docs/assets/full-report/controller/image21-lead-compensator-bode-shape.png` | Bölüm 5.4 | Lead compensator Bode davranışı |
| `docs/assets/full-report/controller/image22-lead-compensator-frequency-response.png` | Bölüm 5.4 | Lead compensator frekans cevabı |
| `docs/assets/full-report/controller/image23-lead-compensated-open-loop-bode.png` | Bölüm 5.4 | Lead sonrası açık çevrim Bode |
| `docs/assets/full-report/controller/image24-lag-pi-compensator-bode-shape.png` | Bölüm 5.5 | Lag/PI compensator Bode davranışı |
| `docs/assets/full-report/controller/image25-pid-compensator-bode-curve.png` | Bölüm 5.6 | PID compensator Bode eğrisi |
| `docs/assets/full-report/controller/image26-lt1215-opamp-gain-frequency.png` | Bölüm 5.7 | LT1215 op-amp gain/frequency grafiği |
| `docs/assets/full-report/controller/image27-final-open-loop-bode.png` | Bölüm 5.8 | Nihai açık çevrim Bode |
| `docs/assets/full-report/controller/image28-calculated-open-loop-transfer-function.png` | Bölüm 5.8 | Hesaplanan $T(s)$ |
| `docs/assets/full-report/controller/image29-t-of-s-closed-loop-expressions.png` | Bölüm 5.8 | $T(s)$ kapalı çevrim ifadeleri |
| `docs/assets/full-report/controller/image30-decorative-small-media-30.png` | Bölüm 5.8 | Kaynak DOCX küçük medya nesnesi; eksiksiz aktarım için ölçeklenerek bağlandı |
| `docs/assets/full-report/controller/image31-closed-loop-reference-to-output-response.png` | Bölüm 5.8 | Reference-to-output cevabı |
| `docs/assets/full-report/opamp/image32-decorative-small-media-32.png` | Bölüm 6 | Kaynak DOCX küçük medya nesnesi; eksiksiz aktarım için ölçeklenerek bağlandı |
| `docs/assets/full-report/opamp/image33-decorative-small-media-33.png` | Bölüm 6 | Kaynak DOCX küçük medya nesnesi; eksiksiz aktarım için ölçeklenerek bağlandı |
| `docs/assets/full-report/opamp/image34-opamp-implementation-circuit.png` | Bölüm 6 | Op-amp gerçekleştirme devresi |
| `docs/assets/full-report/opamp/image35-sensor-gain-voltage-divider.png` | Bölüm 6.1 | Sensor gain gerilim bölücü |
| `docs/assets/full-report/opamp/image36-compensator-target-frequency-gain.png` | Bölüm 6.2 | Compensator hedef frekans/kazanç davranışı |
| `docs/assets/full-report/opamp/image37-simplified-compensator-circuit.png` | Bölüm 6.2 | Sadeleştirilmiş compensator devresi |
| `docs/assets/full-report/opamp/image38-r2-c2-impedance-comparison.png` | Bölüm 6.2 | $R_2$ ve $C_2$ empedans davranışı |
| `docs/assets/full-report/opamp/image39-capacitor-impedance-plus-20db-dec.png` | Bölüm 6.2 | $+20\,\text{dB/dec}$ eğim |
| `docs/assets/full-report/opamp/image40-z1-z2-impedance-network-1.png` | Bölüm 6.2 | $Z_1/Z_2$ empedans ağı |
| `docs/assets/full-report/opamp/image41-z1-z2-impedance-network-2.png` | Bölüm 6.2 | $Z_1/Z_2$ empedans ağı |
| `docs/assets/full-report/simulation/image42-output-power-50w-operating-point.png` | Bölüm 7.3 | Yaklaşık 49.6 W çıkış gücü |
| `docs/assets/full-report/simulation/image43-output-power-125w-operating-point.png` | Bölüm 7.3 | Yaklaşık 124.2 W çıkış gücü |
| `docs/assets/full-report/simulation/image44-static-output-voltage-measurement.png` | Bölüm 7.4 | Statik çıkış gerilimi |
| `docs/assets/full-report/simulation/image45-transient-output-voltage-load-current.png` | Bölüm 7.5 | Transient çıkış gerilimi |
| `docs/assets/full-report/simulation/image46-output-ripple-measurement.png` | Bölüm 7.6 | Output ripple |
| `docs/assets/full-report/simulation/image47-input-power-36v-measurement.png` | Bölüm 7.7 | 36 V girişte giriş gücü |
| `docs/assets/full-report/simulation/image48-output-power-36v-measurement.png` | Bölüm 7.7 | 36 V girişte çıkış gücü |
| `docs/assets/full-report/simulation/image49-output-power-24v-measurement.png` | Bölüm 7.7 | 24 V girişte çıkış gücü |
| `docs/assets/full-report/simulation/image50-input-power-24v-measurement.png` | Bölüm 7.7 | 24 V girişte giriş gücü |
| `docs/assets/full-report/future-work/image51-lm5146-typical-application.png` | Bölüm 8 | LM5146 tipik uygulama |
| `docs/assets/full-report/appendices/image52-output-capacitor-datasheet-excerpt.png` | Ek-1 | Sığaç veri sayfası |
| `docs/assets/full-report/appendices/image53-ltspice-circuit-overview.png` | Ek-2 | LTspice devre genel görünümü |

## Manuel Takip Gereken Öğeler

- `image12.png`, `image13.png`, `image30.png`, `image32.png`, `image33.png` artık `docs/full-report.md` içinde doğrudan bağlandı. Boyutları çok küçük olduğu için ölçeklenerek gösterildi; PDF render ile teknik içerik taşıyıp taşımadıkları son kez doğrulanabilir.
- Input voltage transient, input current ripple ve sıcaklık aralığı gereksinimleri raporda hedef olarak listelenmiş olsa da ayrı görsel doğrulamayla kapatılmamış.
- Büyük üçüncü taraf kaynak PDF'lerin repo içinde tutulması lisans/dağıtım açısından ayrıca değerlendirilmeli.
