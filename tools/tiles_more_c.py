"""DDP vs FSDP scaling tile (410x200), drawn from the demo's real measurements (results/nvlink of ddp-fsdp-scaling-demo):
peak GiB per GPU vs model size at 4x A100-SXM4-80GB (NVLink), plus the profiler's share of communication time hidden behind compute.
The planned NVLink-vs-PCIe panel is not drawn because the PCIe arm did not run (no stock)."""
from common import f, text
from tiles import tile

SIZES = ("0.5B", "1.5B", "3B", "7B")
# peak GiB per GPU, 4 GPUs, global batch 32 x 512 (3B and 7B with activation checkpointing, micro-batch 4); None = OOM
MEM = {"ddp": (22.93, 47.5, 65.1, None), "fsdp_zero2": (16.1, 27.1, 24.6, 54.2), "fsdp": (15.44, 24.6, 19.4, 42.0)}
LAB = {"ddp": "DDP", "fsdp_zero2": "ZeRO-2", "fsdp": "ZeRO-3"}
COL = {"ddp": "blue", "fsdp_zero2": "green", "fsdp": "violet"}
# profiler, 7B ZeRO-3, rank-0 GPU: comm busy 40.8 % of the step window, 91 % of it overlapped with compute
COMM_SHARE, COMM_OVERLAP = 40.8, 0.91
DUR = 9
def ddp_fsdp(P):
    out = [text(14, 18, "peak GiB per GPU vs model size", P, 9, "muted", "m")]
    x0, dx, yb, yt = 40, 62, 124, 48          # x of first size, spacing, baseline (0 GiB), 80 GiB line
    sc = (yb - yt) / 80
    xs = [x0 + i * dx for i in range(4)]
    out.append(f'<line x1="30" y1="{yb}" x2="236" y2="{yb}" stroke="{P["line"]}"/>')
    out.append(f'<line x1="30" y1="{yt}" x2="236" y2="{yt}" stroke="{P["red"]}" stroke-dasharray="3 3" stroke-opacity=".7"/>')
    out.append(text(32, yt + 10, "80 GB GPU", P, 8, "red", "m"))
    for x, sz in zip(xs, SIZES):
        out.append(text(x, yb + 13, sz, P, 9, "muted", "m", anchor="middle"))
    for s in ("ddp", "fsdp_zero2", "fsdp"):
        pts = [(x, yb - m * sc) for x, m in zip(xs, MEM[s]) if m is not None]
        d = "M" + " L".join(f"{f(x)} {f(y)}" for x, y in pts)
        out.append(f'<path d="{d}" fill="none" stroke="{P[COL[s]]}" stroke-width="2" stroke-linejoin="round" pathLength="1" '
                   f'stroke-dasharray="1" stroke-dashoffset="0"><animate attributeName="stroke-dashoffset" dur="{DUR}s" '
                   f'repeatCount="indefinite" values="1;1;0;0;1" keyTimes="0;.04;.4;.94;1"/></path>')
        for x, y in pts:
            out.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="2.6" fill="{P[COL[s]]}"/>')
    # DDP wall at 7B
    wx = xs[3]
    out.append(f'<path d="M{wx - 5} {yt - 5 + 6} l10 10 m0 -10 l-10 10" stroke="{P["blue"]}" stroke-width="2.2" fill="none"/>'
               + text(wx - 8, yt + 20, "DDP: OOM", P, 8.5, "blue", "m", "600", anchor="end"))
    for i, s in enumerate(("ddp", "fsdp_zero2", "fsdp")):
        out.append(f'<rect x="{20 + i * 58}" y="26" width="7" height="7" rx="2" fill="{P[COL[s]]}"/>'
                   + text(30 + i * 58, 33, LAB[s], P, 8.5, "ink", "m"))
    # right panel: communication hidden behind compute (profiler)
    px, pw = 262, 128
    out.append(text(px, 50, "7B ZeRO-3, NCCL time", P, 9, "muted", "m"))
    out.append(text(px, 62, "(profiler, 3 steps)", P, 8, "muted", "m"))
    wc = COMM_SHARE / 100 * pw / 0.5          # bar spans 50 % of the step
    wo = wc * COMM_OVERLAP
    out.append(f'<rect x="{px}" y="72" width="{pw}" height="14" rx="3" fill="{P["faint"]}"/>'
               f'<rect x="{px}" y="72" width="{f(wo)}" height="14" rx="3" fill="{P["violet"]}" fill-opacity=".85">'
               f'<animate attributeName="width" dur="{DUR}s" repeatCount="indefinite" values="0;0;{f(wo)};{f(wo)};0" keyTimes="0;.4;.6;.94;1"/></rect>'
               f'<rect x="{f(px + wo)}" y="72" width="{f(wc - wo)}" height="14" fill="{P["amber"]}" fill-opacity=".9"/>')
    out.append(text(px, 100, f"{COMM_SHARE:.0f} % of step is NCCL;", P, 9, "ink", "m"))
    out.append(text(px, 112, f"{COMM_OVERLAP * 100:.0f} % overlapped with compute", P, 9, "ink", "m"))
    out.append(text(px, 128, "NVLink only; PCIe arm not run", P, 8, "muted", "m"))
    return tile(P, "DDP vs FSDP scaling",
                "DDP vs FSDP scaling", "Qwen2.5 0.5B to 7B · 4 GPUs · NCCL", True,
                "Animation: lines draw peak memory per GPU against model size from 0.5B to 7B on four A100 GPUs for DDP, FSDP "
                "ZeRO-2 and FSDP ZeRO-3. DDP reaches 65 GiB at 3B and runs out of the 80 GB at 7B, while ZeRO-2 and ZeRO-3 train 7B "
                "at 54 and 42 GiB. A side bar shows that about 91 % of NCCL time overlaps with compute in a profiled 7B ZeRO-3 step. "
                "Drawn from the demo's real measurements.",
                "".join(out))


NEW_CARDS = {"tiles/ddp-fsdp-scaling": ddp_fsdp}
