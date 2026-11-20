""" 
python3 psnr.py --original test.bmp --encrypted etest.bmp --decrypted result.bmp
"""

import argparse
import numpy as np
from PIL import Image

def psnr(image1, image2):
    a = np.asarray(Image.open(image1).convert("RGB"), dtype=np.float64)
    b = np.asarray(Image.open(image2).convert("RGB"), dtype=np.float64)

    if a.shape != b.shape:
        raise ValueError("Image dimensions must match")

    mse = np.mean((a - b) ** 2)
    return float("inf") if mse == 0 else 10 * np.log10(255**2 / mse)

parser = argparse.ArgumentParser()
parser.add_argument("--original", required=True)
parser.add_argument("--encrypted", required=True)
parser.add_argument("--decrypted", required=True)
args = parser.parse_args()

print(f"Original vs Encrypted: {psnr(args.original, args.encrypted):.6f} dB")
print(f"Original vs Decrypted: {psnr(args.original, args.decrypted):.6f} dB")
