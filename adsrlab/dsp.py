from __future__ import annotations

import math
import numpy as np

from .envelope import adsr_envelope


def _time(n: int, sr: int) -> np.ndarray:
    return (np.arange(n, dtype=np.float32) / float(sr)).astype(np.float32)


def oscillator(
    freq: float,
    dur: float,
    *,
    sr: int = 44100,
    vol: float = 0.6,
    wave: str = "sine",
    adsr: tuple[float, float, float, float] = (0.02, 0.08, 0.7, 0.12),
) -> np.ndarray:
    """
    Basic oscillator with ADSR.
    wave: "sine" | "square" | "saw"
    """
    n = int(sr * float(dur))
    if n <= 0:
        return np.zeros(0, dtype=np.float32)

    t = _time(n, sr)
    w = wave.lower()

    if w == "sine":
        y = np.sin(2.0 * np.pi * float(freq) * t)
    elif w == "square":
        y = np.sign(np.sin(2.0 * np.pi * float(freq) * t))
    elif w == "saw":
        # normalized saw: -1..1
        y = 2.0 * (t * float(freq) - np.floor(0.5 + t * float(freq)))
    else:
        y = np.sin(2.0 * np.pi * float(freq) * t)

    y = y.astype(np.float32)
    a, d, s, r = adsr
    y *= adsr_envelope(n, a=a, d=d, s=s, r=r)

    return (float(vol) * y).astype(np.float32)


def sweep_exp(
    f0: float,
    f1: float,
    dur: float,
    *,
    sr: int = 44100,
    vol: float = 0.6,
    adsr: tuple[float, float, float, float] = (0.01, 0.06, 0.5, 0.2),
) -> np.ndarray:
    """
    Exponential frequency sweep using phase integration.
    """
    n = int(sr * float(dur))
    if n <= 0:
        return np.zeros(0, dtype=np.float32)

    t = _time(n, sr)
    f0 = float(max(1e-6, f0))
    f1 = float(max(1e-6, f1))
    dur = float(max(1e-6, dur))

    k = math.log(f1 / f0) / dur
    # phase(t) = 2π * f0 * (exp(k t) - 1) / k
    phase = 2.0 * np.pi * f0 * (np.exp(k * t) - 1.0) / k
    y = np.sin(phase).astype(np.float32)

    a, d, s, r = adsr
    y *= adsr_envelope(n, a=a, d=d, s=s, r=r)
    return (float(vol) * y).astype(np.float32)


def white_noise(
    dur: float,
    *,
    sr: int = 44100,
    vol: float = 0.35,
    adsr: tuple[float, float, float, float] = (0.005, 0.05, 0.4, 0.25),
    rng: np.random.Generator | None = None,
) -> np.ndarray:
    """
    White noise burst with ADSR + normalization.
    """
    n = int(sr * float(dur))
    if n <= 0:
        return np.zeros(0, dtype=np.float32)

    if rng is None:
        rng = np.random.default_rng()

    y = rng.standard_normal(n).astype(np.float32)

    a, d, s, r = adsr
    y *= adsr_envelope(n, a=a, d=d, s=s, r=r)

    peak = float(np.max(np.abs(y))) if n > 0 else 0.0
    if peak > 1e-9:
        y /= peak

    return (float(vol) * y).astype(np.float32)


def mix(*tracks: np.ndarray) -> np.ndarray:
    """
    Sum tracks; return float32. (No clipping protection here.)
    """
    if not tracks:
        return np.zeros(0, dtype=np.float32)
    n = max((len(x) for x in tracks), default=0)
    y = np.zeros(n, dtype=np.float32)
    for x in tracks:
        if x is None or len(x) == 0:
            continue
        y[: len(x)] += x.astype(np.float32, copy=False)
    return y


def normalize_peak(y: np.ndarray, *, headroom: float = 0.95) -> np.ndarray:
    """
    Peak-normalize to headroom (<=1.0). Safe for export.
    """
    if y is None or len(y) == 0:
        return np.zeros(0, dtype=np.float32)

    y = y.astype(np.float32, copy=False)
    peak = float(np.max(np.abs(y)))
    if peak < 1e-9:
        return y.copy()

    scale = float(headroom) / peak
    if scale >= 1.0:
        return y.copy()
    return (y * scale).astype(np.float32)
