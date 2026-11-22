
# Distributed Chaotic Image Encryption on ESP32-S3

This repository provides supporting experimental evidence for the research paper **"Design and Evaluation of Secure Distributed Chaotic Image Encryption on ESP32-S3."**

The research presents a distributed image encryption system using independent Wi-Fi-connected ESP32-S3 microcontrollers. A Python-based master coordinates image processing across multiple workers using segments of a single continuous chaotic sequence. ECDSA authentication and TLS 1.3 mutual authentication secure device communication.

## Repository Structure

### [Appendices](./Appendices)
Screenshots and supporting evidence for the research paper:
- SHA-256, SSIM, and MSE verification
- Shannon entropy and NPCR evaluation
- Adjacent-pixel correlation
- Known-Plaintext Attack (KPA)
- Chosen-Plaintext Attack (CPA)
- Worker malfunction and task reassignment
- TLS 1.3 communication security

### [attacks](./attacks)
Python script for testing cross-image keystream recovery:
- `kpa.py` — Used for KPA and CPA experiments.

### [evaluations](./evaluations)
Python scripts for image evaluation:
- `verify_sha256.py` — Lossless recovery verification
- `ssim.py` — Structural similarity
- `mse.py` — Mean squared error
- `psnr.py` — Peak signal-to-noise ratio
- `entropy.py` — Shannon entropy
- `histogram.py` — Pixel intensity distribution
- `npcr.py` — Number of Pixels Change Rate
- `uaci.py` — Unified Average Changing Intensity
- `correlation.py` — Adjacent-pixel correlation

### [output](./output)
Experimental images and recorded evaluation results:
- Original BMP images
- Single-pixel-modified BMP images
- Encrypted and decrypted BMP images
- Chosen plaintext images (black, white, and one-white-pixel)
- Correlation plots and image samples
- Text files containing actual experimental outputs:
- Encryption and decryption images demonstrating different worker counts and block sizes.
  - `sha256.txt`
  - `ssim.txt`
  - `mse.txt`
  - `entropy.txt`
  - `correlation.txt`
  - `pncr-uaci.txt`
  - `kpa.txt`

## Purpose

This repository allows readers and researchers to inspect the experimental data, verify the reported measurements, and examine supporting evidence.

## Scope

This repository contains evaluation scripts and experimental evidence. It does not include the complete ESP32-S3 firmware or distributed system implementation.

## Repository Link

https://github.com/malmozaini81/chaotic/
