"""DDP vs FSDP scaling tile (410x200), drawn from the demo's real measurements (results/main of ddp-fsdp-scaling-demo)."""
from common import f, text
from tiles import tile

# tokens/s (median, steps 10-249) and peak GiB per GPU, 4x A100-SXM4-80GB, Qwen2.5-0.5B, global batch 32 x 512 tokens
TPUT = {"ddp": (23181, 46026, 85975), "fsdp": (23365, 45264, 87220)}
EFF4 = {"ddp": "92.7 %", "fsdp": "93.3 %"}
MEM4 = {"ddp": 22.93, "fsdp": 15.44}
DUR = 9


def _grow(y0, h, begin_t=0.0):
    """Bar rising from the baseline y0 to height h, held, then reset (SMIL; static attributes show the full bar)."""
    k = f"0;{begin_t:.2f};{begin_t + .3:.2f};.94;1"
    hv = f"0;0;{f(h)};{f(h)};0"
    yv = f"{f(y0)};{f(y0)};{f(y0 - h)};{f(y0 - h)};{f(y0)}"
    return (f'<animate attributeName="height" dur="{DUR}s" repeatCount="indefinite" values="{hv}" keyTimes="{k}"/>'
            f'<animate attributeName="y" dur="{DUR}s" repeatCount="indefinite" values="{yv}" keyTimes="{k}"/>')


def _fade(t0):
    return (f'<animate attributeName="fill-opacity" dur="{DUR}s" repeatCount="indefinite" values="0;0;1;1;0" '
            f'keyTimes="0;{t0:.2f};{t0 + .06:.2f};.94;1"/>')


def ddp_fsdp(P):
    out = [text(14, 20, "tokens / s, global batch fixed", P, 9, "muted", "m")]
    base, hmax, top = 118, 84, 87220
    col = {"ddp": "blue", "fsdp": "violet"}
    for g, x0 in enumerate((22, 96, 170)):
        for i, s in enumerate(("ddp", "fsdp")):
            h = TPUT[s][g] / top * hmax
            x = x0 + i * 28
            t0 = .04 + g * .12 + i * .03
            out.append(f'<rect x="{x}" y="{f(base - h)}" width="24" height="{f(h)}" rx="3" fill="{P[col[s]]}" '
                       f'fill-opacity=".85">{_grow(base, h, t0)}</rect>')
        out.append(text(x0 + 26, 132, f"{(1, 2, 4)[g]} GPU" + ("" if g == 0 else "s"), P, 9.5, "muted", "m",
                        anchor="middle"))
    out.append(f'<line x1="14" y1="{base}" x2="250" y2="{base}" stroke="{P["line"]}"/>')
    for i, s in enumerate(("ddp", "fsdp")):
        x = 170 + i * 28 + 12
        out.append(f'<text x="{x}" y="{f(base - TPUT[s][2] / top * hmax - 5)}" class="m" font-size="7.5" '
                   f'text-anchor="middle" fill="{P[col[s]]}" fill-opacity="0" font-weight="600">{EFF4[s]}{_fade(.55)}</text>')
    # legend + memory panel
    for i, (s, lab) in enumerate((("ddp", "DDP"), ("fsdp", "FSDP"))):
        out.append(f'<rect x="{22 + i * 52}" y="32" width="8" height="8" rx="2" fill="{P[col[s]]}"/>'
                   + text(34 + i * 52, 40, lab, P, 9.5, "ink", "m"))
    out.append(text(262, 50, "peak GiB per GPU (4 GPUs)", P, 9, "muted", "m"))
    for i, s in enumerate(("ddp", "fsdp")):
        y, w = 58 + i * 30, MEM4[s] / 25 * 96
        out.append(text(262, y + 9, s.upper(), P, 9.5, "ink", "m")
                   + f'<rect x="262" y="{y + 13}" width="{f(w)}" height="11" rx="3" fill="{P[col[s]]}" fill-opacity=".85">'
                     f'<animate attributeName="width" dur="{DUR}s" repeatCount="indefinite" values="0;0;{f(w)};{f(w)};0" '
                     f'keyTimes="0;.45;.7;.94;1"/></rect>'
                   + text(262 + w + 5, y + 22, f"{MEM4[s]:.1f}", P, 9.5, s == "ddp" and "blue" or "violet", "m", "600"))
    out.append(text(262, 126, "FSDP: 33 % less memory,", P, 9, "muted", "m") + text(262, 138, "throughput within 2 %", P, 9, "muted", "m"))
    return tile(P, "DDP vs FSDP scaling",
                "DDP vs FSDP scaling", "Qwen2.5-0.5B · 1 to 4 GPUs · NCCL", True,
                "Animation: grouped bars grow for DDP and FSDP throughput at 1, 2 and 4 GPUs (23k to 86k and 87k tokens per "
                "second, about 93 % scaling efficiency at 4 GPUs for both), then bars for peak memory per GPU at 4 GPUs "
                "(DDP 22.9 GiB, FSDP 15.4 GiB). Drawn from the demo's real measurements on 4 A100 GPUs.",
                "".join(out))


NEW_CARDS = {"tiles/ddp-fsdp-scaling": ddp_fsdp}
