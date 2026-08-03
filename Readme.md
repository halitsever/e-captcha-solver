<p align="center" class="logo-section">
<img src="/.github/assets/logo.svg" height="80" width="80"/>
</br>
  <img src="https://halitsever-api.vercel.app/api/repo-title?title=E-Captcha+Solver">

<p align="center">
E-captcha recognition with a CRNN (~95% accuracy)<br>
<br/>
<br/>
<img src="https://img.shields.io/github/sponsors/halitsever"/>
</p>
<p align="center">
<a align="center" href="#">Documentation</a>
  </p>
</p>

<p align="center">
<img src="https://halitsever-api.vercel.app/api/details"/>
</p>

- 🧠 Five convolutional blocks, a two-layer bidirectional LSTM with 256 hidden units, and a CTC head on top
- 🔤 A fixed 19-letter alphabet (`abcdefghjkmnrstuvyz`) and five characters per image
- 🖼️ Any input size works. Images are converted to 200x50 grayscale before they reach the model
- 📊 Every prediction comes back with a confidence score, so you can retry the weak ones instead of failing
- 🟢 A Node.js runtime over ONNX, for projects that do not want Python in production
- 🌐 A FastAPI endpoint if you would rather call it over HTTP

<p align="center" >
<img src="https://halitsever-api.vercel.app/api/installation"/>
</p>

```bash
git clone https://github.com/halitsever/e-captcha-solver.git
cd e-captcha-solver
pip install -r requirements.txt
```

Put `ctc_model.pt` in the project root, then read an image:

```bash
python solve_ctc.py captcha.jpg
# captcha.jpg   hvnyf   0.99
```

Pass a folder instead of a file to run a batch. From your own code:

```python
from infer import CaptchaSolver

solver = CaptchaSolver("ctc_model.pt")
text, conf = solver.solve("captcha.jpg")     # also takes a PIL image
text, conf = solver.solve_bytes(response.content)
```

Over HTTP:

```bash
pip install fastapi uvicorn python-multipart
uvicorn server:app --port 8000
curl -F file=@captcha.jpg http://localhost:8000/solve
# {"text":"hvnyf","conf":0.99}
```

From Node, with no Python at runtime. Export the model once, then install and run:

```bash
pip install onnx onnxscript
python export_onnx.py --model ctc_model.pt --out ctc_model.onnx

cd node && npm install
node solve.js ../captcha.jpg ../ctc_model.onnx
# hvnyf
```

The ONNX session is built on the first call and reused after that, so a long run of images only pays that cost once.

To train on your own captchas, put the images in `data/` and their labels in a `labels.csv` with `filename,label` columns:

```bash
python train_ctc.py --data data --labels labels.csv --epochs 400 --out ctc_model.pt
```

`gen_synthetic.py` writes synthetic training images if you are short on real ones, and `pseudo_label_ctc.py` labels an unlabeled folder with a model you already have, keeping only the predictions above a confidence threshold. `captcha_ctc_colab.ipynb` runs the whole training pass on a Colab GPU.

<p align="center" href="https://github.com/halitsever/e-captcha-solver/issues">
<img src="https://halitsever-api.vercel.app/api/issue"/>
</p>

<p align="center">
<img src="https://halitsever-api.vercel.app/api/sponsor"/>
</p>

<p align="center">
<img src="https://halitsever-api.vercel.app/api/license"/>
</p>

<p align="center">
  MIT LICENSE | Halit Sever 
</p>
