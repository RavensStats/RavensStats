"""Linear A hero: the card frame with the real demo recording playing in its right panel, as a GIF.

  python tools/build_linear_a.py <demo.mp4> [--edge <msedge.exe>]

GitHub never autoplays README videos, but GIFs loop like the SVG cards. The frame comes from
heroes.linear_a (same palette and text layout as the other heroes); headless Edge rasterises it,
then ffmpeg composites the recording (sped up 1.4x, 10 fps) with rounded corners.
Needs ffmpeg on PATH and Pillow.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

import heroes
from common import DARK, LIGHT

ASSETS = Path(__file__).resolve().parent.parent / "assets" / "hero"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
SPEED, FPS = 1.4, 10
TRIM = 1.0  # the recording opens on a blank page


def probe(video):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(video)],
                       check=True, capture_output=True, text=True)
    return float(r.stdout)


def rasterise(svg, png, bg, edge, tmp):
    page = tmp / "frame.html"
    (tmp / "frame.svg").write_text(svg, encoding="utf-8")
    page.write_text(f'<!doctype html><body style="margin:0;background:{bg}">'
                    f'<img src="frame.svg" width="840" height="300" style="display:block"></body>')
    subprocess.run([edge, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--user-data-dir={tmp / 'prof'}",
                    "--window-size=840,300", f"--screenshot={png}", page.as_uri()],
                   check=True, capture_output=True)


if __name__ == "__main__":
    video = Path(sys.argv[1])
    edge = sys.argv[sys.argv.index("--edge") + 1] if "--edge" in sys.argv else EDGE
    x, y, w, h = heroes.VIDEO_BOX
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        mask = tmp / "mask.png"
        m = Image.new("L", (w, h), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radius=9, fill=255)
        m.save(mask)
        for P in (LIGHT, DARK):
            card = tmp / f"card-{P['name']}.png"
            rasterise(heroes.linear_a(P), card, P["bg"], edge, tmp)
            out = ASSETS / f"linear-a-{P['name']}.gif"
            dur = f"{(probe(video) - TRIM) / SPEED:.2f}"
            comp = (f"[1:v]setpts=PTS/{SPEED},fps={FPS},scale={w}:{h}:flags=lanczos,format=rgba[v];"
                    f"[2:v]format=gray[m];[v][m]alphamerge[vm];[0:v][vm]overlay={x}:{y}:shortest=1")
            stills = ["-loop", "1", "-framerate", str(FPS), "-t", dur]  # bounded, so nothing piles up
            inputs = [*stills, "-i", str(card), "-ss", str(TRIM), "-i", str(video), *stills, "-i", str(mask)]
            pal = tmp / "palette.png"  # two passes: no frame buffering for palettegen
            subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex",
                            comp + ",palettegen=max_colors=200:stats_mode=diff", "-frames:v", "1", str(pal)], check=True)
            subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-i", str(pal), "-filter_complex",
                            comp + "[c];[c][3:v]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle",
                            "-loop", "0", str(out)], check=True)
            print(f"{out.name} {out.stat().st_size / 1e6:.2f} MB")
