# ADSR Synthesizer

**ADSR Synthesizer (ADSR-Synthesizer)** is a small, focused toolkit for **procedural SFX synthesis for games**, built in Python.

It is designed to generate **clean, consistent, game-ready sound effects** using classic DSP building blocks, with an emphasis on determinism, repeatability, and low asset overhead.

This repository exists as a **reference and internal tooling project** under **TF141 Labs**, the applied engineering lab of **NISHANTH MURTHY KOTTAPALLI**.

---

## What this toolkit provides

ADSR Synthesizer focuses on **code-driven sound generation**, suitable for games, simulations, and tooling pipelines.

Core capabilities include:

- **Oscillators**
  - Sine
  - Square
  - Sawtooth

- **ADSR envelopes**
  - Attack / Decay / Sustain / Release shaping
  - Deterministic envelope control

- **Frequency sweeps**
  - Whooshes
  - Risers
  - Drops

- **Noise sources**
  - Impacts
  - Clicks
  - Wind / whoosh layers

- **Mixing & normalization**
  - Predictable output levels
  - Batch-friendly processing

- **Export**
  - WAV output
  - Optional MP3 encoding via FFmpeg

- **Asset packaging**
  - Optional ZIP bundling for game builds or pipelines

The goal is not musical synthesis, but **practical SFX generation for interactive systems**.

---

## Why procedural audio

Procedural audio is especially effective when you need to:

- Maintain a consistent sound style quickly
- Generate variations to avoid repetitive SFX
- Keep builds lightweight
- Regenerate assets deterministically from code
- Integrate audio generation into build or tooling pipelines

This project is intentionally **minimal and explicit**, avoiding opaque abstractions.

---

## Quick start

### Requirements

- Python **3.10+** (recommended)
- `numpy`
- `Pillow` (only if generating icons or images)
- `ffmpeg` (only if exporting MP3)

Install dependencies:

```bash
pip install -r requirements.txt
````

Asset generation is typically driven via scripts in `scripts/`.

---

## Intended usage & scope

> **Important**

This repository is **public for visibility and reference**, but the code is **proprietary**.

* Intended for **internal use** by TF141 Labs
* Not licensed for external reuse, redistribution, or derivative works
* No client deliverables or production assets are included

If you are evaluating this repository, treat it as a **design and implementation reference**, not a reusable library.

---

## License

This project is released under a **Proprietary License**.

* Source code is visible for reference purposes only
* No rights are granted for external use, modification, or distribution
* Use is restricted to the copyright holder and explicitly authorized collaborators

See the `LICENSE` file for full terms.

---

## About TF141 Labs

TF141 Labs is the applied engineering lab of **NISHANTH MURTHY KOTTAPALLI**, focused on:

* Reproducible infrastructure
* AI and systems engineering
* Practical, debrief-first technical work

No hype.
No client work.
Just systems that survive contact with reality.

---

<sub>
TF141 Labs is a fictional-inspired lab name.  
No affiliation with Activision or Call of Duty.
</sub>
```
