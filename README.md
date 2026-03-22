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

## Bu Repoda Ne Var

- MIT design-project gereksinimlerine gore gelistirilmis birinci buck converter calismasi
- Ayrintili hesaplar, analiz ve benzetim sonuclari
- Ana rapor PDF'i ve calisma dosyalari

## Ana Dokuman

- [Birinci_Buck_Converter_Serbest_Projesi.pdf](./Birinci_Buck_Converter_Serbest_Projesi.pdf)

## Not

Bu repo tamamlanmis birinci calismayi temsil eder. Daha gelismis ve halen uzerinde calisilan ikinci proje icin:

- [MIT_Buck_Converter_DEVAM_EDIYOR](https://github.com/gokberkgucin/MIT_Buck_Converter_DEVAM_EDIYOR)
