
# Distributed Chaotic Image Encryption on ESP32-S3

This repository provides supporting experimental evidence for the research paper **"Design and Evaluation of Secure Distributed Chaotic Image Encryption on ESP32-S3."**

The research presents a distributed image encryption system using independent Wi-Fi-connected ESP32-S3 microcontrollers. A Python-based master coordinates image processing across multiple workers using segments of a single continuous chaotic sequence. ECDSA authentication and TLS 1.3 mutual authentication secure device communication.

## Repository Contents

- **Python Evaluation Scripts:** Tools used to calculate and verify experimental metrics.
- **Test Images:** Original, encrypted, and decrypted BMP images.
- **Experimental Results:** Verification outputs covering correctness, image statistics, and cryptographic attack tests.
- **Execution Logs:** Evidence of distributed processing, fault tolerance, and task reassignment.
- **Supporting Tables and Figures:** Additional experimental evidence referenced in the paper.

## Purpose

This repository allows readers and researchers to inspect the experimental data, verify the reported measurements, and examine supporting evidence.

## Scope

This repository contains evaluation scripts and experimental evidence. It does not include the complete ESP32-S3 firmware or distributed system implementation.

## Repository Link

https://github.com/malmozaini81/chaotic/
