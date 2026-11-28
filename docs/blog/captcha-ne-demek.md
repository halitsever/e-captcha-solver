---
title: "Captcha Ne Demek? Captcha Kodu ve Doğrulaması Nedir?"
titleTemplate: false
description: "Captcha ne demek, captcha kodu ve captcha doğrulaması nedir? Sitelerin neden bu testi istediği, captcha türleri ve kod yanlış çıktığında ne yapılacağı."
headline: "Captcha ne demek? Captcha kodu nedir?"
date: "2026-11-28"
keyword: "captcha ne demek"
lang: "tr"
hreflang: {"tr": "blog/captcha-ne-demek", "en": "blog/what-is-a-captcha-challenge", "x-default": "blog/what-is-a-captcha-challenge"}
faq: [{"q": "Captcha ne işe yarar?", "a": "Formları, girişleri ve kayıtları otomatik programlara karşı korur. Spam, sahte hesap ve şifre deneme saldırılarını yavaşlatır."}, {"q": "Captcha kodu nereye yazılır?", "a": "Resmin hemen altındaki ya da yanındaki kutuya. Kodu gördüğünüz gibi, boşluk bırakmadan yazın."}, {"q": "Captcha doğrulaması neden sürekli çıkıyor?", "a": "VPN, ortak bir ağ ya da kısa sürede çok sayıda istek sitenin sizi otomatik trafik sanmasına yol açabilir. VPN'i kapatıp tekrar deneyin."}]
---

# Captcha ne demek? Captcha kodu nedir?

<p class="post-meta">Yazan <a href="https://halit.org">Halit Sever</a> · <time datetime="2026-11-28">28 Kasım 2026</time></p>

<p class="lead">Captcha, bir sitenin karşısındakinin insan mı yoksa bir program mı olduğunu anlamak için sorduğu küçük bir testtir. Bulanık harfleri yazmak, "Ben robot değilim" kutusunu işaretlemek ya da trafik ışıklı kareleri seçmek bu testin farklı biçimleridir.</p>

## Captcha kelimesinin anlamı

CAPTCHA, İngilizce "Completely Automated Public Turing test to tell Computers and Humans Apart" ifadesinin kısaltmasıdır. Türkçesiyle: bilgisayarları ve insanları ayırmak için tamamen otomatik, herkese açık bir Turing testi. Adı, Carnegie Mellon Üniversitesi'nden Luis von Ahn, Manuel Blum, Nicholas Hopper ve John Langford'un 2003 tarihli makalesinden gelir. Testi bir insan değil, bilgisayar hazırlar ve puanlar.

## Captcha doğrulaması nasıl çalışır?

Her captcha bir soru ve cevaptan oluşur:

1. Site bir görev hazırlar ve doğru cevabı kendi sunucusunda saklar.
2. Siz görevi çözersiniz, tarayıcı cevabı formla birlikte gönderir.
3. Sunucu cevabı kontrol eder. Doğruysa ve süresi dolmadıysa işlem devam eder.

"Captcha doğrulaması" denince bu kontrol kastedilir. Kontrol tarayıcıda değil sunucuda yapılmalıdır, yoksa bir program formu captcha'sız gönderebilir.

## Captcha kodu nedir?

Captcha kodu, resmin içine eğri büğrü çizilmiş birkaç harf ya da rakamdır. Site kodu o anda rastgele üretir, üstüne çizgi ve gürültü ekleyerek resme çevirir ve gerçek metni sunucuda tutar. Siz resmi okuyup kutuya yazarsınız.

Bu projedeki örnek E-captcha'dır: 200 x 50 piksellik gri bir resimde 19 harflik bir alfabeden seçilmiş beş küçük harf. Bu tür bir kodun adım adım nasıl üretildiği İngilizce [captcha kodu yazısında](/blog/what-is-a-captcha-code) anlatılıyor.

## Captcha türleri

| Tür | Ne yaparsınız |
| --- | --- |
| Metin captcha | Resimdeki harf ya da rakamları yazarsınız |
| Matematik captcha | "3 + 4 kaç?" gibi bir toplamı cevaplarsınız |
| Resim seçme | Otobüs ya da yaya geçidi olan kareleri seçersiniz |
| Onay kutusu | "Ben robot değilim" kutusunu işaretlersiniz, gerekirse bir resim görevi açılır |
| Görünmez | Hiçbir şey yapmazsınız, site arka planda bir risk puanı alır |

Google'ın reCAPTCHA'sı, hCaptcha ve Cloudflare Turnstile bu türlerin en yaygın örnekleridir. Yeni sistemler resimden çok tarayıcıdan ve istekten gelen sinyallere bakar.

## Metin captcha'lar neden zayıf?

Bir sitenin captcha kodları genelde hep aynı tarzdadır: aynı yazı tipleri, aynı uzunluk, aynı alfabe. Bu tarzdan birkaç bin etiketli örnekle eğitilen küçük bir yapay zekâ modeli kodları okumayı öğrenebilir. Bu depodaki model de böyle bir örnektir: sadece E-captcha'yı okur ve README'ye göre E-captcha'da yaklaşık %95 doğruluk verir. Bu yüzden önemli formlarda metin captcha'nın yanına hız sınırı ve sunucu tarafı kontroller eklenir.

## Kod sürekli yanlış çıkıyorsa

- Büyük-küçük harfe dikkat edin. Bazı siteler fark gözetir, bazıları gözetmez.
- Okuyamadığınız resim için yeni kod isteyin. Çoğu formda yenile düğmesi vardır.
- Sayfayı uzun süre açık bıraktıysanız kodun süresi dolmuş olabilir. Sayfayı yenileyin.
- Çerezleri ya da JavaScript'i engelleyen bir eklenti captcha'nın çalışmasını bozabilir.

Google aramada "olağandışı trafik" uyarısıyla gelen captcha'nın sebepleri ayrı bir yazıda: [Google unusual traffic captcha](/blog/google-captcha-unusual-traffic).

## Sık sorulan sorular

### Captcha ne işe yarar?

Formları, girişleri ve kayıtları otomatik programlara karşı korur. Spam, sahte hesap ve şifre deneme saldırılarını yavaşlatır.

### Captcha kodu nereye yazılır?

Resmin hemen altındaki ya da yanındaki kutuya. Kodu gördüğünüz gibi, boşluk bırakmadan yazın.

### Captcha doğrulaması neden sürekli çıkıyor?

VPN, ortak bir ağ ya da kısa sürede çok sayıda istek sitenin sizi otomatik trafik sanmasına yol açabilir. VPN'i kapatıp tekrar deneyin.

## İlgili yazılar

- [What is a CAPTCHA challenge-response test?](/blog/what-is-a-captcha-challenge)
- [Why Google shows an "unusual traffic" captcha](/blog/google-captcha-unusual-traffic)
- [What is a captcha code?](/blog/what-is-a-captcha-code)
- [Tüm yazılar](/blog/)
