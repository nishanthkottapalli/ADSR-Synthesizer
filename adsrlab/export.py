from __future__ import annotations

import os
import shutil
import subprocess
import wave
import numpy as np


def write_wav_mono16(path: str, y: np.ndarray, *, sr: int = 44100) -> None:
    """
    Write mono 16-bit PCM WAV.
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    y = np.asarray(y, dtype=np.float32)
    y16 = np.int16(np.clip(y, -1.0, 1.0) * 32767)

    with wave.open(path, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(int(sr))
        wf.writeframes(y16.tobytes())


def _ensure_ffmpeg() -> str:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError(
            "ffmpeg not found on PATH. Install ffmpeg to enable MP3 export."
        )
    return ffmpeg


def wav_to_mp3(wav_path: str, mp3_path: str, *, quality: int = 4) -> None:
    """
    Convert WAV to MP3 using ffmpeg + libmp3lame.
    quality: ffmpeg -qscale:a (0 best .. 9 worst). 4 is a good default.
    """
    ffmpeg = _ensure_ffmpeg()
    os.makedirs(os.path.dirname(mp3_path) or ".", exist_ok=True)

    subprocess.check_call(
        [
            ffmpeg,
            "-y",
            "-hide_banner",
            "-loglevel",
            "error",
            "-i",
            wav_path,
            "-codec:a",
            "libmp3lame",
            "-qscale:a",
            str(int(quality)),
            mp3_path,
        ]
    )
