import argparse, glob, os, sys
import torch
from PIL import Image
from model_ctc import load_model, preprocess, greedy_decode


def solve_image(model, path, device="cpu"):
    x = preprocess(Image.open(path)).unsqueeze(0).to(device)
    with torch.no_grad():
        logits = model(x)                        
        probs = logits.softmax(2)
    text = greedy_decode(logits)[0]
    conf = float(probs.max(2).values.mean())
    return text, conf


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--model", default="ctc_model.pt")
    args = ap.parse_args()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = load_model(args.model, device)

    paths = []
    for inp in args.inputs:
        if os.path.isdir(inp):
            paths += sorted(glob.glob(os.path.join(inp, "*.jpg")))
            paths += sorted(glob.glob(os.path.join(inp, "*.png")))
        else:
            paths += glob.glob(inp)
    if not paths:
        print("No images found", file=sys.stderr); sys.exit(1)
    for p in paths:
        t, c = solve_image(model, p, device)
        print(f"{os.path.basename(p)}\t{t}\t{c:.2f}")


if __name__ == "__main__":
    main()
