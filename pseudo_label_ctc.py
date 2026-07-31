import argparse, csv, glob, os
import torch
from PIL import Image
from model_ctc import load_model, preprocess, greedy_decode, CAPTCHA_LEN


@torch.no_grad()
def predict(model, path, device):
    x = preprocess(Image.open(path)).unsqueeze(0).to(device)
    logits = model(x)
    text = greedy_decode(logits)[0]
    conf = float(logits.softmax(2).max(2).values.mean())
    return text, conf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--model", default="ctc_model.pt")
    ap.add_argument("--thresh", type=float, default=0.97)
    ap.add_argument("--out", default="pseudo_labels.csv")
    args = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = load_model(args.model, device)
    paths = sorted(glob.glob(os.path.join(args.dir, "*.jpg"))) + \
            sorted(glob.glob(os.path.join(args.dir, "*.png")))
    kept = 0
    with open(args.out, "w", newline="") as f:
        w = csv.writer(f); w.writerow(["filename", "label"])
        for p in paths:
            t, c = predict(model, p, device)
            if c >= args.thresh and len(t) == CAPTCHA_LEN:
                w.writerow([os.path.basename(p), t]); kept += 1
    print(f"Labeled {kept} of {len(paths)} images (conf >= {args.thresh}, exactly {CAPTCHA_LEN} chars) -> {args.out}")
    if paths:
        print(f"Acceptance rate: {kept/len(paths)*100:.1f}%")


if __name__ == "__main__":
    main()
