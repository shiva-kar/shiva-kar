#!/usr/bin/env python3
"""Developer setup and daily tools component."""
import config
import kit
from kit import BLUE, CARD2, EDGE, MUTED, TEXT, card, label, t, tag


def tools(w):
    m = w < 600
    pad = 20 if m else 26
    body = [label(pad, pad + 10, "DEVELOPER SETUP AND DAILY TOOLS", BLUE, 11.5)]
    y = pad + 32

    if not m:
        # Desktop: 2-column balanced grid of 4 categories (2 rows x 2 cols)
        col_gap = 20
        cw = (w - 2 * pad - col_gap) / 2
        categories = config.TOOLS
        # Split into rows of 2
        for row_idx in range(0, len(categories), 2):
            row_cats = categories[row_idx:row_idx + 2]
            max_cat_h = 0
            cat_bodies = []
            for col_idx, (cat_name, cat_tools) in enumerate(row_cats):
                cx = pad if col_idx == 0 else pad + cw + col_gap
                cy = y
                cb = [
                    f'<rect x="{cx:.1f}" y="{cy:.1f}" width="{cw:.1f}" height="28" rx="6" fill="{CARD2}" stroke="{EDGE}"/>',
                    t(cx + 12, cy + 18.5, cat_name.upper(), "monob", 11, BLUE, ls=1.0)
                ]
                tx = cx
                ty = cy + 36
                for tool in cat_tools:
                    s, tw_val = tag(tx, ty, tool, BLUE, 11.5, h=26)
                    if tx + tw_val > cx + cw and tx > cx:
                        tx = cx
                        ty += 34
                        s, tw_val = tag(tx, ty, tool, BLUE, 11.5, h=26)
                    cb.append(s)
                    tx += tw_val + 8
                cat_h = ty + 26 - cy
                max_cat_h = max(max_cat_h, cat_h)
                cat_bodies.append("".join(cb))
            body.extend(cat_bodies)
            y += max_cat_h + 16
    else:
        # Mobile: stacked categories
        for cat_name, cat_tools in config.TOOLS:
            body.append(t(pad, y + 14, cat_name.upper(), "monob", 11, BLUE, ls=1.0))
            y += 24
            tx = pad
            for tool in cat_tools:
                s, tw_val = tag(tx, y, tool, BLUE, 11, h=24)
                if tx + tw_val > w - pad and tx > pad:
                    tx = pad
                    y += 32
                    s, tw_val = tag(tx, y, tool, BLUE, 11, h=24)
                body.append(s)
                tx += tw_val + 6
            y += 38

    total_h = y + pad - 6
    return w, total_h, card(0, 0, w, total_h) + "".join(body)
