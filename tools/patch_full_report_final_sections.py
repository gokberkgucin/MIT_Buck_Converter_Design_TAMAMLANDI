#!/usr/bin/env python3
"""Patch section 7 onward in docs/full-report.md and write summary docs."""

from __future__ import annotations

from pathlib import Path


REPORT = Path("docs/full-report.md")
VERIFICATION = Path("docs/verification-summary.md")
SOURCE_MAP = Path("docs/source-map.md")

FINAL_SECTIONS = r"""# 7. Benzetim Sonuçları

Bu bölümde amaç, tasarım gereksinimlerini karşılayabilen bir devre tasarlandığını göstermek ve önceki bölümlerde kağıt-kalem ile yapılan hesapların LTspice benzetimleriyle doğrulanmasını sağlamaktır. Bu nedenle bulunan değerler olduğu gibi LTspice devresinde kullanılmış, sonuçlar görsellerle birlikte raporlanmıştır.

<a id="tasarim-gereksinimleri"></a>
## 7.1. Tasarım Gereksinimleri

| Gereksinim | Hedef | Raporlanan benzetim sonucu | Değerlendirme | Kanıt |
|---|---:|---:|---|---|
| Input voltage range | $24-36\,\text{V}$ | $24\,\text{V}$ ve $36\,\text{V}$ çalışma noktaları kullanıldı | Geçti | [Bölüm 7.2](#benzetimde-kullanilan-elemanlar-ve-parametreler) |
| Input voltage transient limit | $44\,\text{V}$, en çok $1\,\text{ms}$ | Gereksinim olarak listelenmiş; bu raporda ayrı transient dayanım dalga şekli yok | Takip gerekiyor | Not |
| Output power range | $50-125\,\text{W}$ | Yaklaşık $49.6-124.2\,\text{W}$ | Geçti | [Şekil 7.1](#fig-output-power-50w), [Şekil 7.2](#fig-output-power-125w) |
| Output voltage static requirement | $14\,\text{V}\pm3\%$ | Raporlanan sapma yaklaşık $\%1.30$ | Geçti | [Şekil 7.3](#fig-static-output) |
| Output voltage transient limits | $14\,\text{V}\pm20\%$ | Raporlanan transient sapma yaklaşık $\pm\%8.58$ | Geçti | [Şekil 7.4](#fig-transient-output) |
| Allowed output voltage ripple | $100\,\text{mV}_{p-p}$ | Yaklaşık $37.38\,\text{mV}_{p-p}$ | Geçti | [Şekil 7.5](#fig-output-ripple) |
| Allowed input current ripple | $50\,\text{mA}_{p-p}$, ideal source | Bu raporda ayrı görsel kanıtla kapatılmamış | Takip gerekiyor | Not |
| Minimum efficiency | $\%90$ | Yaklaşık $\%97.78$ ve diğer çalışma noktalarında $\%97.99$, $\%98.63$, $\%98.14$ | Geçti | [Şekil 7.6](#fig-eff-36v), [Şekil 7.7](#fig-eff-24v) |
| Ambient temperature range | $-20^\circ\text{C}$ to $+50^\circ\text{C}$ | Gereksinim olarak listelenmiş; sıcaklık sweep'i bu raporda yok | Takip gerekiyor | Not |

Notlar:

1. Converter, $44\,\text{V}$ input voltage transient durumunda hayatta kalabilmelidir; bu transient sırasında çalışması zorunlu değildir.
2. Output voltage, minimum ve maksimum yük arasındaki adımlarda belirtilen sınırların dışına çıkmamalıdır.

<a id="benzetimde-kullanilan-elemanlar-ve-parametreler"></a>
## 7.2. Benzetimde Kullanılan Elemanlar ve Parametreler

| Parametre / eleman | Değer |
|---|---:|
| Giriş gerilimi, $V_{s,max}$ | $36\,\text{V}$ |
| Giriş gerilimi, $V_{s,min}$ | $24\,\text{V}$ |
| Maksimum çıkış gücü, $P_{max}$ | $125\,\text{W}$ |
| Minimum çıkış gücü | $50\,\text{W}$ |
| Çıkış gerilimi, $V_o$ | $14\,\text{V}$ |
| Hesaplanan çıkış ripple hedefi | $\Delta V_o \approx 27\,\text{mV}$ |
| Çıkış sığacı | $C=82\,\mu\text{F}$ |
| Sığaç ESR | $R_{ESR}=19.39\,\text{m}\Omega$ |
| MOSFET | BSC150N03LD |
| MOSFET on direnci | $R_{on}=15\,\text{m}\Omega$ |
| Bobin seri direnci | $R_L=15\,\text{m}\Omega$ |
| Minimum yük direnci | $R_{load,min}=1.569\,\Omega$ |
| Maksimum yük direnci | $R_{load,max}=3.921\,\Omega$ |
| Minimum duty cycle | $D_{min}=0.3888$ |
| Maksimum duty cycle | $D_{max}=0.5833$ |
| Op-amp | LT1215, $23\,\text{MHz}$ |
| Compensator elemanları | $R_2=100\,\text{k}\Omega$, $R_1=21\,\text{k}\Omega$, $R_4=2.4\,\text{k}\Omega$, $C_2=1.59\,\text{nF}$, $C_4=2.2\,\text{nF}$ |
| Sensor gain elemanları | $R_3=12.8\,\text{k}\Omega$, $R_5=87.2\,\text{k}\Omega$ |
| Gate dirençleri | $R_{g1}=5\,\Omega$, $R_{g2}=5\,\Omega$ |
| Schottky diyot | 1N5817, $1\,\text{A}$, $20\,\text{V}$ |
| PWM ramp genliği | $V_m=4\,\text{V}$ |
| Anahtarlama frekansı | $f_s=100\,\text{kHz}$ |
| Referans gerilimi | $V_{ref}=1.8\,\text{V}$ |

<a id="cikis-gucu"></a>
## 7.3. Çıkış Gücü

İstenen güç aralığı:

$$
50\,\text{W} \le P_{out} \le 125\,\text{W}
$$

Benzetimde raporlanan güç aralığı:

$$
P_{out} \approx 49.5957\,\text{W} - 124.1839\,\text{W}
$$

Bu değerler hedeflenen $50-125\,\text{W}$ aralığının çok yakınında ve pratik tolerans içinde kabul edilmiştir.

<a id="fig-output-power-50w"></a>
![Yaklaşık 50 W çıkış gücü çalışma noktası](assets/docx-media/media/image42.png)

*Şekil 7.1 - Düşük güç çalışma noktasında $P_{out}\approx49.5957\,\text{W}$ ölçümü.*

<a id="fig-output-power-125w"></a>
![Yaklaşık 125 W çıkış gücü çalışma noktası](assets/docx-media/media/image43.png)

*Şekil 7.2 - Yüksek güç çalışma noktasında $P_{out}\approx124.1839\,\text{W}$ ölçümü.*

<a id="output-voltage-static-requirement"></a>
## 7.4. Output Voltage Static Requirement

İstenen statik çıkış gerilimi:

$$
V_o = 14\,\text{V}\pm3\%
$$

Raporlanan sonuçta statik çıkış geriliminde yaklaşık $\%1.30$ sapma olduğu belirtilmiştir. Görseldeki cursor değeri:

$$
V_{out}\approx13.981693\,\text{V}
$$

olarak okunmaktadır. Her iki durumda da değer $14\,\text{V}\pm3\%$ statik gereksiniminin içindedir.

<a id="fig-static-output"></a>
![Statik çıkış gerilimi ölçümü](assets/docx-media/media/image44.png)

*Şekil 7.3 - Statik çıkış gerilimi ölçümü; kaynak raporda yaklaşık $\%1.30$ sapma not edilmiştir.*

<a id="output-voltage-transient-limits"></a>
## 7.5. Output Voltage Transient Limits

İstenen transient sınırı:

$$
V_o = 14\,\text{V}\pm20\%
$$

Benzetimde yük akımı yaklaşık $1\,\mu\text{s}$ içinde:

$$
I_{max}=8.92\,\text{A}
\quad \rightarrow \quad
I_{min}=3.57\,\text{A}
$$

arasında değişmektedir. Kaynak raporda çıkış gerilimindeki transient sapma yaklaşık:

$$
\pm 8.58\%
$$

olarak verilmiştir. Bu değer $20\%$ transient sınırının içindedir.

Grafikte çıkış geriliminin düşük akım/yük geçişinde yaklaşık $12.70\,\text{V}$ seviyesine indiği ve üst yönde yaklaşık $15.17\,\text{V}$ seviyesine çıktığı görülür. Yaklaşık $0.3\,\text{ms}$ içinde toparlanma not edilmiştir.

<a id="fig-transient-output"></a>
![Transient çıkış gerilimi ve yük akımı davranışı](assets/docx-media/media/image45.png)

*Şekil 7.4 - Minimum ve maksimum yük akımı arasında transient çıkış gerilimi davranışı.*

<a id="allowed-output-voltage-ripple"></a>
## 7.6. Allowed Output Voltage Ripple

İstenen çıkış ripple sınırı:

$$
\Delta V_{o,p-p} \le 100\,\text{mV}
$$

Kararlı halde raporlanan tepeden tepeye çıkış gerilimi dalgalanması:

$$
\Delta V_o \approx 37.38\,\text{mV}
$$

olarak ölçülmüştür. Bu değer $100\,\text{mV}_{p-p}$ sınırının belirgin biçimde altındadır.

<a id="fig-output-ripple"></a>
![Çıkış ripple ölçümü](assets/docx-media/media/image46.png)

*Şekil 7.5 - Kararlı halde $V_{out}$ ripple ölçümü: yaklaşık $37.38\,\text{mV}_{p-p}$.*

<a id="verimlilik"></a>
## 7.7. Verimlilik

İstenen minimum verimlilik:

$$
\eta \ge 90\%
$$

Kaynak raporda $V_g=36\,\text{V}$ ve $R=1.569\,\Omega$ için:

$$
\eta
=
\frac{P_{out}}{P_{in}}
=
\frac{123.8\,\text{W}}{126.6\,\text{W}}
=
0.9778
$$

olarak verilmiştir. Bu:

$$
\eta \approx 97.78\%
$$

demektir.

<a id="fig-eff-36v"></a>
![36 V girişte giriş gücü ölçümü](assets/docx-media/media/image47.png)

*Şekil 7.6 - $V_g=36\,\text{V}$ ve $R=1.569\,\Omega$ için giriş gücü ölçümü; ortalama $P_{in}\approx126.6\,\text{W}$.*

![36 V girişte çıkış gücü ölçümü](assets/docx-media/media/image48.png)

*Şekil 7.7 - $V_g=36\,\text{V}$ ve $R=1.569\,\Omega$ için çıkış gücü ölçümü; ortalama $P_{out}\approx123.8\,\text{W}$.*

Diğer çalışma noktaları:

| Çalışma noktası | Raporlanan güç oranı | Verim |
|---|---:|---:|
| $V_g=24\,\text{V}$, $R=1.569\,\Omega$ | $124.01\,\text{W}/126.55\,\text{W}$ | $97.99\%$ |
| $V_g=24\,\text{V}$, $R=3.921\,\Omega$ | $49.599\,\text{W}/50.29\,\text{W}$ | $98.63\%$ |
| $V_g=36\,\text{V}$, $R=3.921\,\Omega$ | $49.542\,\text{W}/50.482\,\text{W}$ | $98.14\%$ |

<a id="fig-eff-24v"></a>
![24 V girişte çıkış gücü ölçümü](assets/docx-media/media/image49.png)

*Şekil 7.8 - $V_g=24\,\text{V}$, $R=1.569\,\Omega$ için $P_{out}\approx124.01\,\text{W}$.*

![24 V girişte giriş gücü ölçümü](assets/docx-media/media/image50.png)

*Şekil 7.9 - $V_g=24\,\text{V}$, $R=1.569\,\Omega$ için $P_{in}\approx126.55\,\text{W}$.*

<a id="hesaplamalarin-dogrulanmasi"></a>
## 7.8. Hesaplamaların Doğrulanması

Bu bölümün iki temel amacı vardır:

- Belirlenen tasarım specifications'larını karşılayabilen bir devre tasarlandığını göstermek.
- Önceki bölümlerde kağıt-kalemle yapılan hesaplamaların doğrulamasını yapmak.
- Bu yüzden bulunan değerler olduğu gibi değiştirilmeden LTspice'da kullanılmıştır.
- Bu değerlerin benzetim sonuçları gösterilmiştir.
- İyileştirmeler yapmak mümkündür; bu ilk çalışma, hesaplanan değerlerin hedefleri karşıladığını gösteren temel doğrulama niteliğindedir.

Doğrulama sonuçları özetle:

| Doğrulama alanı | Sonuç |
|---|---|
| Güç aralığı | Yaklaşık $49.6-124.2\,\text{W}$ |
| Statik çıkış gerilimi | Hedef $14\,\text{V}\pm3\%$ içinde |
| Transient çıkış sapması | Yaklaşık $\pm8.58\%$, hedef $\pm20\%$ içinde |
| Çıkış ripple | Yaklaşık $37.38\,\text{mV}_{p-p}$, hedef $100\,\text{mV}_{p-p}$ altında |
| Verim | Yaklaşık $97.78\%$ ana raporlanan çalışma noktası; tüm raporlanan noktalar $\%90$ üzerinde |

<a id="projenin-gelecegi"></a>
# 8. Projenin Geleceği

Projenin devamında yapılacaklar:

- LM5146 kontrolcüsü kullanılacak.
- Giriş filtresi tasarlanacak.
- Eleman seçimleri kesinleştirilecek.
- MOSFET sürücüsü ile ilgili hesaplar yapılacak.
- Ortalama model kullanılarak frekans alanında inceleme yapılacak.
- Verimlilikler ve kayıplar hesaplanacak.
- Parametrik değerler verilerek iyileştirmeler yapılacak.
- Bobinle ilgili hesaplar detaylandırılacak.
- Altium'da çizim yapılacak.

![LM5146 tipik uygulama şeması](assets/docx-media/media/image51.png)

*Şekil 8.1 - LM5146 tabanlı sonraki tasarım yönü için tipik uygulama şeması.*

<a id="kaynaklar"></a>
# Kaynaklar

[1] R. W. Erickson and D. Maksimovic, *Fundamentals of Power Electronics*, 3rd ed., Cham: Springer, 2020.

[2] P. Parto, P. Asadi, and A. M. Rahimi, "Compensator design procedure for buck converter with voltage-mode error-amplifier," Application Note AN-1162, International Rectifier, 2006.

[3] Wikipedia contributors, "Root mean square," Wikipedia. Available: <https://en.wikipedia.org/wiki/Root_mean_square>.

[4] D. Can, "DC-DC Buck Converter Design Part 1 - Open-Loop Design - Calculations & MATLAB & TINA-TI SPICE," YouTube. Available: <https://youtu.be/fE1lxyE7ILI?si=ux-xqTelJLZC5YQm>.

[5] E. Rogers, "Understanding Buck Power Stages in Switchmode Power Supplies," Texas Instruments Application Report, SLVA044, March 1999.

[6] B. Hauke, "Basic Calculation of a Buck Converter's Power Stage," Texas Instruments Application Report, SLVA477B, December 2011, revised August 2015.

[7] T. Taufik, "Practical Design of Buck Converter," California Polytechnic State University.

## Repo İçindeki Reference / Source Material Notu

Repo içinde `G5_mit6_622_s23_designproj.pdf`, `G32_lm5146-q1.pdf` ve power electronics kaynak kitabı PDF/TXT dosyaları source/reference material olarak durmaktadır. Üçüncü taraf PDF'lerin lisans ve dağıtım durumu bu çalışma içinde ayrıca doğrulanmadı; bu nedenle teknik dokümantasyonda nötr biçimde referans materyali olarak konumlandırılmıştır.

<a id="ekler"></a>
# Ekler

<a id="ek-1-sigac-verisayfasi"></a>
## EK-1. Sığaç Verisayfası

Kaynak raporda seçilen çıkış sığacı için veri sayfası kesiti verilmiştir. $82\,\mu\text{F}$ sınıfındaki sığaç ve ESR/ripple bilgileri güç katı hesabında kullanılan $C$ ve $R_{ESR}$ seçimlerini destekler.

![Sığaç veri sayfası kesiti](assets/docx-media/media/image52.png)

*Şekil E.1 - Sığaç veri sayfası kesiti; $82\,\mu\text{F}$ satırı kaynak raporda işaretlenmiştir.*

<a id="ek-2-genel-gorunum"></a>
## EK-2. Genel Görünüm

Kaynak raporda LTspice devresinin genel görünümü de ek olarak verilmiştir. Bu devre görünümünde güç katı, bootstrap/driver yapısı, PWM, LT1215 op-amp compensator, feedback dirençleri ve yük yapısı birlikte görülür.

![LTspice devresinin genel görünümü](assets/docx-media/media/image53.png)

*Şekil E.2 - Senkron buck converter LTspice devresinin genel görünümü.*
"""


VERIFICATION_CONTENT = r"""# Verification Summary

Bu dosya, `docs/full-report.md` içindeki Bölüm 7 doğrulama sonuçlarının kısa karşılaştırma tablosudur.

| Hedef spesifikasyon | Raporlanan benzetim sonucu | Değerlendirme | İlgili görsel/link | Not |
|---|---:|---|---|---|
| Input voltage range: $24-36\,\text{V}$ | $24\,\text{V}$ ve $36\,\text{V}$ çalışma noktaları kullanıldı | Geçti | [7.2 parametre tablosu](full-report.md#benzetimde-kullanilan-elemanlar-ve-parametreler) | İki uç giriş gerilimi benzetim parametresi olarak kullanılmış. |
| Input voltage transient limit: $44\,\text{V}$, en çok $1\,\text{ms}$ | Ayrı dayanım benzetimi raporlanmadı | Takip gerekiyor | [7.1 gereksinimler](full-report.md#tasarim-gereksinimleri) | Converter'ın hayatta kalma şartı; bu raporda görsel kanıt yok. |
| Output power range: $50-125\,\text{W}$ | Yaklaşık $49.5957-124.1839\,\text{W}$ | Geçti | [49.6 W](full-report.md#fig-output-power-50w), [124.2 W](full-report.md#fig-output-power-125w) | Alt uç hedefe çok yakın; pratik tolerans içinde kabul edilmiş. |
| Output voltage static requirement: $14\,\text{V}\pm3\%$ | Raporlanan sapma yaklaşık $\%1.30$ | Geçti | [static output](full-report.md#fig-static-output) | Görsel cursor değeri $13.981693\,\text{V}$; hedef aralığın içinde. |
| Output voltage transient limits: $14\,\text{V}\pm20\%$ | Yaklaşık $\pm8.58\%$ sapma | Geçti | [transient response](full-report.md#fig-transient-output) | Kaynak raporda yaklaşık $0.3\,\text{ms}$ toparlanma not edilmiş. |
| Allowed output voltage ripple: $100\,\text{mV}_{p-p}$ | Yaklaşık $37.38\,\text{mV}_{p-p}$ | Geçti | [output ripple](full-report.md#fig-output-ripple) | Hedef sınırın belirgin biçimde altında. |
| Allowed input current ripple: $50\,\text{mA}_{p-p}$, ideal source | Ayrı görsel kanıt raporlanmadı | Takip gerekiyor | [7.1 gereksinimler](full-report.md#tasarim-gereksinimleri) | Giriş filtresi / input-side tasarım sonraki proje kapsamında ele alınmalı. |
| Minimum efficiency: $\%90$ | Ana çalışma noktası yaklaşık $\%97.78$ | Geçti | [efficiency 36 V](full-report.md#fig-eff-36v), [efficiency 24 V](full-report.md#fig-eff-24v) | Diğer raporlanan noktalar: $\%97.99$, $\%98.63$, $\%98.14$. |
| Ambient temperature range: $-20^\circ\text{C}$ to $+50^\circ\text{C}$ | Sıcaklık sweep'i raporlanmadı | Takip gerekiyor | [7.1 gereksinimler](full-report.md#tasarim-gereksinimleri) | Gereksinim listelenmiş, ayrı sıcaklık analizi yok. |

## Kısa Sonuç

Raporlanan LTspice doğrulamaları, output-side ana hedefleri karşılamaktadır: güç aralığı yaklaşık $49.6-124.2\,\text{W}$, statik çıkış gereksinimi hedef içinde, transient sapma yaklaşık $\pm8.58\%$, ripple yaklaşık $37.4\,\text{mV}$ ve verim yaklaşık $\%97.78$ olarak görünür hale getirilmiştir.
"""


SOURCE_MAP_CONTENT = r"""# Source Map

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
| `docs/assets/docx-media/media/image1.png` | Bölüm 2.1 | Type-3 compensator frekans ilişkileri |
| `docs/assets/docx-media/media/image2.png` | Bölüm 2.1 | Frekans sıralaması |
| `docs/assets/docx-media/media/image3.png` | Bölüm 3.2 | Güç katı hesap akışı/devre görseli |
| `docs/assets/docx-media/media/image4.jpeg` | Bölüm 3.3 | 36 V duty-cycle kontrolü |
| `docs/assets/docx-media/media/image5.png` | Bölüm 3.3 | 24 V duty-cycle kontrolü |
| `docs/assets/docx-media/media/image6.png` | Bölüm 4 | Durum denklemleri |
| `docs/assets/docx-media/media/image7.png` | Bölüm 4.1 | ESR etkisi |
| `docs/assets/docx-media/media/image8.png` | Bölüm 4.1 | Genel akım/gerilim dalga biçimleri |
| `docs/assets/docx-media/media/image9.png` | Bölüm 4.2 | Dalga biçimi etiket görseli |
| `docs/assets/docx-media/media/image10.png` | Bölüm 4.2 | Dalga biçimi denklem/etiket görseli |
| `docs/assets/docx-media/media/image11.png` | Bölüm 4.2 | Buck converter genel dalga biçimleri |
| `docs/assets/docx-media/media/image14.png` | Bölüm 5 | Kontrolcü tasarımı giriş diyagramı |
| `docs/assets/docx-media/media/image15.png` | Bölüm 5.1 | Sistem block diagramı |
| `docs/assets/docx-media/media/image16.png` | Bölüm 5.1 | Kapalı çevrim ifade ilişkisi |
| `docs/assets/docx-media/media/image17.png` | Bölüm 5.1 | Kapalı çevrim ifade ilişkisi |
| `docs/assets/docx-media/media/image18.png` | Bölüm 5.3 | Açık çevrim transfer fonksiyonu |
| `docs/assets/docx-media/media/image19.png` | Bölüm 5.3 | Uncompensated loop gain ifadesi |
| `docs/assets/docx-media/media/image20.png` | Bölüm 5.3 | Uncompensated Bode diyagramı |
| `docs/assets/docx-media/media/image21.png` | Bölüm 5.4 | Lead compensator Bode davranışı |
| `docs/assets/docx-media/media/image22.png` | Bölüm 5.4 | Lead compensator frekans cevabı |
| `docs/assets/docx-media/media/image23.png` | Bölüm 5.4 | Lead sonrası açık çevrim Bode |
| `docs/assets/docx-media/media/image24.png` | Bölüm 5.5 | Lag/PI compensator Bode davranışı |
| `docs/assets/docx-media/media/image25.png` | Bölüm 5.6 | PID compensator Bode eğrisi |
| `docs/assets/docx-media/media/image26.png` | Bölüm 5.7 | LT1215 op-amp gain/frequency grafiği |
| `docs/assets/docx-media/media/image27.png` | Bölüm 5.8 | Nihai açık çevrim Bode |
| `docs/assets/docx-media/media/image28.png` | Bölüm 5.8 | Hesaplanan $T(s)$ |
| `docs/assets/docx-media/media/image29.png` | Bölüm 5.8 | $T(s)$ kapalı çevrim ifadeleri |
| `docs/assets/docx-media/media/image31.png` | Bölüm 5.8 | Reference-to-output cevabı |
| `docs/assets/docx-media/media/image34.png` | Bölüm 6 | Op-amp gerçekleştirme devresi |
| `docs/assets/docx-media/media/image35.png` | Bölüm 6.1 | Sensor gain gerilim bölücü |
| `docs/assets/docx-media/media/image36.png` | Bölüm 6.2 | Compensator hedef frekans/kazanç davranışı |
| `docs/assets/docx-media/media/image37.png` | Bölüm 6.2 | Sadeleştirilmiş compensator devresi |
| `docs/assets/docx-media/media/image38.png` | Bölüm 6.2 | $R_2$ ve $C_2$ empedans davranışı |
| `docs/assets/docx-media/media/image39.png` | Bölüm 6.2 | $+20\,\text{dB/dec}$ eğim |
| `docs/assets/docx-media/media/image40.png` | Bölüm 6.2 | $Z_1/Z_2$ empedans ağı |
| `docs/assets/docx-media/media/image41.png` | Bölüm 6.2 | $Z_1/Z_2$ empedans ağı |
| `docs/assets/docx-media/media/image42.png` | Bölüm 7.3 | Yaklaşık 49.6 W çıkış gücü |
| `docs/assets/docx-media/media/image43.png` | Bölüm 7.3 | Yaklaşık 124.2 W çıkış gücü |
| `docs/assets/docx-media/media/image44.png` | Bölüm 7.4 | Statik çıkış gerilimi |
| `docs/assets/docx-media/media/image45.png` | Bölüm 7.5 | Transient çıkış gerilimi |
| `docs/assets/docx-media/media/image46.png` | Bölüm 7.6 | Output ripple |
| `docs/assets/docx-media/media/image47.png` | Bölüm 7.7 | 36 V girişte giriş gücü |
| `docs/assets/docx-media/media/image48.png` | Bölüm 7.7 | 36 V girişte çıkış gücü |
| `docs/assets/docx-media/media/image49.png` | Bölüm 7.7 | 24 V girişte çıkış gücü |
| `docs/assets/docx-media/media/image50.png` | Bölüm 7.7 | 24 V girişte giriş gücü |
| `docs/assets/docx-media/media/image51.png` | Bölüm 8 | LM5146 tipik uygulama |
| `docs/assets/docx-media/media/image52.png` | Ek-1 | Sığaç veri sayfası |
| `docs/assets/docx-media/media/image53.png` | Ek-2 | LTspice devre genel görünümü |

## Manuel Takip Gereken Öğeler

- `image12.png`, `image13.png`, `image30.png`, `image32.png`, `image33.png` çok küçük artefakt medya nesneleri gibi görünüyor; PDF render ile nihai olarak doğrulanmalı.
- Input voltage transient, input current ripple ve sıcaklık aralığı gereksinimleri raporda hedef olarak listelenmiş olsa da ayrı görsel doğrulamayla kapatılmamış.
- Büyük üçüncü taraf kaynak PDF'lerin repo içinde tutulması lisans/dağıtım açısından ayrıca değerlendirilmeli.
"""


def patch_report() -> None:
    text = REPORT.read_text(encoding="utf-8")
    marker = "# Benzetim"
    start = text.index(marker)
    REPORT.write_text(text[:start] + FINAL_SECTIONS.rstrip() + "\n", encoding="utf-8", newline="\n")


def write_auxiliary() -> None:
    VERIFICATION.write_text(VERIFICATION_CONTENT.rstrip() + "\n", encoding="utf-8", newline="\n")
    SOURCE_MAP.write_text(SOURCE_MAP_CONTENT.rstrip() + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    patch_report()
    write_auxiliary()
    print("patched final sections and wrote verification/source-map docs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
