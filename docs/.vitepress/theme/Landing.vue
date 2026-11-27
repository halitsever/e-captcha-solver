<script setup lang="ts">
import { withBase } from 'vitepress'
import SampleFigure from './SampleFigure.vue'
import ArchFigure from './ArchFigure.vue'
import CtcDecode from './CtcDecode.vue'

const repo = 'https://github.com/halitsever/e-captcha-solver'

const facts = [
  { k: 'Accuracy, full string', v: 'about 95%', src: 'Readme.md, captcha_ctc_colab.ipynb' },
  { k: 'Alphabet', v: 'abcdefghjkmnrstuvyz', mono: true, src: 'model_ctc.py' },
  { k: 'Characters per image', v: '5', src: 'model_ctc.py' },
  { k: 'Model input', v: '200 × 50 grayscale, scaled to [-1, 1]', src: 'model_ctc.py' },
  { k: 'Model output', v: '50 time steps × 20 classes', src: 'model_ctc.py' },
  { k: 'Trainable parameters', v: '4,994,676', src: 'counted from model_ctc.py' },
  { k: 'Default training run', v: '400 epochs, batch 64, Adam at 1e-3, cosine schedule', src: 'train_ctc.py' },
  { k: 'Training time', v: '15 to 20 minutes on a Colab GPU', src: 'captcha_ctc_colab.ipynb' },
  { k: 'Validation hold-out', v: '200 images', src: 'train_ctc.py' },
]

const guides = [
  { href: '/guide/quick-start', t: 'Solve a captcha in Python: quick start', d: 'Install, add weights, read one image or a folder from the command line or from your own code.' },
  { href: '/guide/crnn', t: 'CRNN explained with a real captcha model', d: 'Every layer of the network with its output shape, and why the width ends at 50.' },
  { href: '/guide/ctc-loss', t: 'CTC loss and CTC decoding explained', d: 'How 50 predictions become five letters, in training and at inference.' },
  { href: '/guide/training', t: 'Train a captcha recognition model', d: 'Labels file, augmentation, synthetic images, pseudo-labelling and the Colab notebook.' },
  { href: '/guide/onnx-node', t: 'ONNX export and Node.js inference', d: 'Export the checkpoint once and run it from Node with onnxruntime-node and sharp.' },
  { href: '/guide/api-server', t: 'Captcha solver API with FastAPI', d: 'The POST /solve endpoint, its request and response, and what it does not handle.' },
]

const py = `from infer import CaptchaSolver

solver = CaptchaSolver("ctc_model.pt")
text, conf = solver.solve("captcha.jpg")
text, conf = solver.solve_bytes(response.content)`

const http = `pip install fastapi uvicorn python-multipart
uvicorn server:app --port 8000
curl -F file=@captcha.jpg http://localhost:8000/solve
# {"text":"hvnyf","conf":0.99}`

const node = `python export_onnx.py --model ctc_model.pt --out ctc_model.onnx
cd node && npm install
node solve.js ../captcha.jpg ../ctc_model.onnx
# hvnyf`
</script>

<template>
  <div class="paper">
    <header class="front">
      <div class="title-block">
        <h1>E-captcha solver: open-source captcha OCR in Python</h1>
        <p class="byline">Halit Sever. PyTorch, MIT licence.</p>
        <p class="abstract">
          <b>Abstract.</b> E-captcha solver is a text captcha solver written in Python. A PyTorch CRNN reads five-letter E-captcha images
          and is trained with CTC loss, so the labels are plain strings with no character positions. The README states about 95% accuracy.
          The repository holds the model, the training script, a synthetic data generator, an ONNX export and three ways to run inference:
          a Python class, a FastAPI endpoint and a Node.js module. Trained weights are not included.
        </p>
        <p class="actions">
          <a class="primary" :href="withBase('/guide/quick-start')">Read the quick start</a>
          <a class="source" :href="repo">
            <svg viewBox="0 0 16 16" width="18" height="18" aria-hidden="true">
              <path
                fill="currentColor"
                d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"
              />
            </svg>
            Source on GitHub
          </a>
        </p>
      </div>

      <figure class="fig fig-samples">
        <SampleFigure />
        <figcaption>
          <b>Fig. 1.</b> The ten labelled images in <code>samples/</code>. Each label is the ground truth from the file name. No trained
          weights ship with the repository, so this page shows no predictions.
        </figcaption>
      </figure>
    </header>

    <section class="sec">
      <h2>The model</h2>
      <div class="split">
        <div class="prose">
          <p>
            The network in <code>model_ctc.py</code> has three parts. Five convolutional blocks turn a 200 × 50 grayscale image into a
            strip that is 1 pixel high, 50 wide and 256 channels deep. Each block is two 3 × 3 convolutions with batch normalisation and
            ReLU, followed by max pooling.
          </p>
          <p>
            Only the first two blocks pool horizontally. The width stops at 50 while the height keeps shrinking to 1, and those 50 columns
            become the time steps of a sequence.
          </p>
          <p>
            A two-layer bidirectional LSTM with 256 hidden units reads the sequence in both directions. A linear layer then scores 20
            classes at every step: the 19 letters of the alphabet plus the CTC blank. The whole model has 4,994,676 trainable parameters,
            counted from the layer definitions.
          </p>
          <p><a :href="withBase('/guide/crnn')">CRNN explained, layer by layer</a></p>
        </div>
        <figure class="fig">
          <ArchFigure />
          <figcaption>
            <b>Fig. 2.</b> The CRNN as defined in <code>model_ctc.py</code>, with the output shape of each stage. Feature maps are drawn
            to scale. The output shown is the label of sample 01.
          </figcaption>
        </figure>
      </div>
    </section>

    <section class="sec">
      <h2>Decoding with CTC</h2>
      <div class="prose">
        <p>
          The model makes 50 predictions for a five-letter answer, and CTC decides how they line up. In training,
          <code>nn.CTCLoss</code> sums over every 50-step path that reduces to the label. At inference <code>greedy_decode</code> takes the
          top class at each step, merges runs of the same class and removes blanks.
        </p>
        <p>
          The blank is what lets a doubled letter survive. In <code>btffj</code> the two runs of f have a blank between them, so they stay
          two letters. Without it they would merge into one.
        </p>
      </div>
      <figure class="fig">
        <CtcDecode />
        <figcaption>
          <b>Fig. 3.</b> Greedy CTC decoding on sample 09. Each of the 50 steps advances 4 pixels across the image. The path is written by
          hand to show the rule. It is not model output.
        </figcaption>
      </figure>
      <p class="prose"><a :href="withBase('/guide/ctc-loss')">CTC loss and decoding in this code</a></p>
    </section>

    <section class="sec">
      <h2>What the repository states</h2>
      <div class="table-scroll">
        <table class="facts">
          <caption>
            <b>Table 1.</b> Figures and constants, each with the file it comes from.
          </caption>
          <thead>
            <tr>
              <th scope="col">Property</th>
              <th scope="col">Value</th>
              <th scope="col">Source</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="f in facts" :key="f.k">
              <th scope="row">{{ f.k }}</th>
              <td :class="{ mono: f.mono }">{{ f.v }}</td>
              <td class="src">{{ f.src }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <p class="prose note">
        The notebook adds that a retry or two puts the effective success rate near 100%. Every prediction comes back with a confidence
        score, so a caller can retry the weak ones. The repository has no benchmark set beyond the ten images in Fig. 1, and this page does
        not reproduce the accuracy figure.
      </p>
    </section>

    <section class="sec">
      <h2>Running it</h2>
      <p class="prose">
        Put a trained <code>ctc_model.pt</code> in the project root first. The Python class returns the text and a confidence between 0 and
        1. The HTTP server and the Node.js module wrap the same model.
      </p>
      <div class="listings">
        <figure class="listing">
          <pre><code>{{ py }}</code></pre>
          <figcaption><b>Listing 1.</b> Python, from <code>infer.py</code>.</figcaption>
        </figure>
        <figure class="listing">
          <pre><code>{{ http }}</code></pre>
          <figcaption><b>Listing 2.</b> HTTP, from <code>server.py</code>.</figcaption>
        </figure>
        <figure class="listing">
          <pre><code>{{ node }}</code></pre>
          <figcaption><b>Listing 3.</b> Node.js over ONNX, from <code>node/solve.js</code>.</figcaption>
        </figure>
      </div>
    </section>

    <section class="sec">
      <h2>Scope</h2>
      <div class="prose">
        <p>
          The model only knows the E-captcha alphabet and the five-character length, so it is not a general captcha solver. Other text
          captchas need their own training run. A different alphabet or length also means changing the constants in
          <code>model_ctc.py</code>, <code>gen_synthetic.py</code> and <code>node/solve.js</code>.
        </p>
        <p>Challenge widgets such as reCAPTCHA or hCaptcha are out of scope.</p>
      </div>
    </section>

    <section class="sec">
      <h2>Guides</h2>
      <ol class="refs">
        <li v-for="g in guides" :key="g.href">
          <a :href="withBase(g.href)">{{ g.t }}</a>
          <span>{{ g.d }}</span>
        </li>
      </ol>
    </section>
  </div>
</template>

<style scoped>
.paper {
  max-width: 1160px;
  margin: 0 auto;
  padding: 3.5rem 24px 5rem;
  color: var(--ec-ink);
  counter-reset: sec;
}
.paper :deep(code),
.paper code {
  font-family: var(--ec-mono);
  font-size: 0.84em;
  font-variant-numeric: lining-nums;
}
a {
  color: var(--ec-accent);
  text-decoration: underline;
  text-decoration-thickness: 1px;
  text-underline-offset: 3px;
}
a:hover {
  color: var(--ec-accent-deep);
}

.front {
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(0, 1fr);
  gap: 4.5rem;
  align-items: start;
  padding-bottom: 3.5rem;
}
h1 {
  font-size: clamp(2.3rem, 4.7vw, 3.75rem);
  line-height: 1.04;
  font-weight: 480;
  letter-spacing: -0.024em;
  text-wrap: balance;
}
.byline {
  margin-top: 1.5rem;
  font-size: 1.05rem;
  font-style: italic;
  color: var(--ec-ink-2);
}
.abstract {
  margin-top: 1.6rem;
  padding-top: 1.4rem;
  border-top: 1px solid var(--ec-rule-strong);
  font-size: 1.14rem;
  line-height: 1.62;
  max-width: 62ch;
}
.abstract b {
  font-weight: 650;
}
.actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 1rem 1.8rem;
  margin-top: 2rem;
}
.primary {
  display: inline-block;
  padding: 0.62rem 1.25rem 0.68rem;
  background: var(--ec-accent);
  color: #fff;
  font-size: 1.05rem;
  font-weight: 550;
  text-decoration: none;
  border-radius: 2px;
  transition: background-color 0.15s;
}
.primary:hover {
  background: var(--ec-accent-deep);
  color: #fff;
}
.source {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--ec-ink);
  font-size: 1.05rem;
}

.fig-samples {
  margin: 0.6rem 0 0;
}

.sec {
  counter-increment: sec;
  display: grid;
  grid-template-columns: 4.5rem minmax(0, 1fr);
  padding: 2.6rem 0 3rem;
  border-top: 1px solid var(--ec-rule-strong);
}
.sec > * {
  grid-column: 2;
}
.sec::before {
  content: counter(sec);
  grid-column: 1;
  grid-row: 1;
  font-size: 1.7rem;
  line-height: 1.2;
  font-weight: 480;
  color: var(--ec-accent);
  font-variant-numeric: lining-nums;
}
h2 {
  font-size: 1.7rem;
  line-height: 1.2;
  font-weight: 600;
  letter-spacing: -0.012em;
  margin-bottom: 1.2rem;
}
.prose {
  max-width: 64ch;
  font-size: 1.1rem;
  line-height: 1.66;
}
.prose p + p {
  margin-top: 0.95rem;
}
.note {
  margin-top: 1.3rem;
  font-size: 1rem;
  color: var(--ec-ink-2);
}
.split {
  display: grid;
  grid-template-columns: minmax(0, 0.82fr) minmax(0, 1fr);
  gap: 3.5rem;
  align-items: start;
}
.split .fig {
  margin: 0.3rem 0 0;
}

.facts {
  width: 100%;
  min-width: 34rem;
  border-collapse: collapse;
  border-top: 1.5px solid var(--ec-rule-strong);
  border-bottom: 1.5px solid var(--ec-rule-strong);
  font-size: 1.03rem;
  font-variant-numeric: lining-nums tabular-nums;
}
.facts caption {
  caption-side: top;
  text-align: left;
  padding-bottom: 0.8rem;
  font-size: 0.95rem;
  color: var(--ec-ink-2);
}
.facts caption b {
  color: var(--ec-ink);
  font-weight: 600;
}
.facts th,
.facts td {
  padding: 0.55rem 1.4rem 0.55rem 0;
  text-align: left;
  vertical-align: baseline;
}
.facts thead th {
  font-weight: 600;
  border-bottom: 1px solid var(--ec-rule-strong);
}
.facts tbody th {
  font-weight: 400;
  width: 30%;
}
.facts tbody tr + tr > * {
  border-top: 1px solid var(--ec-rule);
}
.facts td.mono {
  font-family: var(--ec-mono);
  font-size: 0.92rem;
  letter-spacing: 0.06em;
  color: var(--ec-accent);
}
.facts .src {
  width: 30%;
  padding-right: 0;
  font-family: var(--ec-mono);
  font-size: 0.8rem;
  color: var(--ec-ink-2);
}

.listings {
  display: grid;
  gap: 1.8rem;
  max-width: 46rem;
  margin-top: 1.8rem;
}
.listing {
  margin: 0;
  min-width: 0;
}
.listing pre {
  margin: 0;
  padding: 1rem 1.2rem;
  overflow-x: auto;
  background: var(--ec-wash);
  border-left: 2px solid var(--ec-ink);
}
.listing pre code {
  font-size: 0.8rem;
  line-height: 1.7;
  white-space: pre;
}
.listing figcaption {
  margin-top: 0.7rem;
  font-size: 0.95rem;
  color: var(--ec-ink-2);
}
.listing figcaption b {
  color: var(--ec-ink);
  font-weight: 600;
}

.refs {
  margin: 0;
  padding: 0;
  list-style: none;
  counter-reset: ref;
  max-width: 52rem;
}
.refs li {
  counter-increment: ref;
  display: grid;
  grid-template-columns: 2.6rem minmax(0, 1fr);
  padding: 0.7rem 0;
  border-bottom: 1px solid var(--ec-rule);
}
.refs li::before {
  content: '[' counter(ref) ']';
  grid-row: 1 / span 2;
  font-family: var(--ec-mono);
  font-size: 0.85rem;
  line-height: 1.9;
  color: var(--ec-ink-3);
}
.refs a {
  font-size: 1.12rem;
  font-weight: 550;
  justify-self: start;
}
.refs span {
  grid-column: 2;
  color: var(--ec-ink-2);
  font-size: 1rem;
  line-height: 1.5;
}

@media (max-width: 960px) {
  .front,
  .split {
    grid-template-columns: minmax(0, 1fr);
    gap: 2.5rem;
  }
  .fig-samples {
    max-width: 26rem;
  }
}
@media (max-width: 720px) {
  .facts {
    min-width: 0;
  }
  .facts thead {
    position: absolute;
    width: 1px;
    height: 1px;
    overflow: hidden;
    clip-path: inset(50%);
  }
  .facts tbody tr {
    display: block;
    padding: 0.6rem 0;
  }
  .facts tbody tr + tr {
    border-top: 1px solid var(--ec-rule);
  }
  .facts tbody th,
  .facts tbody td {
    display: block;
    width: auto;
    padding: 0;
    border: 0 !important;
  }
  .facts tbody th {
    font-weight: 600;
  }
  .facts td.mono {
    font-size: 0.85rem;
    letter-spacing: 0.02em;
  }
  .paper {
    padding: 2rem 16px 3.5rem;
  }
  .sec {
    grid-template-columns: minmax(0, 1fr);
    padding: 2rem 0 2.4rem;
  }
  .sec > * {
    grid-column: 1;
  }
  .sec::before {
    grid-row: auto;
    font-size: 1.1rem;
    margin-bottom: 0.3rem;
  }
  .abstract {
    font-size: 1.06rem;
  }
}
</style>
