---
title: "Python OCR: Image to Text With and Without Tesseract"
titleTemplate: false
description: "Turn an image into text in Python: pytesseract for clean printed text, with install steps and options, and a trained CRNN for noisy text like captchas."
headline: "Python OCR: image to text with and without Tesseract"
date: "2026-11-28"
keyword: "python ocr image to text"
faq: [{"q": "Does pip install pytesseract install Tesseract?", "a": "No. pytesseract calls the Tesseract program, which you install separately with your system's package manager or the Windows installer."}, {"q": "How do I OCR a single line or word?", "a": "Pass --psm 7 for one line or --psm 8 for one word in the config argument. The default mode expects a full page."}]
---

# Python OCR: image to text with and without Tesseract

<p class="post-meta">By <a href="https://halit.org">Halit Sever</a> · <time datetime="2026-11-28">28 November 2026</time></p>

<p class="lead">Python has two common routes from an image to text. For clean printed text, such as scans, screenshots and receipts, call Tesseract through pytesseract. For one kind of noisy text that Tesseract keeps misreading, train a small model on examples of it. This page shows both with working code.</p>

## Route 1: pytesseract for printed text

pytesseract is a thin Python wrapper around the Tesseract command-line program. Install Tesseract itself first; the pip package does not include it.

```bash
# Debian or Ubuntu
sudo apt install tesseract-ocr
# macOS with Homebrew
brew install tesseract

pip install pytesseract pillow
```

Then read an image:

```python
from PIL import Image
import pytesseract

text = pytesseract.image_to_string(Image.open("receipt.png"))
print(text)
```

On Windows, if Python cannot find the program, point the wrapper at it:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### Options worth knowing

- **Language.** `lang="deu"` or `lang="eng+tur"` picks the trained language data. Extra languages are separate packages, such as `tesseract-ocr-tur` on Debian.
- **Page segmentation mode.** `config="--psm 7"` tells Tesseract the image is a single line of text, and `--psm 8` a single word. The default assumes a full page and often does worse on a small crop.
- **Allowed characters.** `config="--psm 7 -c tessedit_char_whitelist=0123456789"` limits the output to digits.
- **Positions.** `pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)` returns each word with its box and a confidence.

### Preprocess before you call it

Tesseract does best on large, sharp, high-contrast text. Converting to grayscale, scaling small images up and thresholding to black and white often help more than any option:

```python
img = Image.open("label.png").convert("L")
img = img.resize((img.width * 2, img.height * 2))
img = img.point(lambda p: 255 if p > 150 else 0)
text = pytesseract.image_to_string(img, config="--psm 7")
```

## Route 2: a trained model for one kind of noisy text

Some text defeats general OCR: letters that overlap, lines drawn through them, a background that changes from light to dark. Captchas are the obvious case. For one fixed style, a small model trained on labelled examples of exactly that style reads it far more reliably than a general engine. This repository is an example: a PyTorch CRNN-CTC model that reads E-captcha images.

```python
from infer import CaptchaSolver

solver = CaptchaSolver("ctc_model.pt")
text, conf = solver.solve("captcha.jpg")        # a path or a PIL image
text, conf = solver.solve_bytes(response.content)
```

It returns the text and a confidence score. It only reads the style it was trained on, so it needs a trained `ctc_model.pt` and, for any other text, your own labelled images and a training run. The [quick start](/guide/quick-start) covers setup and the [training guide](/guide/training) covers your own data. [How captcha OCR works](/blog/how-captcha-ocr-works) follows one image through the model.

## Which one should you use?

| Your images | Use |
| --- | --- |
| Documents, screenshots, receipts, signs in many fonts | pytesseract |
| Many languages or layouts | pytesseract with the right language data |
| One fixed, noisy style you have hundreds of labelled samples of | A trained CRNN-CTC model |
| One fixed style, no labels yet | Label a few hundred by hand, or generate synthetic ones as `gen_synthetic.py` does |

The reasons Tesseract struggles with captcha-like text, and what a dedicated model does differently, are in [Tesseract vs a trained CRNN](/blog/tesseract-vs-crnn-captcha).

## FAQ

### Does pip install pytesseract install Tesseract?

No. pytesseract calls the Tesseract program, which you install separately with your system's package manager or the Windows installer.

### How do I OCR a single line or word?

Pass --psm 7 for one line or --psm 8 for one word in the config argument. The default mode expects a full page.

## Related posts

- [How captcha OCR works, step by step](/blog/how-captcha-ocr-works)
- [Tesseract vs a trained CRNN for captcha text](/blog/tesseract-vs-crnn-captcha)
- [Text recognition with OpenCV's dnn module](/blog/opencv-ocr-python)
- [All posts](/blog/)
