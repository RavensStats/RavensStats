"""Palette, frame and text helpers shared by every card.

Colours follow GitHub's Primer scale so the cards sit naturally on the profile page in both
themes. Every card is written twice (light, dark) from the same function: a card takes the
palette P and returns its SVG body, never a hard-coded colour.
"""
import math
from xml.sax.saxutils import escape

LIGHT = dict(name="light", bg="#ffffff", card="#f6f8fa", line="#d0d7de", ink="#1f2328",
             muted="#59636e", faint="#e8ecf0", blue="#0969da", violet="#8250df",
             green="#1a7f37", amber="#bf8700", pink="#bf3989", red="#cf222e", cyan="#1b7c83",
             night="#0b1d3a")
DARK = dict(name="dark", bg="#0d1117", card="#161b22", line="#30363d", ink="#e6edf3",
            muted="#9198a1", faint="#21262d", blue="#4493f8", violet="#ab7df8",
            green="#3fb950", amber="#d29922", pink="#f778ba", red="#f85149", cyan="#39c5cf",
            night="#0b1d3a")
ACCENTS = ("blue", "violet", "green", "amber", "pink", "cyan")

SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI','Noto Sans',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"

BASE_CSS = (f".s{{font-family:{SANS}}}.m{{font-family:{MONO}}}"
            "@media (prefers-reduced-motion:reduce){*{animation:none!important}}")


def esc(s):
    return escape(s, {'"': "&quot;"})


def f(x):
    """Compact number for coordinates."""
    return f"{x:.1f}".rstrip("0").rstrip(".")


def doc(w, h, P, title, desc, body, css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="t d">'
            f'<title id="t">{esc(title)}</title><desc id="d">{esc(desc)}</desc>'
            f'<style>{BASE_CSS}{css}</style>'
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="{P["card"]}" '
            f'stroke="{P["line"]}"/>{body}</svg>')


def text(x, y, s, P, size=13, color="ink", cls="s", weight=None, anchor=None, extra=""):
    a = f' font-weight="{weight}"' if weight else ""
    a += f' text-anchor="{anchor}"' if anchor else ""
    return (f'<text x="{f(x)}" y="{f(y)}" class="{cls}" font-size="{size}" '
            f'fill="{P[color]}"{a}{extra}>{esc(s)}</text>')


def wrap(s, n):
    lines, cur = [], ""
    for w in s.split():
        if cur and len(cur) + 1 + len(w) > n:
            lines.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return lines + [cur]


def chips(x, y, labels, P, size=11):
    out = []
    for lab in labels:
        w = len(lab) * size * 0.62 + 18
        out.append(f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="22" rx="11" '
                   f'fill="{P["faint"]}" stroke="{P["line"]}"/>'
                   + text(x + w / 2, y + 15, lab, P, size, "ink", "m", anchor="middle"))
        x += w + 6
    return "".join(out)


def badge(x, y, private, P):
    lab, col = ("PRIVATE REPO", "amber") if private else ("PUBLIC REPO", "green")
    w = len(lab) * 6.3 + 24
    return (f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="18" rx="9" fill="{P["card"]}" '
            f'stroke="{P[col]}" stroke-opacity=".6"/>'
            f'<circle cx="{f(x + 10)}" cy="{f(y + 9)}" r="3" fill="{P[col]}"/>'
            + text(x + 17, y + 13, lab, P, 9.5, col, "m", weight="600", extra=' letter-spacing=".6"'))


def hero_text(P, kicker, title, body, tags, foot, accent, private):
    """Left column of an 840x300 hero card."""
    out = [badge(32, 26, private, P),
           text(32, 70, kicker, P, 11, accent, "m", weight="600", extra=' letter-spacing="1.6"')]
    y = 102
    for line in title:
        out.append(text(32, y, line, P, 25, "ink", weight="700"))
        y += 30
    y += 2
    for line in wrap(body, 54):
        out.append(text(32, y, line, P, 13.5, "muted"))
        y += 20
    out.append(chips(32, 236, tags, P))
    out.append(text(32, 282, foot, P, 10, "muted", "m"))
    return "".join(out)


def tile_frame(P, title, sub, private, body, w=410, h=200):
    """Viz area on top (clipped to y < 146), title strip below."""
    return (f'<clipPath id="vz"><rect x="1" y="1" width="{w - 2}" height="145" rx="13"/></clipPath>'
            f'<g clip-path="url(#vz)">{body}</g>'
            f'<line x1="1" y1="146" x2="{w - 1}" y2="146" stroke="{P["line"]}"/>'
            + text(18, 172, title, P, 15, "ink", weight="700")
            + text(18, 190, sub, P, 11.5, "muted")
            + badge(w - 118, 12, private, P))


def polyline(pts):
    return "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)


def rng(seed):
    """Tiny deterministic LCG so regenerated cards don't change between builds."""
    state = [seed]

    def r():
        state[0] = (state[0] * 1103515245 + 12345) % 2 ** 31
        return state[0] / 2 ** 31
    return r


def hexagon(cx, cy, r, squash=1.0):
    return " ".join(f"{f(cx + r * math.cos(math.radians(60 * k + 30)))},"
                    f"{f(cy + r * squash * math.sin(math.radians(60 * k + 30)))}" for k in range(6))
