#!/usr/bin/env python3
"""Currently component: focus areas and current engineering work."""
import config
import kit
from kit import BODY, CARD, EDGE, GREEN, MUTED, TEXT, card, t, wrap


def currently(w):
    m = w < 600
    pad = 18 if m else 24
    y = pad + 14
    body = []
    
    for i, item in enumerate(config.CURRENTLY):
        # Subtle diamond indicator matching portfolio evidence tree (◆ in green)
        body.append(t(pad, y - 1, "◆", "body", 10.5, GREEN))
        for ln in wrap(item, "body", 13.5 if m else 14, w - 2 * pad - 22, maxlines=2):
            body.append(t(pad + 18, y, ln, "body", 13.5 if m else 14, TEXT))
            y += 19
        y += 6
        if i < len(config.CURRENTLY) - 1:
            body.append(f'<line x1="{pad + 18}" x2="{w - pad}" y1="{y - 2}" y2="{y - 2}" stroke="{EDGE}"/>')
            y += 10

    h = y + pad - 6
    return w, h, card(0, 0, w, h, 6, fill=CARD, stroke=EDGE) + "".join(body)

