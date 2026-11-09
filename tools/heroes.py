"""Banner and the four 840x300 hero cards."""
import json
import math
from pathlib import Path

from common import ACCENTS, chips, doc, f, hero_text, polyline, rng, text, wrap

DATA = Path(__file__).resolve().parent / "data"


# ---------------------------------------------------------------- banner
TAGLINES = [
    "Energy & technology professional · 10+ years in US utilities",
    "Data & business analyst · software developer · test manager",
    "AI research · MSc thesis on long-context LLM inference",
    "Robotics & quantum computing research",
]


def banner(P):
    w, h = 840, 210
    waves = []
    for i, (col, amp, per, y0, dur) in enumerate([("blue", 14, 210, 150, 14), ("violet", 10, 160, 165, 10),
                                                  ("cyan", 18, 280, 178, 18)]):
        pts = [(x, y0 + amp * math.sin(2 * math.pi * x / per)) for x in range(0, 2 * 840 + per, 6)]
        shift = per * round(840 / per)  # whole periods, so the loop is seamless
        waves.append(f'<path d="{polyline(pts)}" fill="none" stroke="{P[col]}" stroke-width="1.6" '
                     f'stroke-opacity=".35"><animateTransform attributeName="transform" type="translate" '
                     f'from="0 0" to="-{shift} 0" dur="{dur}s" repeatCount="indefinite"/></path>')
    r = rng(7)
    nodes, edges = [], []
    pts = [(560 + r() * 250, 28 + r() * 120) for _ in range(14)]
    for i, (x, y) in enumerate(pts):
        for j in range(i):
            if math.dist((x, y), pts[j]) < 70:
                edges.append(f'<line x1="{f(x)}" y1="{f(y)}" x2="{f(pts[j][0])}" y2="{f(pts[j][1])}" '
                             f'stroke="{P["line"]}"/>')
        col = P[ACCENTS[i % len(ACCENTS)]]
        nodes.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="3.2" fill="{col}" class="nd" '
                     f'style="animation-delay:{f(i * 0.37)}s"/>')
    tags = []
    n = len(TAGLINES)
    for i, t in enumerate(TAGLINES):
        tags.append(f'<g class="tg" style="animation-delay:{i * 3}s">'
                    + text(42, 168, "› " + t, P, 15, "ink", "m") + "</g>")
    css = (f".nd{{animation:nd 3s ease-in-out infinite}}@keyframes nd{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}"
           f".tg{{opacity:0;animation:tg {3 * n}s infinite}}"
           f"@keyframes tg{{0%{{opacity:0;transform:translateY(6px)}}3%,22%{{opacity:1;transform:none}}"
           f"25%,100%{{opacity:0;transform:translateY(-6px)}}}}")
    body = ("".join(waves) + "".join(edges) + "".join(nodes)
            + f'<rect x="20" y="138" width="560" height="44" rx="10" fill="{P["card"]}" fill-opacity=".85"/>'
            + text(40, 82, "Andrew Mullen", P, 46, "ink", weight="800", extra=' letter-spacing="-.5"')
            + text(42, 112, "@RavensStats  ·  energy · data · AI · robotics · quantum", P, 13, "muted", "m")
            + "".join(tags))
    return doc(w, h, P, "Andrew Mullen", "Banner: Andrew Mullen, energy and technology professional with 10+ years in "
               "US utilities; data and business analyst, software developer, test manager; AI, robotics and quantum research.", body, css)


# ---------------------------------------------------------------- drone swarm (real sim data)
def drone(P):
    d = json.load(open(DATA / "drone_window.json"))
    s, ox, oy = 52.0, 540.0, 20.0
    X = lambda x: ox + x * s
    Y = lambda y: oy + (5 - y) * s
    (rx0, ry0, _), (rx1, ry1, _) = d["room"]
    out = [f'<clipPath id="room"><rect x="{f(X(rx0))}" y="{f(Y(ry1))}" width="{f((rx1 - rx0) * s)}" '
           f'height="{f((ry1 - ry0) * s)}" rx="6"/></clipPath>',
           f'<rect x="{f(X(rx0))}" y="{f(Y(ry1))}" width="{f((rx1 - rx0) * s)}" height="{f((ry1 - ry0) * s)}" '
           f'rx="6" fill="{P["bg"]}" stroke="{P["line"]}"/>']
    grid = [f'<line x1="{f(X(v))}" y1="{f(Y(ry0))}" x2="{f(X(v))}" y2="{f(Y(ry1))}"/>'
            f'<line x1="{f(X(rx0))}" y1="{f(Y(v))}" x2="{f(X(rx1))}" y2="{f(Y(v))}"/>'
            for v in [0.5 * k for k in range(1, 10)] if rx0 < v < rx1]
    out.append(f'<g stroke="{P["faint"]}">{"".join(grid)}</g>')
    # Lighthouse sweeps: each station's beam swings across the room
    beams = []
    cx, cy = X(2.5), Y(2.5)
    for i, (sx, sy, _) in enumerate(d["stations"]):
        px, py = X(sx), Y(sy)
        a = math.degrees(math.atan2(cy - py, cx - px))
        beams.append(
            f'<path d="M{f(px)} {f(py)} l300 -14 l0 28z" fill="{P["cyan"]}" fill-opacity=".13">'
            f'<animateTransform attributeName="transform" type="rotate" dur="{f(1.6 + 0.3 * i)}s" '
            f'repeatCount="indefinite" values="{f(a - 50)} {f(px)} {f(py)};{f(a + 50)} {f(px)} {f(py)};'
            f'{f(a - 50)} {f(px)} {f(py)}"/></path>')
    out.append(f'<g clip-path="url(#room)">{"".join(beams)}</g>')
    for sx, sy, _ in d["stations"]:
        out.append(f'<rect x="{f(X(sx) - 6)}" y="{f(Y(sy) - 6)}" width="12" height="12" rx="3" '
                   f'fill="{P["cyan"]}"/>')
    for px, py in d["pads"]:
        out.append(f'<rect x="{f(X(px) - 8)}" y="{f(Y(py) - 8)}" width="16" height="16" rx="3" fill="none" '
                   f'stroke="{P["green"]}" stroke-width="1.4" stroke-dasharray="3 2"/>')

    frames = [k * 10.0 for k in range(121)]

    def at(tr, t):
        prev = [p for p in tr if p[0] <= t]
        nxt = [p for p in tr if p[0] > t]
        if not prev:
            return nxt[0]
        a = prev[-1]
        if not nxt or nxt[0][0] - a[0] > 12:  # parked: positions are only logged while moving
            return a
        b = nxt[0]
        u = (t - a[0]) / (b[0] - a[0])
        return [a[i] + u * (b[i] - a[i]) for i in range(4)]

    dur = "12s"
    for i, tr in enumerate(d["tracks"]):
        col = P[ACCENTS[i]]
        air = [(X(x), Y(y)) for t, x, y, z in tr if 0 <= t <= 1200 and z > 0.3]
        if len(air) > 1:
            out.append(f'<path d="{polyline(air)}" fill="none" stroke="{col}" stroke-opacity=".28" '
                       f'stroke-width="1.3" stroke-linejoin="round"/>')
        ps = [at(tr, t) for t in frames]
        xs = ";".join(f(X(p[1])) for p in ps)
        ys = ";".join(f(Y(p[2])) for p in ps)
        rs = ";".join(f(3.5 + 4.5 * min(p[3], 1.0)) for p in ps)
        ops = ";".join(".95" if p[3] > 0.3 else ".45" for p in ps)
        anim = (f'<animate attributeName="cx" dur="{dur}" repeatCount="indefinite" values="{xs}"/>'
                f'<animate attributeName="cy" dur="{dur}" repeatCount="indefinite" values="{ys}"/>')
        out.append(f'<circle r="11" fill="{col}" fill-opacity=".15">{anim}'
                   f'<animate attributeName="opacity" dur="{dur}" repeatCount="indefinite" values="{ops}"/></circle>'
                   f'<circle fill="{col}" stroke="{P["bg"]}" stroke-width="1.2">{anim}'
                   f'<animate attributeName="r" dur="{dur}" repeatCount="indefinite" values="{rs}"/></circle>')
    out.append(text(X(rx0) - 12, 291, "▣ base station  ⬚ charger  ● drone (size = altitude)",
                    P, 9.5, "muted", "m"))
    left = hero_text(
        P, "RESEARCH · AERIAL ROBOTICS", ["Self-maintaining", "drone swarm"],
        "A Lighthouse-tracked Crazyflie swarm designed to plan around weak tracking coverage, "
        "land to recharge and repair itself; so far tested in simulation and Gazebo with the "
        "real firmware, ahead of hardware flights.",
        ["Python", "ROS 2", "Gazebo", "Crazyflie"],
        "real trajectories from the project simulator · 20 sim-min in 12 s", "cyan", True)
    return doc(840, 300, P, "Self-maintaining drone swarm",
               "Animated top-down view of six simulated Crazyflie drones flying in a room swept by four "
               "Lighthouse base stations, taking turns to land on chargers. Positions come from the project's "
               "own simulator.", left + "".join(out))


# ---------------------------------------------------------------- outage risk from short outages (real offline drift data)
def outage_risk(P):
    d = json.load(open(DATA / "outage_risk_flight.json"))
    T = 16  # seconds per loop
    pc = lambda x: f(x * 100)
    css = []

    def show(name, t0, t1, end=.95):
        """name fades in over t0..t1, holds, fades out over end..end+.03 (fractions of the loop)."""
        css.append(f".{name}{{opacity:0;animation:{name} {T}s infinite}}@keyframes {name}{{0%,{pc(t0)}%{{opacity:0}}"
                   f"{pc(t1)}%,{pc(end)}%{{opacity:1}}{pc(min(end + .03, 1))}%,100%{{opacity:0}}}}")

    out = []
    # ---- scene (schematic): two base stations, the drone (= the reference) and its own estimate
    bs = [(446, 42), (558, 42)]
    dx, dy = 502, 118
    out.append(f'<rect x="432" y="26" width="140" height="170" rx="8" fill="{P["bg"]}" stroke="{P["line"]}"/>')
    for x, y in bs:
        out.append(f'<path d="M{x} {y} L{dx - 8} {dy + 5} L{dx + 8} {dy - 5}z" fill="{P["cyan"]}" class="bm"/>'
                   f'<rect x="{x - 7}" y="{y - 6}" width="14" height="12" rx="3" fill="{P["cyan"]}"/>')
    outs = [(.08, .14, (13, -9)), (.19, .25, (-12, 10)), (.30, .36, (11, 12)), (.54, .68, (-36, 30))]
    # beams keep sweeping (the reference keeps coming); they dim while the drone ignores them
    stops = ["0%{fill-opacity:.24}"]
    for t0, t1, _ in outs:
        stops.append(f"{pc(t0)}%{{fill-opacity:.24}}{pc(t0 + .01)}%,{pc(t1)}%{{fill-opacity:.06}}"
                     f"{pc(t1 + .01)}%{{fill-opacity:.24}}")
    css.append(f".bm{{animation:bm {T}s infinite}}@keyframes bm{{{''.join(stops)}100%{{fill-opacity:.24}}}}")
    # the estimate drifts off during each outage and snaps back when fixes resume
    kt, vals = ["0"], ["0 0"]
    for t0, t1, (ex, ey) in outs:
        kt += [f(t0), f(t1), f(t1 + .006)]
        vals += ["0 0", f"{ex} {ey}", "0 0"]
    kt.append("1")
    vals.append("0 0")
    splines = ";".join(["0 0 1 1", ".4 0 .9 .6", "0 0 1 1"] * len(outs) + ["0 0 1 1"])
    est = (f'<g><circle cx="{dx}" cy="{dy}" r="10" fill="none" stroke="{P["amber"]}" stroke-width="2" '
           f'stroke-dasharray="3 2"/><circle cx="{dx}" cy="{dy}" r="2.4" fill="{P["amber"]}"/>'
           f'<animateTransform attributeName="transform" type="translate" dur="{T}s" repeatCount="indefinite" '
           f'values="{";".join(vals)}" keyTimes="{";".join(kt)}" calcMode="spline" keySplines="{splines}"/></g>')
    icon = "".join(f'<circle cx="{dx + sx * 9}" cy="{dy + sy * 9}" r="4.5" fill="none" stroke="{P["ink"]}" '
                   f'stroke-width="1.4"/>' for sx in (-1, 1) for sy in (-1, 1))
    icon += (f'<path d="M{dx - 9} {dy - 9} L{dx + 9} {dy + 9} M{dx + 9} {dy - 9} L{dx - 9} {dy + 9}" '
             f'stroke="{P["ink"]}" stroke-width="2"/><circle cx="{dx}" cy="{dy}" r="3" fill="{P["ink"]}"/>')
    line = "".join(f'<animate attributeName="{a}" dur="{T}s" repeatCount="indefinite" values="'
                   + ";".join(f(c + float(v.split()[k])) for v in vals) + f'" keyTimes="{";".join(kt)}" '
                   f'calcMode="spline" keySplines="{splines}"/>' for a, c, k in (("x2", dx, 0), ("y2", dy, 1)))
    out.append(f'<line x1="{dx}" y1="{dy}" x2="{dx}" y2="{dy}" stroke="{P["amber"]}" stroke-width="1.6">{line}</line>'
               + icon + est + '<g class="dl">' + text(dx + 2, dy + 34, "drift", P, 9.5, "amber", "m", weight="600") + "</g>")
    show("dl", .62, .64, end=.67)
    for i, (t0, t1, _) in enumerate(outs):
        out.append(f'<g class="ot{i}">' + text(dx, 168, "fixes ignored", P, 9.5, "red", "m", weight="600",
                                               anchor="middle") + "</g>")
        show(f"ot{i}", t0, t0 + .01, end=t1 - .02)
    out.append(text(dx, 186, "✕ reference  ◌ estimate", P, 8.5, "muted", "m", anchor="middle"))
    out.append(text(dx, 212, "schematic", P, 9.5, "muted", "m", anchor="middle"))
    # ---- real data: drift per outage on one public-dataset flight
    x0, x1, y0, y1, top = 606.0, 812.0, 32.0, 178.0, 0.9
    X = lambda t: x0 + t / 3.3 * (x1 - x0)
    Y = lambda m: y1 - min(m, top) / top * (y1 - y0)
    out.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="{P["bg"]}" stroke="{P["line"]}"/>')
    for v in (.25, .5, .75):
        out.append(f'<line x1="{x0}" x2="{x1}" y1="{f(Y(v))}" y2="{f(Y(v))}" stroke="{P["faint"]}"/>')
    for v, lab in ((0, "0"), (.25, ".25"), (.5, ".50"), (.75, ".75")):
        out.append(text(x0 - 5, Y(v) + 3, lab, P, 9, "muted", "m", anchor="end"))
    out.append(text(x0 + 6, y0 + 13, "drift (m)", P, 9, "muted", "m"))
    for t in (1, 1.5, 3):
        out.append(text(X(t), y1 + 12, f"{t:g} s", P, 9, "muted", "m", anchor="middle"))
    out.append(text((x0 + x1) / 2, 212, "outage length · one public flight", P, 9.5, "muted", "m", anchor="middle"))
    r = rng(5)
    lad = [(1.0, v) for v in d["ladder_1s"]] + [(1.5, v) for v in d["ladder_1.5s"]]
    keys = [r() for _ in lad]
    lad = [lad[i] for i in sorted(range(len(lad)), key=keys.__getitem__)]  # appear in a shuffled order
    G = 6
    groups = [[] for _ in range(G)]
    for i, (t, v) in enumerate(lad):
        groups[i * G // len(lad)].append(f'<circle cx="{f(X(t) + (r() - .5) * 16)}" cy="{f(Y(v))}" r="2.3"/>')
    for g, dots in enumerate(groups):
        out.append(f'<g class="ld{g}" fill="{P["blue"]}" fill-opacity=".75">{"".join(dots)}</g>')
        show(f"ld{g}", .06 + g * .05, .08 + g * .05)
    lim = d["limit_3s_m"]
    own, sim = lim["ladder"], lim["simulator"]
    xb, xl = X(3), X(1.5) + 12
    out.append(f'<g class="bd"><rect x="{f(xb - 12)}" y="{f(Y(own))}" width="24" height="{f(y1 - Y(own))}" '
               f'fill="{P["green"]}" fill-opacity=".18"/>'
               f'<path d="M{f(xl)} {f(Y(own))} H{x1}" stroke="{P["green"]}" stroke-width="2"/>'
               + text(xb - 16, Y(own) - 14, "limit from", P, 9, "green", "m", weight="600", anchor="end")
               + text(xb - 16, Y(own) - 4, "own outages", P, 9, "green", "m", weight="600", anchor="end") + "</g>")
    show("bd", .38, .41)
    held = d["heldout_3s"]
    n_own = sum(v > own for v in held)
    n_sim = sum(v > sim for v in held)
    n_fit = sum(v > lim["simulator_fitted"] for v in held)
    hd = []
    for v in held:
        cls = "ho" if v > own else ("hs" if v > sim else "hn")
        hd.append(f'<circle cx="{f(xb + (r() - .5) * 18)}" cy="{f(Y(v))}" r="2.6" class="{cls}"/>')
    out.append(f'<g class="hd" fill="{P["violet"]}">{"".join(hd)}</g>')
    show("hd", .52, .58)
    css.append(f".ho{{animation:ho {T}s infinite}}@keyframes ho{{0%,62%{{fill:{P['violet']}}}64%,95%{{fill:{P['red']}}}"
               f"98%,100%{{fill:{P['violet']}}}}}"
               f".hs{{animation:hs {T}s infinite}}@keyframes hs{{0%,74%{{fill:{P['violet']}}}77%,95%{{fill:{P['red']}}}"
               f"98%,100%{{fill:{P['violet']}}}}}")
    out.append(f'<g class="sl"><path d="M{f(xl)} {f(Y(sim))} H{x1}" stroke="{P["red"]}" stroke-width="2" '
               f'stroke-dasharray="4 3"/>'
               + text(xb - 16, Y(sim) - 5, "simulator", P, 9, "red", "m", weight="600", anchor="end") + "</g>")
    show("sl", .70, .73)
    caps = [(.0, .37, f"1 · {len(lad)} short outages, one dot each"),
            (.38, .50, "2 · predict the 3 s abort limit"),
            (.52, .69, f"3 · {len(held)} held-out 3 s outages: {n_own} over"),
            (.70, .95, f"4 · simulator's limit: {n_sim} of {len(held)} over")]
    for i, (t0, t1, s) in enumerate(caps):
        out.append(f'<g class="cp{i}">' + text(586, 21, s, P, 10, "ink", "m", weight="600") + "</g>")
        show(f"cp{i}", t0, t0 + .01, end=t1)
    # ---- six public datasets: share of held-out 3 s outages beyond each abort limit (target 10 %)
    ex = d["abort_limit_exceedance_by_dataset"]
    tx0, tx1 = 540.0, 752.0
    TX = lambda p: tx0 + p * (tx1 - tx0)
    out.append(text(432, 236, "abort limit exceeded, 6 public datasets (target 10 %)", P, 9.5, "ink", "m",
                    weight="600"))
    out.append(f'<path d="M{f(TX(.1))} 243 V286" stroke="{P["green"]}" stroke-dasharray="2 2"/>')
    for i, (key, lab, col) in enumerate((("simulator", "datasheet sim", "red"),
                                         ("simulator_fitted", "fitted sim", "red"),
                                         ("ladder", "own outages", "green"))):
        y = 252 + i * 15
        vals = [v[key] for v in ex.values()]
        out.append(text(432, y + 3, lab, P, 9.5, "muted", "m")
                   + f'<line x1="{tx0}" x2="{tx1}" y1="{y}" y2="{y}" stroke="{P["faint"]}" stroke-width="4" '
                   f'stroke-linecap="round"/>'
                   + "".join(f'<circle cx="{f(TX(v))}" cy="{y}" r="3.6" fill="{P[col]}" fill-opacity=".8" '
                             f'stroke="{P["card"]}"/>' for v in vals)
                   + text(tx1 + 10, y + 3, f"{min(vals) * 100:.0f}–{max(vals) * 100:.0f} %", P, 9.5, "ink", "m"))
    left = hero_text(
        P, "RESEARCH · AERIAL ROBOTICS · SAFETY", ["Outage risk from", "short outages"],
        "In flight, a drone briefly ignores its positioning while the system keeps a reference, so drift "
        "is measured directly. Its own safe 1–1.5 s outages predict its longer ones; simulators "
        "misjudge them.",
        ["Python", "Crazyflie", "Lighthouse", "statistics"],
        "real drift data from a public flight log · scene schematic", "blue", True)
    desc = (f"Animated: a schematic drone ignores its positioning fixes while the base stations keep sweeping, and "
            f"its estimate drifts away from the reference. Real offline data from one public-dataset flight: "
            f"{len(lad)} short 1-1.5 s outages build a ladder of drift, a 3 s abort limit is predicted from them, and "
            f"{n_own} of {len(held)} held-out 3 s outages exceed it, against {n_sim} (datasheet noise) and {n_fit} "
            f"(fitted noise) of {len(held)} for the simulators' limits. Below: the share of outages beyond each "
            f"limit on six public datasets.")
    return doc(840, 300, P, "Outage risk from short outages", desc, left + "".join(out),
               "".join(css))


# ---------------------------------------------------------------- quantum (textbook surface code only)
def quantum(P):
    g, ox, oy = 34, 452, 58  # 5x5 data qubits
    Q = lambda i, j: (ox + i * g, oy + j * g)
    out = []
    for i in range(4):
        for j in range(4):
            x, y = Q(i, j)
            col = P["blue"] if (i + j) % 2 == 0 else P["violet"]
            out.append(f'<rect x="{x}" y="{y}" width="{g}" height="{g}" fill="{col}" class="pq" '
                       f'style="animation-delay:{f((i + j) * .18)}s"/>')
    r = g / 2
    for i in range(4):  # weight-2 boundary checks, alternating as on a rotated d=5 code
        if i % 2 == 1:
            x, y = Q(i, 0)
            out.append(f'<path d="M{x} {y} a{r} {r} 0 0 1 {g} 0z" fill="{P["blue"]}" class="pq"/>')
        if i % 2 == 0:
            x, y = Q(i, 4)
            out.append(f'<path d="M{x} {y} a{r} {r} 0 0 0 {g} 0z" fill="{P["blue"]}" class="pq"/>')
    for j in range(4):
        if j % 2 == 0:
            x, y = Q(0, j)
            out.append(f'<path d="M{x} {y} a{r} {r} 0 0 0 0 {g}z" fill="{P["violet"]}" class="pq"/>')
        if j % 2 == 1:
            x, y = Q(4, j)
            out.append(f'<path d="M{x} {y} a{r} {r} 0 0 1 0 {g}z" fill="{P["violet"]}" class="pq"/>')
    # syndrome: an X error on qubit (2,2) flips the two adjacent Z checks (2,1) and (1,2)
    for i, j in ((2, 1), (1, 2)):
        x, y = Q(i, j)
        out.append(f'<rect x="{x + 2}" y="{y + 2}" width="{g - 4}" height="{g - 4}" rx="4" fill="{P["amber"]}" '
                   f'class="syn"/>')
    a, b = Q(2.5, 1.5), Q(1.5, 2.5)
    out.append(f'<path d="M{a[0]} {a[1]} L{b[0]} {b[1]}" pathLength="1" class="fix" stroke="{P["green"]}" '
               f'stroke-width="4" stroke-linecap="round"/>')
    for i in range(5):
        for j in range(5):
            x, y = Q(i, j)
            out.append(f'<circle cx="{x}" cy="{y}" r="5.5" fill="{P["card"]}" stroke="{P["ink"]}" stroke-width="1.6"/>')
    for i in range(4):
        for j in range(4):
            x, y = Q(i + .5, j + .5)
            out.append(f'<circle cx="{x}" cy="{y}" r="2.2" fill="{P["ink"]}" fill-opacity=".55"/>')
    ex, ey = Q(2, 2)
    out.append(f'<circle cx="{ex}" cy="{ey}" r="9" fill="none" stroke="{P["red"]}" stroke-width="3" class="err"/>'
               f'<circle cx="{ex}" cy="{ey}" r="5.5" fill="{P["green"]}" class="ok"/>')
    out.append(text(ox + 2 * g, 228, "rotated surface code, d = 5 (schematic)", P, 9.5, "muted", "m",
                    anchor="middle"))
    leg = [("blue", "X check"), ("violet", "Z check"), ("red", "error"), ("amber", "syndrome"), ("green", "correction")]
    lx = 448
    for col, lab in leg:
        out.append(f'<rect x="{lx}" y="262" width="10" height="10" rx="2" fill="{P[col]}"/>'
                   + text(lx + 14, 271, lab, P, 9.5, "muted", "m"))
        lx += 22 + len(lab) * 6.2
    # scrolling syndrome-extraction circuit
    cx0, cx1, wy = 650, 815, [70, 98, 126, 154, 182]
    circ = [f'<line x1="{cx0}" x2="{cx1}" y1="{y}" y2="{y}" stroke="{P["muted"]}" stroke-opacity=".6"/>' for y in wy]
    gates = []
    pattern = [(0, 2), (1, 2), (3, 2), (4, 2), (2, 0), (2, 4)]
    for k in range(12):
        c, t = pattern[k % 6]
        x = cx0 + 14 + k * 28
        gates.append(f'<line x1="{x}" x2="{x}" y1="{wy[c]}" y2="{wy[t]}" stroke="{P["ink"]}" stroke-width="1.4"/>'
                     f'<circle cx="{x}" cy="{wy[c]}" r="3.5" fill="{P["ink"]}"/>'
                     f'<circle cx="{x}" cy="{wy[t]}" r="7" fill="{P["card"]}" stroke="{P["ink"]}" stroke-width="1.4"/>'
                     f'<path d="M{x - 7} {wy[t]} h14 M{x} {wy[t] - 7} v14" stroke="{P["ink"]}" stroke-width="1.4"/>')
    circ.append(f'<clipPath id="cc"><rect x="{cx0}" y="56" width="{cx1 - cx0 - 26}" height="140"/></clipPath>'
                f'<g clip-path="url(#cc)"><g class="scr">{"".join(gates)}</g></g>')
    circ.append(f'<rect x="{cx1 - 22}" y="{wy[2] - 10}" width="22" height="20" rx="3" fill="{P["amber"]}" '
                f'fill-opacity=".25" stroke="{P["amber"]}"/>'
                f'<path d="M{cx1 - 18} {wy[2] + 5} q7 -11 14 0" fill="none" stroke="{P["ink"]}" stroke-width="1.2"/>')
    circ.append(text((cx0 + cx1) / 2, 228, "syndrome extraction", P, 9.5, "muted", "m", anchor="middle"))
    out += circ
    css = (".pq{fill-opacity:.16;animation:pq 2.4s ease-in-out infinite}"
           "@keyframes pq{0%,100%{fill-opacity:.14}50%{fill-opacity:.38}}"
           ".err{opacity:0;animation:er 8s infinite}@keyframes er{0%,22%{opacity:0}25%,58%{opacity:1}63%,100%{opacity:0}}"
           ".syn{opacity:0;animation:sy 8s infinite}@keyframes sy{0%,30%{opacity:0}34%,58%{opacity:.85}64%,100%{opacity:0}}"
           ".fix{stroke-dasharray:1;stroke-dashoffset:1;opacity:0;animation:fx 8s infinite}"
           "@keyframes fx{0%,42%{stroke-dashoffset:1;opacity:0}43%{opacity:1;stroke-dashoffset:1}52%,60%{stroke-dashoffset:0;opacity:1}"
           "66%,100%{stroke-dashoffset:0;opacity:0}}"
           ".ok{opacity:0;animation:ok 8s infinite}@keyframes ok{0%,52%{opacity:0}55%,64%{opacity:1}70%,100%{opacity:0}}"
           ".scr{animation:sc 6s linear infinite}@keyframes sc{from{transform:translateX(0)}to{transform:translateX(-168px)}}")
    left = hero_text(
        P, "RESEARCH · QUANTUM COMPUTING", ["Error-corrected", "quantum circuits"],
        "Exploring fault-tolerant quantum computing: surface-code error correction, benchmark "
        "circuits in OpenQASM, and simulation of how logical qubits detect and fix physical errors.",
        ["Python", "OpenQASM", "QEC", "simulation"],
        "textbook illustration · an error, its syndrome and the decoder's fix", "violet", True)
    return doc(840, 300, P, "Error-corrected quantum circuits",
               "Animated rotated surface code: stabilizer checks pulse, an error appears on a data qubit, two "
               "checks light up as the syndrome and a decoder draws the correction, beside a scrolling "
               "syndrome-extraction circuit.", left + "".join(out), css)


# ---------------------------------------------------------------- voice2vision
def voice(P):
    out = []
    bx, by = 452, 70
    r = rng(11)
    for k in range(26):
        h = 10 + r() * 30
        out.append(f'<rect x="{bx + k * 6.2}" y="{f(by - h / 2)}" width="3.6" height="{f(h)}" rx="1.8" '
                   f'fill="{P["pink"]}" class="wb" style="animation-duration:{f(.5 + r() * .7)}s;'
                   f'animation-delay:-{f(r())}s"/>')
    out.append(f'<circle cx="{bx + 4}" cy="34" r="4" fill="{P["red"]}" class="rec"/>'
               + text(bx + 13, 38, "listening", P, 10, "muted", "m"))
    phrases = ["“a cabin in the snow”", "“… at night”", "“add a deer on the left”"]
    for i, p in enumerate(phrases):
        out.append(f'<g class="ph{i}">' + text(bx, 128 + i * 26, p, P, 13, "ink", "m") + "</g>")
    out.append(f'<path d="M618 160 h18 m-6 -6 l6 6 l-6 6" fill="none" stroke="{P["muted"]}" stroke-width="1.6"/>'
               + text(bx, 254, "speech → Whisper → LLM director → image model", P, 9.5, "muted", "m"))
    # picture frame
    fx, fy, fw, fh = 648, 40, 166, 166
    pic = [f'<clipPath id="pf"><rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="8"/></clipPath>']
    scene = [f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="#9ecbff"/>',
             f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="{P["night"]}" class="nt"/>',
             f'<polygon points="{fx},{fy + 110} {fx + 40},{fy + 62} {fx + 70},{fy + 95} {fx + 110},{fy + 50} '
             f'{fx + fw},{fy + 105} {fx + fw},{fy + fh} {fx},{fy + fh}" fill="#c9d6e3"/>',
             f'<polygon points="{fx + 30},{fy + 77} {fx + 40},{fy + 62} {fx + 50},{fy + 77}" fill="#ffffff"/>'
             f'<polygon points="{fx + 98},{fy + 67} {fx + 110},{fy + 50} {fx + 122},{fy + 66}" fill="#ffffff"/>',
             f'<path d="M{fx} {fy + 128} Q{fx + 80} {fy + 112} {fx + fw} {fy + 126} V{fy + fh} H{fx}z" fill="#f4f8fc"/>',
             f'<rect x="{fx + 84}" y="{fy + 98}" width="46" height="32" fill="#8b5a3c"/>'
             f'<polygon points="{fx + 78},{fy + 100} {fx + 107},{fy + 78} {fx + 136},{fy + 100}" fill="#5b3a29"/>'
             f'<path d="M{fx + 80} {fy + 99} L{fx + 107} {fy + 79} L{fx + 134} {fy + 99}" stroke="#fff" '
             f'stroke-width="3" fill="none"/>'
             f'<rect x="{fx + 120}" y="{fy + 80}" width="7" height="12" fill="#5b3a29"/>'
             f'<rect x="{fx + 92}" y="{fy + 106}" width="10" height="9" fill="#3b2a20"/>'
             f'<rect x="{fx + 92}" y="{fy + 106}" width="10" height="9" fill="#ffd166" class="lit"/>'
             f'<rect x="{fx + 110}" y="{fy + 110}" width="11" height="20" fill="#3b2a20"/>']
    stars = "".join(f'<circle cx="{f(fx + 8 + r() * 150)}" cy="{f(fy + 6 + r() * 50)}" r="{f(.6 + r())}" fill="#fff"/>'
                    for _ in range(16))
    night = (f'<g class="nt">{stars}<circle cx="{fx + 132}" cy="{fy + 26}" r="11" fill="#fdf3c4"/>'
             f'<circle cx="{fx + 137}" cy="{fy + 22}" r="10" fill="{P["night"]}"/></g>')
    deer = (f'<g class="dr" fill="#6b4a33"><ellipse cx="{fx + 38}" cy="{fy + 124}" rx="14" ry="7"/>'
            f'<rect x="{fx + 27}" y="{fy + 128}" width="2.5" height="13"/><rect x="{fx + 46}" y="{fy + 128}" width="2.5" height="13"/>'
            f'<rect x="{fx + 31}" y="{fy + 129}" width="2.5" height="12"/><rect x="{fx + 42}" y="{fy + 129}" width="2.5" height="12"/>'
            f'<path d="M{fx + 48} {fy + 121} l6 -12 l5 1 l-3 13z"/><ellipse cx="{fx + 57}" cy="{fy + 108}" rx="5" ry="3.5"/>'
            f'<path d="M{fx + 55} {fy + 105} l-2 -8 m2 8 l3 -9 m-3 3 l-4 -3 m5 1 l4 -3" stroke="#6b4a33" stroke-width="1.3" fill="none"/></g>')
    noise = []
    for i in range(12):
        for j in range(12):
            v = int(90 + r() * 140)
            noise.append(f'<rect x="{fx + i * 14}" y="{fy + j * 14}" width="14" height="14" '
                         f'fill="rgb({v},{int(v * .95)},{min(255, v + 25)})"/>')
    pic.append(f'<g clip-path="url(#pf)"><rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" fill="{P["faint"]}"/>'
               f'<g class="sc1">{"".join(scene)}{night}</g>{deer}<g class="nz">{"".join(noise)}</g></g>'
               f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="8" fill="none" stroke="{P["line"]}"/>')
    out += pic
    out.append(text(fx + fw / 2, 222, "refined phrase by phrase", P, 9.5, "muted", "m", anchor="middle"))
    T = "10s infinite"
    css = (".wb{transform-box:fill-box;transform-origin:center;animation:wb .8s ease-in-out infinite alternate}"
           "@keyframes wb{from{transform:scaleY(.25)}to{transform:scaleY(1)}}"
           ".rec{animation:rc 1.2s ease-in-out infinite}@keyframes rc{50%{opacity:.25}}"
           f".ph0{{animation:p0 {T}}}@keyframes p0{{0%,4%{{opacity:0}}9%,90%{{opacity:1}}96%,100%{{opacity:0}}}}"
           f".ph1{{animation:p1 {T}}}@keyframes p1{{0%,36%{{opacity:0}}41%,90%{{opacity:1}}96%,100%{{opacity:0}}}}"
           f".ph2{{animation:p2 {T}}}@keyframes p2{{0%,60%{{opacity:0}}65%,90%{{opacity:1}}96%,100%{{opacity:0}}}}"
           f".sc1{{animation:s1 {T}}}@keyframes s1{{0%,10%{{opacity:0}}28%,92%{{opacity:1}}98%,100%{{opacity:0}}}}"
           f".nz{{animation:nz {T}}}@keyframes nz{{0%,9%{{opacity:0}}12%{{opacity:1}}30%,100%{{opacity:0}}}}"
           f".nt{{animation:nt {T}}}@keyframes nt{{0%,42%{{opacity:0}}52%,100%{{opacity:1}}}}"
           f".lit{{animation:lt {T}}}@keyframes lt{{0%,46%{{opacity:0}}54%,100%{{opacity:1}}}}"
           f".dr{{animation:de {T}}}@keyframes de{{0%,66%{{opacity:0}}76%,92%{{opacity:1}}98%,100%{{opacity:0}}}}")
    left = hero_text(
        P, "AI TOOLS · SPEECH → IMAGE / UI", ["Voice to Vision"],
        "Say “a cabin in the snow … at night … add a deer on the left” and the picture updates "
        "while you are still talking. Code owns the scene; an LLM director only picks among the "
        "options the code offers. A sibling tool builds UI prototypes by voice.",
        ["Python", "Whisper", "SD-Turbo", "LLM tools"],
        "illustration of the live loop · undo is instant", "pink", True)
    return doc(840, 300, P, "Voice to Vision",
               "Animated illustration: a waveform listens, three spoken phrases appear, and a picture of a cabin in "
               "the snow resolves from noise, turns to night and gains a deer.", left + "".join(out), css)


# ---------------------------------------------------------------- Linear A (frame for the demo-video GIF)
VIDEO_BOX = (420, 25, 400, 250)  # where build_linear_a.py composites the recording


def linear_a(P):
    x, y, w, h = VIDEO_BOX
    left = hero_text(
        P, "AI · COMPUTER VISION · ANCIENT SCRIPTS", ["Linear A", "Tablet Reader"],
        "Upload a Minoan tablet drawing: a detector and classifier box the signs, propose readings "
        "and check the fractions against the KU-RO total. Linear A is undeciphered, so it reads "
        "signs and sums, not prose.",
        ["Python", "FastAPI", "YOLO", "Vue"],
        "real demo recording · Rikoleurt/ASE_Group3", "amber", False)
    frame = (f'<rect x="{x - 1}" y="{y - 1}" width="{w + 2}" height="{h + 2}" rx="10" fill="{P["bg"]}" '
             f'stroke="{P["line"]}"/>')
    return doc(840, 300, P, "Linear A Tablet Reader",
               "Demo recording of the Linear A Tablet Reader: a tablet drawing is uploaded, signs are boxed and "
               "read, and the fraction check compares the entries with the KU-RO total.", left + frame)


CARDS = {"banner": banner, "hero/drone": drone, "hero/outage-risk": outage_risk,
         "hero/quantum": quantum, "hero/voice2vision": voice}
