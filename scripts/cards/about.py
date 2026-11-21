#!/usr/bin/env python3
"""About Me component: clear, human summary of focus and engineering background."""
import config
import kit
from kit import BODY, CARD, EDGE, GREEN, card, t, wrap


def about(w):
    m = w < 600
    pad_x = 20 if m else 26
    pad_y = 18 if m else 22
    size = 13.5 if m else 14.5
    lh = 22 if m else 24
    maxw = w - 2 * pad_x
    
    body = [
        t(pad_x, pad_y + 13, "JAVA BACKEND & SYSTEMS DEVELOPER · GODOT CONTRIBUTOR", "bodyb", 11.5, GREEN, ls=0.5)
    ]
    
    lines = wrap(config.ABOUT, "body", size, maxw)
    y = pad_y + 36
    for ln in lines:
        body.append(t(pad_x, y, ln, "body", size, BODY))
        y += lh
    
    h = y + pad_y - lh + 8
    return w, h, card(0, 0, w, h, 8, fill=CARD, stroke=EDGE) + "".join(body)
