"""
ADSRLab — Procedural SFX synthesis toolkit for games.

Core primitives:
- oscillators (sine/square/saw)
- ADSR envelopes
- sweeps + noise
- mixing + normalization
- WAV export + optional MP3 (ffmpeg)
"""

from .envelope import adsr_envelope
from .dsp import oscillator, sweep_exp, white_noise, mix, normalize_peak
from .export import write_wav_mono16, wav_to_mp3

__all__ = [
    "adsr_envelope",
    "oscillator",
    "sweep_exp",
    "white_noise",
    "mix",
    "normalize_peak",
    "write_wav_mono16",
    "wav_to_mp3",
]
