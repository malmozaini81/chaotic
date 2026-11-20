#python3 entropy.py --original test.bmp --encrypted etest.bmp --decrypted result.bmp
import argparse
import numpy as np
from PIL import Image

def entropy(filename):
    pixels = np.asarray(Image.open(filename).convert("RGB"))
    data = pixels.ravel()

    counts = np.bincount(data, minlength=256)
    probabilities = counts[counts > 0] / data.size

    return -np.sum(probabilities * np.log2(probabilities))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--original", required=True)
    parser.add_argument("--encrypted", required=True)
    parser.add_argument("--decrypted", required=True)
    args = parser.parse_args()

    print(f"{'Image':<15} {'Entropy (bits/byte)':>20}")
    print("-" * 36)

    for name, filename in [
        ("Original", args.original),
        ("Encrypted", args.encrypted),
        ("Decrypted", args.decrypted)
    ]:
        print(f"{name:<15} {entropy(filename):>20.6f}")

    print(f"{'Ideal':<15} {8.0:>20.6f}")

if __name__ == "__main__":
    main()
