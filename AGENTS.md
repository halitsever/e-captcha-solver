# AGENTS.md

E-captcha solver is a PyTorch CRNN-CTC model, with Python, FastAPI and Node.js (ONNX) inference, for developers who need to read E-captcha text captchas.

## Verify a change

CI (`.github/workflows/ci.yml`) has no test suite. It checks that the code installs and parses:

- Python 3.12, repo root: `pip install --extra-index-url https://download.pytorch.org/whl/cpu -r requirements.txt`, then `python -m compileall -q .`
- Node 22, from `node/`: `npm ci`, then `node --check solve.js`, then `node -e "require('sharp'); require('onnxruntime-node')"`

Checking real predictions needs a trained model (see below): `python solve_ctc.py samples/` reads the labelled images in `samples/`, whose file names end in the expected text.

## Gotchas

- No trained model is in the repo. `*.pt`, `*.pth`, `*.onnx`, `*.ckpt` and `data/` are gitignored. Train one with `train_ctc.py` or ask the owner, and keep weights and training data out of commits.
- `server.py` loads `ctc_model.pt` at import time, so `uvicorn server:app` fails without the file.
- `fastapi`, `uvicorn`, `python-multipart` (HTTP server) and `onnx`, `onnxscript` (export) are not in `requirements.txt`. Install them separately when you need them.
- The alphabet `abcdefghjkmnrstuvyz`, the 5-character length and the 200x50 input size are repeated in `model_ctc.py`, `gen_synthetic.py`, `export_onnx.py` and `node/solve.js`. Change them together; a new alphabet invalidates every trained model.
- Preprocessing (grayscale, resize to 200x50, scale to [-1, 1]) exists three times: `model_ctc.preprocess`, `train_ctc.to_tensor` and `toTensor` in `node/solve.js`. Keep them identical or accuracy drops.
- On Linux x64, `npm ci` in `node/` also downloads the CUDA build of onnxruntime from NuGet, which is large. Set `ONNXRUNTIME_NODE_INSTALL=skip` when CPU inference is enough.
- `node/` is an unpublished CommonJS helper with its own lockfile. Dependabot bumps it, `requirements.txt` and the workflows weekly.

## Conventions

- Commit subjects in conventional-commit style, in English, subject line only: no body, no trailer.
- Work on a branch and open a PR against `main`. The owner merges.
- Write new text without emoji. Keep code comments short, one line where possible, and say why.
- The README follows the owner's template. Keep every image served from `halitsever-api.vercel.app` byte-for-byte; only the `title=` value of `api/repo-title` and the issue wrapper link may be corrected.
- Leave version bumps and publishing to the owner.
