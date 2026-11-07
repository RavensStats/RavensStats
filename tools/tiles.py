"""The 410x200 project tiles. Game tiles keep this frame so a GIF clip can replace them later."""
import json
import math
from pathlib import Path

from common import ACCENTS, doc, f, hexagon, polyline, rng, text, tile_frame

DATA = Path(__file__).resolve().parent / "data"


def tile(P, name, title, sub, private, desc, body, css=""):
    return doc(410, 200, P, name, desc, tile_frame(P, title, sub, private, body), css)


# ---------------------------------------------------------------- MSc thesis (topic only)
def thesis(P):
    out = [text(18, 30, "long context", P, 9.5, "muted", "m")]
    lx, ly, lw, lh = 312, 44, 78, 64
    out.append(f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="10" fill="{P["violet"]}" fill-opacity=".14" '
               f'stroke="{P["violet"]}"/>' + text(lx + lw / 2, ly + 37, "LLM", P, 15, "violet", "m", weight="700",
                                                     anchor="middle"))
    out.append(f'<rect x="150" y="98" width="86" height="30" rx="7" fill="{P["faint"]}" stroke="{P["line"]}"/>'
               + text(193, 117, "recompute", P, 10, "muted", "m", anchor="middle")
               + text(222, 64, "reuse", P, 10, "green", "m", anchor="middle"))
    cached = {1, 2, 4, 5, 7, 8}
    dur = 6
    for i in range(10):
        x, y = 22 + i * 27, 46
        reuse = i in cached
        col = P["green"] if reuse else P["blue"]
        ex, ey = lx + 6, ly + 20 + (i % 5) * 6
        if reuse:
            path = f"M{x} {y} C{x + 60} {y - 22} {ex - 60} {ey - 20} {ex} {ey}"
            t0 = .10 + i * .025
            t1 = t0 + .14
        else:
            path = f"M{x} {y} C{x} 110 150 113 193 113 S{ex - 30} {ey + 30} {ex} {ey}"
            t0 = .14 + i * .03
            t1 = t0 + .40
        kt = f"0;{f(t0)};{f(t1)};1"
        out.append(f'<rect x="{x - 11}" y="{y - 7}" width="22" height="14" rx="3" fill="{col}" fill-opacity=".22" '
                   f'stroke="{col}" stroke-dasharray="2 2"/>')
        out.append(f'<g><rect x="-11" y="-7" width="22" height="14" rx="3" fill="{col}"/>'
                   f'<animateMotion dur="{dur}s" repeatCount="indefinite" path="{path}" keyPoints="0;0;1;1" '
                   f'keyTimes="{kt}" calcMode="linear"/>'
                   f'<animate attributeName="opacity" dur="{dur}s" repeatCount="indefinite" values="1;1;0;0" '
                   f'keyTimes="0;{f(t1)};{f(min(t1 + .04, .99))};1"/></g>')
    for k in range(5):
        out.append(f'<circle cx="{404 - 6}" cy="{60 + k * 9}" r="0" fill="{P["violet"]}">'
                   f'<animate attributeName="r" dur="{dur}s" repeatCount="indefinite" values="0;0;3;3;0" '
                   f'keyTimes="0;{f(.62 + k * .05)};{f(.64 + k * .05)};.94;1"/></circle>')
    return tile(P, "MSc thesis", "MSc thesis · long-context LLM inference",
                "Faster long-context LLM inference by reusing cached work", True,
                "Animation: context chunks flow into an LLM; cached chunks take a fast reuse lane, the rest are "
                "recomputed.", "".join(out))


# ---------------------------------------------------------------- The Final Platform
def final_platform(P):
    r = rng(3)
    plats = []
    y = 132
    k = 0
    while y > 16:
        w = 46 + r() * 50
        x = 110 + r() * (190 - w)
        plats.append((x, y, w))
        y -= 15 + r() * 5
        k += 1
    out = []
    dur = 8
    for i, (x, y, w) in enumerate(plats):
        top = i == len(plats) - 1
        col = P["amber"] if top else P["cyan"]
        # the Void's crest rises from y=150 to y=72 over 85 % of the cycle; platforms it reaches de-rez
        u = max(0.02, (150 - y) / 78 * 0.85)
        anim = ("" if top or y < 66 else
                f'<animate attributeName="opacity" dur="{dur}s" repeatCount="indefinite" values="1;1;0;0;1" '
                f'keyTimes="0;{f(u)};{f(min(u + .04, .95))};.97;1"/>')
        out.append(f'<g><rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="6" rx="2" fill="{col}"/>'
                   f'<rect x="{f(x + 3)}" y="{f(y + 6)}" width="{f(w - 6)}" height="3" rx="1" fill="{col}" '
                   f'fill-opacity=".4"/>{anim}</g>')
    tx, ty, tw = plats[-1]
    out.append(f'<rect x="{f(tx - 4)}" y="{f(ty - 4)}" width="{f(tw + 8)}" height="14" rx="5" fill="{P["amber"]}" '
               f'fill-opacity=".18" class="gl"/>')
    for p in range(4):
        hops = [plats[min(len(plats) - 1, j)] for j in range(p % 2, len(plats), 1)]
        pts = [(x + w * (.25 + .17 * p), y - 4) for x, y, w in hops]
        d = "M" + " ".join(f"{f(a)} {f(b)}" if n == 0 else
                           f"Q{f((pts[n - 1][0] + a) / 2)} {f(min(pts[n - 1][1], b) - 14)} {f(a)} {f(b)}"
                           for n, (a, b) in enumerate(pts))
        out.append(f'<rect x="-3.5" y="-7" width="7" height="7" rx="1.5" fill="{P[["pink", "green", "violet", "blue"][p]]}">'
                   f'<animateMotion dur="{dur}s" repeatCount="indefinite" path="{d}" begin="-{f(p * .3)}s"/></rect>')
    wave = polyline([(x, 6 * math.sin(x / 14)) for x in range(0, 456, 6)])
    out.append(f'<linearGradient id="vd" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P["violet"]}" '
               f'stop-opacity=".9"/><stop offset="1" stop-color="{P["violet"]}" stop-opacity=".25"/></linearGradient>'
               f'<g><path d="{wave} V200 H0z" fill="url(#vd)"><animateTransform attributeName="transform" '
               f'type="translate" values="-30 0;0 0" dur="1.6s" repeatCount="indefinite"/></path>'
               f'<animateTransform attributeName="transform" type="translate" dur="{dur}s" repeatCount="indefinite" '
               f'values="0 150;0 72;0 72;0 150" keyTimes="0;.85;.97;1"/></g>')
    out.append(text(316, 44, "the Final", P, 9.5, "amber", "m") + text(316, 56, "Platform", P, 9.5, "amber", "m")
               + text(316, 138, "the Void", P, 9.5, "card", "m", weight="700"))
    css = ".gl{animation:gl 1.4s ease-in-out infinite}@keyframes gl{50%{fill-opacity:.45}}"
    return tile(P, "The Final Platform", "The Final Platform",
                "PvPvE physics climber: build up, shove rivals, outrun the Void", True,
                "Animation: players hop up a procedurally generated stack of platforms while a violet Void rises "
                "and erases the platforms below.", "".join(out), css)


# ---------------------------------------------------------------- Battleblips
def battleblips(P):
    out = []
    layers = [(50, "ZENITH"), (88, "HORIZON"), (126, "NADIR")]
    for ly, name in layers:
        hexes = []
        for i in range(9):
            for j in range(3):
                cx = 112 + i * 26 + (j % 2) * 13
                cy = ly - 10 + j * 10
                hexes.append(f'<polygon points="{hexagon(cx, cy, 8.5, .42)}"/>')
        out.append(f'<g fill="{P["blue"]}" fill-opacity=".06" stroke="{P["blue"]}" stroke-opacity=".45">{"".join(hexes)}</g>'
                   + text(18, ly + 3, name, P, 9, "muted", "m", extra=' letter-spacing="1"'))
    sx, sy = 190, 88
    out.append(f'<ellipse cx="{sx}" cy="{sy}" rx="90" ry="38" fill="none" stroke="{P["cyan"]}" stroke-width="2" class="ping"/>'
               f'<ellipse cx="{sx}" cy="{sy}" rx="90" ry="38" fill="none" stroke="{P["cyan"]}" stroke-width="1.2" class="ping" '
               f'style="animation-delay:.6s"/>'
               f'<line x1="{sx}" y1="42" x2="{sx}" y2="134" stroke="{P["cyan"]}" stroke-opacity=".35" stroke-dasharray="2 3"/>'
               f'<polygon points="{sx - 8},{sy + 4} {sx + 10},{sy} {sx - 8},{sy - 4} {sx - 4},{sy}" fill="{P["blue"]}"/>')
    ex, ey = 268, 128
    out.append(f'<g class="hid"><polygon points="{ex + 8},{ey + 4} {ex - 10},{ey} {ex + 8},{ey - 4} {ex + 4},{ey}" '
               f'fill="{P["red"]}"/><rect x="{ex - 16}" y="{ey - 12}" width="32" height="20" rx="3" fill="none" '
               f'stroke="{P["red"]}" stroke-dasharray="3 2"/>' + text(ex + 20, ey - 6, "DETECTED", P, 8.5, "red", "m")
               + "</g>")
    dx, dy = 250, 46
    out.append(f'<g class="dec"><circle cx="{dx}" cy="{dy}" r="4" fill="{P["amber"]}"/>'
               + text(dx + 8, dy + 3, "decoy?", P, 8.5, "amber", "m") + "</g>")
    css = (".ping{transform-box:fill-box;transform-origin:center;animation:pg 3s ease-out infinite both}"
           "@keyframes pg{0%{transform:scale(.05);opacity:1}100%{transform:scale(1.25);opacity:0}}"
           ".hid{opacity:0;animation:hd 3s infinite}@keyframes hd{0%,52%{opacity:0}58%,80%{opacity:1}92%,100%{opacity:0}}"
           ".dec{animation:dc .7s steps(2) infinite}@keyframes dc{50%{opacity:.2}}")
    return tile(P, "Battleblips", "Battleblips",
                "Hex-layered space tactics built on hidden information", True,
                "Animation: three stacked hex layers; a sonar ping from the player's ship reveals a hidden enemy on "
                "the lower layer while a decoy flickers above.", "".join(out), css)


# ---------------------------------------------------------------- Doodle-Coaster
def doodle(P):
    pts = []
    for k in range(91):
        x = 18 + k * 4.2
        y = 92 - 34 * math.sin(k / 9.5) * math.exp(-k / 140) - 12 * math.sin(k / 3.9 + 1) * (k > 40)
        pts.append((x, y))
    d = polyline(pts)
    grid = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="146"/>' for x in range(0, 410, 16)) + \
        "".join(f'<line x1="0" y1="{y}" x2="410" y2="{y}"/>' for y in range(6, 146, 16))
    out = [f'<g stroke="{P["blue"]}" stroke-opacity=".08">{grid}</g>']
    struts = "".join(f'<line x1="{f(x)}" y1="{f(y + 3)}" x2="{f(x)}" y2="140"/>' for x, y in pts[::6])
    out.append(f'<g stroke="{P["muted"]}" stroke-opacity=".5" class="st">{struts}</g>')
    out.append(f'<path d="{d}" pathLength="1" class="tr" fill="none" stroke="{P["ink"]}" stroke-width="3" '
               f'stroke-linecap="round" stroke-linejoin="round"/>')
    dur = 8
    out.append(f'<g class="pen"><g transform="rotate(35)"><rect x="-2.5" y="-26" width="5" height="22" fill="{P["amber"]}"/>'
               f'<polygon points="-2.5,-4 2.5,-4 0,2" fill="{P["ink"]}"/></g>'
               f'<animateMotion dur="{dur}s" repeatCount="indefinite" path="{d}" keyPoints="0;1;1" keyTimes="0;.42;1" '
               f'calcMode="linear"/></g>')
    out.append(f'<g class="cart"><rect x="-11" y="-13" width="22" height="10" rx="3" fill="{P["red"]}"/>'
               f'<circle cx="-6" cy="-2" r="2.6" fill="{P["ink"]}"/><circle cx="6" cy="-2" r="2.6" fill="{P["ink"]}"/>'
               f'<circle cx="-3" cy="-16" r="3" fill="{P["amber"]}"/><circle cx="4" cy="-16" r="3" fill="{P["blue"]}"/>'
               f'<animateMotion dur="{dur}s" repeatCount="indefinite" path="{d}" rotate="auto" '
               f'keyPoints="0;0;1;1" keyTimes="0;.47;.9;1" calcMode="spline" keySplines="0 0 1 1;.4 0 .6 1;0 0 1 1"/></g>')
    css = (".tr{stroke-dasharray:1;stroke-dashoffset:1;animation:tr 8s linear infinite}"
           "@keyframes tr{0%{stroke-dashoffset:1;opacity:1}42%,92%{stroke-dashoffset:0;opacity:1}98%,100%{stroke-dashoffset:0;opacity:0}}"
           ".st{animation:st 8s infinite}@keyframes st{0%,40%{opacity:0}46%,92%{opacity:1}98%,100%{opacity:0}}"
           ".pen{animation:pn 8s infinite}@keyframes pn{0%,42%{opacity:1}45%,100%{opacity:0}}"
           ".cart{animation:ct 8s infinite}@keyframes ct{0%,45%{opacity:0}47%,92%{opacity:1}96%,100%{opacity:0}}")
    return tile(P, "Doodle-Coaster", "Doodle-Coaster",
                "Draw a roller coaster's side profile, then ride what you drew", True,
                "Animation: a pencil sketches a coaster track on graph paper, supports appear, then a cart rides it.",
                "".join(out), css)


# ---------------------------------------------------------------- Survivors-like
def survivors(P):
    cx, cy = 205, 74
    r = rng(5)
    out = [f'<circle cx="{cx}" cy="{cy}" r="34" fill="{P["amber"]}" fill-opacity=".08" stroke="{P["amber"]}" '
           f'stroke-opacity=".3" class="aura"/>']
    dur = 3
    for k in range(22):
        a = r() * 2 * math.pi
        sx, sy = cx + 230 * math.cos(a), cy + 110 * math.sin(a)
        ex, ey = cx + 30 * math.cos(a), cy + 30 * math.sin(a)
        b = f(-r() * dur)
        col = P[["red", "violet", "pink"][k % 3]]
        out.append(f'<circle r="{f(3.5 + r() * 2.5)}" fill="{col}">'  # mythic horde
                   f'<animateMotion dur="{dur}s" begin="{b}s" repeatCount="indefinite" path="M{f(sx)} {f(sy)} L{f(ex)} {f(ey)}"/>'
                   f'<animate attributeName="opacity" dur="{dur}s" begin="{b}s" repeatCount="indefinite" '
                   f'values="0;1;1;0" keyTimes="0;.15;.9;1"/></circle>'
                   f'<path d="M0 -4 L3 0 L0 4 L-3 0z" fill="{P["green"]}" transform="translate({f(ex)} {f(ey)})">'
                   f'<animate attributeName="opacity" dur="{dur}s" begin="{b}s" repeatCount="indefinite" '
                   f'values="0;0;1;0" keyTimes="0;.9;.93;1"/></path>')
    # forged blades orbiting the smith, plus a few rising embers
    orb = "".join(f'<path d="M0 -3 L12 0 L0 3z" fill="{P["amber"]}" '
                  f'transform="translate({f(cx + 24 * math.cos(k * 2.094))} {f(cy + 24 * math.sin(k * 2.094))}) '
                  f'rotate({f(math.degrees(k * 2.094) + 90)})"/>' for k in range(3))
    out.append(f'<g>{orb}<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" '
               f'to="360 {cx} {cy}" dur="1.1s" repeatCount="indefinite"/></g>')
    for k in range(6):
        ex = cx - 10 + k * 4
        out.append(f'<circle cx="{ex}" cy="{cy}" r="1.6" fill="{P["amber"]}" class="em" '
                   f'style="animation-delay:{f(k * .25)}s"/>')
    out.append(f'<path d="M{cx - 9} {cy + 2} h18 l-3 5 h-12z M{cx - 4} {cy + 7} h8 v4 h-8z" fill="{P["muted"]}"/>'
               f'<g transform="translate({cx} {cy - 4})"><g class="ham"><rect x="-1.2" y="-12" width="2.4" height="12" '
               f'fill="{P["muted"]}"/><rect x="-6" y="-16" width="12" height="6" rx="1" fill="{P["amber"]}"/></g></g>')
    css = (".aura{transform-box:fill-box;transform-origin:center;animation:au 1.5s ease-in-out infinite}"
           "@keyframes au{50%{transform:scale(1.15)}}"
           ".ham{transform-origin:0 0;animation:hm .55s ease-in infinite}@keyframes hm{0%{transform:rotate(-40deg)}"
           "70%{transform:rotate(25deg)}100%{transform:rotate(-40deg)}}"
           ".em{animation:em 1.5s ease-out infinite}@keyframes em{0%{opacity:0;transform:none}"
           "20%{opacity:1}100%{opacity:0;transform:translateY(-26px)}}")
    return tile(P, "Hephaestus Protocol", "Hephaestus Protocol",
                "Mythic bullet-heaven roguelike: forge weapons mid-battle", "steam",
                "Animation: a smith hammers at an anvil while forged blades orbit and mythic hordes converge and "
                "pop into XP gems.", "".join(out), css)


# ---------------------------------------------------------------- Candy Kings
def candy(P):
    out = []
    r = rng(9)

    def army(cx, cy, col, n):
        g = []
        for _ in range(n):
            a, d = r() * 6.283, 12 + r() * 22
            g.append(f'<circle cx="{f(cx + d * math.cos(a))}" cy="{f(cy + d * .7 * math.sin(a))}" r="5.5" fill="{col}"/>')
        return "".join(g)
    out.append(army(90, 82, P["violet"], 11) + army(320, 82, P["pink"], 11))
    out.append(f'<circle cx="90" cy="80" r="10" fill="{P["violet"]}" stroke="{P["card"]}" stroke-width="2"/>'
               f'<path d="M82 70 l3 -8 l5 5 l5 -5 l3 8z" fill="{P["amber"]}"/>'
               f'<circle cx="320" cy="80" r="10" fill="{P["pink"]}" stroke="{P["card"]}" stroke-width="2"/>'
               f'<path d="M320 70 l3 -14 l3 14z" fill="{P["amber"]}"/>')
    for i, (x, y) in enumerate([(192, 50), (215, 108), (230, 62), (180, 100)]):
        col = P["pink"] if i % 2 else P["violet"]
        out.append(f'<path d="M{x} {y - 6} l5 6 l-5 6 l-5 -6z" fill="{col}" class="gem" style="animation-delay:{i * .4}s"/>')
    tx, ty = 300, 98
    out.append(f'<circle cx="{tx}" cy="{ty}" r="6" fill="{P["pink"]}" class="fat"/>')
    for k in range(10):
        a = k * 0.628
        col = P[ACCENTS[k % 6]]
        out.append(f'<rect x="{tx - 2}" y="{ty - 2}" width="4" height="4" fill="{col}" class="cf" '
                   f'style="--dx:{f(26 * math.cos(a))}px;--dy:{f(22 * math.sin(a) - 8)}px"/>')
    out.append(f'<g><circle r="4.5" fill="{P["amber"]}"/><path d="M-4 0 l-5 -4 v8z M4 0 l5 -4 v8z" fill="{P["amber"]}"/>'
               f'<animateMotion dur="3s" repeatCount="indefinite" path="M100 74 Q200 -10 {tx} {ty}" '
               f'keyPoints="0;1;1" keyTimes="0;.4;1" calcMode="linear" rotate="auto"/>'
               f'<animate attributeName="opacity" dur="3s" repeatCount="indefinite" values="1;1;0;0;1" '
               f'keyTimes="0;.4;.41;.98;1"/></g>')
    css = (".gem{transform-box:fill-box;transform-origin:center;animation:gm 1.6s ease-in-out infinite}"
           "@keyframes gm{50%{transform:scale(1.3)}}"
           ".fat{transform-box:fill-box;transform-origin:center;animation:ft 3s infinite}"
           "@keyframes ft{0%,40%{transform:scale(1);opacity:1}54%{transform:scale(1.8);opacity:1}56%{transform:scale(2.1);opacity:0}"
           "88%{transform:scale(.2);opacity:0}100%{transform:scale(1);opacity:1}}"
           ".cf{opacity:0;animation:cf 3s ease-out infinite}"
           "@keyframes cf{0%,54%{opacity:0;transform:translate(0,0)}56%{opacity:1}85%{opacity:0;transform:translate(var(--dx),var(--dy)) rotate(180deg)}100%{opacity:0}}")
    return tile(P, "Candy Kings", "Candy Kings",
                "Couch co-op game: feed the other army sweets until they pop", True,
                "Animation: a purple candy army and a pink unicorn army face off; a thrown sweet inflates an enemy "
                "until it pops into confetti.", "".join(out), css)


# ---------------------------------------------------------------- ROSViz Web
def rosviz(P):
    out = [f'<rect x="12" y="12" width="214" height="124" rx="8" fill="{P["bg"]}" stroke="{P["line"]}"/>']
    grid = "".join(f'<line x1="{x}" y1="12" x2="{x}" y2="136"/>' for x in range(30, 226, 18)) + \
        "".join(f'<line x1="12" y1="{y}" x2="226" y2="{y}"/>' for y in range(30, 136, 18))
    out.append(f'<g stroke="{P["faint"]}">{grid}</g>')
    # 10 s story: the robot drives at a wall, the monitor warns, goes critical and auto-stops it,
    # then the alert clears and it re-plans around the obstacle.
    out.append(f'<rect x="152" y="82" width="9" height="54" fill="{P["muted"]}" fill-opacity=".6"/>'
               f'<rect x="80" y="56" width="9" height="34" fill="{P["muted"]}" fill-opacity=".6"/>'
               f'<rect x="184" y="30" width="30" height="9" fill="{P["muted"]}" fill-opacity=".6"/>')
    route = "M30 110 L136 110 L136 40 L40 40 L30 110"
    stop = 106 / (106 + 70 + 96 + math.hypot(10, 70))  # fraction of the route where it halts
    out.append(f'<path d="{route}" fill="none" stroke="{P["green"]}" stroke-opacity=".35" stroke-dasharray="3 3"/>')
    rays = "".join(f'<line x1="0" y1="0" x2="{f(30 * math.cos(math.radians(a)))}" y2="{f(30 * math.sin(math.radians(a)))}"/>'
                   for a in range(-50, 51, 10))
    kp, kt = f"0;{f(stop)};{f(stop)};1", ".0;.32;.58;1"
    out.append(f'<g><g stroke="{P["cyan"]}" stroke-opacity=".5" class="ray">{rays}<animateTransform attributeName="transform" '
               f'type="rotate" values="-20;20;-20" dur="1.2s" repeatCount="indefinite"/></g>'
               f'<circle r="11" fill="none" stroke="{P["red"]}" stroke-width="2.5" class="halt"/>'
               f'<circle r="7" fill="{P["blue"]}"/><path d="M2 -3 L7 0 L2 3z" fill="{P["card"]}"/>'
               f'<animateMotion dur="10s" repeatCount="indefinite" path="{route}" rotate="auto" keyPoints="{kp}" '
               f'keyTimes="{kt}" calcMode="linear"/></g>')
    out.append(text(18, 130, "/scan  /odom  /imu", P, 8.5, "muted", "m"))
    px = 236
    out.append(text(px, 46, "safety monitor", P, 9, "muted", "m", weight="600"))
    rows = [("w", "amber", "WARN  collision_fwd"), ("c", "red", "CRIT  collision_fwd"),
            ("s", "red", "AUTO-STOP  /cmd_vel = 0"), ("k", "green", "OK    alert cleared")]
    for i, (cls, col, lab) in enumerate(rows):
        y = 52 + i * 20
        out.append(f'<g class="r{cls}"><rect x="{px}" y="{y}" width="162" height="16" rx="4" fill="{P[col]}" '
                   f'fill-opacity=".14" stroke="{P[col]}" stroke-opacity=".7"/>'
                   + text(px + 7, y + 11.5, lab, P, 9, col, "m") + "</g>")
    out.append(text(px, 140, "→ dashboard · Prometheus · Grafana", P, 8.5, "muted", "m"))
    T = "10s infinite"
    css = (f".rw{{animation:rw {T}}}@keyframes rw{{0%,22%{{opacity:0}}25%,92%{{opacity:1}}97%,100%{{opacity:0}}}}"
           f".rc{{animation:rc {T}}}@keyframes rc{{0%,29%{{opacity:0}}31%,92%{{opacity:1}}97%,100%{{opacity:0}}}}"
           f".rs{{animation:rs {T}}}@keyframes rs{{0%,32%{{opacity:0}}34%,92%{{opacity:1}}97%,100%{{opacity:0}}}}"
           f".rk{{animation:rk {T}}}@keyframes rk{{0%,56%{{opacity:0}}59%,92%{{opacity:1}}97%,100%{{opacity:0}}}}"
           f".halt{{opacity:0;animation:ht {T}}}@keyframes ht{{0%,31%{{opacity:0}}33%,56%{{opacity:1}}59%,100%{{opacity:0}}}}")
    return tile(P, "ROSViz Web", "ROSViz Web",
                "Automated ROS 2 safety monitor + live dashboard integration", False,
                "Animation: a robot drives at a wall; the safety monitor warns, goes critical and auto-stops it, then "
                "clears the alert as it re-plans, with alerts streamed to the dashboard and Grafana.", "".join(out), css)


# ---------------------------------------------------------------- fantasy league pages
def fantasy(P):
    teams = ["Gridiron Gang", "Blitz Brigade", "End Zone Elite", "Fourth & Long", "Hail Marys"]
    ranks = [[0, 1, 2, 3, 4], [1, 0, 3, 2, 4], [1, 3, 0, 4, 2], [0, 1, 2, 3, 4]]  # per week, team -> row
    scores = [[118, 112, 104, 97, 90], [121, 126, 99, 108, 94], [116, 131, 102, 92, 123], [118, 112, 104, 97, 90]]
    out = []
    for w, lab in enumerate(["WEEK 7", "WEEK 8", "WEEK 9"]):
        out.append(f'<g class="wk" style="animation-delay:{w * 3}s">' + text(282, 26, lab, P, 10, "muted", "m", anchor="end")
                   + "</g>")
    out.append(text(18, 26, "STANDINGS", P, 10, "muted", "m", weight="600", extra=' letter-spacing="1.2"'))
    for row in range(5):
        out.append(text(22, 50 + row * 20, str(row + 1), P, 11, "muted", "m"))
    kt = "0;.30;.33;.63;.66;.96;1"
    for t, name in enumerate(teams):
        ys = [36 + ranks[w][t] * 20 for w in range(4)]
        yv = f"0 {ys[0]};0 {ys[0]};0 {ys[1]};0 {ys[1]};0 {ys[2]};0 {ys[2]};0 {ys[3]}"
        ws = [scores[w][t] * 1.6 for w in range(4)]
        wv = f"{f(ws[0])};{f(ws[0])};{f(ws[1])};{f(ws[1])};{f(ws[2])};{f(ws[2])};{f(ws[3])}"
        col = P[ACCENTS[t]]
        out.append(f'<g><animateTransform attributeName="transform" type="translate" values="{yv}" keyTimes="{kt}" '
                   f'dur="9s" repeatCount="indefinite" calcMode="spline" '
                   f'keySplines="0 0 1 1;.5 0 .5 1;0 0 1 1;.5 0 .5 1;0 0 1 1;.5 0 .5 1"/>'
                   f'<circle cx="46" cy="9" r="6" fill="{col}"/>' + text(58, 13, name, P, 11, "ink")
                   + f'<rect x="160" y="3" width="10" height="12" rx="3" fill="{col}" fill-opacity=".55">'
                   f'<animate attributeName="width" values="{wv}" keyTimes="{kt}" dur="9s" repeatCount="indefinite"/></rect></g>')
    css = ".wk{opacity:0;animation:wk 9s infinite}@keyframes wk{0%{opacity:0}3%,30%{opacity:1}34%,100%{opacity:0}}"
    return tile(P, "Fantasy league pages", "Fantasy league pages",
                "Sleeper league sites + scripts for 112/224-team leagues", False,
                "Animation: a league standings table re-sorts week by week as scoring bars grow and shrink.",
                "".join(out), css)


# ---------------------------------------------------------------- Proth Prime Search (real sieve data)
def proth(P):
    """First 240 odd k of k*2^332200000+1; each dot fades in the wave of its real smallest factor."""
    cells = json.loads((DATA / "proth_sieve_small_k.json").read_text())["cells"]
    waves = [("q = 3", lambda q: q == 3), ("q = 5", lambda q: q == 5), ("q = 7", lambda q: q == 7),
             ("q = 11", lambda q: q == 11), ("q = 13", lambda q: q == 13), ("q ≤ 97", lambda q: 17 <= q <= 97),
             ("q ≤ 10⁶", lambda q: 101 <= q <= 10 ** 6), ("q ≤ 8·10¹²", lambda q: q == -1)]
    T, dur = [.06 + i * .075 for i in range(len(waves))], 12
    dots = []
    for i, (k, q) in enumerate(cells):
        x, y = 18 + (i % 24) * 10.5, 32 + (i // 24) * 10.5
        cls = "sv" if q == 0 else f"w{next(j for j, (_, hit) in enumerate(waves) if hit(q))}"
        dots.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="3.4" class="{cls}"/>')
    out = [text(18, 20, "k = 1, 3, 5 … 479", P, 9, "muted", "m"),
           f'<g fill="{P["blue"]}">{"".join(dots)}</g>',
           text(290, 50, "N = k·2ⁿ + 1", P, 10.5, "ink", "m", weight="600"),
           text(290, 63, "n = 332,200,000", P, 9, "muted", "m")]
    for i, (lab, _) in enumerate(waves):
        out.append(f'<g class="l{i}">' + text(290, 84, "sieve " + lab, P, 10, "red", "m", weight="600") + "</g>")
    out.append('<g class="ls">' + text(290, 84, "10 survive: prime?", P, 10, "amber", "m", weight="600") + "</g>")
    out.append(text(290, 102, "all odd k < 10⁹:", P, 9, "muted", "m")
               + text(290, 114, "500M → 15.3M left", P, 9, "ink", "m")
               + text(290, 126, "P(prime) ≈ 3·10⁻⁷", P, 9, "muted", "m")
               + text(290, 138, "≈ 4.3 primes in pool", P, 9, "muted", "m"))
    pc = lambda x: f(x * 100)
    css = [f".w{i}{{animation:w{i} {dur}s infinite}}@keyframes w{i}{{0%,{pc(t)}%{{fill-opacity:1}}"
           f"{pc(t + .03)}%,95%{{fill-opacity:.1}}100%{{fill-opacity:1}}}}" for i, t in enumerate(T)]
    css += [f".l{i}{{fill-opacity:0;animation:l{i} {dur}s infinite}}@keyframes l{i}{{0%,{pc(t - .03)}%{{fill-opacity:0}}"
            f"{pc(t - .02)}%,{pc(t + .045)}%{{fill-opacity:1}}{pc(t + .055)}%,100%{{fill-opacity:0}}}}" for i, t in enumerate(T)]
    css.append(f".ls{{fill-opacity:0;animation:ls {dur}s infinite}}@keyframes ls{{0%,64%{{fill-opacity:0}}"
               f"66%,93%{{fill-opacity:1}}95%,100%{{fill-opacity:0}}}}"
               f".sv{{transform-box:fill-box;transform-origin:center;animation:sv {dur}s infinite}}"
               f"@keyframes sv{{0%,64%{{fill:{P['blue']};transform:scale(1)}}68%{{fill:{P['amber']};transform:scale(1.6)}}"
               f"74%,80%,86%{{fill:{P['amber']};transform:scale(1.2)}}77%,83%,89%{{fill:{P['amber']};transform:scale(1.6)}}"
               f"93%{{fill:{P['amber']};transform:scale(1.2)}}97%,100%{{fill:{P['blue']};transform:scale(1)}}}}")
    return tile(P, "Proth Prime Search", "Proth Prime Search",
                "Sieving 500M candidates for a 100-million-digit prime", True,
                "Animation: the first 240 odd k of k·2^332,200,000 + 1 on a grid. Waves of primes q = 3, 5, 7, … "
                "knock out every k with that factor, using the project's real sieve data, until only the 10 true "
                "survivors remain, glowing because their primality is still unknown.", "".join(out), "".join(css))


CARDS = {"tiles/thesis": thesis, "tiles/final-platform": final_platform, "tiles/battleblips": battleblips,
         "tiles/doodle-coaster": doodle, "tiles/hephaestus-protocol": survivors, "tiles/candy-kings": candy,
         "tiles/rosviz": rosviz, "tiles/fantasy": fantasy, "tiles/proth-prime-search": proth}
