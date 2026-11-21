#!/usr/bin/env python3
"""Hero and top statistics summary components."""
import config
import kit
from kit import BLUE, CARD, CARD2, EDGE, GREEN, MUTED, ORANGE, TEXT, card, short, t, wrap


def hero(w, data):
    m = w < 600
    pad = 24 if m else 40
    big = 38 if m else 50
    sub = 15 if m else 17
    loc = config.LOCATION or data.get("location") or ""
    sublines = wrap(config.SUBTITLE, "body", sub, w - 2 * pad)
    y = pad + big
    yy = y + 22
    for _ in sublines:
        yy += sub + 6
    if loc:
        yy += 20
    h = yy + pad - 6
    body = [
        card(0, 0, w, h, 12),
        t(pad, y, config.NAME, "head", big, "#ffffff"),
    ]
    cur_y = y + 26
    for ln in sublines:
        body.append(t(pad, cur_y, ln, "body", sub, MUTED))
        cur_y += sub + 6
    if loc:
        body.append(t(pad, cur_y + 12, loc, "body", 13, MUTED))
    return w, h, "".join(body)


def pills(w, data):
    m = w < 600
    merged_godot = sum(1 for p in data.get("merged", []) if p["repo"] == "godotengine/godot")
    items = [
        ("Godot Merged", str(merged_godot), GREEN),
        ("Pull Requests", str(data.get("prs_total", 0)), BLUE),
        ("Contributions", f'{data.get("calendar", {}).get("total", 0):,}', TEXT),
        ("Stars Earned", str(data.get("stars", 0)), ORANGE),
        ("Followers", str(data.get("followers", 0)), TEXT),
    ]
    
    pad = 12 if m else 16
    gap = 8
    
    if m:
        cols = 2
        card_w = (w - pad * 2 - gap) / cols
        h_cell = 54
        body = []
        for i, (lab, val, col) in enumerate(items):
            r, c = divmod(i, cols)
            # Center last odd item if any
            if i == len(items) - 1 and len(items) % 2 == 1:
                cx = pad + (w - 2 * pad - card_w) / 2
            else:
                cx = pad + c * (card_w + gap)
            cy = pad + r * (h_cell + gap)
            body.append(card(cx, cy, card_w, h_cell, 8, fill=CARD2, stroke=EDGE))
            body.append(t(cx + card_w / 2, cy + 24, val, "bodyb", 16, col, "middle"))
            body.append(t(cx + card_w / 2, cy + 42, lab, "body", 11.5, MUTED, "middle"))
        rows = (len(items) + cols - 1) // cols
        total_h = pad * 2 + rows * (h_cell + gap) - gap
        return w, total_h, "".join(body)
    else:
        cols = len(items)
        card_w = (w - gap * (cols - 1)) / cols
        h_cell = 58
        body = []
        for i, (lab, val, col) in enumerate(items):
            cx = i * (card_w + gap)
            body.append(card(cx, 0, card_w, h_cell, 8, fill=CARD2, stroke=EDGE))
            body.append(t(cx + card_w / 2, 26, val, "bodyb", 18, col, "middle"))
            body.append(t(cx + card_w / 2, 45, lab, "body", 12, MUTED, "middle"))
        return w, h_cell, "".join(body)

