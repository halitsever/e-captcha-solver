import io
import torch
from fastapi import FastAPI, File, UploadFile
from PIL import Image
from model_ctc import load_model, preprocess, greedy_decode

app = FastAPI(title="Text Captcha Solver")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = load_model("ctc_model.pt", device)


@app.post("/solve")
async def solve(file: UploadFile = File(...)):
    img = Image.open(io.BytesIO(await file.read()))
    x = preprocess(img).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(x)
    text = greedy_decode(logits)[0]
    conf = float(logits.softmax(2).max(2).values.mean())
    return {"text": text, "conf": round(conf, 3)}
