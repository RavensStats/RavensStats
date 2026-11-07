"""Four more 410x200 project tiles (Tic Tac Toe Evolved, Guess Who, backdoor robustness, diffusion quantization).

Same frame and palette as tiles.py. Fades use fill-/stroke-opacity; scene switches use visibility.
"""
import math

from common import ACCENTS, f, rng, text
from tiles import tile


def _n(x):
    """Number with 4 decimals, for keyTimes (common.f keeps only 1)."""
    return f"{x:.4f}".rstrip("0").rstrip(".")


def _p(t):
    return f"{t * 100:.2f}".rstrip("0").rstrip(".")


def _kf(name, dur, stops, base=""):
    """CSS class + keyframes. stops: [(t in 0..1, 'decls'), ...]; base: static decls (also the reduced-motion state)."""
    frames = "".join(f"{_p(t)}%{{{d}}}" for t, d in stops)
    return f".{name}{{{base}animation:{name} {dur}s linear infinite}}@keyframes {name}{{{frames}}}"


def _on(t, prop="stroke-opacity", t_end=1.0, w=.008):
    """Hidden until t, shown until t_end (then hidden again if t_end < 1). prop may be "a;b" for several."""
    def d(v):
        return ";".join(f"{p}:{v}" for p in prop.split(";"))
    st = [(0, d(0)), (t, d(0)), (t + w, d(1))]
    if t_end < 1:
        st += [(t_end, d(1)), (t_end + w, d(0))]
    return st + [(1, d(1 if t_end >= 1 else 0))]


def _atf(typ, stops, dur, begin=0):
    """SMIL animateTransform (CSS transform animations are unreliable in SVG-as-image renders)."""
    bg = f' begin="{_n(begin)}s"' if begin else ""
    return (f'<animateTransform attributeName="transform" type="{typ}" dur="{dur}s" repeatCount="indefinite"{bg} '
            f'values="{";".join(v for _, v in stops)}" keyTimes="{";".join(_n(t) for t, _ in stops)}"/>')


def _vis(a, b, dur):
    """SMIL child for a <g>: visible only for a <= t < b of the cycle (discrete, so no fades)."""
    vals, kts = ("visible;hidden", f"0;{_n(b)}") if a == 0 else (
        ("hidden;visible", f"0;{_n(a)}") if b >= 1 else ("hidden;visible;hidden", f"0;{_n(a)};{_n(b)}"))
    return (f'<animate attributeName="visibility" calcMode="discrete" dur="{dur}s" repeatCount="indefinite" '
            f'values="{vals}" keyTimes="{kts}"/>')


# ---------------------------------------------------------------- Tic Tac Toe Evolved
def tictactoe(P):
    dur, S, X0, Y0 = 12, 32, 60, 25
    css, out = [], []
    uid = [0]

    def cls():
        uid[0] += 1
        return f"m{uid[0]}"

    def cxy(c, r):
        return X0 + S * c + S / 2, Y0 + S * r + S / 2

    def cell(c, r, extra=""):
        return (f'<rect x="{X0 + S * c + 2}" y="{Y0 + S * r + 2}" width="{S - 4}" height="{S - 4}" rx="5" '
                f'fill="{P["faint"]}" stroke="{P["line"]}"{extra}/>')

    def mark(kind, c, r, k):
        x, y = cxy(c, r)
        if kind == "X":
            return (f'<path d="M{f(x - 7.5)} {f(y - 7.5)}L{f(x + 7.5)} {f(y + 7.5)}M{f(x + 7.5)} {f(y - 7.5)}'
                    f'L{f(x - 7.5)} {f(y + 7.5)}" fill="none" stroke="{P["blue"]}" stroke-width="3.2" '
                    f'stroke-linecap="round" class="{k}"/>')
        return (f'<circle cx="{f(x)}" cy="{f(y)}" r="8.5" fill="none" stroke="{P["amber"]}" stroke-width="3" '
                f'class="{k}"/>')

    def winline(c0, r0, c1, r1, t):
        k = cls()
        (x0, y0), (x1, y1) = cxy(c0, r0), cxy(c1, r1)
        css.append(_kf(k, dur, [(0, "stroke-dashoffset:1"), (t, "stroke-dashoffset:1"),
                                (t + .02, "stroke-dashoffset:0"), (1, "stroke-dashoffset:0")]))
        return (f'<path d="M{f(x0 - 14)} {f(y0)}L{f(x1 + 14)} {f(y1)}" pathLength="1" stroke-dasharray="1" '
                f'stroke="{P["green"]}" stroke-width="3.5" stroke-linecap="round" stroke-opacity=".85" class="{k}"/>')

    out.append("".join(cell(c, r) for c in range(3) for r in range(3)))

    # scene 0: Classic, X takes the top row
    s0 = []
    for i, (kind, c, r) in enumerate([("X", 0, 0), ("O", 1, 1), ("X", 2, 0), ("O", 0, 2), ("X", 1, 0)]):
        k = cls()
        css.append(_kf(k, dur, _on(.02 + i * .03)))
        s0.append(mark(kind, c, r, k))
    s0.append(winline(0, 0, 2, 0, .175))

    # scene 1: Gravity, marks drop to the column floor; X takes the bottom row
    s1 = []
    for i, (kind, c, r) in enumerate([("X", 1, 2), ("O", 1, 1), ("X", 0, 2), ("O", 0, 1), ("X", 2, 2)]):
        k, t, dy = cls(), .27 + i * .033, S * r + 34
        css.append(_kf(k, dur, _on(t, w=.002)))
        s1.append(f'<g>{mark(kind, c, r, k)}'
                  + _atf("translate", [(0, f"0 -{dy}"), (t, f"0 -{dy}"), (t + .018, "0 0"), (1, "0 0")], dur) + "</g>")
    s1.append(f'<line x1="{X0}" y1="{Y0 + 3 * S + 3}" x2="{X0 + 3 * S}" y2="{Y0 + 3 * S + 3}" stroke="{P["muted"]}" '
              f'stroke-width="2" stroke-linecap="round"/>')
    s1.append(winline(0, 2, 2, 2, .445))

    # scene 2: Quantum, only each player's 3 newest marks survive and older ones fade
    s2 = []
    seq = [("X", 0, 0), ("O", 1, 1), ("X", 2, 2), ("O", 0, 2), ("X", 2, 0), ("O", 1, 0), ("X", 0, 1), ("O", 2, 1)]
    times = [.515 + i * .027 for i in range(len(seq))]
    for i, (kind, c, r) in enumerate(seq):
        k = cls()
        st = [(0, "stroke-opacity:0"), (times[i], "stroke-opacity:0")]
        removed = i + 6 if i + 6 < len(seq) else None  # the same player's 4th later mark evicts this one
        for j in range(i, len(seq)):
            if removed is not None and j >= removed:
                st.append((times[j], st[-1][1]))
                st.append((times[j] + .012, "stroke-opacity:0"))
                break
            a = max(.15, 1 - .85 * (j - i) / 3)
            st.append((times[j] + .003, f"stroke-opacity:{f(a)}"))
        st.append((1, st[-1][1]))
        css.append(_kf(k, dur, st))
        s2.append(mark(kind, c, r, k))

    # scene 3: Expansion, a random edge grows after every move
    s3 = []
    for col, t in ((3, .785), (-1, .83)):
        k, h = cls(), cls()
        css.append(_kf(k, dur, _on(t, "fill-opacity;stroke-opacity", w=.012)))
        css.append(_kf(h, dur, [(0, "stroke-opacity:0"), (t, "stroke-opacity:0"), (t + .01, "stroke-opacity:1"),
                                (t + .05, "stroke-opacity:0"), (1, "stroke-opacity:0")]))
        s3.append("".join(cell(col, r, f' class="{k}"') for r in range(3)))
        s3.append(f'<rect x="{X0 + S * col}" y="{Y0}" width="{S}" height="{3 * S}" rx="7" fill="none" '
                  f'stroke="{P["pink"]}" stroke-width="2" class="{h}"/>')
    for (kind, c, r), t in ((("X", 1, 1), .77), (("O", 3, 0), .81), (("X", -1, 2), .855)):
        k = cls()
        css.append(_kf(k, dur, _on(t)))
        s3.append(mark(kind, c, r, k))

    # right panel: the eight modes, the one on the board highlighted, plus its rule
    names = ["Classic", "Expansion", "Recursive", "Ultimate", "Quantum", "Gravity", "Wild", "Mirror"]

    def chip(i, active):
        x, y = 206 + (i // 4) * 98, 37 + (i % 4) * 24
        if active:
            return (f'<rect x="{x}" y="{y}" width="90" height="19" rx="9.5" fill="{P["violet"]}" fill-opacity=".16" '
                    f'stroke="{P["violet"]}"/>' + text(x + 45, y + 13, names[i], P, 10, "violet", "m", "700", "middle"))
        return (f'<rect x="{x}" y="{y}" width="90" height="19" rx="9.5" fill="{P["card"]}" stroke="{P["line"]}"/>'
                + text(x + 45, y + 13, names[i], P, 10, "muted", "m", anchor="middle"))

    out.append(text(206, 27, "8 MODES", P, 9.5, "muted", "m", "600", extra=' letter-spacing="1"')
               + "".join(chip(i, False) for i in range(8)))
    rules = ["3 in a row wins", "pieces fall to the column floor", "only your 3 newest marks survive",
             "a random edge grows each move"]
    for k, (body, mode) in enumerate(zip((s0, s1, s2, s3), (0, 5, 4, 1))):
        out.append(f'<g{"" if k == 0 else ' visibility="hidden"'}>{_vis(k / 4, (k + 1) / 4, dur)}{"".join(body)}{chip(mode, True)}'
                   + text(206, 139, rules[k], P, 9.5, "ink", "m") + "</g>")
    return tile(P, "Tic Tac Toe Evolved", "Tic Tac Toe Evolved",
                "Eight rule variants of tic-tac-toe, two-player or vs AI", True,
                "Animation: one board plays through four of the game's eight modes in turn: Classic (X wins the top "
                "row), Gravity (marks drop to the column floor), Quantum (older marks fade and each player's fourth "
                "mark erases their oldest) and Expansion (a new column grows after each move), while the mode list "
                "highlights the active variant.", "".join(out), "".join(css))


# ---------------------------------------------------------------- Guess Who
def guess_who(P):
    dur, W, H = 10, 30, 38
    r = rng(11)
    hair_cols = ["amber", "ink", "red", "violet"]
    cards = [dict(hat=r() < .3, glasses=r() < .42, beard=r() < .35, hair=int(r() * 4), bg=ACCENTS[int(r() * 6)])
             for _ in range(24)]
    target = 13
    cards[target].update(hat=False, glasses=True, beard=False, hair=0)
    qs = [("Hat?", "hat", False), ("Glasses?", "glasses", True), ("Beard?", "beard", False),
          ("Blond hair?", "hair", True)]

    def keeps(cd, attr, yes):
        v = cd["hair"] == 0 if attr == "hair" else cd[attr]
        return v == yes
    for i, cd in enumerate(cards):  # make the target the only card matching every answer
        if i != target and all(keeps(cd, a, y) for _, a, y in qs):
            cd["hair"] = 1
    alive, out_q = set(range(24)), []
    for _, a, y in qs:
        gone = {i for i in alive if not keeps(cards[i], a, y)}
        out_q.append(gone)
        alive -= gone
    assert alive == {target} and all(out_q), (alive, [len(g) for g in out_q])

    T = [.04 + .17 * i for i in range(5)]  # question times; answers +.05, flips +.07
    css, out = [], []
    for k, t in enumerate(T[:4]):
        tf = t + .07
        css.append(_kf(f"o{k}", dur, [(0, "fill-opacity:0"), (tf + .01, "fill-opacity:0"),
                                      (tf + .025, "fill-opacity:1"), (.95, "fill-opacity:1"),
                                      (.96, "fill-opacity:0"), (1, "fill-opacity:0")]))
    when = {i: k for k, g in enumerate(out_q) for i in g}
    for i, cd in enumerate(cards):
        x, y = 14 + (i % 8) * 34, 12 + (i // 8) * 43
        u = f' x="{x}" y="{y}"'
        face = [f'<use href="#cr"{u}/><use href="#tn"{u} fill="{P[cd["bg"]]}"/><use href="#hd"{u}/>'
                f'<use href="#hr"{u} fill="{P[hair_cols[cd["hair"]]]}"/>']
        if cd["beard"]:
            face.append(f'<use href="#bd"{u} fill="{P[hair_cols[cd["hair"]]]}"/>')
        if cd["glasses"]:
            face.append(f'<use href="#gs"{u}/>')
        if cd["hat"]:
            face.append(f'<use href="#ht"{u}/>')
        if i in when:
            k, d = when[i], (i % 8) * .03
            tf, yb = T[k] + .07, y + H
            flip = _atf("scale", [(0, "1 1"), (tf, "1 1"), (tf + .025, "1 .13"), (.95, "1 .13"), (.975, "1 1"),
                                  (1, "1 1")], dur, d)
            out.append(f'<g transform="translate(0 {yb})"><g>{flip}<g transform="translate(0 -{yb})">{"".join(face)}'
                       f'<use href="#ov"{u} class="o{k}" style="animation-delay:{_n(d)}s"/></g></g></g>')
        else:
            out.append("".join(face))
            out.append(f'<rect x="{x - 2}" y="{y - 2}" width="{W + 4}" height="{H + 4}" rx="6" fill="none" '
                       f'stroke="{P["amber"]}" stroke-width="2.2" class="gl"/>')
    # card parts, drawn relative to the card's top-left corner (cx = 15, head centre y = 18)
    out.insert(0, f'<defs><g id="cr"><rect width="{W}" height="{H}" rx="4" fill="{P["bg"]}" stroke="{P["line"]}"/>'
                  f'<rect x="4" y="31" width="{W - 8}" height="4" rx="2" fill="{P["line"]}"/></g>'
                  f'<rect id="tn" x="2" y="2" width="{W - 4}" height="27" rx="3" fill-opacity=".2"/>'
                  f'<g id="hd"><circle cx="15" cy="18" r="7.5" fill="{P["faint"]}" stroke="{P["muted"]}" '
                  f'stroke-width=".8"/><circle cx="12" cy="18" r="1" fill="{P["ink"]}"/><circle cx="18" cy="18" r="1" '
                  f'fill="{P["ink"]}"/><path d="M13 21.5h4" stroke="{P["ink"]}" stroke-width=".9"/></g>'
                  f'<path id="hr" d="M6.5 17a8.5 9.5 0 0 1 17 0q-8.5-7-17 0z"/>'
                  f'<path id="bd" d="M8.5 19q6.5 10 13 0q-6.5 4-13 0z"/>'
                  f'<g id="gs" fill="none" stroke="{P["ink"]}" stroke-width=".9"><circle cx="12" cy="18" r="2.4"/>'
                  f'<circle cx="18" cy="18" r="2.4"/><path d="M14.4 18h1.2"/></g>'
                  f'<path id="ht" d="M5 11h20M9 11v-6h12v6" fill="{P["blue"]}" stroke="{P["blue"]}" stroke-width="2" '
                  f'stroke-linejoin="round"/>'
                  f'<rect id="ov" width="{W}" height="{H}" rx="4" fill="{P["muted"]}"/></defs>')
    css.append(_kf("gl", dur, [(0, "stroke-opacity:0"), (T[4] + .06, "stroke-opacity:0"),
                               (T[4] + .08, "stroke-opacity:1"), (.94, "stroke-opacity:1"), (.96, "stroke-opacity:0"),
                               (1, "stroke-opacity:0")], "stroke-opacity:0;"))

    # right panel: question log and the cards still standing
    out.append(text(298, 44, "QUESTIONS", P, 9, "muted", "m", "600", extra=' letter-spacing="1"'))
    log = [(q, "yes" if y else "no") for q, _, y in qs] + [("Guess!", "yes!")]
    for i, (q, a) in enumerate(log):
        yy = 58 + i * 16
        css.append(_kf(f"q{i}", dur, _on(T[i], "fill-opacity", .955)))
        css.append(_kf(f"a{i}", dur, _on(T[i] + .05, "fill-opacity", .955)))
        out.append(text(298, yy, q, P, 10, "ink", f"m q{i}")
                   + text(398, yy, a, P, 10, "green" if a != "no" else "red", f"m a{i}", "700", "end"))
    left = [24]
    for g in out_q:
        left.append(left[-1] - len(g))
    edges = [0] + [t + .09 for t in T[:4]] + [.955]
    for i, n in enumerate(left):
        a, b = edges[i], edges[i + 1]
        st = ([(0, "fill-opacity:1")] if i == 0 else [(0, "fill-opacity:0"), (a, "fill-opacity:0"),
                                                       (a + .005, "fill-opacity:1")])
        st += [(b, "fill-opacity:1"), (b + .005, "fill-opacity:0"), (1, "fill-opacity:1" if i == 0 else "fill-opacity:0")]
        if i == 0:
            st = [(0, "fill-opacity:1"), (b, "fill-opacity:1"), (b + .005, "fill-opacity:0"), (.955, "fill-opacity:0"),
                  (.96, "fill-opacity:1"), (1, "fill-opacity:1")]
        css.append(_kf(f"n{i}", dur, st, "" if i == 0 else "fill-opacity:0;"))
        out.append(text(298, 140, f"{n} card{'s' if n != 1 else ''} left", P, 10, "amber" if n == 1 else "muted",
                        f"m n{i}", "600"))
    return tile(P, "Guess Who", "Guess Who",
                "Seeded boards with share codes; faces from a wiki scraper", True,
                "Animation: a board of 24 abstract face cards; yes/no questions about hats, glasses, beards and hair "
                "flip the non-matching cards down one question at a time until a single card is left and the guess "
                "is right.", "".join(out), "".join(css))


# ---------------------------------------------------------------- Backdoor robustness (two group projects)
def backdoor(P):
    dur = 10
    css, out = [], []
    # clients: CIFAR-style thumbnails; client 3 poisons with a red trigger patch in the bottom-right corner
    ys = [28 + 27 * k for k in range(4)]
    shapes = ["M5 16l6-8 6 8z", "M4 15h14v-4l-4-3h-6l-4 3z", "M11 5a5 5 0 1 0 .1 0z", "M3 15q8-12 16 0z"]
    out.append(text(14, 20, "clients", P, 9, "muted", "m"))
    for k, y in enumerate(ys):
        col = "red" if k == 2 else ACCENTS[k]
        out.append(f'<g transform="translate(14 {y})"><rect width="22" height="22" rx="3" fill="{P[col]}" '
                   f'fill-opacity=".14" stroke="{P[col]}"/><path d="{shapes[k]}" fill="{P[col]}" fill-opacity=".7"/>'
                   + (f'<rect x="15" y="15" width="5" height="5" fill="{P["red"]}"/>' if k == 2 else "") + "</g>")
    # trust flag on the poisoning client (temporal trust extension)
    out.append(f'<g class="fl"><path d="M40 {ys[2] + 3}v16M40 {ys[2] + 3}h9l-2 3.5 2 3.5h-9" fill="{P["red"]}" '
               f'stroke="{P["red"]}" stroke-width="1.2" stroke-linejoin="round"/></g>')
    css.append(_kf("fl", dur, _on(.6, "fill-opacity;stroke-opacity", .955), "fill-opacity:0;stroke-opacity:0;"))

    # U-shaped split: client head -> server backbone -> client tail
    hx, hy, tx, ty = 66, 28, 66, 104
    bx, by, bw, bh = 156, 46, 88, 46
    out.append(f'<path d="M{hx + 50} {hy + 11}C140 {hy + 11} 140 {by + 8} {bx} {by + 8}M{bx} {by + bh - 8}C140 '
               f'{by + bh - 8} 140 {ty + 11} {hx + 50} {ty + 11}" fill="none" stroke="{P["muted"]}" '
               f'stroke-opacity=".6" stroke-dasharray="3 3"/>')
    for x, y, lab in ((hx, hy, "head"), (tx, ty, "tail")):
        out.append(f'<rect x="{x}" y="{y}" width="50" height="22" rx="5" fill="{P["blue"]}" fill-opacity=".12" '
                   f'stroke="{P["blue"]}"/>' + text(x + 25, y + 15, lab, P, 10, "blue", "m", "600", "middle"))
    out.append(text(91, hy + 34, "client", P, 8.5, "muted", "m", anchor="middle")
               + text(91, ty - 6, "client", P, 8.5, "muted", "m", anchor="middle"))
    out.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="7" fill="{P["violet"]}" fill-opacity=".12" '
               f'stroke="{P["violet"]}"/><rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="7" '
               f'fill="{P["amber"]}" class="rb"/>'
               + text(bx + bw / 2, by + 20, "server", P, 10, "violet", "m", "600", "middle")
               + text(bx + bw / 2, by + 33, "backbone", P, 10, "violet", "m", "600", "middle"))
    css.append(_kf("rb", dur, [(0, "fill-opacity:0"), (.58, "fill-opacity:0"), (.6, "fill-opacity:.35"),
                               (.68, "fill-opacity:.35"), (.72, "fill-opacity:0"), (1, "fill-opacity:0")],
                   "fill-opacity:0;"))
    # packets of activations travelling the U, one per client update
    for n, (k, t0) in enumerate(((0, .02), (1, .13), (3, .24), (2, .35), (0, .72))):
        y = ys[k] + 11
        path = (f"M36 {y}L{hx} {hy + 11}H{hx + 50}C140 {hy + 11} 140 {by + 8} {bx} {by + 8}H{bx + bw - 20}"
                f"V{by + bh - 8}H{bx}C140 {by + bh - 8} 140 {ty + 11} {hx + 50} {ty + 11}H{hx}")
        bad = k == 2
        t1 = t0 + .15
        out.append(f'<rect x="-4" y="-4" width="8" height="8" rx="2" fill="{P["red" if bad else "blue"]}" '
                   f'fill-opacity="0"><animateMotion dur="{dur}s" repeatCount="indefinite" path="{path}" '
                   f'keyPoints="0;0;1;1" keyTimes="0;{_n(t0)};{_n(t1)};1" calcMode="linear"/>'
                   f'<animate attributeName="fill-opacity" dur="{dur}s" repeatCount="indefinite" values="0;0;1;1;0;0" '
                   f'keyTimes="0;{_n(t0)};{_n(t0 + .01)};{_n(t1 - .01)};{_n(t1)};1"/></rect>')

    # SafeSplit: checkpoint history, a suspicious update is flagged and rolled back
    out.append(text(262, 46, "backbone checkpoints", P, 8.5, "muted", "m"))

    def ck(i, col, mark):
        x = 262 + 24 * i
        m = (f'<path d="M{x + 5} {63}l3 3.5 6-7" fill="none" stroke="{P[col]}" stroke-width="1.8" '
             f'stroke-linecap="round" stroke-linejoin="round"/>' if mark == "ok" else
             text(x + 9, 68, "!", P, 12, col, "m", "700", "middle"))
        return (f'<rect x="{x}" y="54" width="18" height="18" rx="4" fill="{P[col]}" fill-opacity=".15" '
                f'stroke="{P[col]}"/>' + m)
    out.append("".join(ck(i, "green", "ok") for i in range(3)))
    vis = {"c3": (.39, .96), "c4": (.5, .7), "c5": (.87, .96), "sp": (.52, .58), "ra": (.58, .72)}

    def timed(key, body):
        return f'<g visibility="hidden">{_vis(*vis[key], dur)}{body}</g>'
    out.append(timed("c3", ck(3, "green", "ok")) + timed("c4", ck(4, "red", "bad")) + timed("c5", ck(4, "green", "ok")))
    out.append(timed("ra", f'<path d="M371 75Q359 92 347 77" fill="none" stroke="{P["amber"]}" stroke-width="1.8"/>'
                           f'<path d="M344 82l2.5-6 4.5 4" fill="none" stroke="{P["amber"]}" stroke-width="1.8" '
                           f'stroke-linejoin="round"/>' + text(262, 94, "rollback", P, 10, "amber", "m", "700"))
               + timed("sp", text(262, 94, "suspicious", P, 10, "red", "m", "700")))
    out.append(text(262, 116, "backdoor accuracy", P, 8.5, "muted", "m")
               + text(262, 128, "pixel", P, 9.5, "ink", "m") + text(398, 128, "99.9 → 7.54", P, 9.5, "green", "m",
                                                                     "600", "end")
               + text(262, 140, "semantic", P, 9.5, "ink", "m") + text(398, 140, "100 → 0", P, 9.5, "green", "m",
                                                                         "600", "end"))
    return tile(P, "Backdoor attacks and defences", "Backdoor attacks and defences",
                "Group projects: SafeSplit repro + CNN backdoor robustness", False,
                "Animation: four clients send activations through a U-shaped split model (client head, server "
                "backbone, client tail); one client's image carries a red trigger patch, its checkpoint is flagged "
                "suspicious and rolled back to the last benign one, and the client gets a low-trust flag. Numbers "
                "are SafeSplit's backdoor accuracy without vs with the defence, from the reproduction's README.",
                "".join(out), "".join(css))


# ---------------------------------------------------------------- Diffusion model quantization
def diffusion(P):
    dur = 10
    css, out = [], []
    # target picture (abstract landscape) under a noise layer that clears as denoising runs
    ix, iy, n, c = 16, 16, 11, 10
    out.append(f'<clipPath id="im"><rect x="{ix}" y="{iy}" width="{n * c}" height="{n * c}" rx="6"/></clipPath>'
               f'<g clip-path="url(#im)"><rect x="{ix}" y="{iy}" width="{n * c}" height="{n * c}" fill="{P["blue"]}" '
               f'fill-opacity=".22"/><circle cx="{ix + 78}" cy="{iy + 30}" r="14" fill="{P["amber"]}"/>'
               f'<path d="M{ix} {iy + 80}Q{ix + 30} {iy + 52} {ix + 62} {iy + 76}T{ix + 110} {iy + 70}V{iy + 110}H{ix}z" '
               f'fill="{P["green"]}" fill-opacity=".75"/><path d="M{ix} {iy + 96}Q{ix + 50} {iy + 78} {ix + 110} '
               f'{iy + 94}V{iy + 110}H{ix}z" fill="{P["cyan"]}" fill-opacity=".8"/>'
               f'<path d="M{ix + 28} {iy + 74}l-7 12h14z" fill="{P["ink"]}" fill-opacity=".55"/>')
    r = rng(23)
    pal = ["ink", "muted", "blue", "violet", "pink", "amber", "cyan", "green"]
    paths = {}
    for i in range(n):
        for j in range(n):
            key = (int(r() * 5), pal[int(r() * len(pal))])
            paths.setdefault(key, []).append(f"M{ix + i * c} {iy + j * c}h{c}v{c}h-{c}z")
    out.append("".join(f'<path d="{"".join(v)}" fill="{P[col]}" class="z{g}"/>' for (g, col), v in sorted(paths.items())))
    out.append("</g>" f'<rect x="{ix}" y="{iy}" width="{n * c}" height="{n * c}" rx="6" fill="none" stroke="{P["line"]}"/>')
    # four phases: FP16 x30, INT8 x30, INT4 x30 (stays noisy, CLIPScore drops), INT8 x20 (finishes sooner)
    phases = [(30, 0), (30, 0), (30, .5), (20, 0)]
    for g in range(5):
        st = []
        for p, (steps, resid) in enumerate(phases):
            s, D = p * .25, .19 * steps / 30
            left = resid * (g >= 2)
            st += [(s + .005, "fill-opacity:1"), (s + .005 + D * (g + 1) / 5, f"fill-opacity:{f(left)}"),
                   (s + .238, f"fill-opacity:{f(left)}"), (s + .248, "fill-opacity:1")]
        css.append(_kf(f"z{g}", dur, [(0, "fill-opacity:1")] + st + [(1, "fill-opacity:1")], "fill-opacity:0;"))
    # denoising progress bar
    out.append(f'<rect x="{ix}" y="132" width="110" height="4" rx="2" fill="{P["faint"]}"/>'
               )
    st = [(0, "0 1")]
    for p, (steps, _) in enumerate(phases):
        s, D = p * .25, .19 * steps / 30
        st += [(s + .005, "0 1"), (s + .005 + D, "1 1"), (s + .248, "1 1"), (s + .249, "0 1")]
    out.append(f'<g transform="translate({ix} 0)"><g>{_atf("scale", st + [(1, "0 1")], dur)}'
               f'<rect y="132" width="110" height="4" rx="2" fill="{P["violet"]}"/></g></g>')

    # UNet activation histogram, fake-quantized: INT8 (256 levels) looks like FP16, INT4 (16 levels) snaps
    hx0, base, half = 204, 124, 58
    out.append(text(146, 26, "UNet activations", P, 9, "muted", "m"))
    labels = ["FP16 baseline", "INT8 · 256 levels", "INT4 · 16 levels", "INT8 · 256 levels"]
    for p, lab in enumerate(labels):
        css.append(_kf(f"l{p}", dur, [(0, f"fill-opacity:{1 if p == 0 else 0}")]
                       + ([(p * .25, "fill-opacity:0"), (p * .25 + .002, "fill-opacity:1")] if p else [])
                       + [((p + 1) * .25 - .002, "fill-opacity:1"), ((p + 1) * .25, "fill-opacity:0"),
                          (1, "fill-opacity:0")], "" if p == 0 else "fill-opacity:0;"))
        out.append(text(146, 40, lab, P, 10, "amber" if p == 2 else "violet", f"m l{p}", "700"))
    nb, stack = 32, {}
    bars = []
    for i in range(nb):
        v = -1 + (i + .5) / 16
        h = 64 * math.exp(-(v / .36) ** 2 / 2) + 1.5
        q = max(-8, min(7, round(v * 7))) / 7
        off = stack.get(q, 0)
        stack[q] = off + h
        bars.append((hx0 + v * half - 1.5, h, hx0 + q * half - 1.5, off))
    k = 66 / max(stack.values())  # the whole plot squashes in the INT4 phase so the stacks stay inside it
    hb = []
    for i, (x, h, xq, off) in enumerate(bars):
        sn = f"{f(xq - x)} {f(-off)}"
        hb.append(f'<rect x="{f(x)}" y="{f(base - h)}" width="3" height="{f(h)}">'
                  + _atf("translate", [(0, "0 0"), (.5, "0 0"), (.53, sn), (.72, sn), (.75, "0 0"), (1, "0 0")], dur)
                  + "</rect>")
    sq = f"1 {k:.3f}"
    out.append(f'<g transform="translate(0 {base})"><g>'
               + _atf("scale", [(0, "1 1"), (.5, "1 1"), (.53, sq), (.72, sq), (.75, "1 1"), (1, "1 1")], dur)
               + f'<g transform="translate(0 -{base})" fill="{P["violet"]}" fill-opacity=".8">{"".join(hb)}</g></g></g>')
    ticks = "".join(f"M{f(hx0 + q / 7 * half)} {base + 2}v4" for q in range(-8, 8))
    out.append(f'<line x1="{hx0 - half - 4}" y1="{base}" x2="{hx0 + half + 4}" y2="{base}" stroke="{P["line"]}"/>'
               f'<path d="{ticks}" stroke="{P["amber"]}" stroke-width="1.4" class="tk"/>')
    css.append(_kf("tk", dur, _on(.5, "stroke-opacity", .74), "stroke-opacity:0;"))

    # measured results (notebook): latency per image and CLIPScore, SD v1.5 on one GPU
    out.append(text(274, 46, "mode", P, 8.5, "muted", "m") + text(366, 46, "s/img", P, 8.5, "muted", "m", anchor="end")
               + text(398, 46, "CLIP", P, 8.5, "muted", "m", anchor="end"))
    rows = [("FP16 ×30", 4.98, "33.6"), ("INT8 ×30", 5.31, "33.6"), ("INT4 ×30", 5.44, "18.9"),
            ("INT8 ×20", 3.62, "33.2")]
    for p, (lab, lat, clip) in enumerate(rows):
        y = 62 + p * 20
        css.append(_kf(f"h{p}", dur, [(0, f"fill-opacity:{.16 if p == 0 else 0}")]
                       + ([(p * .25, "fill-opacity:0"), (p * .25 + .004, "fill-opacity:.16")] if p else [])
                       + [((p + 1) * .25 - .004, "fill-opacity:.16"), ((p + 1) * .25, "fill-opacity:0"),
                          (1, "fill-opacity:0")], "fill-opacity:0;"))
        out.append(f'<rect x="270" y="{y - 11}" width="132" height="20" rx="5" fill="{P["violet"]}" class="h{p}"/>'
                   + text(274, y, lab, P, 9.5, "ink", "m", "600")
                   + text(366, y, f"{lat:.2f}", P, 9.5, "ink", "m", anchor="end")
                   + text(398, y, clip, P, 9.5, "red" if p == 2 else "ink", "m", anchor="end")
                   + f'<rect x="274" y="{y + 3}" width="{f(lat / 5.44 * 124)}" height="3" rx="1.5" '
                     f'fill="{P["green" if p == 3 else "amber" if p == 2 else "blue"]}" fill-opacity=".7"/>')
    out.append(text(274, 142, "fewer steps: −27 % latency", P, 9, "green", "m ft", "600"))
    css.append(_kf("ft", dur, _on(.75, "fill-opacity", .985), "fill-opacity:0;"))
    return tile(P, "Diffusion model quantization", "Diffusion model quantization",
                "Group project: Q-Diffusion-style PTQ on Stable Diffusion 1.5", False,
                "Animation: a picture denoises out of random noise four times, as FP16, INT8, INT4 and INT8 with "
                "fewer steps, while a histogram of UNet activations stays smooth at 8 bits and snaps onto 16 levels "
                "at 4 bits. The table gives the notebook's measured seconds per image and CLIPScore for each mode: "
                "fake quantization alone is slower than FP16, INT4 loses quality, and cutting to 20 steps gives a "
                "27 % latency cut.", "".join(out), "".join(css))


NEW_CARDS = {"tiles/tictactoe-evolved": tictactoe, "tiles/guess-who": guess_who,
             "tiles/backdoor-robustness": backdoor, "tiles/diffusion-quantization": diffusion}
