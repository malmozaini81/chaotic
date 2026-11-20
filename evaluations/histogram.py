
"""
Install:
    pip install numpy matplotlib pillow

Run:
    python3 histogram.py --original original.bmp --encrypted encrypted.bmp --dpi 600 --output histogram.png
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def load_image(path):
    return np.asarray(Image.open(path).convert("RGB"))


def calculate_entropy(image):
    # Shannon entropy across all RGB bytes
    values = image.reshape(-1)
    counts = np.bincount(values, minlength=256)
    probabilities = counts / counts.sum()
    p = probabilities[probabilities > 0]
    return -np.sum(p * np.log2(p))


def calculate_histogram(image):
    histograms = []
    for channel in range(3):
        counts = np.bincount(image[:, :, channel].reshape(-1),minlength=256)
        histograms.append(counts / counts.sum())
    return histograms


def plot_histogram(ax, image, title):
    colors = ["#E64B50", "#2CA25F", "#3478F6"]
    labels = ["Red", "Green", "Blue"]

    histograms = calculate_histogram(image)
    entropy = calculate_entropy(image)
    x = np.arange(256)

    for hist, color, label in zip(histograms, colors, labels):
        ax.plot(x,hist,color=color,linewidth=0.9,label=label)

    ax.set_title(title, fontsize=12, pad=10)
    ax.set_xlim(0, 255)
    ax.set_ylim(0, 0.0200)
    #ax.set_ylim(0, max(map(np.max, histograms)) * 1.15)
    ax.set_xticks([0, 64, 128, 192, 255])
    ax.set_yticks(np.arange(0, 0.0201, 0.0025))
    #ax.set_xlabel("Pixel intensity (0–255)",fontsize=10)
    #ax.grid(True,alpha=0.15, linewidth=0.5)

    ax.text(
        0.97,
        0.97,
        f"Shannon entropy = {entropy:.6f} bits/byte",
        transform=ax.transAxes,
        ha="right",
        va="top",
        fontsize=9,
        bbox=dict(
            facecolor="white",
            edgecolor="#CCCCCC",
            boxstyle="round,pad=0.25"
        )
    )

    return entropy


def main():
    parser = argparse.ArgumentParser(description="RGB histogram and Shannon entropy")

    parser.add_argument("--original", required=True)
    parser.add_argument("--encrypted", required=True)
    parser.add_argument("--dpi", type=int, default=600)
    parser.add_argument("--output",default="histogram.png")

    args = parser.parse_args()
    original = load_image(args.original)
    encrypted = load_image(args.encrypted)
    fig, axes = plt.subplots(1,2,figsize=(12, 4),sharey=True)
    e1 = plot_histogram(axes[0],original,"Original image")
    e2 = plot_histogram(axes[1],encrypted,"Encrypted image")
    axes[0].set_ylabel("Normalized channel frequency", fontsize=10)
    handles, labels = axes[0].get_legend_handles_labels()

    '''fig.legend(
        handles,
        labels,
        loc="lower center",
        ncol=3,
        frameon=False,
        fontsize=10,
        bbox_to_anchor=(0.5, -0.02)
    )'''

    fig.subplots_adjust(left=0.08,right=0.98,top=0.88,bottom=0.15,wspace=0.15)
    fig.savefig(args.output,dpi=args.dpi,bbox_inches="tight")
    plt.show()

    print(f"Original entropy:  {e1:.6f} bits/byte")
    print(f"Encrypted entropy: {e2:.6f} bits/byte")
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
