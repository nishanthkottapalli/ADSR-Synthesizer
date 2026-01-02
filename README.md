# ADSRLab

**ADSRLab** is a small, focused toolkit for **procedural SFX synthesis for games** — built in Python.

It’s designed to generate clean, consistent game-ready sounds using classic building blocks:

- **Oscillators** (sine / square / saw)
- **ADSR envelopes**
- **Frequency sweeps** (e.g., whooshes, risers, drops)
- **Noise bursts** (e.g., impacts, clicks, wind/whoosh layers)
- **Mixing + normalization**
- **Export** (WAV) and optional **MP3 encoding** via FFmpeg
- Optional **asset packaging** (e.g., zip bundles for game builds)

> This repository is currently intended for private/internal use under **TF141 Labs**.

---

## What this repo does best

Procedural audio is ideal for:
- creating a consistent sound style quickly
- generating variations (for “less repetitive” SFX)
- keeping builds lightweight (generate on demand)
- producing deterministic assets from code

---

## Quick start

### Requirements
- Python 3.10+ (recommended)
- `numpy`
- `Pillow` (only if you generate icons / images)
- `ffmpeg` (only if you export MP3)

Install Python deps:
```bash
pip install -r requirements.txt
