'''
python3 correlation.py --original original.bmp --encrypted encrypted.bmp
'''

import argparse
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def load_image(path):
    return np.asarray(Image.open(path).convert("RGB"))


def adjacent_pixels(image, direction):
    if direction == "Horizontal":
        a = image[:, :-1, :]
        b = image[:, 1:, :]
    elif direction == "Vertical":
        a = image[:-1, :, :]
        b = image[1:, :, :]
    elif direction == "Diagonal":
        a = image[:-1, :-1, :]
        b = image[1:, 1:, :]
    else:
        raise ValueError(direction)

    return a.reshape(-1, 3), b.reshape(-1, 3)


def plot_rgb_3d(ax, image, direction, samples, seed):
    a, b = adjacent_pixels(image, direction)

    rng = np.random.default_rng(seed)
    n = min(samples, len(a))
    idx = rng.choice(len(a), n, replace=False)

    a = a[idx]
    b = b[idx]

    # Light RGB colors matching the reference
    colors = ["#E8A5A5", "#A5D8BE", "#A6C9F0"]
    coefficients = []

    for channel, color in enumerate(colors):
        x = a[:, channel].astype(float)
        y = b[:, channel].astype(float)

        if np.std(x) == 0 or np.std(y) == 0:
            r = float("nan")
        else:
            r = np.corrcoef(x, y)[0, 1]

        coefficients.append(r)

        ax.scatter(
            x,
            y,
            np.full(n, channel),
            #color=["#E57373", "#4CAF80", "#5B9BD5"][channel],
            color=["#D95353", "#369C68", "#4285C5"][channel],
            s=0.7,
            alpha=0.55,
            edgecolors="none",
            depthshade=False,
            rasterized=True
        )

    ax.set_xlim(0, 255)
    ax.set_ylim(0, 255)
    ax.set_zlim(0, 2)

    ax.set_xticks([0, 50, 100, 150, 200, 250])
    ax.set_yticks([0, 50, 100, 150, 200, 250])

    ax.set_zticks([0, 1, 2])
    ax.set_zticklabels(["R", "G", "B"])

    #ax.set_xlabel("Pixel", fontsize=6, labelpad=0)
    #ax.set_ylabel("Neighbor", fontsize=6, labelpad=0)
    ax.tick_params(labelsize=6, pad=0)

    ax.view_init(elev=28, azim=-60) #box height 
    ax.set_box_aspect((1, 1, 0.7))

    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis._axinfo["grid"]["color"] = (0.65, 0.65, 0.65, 0.5)
        axis._axinfo["grid"]["linewidth"] = 0.5

    title = (
        f"{direction}\n"
        f"R={coefficients[0]:.4f}  "
        f"G={coefficients[1]:.4f}  "
        f"B={coefficients[2]:.4f}"
    )

    #ax.set_title(title, fontsize=8, pad=8)
    #ax.set_title(direction, fontsize=15, pad=2)
    return coefficients


def main():
    parser = argparse.ArgumentParser(description="3D RGB adjacent-pixel correlation")

    parser.add_argument("--original", required=True)
    parser.add_argument("--encrypted", required=True)
    parser.add_argument("--samples", type=int, default=5000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--dpi", type=int, default=600)
    parser.add_argument("--output",default="correlation.png")

    args = parser.parse_args()

    if args.samples < 2:
        parser.error("--samples must be at least 2")

    images = [
        ("Original", load_image(args.original)),
        ("Encrypted", load_image(args.encrypted))
    ]

    directions = ["Horizontal", "Vertical", "Diagonal"]

    fig = plt.figure(figsize=(11, 6))

    for row, (label, image) in enumerate(images):
        for col, direction in enumerate(directions):
            ax = fig.add_subplot(2, 3,row * 3 + col + 1,projection="3d")
            if row == 0:
              ax.set_title(direction, fontsize=10, pad=2)

            coefficients = plot_rgb_3d(ax,image,direction,args.samples,args.seed)

            print(
                f"{label} - {direction}: "
                f"R={coefficients[0]:.4f}, "
                f"G={coefficients[1]:.4f}, "
                f"B={coefficients[2]:.4f}"
            )

    fig.subplots_adjust(
        left=0.07,
        right=0.98,
        top=0.92,
        bottom=0.05,
        wspace=0.15,
        hspace=0.02
    )

    fig.text(
        0.07, 0.73,
        "Original",
        rotation=90,
        fontsize=15,
        fontweight="normal",
        ha="center",
        va="center"
    )

    fig.text(
        0.07, 0.27,
        "Encrypted",
        rotation=90,
        fontsize=15,
        fontweight="normal",
        ha="center",
        va="center"
    )

    fig.savefig(
        args.output,
        dpi=args.dpi,
        bbox_inches="tight"
    )

    plt.show()
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
