#!/usr/bin/env python3
"""Currently component: focus areas and current engineering work."""
import config
from kit import GREEN, TEXT, card, label, t, wrap


def currently(w):
    m = w < 600
    pad = 22 if m else 30
    body = [label(pad + 8, pad + 20, "CURRENTLY", GREEN, 11.5)]
    y = pad + 44
    lh = 26
    for item in config.CURRENTLY:
        body.append(f'<circle cx="{pad + 14}" cy="{y - 4}" r="3" fill="{GREEN}"/>')
        for ln in wrap(item, "body", 13.5 if m else 14.5, w - 2 * pad - 30, maxlines=3):
            body.append(t(pad + 26, y, ln, "body", 13.5 if m else 14.5, TEXT))
            y += 20
        y += lh - 20
    h = y + pad - 8
    return w, h, card(0, 0, w, h) + f'<rect x="0" y="16" width="3.5" height="{h - 32}" rx="1.75" fill="{GREEN}"/>' + "".join(body)
