from __future__ import annotations

import numpy as np


def adsr_envelope(
    n: int,
    *,
    a: float = 0.02,
    d: float = 0.08,
    s: float = 0.7,
    r: float = 0.12,
) -> np.ndarray:
    """
    ADSR envelope as fractions of total samples.

    Parameters:
      n: total samples
      a,d,r: fractions (0..1) of n for attack/decay/release
      s: sustain level (0..1)

    Returns:
      float32 array of shape (n,)
    """
    if n <= 0:
        return np.zeros(0, dtype=np.float32)

    a = float(max(0.0, min(1.0, a)))
    d = float(max(0.0, min(1.0, d)))
    r = float(max(0.0, min(1.0, r)))
    s = float(max(0.0, min(1.0, s)))

    a_n = int(n * a)
    d_n = int(n * d)
    r_n = int(n * r)
    s_n = max(0, n - (a_n + d_n + r_n))

    env = np.zeros(n, dtype=np.float32)

    idx = 0
    if a_n > 0:
        env[idx : idx + a_n] = np.linspace(0.0, 1.0, a_n, endpoint=False, dtype=np.float32)
        idx += a_n

    if d_n > 0:
        env[idx : idx + d_n] = np.linspace(1.0, s, d_n, endpoint=False, dtype=np.float32)
        idx += d_n

    if s_n > 0:
        env[idx : idx + s_n] = s
        idx += s_n

    if r_n > 0:
        env[idx:] = np.linspace(s, 0.0, r_n, endpoint=True, dtype=np.float32)

    return env
