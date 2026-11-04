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
    """Play it like the game: one step at a time, never into a cell the body covers.

    Each step heads for the nearest uneaten day through free cells, but only takes a move that
    leaves the head enough open space to fit the body (so it can't wall itself in); with no
    meal reachable it takes the roomiest move and waits for the tail to clear.
    Returns steps (head cells) and eats (step indices of meals). Stops early only if trapped.
    """
    food = {k for k, v in cells.items() if v[1] > 0}
    steps, eats = [start], []
    if start in food:
        food.discard(start)
        eats.append(0)

    def body_len():
        return min(START_LEN + len(eats), MAX_LEN)

    def blocked():
        # the drawn body spans body_len() steps behind the head, i.e. body_len() + 1 cells
        return set(steps[-(body_len() + 1):])

    def nbrs(cell):
        c, r = cell
        return [n for n in ((c, r - 1), (c + 1, r), (c, r + 1), (c - 1, r)) if n in cells]

    def room(cell, wall):
        seen, q = {cell}, deque([cell])
        while q:
            for n in nbrs(q.popleft()):
                if n not in seen and n not in wall:
                    seen.add(n)
                    q.append(n)
        return len(seen)

    def first_step_to_food(head, wall):
        prev, q = {head: None}, deque([head])
        while q:
            cur = q.popleft()
            if cur in food and cur != head:
                while prev[cur] != head:
                    cur = prev[cur]
                return cur
            for n in nbrs(cur):
                if n not in prev and n not in wall:
                    prev[n] = cur
                    q.append(n)
        return None

    def can_reach_tail(m):
        """After moving to m, can the head still get back to its own tail? Then it can never be trapped."""
        n = min(START_LEN + len(eats) + (m in food), MAX_LEN)
        body = (steps + [m])[-(n + 1):]
        tail, wall = body[0], set(body[1:-1])
        if len(steps) + 1 <= n + 1:  # still unrolling: the tail isn't moving yet, so it needs open space
            return room(m, set(body[:-1])) >= n + 2
        if m == tail:
            return True
        seen, q = {m}, deque([m])
        while q:
            cur = q.popleft()
            for nb in nbrs(cur):
                if nb == tail:
                    return True
                if nb not in seen and nb not in wall:
                    seen.add(nb)
                    q.append(nb)
        return False

    limit = 40 * len(cells)
    while food and len(steps) < limit:
        head, wall = steps[-1], blocked()
        moves = [n for n in nbrs(head) if n not in wall]
        if not moves:
            break  # trapped: the run ends here
        wanted = first_step_to_food(head, wall)
        safe = [m for m in moves if can_reach_tail(m)]
        stalled = len(steps) - (eats[-1] if eats else 0) > 2 * len(cells)
        if wanted in safe or (stalled and wanted):  # long stall: go for it (still never into the body)
            nxt = wanted
        elif safe:  # chase the tail until a meal is safely reachable, drifting towards food
            nxt = min(safe, key=lambda m: min(abs(m[0] - f[0]) + abs(m[1] - f[1]) for f in food))
        else:
            nxt = max(moves, key=lambda m: room(m, wall))
        steps.append(nxt)
        if nxt in food:
            food.discard(nxt)
            eats.append(len(steps) - 1)
    return steps, eats


def check_no_overlap(steps, eats):
    """Every frame: the body's cells (head back body-length steps) must all be distinct."""
    meals = 0
    for i in range(len(steps)):
        while meals < len(eats) and eats[meals] <= i:
            meals += 1
        n = min(START_LEN + meals, MAX_LEN)
        window = steps[max(0, i - n):i + 1]
        assert len(set(window)) == len(window), f"snake crosses itself at step {i}"


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
        if (c, r) in eat_at:  # a trapped run can leave a few days uneaten; those stay green
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
    check_no_overlap(steps, eats)
    left = sum(1 for v in cells.values() if v[1] > 0) - len(eats)
    if left:
        print(f"note: snake trapped with {left} days uneaten")
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
