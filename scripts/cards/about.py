#!/usr/bin/env python3
"""About Me component: clear, human summary of focus and engineering background."""
import config
import kit
from kit import BODY, CARD, EDGE, card, t, wrap


def about(w):
    m = w < 600
    pad = 22 if m else 32
    size = 14.5 if m else 15.5
    lh = int(size * 1.65)
    maxw = w - 2 * pad
    
    lines = wrap(config.ABOUT, "body", size, maxw)
    y = pad + size + 2
    body = []
    for ln in lines:
        body.append(t(pad, y, ln, "body", size, BODY))
        y += lh
    
    h = y + pad - lh + 6
    return w, h, card(0, 0, w, h, 12, fill=CARD, stroke=EDGE) + "".join(body)
