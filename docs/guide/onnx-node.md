---
title: ONNX export and Node.js inference
description: Export the PyTorch captcha OCR model to ONNX and run it in Node.js with onnxruntime-node and sharp. No Python is needed at runtime after the export.
---

# Run the captcha model in Node.js with ONNX Runtime

<p class="lead">The <code>node/</code> folder runs the same model through ONNX Runtime. Python is needed once, to export the checkpoint. After that an image captcha solver runs in a plain Node.js process.</p>

## Export the model

The export needs two packages that are not in `requirements.txt`:

```bash
pip install onnx onnxscript
python export_onnx.py --model ctc_model.pt --out ctc_model.onnx
```

`export_onnx.py` loads the checkpoint on the CPU and traces it with a dummy input of shape `(1, 1, 50, 200)`:

```python
torch.onnx.export(
    model, dummy, args.out,
    input_names=["input"], output_names=["logits"],
    opset_version=12, dynamo=False,
)
```

The graph has one input named `input` and one output named `logits`. No dynamic axes are declared, so the exported model expects one image at a time. Both arguments are optional and default to `ctc_model.pt` and `ctc_model.onnx`.

## Install the Node package

```bash
cd node
npm install
```

There are two dependencies: `onnxruntime-node` runs the model and `sharp` decodes and resizes the image. The package is a CommonJS helper with its own lockfile. It is not published to npm.

::: tip Linux x64
On Linux x64 the `onnxruntime-node` install also downloads the CUDA build of the runtime, which is large. Set `ONNXRUNTIME_NODE_INSTALL=skip` when CPU inference is enough.
:::

## Run it from the command line

```bash
node solve.js ../captcha.jpg ../ctc_model.onnx
# hvnyf
```

The first argument is the image. The second is the model path and defaults to `ctc_model.onnx` in the current directory. The script prints the predicted text and nothing else.

## Use it as a module

```js
const { solve } = require("./solve");

const text = await solve("captcha.jpg", "ctc_model.onnx");
```

`solve` passes its first argument straight to `sharp`, so it can be a file path or a `Buffer` with the image bytes. It returns a promise for the decoded string.

Two differences from the Python API are worth knowing:

- The Node module returns the text only. It does not compute a confidence value.
- The ONNX session is a module-level singleton. It is built on the first call and reused after that, so a long run of images pays the loading cost once. The model path of later calls is ignored for the same reason.

`getSession` is exported too, if you want to load the model before the first image arrives.

## Preprocessing has to match

The model was trained on tensors produced by `preprocess` in Python. `toTensor` in `solve.js` repeats the same three steps: resize to 200 x 50, convert to grayscale, scale to [-1, 1].

```js
const { data, info } = await sharp(input).resize(W, H, { fit: "fill" }).grayscale().raw().toBuffer({ resolveWithObject: true });
const ch = info.channels;
const arr = new Float32Array(W * H);
for (let i = 0; i < W * H; i++) {
  const g = data[i * ch];
  arr[i] = (g / 255 - 0.5) / 0.5;
}
return new ort.Tensor("float32", arr, [1, 1, H, W]);
```

`fit: "fill"` stretches the image to the target size without keeping the aspect ratio, as the Python code does. If you change the preprocessing in one place, change it in the others, or accuracy drops.

## Decoding in JavaScript

The ONNX graph ends at the logits, a `[1, 50, 20]` tensor. `greedyDecode` finds the top class at each of the 50 steps, skips a class that repeats the previous step, and skips class 0, the blank. That is the same rule as `greedy_decode` in Python. [CTC loss and CTC decoding](./ctc-loss) explains it with a worked example.

The alphabet is written out again in `solve.js` as `CHARS`. Keep it identical to the one in `model_ctc.py`.
