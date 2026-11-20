
""" 
python3 uaci.py --encrypted encrypted.bmp --encrypted1 encrypted1.bmp
Test	Ideal reference for 8-bit random ciphertext
NPCR	≈ 99.6094%
UACI	≈ 33.4635%
Important: These reference values are for differential testing. 
Do not compare test.bmp directly against etest.bmp to claim differential attack resistance.
You must encrypt the original image twice, changing exactly one pixel in the plaintext for 
the second encryption while keeping the key and chaotic parameters identical. 
"""

import argparse
import numpy as np
from PIL import Image

def uaci(encrypted, encrypted1):
    a = np.asarray(Image.open(encrypted).convert("RGB"), dtype=np.float64)
    b = np.asarray(Image.open(encrypted1).convert("RGB"), dtype=np.float64)

    if a.shape != b.shape:
        raise ValueError("Image dimensions must match")

    return np.mean(np.abs(a - b) / 255.0) * 100

parser = argparse.ArgumentParser()
parser.add_argument("--encrypted", required=True)
parser.add_argument("--encrypted1", required=True)
args = parser.parse_args()

print(f"UACI: {uaci(args.encrypted, args.encrypted1):.6f}%")
