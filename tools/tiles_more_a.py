"""Four more 410x200 project tiles: Escape Room, Classic Games, HeroClix Manual, Pokemon Red RL.

Original abstract gameplay drawings only (no sprites, art or logos from the games). Every
animation is CSS keyframes, so the shared reduced-motion rule stops it; fades use
fill-opacity / stroke-opacity.
"""
import math
import re

from common import f, rng, text
from tiles import tile


# ---------------------------------------------------------------- small CSS helpers
def _pc(t):
    return f(t * 100) + "%"


def _kf(name, dur, stops, base="", timing="linear"):
    """stops: [(t in 0..1, 'css decls')] -> a looping keyframe class."""
    body = "".join(f"{_pc(t)}{{{css}}}" for t, css in stops)
    return f".{name}{{{base}animation:{name} {dur}s {timing} infinite}}@keyframes {name}{{{body}}}"


def _fade(name, dur, pts, base=0):
    stops = [(t, f"fill-opacity:{f(v)};stroke-opacity:{f(v)}") for t, v in pts]
    return _kf(name, dur, stops, f"fill-opacity:{f(base)};stroke-opacity:{f(base)};")


def _show(name, dur, a, b, base=0, ramp=.012):
    """Visible on [a, b] of the cycle (0 < a < b < 1)."""
    return _fade(name, dur, [(0, 0), (a, 0), (a + ramp, 1), (b, 1), (min(b + ramp, .999), 0), (1, 0)], base)


def _kt(t):
    return f"{t:.4f}".rstrip("0").rstrip(".") or "0"


def _move(dur, pts, ease=True, kind="translate"):
    """SMIL motion (headless renders and every browser advance it): pts = [(t, a, b)] for translate,
    [(t, angle, (cx, cy))] for rotate."""
    if kind == "rotate":
        vals = ";".join(f"{f(a)} {c[0]} {c[1]}" for _, a, c in pts)
    else:
        vals = ";".join(f"{f(x)} {f(y)}" for _, x, y in pts)
    kt = ";".join(_kt(t) for t, *_ in pts)
    sp = (f' calcMode="spline" keySplines="{";".join([".42 0 .58 1"] * (len(pts) - 1))}"' if ease else "")
    return (f'<animateTransform attributeName="transform" type="{kind}" dur="{dur}s" repeatCount="indefinite" '
            f'values="{vals}" keyTimes="{kt}"{sp}/>')


def _attr(dur, attr, pts):
    """SMIL animation of a geometry attribute: pts = [(t, value)]."""
    return (f'<animate attributeName="{attr}" dur="{dur}s" repeatCount="indefinite" '
            f'values="{";".join(f(v) for _, v in pts)}" keyTimes="{";".join(_kt(t) for t, _ in pts)}"/>')


def _inject(body, smil):
    """Put each SMIL element just inside the first element with that class."""
    for name, anim in smil.items():
        m = re.search(rf'<(\w+) [^>]*class="{name}"[^>]*>', body)
        body = body[:m.end()] + anim + body[m.end():]
    return body


# ---------------------------------------------------------------- Escape Room (2D point-and-click)
def escape_room(P):
    D = 12
    css, smil = [], {}
    out = [f'<rect x="14" y="14" width="272" height="122" rx="8" fill="{P["bg"]}" stroke="{P["line"]}"/>',
           f'<rect x="15" y="114" width="270" height="21" fill="{P["faint"]}"/>',
           f'<line x1="15" y1="114" x2="285" y2="114" stroke="{P["line"]}"/>',
           text(22, 28, "bedroom", P, 8.5, "muted", "m")]
    # wall note (the first clue)
    out.append(f'<rect x="44" y="36" width="22" height="27" rx="2" fill="{P["card"]}" stroke="{P["amber"]}"/>'
               + "".join(f'<line x1="48" y1="{y}" x2="{62 if y < 54 else 56}" y2="{y}" stroke="{P["muted"]}"/>'
                         for y in (43, 48, 53, 58)))
    # bed
    out.append(f'<rect x="24" y="72" width="8" height="40" rx="2" fill="{P["violet"]}"/>'
               f'<rect x="32" y="88" width="84" height="16" rx="3" fill="{P["violet"]}" fill-opacity=".55"/>'
               f'<rect x="36" y="82" width="22" height="8" rx="3" fill="{P["card"]}" stroke="{P["line"]}"/>'
               f'<rect x="34" y="104" width="4" height="10" fill="{P["violet"]}"/>'
               f'<rect x="110" y="104" width="4" height="10" fill="{P["violet"]}"/>')
    # light-switch slider puzzle: four sliders, solved at 4-2-3-1 (as in the repo's SliderSnapMonitor)
    px, py = 128, 34
    out.append(f'<rect x="{px}" y="{py}" width="48" height="44" rx="4" fill="{P["card"]}" stroke="{P["line"]}"/>')
    out.append(f'<circle cx="{px + 24}" cy="{py + 7}" r="3" fill="{P["faint"]}" stroke="{P["line"]}"/>'
               f'<circle cx="{px + 24}" cy="{py + 7}" r="3" fill="{P["amber"]}" class="lamp"/>'
               f'<circle cx="{px + 24}" cy="{py + 7}" r="9" fill="{P["amber"]}" class="lampg"/>')
    css.append(_fade("lamp", D, [(0, 0), (.37, 0), (.38, 1), (.95, 1), (.97, 0), (1, 0)]))
    css.append(_fade("lampg", D, [(0, 0), (.37, 0), (.38, .3), (.95, .3), (.97, 0), (1, 0)]))
    start, goal = (1, 4, 1, 3), (4, 2, 3, 1)
    knob_y = lambda k: py + 38 - (k - 1) * 7.5
    slider_t = (.21, .25, .29, .33)
    for i in range(4):
        x = px + 9 + i * 10
        out.append(f'<line x1="{x}" y1="{py + 15}" x2="{x}" y2="{py + 39}" stroke="{P["line"]}" stroke-width="2"/>')
        out.append(f'<g class="kn{i}"><rect x="{x - 3.5}" y="-2" width="7" height="4" rx="1" fill="{P["blue"]}"/></g>')
        y0, y1, t = knob_y(start[i]), knob_y(goal[i]), slider_t[i]
        smil[f"kn{i}"] = _move(D, [(0, 0, y0), (t, 0, y0), (t + .02, 0, y1), (.95, 0, y1), (.98, 0, y0), (1, 0, y0)])
    # drawers (top one opens to show the first key part)
    dx, dy = 192, 80
    out.append(f'<rect x="{dx}" y="{dy}" width="48" height="34" rx="2" fill="{P["amber"]}" fill-opacity=".35" '
               f'stroke="{P["amber"]}"/><line x1="{dx}" y1="{dy + 17}" x2="{dx + 48}" y2="{dy + 17}" stroke="{P["amber"]}"/>'
               f'<rect x="{dx + 20}" y="{dy + 24}" width="8" height="2.5" rx="1" fill="{P["amber"]}"/>')
    out.append(f'<g class="dro"><rect x="{dx - 3}" y="{dy - 2}" width="54" height="20" rx="2" fill="{P["night"]}" '
               f'stroke="{P["amber"]}"/></g>')
    out.append(f'<g class="drc"><rect x="{dx + 20}" y="{dy + 7}" width="8" height="2.5" rx="1" fill="{P["amber"]}"/></g>')
    css.append(_fade("dro", D, [(0, 0), (.44, 0), (.45, 1), (.95, 1), (.97, 0), (1, 0)]))
    css.append(_fade("drc", D, [(0, 1), (.44, 1), (.45, 0), (.95, 0), (.97, 1), (1, 1)], base=1))
    # door with a lock
    out.append(f'<rect x="250" y="38" width="30" height="76" fill="{P["amber"]}" fill-opacity=".9" class="exit"/>'
               f'<rect x="250" y="38" width="30" height="76" fill="none" stroke="{P["muted"]}" stroke-width="2"/>'
               f'<rect x="251" y="39" width="28" height="74" fill="{P["cyan"]}" fill-opacity=".55" stroke="{P["cyan"]}">'
               + _attr(D, "width", [(0, 28), (.78, 28), (.83, 5), (.95, 5), (.98, 28), (1, 28)]) + '</rect>'
               f'<g class="door" fill="none" stroke="{P["cyan"]}"><rect x="255" y="45" width="20" height="26" rx="2"/>'
               f'<rect x="255" y="78" width="20" height="28" rx="2"/></g>'
               f'<g class="lk"><rect x="270" y="74" width="7" height="6" rx="1" fill="{P["red"]}"/>'
               f'<path d="M271.5 74 v-2.5 a2 2 0 0 1 4 0 v2.5" fill="none" stroke="{P["red"]}" stroke-width="1.4"/></g>')
    css.append(_fade("exit", D, [(0, 0), (.78, 0), (.82, .9), (.95, .9), (.97, 0), (1, 0)]))
    css.append(_fade("door", D, [(0, 1), (.78, 1), (.8, 0), (.95, 0), (.98, 1), (1, 1)], base=1))
    css.append(_fade("lk", D, [(0, 1), (.77, 1), (.79, 0), (.95, 0), (.97, 1), (1, 1)], base=1))
    out.append(f'<g class="esc">' + text(212, 30, "ESCAPED!", P, 11, "green", "m", weight="700", anchor="middle")
               + "</g>")
    css.append(_show("esc", D, .83, .95))

    # inventory (right panel)
    out.append(text(300, 48, "inventory", P, 9, "muted", "m", weight="600"))
    slots = [(300, 54), (332, 54), (364, 54)]
    for sx, sy in slots:
        out.append(f'<rect x="{sx}" y="{sy}" width="26" height="26" rx="4" fill="{P["faint"]}" stroke="{P["line"]}"/>')

    def key_part(half):
        bow = (f'<circle cx="-5" cy="0" r="3.5" fill="none" stroke="{P["amber"]}" stroke-width="2"/>'
               f'<rect x="-1.5" y="-1" width="4" height="2" fill="{P["amber"]}"/>')
        bit = (f'<rect x="-1" y="-1" width="7" height="2" fill="{P["amber"]}"/>'
               f'<rect x="3" y="1" width="1.8" height="3" fill="{P["amber"]}"/><rect x="5.5" y="1" width="1.8" height="3" '
               f'fill="{P["amber"]}"/>')
        return bow if half == 0 else bit

    # key part 1: appears in the open drawer, flies to slot 1; part 2: under the bed, flies to slot 2
    s1, s2 = (313, 67), (345, 67)
    out.append(f'<g class="kp1m"><g class="kp1">{key_part(0)}</g></g>'
               f'<g class="kp2m"><g class="kp2">{key_part(1)}</g></g>')
    css.append(_show("kp1", D, .45, .70))
    smil["kp1m"] = _move(D, [(0, 216, 89), (.48, 216, 89), (.52, *s1), (.66, *s1), (.70, s1[0] + 3, s1[1]), (1, 216, 89)])
    css.append(_show("kp2", D, .57, .70))
    smil["kp2m"] = _move(D, [(0, 72, 109), (.60, 72, 109), (.64, *s2), (.66, *s2), (.70, s1[0] + 2, s1[1]), (1, 72, 109)])
    out.append(f'<g class="key"><g transform="translate({s1[0] - 1} {s1[1]})">{key_part(0)}'
               f'<g transform="translate(3 0)">{key_part(1)}</g></g></g>')
    css.append(_show("key", D, .70, .79))
    out.append(f'<g class="keyd"><circle cx="{s1[0]}" cy="{s1[1]}" r="11" fill="none" stroke="{P["green"]}" '
               f'stroke-width="1.5"/></g>')
    css.append(_show("keyd", D, .70, .76))

    # status line
    steps = [(.08, .19, "clue found", "amber"), (.20, .36, "slider puzzle", "blue"), (.37, .44, "lights on", "amber"),
             (.45, .56, "key part 1/2", "amber"), (.57, .69, "key part 2/2", "amber"),
             (.70, .77, "combined: key", "green"), (.78, .95, "door unlocked", "green")]
    for i, (a, b, lab, col) in enumerate(steps):
        out.append(f'<g class="st{i}">' + text(300, 102, "›", P, 10, col, "m", weight="700")
                   + text(310, 102, lab, P, 9.5, col, "m", weight="600") + "</g>")
        css.append(_show(f"st{i}", D, a, b))
    out.append(text(300, 120, "point, click,", P, 8.5, "muted", "m") + text(300, 132, "combine, escape", P, 8.5, "muted", "m"))

    # message box from the clue
    out.append(f'<g class="msg"><rect x="80" y="118" width="120" height="15" rx="4" fill="{P["card"]}" '
               f'stroke="{P["amber"]}"/>' + text(140, 128.5, "you found a note", P, 8, "ink", "m", anchor="middle")
               + "</g>")
    css.append(_show("msg", D, .09, .19))

    # cursor + click ripples
    way = [(0, 205, 128), (.06, 56, 50), (.16, 56, 50)]
    for i in range(4):  # grab each knob at its start notch, drag it to the solution notch
        x = px + 9 + i * 10
        way += [(slider_t[i] - .01, x, knob_y(start[i])), (slider_t[i] + .02, x, knob_y(goal[i]))]
    way += [(.42, 216, 88), (.47, 218, 90), (.55, 72, 108), (.59, 74, 110), (.74, 266, 78), (.80, 268, 80),
            (.92, 236, 128), (1, 205, 128)]
    out.append(f'<g class="cur"><path d="M0 0 L0 13 L3.5 9.6 L6 15 L8.2 14 L5.8 8.6 L10.5 8.6z" fill="{P["ink"]}" '
               f'stroke="{P["card"]}" stroke-width="1.2"/></g>')
    smil["cur"] = _move(D, way)
    clicks = [(.07, 56, 50)] + [(slider_t[i] - .01, px + 9 + i * 10, knob_y(start[i])) for i in range(4)] + \
        [(.43, 216, 88), (.48, 218, 90), (.56, 72, 108), (.60, 74, 110), (.76, 266, 78)]
    for i, (t, x, y) in enumerate(clicks):
        out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="2" fill="none" stroke="{P["pink"]}" stroke-width="1.5" '
                   f'class="ck{i}">' + _attr(D, "r", [(0, 2), (t, 2), (t + .04, 9), (1, 9)]) + "</circle>")
        css.append(_fade(f"ck{i}", D, [(0, 0), (t, 0), (t + .005, 1), (t + .04, 0), (1, 0)]))
    return tile(P, "Escape Room", "Escape Room",
                "A 2D point-and-click escape room, built in Unity", False,
                "Animation: in a bedroom scene a cursor reads a note, sets a four-slider light puzzle to its "
                "solution, finds two key parts in a drawer and under the bed, combines them into a key and "
                "unlocks the door.", _inject("".join(out), smil), "".join(css))


# ---------------------------------------------------------------- Classic Games (revived for Windows)
def classic_games(P):
    D = 10
    css, smil = [], {}
    cx, cy = 62, 80
    out = [text(cx, 30, "1990s originals", P, 8.5, "muted", "m", anchor="middle")]
    out.append(f'<circle cx="{cx}" cy="{cy}" r="36" fill="{P["faint"]}" stroke="{P["line"]}"/>')
    sheen = "".join(f'<path d="M{f(cx + rr * math.cos(a0))} {f(cy + rr * math.sin(a0))} A{rr} {rr} 0 0 1 '
                    f'{f(cx + rr * math.cos(a0 + 1.1))} {f(cy + rr * math.sin(a0 + 1.1))}" fill="none" stroke="{P[col]}" '
                    f'stroke-width="3" stroke-opacity=".55" stroke-linecap="round"/>'
                    for rr, a0, col in ((30, 0, "violet"), (24, .5, "cyan"), (18, 1.0, "amber"),
                                        (30, 3.14, "pink"), (24, 3.64, "blue"), (18, 4.14, "green")))
    out.append(f'<g>{sheen}<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" '
               f'to="360 {cx} {cy}" dur="1.6s" repeatCount="indefinite"/></g>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="10" fill="{P["card"]}" stroke="{P["line"]}"/>'
               f'<circle cx="{cx}" cy="{cy}" r="4" fill="{P["bg"]}" stroke="{P["line"]}"/>')
    out.append(text(cx, 132, "CD · Mac · arcade", P, 8.5, "muted", "m", anchor="middle"))

    # modern window
    wx, wy, ww, wh = 124, 20, 166, 116
    out.append(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="6" fill="{P["bg"]}" stroke="{P["line"]}"/>'
               f'<path d="M{wx} {wy + 15} h{ww}" stroke="{P["line"]}"/>'
               + text(wx + 8, wy + 11, "Windows 10/11", P, 8, "muted", "m")
               + f'<path d="M{wx + ww - 40} {wy + 8} h6" stroke="{P["muted"]}"/>'
               f'<rect x="{wx + 26 + ww - 52}" y="{wy + 5}" width="6" height="6" fill="none" stroke="{P["muted"]}"/>'
               f'<path d="M{wx + ww - 13} {wy + 5} l6 6 M{wx + ww - 7} {wy + 5} l-6 6" stroke="{P["muted"]}"/>')
    # data from the disc streams into the window
    for k in range(6):
        t0 = .01 + k * .025
        out.append(f'<g class="pk{k}"><g class="pk{k}f"><rect x="-3" y="-3" width="6" height="6" rx="1" '
                   f'fill="{P["blue"]}"/></g></g>')
        smil[f"pk{k}"] = _move(D, [(0, 100, 80), (t0, 100, 80), (t0 + .08, 150, 80), (1, 150, 80)], False)
        css.append(_fade(f"pk{k}f", D, [(0, 0), (t0, 0), (t0 + .01, 1), (t0 + .07, 1), (t0 + .08, 0), (1, 0)]))

    # compatibility fixes apply (each is a technique the repo's README lists)
    fixes = ["proxy DLL hooks", "no-CD check", "WinG → DirectDraw", "QuickTime → AVI", "scaled window", "Alt+Enter"]
    for i, lab in enumerate(fixes):
        t0 = .14 + i * .045
        out.append(f'<g class="fx{i}">' + text(wx + 10, wy + 32 + i * 13, "✓", P, 9.5, "green", "m", weight="700")
                   + text(wx + 22, wy + 32 + i * 13, lab, P, 9, "ink", "m") + "</g>")
        css.append(_show(f"fx{i}", D, t0, .46))

    # the game runs: an original answer-the-sum shooter, nothing copied from any title
    gx = wx + ww / 2
    game = [text(gx, wy + 30, "7 × 6 = ?", P, 11, "ink", "m", weight="700", anchor="middle")]
    bubs = []
    answers = [(gx - 50, "42", "green"), (gx, "36", "violet"), (gx + 50, "48", "pink")]
    for i, (ax, lab, col) in enumerate(answers):
        bub = (f'<circle cx="{f(ax)}" cy="0" r="11" fill="{P["card"]}" stroke="{P[col]}"/>'
               + text(ax, 3.5, lab, P, 10, col, "m", weight="700", anchor="middle"))
        bubs.append(f'<g class="hit">{bub}</g>' if i == 0 else bub)
    game.append(f'<g class="bdrop">{"".join(bubs)}</g>')
    game.append(f'<g class="ship"><path d="M0 -8 L7 6 L0 3 L-7 6z" fill="{P["blue"]}"/></g>')
    game.append(f'<g class="laser"><line x1="{f(gx - 50)}" y1="{wy + 98}" x2="{f(gx - 50)}" y2="86" '
                f'stroke="{P["red"]}" stroke-width="2"/></g>')
    game.append(f'<g class="pop"><circle cx="{f(gx - 50)}" cy="86" r="9" fill="none" stroke="{P["green"]}" '
                f'stroke-width="2">' + _attr(D, "r", [(0, 9), (.66, 9), (.74, 19), (1, 19)]) + '</circle></g>')
    game.append(f'<g class="pts">' + text(gx - 50, 70, "+10", P, 10, "green", "m", weight="700", anchor="middle") + "</g>")
    out.append(f'<g class="game">{"".join(game)}</g>')
    css.append(_show("game", D, .48, .95))
    smil["bdrop"] = _move(D, [(0, 0, 62), (.48, 0, 62), (.66, 0, 86), (1, 0, 86)], False)
    css.append(_show("hit", D, .48, .66))
    smil["ship"] = _move(D, [(0, gx, wy + 106), (.50, gx, wy + 106), (.62, gx - 50, wy + 106), (1, gx - 50, wy + 106)])
    css.append(_show("laser", D, .63, .665))
    css.append(_fade("pop", D, [(0, 0), (.66, 0), (.67, 1), (.74, 0), (1, 0)]))
    css.append(_show("pts", D, .67, .9))

    # right column: what the repo holds
    out.append(text(300, 48, "the fixes", P, 9, "muted", "m", weight="600"))
    items = [("blue", "proxy DLLs"), ("violet", "PowerPC → C"), ("pink", "arcade emulator"), ("green", "setup scripts"),
             ("amber", "per-game notes")]
    for i, (col, lab) in enumerate(items):
        y = 64 + i * 15
        out.append(f'<rect x="300" y="{y - 6}" width="6" height="6" rx="1" fill="{P[col]}"/>'
                   + text(311, y, lab, P, 9, "ink", "m"))
    out.append(text(300, 138, "game files not in repo", P, 8, "muted", "m"))
    return tile(P, "Classic Games", "Classic Games",
                "Kids' CD-ROM, Mac and arcade games revived for Windows 10/11", True,
                "Animation: a spinning disc streams into a Windows 10/11 window, compatibility fixes tick off one by "
                "one (proxy DLL hooks, no-CD, DirectDraw, AVI video, window scaling) and an abstract answer-the-sum "
                "shooter starts running.", _inject("".join(out), smil), "".join(css))


# ---------------------------------------------------------------- HeroClix Manual (tabletop gameplay, abstract)
def heroclix(P):
    D = 10
    css, smil = [], {}
    ox, oy, c, cols, rows = 14, 14, 18, 12, 7
    cell = lambda i, j: (ox + i * c + c / 2, oy + j * c + c / 2)
    out = [f'<rect x="{ox}" y="{oy}" width="{cols * c}" height="{rows * c}" rx="4" fill="{P["bg"]}" stroke="{P["line"]}"/>']
    grid = "".join(f'<line x1="{ox + i * c}" y1="{oy}" x2="{ox + i * c}" y2="{oy + rows * c}"/>' for i in range(1, cols)) + \
        "".join(f'<line x1="{ox}" y1="{oy + j * c}" x2="{ox + cols * c}" y2="{oy + j * c}"/>' for j in range(1, rows))
    out.append(f'<g stroke="{P["faint"]}">{grid}</g>')
    # terrain: blocking walls, hindering squares, water
    for i, j in ((6, 0), (6, 1), (2, 2), (3, 2)):
        out.append(f'<rect x="{ox + i * c + 1}" y="{oy + j * c + 1}" width="{c - 2}" height="{c - 2}" rx="2" '
                   f'fill="{P["muted"]}" fill-opacity=".55"/>')
    for i, j in ((8, 4), (9, 4), (8, 5)):
        x, y = ox + i * c, oy + j * c
        out.append(f'<rect x="{x + 1}" y="{y + 1}" width="{c - 2}" height="{c - 2}" rx="2" fill="{P["green"]}" '
                   f'fill-opacity=".14" stroke="{P["green"]}" stroke-opacity=".5" stroke-dasharray="2 2"/>')
    for i, j in ((0, 0), (1, 0), (0, 1)):
        out.append(f'<rect x="{ox + i * c + 1}" y="{oy + j * c + 1}" width="{c - 2}" height="{c - 2}" rx="2" '
                   f'fill="{P["cyan"]}" fill-opacity=".18"/>')

    def fig(col):
        return (f'<circle r="7.5" fill="{P[col]}"/><circle r="4.5" fill="none" stroke="{P["card"]}" stroke-width="1.5"/>'
                f'<rect x="-1.5" y="-7.5" width="3" height="3" fill="{P["card"]}"/>')

    # static figures
    for (i, j), col in (((3, 5), "blue"), ((10, 5), "red")):
        x, y = cell(i, j)
        out.append(f'<g transform="translate({f(x)} {f(y)})">{fig(col)}</g>')
    # mover: 3 squares (diagonals count 1), highlighted path
    path = [(1, 4), (2, 4), (3, 3), (4, 3)]
    for k, (i, j) in enumerate(path[1:]):
        out.append(f'<g class="mv"><rect x="{ox + i * c + 2}" y="{oy + j * c + 2}" width="{c - 4}" height="{c - 4}" rx="2" '
                   f'fill="{P["blue"]}" stroke="{P["blue"]}"/></g>')
    css.append(_fade("mv", D, [(0, 0), (.04, 0), (.06, .22), (.30, .22), (.33, 0), (1, 0)]))
    tgt = cell(10, 1)
    out.append(f'<g class="tring"><circle cx="{f(tgt[0])}" cy="{f(tgt[1])}" r="11" fill="none" stroke="{P["red"]}" '
               f'stroke-width="1.5" stroke-dasharray="3 2"/></g>')
    css.append(_show("tring", D, .32, .70))
    end = cell(*path[-1])
    out.append(f'<path d="M{f(end[0])} {f(end[1])} L{f(tgt[0])} {f(tgt[1])}" pathLength="1" class="lof" fill="none" '
               f'stroke="{P["amber"]}" stroke-width="2" stroke-dasharray="1"/>')
    css.append(".lof{stroke-dashoffset:1;animation:lof 10s infinite}@keyframes lof{0%,32%{stroke-dashoffset:1;stroke-opacity:1}"
               "38%,68%{stroke-dashoffset:0;stroke-opacity:1}72%,100%{stroke-dashoffset:0;stroke-opacity:0}}")
    out.append(f'<g class="lofl">' + text(end[0] + 32, end[1] + 2, "line of fire", P, 8.5, "amber", "m") + "</g>")
    css.append(_show("lofl", D, .37, .68))
    # target figure + damage flash
    out.append(f'<g transform="translate({f(tgt[0])} {f(tgt[1])})">{fig("red")}</g>'
               f'<g class="flash"><circle cx="{f(tgt[0])}" cy="{f(tgt[1])}" r="9" fill="{P["amber"]}"/></g>')
    css.append(_fade("flash", D, [(0, 0), (.58, 0), (.585, .8), (.62, 0), (.64, .8), (.67, 0), (1, 0)]))
    out.append(f'<g class="dmg">' + text(tgt[0] - 16, tgt[1] + 24, "2 clicks", P, 9, "red", "m", weight="700") + "</g>")
    css.append(_show("dmg", D, .59, .82))
    # the moving figure
    pts = [(0, *cell(*path[0])), (.08, *cell(*path[0]))]
    for k, sq in enumerate(path[1:]):
        pts.append((.08 + (k + 1) * .07, *cell(*sq)))
    pts += [(.94, *cell(*path[-1])), (1, *cell(*path[0]))]
    out.append(f'<g class="hero">{fig("blue")}</g>')
    smil["hero"] = _move(D, pts)

    # right panel: dice, the roll, the target's combat dial
    rx = 244
    out.append(text(rx, 46, "attack roll", P, 9, "muted", "m", weight="600"))
    pip = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)], 4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
           5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}

    def die(x, y, n):
        return (f'<rect x="{x}" y="{y}" width="16" height="16" rx="3" fill="{P["card"]}" stroke="{P["ink"]}"/>'
                + "".join(f'<circle cx="{f(x + 8 + 4.5 * a)}" cy="{f(y + 8 + 4.5 * b)}" r="1.6" fill="{P["ink"]}"/>'
                          for a, b in pip[n]))
    seq = [(3, 6), (1, 4), (6, 2), (5, 3)]  # tumbling faces, then the result 5 + 3
    for k, (a, b) in enumerate(seq):
        out.append(f'<g class="dc{k}">{die(rx, 54, a)}{die(rx + 22, 54, b)}</g>')
        if k < 3:
            t0 = .40 + k * .025
            css.append(_show(f"dc{k}", D, t0, t0 + .02, ramp=.004))
        else:
            css.append(_fade(f"dc{k}", D, [(0, 1), (.39, 1), (.395, 0), (.475, 0), (.48, 1), (1, 1)], base=1))
    out.append(f'<g class="r1">' + text(rx, 88, "9 + 8 = 17", P, 9, "ink", "m") + "</g>")
    out.append(f'<g class="r2">' + text(rx, 101, "vs DEF 17", P, 9, "ink", "m") + "</g>")
    out.append(f'<g class="r3">' + text(rx, 116, "HIT", P, 11, "green", "m", weight="700") + "</g>")
    css.append(_show("r1", D, .49, .9) + _show("r2", D, .52, .9) + _show("r3", D, .55, .9))
    out.append(text(rx, 136, "2d6 + attack", P, 8, "muted", "m"))

    dcx, dcy, dr = 360, 100, 33
    out.append(text(dcx, 60, "target's dial", P, 8.5, "muted", "m", anchor="middle"))
    ticks = "".join(f'<line x1="{f(dcx + (dr - 6) * math.cos(a))}" y1="{f(dcy + (dr - 6) * math.sin(a))}" '
                    f'x2="{f(dcx + (dr - 1) * math.cos(a))}" y2="{f(dcy + (dr - 1) * math.sin(a))}"/>'
                    for a in (k * math.pi / 6 for k in range(12)))
    out.append(f'<circle cx="{dcx}" cy="{dcy}" r="{dr}" fill="{P["faint"]}" stroke="{P["line"]}"/>'
               f'<g stroke="{P["muted"]}" stroke-width="1.5">{ticks}'
               f'<circle cx="{dcx}" cy="{dcy + dr - 9}" r="2.2" fill="{P["red"]}" stroke="none"/>'
               + _move(D, [(t, a, (dcx, dcy)) for t, a in ((0, 0), (.60, 0), (.62, -30), (.64, -30), (.66, -60),
                                                            (.94, -60), (.98, 0), (1, 0))], kind="rotate") + "</g>")
    wx0, wy0 = dcx - 22, dcy - 22
    out.append(f'<rect x="{wx0}" y="{wy0}" width="44" height="32" rx="4" fill="{P["card"]}" stroke="{P["ink"]}"/>')
    stats = [(8, 10, 17, 3, "click 1"), (7, 10, 16, 3, "click 2"), (7, 9, 16, 2, "click 3")]
    cols_ = ("blue", "red", "green", "amber")
    for k, vals in enumerate(stats):
        g = []
        for s in range(4):
            x = wx0 + 6 + (s % 2) * 22
            y = wy0 + 13 + (s // 2) * 13
            g.append(f'<rect x="{x - 3}" y="{y - 6}" width="2.5" height="7" fill="{P[cols_[s]]}"/>'
                     + text(x + 1, y, str(vals[s]), P, 10, "ink", "m", weight="700"))
        g.append(text(dcx, dcy + 22, vals[4], P, 8, "muted", "m", anchor="middle"))
        out.append(f'<g class="v{k}">{"".join(g)}</g>')
    css.append(_fade("v0", D, [(0, 1), (.61, 1), (.615, 0), (.95, 0), (.96, 1), (1, 1)], base=1))
    css.append(_fade("v1", D, [(0, 0), (.61, 0), (.615, 1), (.65, 1), (.655, 0), (1, 0)]))
    css.append(_fade("v2", D, [(0, 0), (.65, 0), (.655, 1), (.95, 1), (.96, 0), (1, 0)]))
    return tile(P, "HeroClix", "HeroClix",
                "HeroClix in Unity: 13k units, rules engine, online play", True,
                "Animation: on a square-grid map a figure moves three squares, traces a line of fire to an enemy, "
                "rolls 2d6 against its defense and hits, and the target's combat dial clicks twice as its values drop.",
                _inject("".join(out), smil), "".join(css))


# ---------------------------------------------------------------- Pokemon Red RL experiments (agent exploring)
def pokemon_rl(P):
    D = 12
    css = []
    ox, oy, c, W, H = 14, 20, 10, 20, 11
    blocked = set()
    for bx, by, bw, bh in ((3, 2, 2, 3), (8, 0, 1, 4), (11, 5, 3, 2), (15, 1, 2, 3), (6, 7, 4, 1), (16, 7, 1, 3),
                           (1, 8, 2, 2), (12, 2, 1, 1), (19, 4, 1, 3)):
        blocked |= {(x, y) for x in range(bx, bx + bw) for y in range(by, by + bh)}
    free = [(x, y) for x in range(W) for y in range(H) if (x, y) not in blocked]
    # deterministic DFS-style exploration with backtracking: the agent walks every step it takes
    r = rng(11)
    start = (1, 5)
    walk, seen, stack = [start], {start}, [start]
    while len(walk) < 118 and stack:
        x, y = stack[-1]
        nb = [(x + dx, y + dy) for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1))]
        nb = [p for p in nb if 0 <= p[0] < W and 0 <= p[1] < H and p not in blocked and p not in seen]
        if nb:
            nb.sort(key=lambda p: (p[0] < x) * .6 + r())  # drift east, like heading out of town
            p = nb[0]
            seen.add(p)
            stack.append(p)
        else:
            stack.pop()
            if not stack:
                break
            p = stack[-1]
        walk.append(p)
    n = len(walk)
    t0, t1 = .03, .90
    tt = [t0 + (t1 - t0) * k / (n - 1) for k in range(n)]
    out = [f'<rect x="{ox}" y="{oy}" width="{W * c}" height="{H * c}" rx="3" fill="{P["bg"]}" stroke="{P["line"]}"/>']
    grid = "".join(f'<line x1="{ox + i * c}" y1="{oy}" x2="{ox + i * c}" y2="{oy + H * c}"/>' for i in range(1, W)) + \
        "".join(f'<line x1="{ox}" y1="{oy + j * c}" x2="{ox + W * c}" y2="{oy + j * c}"/>' for j in range(1, H))
    out.append(f'<g stroke="{P["faint"]}">{grid}</g>')
    out.append(f'<g fill="{P["muted"]}" fill-opacity=".45">'
               + "".join(f'<rect x="{ox + x * c + .5}" y="{oy + y * c + .5}" width="{c - 1}" height="{c - 1}" rx="1"/>'
                         for x, y in sorted(blocked)) + "</g>")
    # coverage heat map: first visit (amber), second visit (red), grouped into time buckets
    NB = 12
    first, second = {}, {}
    for k, p in enumerate(walk):
        if p not in first:
            first[p] = k
        elif p not in second:
            second[p] = k
    for layer, visits, col in (("h", first, "amber"), ("g", second, "red")):
        buckets = {}
        for p, k in visits.items():
            buckets.setdefault(min(NB - 1, int((tt[k] - t0) / (t1 - t0 + 1e-9) * NB)), []).append((p, k))
        for b, cells in sorted(buckets.items()):
            ta = max(tt[k] for _, k in cells)
            out.append(f'<g class="{layer}{b}" fill="{P[col]}">'
                       + "".join(f'<rect x="{ox + x * c}" y="{oy + y * c}" width="{c}" height="{c}"/>' for (x, y), _ in cells)
                       + "</g>")
            v = .42 if layer == "h" else .38
            css.append(f".{layer}{b}{{fill-opacity:0;animation:{layer}{b} {D}s infinite}}@keyframes {layer}{b}{{0%,"
                       f"{_pc(ta - .01)}{{fill-opacity:0}}{_pc(ta)},93%{{fill-opacity:{v}}}97%,100%{{fill-opacity:0}}}}")
    # reward events on the map (story event, battle damage, heal) at cells the walk reaches
    ev_idx = [int(n * .28), int(n * .55), int(n * .8)]
    evs = [("event", "violet"), ("battle", "red"), ("heal", "green")]
    for (lab, col), k in zip(evs, ev_idx):
        x, y = walk[k]
        cxp, cyp = ox + x * c + c / 2, oy + y * c + c / 2
        out.append(f'<path d="M{f(cxp)} {f(cyp - 4)} l4 4 l-4 4 l-4 -4z" fill="{P[col]}"/>')
        out.append(f'<g class="e{lab}"><circle cx="{f(cxp)}" cy="{f(cyp)}" r="7" fill="none" stroke="{P[col]}" '
                   f'stroke-width="2"/>' + text(min(cxp + 7, ox + W * c - 34), max(cyp - 7, oy + 8), f"+{lab}", P, 8.5,
                                               col, "m", weight="700") + "</g>")
        css.append(_show(f"e{lab}", D, tt[k], tt[k] + .08))
    # the agent
    kfs = [(0, *walk[0])] + [(t, *p) for t, p in zip(tt, walk)] + [(.97, *walk[-1]), (.975, *walk[0]), (1, *walk[0])]
    out.append(f'<g><rect x="{ox + 1}" y="{oy + 1}" width="{c - 2}" height="{c - 2}" rx="2" fill="{P["blue"]}" '
               f'stroke="{P["card"]}"/>' + _move(D, [(t, x * c, y * c) for t, x, y in kfs], False) + "</g>")
    out.append(text(ox, oy + H * c + 12, "agent: PPO over PyBoy, pixels + RAM state", P, 8, "muted", "m"))

    # right panel: coverage and the shaped reward
    rx, rw = 232, 164
    total = len(free)
    out.append(text(rx, 48, "map coverage", P, 9, "muted", "m", weight="600"))
    out.append(f'<rect x="{rx}" y="54" width="{rw}" height="7" rx="3.5" fill="{P["faint"]}" stroke="{P["line"]}"/>')
    cov = [sum(1 for k in first.values() if k <= i) / total for i in range(n)]
    stops = [(0, 0)] + [(tt[i], cov[i]) for i in range(0, n, 6)] + [(t1, cov[-1]), (.94, cov[-1]), (.97, 0), (1, 0)]
    out.append(f'<rect x="{rx}" y="54" width="0" height="7" rx="3.5" fill="{P["amber"]}">'
               + _attr(D, "width", [(t, rw * v) for t, v in stops]) + "</rect>")
    # percentage label, bucketed
    for b in range(6):
        ta = t0 + (t1 - t0) * b / 6
        tb = t0 + (t1 - t0) * (b + 1) / 6 if b < 5 else .95
        i = min(n - 1, int((tb - t0) / (t1 - t0) * (n - 1)))
        out.append(f'<g class="pc{b}">' + text(rx + rw, 48, f"{round(cov[i] * 100)} %", P, 9, "amber", "m",
                                               weight="700", anchor="end") + "</g>")
        css.append(_show(f"pc{b}", D, max(ta, .02), tb - .005, ramp=.004))
    # reward curve: exploration adds a little per new tile, events add steps
    rew, acc = [], 0.0
    for k, p in enumerate(walk):
        if first.get(p) == k:
            acc += 1
        if k in ev_idx:
            acc += 9
        rew.append(acc)
    cx0, cy0, cw, ch = rx, 82, rw, 50
    out.append(text(rx, 76, "shaped reward", P, 9, "muted", "m", weight="600"))
    out.append(f'<path d="M{cx0} {cy0} v{ch} h{cw}" fill="none" stroke="{P["line"]}"/>')
    pts = [(cx0 + cw * (tt[k] - t0) / (t1 - t0), cy0 + ch - ch * rew[k] / rew[-1] * .92) for k in range(n)]
    d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)
    out.append(f'<clipPath id="rc"><rect x="{cx0}" y="{cy0 - 4}" height="{ch + 6}" width="0">'
               + _attr(D, "width", [(0, 0), (t0, 0), (t1, cw + 2), (.94, cw + 2), (.97, 0), (1, 0)]) + "</rect></clipPath>")
    out.append(f'<g clip-path="url(#rc)"><path d="{d} V{cy0 + ch} H{cx0}z" fill="{P["green"]}" fill-opacity=".14"/>'
               f'<path d="{d}" fill="none" stroke="{P["green"]}" stroke-width="2" stroke-linejoin="round"/></g>')
    for (lab, col), k in zip(evs, ev_idx):
        x, y = pts[k]
        out.append(f'<g class="ev{lab}"><circle cx="{f(x)}" cy="{f(y)}" r="3" fill="{P[col]}"/></g>')
        css.append(_fade(f"ev{lab}", D, [(0, 0), (tt[k] - .002, 0), (tt[k], 1), (.94, 1), (.97, 0), (1, 0)]))
    out.append(text(rx + rw, cy0 + ch + 10, "steps →", P, 8, "muted", "m", anchor="end"))
    return tile(P, "Pokémon Red RL experiments", "Pokémon Red RL experiments",
                "Fork of an RL project: reward shaping and seeded PPO sweeps", False,
                "Animation: an agent explores a tile map while a coverage heat map fills in behind it, story-event, "
                "battle and heal rewards pop as it reaches them, and the coverage bar and shaped-reward curve rise.",
                "".join(out), "".join(css))


NEW_CARDS = {"tiles/escape-room": escape_room, "tiles/classic-games": classic_games,
             "tiles/heroclix-manual": heroclix, "tiles/pokemon-red-rl": pokemon_rl}
