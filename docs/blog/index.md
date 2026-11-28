---
title: "Captcha and OCR Blog: How Captchas Work"
titleTemplate: false
description: "How captcha challenge-response tests, math captchas and captcha codes work, why Google shows unusual traffic pages, and how OCR reads text in Python."
---

# Captchas and OCR, explained

<p class="lead">Notes on how captchas work and how OCR models read text images. The examples come from this project's code: a small CRNN-CTC model that reads one captcha style, E-captcha. Nothing here is a guide to getting past other sites' captchas.</p>

## [What is a CAPTCHA challenge-response test?](/blog/what-is-a-captcha-challenge)

What a CAPTCHA challenge-response test is, how the server checks the answer, the main kinds of captcha in use today and why text captchas are easy for OCR.

## [Math CAPTCHAs: how they work and where they fall short](/blog/mathematical-captcha)

How a mathematical captcha works, how to build one that is checked on the server, and why a sum like 3 + 4 stops simple bots but little else. Python example.

## [Why Google shows an "unusual traffic" captcha](/blog/google-captcha-unusual-traffic)

Why Google says it detected unusual traffic from your computer network, what causes the reCAPTCHA page (VPNs, shared networks, malware) and what to do about it.

## [What is a captcha code?](/blog/what-is-a-captcha-code)

A captcha code is the distorted text you type to prove you are human. How a text captcha is generated step by step, with real samples and the code behind them.

## [How captcha OCR works, step by step](/blog/how-captcha-ocr-works)

How OCR solves a text captcha, step by step: preprocessing, a CNN, a bidirectional LSTM, CTC decoding and a confidence score, shown with a real CRNN-CTC model.

## [Python OCR: image to text with and without Tesseract](/blog/python-ocr-image-to-text)

Turn an image into text in Python: pytesseract for clean printed text, with install steps and options, and a trained CRNN for noisy text like captchas.

## [Tesseract vs a trained CRNN for captcha text](/blog/tesseract-vs-crnn-captcha)

Why Tesseract OCR in Python misreads captcha text, what preprocessing can and cannot fix, and why a small CRNN trained on one captcha style reads it better.

## [Captcha ne demek? Captcha kodu nedir?](/blog/captcha-ne-demek)

Captcha ne demek, captcha kodu ve captcha doğrulaması nedir? Sitelerin neden bu testi istediği, captcha türleri ve kod yanlış çıktığında ne yapılacağı.
