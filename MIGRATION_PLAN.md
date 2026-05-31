# Migration Plan

Bu dosya, kaynak DOCX belgesindeki teknik icerigi GitHub'da okunabilir repo dokumantasyonuna donusturmek icin uygulanacak dosya ve icerik planidir. Bu adimda buyuk icerik tasima yapilmadi; yalnizca hedef yapi ve migration kurallari kayda gecirildi.

## Ana Ilke

Repo, tek bir uzun README yerine kisa bir giris sayfasi ve bolumlere ayrilmis teknik dokumantasyon yapisina donusturulmeli.

Source of truth sirasi:

1. `Birinci_donem_Buck_Converter_Serbest_Projesi.docx`
2. Yereldeki gorseller, simulasyon ekran goruntuleri ve LTspice dosyalari
3. Mevcut repo icerigi

Celiski durumunda mevcut `README.md` degil, kaynak DOCX kazanacak.

## Hedef Klasor Yapisi

Onerilen nihai yapi:

```text
.
|-- README.md
|-- REPO_AUDIT.md
|-- MIGRATION_PLAN.md
|-- docs/
|   |-- 00-abstract.md
|   |-- 01-giris.md
|   |-- 02-guc-ve-kontrol-tasarim-yontemi.md
|   |-- 03-guc-kati-hesaplamalari.md
|   |-- 04-cevirici-durum-denklemleri.md
|   |-- 05-kontrolcu-tasarimi.md
|   |-- 06-opamp-gerceklemesi.md
|   |-- 07-benzetim-sonuclari.md
|   |-- 08-projenin-gelecegi.md
|   |-- references.md
|   `-- appendices.md
|-- assets/
|   |-- figures/
|   |-- screenshots/
|   `-- docx-media/
|-- simulations/
|   `-- ltspice/
|       |-- circuits/
|       |-- symbols/
|       |-- libraries/
|       `-- results/
|-- references/
|   |-- datasheets/
|   |-- project-brief/
|   `-- extracted-text/
`-- BOM/
```

Bu yapi olusturulurken mevcut dosyalar hemen silinmemeli. Once yeni yapiya kopyalama/tasima ve link kontrolu yapilmali; orijinal path'ler ancak migration tamamlandiktan sonra temizlenmeli.

## README Stratejisi

`README.md` yeniden yazilacak ama asiri uzatilmayacak.

Yeni README sunlari icermeli:

- Projenin tek paragraf teknik ozeti
- Hedef tasarim gereksinimleri tablosu
- Ana sonuclarin kisa tablosu
- `docs/` bolumlerine navigasyon
- Ana rapor linkleri: `Birinci_donem_Buck_Converter_Serbest_Projesi.docx` ve `Birinci_donem_Buck_Converter_Serbest_Projesi.pdf`
- Simulasyon dosyalarina kisa yonlendirme
- Source-of-truth notu

README sunlari icermemeli:

- DOCX'in tam metni
- Uzun denklem turetimleri
- Tum ekran goruntuleri
- Uzun kaynak kitap notlari

## DOCX Basliklarini Repo Dosyalarina Tasima Haritasi

| DOCX bolumu | Hedef Markdown | Migration notu |
|---|---|---|
| `ABSTRACT` | `docs/00-abstract.md` | Ingilizce abstract korunacak; gerekirse kisa Turkce ozet eklenecek. |
| `İÇİNDEKİLER` | README ve docs linkleri | DOCX TOC birebir tasinmayacak; Markdown linkleriyle yeniden kurulacak. |
| `BÖLÜM 1` | `docs/01-giris.md` | Bolum etiketi metadata veya giris notu olarak kullanilacak. |
| `GİRİŞ` | `docs/01-giris.md` | Projenin problemi ve baglami. |
| `Çalışmanın Amacı ve Kapsamı` | `docs/01-giris.md` | Kaynak DOCX metni esas alinacak. |
| `Buck Converter Nedir?` | `docs/01-giris.md` | Kisa teknik arka plan. |
| `Güç ve Kontrol Tasarımında İzlenen Yöntem` | `docs/02-guc-ve-kontrol-tasarim-yontemi.md` | Guc kati ve kontrol tasarimini birlikte dusunme yaklasimi. |
| `Frekans Seçim Kuralları ve Hesaplamalar` | `docs/02-guc-ve-kontrol-tasarim-yontemi.md` | `images/readme/frequency_ordering.png` ve ilgili denklemlerle desteklenmeli. |
| `Hesaplamalarda Kullanılacak Parametreler:` | `docs/02-guc-ve-kontrol-tasarim-yontemi.md` | Parametre listesi tabloya donusturulebilir. |
| `Güç Katı Hesaplamaları:` | `docs/03-guc-kati-hesaplamalari.md` | L, C, ESR, duty cycle, guc ve ripple hesaplari ayrilmali. |
| `Çevirici Durum Denklemleri` | `docs/04-cevirici-durum-denklemleri.md` | `images/readme/converter_state_equations.png` ve ilgili matematik nesneleriyle aktarilmali. |
| `ESR Etkisi` | `docs/04-cevirici-durum-denklemleri.md` | ESR etkisi hem metin hem denklem/gorsel ile korunmali. |
| `Genel Dalga-Biçimleri` | `docs/04-cevirici-durum-denklemleri.md` | Dalga bicimi gorselleri dogrulanmali. |
| `kontrolcu tasarımı` | `docs/05-kontrolcu-tasarimi.md` | Baslik yazimi normalize edilecek: `Kontrolcü Tasarımı`. |
| `Kontrolcu Hesabı` | `docs/05-kontrolcu-tasarimi.md` | Sensor gain, Gvd, loop gain, lead/lag/PID hesaplari alt bolumlere ayrilmali. |
| `Op-amp devresi -gerçeklemesi` | `docs/06-opamp-gerceklemesi.md` | Baslik normalize edilecek: `Op-Amp Devresi Gerçeklemesi`. |
| `Sensor Gain (H(s))` | `docs/06-opamp-gerceklemesi.md` | Direnc bolucu/sensor gain formulleri korunmali. |
| `Compensator  Devresi` | `docs/06-opamp-gerceklemesi.md` | Fazladan bosluk temizlenecek; op-amp komponent degerleri tabloya alinacak. |
| `Benzetim sonuçları` | `docs/07-benzetim-sonuclari.md` | En kanit yogun dosya olacak; ekran goruntuleriyle linklenmeli. |
| `Tasarım Gereksinimleri` | `docs/07-benzetim-sonuclari.md` | Requirements tablosu DOCX'e gore yeniden yazilacak. |
| `Benzetimde kullanılan elemanlar ve parametreler` | `docs/07-benzetim-sonuclari.md` | LTspice parametre tablosu ile iliskilendirilmeli. |
| `Çıkış Gücü` | `docs/07-benzetim-sonuclari.md` | `images/readme/output_power_125w.jpg` ve `images/readme/output_power_55w.jpg` kullanilabilir. |
| `Output Voltage (static requirement):` | `docs/07-benzetim-sonuclari.md` | Statik cikis gerilimi kaniti tablo/gorsel ile verilmeli. |
| `Output Voltage (transient limits):` | `docs/07-benzetim-sonuclari.md` | Transient kaniti mevcut gorsellerden dogrulanmali. |
| `Allowed output voltage ripple (p-p, any R load)` | `docs/07-benzetim-sonuclari.md` | `images/readme/output_ripple.jpg` kullanilabilir. |
| `Verimlilik` | `docs/07-benzetim-sonuclari.md` | Rapor iddiasi, LTspice log/olcum ile eslestirilmeli. |
| `Hesaplamaların Doğrulanması` | `docs/07-benzetim-sonuclari.md` | DOCX'teki amac maddeleri korunmali. |
| `PROJENIN GELECEĞİ` | `docs/08-projenin-gelecegi.md` | Ikinci proje/LM5146/giris filtresi notlari ayrica belirtilmeli. |
| `KAYNAKLAR` | `docs/references.md` | PDF/TXT kaynaklar duzenli listeye alinmali. |
| `EKLER` | `docs/appendices.md` | Eklerin kapsami netlestirilmeli. |
| `EK-1. Sığaç Verisayfası` | `docs/appendices.md` | Datasheet/gorsel kaynagi dogrulanmali. |
| `EK-2. Genel görünüm` | `docs/appendices.md` | Genel gorunum gorseli eksikse DOCX'ten cikarilmali. |

## Gorsel Migration Plani

1. DOCX icindeki tum medya `assets/docx-media/` altina tam set olarak cikarilmali.
2. Halihazirda temiz adlandirilmis gorseller `images/readme/` icinden `assets/figures/` ve `assets/screenshots/` altina kopyalanmali veya tasinmali.
3. `ekran gorüntüleri/` altindaki orijinal dosyalar, GitHub uyumlu ASCII slug adlariyla `assets/screenshots/` altina alinmali.
4. Her gorsel icin bir mapping tablosu olusturulmali:

```text
source path -> target path -> kullanildigi docs bolumu -> caption -> dogrulama durumu
```

Oncelikli mevcut gorseller:

- `images/readme/frequency_ordering.png`
- `images/readme/type3_frequency_relations.png`
- `images/readme/converter_state_equations.png`
- `images/readme/control_system_block.png`
- `images/readme/uncompensated_loop_bode.png`
- `images/readme/final_loop_gain.png`
- `images/readme/gcs.jpg`
- `images/readme/output_power_125w.jpg`
- `images/readme/output_power_55w.jpg`
- `images/readme/output_ripple.jpg`
- `images/readme/pid_fl_2khz.jpg`
- `images/readme/opamp_gain_freq.jpg`

## Denklem Migration Plani

DOCX'te cok sayida matematik nesnesi bulundugu icin denklemler otomatik metin cikarimi ile guvenilir tasinamaz.

Onerilen kural:

- Basit tek satir denklemler Markdown/LaTeX olarak yazilsin.
- Karmasik veya bozulma riski yuksek denklemler ilk geciste gorsel olarak korunsun.
- Her denklem gorseli icin alt metin/caption eklensin.
- Denklem numaralari gerekiyorsa Markdown bolumlerinde yeniden elle verilsin.
- Aktarilan denklemler kaynak DOCX ve PDF ile gozle karsilastirilsin.

## LTspice Migration Plani

Mevcut LTspice klasoru korunmali, ancak GitHub okunurlugu icin kaynak ve sonuc dosyalari ayrilmali.

Onerilen hedef:

| Mevcut tur | Hedef |
|---|---|
| `.asc` | `simulations/ltspice/circuits/` |
| `.asy` | `simulations/ltspice/symbols/` |
| `.lib` | `simulations/ltspice/libraries/` |
| `.log`, `.plt`, `.net` | `simulations/ltspice/results/` veya ilgili circuit yaninda |
| `.raw` | `simulations/ltspice/results/`, Git LFS veya release artifact karariyla |

Buck projesiyle dogrudan iliskili gorunen dosyalar:

- `LTspice_AveragedSwitchModelingSimulation/SyncBuck_switching_CL.asc`
- `LTspice_AveragedSwitchModelingSimulation/SyncBuck_average_CL.asc`
- `LTspice_AveragedSwitchModelingSimulation/SyncBuck_average_fresponses.asc`
- `LTspice_AveragedSwitchModelingSimulation/SyncBuck_average_parameters.asc`
- `LTspice_AveragedSwitchModelingSimulation/SyncBuck_average_Zout.asc`
- `LTspice_AveragedSwitchModelingSimulation/BuckRegulator9-5-4_avg.asc`
- `LTspice_AveragedSwitchModelingSimulation/PID_compensator.asc`
- `LTspice_AveragedSwitchModelingSimulation/load.asc`

Boost, flyback ve SEPIC dosyalari egitim/referans ornekleri olabilir. Bunlar nihai repo icinde kalacaksa `simulations/ltspice/examples/` gibi ayri bir yere alinmali.

## Referans Dosyalari Migration Plani

Onerilen hedefler:

| Mevcut path | Hedef path | Not |
|---|---|---|
| `G5_mit6_622_s23_designproj.pdf` | `references/project-brief/mit6_622_s23_designproj.pdf` | Proje sartnamesi |
| `G5_mit6_622_s23_designproj.txt` | `references/extracted-text/mit6_622_s23_designproj.txt` | Arama yardimcisi |
| `G32_lm5146-q1.pdf` | `references/datasheets/lm5146-q1.pdf` | Datasheet |
| `G31_Robert_Erikson_fundamentals-of-power-electronics-3n_2020.pdf` | Karar bekliyor | Buyuk/telifli kaynak olabilir |
| `G31_Robert_Erikson_fundamentals-of-power-electronics-3n_2020.txt` | Karar bekliyor | Buyuk/telifli metin cikarimi olabilir |

## Uygulama Sirasi

1. `docs/` ve `assets/` klasorlerini olustur.
2. DOCX icindeki tum medyayi tam olarak cikar ve `assets/docx-media/` altina koy.
3. Mevcut `images/readme/` gorsellerini hedef `assets/` yapisina map et.
4. `docs/00-abstract.md` ile basla; sonra `docs/01-giris.md` ve `docs/02-guc-ve-kontrol-tasarim-yontemi.md` dosyalarini olustur.
5. Denklem/gorsel bozulmasi en yuksek oldugu icin once `docs/05-kontrolcu-tasarimi.md` icin kucuk bir pilot migration yap.
6. Pilot dogruysa tum bolumleri DOCX baslik yapisina gore aktar.
7. `docs/07-benzetim-sonuclari.md` icin LTspice dosyalari, loglar ve ekran goruntuleriyle kanit haritasi kur.
8. README'yi son adimda yeniden yaz; tum linkler olustuktan sonra navigasyon ver.
9. Relative link kontrolu yap.
10. Encoding kontrolu yap: UTF-8, bozuk karakter yok, Markdown linkleri calisiyor.

## Link ve Adlandirma Kurallari

- Repo icinde absolute path kullanilmayacak.
- Yeni dosya adlari kucuk harfli, ASCII, tire ayrimli olusturulacak.
- Turkce basliklar metinde korunabilir; anchor ve dosya adlarinda sade ASCII slug kullanilacak.
- Dosya adlarinda bosluk, apostrof, `ü`, `ğ`, `ı`, `ş`, `ç`, `ö` kullanilmamasi tercih edilecek.
- Eski path'ler migration bitene kadar korunacak.

## Koruma Kurallari

- Kaynak DOCX ve PDF silinmeyecek.
- Orijinal ekran goruntuleri migration bitmeden silinmeyecek.
- LTspice kaynak dosyalari silinmeyecek.
- `.raw` dosyalari buyuk olsa bile tekrar uretilebilirlik karari verilmeden silinmeyecek.
- Bos klasorler son temizlik adimina kadar korunacak.

## Kontrol Listesi

- [ ] DOCX medya tam cikarildi.
- [ ] DOCX basliklariyla `docs/` dosyalari birebir eslendi.
- [ ] Tum denklemler ya LaTeX ya dogrulanmis gorsel olarak aktarildi.
- [ ] Tum gorseller caption ve kaynak bolum bilgisiyle eklendi.
- [ ] LTspice dosyalari kaynak/sonuc olarak ayrildi.
- [ ] README kisa ve navigasyon odakli yeniden yazildi.
- [ ] Relative linkler kontrol edildi.
- [ ] UTF-8 karakter kontrolu yapildi.
- [ ] Buyuk dosya ve telif riskleri icin karar verildi.

## Kritik Riskler

- Kayip gorsel: DOCX medyasi tam cikarilmadan `images/docx_extracted/` yeterli sanilmamali.
- Bozuk denklem: Matematik nesneleri otomatik Markdown'a cevrilirse anlam kaybi olabilir.
- Turkce karakter: Mevcut README'deki encoding bozulmalari tekrar etmemeli.
- Kirik link: Eski dosya adlarinda bosluk ve Turkce karakter oldugu icin link kontrolu zorunlu.
- Asiri uzun README: Tum rapor README'ye konursa repo okunurlugu duser.
- GitHub dosya boyutu: Buyuk `.raw` ve kaynak PDF dosyalari icin LFS/release/dis kaynak karari gerekebilir.
- Simulasyon kapsami: Buck disi boost/flyback/SEPIC ornekleri yanlislikla ana proje kaniti gibi sunulmamali.

## Belirsizlikler

- Hangi `.raw` dosyalarinin nihai repoda kalmasi gerektigi kesin degil.
- DOCX'teki tum gorsellerin hangi sirayla ve hangi caption ile kullanilacagi henuz map edilmedi.
- Kaynak kitap PDF/TXT dosyalarinin repoda tutulmasi icin lisans/onay durumu bilinmiyor.
- Mevcut PDF'in DOCX ile tam ayni revizyon olup olmadigi henuz render/diff ile dogrulanmadi.
- Bos klasorlerin proje sahibi tarafindan planlanmis bir kullanim amaci olup olmadigi bilinmiyor.
