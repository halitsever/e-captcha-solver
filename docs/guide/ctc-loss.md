---
title: CTC loss and CTC decoding explained
description: CTC loss explained with real PyTorch code. How nn.CTCLoss trains a model without alignments, and how greedy CTC decoding collapses repeats and drops blanks.
---

# How CTC loss and CTC decoding turn 50 predictions into five letters

<p class="lead">The model outputs 50 predictions for every image, and the answer has five letters. Connectionist Temporal Classification, CTC for short, is the rule that connects the two. It is used twice: as the loss in training and as the decoder at inference.</p>

## The alignment problem

After the [convolutional and recurrent layers](./crnn) the network has one row of 20 scores for each of 50 time steps. Each step corresponds to a 4 pixel advance across the image.

The training labels are plain strings such as `btffj`. Nothing in them says which steps belong to which letter. In these images the letters shift, tilt and overlap, so a fixed split into five equal slices would be wrong most of the time.

CTC removes the need for that information. It adds one extra class, the blank, and defines how a 50-step sequence reduces to a short string.

## The collapse rule

A path is one class per time step. To read a path:

1. Merge every run of the same class into one.
2. Remove the blanks.

<figure class="fig">
  <CtcDecode />
  <figcaption><b>Fig. 1.</b> Greedy CTC decoding on sample 09, labelled <code>btffj</code>. The blank is written as a hyphen. The path is written by hand to show the rule. It is not model output.</figcaption>
</figure>

The blank does two jobs. It fills the steps where no letter is present, such as the empty right half of the image above. It also separates repeated letters. The two runs of `f` in the figure stay apart because a blank sits between them. Without it, `fff` followed by `ff` would be one run and the result would be `btfj`.

## CTC loss in training

Many different paths reduce to the same string. The letter `b` could cover three steps or five, and could start a step earlier or later. CTC loss does not pick one. It adds up the probability of every path that reduces to the label and returns the negative log of that sum. The sum is computed with dynamic programming, as described by Graves and colleagues in 2006, so it stays cheap even though the number of paths is very large.

This is the training step in `train_ctc.py`:

```python
ctc = nn.CTCLoss(blank=0, zero_infinity=True)

logits = model(xs)
logp = logits.log_softmax(2).permute(1, 0, 2)
T = logp.size(0)
inlen = torch.full((xs.size(0),), T, dtype=torch.long)
loss = ctc(logp, ys, inlen, tlens)
```

A few details matter here:

- `nn.CTCLoss` expects log probabilities with time first, so the logits go through `log_softmax` and are permuted from `(batch, 50, 20)` to `(50, batch, 20)`.
- `inlen` is the input length for each image. Every image has the same width, so it is always 50.
- `ys` holds all the labels of the batch in one flat tensor, and `tlens` holds the length of each. The `collate` function builds both.
- `blank=0` matches `BLANK = 0` in `model_ctc.py`. Letters are encoded from 1 to 19.
- `zero_infinity=True` replaces an infinite loss with zero. That happens when no valid path exists for a sample, and it keeps one bad sample from breaking the whole batch.

A path needs at least one step per letter, plus one blank between repeated letters. With 50 steps for five letters there is plenty of room.

## Greedy CTC decoding at inference

At inference the code takes the most likely class at each step and applies the collapse rule. This is the whole decoder in `model_ctc.py`:

```python
@torch.no_grad()
def greedy_decode(logits):
    idxs = logits.argmax(dim=2).cpu().numpy()
    out = []
    for row in idxs:
        chars = []
        prev = -1
        for i in row:
            if i != prev and i != BLANK:
                chars.append(IDX_TO_CHAR.get(int(i), ""))
            prev = i
        out.append("".join(chars))
    return out
```

The condition `i != prev and i != BLANK` is both steps of the rule in one line. A class is kept when it differs from the previous step and is not the blank. `greedyDecode` in `node/solve.js` is the same loop in JavaScript.

Greedy decoding follows the single best path. It does not search over alternatives, and it does not force the result to be five letters long. A decoded string can be shorter or longer when the model is unsure, which is why `pseudo_label_ctc.py` keeps only predictions with exactly five characters.

## The confidence score

The Python entry points also return a confidence:

```python
conf = float(logits.softmax(2).max(2).values.mean())
```

It is the highest probability at each step, averaged over the 50 steps. Blank steps count as much as letter steps. Treat it as a score for the whole string.

## How accuracy is measured

`train_ctc.py` reports two numbers on the held-out images. Character accuracy compares the prediction with the label position by position, after padding or cutting the prediction to five characters. String accuracy counts a prediction only when the whole string matches. The checkpoint is saved when string accuracy matches or beats the best so far. The project's training notebook puts full-string accuracy at around 95%.
