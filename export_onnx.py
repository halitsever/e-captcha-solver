import argparse, torch
from model_ctc import load_model

ap = argparse.ArgumentParser()
ap.add_argument("--model", default="ctc_model.pt")
ap.add_argument("--out", default="ctc_model.onnx")
args = ap.parse_args()

model = load_model(args.model, "cpu")
dummy = torch.randn(1, 1, 50, 200)          
torch.onnx.export(
    model, dummy, args.out,
    input_names=["input"], output_names=["logits"],
    opset_version=12, dynamo=False,
)
print("Wrote ONNX ->", args.out)
