/* 
Install:  npm install
CLI:      node solve.js captcha.jpg [ctc_model.onnx]
*/

const ort = require("onnxruntime-node");
const sharp = require("sharp");

const CHARS = "abcdefghjkmnrstuvyz";
const W = 200,
  H = 50;

let _session = null;
async function getSession(modelPath = "ctc_model.onnx") {
  if (!_session) _session = await ort.InferenceSession.create(modelPath);
  return _session;
}

async function toTensor(input) {
  const { data, info } = await sharp(input).resize(W, H, { fit: "fill" }).grayscale().raw().toBuffer({ resolveWithObject: true });
  const ch = info.channels;
  const arr = new Float32Array(W * H);
  for (let i = 0; i < W * H; i++) {
    const g = data[i * ch];
    arr[i] = (g / 255 - 0.5) / 0.5;
  }
  return new ort.Tensor("float32", arr, [1, 1, H, W]);
}

function greedyDecode(logits, T, C) {
  let out = "",
    prev = -1;
  for (let t = 0; t < T; t++) {
    let best = 0,
      bestVal = -Infinity;
    for (let c = 0; c < C; c++) {
      const v = logits[t * C + c];
      if (v > bestVal) {
        bestVal = v;
        best = c;
      }
    }
    if (best !== prev && best !== 0) out += CHARS[best - 1];
    prev = best;
  }
  return out;
}

async function solve(input, modelPath = "ctc_model.onnx") {
  const session = await getSession(modelPath);
  const tensor = await toTensor(input);
  const results = await session.run({ input: tensor });
  const logits = results.logits; // dims [1, T, C]
  const [, T, C] = logits.dims;
  return greedyDecode(logits.data, T, C);
}

module.exports = { solve, getSession };

if (require.main === module) {
  const file = process.argv[2];
  const model = process.argv[3] || "ctc_model.onnx";
  if (!file) {
    console.error("Usage: node solve.js <captcha.jpg> [ctc_model.onnx]");
    process.exit(1);
  }
  solve(file, model)
    .then((t) => console.log(t))
    .catch((e) => {
      console.error(e);
      process.exit(1);
    });
}
