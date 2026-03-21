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
