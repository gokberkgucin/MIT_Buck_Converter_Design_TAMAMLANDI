# MIT Buck Converter Design

Bu README, tamamlanmış buck converter tasarımının tez belgesinden GitHub uyumlu olarak parça parça aktarımı için tutulur.

Tezdeki teknik içerik, mümkün olduğunca orijinal metne sadık kalınarak eklenecektir. Kısa eklemeler `Ek not:` başlığı altında ayrıca belirtilecektir.

## BÖLÜM 1

### 1. GİRİŞ

#### 1.1. Çalışmanın Amacı ve Kapsamı

Bu çalışmanın amacı, belirlenen tasarım gereksinimlerini karşılayan bir DC-DC senkron buck konvertörünün tasarımını, analizini ve benzetimini gerçekleştirmektir. Çalışma, buck konvertör devresinin temel prensiplerini, güç katı hesaplamalarını ve kontrolcü tasarımını ele almaktadır. Tasarlanan sistem, verilen giriş voltaj aralığında çıkış voltajını sabit tutmayı hedeflemekte ve yüksek verimlilikle çalışması planlanmıştır.

#### 1.2. Buck Converter Nedir?

Buck converter, yüksek giriş gerilimini daha düşük bir çıkış gerilimine dönüştüren bir DC-DC dönüştürücü türüdür. Bu tür devreler, enerji kaybını azaltarak verimli bir şekilde enerji dönüşümü sağlar. Anahtar transistör, diyot, bobin ve kapasitör gibi temel elemanlardan oluşan buck converter, çeşitli elektronik cihazlarda güç yönetimi için yaygın olarak kullanılır.

Ek not:

Bu ilk aktarım turunda, tezdeki teknik içeriğin giriş kısmı eklendi. Sonraki mesajda aynı düzenle bir sonraki bölüme geçilebilir.

## 2. GÜÇ VE KONTROL TASARIMINDA İZLENEN YÖNTEM

Okuduğum kaynaklarda önce güç katı (Power Stage) hesaplamaları yapılıyor. Akım, gerilim değerleri, elemanların değerleri, kayıpları belirleniyor. Ardından kontrolcünün tasarımına geçiliyor. Güç ile kontrol tasarımı öncelik-sonralık ilişkisi olsa da birbirinden ayrık iki farklı süreçmiş gibi anlatılıyor. Kontrolcü tasarımında, bu güç katında belirlediğimiz parametreler kullanılıyor. Bu yöntem izlenerek yapılan çalışmada, frekansları istenen yerde tutmak zor olabiliyor. Güç aşamasına dönüp değeri yeniden değiştirmek zorunda kalınabiliyor. Örneğin güç katı aşamasındayken, serbestçe seçtiğimiz bir değer, kontrolcü aşamasında, tasarımı zorlaştırabiliyor. Oysaki bu serbest seçimin, ileride kısıtlayıcı bir seçim olacağını bilmiş olsaydık, bunu yapmazdık. Sonuç olarak, güç ve kontrol tasarımını bütünleşik biçimde düşünerek, birbirlerini etkileyen parametreleri, tasarım sürecinin başından itibaren göz önünde bulundurmak, tasarımın daha sağlıklı ve kolay bir şekilde yapılmasına yardımcı oluyor.

Ek not:

Bu bölüm, tezdeki tasarım yaklaşımının temel motivasyonunu veriyor. Sonraki parçada bunun devamında gelen teknik tasarım adımlarına geçebiliriz.

### 2.1. Frekans Seçim Kuralları ve Hesaplamalar

Kaynak [1] ve [2]'deki Type-3 Compensator'lü bir kontrolcü sistemindeki, frekanslarla ilgili tavsiye edilen seçim kurallarını bir araya getirdim.

- $f_s = f_{p2} = f_{esr}$
- $f_c = \dfrac{f_s}{10}$
- $f_L < \dfrac{f_c}{10}$
- $f_o$, $f_z$'den küçük, $f_L$'den büyük olacak.

Bu koşulları birleştirip, tüm frekansları yatay eksende, büyüklük sırasına göre sıraladım.

![Frekans seçim kuralları](image.png)

Denklemi belli olan frekanslar, ve seçimini bizim yaptığımız parametreler var.

- $f_{esr} = \dfrac{1}{2\pi C R_{esr}}$
- $f_o = \dfrac{1}{2\pi\sqrt{CL}}$
- $f_s = 100\,\text{kHz}$ ve $\theta = 52^\circ$

Yukarıdaki tüm koşulları ve denklemler dikkate alarak hesaplama yaptığımızda, birtakım sonuçlar elde ettik:

```math
f_s = 100\,\text{kHz}
```

```math
f_{P2} = f_{ESR} = f_s = 100\,\text{kHz}
```

```math
f_{ESR} = \frac{1}{2\pi C R_{esr}} = 100\,\text{kHz}
```

Buradan:

```math
C R_{esr} = \frac{1}{2\pi \cdot 100\,\text{kHz}} \approx 1.59 \times 10^{-6}
```

```math
f_c = \frac{f_s}{10} = 10\,\text{kHz}
```

```math
f_z = 3.44\,\text{kHz}
```

```math
f_{p1} = 29\,\text{kHz}
```

```math
f_L \le 1\,\text{kHz}
```

Buradan $f_L$'yi $1\,\text{kHz}$ olarak seçtim.

```math
f_L < f_0 < f_z
```

```math
1\,\text{kHz} < \frac{1}{2\pi\sqrt{CL}} < 3.44\,\text{kHz}
```

Buradan:

```math
2.44 \times 10^{-9} < C L < 25.3 \times 10^{-9}
```

Kontrolcü kısmından elde edilip güç hesabında kullanacağımız iki denklem bunlardır:

```math
2.44 \times 10^{-9} < C L < 25.3 \times 10^{-9}
```

```math
C R_{esr} \approx 1.59 \times 10^{-6}
```

Ek not:

Bu bölümde, kontrolcü tarafından dayatılan frekans kuralları açıkça güç katı seçimlerine bağlanıyor. Sonraki parçada bu kısıtların komponent seçimlerine nasıl yansıdığına geçebiliriz.

### 2.2. Hesaplamalarda Kullanılacak Parametreler

### 3. Güç Katı Hesaplamaları

Buck converter, en yüksek giriş gerilimindeyken (36V), en yüksek gücü (125W) verebilecek biçimde tasarlandı. Yüksek gerilimdeyken, duty cycle $D$ daha düşük olmak zorunda.

Küçük $D$; ana mosfetin daha kısa süre iletimde kalması, bobin ve sığacın dolması için daha az süreleri var demektir. Dolmaları için tanınan süre daha kısa olsa da aynı miktarda enerjiyi depolamak zorundalar, yüksek akım çekmeliler, yüksek gerilime çıkabilmelidirler. (Sabit çıkış gerilimi için). Öyleyse $L$ ve $C$ değerleri büyüyecek.

Yüksek çıkış gücü de zorlayıcı durumdur, düşük güce göre.

Esr koşulunu sağlamak için, aşağıdaki koşulun sağlanması gerekir:

```math
C > 28.4\,\mu\text{F}
```

$L$ sabit tutulursa:

```math
44\,\mu\text{F} < C < 527\,\mu\text{F}
```

$C$’nin yukarıdaki değer aralığında olması, $f_o$ resonance frekansının aşağıdaki değer aralığında olması demektir.

```math
f_L < f_0 < f_Z
```

```math
1\,\text{kHz} < f_0 < 3.44\,\text{kHz}
```

```math
C = 82\,\mu\text{F}
```

$C = 82\,\mu\text{F}$’lik sığaç seçelim.

Çünkü $82\,\mu\text{F}$’lik sığacın $ESR$’si $20\,\text{m}\Omega$’dur. Böylece aşağıdaki koşulu sağlamış oluruz. (ek-1)

```math
C R_{esr} \approx 1.59 \times 10^{-6}
```

```math
f_0 = 2.5\,\text{kHz}
```

```math
C = 82\,\mu\text{F}
```

$f_0 = 2.5\,\text{kHz}$ ve $C = 82\,\mu\text{F}$ iken $L$’nin kaç olduğunu bulalım.

```math
f_0 = \frac{1}{2\pi\sqrt{LC}}
```

Buradan:

```math
L = 49.42\,\mu\text{H}
```

Yeni $L$ ve $C$ değerlerine göre hesabımızı yenilemeliyiz.

Ek not:

Bu parçada, kontrolcü tarafından getirilen frekans kısıtlarının güç katı komponent seçimine nasıl döndüğü görülüyor. Sonraki doğal devam, çevirici durum denklemleri ve küçük işaret modeline geçiş kısmı olacak.

### 4. Çevirici Durum Denklemleri

Zaman alanında buck converter’ın tüm davranışını temsil eden bu denklemleri, LTSpice benzetim sonuçları ile denklemlerden birkaçını doğrulamaya çalışacağım.

#### 4.1. ESR Etkisi

#### 4.2. Genel Dalga-Biçimleri

### 5. Kontrolcu Tasarımı

Amaç: Çıkış gerilimini sabit ve iyi kontrol edilmiş değerde tutmaktır.

Küçük-işaret ac modeli kullandık.

T(s) Kontrolcünün açık-cevrim transfer fonksiyonudur.

T(s) çevrim kazancı yüksek tasarlayarak, çıkışın sadece referansı takip etmesini, ve bozucularının etkilerini en aza indirmesini hedefliyoruz.

#### 5.1. Kontrolcu Hesabı

```math
V_m = 4\,\text{V}
```

```math
V_{ref} = 1.8\,\text{V}
```

Vref =1.8V olarak belirledik. Bu değerler kullanacağımız pwm ve op-amp çalışabileceği değer aralığı ile uyumlu.

H(s) sensör Kazancı ne olmalı?

```math
V_e = V_{ref} - H \times V
```

Sıfır hata ile takip edecek.

```math
0 = 1.8 - H \times 14
```

```math
H \times V = 1.8
```

```math
H = 0.12857
```

Ek not:

Bu parçada tezdeki kontrol yaklaşımının başlangıcı ve sensör kazancı hesabı yer alıyor. Orijinal metindeki `H x V = 1,8` satırı korunmuş mantığın bir parçası olsa da, temiz hesap adımı fiilen $H = \dfrac{1.8}{14} = 0.12857$ sonucuna götürüyor. Sonraki parçada açık çevrim kazancı ve kompanzatör tasarımına geçebiliriz.

#### 5.2. Açık Çevrim Kazancı ve Lead (PD) Compensator

```math
G_{vd}(s)
```

Control-to-Output:

Çeviricinin fiziksel bileşenlerinden türetilir.

Bu transfer fonksiyonu, ’daki küçük değişimlerin, çıkış gerilimine olan etkisini inceler.

Çıkış geriliminin istenen bir seviyede tutulması için ’ın nasıl ayarlanması gerektiği bu fonksiyon ile belirlenir.

resonance kutup çifti frekansı

```math
Q_{load} = 2.02 \quad \text{veya} \quad 6.112\,\text{dB}
```

```math
Q = 1.789 < 2.02
```

’nin düşük frekans kazancıdır. PWM’nin kazancını dahil ederek.

Compensator’un 1 olduğu, henüz açık çevrimde etkisinin olmadığı durumda, Açık-çevrim’in kazancını ’yu bulacağız.

Açık-Çevrim T.F’nin düşük frekans kazancıdır.

Uncompensated Kazancını hesaplamaktaki amacımız, Compensator’den ne kadar kazanç elde etmemiz gerektiğini bulmak.

Hedeflediğimiz fc crossover (fs/10 = 10kHz) frekansındaki kazancı, 0dB’ye çıkarmak için ne kadar kazanca ihtiyacımız var. 22.3 dB artış gerekiyor.

Ayrıca, hedef fc’nin phase margin’i 14 derece. Bir de bu loop-gain’de ‘defects’ler vardır. O sebeple P.M, 14 dereceden daha azdır. [1]

Lead (PD) Compensator Eklenmesi

```math
f_c = 10\,\text{kHz}
```

```math
P.M = 53^\circ
```

fc = 10kHz, P.M = 53 derece hedefliyoruz.

Phase Margin’i 53 derece olarak hedeflememizin sebebi, Kapalı-çevrimin Q-factor =1 yapan P.M derecesidir. Bu Q-factor sayısı da hem kararlı hem de hızlı bir tepki için dengeli seçim.

Eklenen lead compensatorun sıfırı, frekansındadır, kutbu frekansındadır. ’den kat derecesinde daha büyük olacak şekilde.

Lead compensator’un phase margin’i en çok arttırabildiği frekans, frekansıdır. Üstteki Bode diagramı da bunu doğruluyor.

Eklediğimiz lead compensator’un phase marginini azami derecede arttırmasını istediğimizden olacak şekilde belirliyoruz. ve

Türetmelerini, cebirsel işlemleri atlayıp doğrudan ve ’yi veren denklemleri yazıyorum.

```math
53^\circ
```

Bu frekans değerlerini zaten bulmuştuk. Güç katında bunları dikkate alarak tasarım yapmıştık.

Doğrudan denklemi yazarsak, Lead compensator’un DC kazancı:

Lead compensatorun fc frekansındayken kazancını veren denklem:

Sonuç, tam da istediğimiz fc frekansındaki kazancı artışı kadar.

Lead compensator’un değerleriyle beraber yazıp Bode diagramını çizdirip, bazı yerleri gösterelim. Ayrıca bu T.F’ye op-amp’tan gelen kutbu () da ekledim. İlerleyen bölümlerde bunu açıklayacağım.

Lead compensator’un eklenmiş haliyle açık-çevrim T(s)’nin Bode diagramına bakalım.

Ek not:

Bu parçada docx içindeki metnin önemli kısmı korunabildi, fakat bazı denklem alanları Word’den eksik/bozuk taşındığı için sembollerin bir bölümü görünmüyor. Buna rağmen sayısal tasarım niyeti net: yaklaşık $22.3\,\text{dB}$ ek kazanç ihtiyacı, $f_c = 10\,\text{kHz}$ ve yaklaşık $53^\circ$ hedef phase margin. Sonraki parçada LAG (PI) compensator ve birleştirilmiş PID yapısına geçebiliriz.

#### 5.3. LAG (PI) Compensator Eklenmesi

seçmiştik. Pratik kural olarak fc’den en az 10 kat az olmalıydı. [1]

Eklenen sıfır normal sıfırdan farklıdır, ‘inverted zero’ dur.

#### 5.4. PID Compensator Birleştirilmiş Hali

#### 5.5. Op-amp ve Kutbu

Tasarımımızda kullandığımız, LT1215 op-amp’ın yüksek frekanslara doğru gidildikçe kazancını koruyamamasını temsil eden bir kutup ekleyeceğiz. bu kutup .

Opampın yukarıdaki kazanç değerini 100kHz frekansına kadar verebildiğini, aşağıdaki voltage gain vs frequency grafiğinden görebiliyoruz.

#### 5.6. Açık-Çevrim Transfer Fonksiyonu T(s)

```math
P.M = 55^\circ
```

```math
f_c = 10.3\,\text{kHz}
```

PM = 55 DERECE, Crossover frequency = 10.3kHz. Hedeflediğimiz gibi.

Hesapladığımız Açık-Çevrim Transfer Fonksiyonu T(s)

Hesapladığımız T(s) aşağıdaki trasfer fonksiyonlarında kullanılacak.

### 6. Op-amp devresi -gerçeklemesi

#### 6.1. Sensor Gain (H(s))

#### 6.2. Compensator Devresi

Vc =      x  (  V+  -  V-  )

|  |  =  | Z2(s) | *  |  | şeklinde düşünebiliriz.

Bulunan tüm denklemleri yazalım.

=40,144  ve       1/R4 > R2

Yukarıdaki iki denklemi de dikkate aldığımda kΩ’lar mertebesine çıkması gereken dirençler çok küçük çıktı. O yüzden dikkate almadım.

```math
C_2 R_2 = 152.1549\,\mu
```

```math
C_4 R_4 = 5.4881\,\mu
```

```math
C_4 R_1 = 46.2659\,\mu
```

=4,762

4 Tane denklem, 5 tane bilinmeyen var. R1, R2, R4, C2, C4

Bu sebepten dolayı bilinmeyenlerden birine değer vererek çözeceğiz.

Matematiksel olarak sonsuz sayıda çözüm mümkün olsa da, bu değerlerin devredeki fiziksel karşılığını düşünerek değer vereceğiz.

R2’ye A diyelim.

R2’ ye A diyelim

```math
R_2 = A
```

R1​= ​

```math
R_4 = 0.0249\,A
```

C2=

C4​= ​

olur.

Eğer A = 100k dersek

```math
R_2 = 100\,\text{k}\Omega
```

```math
R_1 = 21\,\text{k}\Omega
```

```math
R_4 = 2.4\,\text{k}\Omega
```

```math
C_2 = 1.59\,\text{nF}
```

```math
C_4 = 2.2\,\text{nF}
```

elde ederiz.

Ek not:

Bu parçada Word belgesindeki denklem yerleşimi daha da bozulduğu için bazı satırlar eksik sembolle geliyor; bu yüzden görünür sayısal sonuçları temiz matematik biçimine taşıdım, eksik sembollü satırları ise olduğu gibi korudum. Buna rağmen tasarım sonucu net biçimde okunabiliyor: yaklaşık $55^\circ$ phase margin, $10.3\,\text{kHz}$ crossover ve son kompanzatör seçiminde $R_2 = 100\,\text{k}\Omega$, $R_1 = 21\,\text{k}\Omega$, $R_4 = 2.4\,\text{k}\Omega$, $C_2 = 1.59\,\text{nF}$, $C_4 = 2.2\,\text{nF}$.

## 7. Benzetim Sonuçları

### 7.1. Tasarım Gereksinimleri

- Input voltage range: 24-36 V
- Input voltage transient limit: 44 V for up to 1 ms
- Output Power Range (resistive load): 50 - 125 W
- Output Voltage (static requirement): 14 V ± 3%
- Output Voltage (transient limits): 14 V ± 20%
- Allowed output voltage ripple (p-p, any R load): 100 mV
- Allowed input current ripple (p-p, ideal source): 50 mA
- Minimum efficiency (across voltage, load): 90%
- Ambient temperature range: -20ºC – +50ºC

1 The converter must be able to survive this input voltage transient, but does not have to run during the transient.

2 The voltage should not vary outside this range during steps between minimum and maximum load.

### 7.2. Benzetimde Kullanılan Elemanlar ve Parametreler

### 7.3. Çıkış Gücü

### 7.4. Output Voltage (static requirement)

### 7.5. Output Voltage (transient limits)

### 7.6. Allowed output voltage ripple (p-p, any R load)

### 7.7. Verimlilik

### 7.8. Hesaplamaların Doğrulanması

Bu bölümün iki temel amacı vardır:

- Belirlenen tasarım ‘specifications’larını karşılayabilen bir devre tasarlandığı göstermek.
- Önceki bölümlerde kağıt-kalemle yapılan hesaplamaların doğrulamasını yapmaktı.

Bu yüzden, bulunan değerler olduğu gibi değiştirilmeden LTSPICE’da kullanılmıştır. Bu değerlerin benzetim sonuçları gösterilmiştir.

İyileştirmeler yapmak pekâlâ mümkündür, kolaydır.

Ek not:

Bu parça, benzetim bölümünün çerçevesini ve hangi gereksinimlere göre doğrulama yapıldığını netleştiriyor. Sonraki doğal devam, `PROJENIN GELECEĞİ` başlığı olur.

## 8. PROJENIN GELECEĞİ

Projenin devamında yapılacakları maddeler halinde özet olarak sıralarsam:

- Lm5146 kontrolcüsü kullanacağım.
- Giriş filtresini tasarlayacağım.
- Eleman seçimlerini kesinleştireceğim.
- Mosfet sürücüsü ile ilgili hesapları yapacağım.
- Ortalama modelini kullanarak, frekans alanında inceleyeceğim. Verimlilikleri, kayıpları hesaplayacağım. Parametrik değerler verip iyileştirmeler yapacağım.
- Bobinle ilgili hesapları yapacağım.
- Altuim'da çizim.

Ek not:

Bu bölüm, tezin bu sürümünün aslında tamamlanmış bir son ürün değil, sonraki fazlara açılan bir ara teslim mantığıyla kurgulandığını açıkça gösteriyor. Bir sonraki parçada istersek `KAYNAKLAR` başlığını, istersek README için daha anlamlı olan görsel/simülasyon dosyalarını öne çıkaran kısa bir yönlendirme bölümü ekleyebiliriz.

## 9. KAYNAKLAR

## 10. EKLER

### EK-1. Sığaç Verisayfası

### EK-2. Genel görünüm

Ek not:

Docx metin çıkarımında bu aşamadan sonra yalnızca başlıklar görünüyor; kaynak listesinin ayrıntılı maddeleri ve ek içeriklerin gövdesi metne taşınmamış. Bu nedenle README'ye tezde görünür olan başlıkları aynen ekledim. İstersek bir sonraki adımda PDF'den veya ek dosyalardan yararlanarak `KAYNAKLAR` ve `EKLER` bölümlerini daha dolu hale getirebiliriz.
