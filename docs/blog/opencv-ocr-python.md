---
title: "OCR With OpenCV in Python: What It Can Do"
titleTemplate: false
description: "OpenCV does OCR in its dnn module: a text detector plus a CRNN recognizer with CTC decoding. How the API works in Python and how it compares with this repo."
headline: "Text recognition with OpenCV's dnn module"
date: "2026-11-28"
keyword: "ocr opencv python"
faq: [{"q": "Can OpenCV do OCR?", "a": "Yes, through its dnn module since OpenCV 4.5: TextDetectionModel finds text and TextRecognitionModel reads it with a CRNN model and CTC decoding. You supply the model file."}, {"q": "Does OpenCV include OCR models?", "a": "No. The OpenCV tutorial links pretrained ONNX models, such as a CRNN for digits and lowercase letters, that you download separately."}, {"q": "Is OpenCV OCR better than Tesseract?", "a": "They suit different text. Tesseract is built for printed documents; OpenCV's detector and CRNN suit text in photos. Neither reads a distorted captcha style well without training on it."}]
---

# Text recognition with OpenCV's dnn module

<p class="post-meta">By <a href="https://halit.org">Halit Sever</a> · <time datetime="2026-11-28">28 November 2026</time></p>

<p class="lead">OpenCV is best known for image processing, but since version 4.5 its dnn module also has high-level classes for reading text: one finds text in an image, another reads a cropped line. The reader is the same kind of model this repository uses, a CRNN trained with CTC loss.</p>

## The two classes

From OpenCV's [text spotting tutorial](https://github.com/opencv/opencv/blob/4.x/doc/tutorials/dnn/dnn_text_spotting/dnn_text_spotting.markdown) (OpenCV 4.5 or later):

- **`TextDetectionModel`** finds where text is. It supports DB models (`TextDetectionModel_DB`) and EAST models (`TextDetectionModel_EAST`), and returns four-point boxes.
- **`TextRecognitionModel`** reads a cropped image of one line of text. It only supports CNN + RNN + CTC models, the CRNN family, with `CTC-greedy` or `CTC-prefix-beam-search` decoding.

OpenCV ships no weights itself. The tutorial links pretrained ONNX files, for example a CRNN with 36 classes (digits and lowercase letters) trained on the synthetic MJSynth dataset, and a 94-class model with capitals and punctuation.

## Reading a text line in Python

The tutorial's example is C++. This is the same code with OpenCV's Python bindings, which name the classes `cv.dnn_TextRecognitionModel` and so on, as OpenCV's own Python tests do. We have not run it for this post, so treat it as a starting point:

```python
import cv2 as cv

model = cv.dnn_TextRecognitionModel("crnn_cs.onnx")
model.setDecodeType("CTC-greedy")
with open("alphabet_94.txt", encoding="utf-8") as f:
    model.setVocabulary([line.rstrip("\n") for line in f])

# Scale and mean map pixels from 0..255 to -1..1, at the model's 100x32 input size.
model.setInputParams(scale=1 / 127.5, size=(100, 32), mean=(127.5, 127.5, 127.5))

image = cv.imread("text_line.png")
print(model.recognize(image))
```

The tutorial's own test image prints `welcome`. For a full photo, run a `TextDetectionModel` first, crop each box, and pass the crops to `recognize`.

## How this compares with the model in this repository

The [E-captcha model](/guide/crnn) is the same architecture, trained for one job:

| | OpenCV's sample CRNN | This repository |
| --- | --- | --- |
| Input | 100 x 32 | 200 x 50 grayscale |
| Pixel scaling | 0..255 to -1..1 | 0..255 to -1..1 |
| Classes | 36 or 94 plus the CTC blank | 19 letters plus the blank |
| Trained on | Synthetic and real scene text | E-captcha images and synthetic look-alikes |
| Decoding | Greedy or prefix beam search | Greedy, in `model_ctc.greedy_decode` |

The preprocessing lines up, but the exported file does not drop straight into OpenCV: `export_onnx.py` writes the output as (batch, time, classes), while `TextRecognitionModel` expects (time, batch, classes). The model would need a transpose before export, and we have not tested that path. To run this model without PyTorch, the [ONNX and Node.js guide](/guide/onnx-node) uses onnxruntime instead.

## When to use what

- **Printed text in documents or screenshots:** Tesseract is the easier start; see [Python OCR](/blog/python-ocr-image-to-text).
- **Text in photos and scenes:** OpenCV's detector plus a pretrained CRNN.
- **One fixed, distorted style:** a small CRNN trained on that style, as compared in [Tesseract vs a trained CRNN](/blog/tesseract-vs-crnn-captcha).

## FAQ

### Can OpenCV do OCR?

Yes, through its dnn module since OpenCV 4.5: TextDetectionModel finds text and TextRecognitionModel reads it with a CRNN model and CTC decoding. You supply the model file.

### Does OpenCV include OCR models?

No. The OpenCV tutorial links pretrained ONNX models, such as a CRNN for digits and lowercase letters, that you download separately.

### Is OpenCV OCR better than Tesseract?

They suit different text. Tesseract is built for printed documents; OpenCV's detector and CRNN suit text in photos. Neither reads a distorted captcha style well without training on it.

## Related posts

- [How captcha OCR works, step by step](/blog/how-captcha-ocr-works)
- [Python OCR: image to text with and without Tesseract](/blog/python-ocr-image-to-text)
- [Tesseract vs a trained CRNN for captcha text](/blog/tesseract-vs-crnn-captcha)
- [All posts](/blog/)
