#!/usr/bin/env python3
"""Hero and top statistics pills components."""
import config
import kit
from kit import BLUE, CARD, CARD2, EDGE2, GREEN, MUTED, ORANGE, PURPLE, card, label, mix, t, wrap


def hero(w, data):
    m = w < 600
    pad = 24 if m else 48
    big = 42 if m else 56
    sub = 15 if m else 17
    loc = (config.LOCATION or data.get("location") or "").upper()
    sublines = wrap(config.SUBTITLE, "bodyb", sub, w - 2 * pad - (0 if m else 260))
    stat_w = kit.tw(config.STATUS, "monob", 11.5, 1.2) + 38
    y = 52 + big + 10
    yy = y + 32
    py = yy + len(sublines) * (sub + 8)
    h = py + 48 if m else 240
    body = [
        card(0, 0, w, h, 14),
        label(pad, 48, "HI, I AM", BLUE, 11.5),
        t(pad, y, config.NAME, "head", big, "#ffffff")
    ]
    for ln in sublines:
        body.append(t(pad, yy, ln, "bodyb", sub, MUTED))
        yy += sub + 8
    if not m:
        py = 186
    body.append(
        f'<rect x="{pad}" y="{py}" width="{stat_w:.1f}" height="28" rx="6" fill="{GREEN}" fill-opacity=".1" '
        f'stroke="{GREEN}" stroke-opacity=".35"/>'
        f'<circle cx="{pad + 14}" cy="{py + 14}" r="3.5" fill="{GREEN}"/>'
    )
    body.append(t(pad + 26, py + 18.5, config.STATUS, "monob", 11.5, GREEN, ls=1.2))
    if loc:
        body.append(t(pad if m else pad + stat_w + 16, py + (44 if m else 18.5), loc, "mono", 11, MUTED, ls=1.2))
    return w, h, "".join(body)


def pills(w, data):
    merged_godot = sum(1 for p in data.get("merged", []) if p["repo"] == "godotengine/godot")
    items = [
        ("FOLLOWERS", str(data.get("followers", 0)), BLUE),
        ("TOTAL STARS", str(data.get("stars", 0)), ORANGE),
        ("PULL REQUESTS", str(data.get("prs_total", 0)), BLUE),
        ("GODOT MERGED", str(merged_godot), GREEN),
        ("CERTIFIED", "CS50x + CS50 SQL", PURPLE),
        ("CONTRIBUTIONS", f'{data.get("calendar", {}).get("total", 0):,}', BLUE),
        ("PORTFOLIO", "SHIVAKAR.ME", BLUE)
    ]
    gap, ph = 10, 34
    rows, cur, cw = [], [], 0
    for it in items:
        lw = kit.tw(it[0], "mono", 11, 1.2) + 24
        vw = kit.tw(it[1], "monob", 12.5, 0.8) + 24
        pw = lw + vw
        if cur and cw + gap + pw > w:
            rows.append((cur, cw))
            cur, cw = [], 0
        cw += (gap if cur else 0) + pw
        cur.append((it, lw, vw))
    rows.append((cur, cw))
    body = []
    for r, (row, rw) in enumerate(rows):
        x = (w - rw) / 2
        y = r * (ph + 10)
        for (lab, val, col), lw, vw in row:
            pw = lw + vw
            body.append(f'<rect x="{x + .5:.1f}" y="{y + .5}" width="{pw - 1:.1f}" height="{ph - 1}" rx="17" fill="{CARD2}" stroke="{EDGE2}"/>'
                        f'<path d="M{x + 17:.1f} {y} A17 17 0 0 0 {x + 17:.1f} {y + ph} H{x + lw:.1f} V{y} Z" fill="{mix(col, CARD, .12)}"/>'
                        f'<line x1="{x + lw:.1f}" y1="{y}" x2="{x + lw:.1f}" y2="{y + ph}" stroke="{EDGE2}"/>')
            body.append(t(x + 12, y + 21.5, lab, "mono", 11, MUTED, ls=1.2))
            body.append(t(x + lw + 12, y + 22, val, "monob", 12.5, col, ls=0.8))
            x += pw + gap
    return w, len(rows) * (ph + 10) - 10, "".join(body)
