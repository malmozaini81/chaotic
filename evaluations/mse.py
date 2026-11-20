""" 
python3 psnr.py --original test.bmp --encrypted etest.bmp --decrypted result.bmp
python3 mse.py --original test.bmp --encrypted etest.bmp --decrypted result.bmp

Expected interpretation
Comparison	PSNR	MSE
Original vs. Encrypted	Low	High
Original vs. Decrypted	Infinity (∞)	0
"""


import argparse
import numpy as np
from PIL import Image

def mse(image1, image2):
    a = np.asarray(Image.open(image1).convert("RGB"), dtype=np.float64)
    b = np.asarray(Image.open(image2).convert("RGB"), dtype=np.float64)

    if a.shape != b.shape:
        raise ValueError("Image dimensions must match")

    return np.mean((a - b) ** 2)

parser = argparse.ArgumentParser()
parser.add_argument("--original", required=True)
parser.add_argument("--encrypted", required=True)
parser.add_argument("--decrypted", required=True)
args = parser.parse_args()

print(f"Original vs Encrypted: {mse(args.original, args.encrypted):.6f}")
print(f"Original vs Decrypted: {mse(args.original, args.decrypted):.6f}")
