
"""
Usage:
python correlation.py --original original.bmp --encrypted encrypted.bmp

correlation2.py --original C:\Users\x\Desktop\test\server\output\take\natural.bmp --encrypted C:\Users\x\Desktop\test\server\output\take\enatural.bmp --output C:\Users\x\Desktop\test\server\output\corr-natural.png

correlation2.py --original C:\Users\x\Desktop\test\server\output\take\medical.bmp --encrypted C:\Users\x\Desktop\test\server\output\take\emedical.bmp --output C:\Users\x\Desktop\test\server\output\corr-medical.png

correlation2.py --original C:\Users\x\Desktop\test\server\output\take\control.bmp --encrypted C:\Users\x\Desktop\test\server\output\take\econtrol.bmp --output C:\Users\x\Desktop\test\server\output\corr-control.png

"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

DIRECTIONS = {
    "Horizontal": (0, 1),
    "Vertical": (1, 0),
    "Diagonal": (1, 1),
}

"""
COLORS = {
    "Horizontal": "#070ef0", #"#2166AC",
    "Vertical": "#f01d0a", #"#2CA25F",
    "Diagonal": "#0feb07", #"#D95F0E",
}
"""
COLORS = {
    "Horizontal": "#555555",
    "Vertical": "#555555",
    "Diagonal": "#555555",
}

def load_image(path):
    return np.asarray(
        Image.open(path).convert("L"), dtype=np.uint8
    )


def get_pairs(image, direction, samples, rng):
    dy, dx = direction
    height, width = image.shape

    y = rng.integers(0, height - dy, samples)
    x = rng.integers(0, width - dx, samples)

    first = image[y, x].astype(float)
    second = image[y + dy, x + dx].astype(float)

    return first, second


def correlation(x, y):
    x = np.asarray(x, dtype=np.float64).ravel()
    y = np.asarray(y, dtype=np.float64).ravel()
    if np.std(x) == 0 or np.std(y) == 0:
        return float("nan")
    return np.corrcoef(x, y)[0, 1]


# Terminal output only — RGB correlations
def print_rgb_results(original_path, encrypted_path):
    results = {}

    for title, path in [
        ("Original", original_path),
        ("Encrypted", encrypted_path),
    ]:
        image = np.asarray(
            Image.open(path).convert("RGB"),
            dtype=np.uint8
        )

        results[title] = {}

        for name, (dy, dx) in DIRECTIONS.items():
            a = image[:image.shape[0]-dy, :image.shape[1]-dx]
            b = image[dy:, dx:]

            values = [
                correlation(a[:, :, c], b[:, :, c])
                for c in range(3)
            ]

            results[title][name] = values

            print(
                f"{title} - {name}: "
                f"R={values[0]:.4f}, "
                f"G={values[1]:.4f}, "
                f"B={values[2]:.4f}"
            )

    means = {
        name: np.mean(np.abs(results["Encrypted"][name]))
        for name in DIRECTIONS
    }

    """
    print("\nEncrypted Mean Absolute Correlation")
    print("| Horizontal | Vertical | Diagonal |")
    print("|------------|----------|----------|")
    print(
        f"| {means['Horizontal']:.4f} "
        f"| {means['Vertical']:.4f} "
        f"| {means['Diagonal']:.4f} |"
    )
    """
    print("\nEncrypted Mean Absolute RGB Correlation")
    print(f"{'Horizontal':>12}  {'Vertical':>12}  {'Diagonal':>12}")
    print("-" * 40)
    print(
        f"{means['Horizontal']:>12.4f}  "
        f"{means['Vertical']:>12.4f}  "
        f"{means['Diagonal']:>12.4f}"
    )
    print()

    print("\nSampled Grayscale Pearson Correlation (Figure Legend)")
    print("-" * 55)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--original", required=True)
    parser.add_argument("--encrypted", required=True)
    parser.add_argument("--samples", type=int, default=1500)
    parser.add_argument("--output", default="correlation.png")
    args = parser.parse_args()

    # Added terminal information only
    print_rgb_results(args.original, args.encrypted)

    images = {
        "Original": load_image(args.original),
        "Encrypted": load_image(args.encrypted),
    }

    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 17,
        "axes.titlesize": 23,
        "axes.labelsize": 19,
        "xtick.labelsize": 16,
        "ytick.labelsize": 16,
    })

    fig, axes = plt.subplots(1, 2, figsize=(12, 5.4))

    for ax, (title, image) in zip(axes, images.items()):
        rng = np.random.default_rng(42)

        for name, direction in DIRECTIONS.items():
            x, y = get_pairs(
                image, direction, args.samples, rng
            )

            r = correlation(x, y)

            ax.scatter(
                x, y,
                s=5,
                alpha=0.35,
                color=COLORS[name],
                linewidths=0,
                label=f"{name[0]}: {r:.4f}"
            )

            print(f"{title:10s} {name:10s}: {r:.6f}")

        ax.set_title(title, pad=12)
        ax.set_xlabel("Pixel intensity")
        ax.set_ylabel("Adjacent pixel intensity")

        ax.set_xlim(0, 255)
        ax.set_ylim(0, 255)
        ax.set_aspect("equal", adjustable="box")

        ax.set_xticks([0, 50, 100, 150, 200, 250])
        ax.set_yticks([0, 50, 100, 150, 200, 250])

        ax.grid(alpha=0.15, linewidth=0.5)
        ax.legend(
            loc="upper left",
            fontsize=17,
            markerscale=3,
            frameon=True
        )

        for spine in ax.spines.values():
            spine.set_linewidth(0.8)

    #fig.tight_layout(pad=1.5)
    fig.subplots_adjust(wspace=0.3)

    fig.savefig(args.output, dpi=600, bbox_inches="tight")
    fig.savefig(
        "correlation.pdf",
        bbox_inches="tight"
    )

    plt.close(fig)


if __name__ == "__main__":
    main()
