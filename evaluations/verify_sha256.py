""" 
python3 verify.py --original test.bmp --decrypted result.bmp
Interpretation:
- IDENTICAL: Both BMP files are byte-for-byte identical, confirming lossless recovery.
- DIFFERENT: At least one byte differs, even if SSIM = 1.0.
This verifies the entire BMP file, including its header and pixel data.
 """

import argparse
import hashlib

def sha256(filename):
    with open(filename, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()

parser = argparse.ArgumentParser()
parser.add_argument("--original", required=True)
parser.add_argument("--decrypted", required=True)
args = parser.parse_args()

a = sha256(args.original)
b = sha256(args.decrypted)

print(f"Original SHA-256:  {a}")
print(f"Decrypted SHA-256: {b}")
print(f"Result: {'IDENTICAL - Lossless recovery' if a == b else 'DIFFERENT - Recovery not exact'}")
