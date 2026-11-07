"""Write every card in both themes: python tools/build_cards.py"""
from pathlib import Path
from xml.dom import minidom

import heroes
import tiles
import tiles_more_a
import tiles_more_b
from common import DARK, LIGHT

ASSETS = Path(__file__).resolve().parent.parent / "assets"
CAPS = {"banner": 40_000, "hero": 40_000, "tiles": 25_000}

if __name__ == "__main__":
    for name, fn in {**heroes.CARDS, **tiles.CARDS, **tiles_more_a.NEW_CARDS, **tiles_more_b.NEW_CARDS}.items():
        for P in (LIGHT, DARK):
            svg = fn(P)
            minidom.parseString(svg)  # fail loudly on malformed XML
            out = ASSETS / f"{name}-{P['name']}.svg"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(svg, encoding="utf-8")
            cap = CAPS[name.split("/")[0]]
            flag = "" if len(svg.encode()) <= cap else f"  OVER CAP {cap}"
            print(f"{out.relative_to(ASSETS.parent)}  {len(svg.encode()) / 1000:.1f} KB{flag}")
