#!/usr/bin/env python3
"""Patch the manually reviewed first half of docs/full-report.md.

This keeps the correction repeatable after regenerating docs/full-report.md from
the DOCX conversion pipeline. It replaces the content from the top of the file
through section 4.2, then leaves section 5 onward untouched for the next manual
editing pass.
"""

from __future__ import annotations

from pathlib import Path


REPORT = Path("docs/full-report.md")

FIRST_HALF = r"""<a id="kapak"></a>
# DC-DC Synchronous Alçaltıcı Dönüştürücü Tasarımı, Analizi ve Benzetimi

## Kapak ve Onay Bilgisi

**2025**

**Lisans Tezi**

**Elektrik-Elektronik Mühendisliği**

**Gökberk Güçin**

Ad SOYAD tarafından hazırlanan "TEZİN ADI" başlıklı bu tezin Lisans Tezi olarak uygun olduğunu onaylarım.

**Tarih:** xx/xx/201x

**Tez danışmanı:** Doç. Dr. Ozan GÜLBUDAK  
Karabük Üniversitesi Elektrik-Elektronik Mühendisliği Bölümü

**Jüri üyesi:** Ünvan. Ad SOYAD  
xxxx Üniversitesi xxx Mühendisliği Bölümü

**Jüri üyesi:** Ünvan. Ad SOYAD  
Karabük Üniversitesi xxxx Bölümü

<a id="abstract"></a>
# Abstract

**B. Sc. Thesis**

**DESIGN, ANALYSIS AND SIMULATION OF DC-DC SYNCHRONOUS BUCK CONVERTER**

**Gökberk Güçin 2017010215016**

**Karabük University**  
**Faculty of Engineering Department of Electrical-Electronics Engineering**

**Thesis Advisor:** Doç. Dr. Ozan GÜLBUDAK

**January 2025, 60 pages**

This undergraduate thesis focuses on the design and analysis of a synchronous DC-DC buck converter, which is widely used in power electronics for efficient voltage regulation. The study includes the systematic calculation and optimization of power stage components such as inductors, capacitors, and MOSFETs to achieve desired performance metrics. A comprehensive control strategy utilizing a PID compensator is developed to ensure stable and precise output voltage regulation under varying load and input conditions. Simulation results verify the design's efficiency, ripple control, and transient response, meeting the specified requirements. The findings demonstrate the feasibility of integrating theoretical principles with practical applications in the field of power electronics.

**Key Words:** Synchronous buck converter, voltage regulation, power electronics, PID compensator, transient response

<a id="icindekiler"></a>
# İçindekiler

- [Kapak ve Onay Bilgisi](#kapak)
- [Abstract](#abstract)
- [1. Giriş](#giris)
  - [1.1. Çalışmanın Amacı ve Kapsamı](#calismanin-amaci-ve-kapsami)
  - [1.2. Buck Converter Nedir?](#buck-converter-nedir)
- [2. Güç ve Kontrol Tasarımında İzlenen Yöntem](#guc-ve-kontrol-tasariminda-izlenen-yontem)
  - [2.1. Frekans Seçim Kuralları ve Hesaplamalar](#frekans-secim-kurallari-ve-hesaplamalar)
  - [2.2. Hesaplamalarda Kullanılacak Parametreler](#hesaplamalarda-kullanilacak-parametreler)
- [3. Güç Katı Hesaplamaları](#guc-kati-hesaplamalari)
- [4. Çevirici Durum Denklemleri](#cevirici-durum-denklemleri)
  - [4.1. ESR Etkisi](#esr-etkisi)
  - [4.2. Genel Dalga-Biçimleri](#genel-dalga-bicimleri)
- [5. Kontrolcü Tasarımı](#kontrolcu-tasarimi)
- [6. Op-Amp Devresi Gerçeklemesi](#op-amp-devresi-gerceklemesi)
- [7. Benzetim Sonuçları](#benzetim-sonuclari)
- [8. Projenin Geleceği](#projenin-gelecegi)
- [Kaynaklar](#kaynaklar)
- [Ekler](#ekler)

<a id="giris"></a>
# 1. Giriş

<a id="calismanin-amaci-ve-kapsami"></a>
## 1.1. Çalışmanın Amacı ve Kapsamı

Bu çalışmanın amacı, belirlenen tasarım gereksinimlerini karşılayan bir DC-DC senkron buck konvertörünün tasarımını, analizini ve benzetimini gerçekleştirmektir. Çalışma, buck konvertör devresinin temel prensiplerini, güç katı hesaplamalarını ve kontrolcü tasarımını ele almaktadır. Tasarlanan sistem, verilen giriş voltaj aralığında çıkış voltajını sabit tutmayı hedeflemekte ve yüksek verimlilikle çalışması planlanmıştır.

<a id="buck-converter-nedir"></a>
## 1.2. Buck Converter Nedir?

Buck converter, yüksek giriş gerilimini daha düşük bir çıkış gerilimine dönüştüren bir DC-DC dönüştürücü türüdür. Bu tür devreler, enerji kaybını azaltarak verimli bir şekilde enerji dönüşümü sağlar. Anahtar transistör, diyot, bobin ve kapasitör gibi temel elemanlardan oluşan buck converter, çeşitli elektronik cihazlarda güç yönetimi için yaygın olarak kullanılır.

<a id="guc-ve-kontrol-tasariminda-izlenen-yontem"></a>
# 2. Güç ve Kontrol Tasarımında İzlenen Yöntem

Okuduğum kaynaklarda önce güç katı (Power Stage) hesaplamaları yapılıyor. Akım, gerilim değerleri, elemanların değerleri, kayıpları belirleniyor. Ardından kontrolcünün tasarımına geçiliyor. Güç ile kontrol tasarımı öncelik-sonralık ilişkisi olsa da birbirinden ayrık iki farklı süreçmiş gibi anlatılıyor.

Kontrolcü tasarımında, bu güç katında belirlediğimiz parametreler kullanılıyor. Bu yöntem izlenerek yapılan çalışmada, frekansları istenen yerde tutmak zor olabiliyor. Güç aşamasına dönüp değeri yeniden değiştirmek zorunda kalınabiliyor.

Örneğin güç katı aşamasındayken, serbestçe seçtiğimiz bir değer, kontrolcü aşamasında tasarımı zorlaştırabiliyor. Oysaki bu serbest seçimin, ileride kısıtlayıcı bir seçim olacağını bilmiş olsaydık, bunu yapmazdık.

Sonuç olarak, güç ve kontrol tasarımını bütünleşik biçimde düşünerek, birbirlerini etkileyen parametreleri tasarım sürecinin başından itibaren göz önünde bulundurmak, tasarımın daha sağlıklı ve kolay bir şekilde yapılmasına yardımcı oluyor.

<a id="frekans-secim-kurallari-ve-hesaplamalar"></a>
## 2.1. Frekans Seçim Kuralları ve Hesaplamalar

Kaynak [1] ve [2]'deki Type-3 Compensator'lü bir kontrolcü sistemindeki frekanslarla ilgili tavsiye edilen seçim kurallarını bir araya getirdim.

- $f_s = f_{p2} = f_{ESR}$
- $f_c = f_s / 10$
- $f_L < f_c / 10$
- $f_0$, $f_z$'den küçük; $f_L$'den büyük olacak.

![Type-3 compensator frekans ilişkileri](assets/docx-media/media/image1.png)

*Şekil 2.1 - Type-3 compensator için kullanılan frekans ilişkileri.*

Bu koşulları birleştirip, tüm frekansları yatay eksende büyüklük sırasına göre sıraladım.

![Frekansların büyüklük sırasına göre dizilimi](assets/docx-media/media/image2.png)

*Şekil 2.2 - Tasarımda kullanılan frekansların hedef sıralaması.*

Denklemi belli olan frekanslar ve seçimini bizim yaptığımız parametreler var:

- $f_{ESR} = \dfrac{1}{2 \pi C R_{ESR}}$
- $f_0 = \dfrac{1}{2 \pi \sqrt{CL}}$
- $f_s = 100\,\text{kHz}$ ve $\theta = 52^\circ$

Yukarıdaki tüm koşullar ve denklemler dikkate alınarak hesaplama yaptığımızda:

$$
f_s = 100\,\text{kHz}
$$

$$
f_{p2} = f_{ESR} = f_s = 100\,\text{kHz}
$$

$$
f_{ESR} = \frac{1}{2 \pi C R_{ESR}} = 100\,\text{kHz}
$$

Buradan:

$$
C R_{ESR} = 1.59\,\mu
$$

elde edilir.

Diğer frekans seçimleri:

- $f_c = f_s / 10 = 10\,\text{kHz}$
- $f_z = 3.44\,\text{kHz}$
- $f_{p1} = 29\,\text{kHz}$
- $f_L \le 1\,\text{kHz}$ olduğundan $f_L = 1\,\text{kHz}$ seçildi.

Tasarım şartı:

$$
f_L < f_0 < f_z
$$

olduğu için:

$$
1\,\text{kHz}
<
\frac{1}{2 \pi \sqrt{CL}}
<
3.44\,\text{kHz}
$$

Buradan:

$$
2.44\,\text{n} < CL < 25.3\,\text{n}
$$

sonucu elde edilir.

Kontrolcü kısmından elde edilip güç hesabında kullanılacak iki ana kısıt:

$$
2.44\,\text{n} < CL < 25.3\,\text{n}
$$

ve

$$
C R_{ESR} = 1.59\,\mu
$$

<a id="hesaplamalarda-kullanilacak-parametreler"></a>
## 2.2. Hesaplamalarda Kullanılacak Parametreler

| Parametre | Değer |
|---|---:|
| Giriş gerilimi, $V_{in,max}$ | $36\,\text{V}$ |
| Giriş gerilimi, $V_{in,min}$ | $24\,\text{V}$ |
| Çıkış gücü | $50\,\text{W} - 125\,\text{W}$ |
| Çıkış gerilimi, $V_o$ | $14\,\text{V}$ |
| Minimum çıkış akımı, $I_{o,min}$ | $\dfrac{50\,\text{W}}{14\,\text{V}} = 3.571\,\text{A}$ |
| Maksimum çıkış akımı, $I_{o,max}$ | $\dfrac{125\,\text{W}}{14\,\text{V}} = 8.92\,\text{A}$ |
| Çıkış gerilimi tepeden tepeye dalgalanma, $\Delta V_o$ | $0.100\,\text{V}$ |
| Minimum yük direnci, $R_{load,min}$ | $\dfrac{V_o}{I_{o,max}} = \dfrac{14\,\text{V}}{8.92\,\text{A}} = 1.569\,\Omega$ |
| Maksimum yük direnci, $R_{load,max}$ | $\dfrac{V_o}{I_{o,min}} = \dfrac{14\,\text{V}}{3.57\,\text{A}} = 3.921\,\Omega$ |

<a id="guc-kati-hesaplamalari"></a>
# 3. Güç Katı Hesaplamaları

Buck converter, en yüksek giriş gerilimindeyken ($36\,\text{V}$), en yüksek gücü ($125\,\text{W}$) verebilecek biçimde tasarlandı. Yüksek gerilimdeyken duty cycle $D$ daha düşük olmak zorunda.

Küçük $D$; ana MOSFET'in daha kısa süre iletimde kalması, bobin ve sığacın dolması için daha az süreleri var demektir. Dolmaları için tanınan süre daha kısa olsa da aynı miktarda enerjiyi depolamak zorundalar; yüksek akım çekmeliler ve yüksek gerilime çıkabilmelidirler. Sabit çıkış gerilimi için bu, $L$ ve $C$ değerlerinin büyümesi anlamına gelir.

Yüksek çıkış gücü de düşük güce göre zorlayıcı durumdur.

## 3.1. İlk Güç Katı Hesapları

| Adım | Hesap / seçim | Sonuç / yorum |
|---|---|---|
| Adım 1: Duty cycle aralığını belirlemek | $\dfrac{V_o}{V_{in,max}} \le D \le \dfrac{V_o}{V_{in,min}}$<br><br>$\dfrac{14\,\text{V}}{36\,\text{V}} \le D \le \dfrac{14\,\text{V}}{24\,\text{V}}$ | $D_{min} = 0.3888$<br>$D_{max} = 0.5833$ |
| Adım 2: Anahtarlama frekansı | $f_s = 100\,\text{kHz}$ | Bu değer frekans planında seçilmişti. |
| Adım 3: Tepeden tepeye bobin akımı dalgalanması | $\Delta I_L = 0.2 \times I_{o,max}$<br>$= 0.2 \times 8.92$<br>$= 1.784\,\text{A}$ | İlk hesap değeri. Bobin akımının $I_{o,max}$ akımının yüzde 20'si kadar tepeden tepeye dalgalanması istendi. Kaynaklar bobin akımı dalgalanma oranının yüzde 20-40 arasında seçilebileceğini belirtiyor. |
| Adım 4: Bobin değerinin hesaplanması | $L = \dfrac{V_o(1-D_{min})}{\Delta I_L f_s}$<br>$= \dfrac{14(1-0.3888)}{1.784 \times 100\,\text{kHz}}$ | $L = 47.94\,\mu\text{H}$ ilk hesap değeri. |
| Adım 5: Sığacın hesaplanması | $C_{min} = \dfrac{1-D_{min}}{8L(\Delta V_o/V_o)f_s^2}$<br>$= \dfrac{1-0.3888}{8(47.94\,\mu\text{H})(0.1/14)(100\,\text{kHz})^2}$ | $C \ge 22.3\,\mu\text{F}$ ilk hesap değeri. |
| Adım 6: Sığacın izin verilen en yüksek ESR değeri | $ESR \le \dfrac{\Delta V_o}{\Delta I_L}$<br>$ESR \le \dfrac{0.1}{1.784}$ | $ESR \le 56\,\text{m}\Omega$ ilk hesap değeri. |
| Adım 7: Frekans kısıtlarıyla kontrol | Önceki frekans kısıtları: $2.44\,\text{n} < CL < 25.3\,\text{n}$ ve $C R_{ESR} = 1.59\,\mu$ | $C \ge 22.3\,\mu\text{F}$, $L = 47.94\,\mu\text{H}$, $ESR \le 56\,\text{m}\Omega$ değerleri birlikte kontrol edildi. |

İlk sığaç hesabı ile $C R_{ESR}$ koşulunu kontrol edersek:

$$
R_{ESR} \approx \frac{1.59\,\mu}{22\,\mu\text{F}} = 71.3\,\text{m}\Omega
$$

Bu değer $56\,\text{m}\Omega$ sınırına yakın fakat koşulu sağlamıyor gibi görünür. Sığacın capacitance değeri arttıkça ESR değeri düşme eğilimindedir. Bu yüzden $C$ biraz artırılıp $ESR$ biraz düşürülerek:

$$
C R_{ESR} = 1.59\,\mu
$$

koşulunu sağlamak mümkündür.

ESR koşulunu sağlamak için:

$$
C > 28.4\,\mu\text{F}
$$

olması gerekir.

$L$ sabit $47.94\,\mu\text{H}$ tutulursa, rezonans frekansı şartını sağlayacak sığaç aralığı yaklaşık:

$$
44\,\mu\text{F} < C < 527\,\mu\text{F}
$$

olmalıdır. Bu aralık, aşağıdaki rezonans frekansı şartını korumak içindir:

$$
f_L < f_0 < f_z
$$

yani:

$$
1\,\text{kHz} < f_0 < 3.44\,\text{kHz}
$$

Bu nedenle:

$$
C = 82\,\mu\text{F}
$$

değerinde bir sığaç seçildi. Çünkü $82\,\mu\text{F}$ sığacın ESR değeri yaklaşık $20\,\text{m}\Omega$ mertebesindedir. Böylece:

$$
C R_{ESR} \approx 1.59\,\mu
$$

koşulu sağlanmış olur.

$f_0 = 2.5\,\text{kHz}$ ve $C = 82\,\mu\text{F}$ iken bobin değeri:

$$
f_0 = \frac{1}{2\pi\sqrt{LC}}
$$

bağıntısından:

$$
L \approx 49.42\,\mu\text{H}
$$

olarak bulunur.

Yeni $L$ ve $C$ değerlerine göre hesap yenilenmelidir.

## 3.2. Güncellenmiş L ve C Değerleriyle Hesaplar

| Adım | Hesap / sonuç | Yorum |
|---|---|---|
| Adım 8: Bobin akımı dalgalanması | $\Delta I_L = \dfrac{V_o(1-D_{min})}{L f_s}$<br>$\Delta I_L \approx 1.714\,\text{A}$ | Bobin değeri arttığı için bobin akımının tepeden tepeye dalgalanması azaldı. |
| Adım 9: Bobin tepe akımı | $I_{L,tepe} = I_{o,max} + \dfrac{\Delta I_L}{2}$<br>$= 8.92 + \dfrac{1.714}{2}$ | $I_{L,tepe} = 9.777\,\text{A}$ |
| Adım 9.2: Bobin en küçük akımı | $I_{L,küçük,tepe} = I_{o,min} - \dfrac{\Delta I_L}{2}$<br>$= 3.571 - \dfrac{1.714}{2}$ | $I_{L,küçük,tepe} = 2.714\,\text{A} > 0\,\text{A}$ olduğundan converter CCM'de kalır. |
| Adım 10: Bobin RMS akımı | $I_{L,RMS} = \sqrt{I_L^2 + \left(\dfrac{\Delta I_L/2}{\sqrt{3}}\right)^2}$<br>$I_{L,RMS} = \sqrt{10.634^2 + \left(\dfrac{1.714/2}{\sqrt{3}}\right)^2}$ | $I_{L,RMS} = 10.645\,\text{A}$ |
| Adım 11: Yeni C ve L ile çıkış dalgalanması | $\Delta V_o = \dfrac{V_o(1-D_{min})}{8LCf_s^2}$<br>$= \dfrac{14(1-0.3888)}{8(47.94\,\mu\text{H})(82\,\mu\text{F})(100\,\text{kHz})^2}$ | $\Delta V_o \approx 27\,\text{mV}$ |
| Adım 12: Sığaç RMS akımı | $I_{C,RMS} = \sqrt{I_C^2 + \left(\dfrac{\Delta I_C/2}{\sqrt{3}}\right)^2}$<br>$I_{C,RMS} = \sqrt{0^2 + \left(\dfrac{1.714/2}{\sqrt{3}}\right)^2}$ | $I_{C,RMS} = 0.4947\,\text{A}$; sığaç bu akıma dayanabilmelidir. |

$L$ ve $C$ değerlerinin artışı, çıkıştaki gerilim dalgalanmasını $100\,\text{mV}$ seviyesinden yaklaşık $27\,\text{mV}$ seviyesine düşürdü. Bu, kapalı çevrimin frekanslarının yerlerini tasarım sürecinin en başından itibaren gözetmenin bir sonucu olarak değerlendirilebilir.

![Güncellenmiş güç katı hesaplarına ait şekil](assets/docx-media/media/image3.png)

*Şekil 3.1 - Kaynak DOCX'teki güç katı hesap akışında kullanılan devre/hesap görseli.*

## 3.3. Duty Cycle Hesabının LTspice ile Kontrolü

Adım 1'de yapılan duty cycle hesabı LTspice benzetiminde kontrol edildi. Steady-state iken, giriş gerilimi $36\,\text{V}$ olduğunda:

$$
3.91\,\mu\text{s} \approx D_{min}\left(\frac{1}{100\,\text{kHz}}\right)
$$

olarak görülmektedir. Bu değer hesaplanan $D_{min}$ ile uyumludur.

Benzer şekilde giriş gerilimi $24\,\text{V}$ iken $D_{max}$ olduğu görülebilir. Ayrıca bu $D_{min}$ ve $D_{max}$ değerleri steady-state için geçerlidir. Transient durumlarında kontrolcünün verdiği emirle $D$, yaklaşık $0.9$ ile $0.1$ arasında değişir.

![36 V giriş için duty-cycle LTspice kontrolü](assets/docx-media/media/image4.jpeg)

*Şekil 3.2 - 36 V girişte steady-state duty-cycle kontrolü.*

![24 V giriş için duty-cycle LTspice kontrolü](assets/docx-media/media/image5.png)

*Şekil 3.3 - 24 V girişte duty-cycle davranışı ve LTspice kontrolü.*

## 3.4. Güç Katı Değer Özeti

| Büyüklük | Değer |
|---|---:|
| Giriş gerilimi, $V_{s,max}$ | $36\,\text{V}$ |
| Giriş gerilimi, $V_{s,min}$ | $24\,\text{V}$ |
| Maksimum çıkış gücü, $P_{max}$ | $125\,\text{W}$ |
| Minimum çıkış gücü | $50\,\text{W}$ |
| Çıkış gerilimi, $V_o$ | $14\,\text{V}$ |
| Çıkış gerilimi tepeden tepeye dalgalanma | $\Delta V_o \approx 27\,\text{mV}$ |
| Sığaç | $C = 82\,\mu\text{F}$ |
| Sığaç ESR | $R_{ESR} = 19.39\,\text{m}\Omega$ |
| MOSFET iletim direnci | $R_{DS(on)} = 15\,\text{m}\Omega$ |
| Bobin seri direnci | $R_L = 15\,\text{m}\Omega$ |
| Minimum yük direnci | $R_{load,min} = 1.569\,\Omega$ |
| Maksimum yük direnci | $R_{load,max} = 3.921\,\Omega$ |
| Minimum duty cycle | $D_{min} = 0.3888$ |
| Maksimum duty cycle | $D_{max} = 0.5833$ |

<a id="cevirici-durum-denklemleri"></a>
# 4. Çevirici Durum Denklemleri

![Buck converter durum denklemleri](assets/docx-media/media/image6.png)

*Şekil 4.1 - Kaynak DOCX'teki buck converter durum denklemleri.*

Zaman alanında buck converter'ın tüm davranışını temsil eden bu denklemleri, LTspice benzetim sonuçları ile denklemlerden birkaçını doğrulamaya çalışacağım.

<a id="esr-etkisi"></a>
## 4.1. ESR Etkisi

ESR etkisi çıkış gerilimini doğrudan etkiler. Kaynak belgede kullanılan ifade:

$$
V_{out} = v + R_{ESR}(i - i_{load})
$$

şeklindedir.

![ESR etkisinin çıkış gerilimi üzerindeki etkisi](assets/docx-media/media/image7.png)

*Şekil 4.2 - ESR'nin çıkış gerilimi dalgalanmasını artıran etkisi.*

Bu görsel ve ifade ile ESR direncinin neden düşük tutulması gerektiği gösterilmiş olur. ESR, çıkış gerilimindeki dalgalanmayı artırır; bu nedenle sığaç seçimi yalnızca kapasite değerine göre değil, ESR davranışına göre de yapılmalıdır.

Kaynak belgede ESR etkisi sonrasında akım ve gerilimlerin genel dalga biçimlerine geçilir.

![Akım ve gerilimlerin genel dalga biçimleri](assets/docx-media/media/image8.png)

*Şekil 4.3 - Buck converter için genel akım ve gerilim dalga biçimleri.*

<a id="genel-dalga-bicimleri"></a>
## 4.2. Genel Dalga-Biçimleri

Genel dalga biçimleri bölümünde, anahtarlama periyodu boyunca akım ve gerilimlerin nasıl değiştiği gösterilir. Bu kısım, güç katı hesaplarında kullanılan $D$, $D'$, $\Delta I_L$, çıkış sığacı akımı ve çıkış gerilimi dalgalanması ilişkilerini görsel olarak destekler.

![Genel dalga biçimleri için küçük işaret/etiket görselleri](assets/docx-media/media/image9.png)

![Genel dalga biçimleri için denklem/etiket görseli](assets/docx-media/media/image10.png)

![Buck converter genel dalga biçimleri](assets/docx-media/media/image11.png)

*Şekil 4.4 - Buck converter akım ve gerilim dalga biçimleri.*

> TODO: Kaynak DOCX bu noktada `image12.png` ve `image13.png` adlı iki adet 2x2 piksel medya nesnesi de içeriyor. Bunlar görünür teknik figür gibi durmadığı için ana akışa gömülmedi; PDF ile karşılaştırılarak boş/artefakt oldukları doğrulanmalı.

<a id="kontrolcu-tasarimi"></a>
"""


def find_control_heading(lines: list[str]) -> int:
    for index, line in enumerate(lines):
        normalized = line.lower()
        if normalized.startswith("# 5. kontrolcü tasarımı"):
            return index
        if normalized.startswith("# kontrolcu tasar"):
            return index
        if normalized.startswith("# kontrolc"):
            return index
    raise RuntimeError("Could not find the section 5 control heading boundary.")


def main() -> int:
    text = REPORT.read_text(encoding="utf-8")
    lines = text.splitlines()
    boundary = find_control_heading(lines)
    tail = lines[boundary + 1 :]
    new_text = FIRST_HALF.rstrip() + "\n# 5. Kontrolcü Tasarımı\n"
    if tail:
        new_text += "\n".join(tail).rstrip() + "\n"
    REPORT.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"patched {REPORT} through section 4.2; preserved {len(tail)} tail lines")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
