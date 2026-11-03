"""Pull the small real-data extracts the hero cards are drawn from.

  python tools/extract_data.py <hou-front-stability clone> <drone-swarm repo clone>

Writes tools/data/ns_curves.json (growth-rate curves, public figure data) and
tools/data/drone_window.json (positions only: 6 drones, 20 sim-minutes; no metrics).
"""
import csv
import json
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent / "data"

NS_FILES = {  # figdata file -> legend label (as in the paper's Fig. 2)
    "ns5e-4_x144_m1_random_tl.csv": "nu=5e-4, m=1",
    "ns5e-4_x144_m2_random_tl.csv": "nu=5e-4, m=2",
    "ns5e-4_x144_m0_random_tl.csv": "nu=5e-4, m=0",
    "ns5e-3_x144_m1_random_tl.csv": "nu=5e-3, m=1",
}
DRONE_T0, DRONE_W = 49800.0, 1200.0


def ns_curves(root):
    curves = []
    for name, label in NS_FILES.items():
        rows = [r for r in csv.reader(open(root / "figdata" / name)) if r and not r[0].startswith("#")]
        hdr, rows = rows[0], rows[1:]
        i, j = hdr.index("fraction"), hdr.index("sigma_Tt")
        pts = [(float(r[i]) * 100, float(r[j])) for r in rows if r[j]]
        curves.append({"label": label, "pts": pts})
    return curves


def drone_window(root):
    s = (root / "site" / "timelapse_data.js").read_text(encoding="utf-8")
    sim = json.loads(s[s.index("{"):s.rindex("}") + 1])["sim"]
    tracks = []
    for v in sim["positions"].values():
        before = [p for p in v if p[0] < DRONE_T0][-1:]  # parked drones only log when they move
        after = [p for p in v if p[0] >= DRONE_T0 + DRONE_W][:1]
        inside = [p for p in v if DRONE_T0 <= p[0] < DRONE_T0 + DRONE_W]
        pts = [(round(t - DRONE_T0, 1), x, y, z) for t, x, y, z in before + inside + after]
        tracks.append(pts)
    return {"room": sim["room"], "pads": sim["pads"], "stations": sim["stations"],
            "window_s": DRONE_W, "tracks": tracks}


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "ns_curves.json").write_text(json.dumps(ns_curves(Path(sys.argv[1]))))
    (OUT / "drone_window.json").write_text(json.dumps(drone_window(Path(sys.argv[2]))))
    print("wrote", *sorted(p.name for p in OUT.iterdir()))
