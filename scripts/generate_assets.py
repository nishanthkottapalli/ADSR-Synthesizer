from __future__ import annotations

import os
import zipfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from adsrlab.dsp import oscillator, sweep_exp, white_noise, mix, normalize_peak
from adsrlab.export import write_wav_mono16, wav_to_mp3


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ASSETS_DIR = os.path.join(ROOT, "assets")
SOUNDS_DIR = os.path.join(ROOT, "sounds")
DIST_DIR = os.path.join(ROOT, "dist")

SR = 44100


def generate_icon(out_dir: str) -> dict[str, str]:
    os.makedirs(out_dir, exist_ok=True)

    W = H = 1024
    img = Image.new("RGBA", (W, H), (10, 10, 12, 255))
    draw = ImageDraw.Draw(img)

    border = 28
    draw.rounded_rectangle(
        [border, border, W - border, H - border],
        radius=120,
        outline=(200, 30, 45, 255),
        width=18,
    )

    for i in range(0, 320, 2):
        alpha = int(70 * (1 - i / 320))
        draw.rounded_rectangle(
            [border + 40 + i, border + 60 + i, W - border - 40 - i, H - border - 60 - i],
            radius=110,
            fill=(200, 30, 45, alpha),
        )

    # Crown
    cx, cy = W // 2, 310
    crown_w, crown_h = 520, 220
    base_y = cy + crown_h // 2
    left = cx - crown_w // 2
    right = cx + crown_w // 2

    draw.rounded_rectangle([left, base_y - 60, right, base_y + 10], radius=30, fill=(200, 30, 45, 255))

    spike_count = 5
    for s in range(spike_count):
        x0 = left + (s + 0.5) * crown_w / spike_count
        peak_y = cy - crown_h // 2 + (20 if s % 2 == 0 else 0)
        tri = [(x0 - 70, base_y - 60), (x0, peak_y), (x0 + 70, base_y - 60)]
        draw.polygon(tri, fill=(200, 30, 45, 255))

    for gx in [cx - 170, cx, cx + 170]:
        draw.ellipse([gx - 22, base_y - 35, gx + 22, base_y + 9], fill=(245, 190, 60, 255))

    # Big K
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        font = ImageFont.truetype(font_path, 520)
    except Exception:
        font = ImageFont.load_default()

    text = "K"
    tw, th = draw.textbbox((0, 0), text, font=font)[2:]
    draw.text((cx - tw / 2, 410), text, font=font, fill=(245, 245, 248, 255))

    draw.rounded_rectangle(
        [cx - 340, 820, cx + 340, 905],
        radius=40,
        fill=(0, 0, 0, 120),
        outline=(200, 30, 45, 200),
        width=4,
    )

    try:
        font2 = ImageFont.truetype(font_path, 70)
    except Exception:
        font2 = ImageFont.load_default()

    sub = "KINGPIN"
    stw, sth = draw.textbbox((0, 0), sub, font=font2)[2:]
    draw.text((cx - stw / 2, 835), sub, font=font2, fill=(245, 190, 60, 255))

    png_path = os.path.join(out_dir, "icon.png")
    ico_path = os.path.join(out_dir, "icon.ico")
    icns_path = os.path.join(out_dir, "icon.icns")

    img.save(png_path, "PNG")
    img.save(ico_path, format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    img.save(icns_path, format="ICNS")

    return {"png": png_path, "ico": ico_path, "icns": icns_path}


def export_sound(name: str, y: np.ndarray, *, mp3: bool = True) -> dict[str, str]:
    os.makedirs(SOUNDS_DIR, exist_ok=True)

    y = normalize_peak(y, headroom=0.95)

    wav_path = os.path.join(SOUNDS_DIR, name.replace(".mp3", ".wav").replace(".wav", ".wav"))
    write_wav_mono16(wav_path, y, sr=SR)

    out = {"wav": wav_path}

    if mp3:
        mp3_path = os.path.join(SOUNDS_DIR, name if name.endswith(".mp3") else f"{name}.mp3")
        try:
            wav_to_mp3(wav_path, mp3_path, quality=4)
            out["mp3"] = mp3_path
        except Exception as e:
            print(f"[warn] MP3 export skipped ({e})")

    return out


def generate_sfx_bank() -> list[str]:
    """
    Generates a starter SFX bank similar to your prototype:
    click, buy, sell, travel, police, bribe, safehouse, gameover
    """
    rng = np.random.default_rng(42)
    exported = []

    # click: short tick
    y = mix(
        oscillator(900, 0.06, sr=SR, vol=0.5),
        oscillator(1800, 0.03, sr=SR, vol=0.25),
    )
    exported.append(export_sound("click.mp3", y)["wav"])

    # buy: upward triad
    buy = np.concatenate(
        [
            oscillator(523.25, 0.12, sr=SR, vol=0.55),
            oscillator(659.25, 0.12, sr=SR, vol=0.55),
            oscillator(783.99, 0.16, sr=SR, vol=0.55),
        ]
    ).astype(np.float32)
    exported.append(export_sound("buy.mp3", buy)["wav"])

    # sell: downward triad
    sell = np.concatenate(
        [
            oscillator(783.99, 0.12, sr=SR, vol=0.5),
            oscillator(659.25, 0.12, sr=SR, vol=0.5),
            oscillator(523.25, 0.16, sr=SR, vol=0.5),
        ]
    ).astype(np.float32)
    exported.append(export_sound("sell.mp3", sell)["wav"])

    # travel: whoosh + sweep
    travel = mix(
        sweep_exp(220, 880, 0.35, sr=SR, vol=0.55),
        white_noise(0.35, sr=SR, vol=0.25, rng=rng),
    )
    exported.append(export_sound("travel.mp3", travel)["wav"])

    # police: alternating siren + low square bed
    seg = 0.18
    siren = np.concatenate(
        [
            oscillator(740, seg, sr=SR, vol=0.45, wave="sine"),
            oscillator(880, seg, sr=SR, vol=0.45, wave="sine"),
            oscillator(740, seg, sr=SR, vol=0.45, wave="sine"),
            oscillator(880, seg, sr=SR, vol=0.45, wave="sine"),
        ]
    ).astype(np.float32)
    bed = oscillator(110, len(siren) / SR, sr=SR, vol=0.15, wave="square")
    police = mix(siren, bed)
    exported.append(export_sound("police.mp3", police)["wav"])

    # bribe: coin jingle
    bribe = mix(
        oscillator(1200, 0.09, sr=SR, vol=0.35),
        oscillator(1600, 0.11, sr=SR, vol=0.25),
        oscillator(900, 0.14, sr=SR, vol=0.2),
    )
    exported.append(export_sound("bribe.mp3", bribe)["wav"])

    # safehouse: soft chime
    safehouse = mix(
        oscillator(440, 0.22, sr=SR, vol=0.35),
        oscillator(660, 0.26, sr=SR, vol=0.22),
        oscillator(880, 0.30, sr=SR, vol=0.18),
    )
    exported.append(export_sound("safehouse.mp3", safehouse)["wav"])

    # gameover: low buzz + downward sweep
    gameover = mix(
        oscillator(70, 0.6, sr=SR, vol=0.35, wave="square"),
        sweep_exp(220, 55, 0.8, sr=SR, vol=0.35),
    )
    exported.append(export_sound("gameover.mp3", gameover)["wav"])

    return exported


def package_zip(zip_name: str = "kingpin-icons-and-sounds.zip") -> str:
    os.makedirs(DIST_DIR, exist_ok=True)
    zip_path = os.path.join(DIST_DIR, zip_name)

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for base in [ASSETS_DIR, SOUNDS_DIR]:
            if not os.path.isdir(base):
                continue
            for root, _, files in os.walk(base):
                for f in files:
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, ROOT)
                    z.write(full, arcname=rel)

    return zip_path


def main() -> None:
    print("[ADSRLab] generating icon assets...")
    icon_paths = generate_icon(ASSETS_DIR)
    for k, v in icon_paths.items():
        print(f"  - {k}: {os.path.relpath(v, ROOT)}")

    print("[ADSRLab] generating SFX bank...")
    wavs = generate_sfx_bank()
    print(f"  - exported {len(wavs)} WAV files into sounds/ (and MP3 if ffmpeg is available)")

    print("[ADSRLab] packaging zip...")
    zip_path = package_zip()
    print(f"  - wrote: {os.path.relpath(zip_path, ROOT)}")


if __name__ == "__main__":
    main()
