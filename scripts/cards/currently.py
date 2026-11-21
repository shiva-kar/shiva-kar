#!/usr/bin/env python3
"""Currently component: focus areas and current engineering work."""
import config
from kit import BODY, CARD, EDGE, MUTED, TEXT, card, t, wrap


def currently(w):
    m = w < 600
    pad = 20 if m else 28
    y = pad + 16
    lh = 24
    body = []
    
    for i, item in enumerate(config.CURRENTLY):
        # Subtle numeric or dash indicator
        body.append(t(pad, y, "•", "body", 13.5, MUTED))
        for ln in wrap(item, "body", 13.5 if m else 14, w - 2 * pad - 24, maxlines=2):
            body.append(t(pad + 20, y, ln, "body", 13.5 if m else 14, TEXT))
            y += 20
        y += 8
        if i < len(config.CURRENTLY) - 1:
            body.append(f'<line x1="{pad + 20}" x2="{w - pad}" y1="{y - 2}" y2="{y - 2}" stroke="{EDGE}"/>')
            y += 12

    h = y + pad - 6
    return w, h, card(0, 0, w, h, 10, fill=CARD, stroke=EDGE) + "".join(body)

