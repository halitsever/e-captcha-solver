import argparse
import csv
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont

IMG_W, IMG_H = 200, 50
ALPHABET = "abcdefghjkmnrstuvyz"    

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]
_FONTS = {}


def _get_font(path, size):
    key = (path, size)
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype(path, size)
    return _FONTS[key]


def _available_fonts():
    return [p for p in FONT_CANDIDATES if os.path.exists(p)]


def _gradient_bg():
    """Left-light to right-dark horizontal gradient, like the real data."""
    left = random.uniform(245, 255)
    right = random.uniform(120, 145)
    row = np.linspace(left, right, IMG_W)
    bg = np.tile(row, (IMG_H, 1))
    vcol = np.linspace(0, random.uniform(4, 10), IMG_H).reshape(-1, 1)
    bg = bg - vcol
    return bg.astype("float32")


def random_text(n=5):
    return "".join(random.choice(ALPHABET) for _ in range(n))


def make_captcha(text=None):
    """Generate one synthetic captcha. Returns (PIL.Image, text)."""
    if text is None:
        text = random_text()
    fonts = _available_fonts()

    bg = _gradient_bg()
    canvas = Image.fromarray(np.clip(bg, 0, 255).astype("uint8"), "L").convert("L")


    baseline = random.uniform(IMG_H - 8, IMG_H - 3)
    base_size = random.randint(40, 48)
    x = random.uniform(6, 14)
    for ch in text:
        fpath = random.choice(fonts)
        size = base_size + random.randint(-2, 2)
        font = _get_font(fpath, size)


        if random.random() < 0.6:
            shade = random.randint(15, 80)
        else:
            shade = random.randint(105, 175)

        bbox = font.getbbox(ch)
        cw = bbox[2] - bbox[0]
        chh = bbox[3] - bbox[1]

        pad = 8
        layer = Image.new("L", (cw + pad * 2, chh + pad * 2), 0)
        alpha = Image.new("L", layer.size, 0)
        d = ImageDraw.Draw(layer)
        da = ImageDraw.Draw(alpha)
        d.text((pad - bbox[0], pad - bbox[1]), ch, fill=shade, font=font)
        da.text((pad - bbox[0], pad - bbox[1]), ch, fill=255, font=font)

        ang = random.uniform(-7, 7)
        layer = layer.rotate(ang, resample=Image.BILINEAR, expand=True)
        alpha = alpha.rotate(ang, resample=Image.BILINEAR, expand=True)

        y = baseline - chh - pad + random.uniform(-2, 2)
        canvas.paste(layer, (int(x), int(y)), alpha)

        x += cw * random.uniform(0.62, 0.82)

    draw = ImageDraw.Draw(canvas)
    for _ in range(random.randint(1, 2)):
        y1 = random.randint(0, IMG_H)
        y2 = random.randint(0, IMG_H)
        shade = random.randint(40, 120)
        draw.line([(-2, y1), (IMG_W + 2, y2)], fill=shade, width=random.randint(1, 2))

    arr = np.asarray(canvas, dtype="float32")
    if random.random() < 0.6:
        arr = arr + np.random.normal(0, random.uniform(2, 8), arr.shape)
    arr = np.clip(arr, 0, 255).astype("uint8")
    return Image.fromarray(arr, "L"), text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=5000)
    ap.add_argument("--out", default="synth")
    ap.add_argument("--labels", default="synth_labels.csv")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    random.seed(args.seed)
    np.random.seed(args.seed)
    os.makedirs(args.out, exist_ok=True)
    with open(args.labels, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["filename", "label"])
        for i in range(args.n):
            img, text = make_captcha()
            fn = f"s_{i:06d}.jpg"
            img.save(os.path.join(args.out, fn), quality=85)
            w.writerow([fn, text])
    print(f"Generated {args.n} synthetic images -> {args.out}/  (labels: {args.labels})")


if __name__ == "__main__":
    main()
