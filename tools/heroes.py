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


# ---------------------------------------------------------------- Navier-Stokes (public figure data)
def navier(P):
    curves = json.load(open(DATA / "ns_curves.json"))
    x0, x1, y0, y1 = 588.0, 812.0, 34.0, 226.0
    X = lambda v: x0 + v / 36 * (x1 - x0)
    Y = lambda v: y1 - (v + 2.2) / 4.6 * (y1 - y0)
    cols = ["blue", "pink", "green", "violet"]
    out = [f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{y1 - y0}" fill="{P["bg"]}" stroke="{P["line"]}"/>']
    for v in (-2, -1, 1, 2):
        out.append(f'<line x1="{x0}" x2="{x1}" y1="{f(Y(v))}" y2="{f(Y(v))}" stroke="{P["faint"]}"/>'
                   + text(x0 - 5, Y(v) + 3, str(v), P, 9, "muted", "m", anchor="end"))
    out.append(f'<line x1="{x0}" x2="{x1}" y1="{f(Y(0))}" y2="{f(Y(0))}" stroke="{P["muted"]}" '
               f'stroke-dasharray="3 3"/>' + text(x0 - 5, Y(0) + 3, "0", P, 9, "muted", "m", anchor="end"))
    for v in (0, 10, 20, 30):
        out.append(text(X(v), y1 + 13, str(v), P, 9, "muted", "m", anchor="middle"))
    out.append(text((x0 + x1) / 2, y1 + 27, "fraction of the remaining time (%)", P, 9.5, "muted", "m",
                    anchor="middle"))
    out.append(f'<text x="0" y="0" class="m" font-size="9.5" fill="{P["muted"]}" text-anchor="middle" '
               f'transform="translate({f(x0 - 24)} {f((y0 + y1) / 2)}) rotate(-90)">amplitude rate σ(T−t)</text>')
    for i, c in enumerate(curves):
        pts = [(X(a), Y(b)) for a, b in c["pts"]]
        out.append(f'<path d="{polyline(pts)}" pathLength="1" class="cv" style="animation-delay:{f(i * .35)}s" '
                   f'fill="none" stroke="{P[cols[i]]}" stroke-width="2.2" stroke-linecap="round"/>')
    lx = x0 - 30
    for i, c in enumerate(curves):
        xx = lx + (i % 2) * 130
        yy = 274 + (i // 2) * 14
        out.append(f'<line x1="{f(xx)}" x2="{f(xx + 14)}" y1="{f(yy - 3)}" y2="{f(yy - 3)}" '
                   f'stroke="{P[cols[i]]}" stroke-width="2.2"/>'
                   + text(xx + 19, yy, c["label"].replace("nu", "ν"), P, 9.5, "muted", "m"))
    # schematic collapsing swirl
    sx, sy = 486, 132
    rings = []
    for k in range(7):
        col = P[["blue", "cyan", "violet", "pink", "amber", "red", "pink"][k]]
        rings.append(f'<ellipse cx="{sx}" cy="{sy}" rx="44" ry="74" fill="none" stroke="{col}" '
                     f'stroke-width="2" class="rg" style="animation-delay:{f(k * 0.5)}s"/>')
    out.append("".join(rings) + f'<circle cx="{sx}" cy="{sy}" r="4" fill="{P["red"]}" class="core"/>'
               + text(sx, 228, "collapsing front", P, 9.5, "muted", "m", anchor="middle")
               + text(sx, 241, "(schematic)", P, 9.5, "muted", "m", anchor="middle"))
    css = (".cv{stroke-dasharray:1;stroke-dashoffset:1;animation:dr 9s ease-in-out infinite both}"
           "@keyframes dr{0%{stroke-dashoffset:1;opacity:1}38%{stroke-dashoffset:0}88%{stroke-dashoffset:0;opacity:1}"
           "96%,100%{stroke-dashoffset:0;opacity:0}}"
           ".rg{transform-box:fill-box;transform-origin:center;animation:rg 3.5s cubic-bezier(.5,0,.9,.6) infinite both}"
           "@keyframes rg{0%{transform:scale(1);opacity:0}15%{opacity:.9}100%{transform:scale(.04);opacity:.2}}"
           ".core{transform-box:fill-box;transform-origin:center;animation:co 1.75s ease-in-out infinite}"
           "@keyframes co{0%,100%{transform:scale(.7)}50%{transform:scale(1.5)}}")
    left = hero_text(
        P, "RESEARCH · FLUID DYNAMICS · PAPER", ["Navier–Stokes collapse"],
        "A certified unstable eigenvalue of a columnar model of the front of Hou's "
        "Navier–Stokes collapse (computer-assisted proof, interval arithmetic), and measured "
        "non-axisymmetric growth on the collapsing state. Companion work: self-similar blowup profiles.",
        ["Python", "NumPy/SciPy", "interval arithmetic"],
        "random-seed curves from the paper's public figure data (figdata/)", "blue", False)
    return doc(840, 300, P, "Navier–Stokes collapse",
               "Animated chart of measured non-axisymmetric growth rates on Hou's collapsing Navier–Stokes state, "
               "for two viscosities and azimuthal modes m = 0, 1, 2, drawn from the paper's figure data, beside a "
               "schematic collapsing swirl.", left + "".join(out), css)


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


CARDS = {"banner": banner, "hero/drone": drone, "hero/navier-stokes": navier,
         "hero/quantum": quantum, "hero/voice2vision": voice}
