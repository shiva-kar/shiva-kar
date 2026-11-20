#!/usr/bin/env python3
"""GitHub activity statistics, streak, and language distribution component."""
from datetime import date

import config
import kit
from kit import BLUE, CARD2, EDGE, GREEN, MUTED, ORANGE, card, label, t

LANG_COL = {
    "TypeScript": "#3178c6",
    "JavaScript": "#f1e05a",
    "Java": "#f89820",
    "C": "#a8b9cc",
    "Python": "#3572a5",
    "C++": "#f34b7d",
    "Shell": "#89e051",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
}


def stats(w, data):
    m = w < 600
    pad = 20 if m else 28
    cal = data.get("calendar", {})
    tiles = [
        ("CONTRIBUTIONS", f"{cal.get('total', 0):,}"),
        ("PULL REQUESTS", str(data.get("prs_total", 0))),
        ("ISSUES", str(data.get("issues_total", 0))),
        ("STARS EARNED", str(data.get("stars", 0))),
        ("FOLLOWERS", str(data.get("followers", 0)))
    ]
    body = [label(pad, pad + 10, f"GITHUB | @{config.USER.upper()}", BLUE, 11.5)]
    cols, gap = (2 if m else 5), 10
    twid = (w - 2 * pad - gap * (cols - 1)) / cols
    y0 = pad + 26
    for i, (lab, val) in enumerate(tiles):
        r, c = divmod(i, cols)
        x, y = pad + c * (twid + gap), y0 + r * 66
        body.append(f'<rect x="{x:.1f}" y="{y}" width="{twid:.1f}" height="56" rx="10" fill="{CARD2}" stroke="{EDGE}"/>')
        body.append(t(x + 14, y + 26, val, "bodyb", 22, "#ffffff"))
        body.append(t(x + 14, y + 44, lab, "mono", 11, MUTED, ls=1.2))
    y = y0 + ((len(tiles) + cols - 1) // cols) * 66 + 8
    weeks, col = [], None
    for d in cal.get("days", []):
        wd = (date.fromisoformat(d["date"]).weekday() + 1) % 7
        if col is None or wd == 0:
            col = [None] * 7
            weeks.append(col)
        col[wd] = d
    nweeks = 26 if m else 53
    weeks = weeks[-nweeks:]
    sbox = 0 if m else 160
    pitch = (w - 2 * pad - sbox - (0 if m else 14)) / nweeks
    # Authentic GitHub Green Heatmap palette
    lv = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    for wi, wk in enumerate(weeks):
        for di, d in enumerate(wk):
            if d:
                body.append(f'<rect x="{pad + wi * pitch:.1f}" y="{y + di * pitch:.1f}" width="{pitch - 2.6:.1f}" '
                            f'height="{pitch - 2.6:.1f}" rx="2" fill="{lv[d["level"]]}"/>')
    hm_h = 7 * pitch
    cur = cal.get("current_streak", 0)
    unit = "DAY" if cur == 1 else "DAYS"
    if m:
        y += hm_h + 14
        body.append(f'<rect x="{pad}" y="{y}" width="{w - 2 * pad}" height="64" rx="10" fill="{CARD2}" stroke="{EDGE}"/>')
        body.append(label(pad + 14, y + 20, "CURRENT STREAK", GREEN, 11))
        body.append(t(pad + 14, y + 48, f"{cur} {unit}", "bodyb", 20, "#ffffff"))
        body.append(t(w - pad - 14, y + 30, f"LONGEST {cal.get('longest_streak', 0)}", "mono", 11, MUTED, "end", 1))
        body.append(t(w - pad - 14, y + 48, f"ACTIVE {cal.get('active_days', 0)}", "mono", 11, MUTED, "end", 1))
        y += 64 + 16
    else:
        sx, bh = w - pad - sbox, max(hm_h, 88)
        body.append(f'<rect x="{sx}" y="{y}" width="{sbox}" height="{bh:.1f}" rx="10" fill="{CARD2}" stroke="{EDGE}"/>')
        body.append(label(sx + 14, y + 22, "CURRENT STREAK", GREEN, 11))
        body.append(t(sx + 14, y + 50, f"{cur} {unit}", "bodyb", 21, "#ffffff"))
        body.append(t(sx + 14, y + 70, f"LONGEST {cal.get('longest_streak', 0)}", "mono", 11, MUTED, ls=1))
        body.append(t(sx + 14, y + 84, f"ACTIVE {cal.get('active_days', 0)}", "mono", 11, MUTED, ls=1))
        y += bh + 20
    basis = "REPO" if data.get("languages_basis") == "repos" else "CODE SIZE"
    body.append(label(pad, y + 8, f"TOP LANGUAGES BY {basis}", ORANGE, 11.5))
    y += 20
    languages = data.get("languages", [])
    total = sum(l["pct"] for l in languages) or 1
    bw = w - 2 * pad
    seg, x = [], pad
    for l in languages:
        sw = bw * l["pct"] / total
        seg.append(f'<rect x="{x:.1f}" y="{y}" width="{sw:.1f}" height="8" fill="{LANG_COL.get(l["name"], MUTED)}"/>')
        x += sw
    body.append(f'<defs><clipPath id="lb"><rect x="{pad}" y="{y}" width="{bw}" height="8" rx="4"/></clipPath></defs>'
                f'<g clip-path="url(#lb)">{"".join(seg)}</g>')
    y += 28
    lc = 2 if m else 3
    lw = (w - 2 * pad) / lc
    for i, l in enumerate(languages):
        r, c = divmod(i, lc)
        lx, ly = pad + c * lw, y + r * 22
        body.append(f'<circle cx="{lx + 5}" cy="{ly - 4}" r="4" fill="{LANG_COL.get(l["name"], MUTED)}"/>')
        body.append(t(lx + 16, ly, f'{l["name"]} {l["pct"]}%', "monob", 12, kit.BODY, ls=0.8))
    y += ((len(languages) + lc - 1) // lc) * 22
    h = y + pad - 12
    return w, h, card(0, 0, w, h) + "".join(body)
