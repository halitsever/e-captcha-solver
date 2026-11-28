---
title: "How Captcha OCR Works, Step by Step"
titleTemplate: false
description: "How OCR solves a text captcha, step by step: preprocessing, a CNN, a bidirectional LSTM, CTC decoding and a confidence score, shown with a real CRNN-CTC model."
headline: "What captcha OCR does to an image, from pixels to letters"
date: "2026-11-28"
keyword: "how to solve a captcha"
faq: [{"q": "Can this model read any captcha?", "a": "No. It reads E-captcha images: five letters from a fixed 19-letter alphabet. Other captchas need their own training data and run."}, {"q": "Why not use Tesseract?", "a": "Tesseract is built for clean printed text. Noisy, overlapping captcha letters are a different problem; the Tesseract vs CRNN post explains why."}]
---

# What captcha OCR does to an image, from pixels to letters

<p class="post-meta">By <a href="https://halit.org">Halit Sever</a> · <time datetime="2026-11-28">28 November 2026</time></p>

<p class="lead">Reading a text captcha with a program is an OCR problem: image in, short string out. This walk-through follows one image through the model in this repository, from pixels to five letters and a confidence score. The model reads one captcha style, E-captcha, and nothing else.</p>

## 1. Preprocess the image

Whatever size the captcha arrives in, `preprocess` in `model_ctc.py` does the same three things:

```python
img = img.convert("L").resize((200, 50))          # grayscale, fixed size
arr = np.asarray(img, dtype="float32") / 255.0    # 0..1
t = (torch.from_numpy(arr).unsqueeze(0) - 0.5) / 0.5   # -1..1
```

The result is a tensor of shape `(1, 50, 200)`. The same steps exist in training and in the Node.js runtime, and they have to stay identical: a model trained on one kind of scaling gets worse when it is fed another.

## 2. Turn pixels into features

Five convolutional blocks read the image. Each has two 3 x 3 convolutions with batch norm and ReLU, then a max-pool. The pooling shrinks the height step by step to 1 but keeps 50 columns of width:

| After block | Channels | Height x width |
| --- | --- | --- |
| 1 | 32 | 25 x 100 |
| 2 | 64 | 12 x 50 |
| 3 | 128 | 6 x 50 |
| 4 | 256 | 3 x 50 |
| 5 | 256 | 1 x 50 |

The image is now a sequence of 50 vectors, one for each thin vertical slice, each with 256 numbers. The [CRNN guide](/guide/crnn) shows every layer with its shapes.

## 3. Read the sequence

A two-layer bidirectional LSTM with 256 hidden units reads the 50 slices left to right and right to left. Each slice's output now carries context from its neighbours, which matters when letters overlap. A linear layer then gives 20 scores per slice: one for each of the 19 letters and one for "blank", meaning no new character here.

## 4. Decode with CTC

The model never learned where each letter sits. It was trained with [CTC loss](/guide/ctc-loss), which only needs the image and its text. Decoding reverses that: take the highest-scoring class in each of the 50 slices, merge repeats, then drop the blanks.

```text
slices (shortened from 50):  - - m m - e e - r r r - b - c c - -
merge repeats:               - m - e - r - b - c -
drop blanks:                 merbc
```

That greedy decode is what `greedy_decode` in `model_ctc.py` does.

## 5. Score the confidence

`CaptchaSolver.solve` in `infer.py` returns the text and a confidence: the average, over the 50 slices, of the probability of the class that was picked.

```python
from infer import CaptchaSolver

solver = CaptchaSolver("ctc_model.pt")
text, conf = solver.solve("captcha.jpg")
```

A low score usually means a messy image: heavy noise, letters merged into one shape. The project uses it in two places. At run time, a caller can ask for a fresh image instead of submitting a doubtful answer. During training, `pseudo_label_ctc.py` keeps only predictions above a threshold when it labels new images.

## 6. Train it on the right data

All of the above only works because the model saw thousands of labelled images of this exact style. `train_ctc.py` trains from a folder of images and a `labels.csv`, and `gen_synthetic.py` makes [synthetic images](/blog/what-is-a-captcha-code) to fill gaps. A different captcha needs its own data, and a different alphabet or length means changing the constants in several files. The [training guide](/guide/training) covers it.

## Where this stops

This kind of OCR applies to text captchas only. Image-selection puzzles, checkbox widgets and invisible scores like reCAPTCHA and Cloudflare Turnstile do not ask anyone to read text, and this project does not touch them. Use it for captchas you own, for research, or to test how weak a text captcha is before you rely on it.

## FAQ

### Can this model read any captcha?

No. It reads E-captcha images: five letters from a fixed 19-letter alphabet. Other captchas need their own training data and run.

### Why not use Tesseract?

Tesseract is built for clean printed text. Noisy, overlapping captcha letters are a different problem; the Tesseract vs CRNN post explains why.

## Related posts

- [What is a captcha code?](/blog/what-is-a-captcha-code)
- [Python OCR: image to text with and without Tesseract](/blog/python-ocr-image-to-text)
- [Tesseract vs a trained CRNN for captcha text](/blog/tesseract-vs-crnn-captcha)
- [All posts](/blog/)
