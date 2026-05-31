# Verification Summary

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
