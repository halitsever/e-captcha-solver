import torch
import torch.nn as nn
import numpy as np
from PIL import Image


CHARS = "abcdefghjkmnrstuvyz"
BLANK = 0                                   
CHAR_TO_IDX = {c: i + 1 for i, c in enumerate(CHARS)}   
IDX_TO_CHAR = {i + 1: c for i, c in enumerate(CHARS)}
NUM_CLASSES = len(CHARS) + 1                
CAPTCHA_LEN = 5
IMG_W, IMG_H = 200, 50


def encode_text(text):
    return [CHAR_TO_IDX[c] for c in text]


def preprocess(img: Image.Image) -> torch.Tensor:
    """PIL image to a normalized (1, H, W) tensor in the range [-1, 1]."""
    img = img.convert("L").resize((IMG_W, IMG_H))
    arr = np.asarray(img, dtype="float32") / 255.0
    t = torch.from_numpy(arr).unsqueeze(0)
    return (t - 0.5) / 0.5


class CRNN(nn.Module):
    def __init__(self, num_classes=NUM_CLASSES, rnn_hidden=256):
        super().__init__()

        def conv(cin, cout, pool):
            return nn.Sequential(
                nn.Conv2d(cin, cout, 3, padding=1),
                nn.BatchNorm2d(cout),
                nn.ReLU(inplace=True),
                nn.Conv2d(cout, cout, 3, padding=1),
                nn.BatchNorm2d(cout),
                nn.ReLU(inplace=True),
                nn.MaxPool2d(pool),
            )


        self.cnn = nn.Sequential(
            conv(1,   32, (2, 2)),     
            conv(32,  64, (2, 2)),     
            conv(64, 128, (2, 1)),     
            conv(128, 256, (2, 1)),   
            conv(256, 256, (3, 1)),   
        )

        self.rnn = nn.LSTM(256, rnn_hidden, num_layers=2,
                           bidirectional=True, batch_first=True, dropout=0.2)
        self.fc = nn.Linear(rnn_hidden * 2, num_classes)

    def forward(self, x):
        f = self.cnn(x)                     
        b, c, h, w = f.size()
        assert h == 1, f"expected height 1, got {h}"
        f = f.squeeze(2).permute(0, 2, 1)    
        f, _ = self.rnn(f)                    
        logits = self.fc(f)                 
        return logits                        


@torch.no_grad()
def greedy_decode(logits):
    """logits: (B, T, C). Greedy CTC: take the top class, collapse repeats, drop blanks."""
    idxs = logits.argmax(dim=2).cpu().numpy()   
    out = []
    for row in idxs:
        chars = []
        prev = -1
        for i in row:
            if i != prev and i != BLANK:
                chars.append(IDX_TO_CHAR.get(int(i), ""))
            prev = i
        out.append("".join(chars))
    return out


def load_model(weights_path, device="cpu"):
    m = CRNN()
    m.load_state_dict(torch.load(weights_path, map_location=device))
    m.to(device).eval()
    return m
