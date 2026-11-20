""" 
pip install numpy pillow scikit-image
python3 ssim.py --original original.bmp --encrypted encrypted.bmp --decrypted decrypted.bmp 

Desired results:
Comparison	Expected SSIM
Original vs Encrypted	Close to 0
Original vs Decrypted	1.000000
"""

import argparse
import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity

def ssim(image1, image2):
    a = np.asarray(Image.open(image1).convert("RGB"))
    b = np.asarray(Image.open(image2).convert("RGB"))

    if a.shape != b.shape:
        raise ValueError("Image dimensions must match")

    return structural_similarity(a, b, channel_axis=2, data_range=255)

parser = argparse.ArgumentParser()
parser.add_argument("--original", required=True)
parser.add_argument("--encrypted", required=True)
parser.add_argument("--decrypted", required=True)
args = parser.parse_args()

print(f"Original vs Encrypted: {ssim(args.original, args.encrypted):.6f}")
print(f"Original vs Decrypted: {ssim(args.original, args.decrypted):.6f}")
