#!/usr/bin/env python3
"""Patch the control and compensator sections of docs/full-report.md.

This script is intentionally repeatable after regenerating the Pandoc draft. It
replaces section 5 through section 6.2, preserving section 7 onward.
"""

from __future__ import annotations

from pathlib import Path


REPORT = Path("docs/full-report.md")

CONTROL_SECTIONS = r"""# 5. Kontrolcü Tasarımı

Amaç, çıkış gerilimini sabit ve iyi kontrol edilmiş bir değerde tutmaktır. Bu bölümde önce küçük işaret modelinden açık çevrim transfer fonksiyonuna gidilir; ardından uncompensated loop gain üzerinden gerekli kompanzasyon kazancı ve faz katkısı belirlenir. Son olarak lead, lag ve PID birleşimi op-amp ile gerçekleştirilecek devreye bağlanır.

![Kontrolcü tasarımına geçişte kullanılan kaynak diyagram](assets/docx-media/media/image14.png)

*Şekil 5.1 - Kaynak DOCX'te kontrolcü tasarımına girişte verilen diyagram.*

## 5.1. Sistem Block Diagramı ve Küçük İşaret Modeli

![Sistemin block diagramı](assets/docx-media/media/image15.png)

*Şekil 5.2 - Buck converter, sensor gain, PWM ve compensator bloklarını içeren kontrol sistemi.*

![Kapalı çevrim ifade ilişkisi 1](assets/docx-media/media/image16.png)

![Kapalı çevrim ifade ilişkisi 2](assets/docx-media/media/image17.png)

*Şekil 5.3 - Küçük işaret modelinde kullanılan kapalı çevrim ifade ilişkileri.*

Küçük işaret AC modeli kullanıldı. Bu modelde $T(s)$ kontrolcünün açık çevrim transfer fonksiyonudur. $T(s)$ çevrim kazancı yüksek tasarlanarak çıkışın sadece referansı takip etmesi ve bozucuların etkilerinin en aza indirilmesi hedeflenir. Kaynak belgede özellikle giriş gerilimi ve yük akımı bozucuları:

$$
\hat{v}_g,\qquad \hat{i}_{load}
$$

olarak gösterilir.

## 5.2. Kontrolcü Hesabı

PWM rampa genliği ve referans gerilimi:

$$
V_m = 4\,\text{V}
$$

$$
V_{ref} = 1.8\,\text{V}
$$

olarak belirlendi. Bu değerler kullanılacak PWM ve op-amp çalışma aralığı ile uyumludur.

### 5.2.1. Sensor Gain, $H(s)$

Sensör kazancı, sıfır hata durumunda çıkış gerilimini referans gerilimine ölçekleyecek şekilde seçilir:

$$
V_e = V_{ref} - H V
$$

Sıfır hata için:

$$
0 = 1.8 - H \cdot 14
$$

Dolayısıyla:

$$
H \cdot V = 1.8
$$

ve:

$$
H = \frac{1.8}{14} = 0.12857
$$

olmalıdır. Sensör kazancı yaklaşık:

$$
H \approx 0.12857
$$

olarak alınır.

### 5.2.2. Control-to-Output Transfer Fonksiyonu, $G_{vd}(s)$

$G_{vd}(s)$, duty cycle küçük işaret değişiminin çıkış gerilimine etkisini gösteren control-to-output transfer fonksiyonudur:

$$
G_{vd}(s) = \frac{\hat{v}}{\hat{d}}
$$

Bu transfer fonksiyonu çeviricinin fiziksel bileşenlerinden türetilir. $\hat{d}(t)$ üzerindeki küçük değişimlerin çıkış gerilimine olan etkisini inceler. Çıkış geriliminin istenen seviyede tutulabilmesi için $\hat{d}(t)$ değerinin nasıl ayarlanması gerektiği bu fonksiyonla belirlenir.

Kaynak belgede kullanılan form:

$$
G_{vd}(s)
=
\frac{V}{D}
\cdot
\frac{1 + \frac{s}{\omega_{ESR}}}
{1 + \frac{1}{Q}\frac{s}{\omega_0} + \left(\frac{s}{\omega_0}\right)^2}
$$

Burada rezonans kutup çifti frekansı:

$$
f_0 = \frac{1}{2\pi\sqrt{LC}}
$$

ve seçilen değerlerle:

$$
f_0 = \frac{1}{2\pi\sqrt{82\,\mu\text{F}\cdot 49.42\,\mu\text{H}}}
\approx 2.5\,\text{kHz}
$$

ESR sıfırı:

$$
f_{ESR} = \frac{1}{2\pi C R_{ESR}}
$$

olup:

$$
f_{ESR}
=
\frac{1}{2\pi \cdot 82\,\mu\text{F}\cdot 19.39\,\text{m}\Omega}
\approx 100\,\text{kHz}
$$

olarak bulunur.

Kayıp kaynaklı kalite faktörü:

$$
Q_{loss}
=
\frac{\sqrt{L/C}}{R_{ESR}+R_L}
=
\frac{\sqrt{49.42\,\mu\text{H}/82\,\mu\text{F}}}{19.39\,\text{m}\Omega + 30\,\text{m}\Omega}
$$

$$
Q_{loss} = 15.718 \quad \text{veya} \quad 23.92\,\text{dB}
$$

Yük kaynaklı kalite faktörü:

$$
Q_{load}
=
\frac{R}{\sqrt{L/C}}
=
\frac{1.569}{\sqrt{49.42\,\mu\text{H}/82\,\mu\text{F}}}
=
2.02
$$

Bu değer dB olarak yaklaşık:

$$
20\log_{10}(2.02)=6.112\,\text{dB}
$$

Toplam kalite faktörü paralel birleşim olarak alınır:

$$
Q = Q_{loss}\parallel Q_{load}
=
\frac{Q_{loss}Q_{load}}{Q_{loss}+Q_{load}}
$$

$$
Q
=
\frac{15.718\cdot 2.02}{15.718+2.02}
=
1.789
<
2.02
$$

Böylece control-to-output transfer fonksiyonu sayısal olarak:

$$
G_{vd}(s)
=
\frac{14}{0.3888}
\cdot
\frac{1 + \frac{s}{2\pi\cdot 100\,\text{kHz}}}
{1 + \frac{1}{1.789}\frac{s}{2\pi\cdot 2.5\,\text{kHz}}
+ \left(\frac{s}{2\pi\cdot 2.5\,\text{kHz}}\right)^2}
$$

şeklinde yazılabilir.

PWM kazancı dahil edildiğinde düşük frekans kazancı:

$$
G_{vd0}\cdot\frac{1}{V_m}
=
\frac{14}{0.3888}\cdot\frac{1}{4}
\approx 9
$$

yani:

$$
20\log_{10}(9) \approx 19.08\,\text{dB}
$$

olur.

## 5.3. Uncompensated Loop Gain

Compensator etkisi henüz yokken $G_c(s)=1$ alınır ve açık çevrim kazancı $T_u(s)$ hesaplanır.

Genel açık çevrim transfer fonksiyonu:

$$
T(s)
=
H_{sense}
\cdot
\frac{1}{V_m}
\cdot
G_{vd}(s)
\cdot
G_c(s)
$$

![Açık çevrim transfer fonksiyonu blok ifadesi](assets/docx-media/media/image18.png)

*Şekil 5.4 - $T(s)$ açık çevrim transfer fonksiyonunun kaynak DOCX'teki gösterimi.*

Uncompensated durumda:

$$
T_u(s)
=
H_{sense}
\cdot
\frac{1}{V_m}
\cdot
G_{vd}(s)
\cdot
1
$$

![Uncompensated loop gain ifadesi](assets/docx-media/media/image19.png)

*Şekil 5.5 - $T_u(s)$ uncompensated loop gain ifadesi.*

Düşük frekans kazancı:

$$
T_{u0}
=
H
\cdot
\frac{1}{V_m}
\cdot
\frac{V}{D}
$$

Sayısal olarak:

$$
T_{u0}
=
0.12857
\cdot
\frac{1}{4}
\cdot
\frac{14}{0.3888}
\approx
1.15713
$$

Bu değer dB cinsinden yaklaşık:

$$
20\log_{10}(1.15713) \approx 1.27\,\text{dB}
$$

olur.

![Uncompensated loop gain Bode diyagramı](assets/docx-media/media/image20.png)

*Şekil 5.6 - Compensator eklenmeden önce açık çevrim Bode diyagramı.*

Uncompensated kazancı hesaplamaktaki amaç, compensator'den ne kadar kazanç elde edilmesi gerektiğini bulmaktır. Hedeflenen crossover frekansı:

$$
f_c = \frac{f_s}{10} = 10\,\text{kHz}
$$

olarak seçildi. Bu frekansta loop gain'i $0\,\text{dB}$ seviyesine çıkarmak için yaklaşık:

$$
22.3\,\text{dB}
$$

kazanç artışı gerekir.

Ayrıca hedef $f_c$ noktasındaki phase margin yaklaşık $14^\circ$ seviyesindedir. Loop gain içinde pratik devre ve model kaynaklı ek bozulmalar da olacağı için gerçek phase margin bunun da altına düşebilir. Bu nedenle faz katkısı sağlayan bir lead compensator gereklidir.

## 5.4. Lead (PD) Compensator Eklenmesi

Lead compensator ile hedef:

$$
f_c \approx 10\,\text{kHz}
$$

ve:

$$
PM \approx 53^\circ
$$

olarak seçildi. Phase margin'in $53^\circ$ seçilmesinin nedeni, kapalı çevrim $Q$ factor değerini yaklaşık $1$ yapan dengeli bir noktaya karşılık gelmesidir. Bu seçim hem kararlı hem de hızlı tepki için uygun bir denge sağlar.

![Lead compensator Bode şekli](assets/docx-media/media/image21.png)

*Şekil 5.7 - Lead compensator'ın faz artırıcı Bode davranışı.*

Lead compensator transfer fonksiyonu:

$$
G_c(s)
=
G_{c0}
\frac{1+\frac{s}{\omega_z}}
{1+\frac{s}{\omega_{p1}}}
$$

şeklinde yazılır. Eklenen lead compensator'ın sıfırı $f_z$ frekansında, kutbu ise $f_{p1}$ frekansındadır. Kutup, sıfırdan daha yüksek frekanstadır.

Lead compensator'ın phase margin'i en çok artırdığı frekans:

$$
f_{\varphi,max}
=
\sqrt{f_z f_{p1}}
$$

frekansıdır. Üstteki Bode diyagramı da bunu gösterir. Faz katkısının hedef crossover frekansında en yüksek olması istendiğinden:

$$
f_c
=
10\,\text{kHz}
=
f_{\varphi,max}
=
\sqrt{f_z f_{p1}}
$$

ve:

$$
\theta = 53^\circ
$$

olarak alınır.

Lead compensator frekansları:

$$
f_z
=
f_c
\sqrt{\frac{1-\sin(\theta)}{1+\sin(\theta)}}
$$

$$
f_z
=
10\,\text{kHz}
\sqrt{\frac{1-\sin(53^\circ)}{1+\sin(53^\circ)}}
\approx
3.44\,\text{kHz}
$$

ve:

$$
f_{p1}
=
f_c
\sqrt{\frac{1+\sin(\theta)}{1-\sin(\theta)}}
$$

$$
f_{p1}
=
10\,\text{kHz}
\sqrt{\frac{1+\sin(53^\circ)}{1-\sin(53^\circ)}}
\approx
29\,\text{kHz}
$$

olarak bulunur.

Bu frekans değerleri güç katı tasarımında zaten dikkate alınmıştı. Böylece güç katı ile kontrolcü tasarımı birbirinden kopuk değil, aynı frekans planını sağlayacak şekilde seçilmiş olur.

Lead compensator'ın DC kazancı:

$$
G_{c0}
=
\frac{1}{T_{u0}}
\left(\frac{f_c}{f_0}\right)^2
\sqrt{\frac{f_z}{f_{p1}}}
$$

Sayısal olarak:

$$
G_{c0}
=
\frac{1}{1.15713}
\left(\frac{10\,\text{kHz}}{2.5\,\text{kHz}}\right)^2
\sqrt{\frac{3.44\,\text{kHz}}{29\,\text{kHz}}}
$$

$$
G_{c0}
\approx
4.762
$$

Bu değer dB olarak:

$$
20\log_{10}(4.762)
\approx
13.56\,\text{dB}
$$

olur.

Lead compensator'ın $f_c$ frekansındaki kazancı:

$$
G_c(f_c)
=
G_{c0}
\sqrt{\frac{f_{p1}}{f_z}}
$$

$$
G_c(f_c)
=
4.762
\sqrt{\frac{29\,\text{kHz}}{3.44\,\text{kHz}}}
\approx
13.826
$$

Bu da:

$$
20\log_{10}(13.826)
\approx
22.8\,\text{dB}
$$

kazanç artışına karşılık gelir. Sonuç, hedeflenen $f_c$ frekansında ihtiyaç duyulan yaklaşık $22.3\,\text{dB}$ artışla uyumludur.

Lead compensator değerleriyle Bode diyagramı çizdirilirken, ileride açıklanacak op-amp kutbu da transfer fonksiyonuna eklendi. Bu op-amp kutbu:

$$
f_{p2} = 100\,\text{kHz}
$$

olarak alınır.

Bu durumda lead compensator:

$$
G_c(s)
=
G_{c0}
\frac{1+\frac{s}{\omega_z}}
{\left(1+\frac{s}{\omega_{p1}}\right)
\left(1+\frac{s}{\omega_{p2}}\right)}
$$

ve sayısal olarak:

$$
G_c(s)
=
4.762
\frac{1+\frac{s}{2\pi\cdot 3.44\,\text{kHz}}}
{\left(1+\frac{s}{2\pi\cdot 29\,\text{kHz}}\right)
\left(1+\frac{s}{2\pi\cdot 100\,\text{kHz}}\right)}
$$

şeklindedir.

![Lead compensator frekans cevabı](assets/docx-media/media/image22.png)

*Şekil 5.8 - Lead compensator'ın Bode diyagramı.*

Lead compensator eklenmiş haliyle açık çevrim $T(s)$ Bode diyagramı:

![Lead compensator eklenmiş açık çevrim Bode diyagramı](assets/docx-media/media/image23.png)

*Şekil 5.9 - Lead compensator eklendikten sonra açık çevrim $T(s)$ Bode diyagramı.*

## 5.5. Lag (PI) Compensator Eklenmesi

![Lag/PI compensator Bode şekli](assets/docx-media/media/image24.png)

*Şekil 5.10 - Lag/PI compensator'ın düşük frekans kazancı artıran davranışı.*

Lag compensator transfer fonksiyonu:

$$
G_c(s)
=
G_{c\infty}
\left(1+\frac{\omega_L}{s}\right)
$$

şeklinde yazılır. Daha önce:

$$
f_L = 1\,\text{kHz}
$$

seçilmişti. Pratik kural olarak $f_L$, $f_c$'den en az 10 kat düşük olmalıdır. Burada:

$$
f_L = \frac{f_c}{10}
$$

koşulu sağlanmaktadır.

Eklenen sıfır normal sıfırdan farklıdır; kaynak belgede "inverted zero" olarak not edilmiştir.

Lag ve lead kazançlarının birleştirileceği ortak kazanç:

$$
G_{c0} = G_{c\infty} = G_{cm}
$$

olarak alınır.

$$
G_{c\infty} = 4.762
$$

Böylece lag compensator:

$$
G_c(s)
=
4.762
\left(1+\frac{2\pi\cdot 1\,\text{kHz}}{s}\right)
$$

şeklindedir.

## 5.6. PID Compensator Birleştirilmiş Hali

Lead ve lag parçaları birleştirildiğinde kullanılacak PID compensator:

$$
G_c(s)
=
G_{cm}
\frac{
\left(1+\frac{s}{\omega_z}\right)
\left(1+\frac{\omega_L}{s}\right)
}{
\left(1+\frac{s}{\omega_{p1}}\right)
\left(1+\frac{s}{\omega_{p2}}\right)
}
$$

olur.

Sayısal değerlerle:

$$
G_c(s)
=
4.762
\frac{
\left(1+\frac{s}{2\pi\cdot 3.44\,\text{kHz}}\right)
\left(1+\frac{2\pi\cdot 1\,\text{kHz}}{s}\right)
}{
\left(1+\frac{s}{2\pi\cdot 29\,\text{kHz}}\right)
\left(1+\frac{s}{2\pi\cdot 100\,\text{kHz}}\right)
}
$$

![PID compensator Bode eğrisi](assets/docx-media/media/image25.png)

*Şekil 5.11 - Kullanılacak $G_c(s)$ PID compensator Bode eğrisi.*

## 5.7. Op-Amp ve Kutup Etkisi

Tasarımda kullanılan LT1215 op-amp'ın yüksek frekanslara doğru gidildikçe kazancını koruyamaması bir kutup ile temsil edilir. Bu kutup:

$$
f_{p2} = 100\,\text{kHz}
$$

olarak eklenmiştir.

Lead compensator'ın yüksek frekanstaki kazanç gereksinimi:

$$
G_{c0}\frac{f_{p1}}{f_z}
=
4.762\frac{29\,\text{kHz}}{3.44\,\text{kHz}}
\approx
40.144
$$

olur. Bu kazanç dB olarak:

$$
20\log_{10}(40.144)
\approx
32.07\,\text{dB}
$$

seviyesindedir.

Op-amp'ın bu kazanç değerini yaklaşık $100\,\text{kHz}$ frekansına kadar verebildiği, aşağıdaki voltage gain vs frequency grafiğinden kontrol edilir.

![LT1215 op-amp gain-frequency grafiği](assets/docx-media/media/image26.png)

*Şekil 5.12 - LT1215 op-amp için kazanç/frekans kısıtı.*

## 5.8. Açık Çevrim Transfer Fonksiyonu, $T(s)$

Compensator, power stage ve sensor gain bir araya getirildiğinde açık çevrim transfer fonksiyonu:

$$
T(s)
=
H
\cdot
\frac{1}{V_m}
\cdot
G_{vd}(s)
\cdot
G_c(s)
$$

şeklindedir.

Tüm sayısal değerler yerine konulduğunda:

$$
T(s)
=
0.12857
\cdot
\frac{1}{4}
\cdot
\frac{14}{0.3888}
\cdot
\frac{1 + \frac{s}{2\pi\cdot 100\,\text{kHz}}}
{1 + \frac{1}{1.789}\frac{s}{2\pi\cdot 2.5\,\text{kHz}}
+ \left(\frac{s}{2\pi\cdot 2.5\,\text{kHz}}\right)^2}
\cdot
4.762
\frac{
\left(1+\frac{s}{2\pi\cdot 3.44\,\text{kHz}}\right)
\left(1+\frac{2\pi\cdot 1\,\text{kHz}}{s}\right)
}{
\left(1+\frac{s}{2\pi\cdot 29\,\text{kHz}}\right)
\left(1+\frac{s}{2\pi\cdot 100\,\text{kHz}}\right)
}
$$

![Nihai açık çevrim Bode diyagramı](assets/docx-media/media/image27.png)

*Şekil 5.13 - Nihai açık çevrim transfer fonksiyonu $T(s)$ için Bode diyagramı.*

Bu Bode diyagramında:

- Phase margin yaklaşık $55^\circ$ olarak görülmektedir.
- Crossover frequency yaklaşık $10.3\,\text{kHz}$ olarak görülmektedir.

Bu sonuç hedeflenen $PM \approx 53^\circ$ ve $f_c \approx 10\,\text{kHz}$ değerleriyle uyumludur.

Kaynak belgede hesaplanan açık çevrim transfer fonksiyonu ayrıca aşağıdaki görsellerle verilmiştir:

![Hesaplanan açık çevrim transfer fonksiyonu](assets/docx-media/media/image28.png)

*Şekil 5.14 - Hesaplanan açık çevrim transfer fonksiyonu $T(s)$.*

Hesaplanan $T(s)$ aşağıdaki kapalı çevrim transfer fonksiyonlarında kullanılacaktır.

![T(s)'nin kapalı çevrim ifadelerinde kullanılması](assets/docx-media/media/image29.png)

*Şekil 5.15 - $T(s)$ ile kurulan kapalı çevrim ifade.*

> TODO: Kaynak DOCX bu noktada `image30.png` adlı 2x2 piksel bir medya nesnesi içeriyor. Görünür teknik figür gibi durmadığı için ana akışa gömülmedi; PDF ile karşılaştırılarak boş/artefakt olduğu doğrulanmalı.

Kapalı çevrim reference-to-output cevabı mavi grafiktir. Kapalı çevrim bandwidth'i ile açık çevrim crossover frekansı birbirine oldukça yakındır. Kapalı çevrimdeki $1/H$ çarpanı olmasaydı tam eşit olacaktı.

![Kapalı çevrim reference-to-output cevabı](assets/docx-media/media/image31.png)

*Şekil 5.16 - Kapalı çevrim reference-to-output cevabı.*

<a id="op-amp-devresi-gerceklemesi"></a>
# 6. Op-Amp Devresi Gerçeklemesi

Transfer fonksiyonları bulunduktan sonra geri besleme, direnç ve sığaçlarla uygun şekilde gerçekleştirilecektir. Aşağıdaki ekran görüntüsü bitirilmiş op-amp gerçekleştirmesidir.

> TODO: Kaynak DOCX, Bölüm 6 başlığı çevresinde `image32.png` ve `image33.png` adlı iki adet 3x3 piksel medya nesnesi içeriyor. Bunlar görünür teknik figür gibi durmadığı için ana akışa gömülmedi; PDF ile karşılaştırılarak boş/artefakt oldukları doğrulanmalı.

![Op-amp gerçekleştirme devresi](assets/docx-media/media/image34.png)

*Şekil 6.1 - Sensor gain ve compensator ağı dahil op-amp gerçekleştirme devresi.*

<a id="sensor-gain-hs"></a>
## 6.1. Sensor Gain, $H(s)$

Sensor gain için gerilim bölücü kullanılır.

![Gerilim bölücü ile H(s) sensor gain gerçekleştirmesi](assets/docx-media/media/image35.png)

*Şekil 6.2 - $H(s)$ sensor gain için gerilim bölücü.*

Seçilen değerler:

$$
R_3 = 12.8\,\text{k}\Omega
$$

$$
R_5 = 87.2\,\text{k}\Omega
$$

Bu gerilim bölücü yaklaşık:

$$
H
=
\frac{R_3}{R_3+R_5}
=
\frac{12.8}{12.8+87.2}
=
0.128
$$

değerini verir. Bu değer, hesaplanan:

$$
H \approx 0.12857
$$

sensör kazancına pratik olarak yakındır.

<a id="compensator-devresi"></a>
## 6.2. Compensator Devresi

Compensator için hedeflenen frekanslar ve kazançlar aşağıdaki Bode davranışına göre belirlenmiştir. Amaç, direnç ve sığaç kullanarak bu Bode eğrisindeki kazanç davranışını elde etmektir.

![Compensator için hedef frekans ve kazanç davranışı](assets/docx-media/media/image36.png)

*Şekil 6.3 - Gerçeklenecek compensator frekansları ve kazançları.*

$V_{ref}$ sabit olan bir tasarımda, $V_{ref}$ önündeki empedans ağını kullanmaya gerek yoktur. Bu nedenle sadeleştirilmiş compensator devresi aşağıdaki gibidir.

![Sadeleştirilmiş compensator devresi](assets/docx-media/media/image37.png)

*Şekil 6.4 - $V_{ref}$ sabit olduğunda kullanılan sadeleştirilmiş compensator ağı.*

Op-amp compensator çıkışı:

$$
V_c
=
\frac{Z_2(s)}{Z_1(s)}
\left(V^+ - V^-\right)
$$

şeklinde düşünülebilir.

Kazanç büyüklüğü:

$$
\left|\frac{Z_2(s)}{Z_1(s)}\right|
=
|Z_2(s)|
\cdot
\left|\frac{1}{Z_1(s)}\right|
$$

olarak ayrıştırılır.

### 6.2.1. $R_2$ ve $C_2$ ile Lag Sıfırının Gerçeklenmesi

![R2 ve C2 empedans karşılaştırması](assets/docx-media/media/image38.png)

*Şekil 6.5 - $R_2$ sabit empedansı ve $Z_{C2}$ eğimi.*

$R_2$ direnci tüm frekanslarda sabittir. $Z_{C2}$ empedansı ise $-20\,\text{dB/dec}$ eğimle azalır. Kaynak belgede $R_2$ ve $Z_{C2}$ değerlerinin:

$$
f_L = 1\,\text{kHz}
$$

frekansında aynı empedansa sahip olması seçilmiştir.

Bu koşul:

$$
R_2 = \frac{1}{2\pi f_L C_2}
$$

ve:

$$
C_2 R_2 = \frac{1}{2\pi f_L}
$$

verir.

$f_L=1\,\text{kHz}$ için:

$$
C_2 R_2
=
\frac{1}{2\pi\cdot 1\,\text{kHz}}
=
159.1549\,\mu
$$

olur.

> Not: Kaynak DOCX'in ilerleyen denklem listesinde bu değer bir yerde `152.1549u` gibi görünmektedir. $f_L=1\,\text{kHz}$ ve nihai $R_2=100\,\text{k}\Omega$, $C_2=1.59\,\text{nF}$ seçimiyle tutarlı değer $159.1549\,\mu$ değeridir.

### 6.2.2. $+20\,\text{dB/dec}$ Eğimin Gerçeklenmesi

![Sığaç empedansının terslenmesiyle +20 dB/dec davranış](assets/docx-media/media/image39.png)

*Şekil 6.6 - Bobin davranışına benzer $+20\,\text{dB/dec}$ eğimin sığaç empedansının terslenmesiyle elde edilmesi.*

Bobin davranışını andıran $+20\,\text{dB/dec}$ eğim, sığaç empedansının terslenmesiyle sağlanır.

### 6.2.3. $Z_1(s)$ ve $Z_2(s)$ Dominant Bileşenleri

$Z_1(s)$ ve $Z_2(s)$ seri bağlı alt elemanlardan oluşur. Bu yüzden belirli frekans aralıklarında bileşenlerden büyük olan empedans eşdeğer davranışı belirler.

![Z1 ve Z2 empedans ağı 1](assets/docx-media/media/image40.png)

![Z1 ve Z2 empedans ağı 2](assets/docx-media/media/image38.png)

![Z1 ve Z2 empedans ağı 3](assets/docx-media/media/image41.png)

*Şekil 6.7 - $Z_1(s)$ ve $Z_2(s)$ için frekans bölgesine göre dominant empedanslar.*

### 6.2.4. Eleman Değerlerinin Çözülmesi

Bulunan denklemler:

$$
\frac{R_2}{R_4} = 40.144
$$

Kaynak belgede ayrıca pratik direnç aralığıyla ilgili bir eşitsizlik notu vardır; bu not sonucunda kiloohm mertebesine çıkması gereken dirençler çok küçük çıktığı için pratik çözümde dikkate alınmamıştır.

Zaman sabiti denklemleri:

$$
C_2 R_2 = 159.1549\,\mu
$$

$$
C_4 R_4 = 5.4881\,\mu
$$

$$
C_4 R_1 = 46.2659\,\mu
$$

Kazanç oranı:

$$
\frac{R_2}{R_1} = 4.762
$$

Toplamda 4 denklem ve 5 bilinmeyen vardır:

$$
R_1,\ R_2,\ R_4,\ C_2,\ C_4
$$

Bu nedenle bilinmeyenlerden birine değer verilerek çözüm yapılır. Matematiksel olarak sonsuz sayıda çözüm mümkün olsa da değerler devredeki fiziksel karşılıkları düşünülerek seçilir.

Kaynak belgede:

$$
R_2 = A
$$

alınır.

Buna göre:

$$
R_1 = \frac{A}{4.762}
$$

$$
R_4 = 0.0249A
$$

$$
C_2 = \frac{159.1549\times 10^{-6}}{A}
$$

$$
C_4 = \frac{220\times 10^{-6}}{A}
$$

elde edilir.

Eğer:

$$
A = 100\,\text{k}\Omega
$$

seçilirse:

| Eleman | Değer |
|---|---:|
| $R_2$ | $100\,\text{k}\Omega$ |
| $R_1$ | $21\,\text{k}\Omega$ |
| $R_4$ | $2.4\,\text{k}\Omega$ |
| $C_2$ | $1.59\,\text{nF}$ |
| $C_4$ | $2.2\,\text{nF}$ |

elde edilir.

Bu değerler, Bölüm 5'te hedeflenen $G_c(s)$ compensator davranışını op-amp devresi üzerinde gerçekleştirmek için kullanılan pratik eleman değerleridir.

<a id="benzetim-sonuclari"></a>
"""


def find_section_start(lines: list[str]) -> int:
    for index, line in enumerate(lines):
        if line.startswith("# 5. Kontrolcü Tasarımı") or line.startswith("# 5. Kontrolc"):
            return index
    raise RuntimeError("Could not find section 5 start.")


def find_section_end(lines: list[str], start: int) -> int:
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("# Benzetim") or lines[index].startswith("# 7. Benzetim"):
            return index
    raise RuntimeError("Could not find section 7 boundary.")


def main() -> int:
    text = REPORT.read_text(encoding="utf-8")
    lines = text.splitlines()
    start = find_section_start(lines)
    end = find_section_end(lines, start)
    new_lines = lines[:start] + CONTROL_SECTIONS.rstrip().splitlines() + lines[end:]
    REPORT.write_text("\n".join(new_lines).rstrip() + "\n", encoding="utf-8", newline="\n")
    print(f"patched {REPORT} sections 5-6.2; preserved line {end + 1} onward")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
