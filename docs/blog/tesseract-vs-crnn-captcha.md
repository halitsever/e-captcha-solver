---
title: "Tesseract OCR vs a Trained CRNN for Captcha Text"
titleTemplate: false
description: "Why Tesseract OCR in Python misreads captcha text, what preprocessing can and cannot fix, and why a small CRNN trained on one captcha style reads it better."
headline: "Tesseract vs a trained CRNN for captcha text"
date: "2026-11-28"
keyword: "tesseract ocr python"
faq: [{"q": "Can Tesseract be retrained on captchas?", "a": "Yes, Tesseract supports fine-tuning its LSTM models on your own line images. The setup is heavier than training a small PyTorch model like this one, but it is possible."}, {"q": "Does a whitelist make Tesseract read captchas?", "a": "It stops impossible characters from appearing in the output. It does not help Tesseract see letters through noise, gradients and overlaps."}]
---

# Tesseract vs a trained CRNN for captcha text

<p class="post-meta">By <a href="https://halit.org">Halit Sever</a> · <time datetime="2026-11-28">28 November 2026</time></p>

<p class="lead">Tesseract is the default answer to "OCR in Python", and it is very good at printed text. Point it at a captcha and the output is usually wrong. The reason is not that Tesseract is old or weak. It was trained for a different kind of image.</p>

## Same family of model, different training

Since version 4, Tesseract recognises each line of text with an LSTM network trained with CTC. That is close to the CRNN in this repository, which also reads the image as a sequence with a bidirectional LSTM and is trained with [CTC loss](/guide/ctc-loss). The architectures are cousins. What differs is everything around them.

| | Tesseract | This project's CRNN |
| --- | --- | --- |
| Trained on | Printed text in many fonts and languages | Labelled E-captcha images and synthetic look-alikes |
| Expects | Pages: finds blocks, lines and words first | One 200 x 50 image with exactly five characters |
| Alphabet | Every character of the chosen language | 19 lowercase letters |
| Background | Assumes dark text on a fairly even light page | Learned the left-light, right-dark gradient |
| Noise | Treats lines and specks as possible characters | Learned to ignore the crossing lines |

## Where Tesseract trips on captcha text

**Layout analysis.** Before it reads anything, Tesseract looks for text blocks and lines. A crossing line or a cluster of specks can be taken for part of a character or split a word. `--psm 7` or `--psm 8` skips some of that, which helps, but the recogniser still sees the clutter.

**Binarisation.** Tesseract turns the image into black and white before recognition. In the repository's generator, which copies the real images, the background runs from about 250 grey on the left to about 130 on the right, and some letters are drawn in 105-175 grey. One global threshold either loses the light letters or turns the dark half of the background into ink.

**Overlapping letters.** E-captcha letters start at 62-82% of the previous letter's width, so neighbours touch. Printed text rarely does that, and Tesseract's training reflects it.

**The wrong alphabet.** Without a whitelist Tesseract may return capitals, digits or punctuation. A whitelist of the 19 letters narrows the output but does not teach it the shapes.

## What preprocessing can fix

You can get Tesseract further with work on the image: remove the gradient by dividing by a blurred copy, threshold adaptively instead of globally, erase thin lines with a morphological opening, scale the image up, and pass a whitelist and `--psm 8`. Each step is tuned by hand for one captcha style, and each new kind of noise needs another step. We have not published a measured comparison for E-captcha, so this page gives no accuracy numbers for Tesseract.

## Why a trained model wins on one style

A model trained on thousands of examples of one captcha style learns the gradient, the line noise and the letter overlap directly. Nobody writes the preprocessing rules. This repository's README reports about 95% accuracy on E-captcha. That figure applies to E-captcha only. The cost is the opposite of Tesseract's: the model reads nothing but that style, and a new style needs new labelled data and a new run of `train_ctc.py`.

## Which to use

Use Tesseract through pytesseract for documents, screenshots and anything in ordinary fonts; the [Python OCR guide](/blog/python-ocr-image-to-text) has the setup and options. Train a small CRNN when you have one fixed, noisy style and can label a few hundred examples or generate them. [How captcha OCR works](/blog/how-captcha-ocr-works) walks through that model one step at a time.

## FAQ

### Can Tesseract be retrained on captchas?

Yes, Tesseract supports fine-tuning its LSTM models on your own line images. The setup is heavier than training a small PyTorch model like this one, but it is possible.

### Does a whitelist make Tesseract read captchas?

It stops impossible characters from appearing in the output. It does not help Tesseract see letters through noise, gradients and overlaps.

## Related posts

- [What is a captcha code?](/blog/what-is-a-captcha-code)
- [How captcha OCR works, step by step](/blog/how-captcha-ocr-works)
- [Python OCR: image to text with and without Tesseract](/blog/python-ocr-image-to-text)
- [All posts](/blog/)
