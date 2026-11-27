---
title: Captcha solver API with FastAPI
description: Run the captcha OCR model as a small HTTP API. One FastAPI endpoint, POST /solve, takes an image upload and returns the text with a confidence score.
---

# Captcha solver API with FastAPI

<p class="lead"><code>server.py</code> is a 20-line FastAPI app with one endpoint. It is the option to pick when the caller is not written in Python, or when several services should share one loaded model.</p>

## Start the server

FastAPI, Uvicorn and the multipart parser are not in `requirements.txt`. Install them next to the base requirements:

```bash
pip install fastapi uvicorn python-multipart
uvicorn server:app --port 8000
```

The app loads `ctc_model.pt` from the current directory when the module is imported. Without that file the server does not start. It uses CUDA when PyTorch can see a GPU and the CPU otherwise.

Uvicorn listens on `127.0.0.1` unless you pass `--host`, so by default the API is reachable only from the same machine.

## POST /solve

<div class="table-scroll">

| | |
| --- | --- |
| Method and path | `POST /solve` |
| Request body | `multipart/form-data` |
| Form field | `file`, the image |
| Response | JSON object with `text` and `conf` |

</div>

```bash
curl -F file=@captcha.jpg http://localhost:8000/solve
# {"text":"hvnyf","conf":0.99}
```

`text` is the decoded string. `conf` is the confidence, rounded to three decimals.

The handler is short enough to read in full:

```python
@app.post("/solve")
async def solve(file: UploadFile = File(...)):
    img = Image.open(io.BytesIO(await file.read()))
    x = preprocess(img).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(x)
    text = greedy_decode(logits)[0]
    conf = float(logits.softmax(2).max(2).values.mean())
    return {"text": text, "conf": round(conf, 3)}
```

The upload is opened with Pillow, so any format Pillow can read will work. The image is then converted to grayscale, resized to 200 x 50 and passed through the model, the same path as the [command line tool](./quick-start).

## Calling it from other languages

Any HTTP client that can send a multipart form will do. From Node.js 18 or later, with nothing installed:

```js
import { readFile } from "node:fs/promises";

const form = new FormData();
form.append("file", new Blob([await readFile("captcha.jpg")]), "captcha.jpg");

const res = await fetch("http://localhost:8000/solve", { method: "POST", body: form });
const { text, conf } = await res.json();
```

## Interactive docs

FastAPI generates an OpenAPI description on its own. With the server running, `/docs` shows a page where you can upload an image and try the endpoint, and `/openapi.json` serves the schema. The app is titled "Text Captcha Solver".

## Using the confidence

`conf` is the model's highest probability at each of its 50 time steps, averaged. It is a score for the whole string. A caller can compare it with a threshold and ask for a new image when the value is low, and can also reject any `text` that is not five letters long. The server applies neither check itself.

## What the server leaves to you

The file is a minimal example. Before you put it on a network, note what it does not do:

- There is no authentication and no rate limit.
- There is no limit on upload size.
- An upload that is not an image raises an error inside the handler, which FastAPI reports as a 500 response. A request without the `file` field gets FastAPI's standard 422 validation error.
- The forward pass runs inside the async handler, so one request is processed at a time per worker.

For a deployment without Python, see [ONNX export and Node.js inference](./onnx-node).
