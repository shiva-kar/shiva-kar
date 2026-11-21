#!/usr/bin/env python3
"""Hero and top statistics summary components."""
import config
import kit
from kit import BLUE, CARD, CARD2, EDGE, GREEN, MUTED, ORANGE, TEXT, TITLE, card, t, wrap


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
        t(pad, y, config.NAME, "head", big, TITLE),
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
    merged_godot = sum(1 for p in data.get("merged", []) if p.get("repo") == "godotengine/godot") or 6
    items = [
        ("BCA COMPUTER SCIENCE", f"CGPA {config.CGPA}", "Amity University Online", TEXT),
        ("GODOT ENGINE", f"{merged_godot} Merged PRs", "15 submitted (C++)", GREEN),
        ("PRIMARY STACK", "Java · Spring Boot", "PostgreSQL · Redis · Docker", TEXT),
        ("BASED IN", "Hojai, Assam, India", "Open to Remote / Relocate", TEXT),
    ]
    
    if m:
        cols = 2
        gap = 10
        card_w = (w - gap) / cols
        h_cell = 70
        body = []
        for i, (lab, val, sub, col) in enumerate(items):
            r, c = divmod(i, cols)
            cx = c * (card_w + gap)
            cy = r * (h_cell + gap)
            body.append(card(cx, cy, card_w, h_cell, 6, fill=CARD2, stroke=EDGE))
            body.append(t(cx + card_w / 2, cy + 20, lab, "bodyb", 10.5, MUTED, "middle", ls=0.3))
            body.append(t(cx + card_w / 2, cy + 42, val, "bodyb", 15, col, "middle"))
            body.append(t(cx + card_w / 2, cy + 59, sub, "body", 10.5, MUTED, "middle"))
        rows = 2
        total_h = rows * h_cell + (rows - 1) * gap
        return w, total_h, "".join(body)
    else:
        cols = 4
        gap = 12
        card_w = (w - gap * (cols - 1)) / cols
        h_cell = 74
        body = []
        for i, (lab, val, sub, col) in enumerate(items):
            cx = i * (card_w + gap)
            body.append(card(cx, 0, card_w, h_cell, 6, fill=CARD2, stroke=EDGE))
            body.append(t(cx + card_w / 2, 22, lab, "bodyb", 10.8, MUTED, "middle", ls=0.4))
            body.append(t(cx + card_w / 2, 45, val, "bodyb", 16.5, col, "middle"))
            body.append(t(cx + card_w / 2, 62, sub, "body", 11.2, MUTED, "middle"))
        return w, h_cell, "".join(body)

