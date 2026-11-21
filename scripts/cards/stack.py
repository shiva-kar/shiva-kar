#!/usr/bin/env python3
"""Tech stack component: clean, static categorized grid of technologies and tools."""
import config
from kit import BODY, CARD, EDGE, ICONS, TEXT, card, icon, t


def marquee(w):
    """Static, non-animated grid of technical skills grouped by discipline."""
    m = w < 600
    pad = 16 if m else 20
    gap = 12
    cols = 1 if m else 2
    cw = w if m else (w - gap) / 2
    
    body = []
    card_y = 0
    
    disciplines = getattr(config, "DISCIPLINES", [])
    for idx, (cat_name, items) in enumerate(disciplines):
        r, c = divmod(idx, cols)
        cx = 0 if m else c * (cw + gap)
        ch = 142
        cy = r * (ch + gap)
        
        cb = [
            card(cx, cy, cw, ch, 6, fill=CARD, stroke=EDGE),
            t(cx + pad, cy + pad + 12, cat_name, "bodyb", 14.5, TEXT),
        ]
        
        icols = 2
        iw = (cw - 2 * pad) / icols
        for i, (name, slug, col) in enumerate(items):
            ir, ic = divmod(i, icols)
            ix = cx + pad + ic * iw
            iy = cy + pad + 38 + ir * 30
            
            c_color = col or ("#" + ICONS[slug]["hex"] if slug in ICONS else "#ffffff")
            if slug and slug in ICONS:
                cb.append(icon(slug, ix, iy - 14, 18, c_color))
                cb.append(t(ix + 26, iy, name, "body", 12.5, BODY))
            else:
                cb.append(f'<circle cx="{ix + 8:.1f}" cy="{iy - 5:.1f}" r="4" fill="{EDGE}"/>')
                cb.append(t(ix + 26, iy, name, "body", 12.5, BODY))
                
        body.append("".join(cb))
        card_y = max(card_y, cy + ch)
        
    total_h = card_y
    return w, total_h, "".join(body)

