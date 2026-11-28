---
title: CRNN explained with a real captcha model
description: CRNN explained with working PyTorch code. Five convolutional blocks, a two-layer bidirectional LSTM and a CTC head, with the output shape of every layer.
---

# Inside a CRNN: the captcha model, layer by layer

<p class="lead">A CRNN is a convolutional recurrent neural network. Convolutions read the image, recurrent layers read the result as a sequence, and CTC turns the sequence into text. This page walks through the one in <code>model_ctc.py</code>.</p>

The design goes back to Shi, Bai and Yao's 2015 paper "An End-to-End Trainable Neural Network for Image-based Sequence Recognition". It suits text images because nobody has to mark where each character sits. The network sees the whole image and outputs the whole string.

<figure class="fig">
  <ArchFigure />
  <figcaption><b>Fig. 1.</b> The CRNN in <code>model_ctc.py</code> with the output shape of each stage for one image. Feature maps are drawn to scale. The output shown is the label of sample 01.</figcaption>
</figure>

## Input

`preprocess` converts an image to grayscale, resizes it to 200 x 50 and scales it to [-1, 1]. The model receives a tensor of shape `(batch, 1, 50, 200)`.

## The convolutional stack

All five blocks have the same structure. Only the channel counts and the pooling window change.

```python
def conv(cin, cout, pool):
    return nn.Sequential(
        nn.Conv2d(cin, cout, 3, padding=1),
        nn.BatchNorm2d(cout),
        nn.ReLU(inplace=True),
        nn.Conv2d(cout, cout, 3, padding=1),
        nn.BatchNorm2d(cout),
        nn.ReLU(inplace=True),
        nn.MaxPool2d(pool),
    )

self.cnn = nn.Sequential(
    conv(1,   32, (2, 2)),
    conv(32,  64, (2, 2)),
    conv(64, 128, (2, 1)),
    conv(128, 256, (2, 1)),
    conv(256, 256, (3, 1)),
)
```

The 3 x 3 convolutions use padding 1, so they keep the size. Only the pooling shrinks the feature map.

<div class="table-scroll">

| Block | Channels | Pool (height x width) | Output (channels x height x width) |
| --- | --- | --- | --- |
| 1 | 1 to 32 | 2 x 2 | 32 x 25 x 100 |
| 2 | 32 to 64 | 2 x 2 | 64 x 12 x 50 |
| 3 | 64 to 128 | 2 x 1 | 128 x 6 x 50 |
| 4 | 128 to 256 | 2 x 1 | 256 x 3 x 50 |
| 5 | 256 to 256 | 3 x 1 | 256 x 1 x 50 |

</div>

### Why the pooling is uneven

The first two blocks halve both sides. After that the pooling window is 1 wide, so the width stays at 50 while the height drops from 12 to 1.

This is the central idea of a CRNN. The height is squeezed away because a line of text has no vertical order to keep. The width is kept because it is the reading direction. Each of the 50 remaining columns covers a 4 pixel step across the original image, and each becomes one time step.

## From feature map to sequence

```python
f = self.cnn(x)
b, c, h, w = f.size()
assert h == 1, f"expected height 1, got {h}"
f = f.squeeze(2).permute(0, 2, 1)
```

The assertion guards the one assumption the model makes: the height must be exactly 1 after the last block. `squeeze` removes that dimension and `permute` moves the width to the middle. The result has shape `(batch, 50, 256)`: 50 time steps with 256 features each.

## The recurrent layers

```python
self.rnn = nn.LSTM(256, rnn_hidden, num_layers=2,
                   bidirectional=True, batch_first=True, dropout=0.2)
```

A column of convolutional features only sees a narrow slice of the image. In these captchas the letters overlap and tilt, so a slice often contains parts of two letters. The LSTM gives every step context from its neighbours.

It is bidirectional: one pass reads left to right, another reads right to left, and their outputs are joined. With 256 hidden units per direction the output has 512 features per step. There are two stacked layers with dropout of 0.2 between them.

## The CTC head

```python
self.fc = nn.Linear(rnn_hidden * 2, num_classes)
```

A single linear layer maps the 512 features to 20 scores at every step. Class 0 is the CTC blank. Classes 1 to 19 are the letters of `abcdefghjkmnrstuvyz`. The model returns raw logits of shape `(batch, 50, 20)`. The softmax is applied outside the model, by the loss in training and by the confidence calculation at inference.

How those 50 rows become five letters is covered in [CTC loss and CTC decoding](./ctc-loss).

## Size of the model

Counting the trainable parameters from the layer definitions gives just under five million.

<div class="table-scroll">

| Part | Parameters |
| --- | --- |
| Five convolutional blocks | 2,354,784 |
| Two-layer bidirectional LSTM | 2,629,632 |
| Linear head | 10,260 |
| Total | 4,994,676 |

</div>

## Changing the alphabet or the size

The alphabet, the five-character length and the 200 x 50 input size are constants. They are repeated in `model_ctc.py`, `gen_synthetic.py`, `export_onnx.py` and `node/solve.js`, so change them together. A new alphabet changes the number of classes, which makes every existing checkpoint unusable. A new input height also has to reach height 1 after the five pooling steps, or the assertion in `forward` fails.
