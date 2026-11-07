"""Pull the small real-data extracts the hero cards are drawn from.

  python tools/extract_data.py <hou-front-stability clone> <drone-swarm repo clone> [<Proth survivors.bin>]

Writes tools/data/ns_curves.json (growth-rate curves, public figure data),
tools/data/drone_window.json (positions only: 6 drones, 20 sim-minutes; no metrics) and, given the
Proth Prime Search phase-A bitmap, tools/data/proth_sieve_small_k.json (240 odd k: smallest factor or survivor).
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


def proth_sieve(bitmap, n=332_200_000, k_max=480, q_max=10 ** 6):
    """First odd k of k*2^n+1: smallest prime factor <= q_max, -1 if only a larger factor (<= 8e12) is known,
    0 if a survivor. bitmap = Proth Prime Search phase-A survivors.bin (bit (k-1)/2, little-endian)."""
    bits = bitmap.read_bytes()
    alive = lambda k: (bits[(k - 1) // 2 >> 3] >> ((k - 1) // 2 & 7)) & 1
    ks = range(1, k_max, 2)
    composite = bytearray(q_max + 1)
    small = {}
    for q in range(3, q_max + 1, 2):  # odd primes q in increasing order, so the first hit is the smallest factor
        if composite[q]:
            continue
        composite[q * q::2 * q] = b"\x01" * len(range(q * q, q_max + 1, 2 * q))
        r = (-pow(2, -n, q)) % q
        for k in ks:
            if k not in small and k % q == r:
                small[k] = q
    return {"source": "Proth Prime Search phase A: all odd k < 1e9 sieved by every prime q <= 8e12",
            "n": n, "k_range": [1, k_max - 1],
            "note": "per odd k: smallest prime factor q <= 1e6 of k*2^n+1; -1 = smallest factor in (1e6, 8e12]; "
                    "0 = survivor (no factor <= 8e12)",
            "cells": [[k, 0 if alive(k) else small.get(k, -1)] for k in ks]}


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    (OUT / "ns_curves.json").write_text(json.dumps(ns_curves(Path(sys.argv[1]))))
    (OUT / "drone_window.json").write_text(json.dumps(drone_window(Path(sys.argv[2]))))
    if len(sys.argv) > 3:  # optional: <Proth Prime Search>/hephaestus_worker/allk/phaseA/survivors.bin
        (OUT / "proth_sieve_small_k.json").write_text(json.dumps(proth_sieve(Path(sys.argv[3])), separators=(",", ":")))
    print("wrote", *sorted(p.name for p in OUT.iterdir()))
