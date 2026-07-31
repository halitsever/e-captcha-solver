import argparse, csv, os, random
import numpy as np
import torch
import torch.nn as nn
from PIL import Image, ImageDraw
from torch.utils.data import Dataset, DataLoader

from model_ctc import CRNN, encode_text, greedy_decode, IMG_W, IMG_H, CAPTCHA_LEN


def augment(img):
    """Light augmentation. Kept modest so character positions stay readable."""
    img = img.convert("L")
    if random.random() < 0.7:
        ang = random.uniform(-4, 4)
        tx = random.uniform(-4, 4); ty = random.uniform(-2, 2)
        img = img.rotate(ang, resample=Image.BILINEAR, fillcolor=255,
                         translate=(int(tx), int(ty)))
    if random.random() < 0.4:
        d = ImageDraw.Draw(img)
        d.line([(0, random.randint(0, IMG_H)), (IMG_W, random.randint(0, IMG_H))],
               fill=random.randint(70, 150), width=1)
    arr = np.asarray(img, dtype="float32") * random.uniform(0.9, 1.1) + random.uniform(-8, 8)
    if random.random() < 0.3:
        arr = arr + np.random.normal(0, random.uniform(2, 6), arr.shape)
    return Image.fromarray(np.clip(arr, 0, 255).astype("uint8"))


def to_tensor(img):
    img = img.convert("L").resize((IMG_W, IMG_H))
    arr = np.asarray(img, dtype="float32") / 255.0
    return (torch.from_numpy(arr).unsqueeze(0) - 0.5) / 0.5


class DS(Dataset):
    def __init__(self, rows, d, train=True):
        self.rows, self.d, self.train = rows, d, train
    def __len__(self): return len(self.rows)
    def __getitem__(self, i):
        fn, lab = self.rows[i]
        img = Image.open(os.path.join(self.d, fn))
        if self.train: img = augment(img)
        return to_tensor(img), torch.tensor(encode_text(lab), dtype=torch.long)


def collate(batch):
    xs = torch.stack([b[0] for b in batch])
    ys = torch.cat([b[1] for b in batch])
    tlens = torch.tensor([len(b[1]) for b in batch], dtype=torch.long)
    return xs, ys, tlens


def char_acc(pred, tgt, n=CAPTCHA_LEN):
    p = (pred + "_" * n)[:n]
    return sum(a == b for a, b in zip(p, tgt)) / n


@torch.no_grad()
def evaluate(model, loader, device):
    model.eval()
    ca = 0.0; sc = 0; tot = 0
    for xs, ys, tlens in loader:
        logits = model(xs.to(device))
        preds = greedy_decode(logits)
        offs = 0; targets = []
        for tl in tlens:
            targets.append(ys[offs:offs+tl]); offs += tl
        from model_ctc import IDX_TO_CHAR
        for p, t in zip(preds, targets):
            ts = "".join(IDX_TO_CHAR[int(i)] for i in t)
            ca += char_acc(p, ts); sc += (p == ts); tot += 1
    return ca / tot, sc / tot


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="data")
    ap.add_argument("--labels", default="labels.csv")
    ap.add_argument("--val", type=int, default=200)
    ap.add_argument("--epochs", type=int, default=400)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--lr", type=float, default=1e-3)
    ap.add_argument("--out", default="ctc_model.pt")
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()

    random.seed(args.seed); np.random.seed(args.seed); torch.manual_seed(args.seed)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Device:", device)

    rows = [(r["filename"], r["label"].strip().lower())
            for r in csv.DictReader(open(args.labels))]
    random.shuffle(rows)
    val, train = rows[:args.val], rows[args.val:]
    print(f"Train {len(train)}  Val {len(val)}")

    tl = DataLoader(DS(train, args.data, True), batch_size=args.batch, shuffle=True,
                    collate_fn=collate, num_workers=2)
    vl = DataLoader(DS(val, args.data, False), batch_size=args.batch, shuffle=False,
                    collate_fn=collate, num_workers=2)

    model = CRNN().to(device)
    opt = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=1e-5)
    sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=args.epochs)
    ctc = nn.CTCLoss(blank=0, zero_infinity=True)

    best = -1.0
    for ep in range(1, args.epochs + 1):
        model.train(); tot = 0.0
        for xs, ys, tlens in tl:
            xs, ys = xs.to(device), ys.to(device)
            logits = model(xs)                       
            logp = logits.log_softmax(2).permute(1, 0, 2)   
            T = logp.size(0)
            inlen = torch.full((xs.size(0),), T, dtype=torch.long)
            loss = ctc(logp, ys, inlen, tlens)
            opt.zero_grad(); loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 5.0)
            opt.step(); tot += loss.item()
        sched.step()
        if ep % 5 == 0 or ep == args.epochs:
            vca, vsa = evaluate(model, vl, device)
            print(f"Epoch {ep:3d} | loss {tot/len(tl):.3f} | val char {vca:.3f} string {vsa:.3f}")
            if vsa >= best:
                best = vsa; torch.save(model.state_dict(), args.out)
                print(f"   -> saved (val string {vsa:.3f})")
    print(f"Done. Best val string: {best:.3f} -> {args.out}")


if __name__ == "__main__":
    main()
