r"""RGB histogram comparison on one shared chart.

Usage:
    python histogram_combined.py --original original.bmp --encrypted encrypted.bmp

histogram2.py --original C:\Users\x\Desktop\test\server\output\take\natural.bmp --encrypted C:\Users\x\Desktop\test\server\output\take\enatural.bmp --output C:\Users\x\Desktop\test\server\output\histo-natural.png

histogram2.py --original C:\Users\x\Desktop\test\server\output\take\medical.bmp --encrypted C:\Users\x\Desktop\test\server\output\take\emedical.bmp --output C:\Users\x\Desktop\test\server\output\histo-medical.png

histogram2.py --original C:\Users\x\Desktop\test\server\output\take\control.bmp --encrypted C:\Users\x\Desktop\test\server\output\take\econtrol.bmp --output C:\Users\x\Desktop\test\server\output\histo-control.png

    
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def load_image(path):
    return np.asarray(Image.open(path).convert('RGB'), dtype=np.uint8)


def calculate_entropy(image):
    values = image.reshape(-1)
    counts = np.bincount(values, minlength=256)
    probabilities = counts / counts.sum()
    p = probabilities[probabilities > 0]
    return -np.sum(p * np.log2(p))


def calculate_histogram(image):
    histograms = []
    for channel in range(3):
        counts = np.bincount(image[:, :, channel].reshape(-1), minlength=256)
        histograms.append(counts / counts.sum())
    return histograms


def main():
    parser = argparse.ArgumentParser(description='Combined original/encrypted RGB histograms')
    parser.add_argument('--original', required=True)
    parser.add_argument('--encrypted', required=True)
    parser.add_argument('--dpi', type=int, default=600)
    parser.add_argument('--output', default='histogram.png')
    args = parser.parse_args()

    original = load_image(args.original)
    encrypted = load_image(args.encrypted)
    e1 = calculate_entropy(original)
    e2 = calculate_entropy(encrypted)

    plt.rcParams.update({
        'font.family': 'DejaVu Sans',
        'font.size': 15,
        'xtick.labelsize': 14,
        'ytick.labelsize': 14,
    })
    fig, ax = plt.subplots(figsize=(11, 4.8))
    colors = ['#E64B50', '#2CA25F', '#3478F6']
    channels = ['R', 'G', 'B']
    x = np.arange(256)

    for image, prefix, style in [(original, 'Original', '-'),(encrypted, 'Encrypted', '--')]:
        for hist, color, channel in zip(calculate_histogram(image), colors, channels):
            ax.plot(x, hist, color=color, linestyle=style, linewidth=2.0,
                    label=f'{prefix} {channel}')

    ax.set_xlim(0, 255)
    ax.set_ylim(0, 0.0200)
    ax.set_xticks([0, 64, 128, 192, 255])
    ax.set_yticks(np.arange(0, 0.0201, 0.0025))
    ax.set_xlabel('Pixel value', fontsize=17)
    #ax.set_ylabel('Normalized channel frequency', fontsize=17)
    ax.legend(fontsize=12, ncol=2, loc='upper left', frameon=True)
    ax.text(0.98, 0.97,
            f'{"Original":<10}: {e1:.6f}\n'
            f'{"Encrypted":<10}: {e2:.6f}',
            transform=ax.transAxes, ha='right', va='top', fontsize=20)#,
            #bbox=dict(facecolor='white', edgecolor='#CCCCCC', boxstyle='round,pad=0.3'))

    fig.subplots_adjust(left=0.12, right=0.98, bottom=0.19, top=0.97)
    ax.tick_params(axis="y", labelleft=False)
    fig.savefig(args.output, dpi=args.dpi, bbox_inches='tight')
    #plt.show()
    plt.close(fig)
    print(f'Original entropy:  {e1:.6f} bits/byte')
    print(f'Encrypted entropy: {e2:.6f} bits/byte')
    print(f'Saved: {args.output}')


if __name__ == '__main__':
    main()
