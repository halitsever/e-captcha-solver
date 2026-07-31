import sys, glob, os
from io import BytesIO
import torch
from PIL import Image
from model_ctc import load_model, preprocess, greedy_decode


class CaptchaSolver:
    def __init__(self, model_path="ctc_model.pt", device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model = load_model(model_path, self.device)

    def solve(self, img):
        """img: a file path (str) or a PIL.Image. Returns (text, confidence)."""
        if isinstance(img, str):
            img = Image.open(img)
        x = preprocess(img).unsqueeze(0).to(self.device)
        with torch.no_grad():
            logits = self.model(x)
        text = greedy_decode(logits)[0]
        conf = float(logits.softmax(2).max(2).values.mean())
        return text, conf

    def solve_bytes(self, data):
        """Solve raw image bytes, for example a captcha fetched over HTTP."""
        return self.solve(Image.open(BytesIO(data)))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python infer.py <image or folder> [model.pt]"); sys.exit(1)
    model_path = sys.argv[2] if len(sys.argv) > 2 else "ctc_model.pt"
    solver = CaptchaSolver(model_path)
    target = sys.argv[1]
    paths = []
    if os.path.isdir(target):
        for ext in ("*.jpg", "*.jpeg", "*.png"):
            paths += sorted(glob.glob(os.path.join(target, ext)))
    else:
        paths = [target]
    for p in paths:
        text, conf = solver.solve(p)
        print(f"{os.path.basename(p)}\t{text}\t{conf:.2f}")
