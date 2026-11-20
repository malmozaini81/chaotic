
""" 
python3 npcr.py --image1 etest.bmp --image2 etest_modified.bmp
Test	Ideal reference for 8-bit random ciphertext
NPCR	≈ 99.6094%
UACI	≈ 33.4635%
Important: These reference values are for differential testing. 
Do not compare test.bmp directly against etest.bmp to claim differential attack resistance.
You must encrypt the original image twice, changing exactly one pixel in the plaintext for the second encryption 
while keeping the key and chaotic parameters identical. 
"""

import argparse
import numpy as np
from PIL import Image

def npcr(image1, image2):
    a = np.asarray(Image.open(image1).convert("RGB"))
    b = np.asarray(Image.open(image2).convert("RGB"))

    if a.shape != b.shape:
        raise ValueError("Image dimensions must match")

    return np.mean(a != b) * 100

parser = argparse.ArgumentParser()
parser.add_argument("--image1", required=True)
parser.add_argument("--image2", required=True)
args = parser.parse_args()

print(f"NPCR: {npcr(args.image1, args.image2):.6f}%")
