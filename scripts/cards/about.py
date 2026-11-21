#!/usr/bin/env python3
"""About Me component: calm, confident editorial summary of backend engineering background."""
import config
import kit
from kit import BODY, CARD, EDGE, GREEN, TEXT, card, t, wrap


def about(w):
    m = w < 600
    pad_x = 20 if m else 28
    pad_y = 18 if m else 24
    maxw = w - 2 * pad_x
    
    body = [
        # Eyebrow in monospace green
        t(pad_x, pad_y + 12, "Java Backend Developer · BCA Student", "mono", 11.5, GREEN),
        # Confident sentence-case headline
        t(pad_x, pad_y + 36, "Building backend applications with Java and Spring Boot.", "bodyb", 16.5 if m else 19.5, TEXT),
    ]
    
    div_y = pad_y + 48
    body.append(f'<line x1="{pad_x}" x2="{w - pad_x}" y1="{div_y}" y2="{div_y}" stroke="{EDGE}" stroke-width="1"/>')
    
    size = 13.5 if m else 14
    lh = 22 if m else 23
    lines = wrap(config.ABOUT, "body", size, maxw)
    y = div_y + 20
    for ln in lines:
        body.append(t(pad_x, y, ln, "body", size, BODY))
        y += lh
    
    h = y + pad_y - lh + 6
    return w, h, card(0, 0, w, h, 6, fill=CARD, stroke=EDGE) + "".join(body)

