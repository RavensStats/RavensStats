"""Contribution snake that grows as it eats, plus the data and page for the playable version.

  GITHUB_TOKEN=... python tools/build_snake.py dist        (what the Action runs)
  python tools/build_snake.py dist --data cal.json          (offline, from a saved calendar)

Writes dist/snake-{light,dark}.svg, dist/contributions.json and the game page (game/ copied in).
The body is the route itself drawn with a moving dash window: the window's far end is the head,
its length is the snake's length, and it lengthens one cell per day eaten (the tail waits a step).
"""
import json
import os
import shutil
import sys
import urllib.request
from collections import deque
from datetime import date
from pathlib import Path

from common import DARK, LIGHT, doc, f, text

ROOT = Path(__file__).resolve().parent.parent
LOGIN = "RavensStats"
QUERY = ('query($l:String!){user(login:$l){contributionsCollection{contributionCalendar{totalContributions '
         'weeks{contributionDays{date contributionCount contributionLevel weekday}}}}}}')
LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
GREENS = {"light": ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"],
          "dark": ["#21262d", "#0e4429", "#006d32", "#26a641", "#39d353"]}

PITCH, CELL, X0, Y0 = 14, 11, 62, 50
SPEED = 8           # cells per second
START_LEN = 3       # segments
MAX_LEN = 60        # the SVG caps growth so the grid stays readable; the playable game does not


def fetch(token):
    req = urllib.request.Request("https://api.github.com/graphql",
                                 json.dumps({"query": QUERY, "variables": {"l": LOGIN}}).encode(),
                                 {"Authorization": f"bearer {token}", "User-Agent": "contribution-snake"})
    cal = json.load(urllib.request.urlopen(req, timeout=30))["data"]["user"]["contributionsCollection"]
    return cal["contributionCalendar"]


def grid(cal):
    """{(col, row): (date, count, level)} for every day in the calendar."""
    return {(c, d["weekday"]): (d["date"], d["contributionCount"], LEVEL[d["contributionLevel"]])
            for c, w in enumerate(cal["weeks"]) for d in w["contributionDays"]}


def route(cells, start):
    """Greedy: walk to the nearest uneaten day (BFS over existing cells). Returns steps and eat indices."""
    food = {k for k, v in cells.items() if v[1] > 0}
    pos, steps, eats = start, [start], []
    if pos in food:
        food.discard(pos)
        eats.append(0)
    while food:
        prev = {pos: None}
        q = deque([pos])
        hit = None
        while q:
            cur = q.popleft()
            if cur in food:
                hit = cur
                break
            c, r = cur
            for nxt in ((c, r - 1), (c + 1, r), (c, r + 1), (c - 1, r)):
                if nxt in cells and nxt not in prev:
                    prev[nxt] = cur
                    q.append(nxt)
        path = []
        while hit != pos:
            path.append(hit)
            hit = prev[hit]
        steps += path[::-1]
        pos = steps[-1]
        food.discard(pos)
        eats.append(len(steps) - 1)
    return steps, eats


def centre(cell):
    c, r = cell
    return X0 + c * PITCH + CELL / 2, Y0 + r * PITCH + CELL / 2


def render(P, cal, cells, steps, eats):
    dt = 1 / SPEED
    t_end = (len(steps) - 1) * dt
    cycle = t_end + 3.0
    total = (len(steps) - 1) * PITCH
    big = total + 2000

    # snake length L(t): grows by one cell over the step after each meal, capped at MAX_LEN
    tk = [i * dt for i in eats]
    knots = sorted({0.0, t_end, *tk, *(min(t + dt, t_end) for t in tk)})

    def length(t):
        grown = sum(min(max((t - e) / dt, 0), 1) for e in tk)
        return PITCH * (START_LEN + min(grown, MAX_LEN - START_LEN))
    keys = [k / cycle for k in knots] + [1.0]
    Ls = [length(t) for t in knots]
    offs = [L - PITCH * SPEED * t for L, t in zip(Ls, knots)]
    Ls.append(Ls[-1])
    offs.append(offs[-1])
    kt = ";".join(f"{k:.5f}" for k in keys)
    dash = ";".join(f"{f(L)} {f(big)}" for L in Ls)
    off = ";".join(f(o) for o in offs)

    pts = [centre(s) for s in steps]
    d = f"M{f(pts[0][0])} {f(pts[0][1])}" + "".join(f"L{f(x)} {f(y)}" for x, y in pts[1:])

    out = []
    for m, lab in month_labels(cal):
        out.append(text(X0 + m * PITCH, Y0 - 8, lab, P, 9.5, "muted", "m"))
    for r, lab in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append(text(X0 - 8, Y0 + r * PITCH + 9, lab, P, 9.5, "muted", "m", anchor="end"))
    greens = GREENS[P["name"]]
    eat_at = {steps[i]: i * dt for i in eats}
    for (c, r), (_, n, lv) in sorted(cells.items()):
        x, y = X0 + c * PITCH, Y0 + r * PITCH
        anim = ""
        if n > 0:
            u = eat_at[(c, r)] / cycle
            anim = (f'<animate attributeName="fill" calcMode="discrete" values="{greens[lv]};{greens[0]}" '
                    f'keyTimes="0;{u:.5f}" dur="{f(cycle)}s" repeatCount="indefinite"/>')
        out.append(f'<rect x="{x}" y="{y}" width="{CELL}" height="{CELL}" rx="2" fill="{greens[lv if n else 0]}">'
                   f'{anim}</rect>')

    def body(width, col, op):
        return (f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{width}" '
                f'stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="{f(PITCH * START_LEN)} {f(big)}">'
                f'<animate attributeName="stroke-dasharray" values="{dash}" keyTimes="{kt}" dur="{f(cycle)}s" '
                f'repeatCount="indefinite"/><animate attributeName="stroke-dashoffset" values="{off}" keyTimes="{kt}" '
                f'dur="{f(cycle)}s" repeatCount="indefinite"/></path>')
    head = (f'<g><circle r="6.5" fill="{P["pink"]}"/><circle cx="2.5" cy="-2.6" r="1.4" fill="#fff"/>'
            f'<circle cx="2.5" cy="2.6" r="1.4" fill="#fff"/>'
            f'<animateMotion path="{d}" dur="{f(cycle)}s" repeatCount="indefinite" rotate="auto" calcMode="linear" '
            f'keyPoints="0;1;1" keyTimes="0;{t_end / cycle:.5f};1"/></g>')
    fade = (f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;{(t_end + 1.4) / cycle:.5f};'
            f'{(t_end + 2.6) / cycle:.5f};1" dur="{f(cycle)}s" repeatCount="indefinite"/>')
    out.append(f'<g>{body(10, P["violet"], ".95")}{body(4, P["card"], ".35")}{head}{fade}</g>')

    total_c = cal["totalContributions"]
    out.append(text(24, 26, "CONTRIBUTION SNAKE", P, 11, "violet", "m", weight="600", extra=' letter-spacing="1.6"')
               + text(186, 26, f"{total_c:,} contributions in the last year · it grows with every day it eats",
                      P, 11, "muted", "m")
               + text(X0, Y0 + 7 * PITCH + 24, "▶ play it yourself: ravensstats.github.io/RavensStats", P, 10.5,
                      "ink", "m"))
    w, h = 840, Y0 + 7 * PITCH + 40
    return doc(w, h, P, "Contribution snake",
               f"A snake crawls over the last year of GitHub contributions ({total_c:,} in total), eating each day "
               f"with a commit and growing longer with every one.", "".join(out))


def month_labels(cal):
    seen, out = set(), []
    for c, w in enumerate(cal["weeks"]):
        d0 = date.fromisoformat(w["contributionDays"][0]["date"])
        key = (d0.year, d0.month)
        if key not in seen and d0.day <= 7 and c < len(cal["weeks"]) - 2:
            seen.add(key)
            out.append((c, d0.strftime("%b")))
    return out


if __name__ == "__main__":
    dist = Path(sys.argv[1])
    dist.mkdir(parents=True, exist_ok=True)
    if "--data" in sys.argv:
        cal = json.loads(Path(sys.argv[sys.argv.index("--data") + 1]).read_text())
    else:
        cal = fetch(os.environ["GITHUB_TOKEN"])
    cells = grid(cal)
    steps, eats = route(cells, (0, 3) if (0, 3) in cells else min(cells))
    for P in (LIGHT, DARK):
        svg = render(P, cal, cells, steps, eats)
        (dist / f"snake-{P['name']}.svg").write_text(svg, encoding="utf-8")
        print(f"snake-{P['name']}.svg {len(svg.encode()) / 1000:.1f} KB, {len(steps)} steps, {len(eats)} meals")
    weeks = [[{"d": d["date"], "c": d["contributionCount"], "l": LEVEL[d["contributionLevel"]], "w": d["weekday"]}
              for d in w["contributionDays"]] for w in cal["weeks"]]
    (dist / "contributions.json").write_text(json.dumps({"login": LOGIN, "total": cal["totalContributions"],
                                                         "generated": date.today().isoformat(), "weeks": weeks}))
    shutil.copytree(ROOT / "game", dist, dirs_exist_ok=True)
    (dist / ".nojekyll").write_text("")
