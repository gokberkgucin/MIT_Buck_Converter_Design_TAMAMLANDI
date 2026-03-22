# MIT Buck Converter Design

Bu repo, [MIT 6.622 Power Electronics Design Project](./G5_mit6_622_s23_designproj.pdf) kapsamindaki specifications'lari karsilamak uzere gelistirilmis birinci buck converter serbest projesine ait belge ve destek dosyalarini icerir.

README, PDF raporunun yerine gecmez. Buradaki amac, calismanin neyi hedefledigini ve neyin dogrulandigini kisa bir ozet halinde sunmaktir.

## Kisa Ozet

Bu calismada senkron bir buck converter tasarlandi; guc kati hesaplari, kontrolcu tasarimi ve benzetim dogrulamalari birlikte ele alindi. Tasarim surecinde bobin, kapasitans, ESR ve anahtarlama ile ilgili guc kati secimleri; ardindan cikis gerilimi regulasyonu icin kompanzasyon ve kontrol yaklasimi gelistirildi.

Calisma, yalnizca devre kurulumunu gosteren bir proje notu degil; hedef specifications'a gore tasarlanmis ve LTspice benzetimleri ile dogrulanmis bir buck converter calismasidir.

## Hedef Specifications

- Input voltage range: `24 V - 36 V`
- Input voltage transient limit: `44 V` for up to `1 ms`
- Output power range: `50 W - 125 W`
- Output voltage static requirement: `14 V ± 3%`
- Output voltage transient limit: `14 V ± 20%`
- Allowed output voltage ripple: `100 mV p-p`
- Allowed input current ripple: `50 mA p-p`
- Minimum efficiency target: `90%`
- Ambient temperature range: `-20 C` to `+50 C`

## Specification Check

Legend:
- `✅` README seviyesinde ozetlenebilen veya raporda acikca karsilandigi belirtilen kosul
- `🟡` Projede takip edilen kosul; ayrintili kanit PDF raporda

| Requirement | Target | LTspice / Report Summary | Status | Evidence |
|---|---|---|---|---|
| Input voltage range | `24 V - 36 V` | Tasarim ve benzetim araligi olarak kullanildi | ✅ | Report Sec. `7.1` |
| Input voltage transient limit | `44 V` for up to `1 ms` | Gereksinim olarak tanimlandi; ayrintili dogrulama PDF raporda | 🟡 | Report Sec. `7.1` |
| Output power range | `50 W - 125 W` | LTspice ekran goruntulerinde yaklasik `49.60 W` ve `124.18 W` calisma noktalarina ulasildi | ✅ | Report Sec. `7.3` |
| Output voltage static requirement | `14 V ± 3%` | Gosterilen kararlı durum dalga seklinde `Vout ≈ 13.95 V`, hedef aralik icinde | ✅ | Report Sec. `7.4` |
| Output voltage transient limit | `14 V ± 20%` | Transient performansin specifications'i karsiladigi raporda belirtiliyor; ayrintili dalga sekli PDF'de | ✅ | Report Sec. `7.5` |
| Allowed output voltage ripple | `100 mV p-p` | Gosterilen dalga seklinde yaklasik `37.38 mV p-p` ripple | ✅ | Report Sec. `7.6` |
| Allowed input current ripple | `50 mA p-p` | Tasarim gereksinimi olarak takip edildi; ayrintili dalga sekli README'de ozetlenmedi | 🟡 | Report Sec. `7.1` / `7.8` |
| Minimum efficiency target | `90%` | Verimlilik dogrulamasinin yapildigi ve specified requirements'in karsilandigi raporda belirtiliyor | ✅ | Report Sec. `7.7` / Abstract |
| Ambient temperature range | `-20 C` to `+50 C` | Proje gereksinimi olarak tanimlandi; README'de ayri sicaklik analizi ozetlenmedi | 🟡 | Report Sec. `7.1` |

Bu tablo, README seviyesinde kisa bir uygunluk ozetidir. Tam dalga sekilleri, hesap adimlari ve ekran goruntuleri ana PDF rapordadir.

## Bu Repoda Ne Var

- MIT design-project gereksinimlerine gore gelistirilmis birinci buck converter calismasi
- Ayrintili hesaplar, analiz ve benzetim sonuclari
- Ana rapor PDF'i ve calisma dosyalari

## Ana Dokuman

- [Birinci_Buck_Converter_Serbest_Projesi.pdf](./Birinci_Buck_Converter_Serbest_Projesi.pdf)

## Not

Bu repo tamamlanmis birinci calismayi temsil eder. Daha gelismis ve halen uzerinde calisilan ikinci proje icin:

- [MIT_Buck_Converter_DEVAM_EDIYOR](https://github.com/gokberkgucin/MIT_Buck_Converter_DEVAM_EDIYOR)
