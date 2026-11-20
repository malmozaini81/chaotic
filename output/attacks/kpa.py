r"""
example: 
C:\Users\x\Desktop\test\server\attacks>python kpa.py --plain1 "C:\Users\x\Desktop\test\server\images\originals\original.bmp" --cipher1 "C:\Users\x\Desktop\test\server\images\eoriginal-bif.bmp" --plain2 "C:\Users\x\Desktop\test\server\images\originals\original1.bmp" --cipher2 "C:\Users\x\Desktop\test\server\images\eoriginal1-bif.bmp"
Recovered bytes: 3.1250%
Exact recovery: False

"""


import argparse
import numpy as np
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("--plain1", required=True)
parser.add_argument("--cipher1", required=True)
parser.add_argument("--plain2", required=True)
parser.add_argument("--cipher2", required=True)
args = parser.parse_args()

def load(path):
    return np.array(Image.open(path).convert("RGB"), dtype=np.uint8)

p1 = load(args.plain1)
c1 = load(args.cipher1)
p2 = load(args.plain2)
c2 = load(args.cipher2)

if not (p1.shape == c1.shape == p2.shape == c2.shape):
    raise ValueError("All images must have identical dimensions")

# Recover combined keystream
key = p1 ^ c1

# Attack second ciphertext
recovered = c2 ^ key

Image.fromarray(recovered).save("kpa_result.bmp")

accuracy = np.mean(recovered == p2) * 100
print(f"Recovered bytes: {accuracy:.4f}%")
print(f"Exact recovery: {np.array_equal(recovered, p2)}")
