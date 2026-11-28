---
title: Train a captcha recognition model
description: Train the CRNN-CTC captcha recognition model on your own labelled images, with synthetic data from gen_synthetic.py, pseudo-labelling and a Colab notebook.
---

# How to train the captcha recognition model on your own data

<p class="lead">The repository ships the training code and no weights. This page covers the data format, the training command, the synthetic image generator, pseudo-labelling and the Colab notebook.</p>

The model only knows the E-captcha alphabet and the five-character length. Other text captchas need their own training run, and a different alphabet or length also means changing the constants described in [CRNN explained](./crnn#changing-the-alphabet-or-the-size).

## Prepare the data

Put the images in a folder and write a CSV with two columns, `filename` and `label`:

```csv
filename,label
0001.jpg,merbc
0002.jpg,tkcdv
```

Labels are stripped and lower-cased when the file is read. Every character has to be in the alphabet `abcdefghjkmnrstuvyz`. A label with any other character stops the run, because it has no class index.

The defaults expect the folder at `data/` and the file at `labels.csv`. Both are gitignored, together with every weight file, so training data and checkpoints stay out of commits.

## Run the training

```bash
python train_ctc.py --data data --labels labels.csv --epochs 400 --out ctc_model.pt
```

<div class="table-scroll">

| Argument | Default | Meaning |
| --- | --- | --- |
| `--data` | `data` | Folder with the images |
| `--labels` | `labels.csv` | CSV with `filename,label` |
| `--val` | `200` | Images held back for validation |
| `--epochs` | `400` | Number of epochs |
| `--batch` | `64` | Batch size |
| `--lr` | `1e-3` | Starting learning rate |
| `--out` | `ctc_model.pt` | Where the best checkpoint is saved |
| `--seed` | `42` | Seed for the shuffle and the augmentation |

</div>

The script shuffles the rows and takes the first `--val` of them as the validation set. The rest is the training set, so you need clearly more than 200 labelled images with the default.

Training uses Adam with weight decay of 1e-5, a cosine learning rate schedule over the full run, [CTC loss](./ctc-loss) and gradient clipping at a norm of 5. It runs on CUDA when a GPU is available and on the CPU otherwise.

Every five epochs it evaluates on the validation set and prints a line such as `Epoch  50 | loss ... | val char ... string ...`. The checkpoint is written whenever string accuracy matches or beats the best so far. String accuracy counts a prediction only when all five letters are right.

The cosine schedule is tied to the epoch count. A shorter run also compresses the schedule.

## Augmentation

Training images go through a light augmentation step. Validation images do not.

- 70% of the time: a rotation of up to 4 degrees with a shift of up to 4 pixels sideways and 2 pixels vertically.
- 40% of the time: one extra line drawn across the image.
- Always: a small change in brightness and contrast.
- 30% of the time: Gaussian noise.

The docstring in the code explains the limit: it is kept modest so character positions stay readable.

## Generate synthetic images

`gen_synthetic.py` writes training images when you are short on real ones.

```bash
python gen_synthetic.py --n 5000 --out synth --labels synth_labels.csv
python train_ctc.py --data synth --labels synth_labels.csv
```

Each image is 200 x 50 with five random letters from the alphabet. The generator draws a horizontal gradient that is light on the left and dark on the right, then places the letters with a random font, size, shade and a rotation of up to 7 degrees. Letters advance by less than their own width, so they overlap. One or two lines cross the image, and noise is added to 60% of them. Files are saved as `s_000000.jpg` and so on, and `--seed` (default 0) makes a run repeatable.

The generator looks for DejaVu Sans, FreeSans and Liberation Sans under `/usr/share/fonts/truetype/`. At least one of them has to be installed.

`train_ctc.py` reads one folder and one CSV. To train on real and synthetic images together, copy them into one folder and join the two CSV files.

## Pseudo-label an unlabelled folder

Once you have a model, `pseudo_label_ctc.py` can label more images for the next training run.

```bash
python pseudo_label_ctc.py --dir unlabeled --model ctc_model.pt --thresh 0.97 --out pseudo_labels.csv
```

It runs the model on every `.jpg` and `.png` in the folder and keeps a prediction only when the confidence is at least `--thresh` and the text has exactly five characters. The output has the same `filename,label` columns as a hand-made labels file. The script ends by printing how many images it labelled and the acceptance rate.

The labels are only as good as the model that wrote them, so a high threshold matters. The default is 0.97.

## Train on Colab

`captcha_ctc_colab.ipynb` runs the whole pass on a Colab GPU. Switch the runtime to GPU, choose Run all, and upload a zip with the project files, a `data/` folder and `labels.csv` when the third cell asks for it. The notebook then trains with the default settings, solves a few images as a demo and offers `ctc_model.pt` as a download.

According to the notebook, 400 epochs take 15 to 20 minutes on a GPU, and full-string accuracy sits around 95%. Its notes add that once the training loss reaches zero, validation accuracy stops climbing, and that cleaning the hardest labels, test-time augmentation or a bigger backbone are the things to try next.
