#!/usr/bin/env python3
"""Verified certifications component: clean side-by-side credential cards."""
import config
from kit import BODY, CARD, CARD2, EDGE, MUTED, TEXT, card, fit, t, wrap


def certs(w):
    m = w < 600
    pad = 18 if m else 24
    gap = 14
    cw = w if m else (w - gap) / 2
    ch = 148 if m else 156

    cards_out = []
    for i, (code, title, issuer, topics) in enumerate(config.CERTS):
        x = 0 if m else i * (cw + gap)
        y = i * (ch + gap) if m else 0

        c = [
            card(x, y, cw, ch, 10, fill=CARD, stroke=EDGE),
            t(x + pad, y + pad + 14, issuer, "body", 12.5, MUTED),
            t(x + pad, y + pad + 40, code, "head", 19, "#ffffff"),
            t(x + pad, y + pad + 62, fit(title, "bodyb", 14, cw - 2 * pad), "bodyb", 14, TEXT),
        ]
        ty = y + pad + 86
        for ln in wrap(topics, "body", 12.5, cw - 2 * pad, maxlines=2):
            c.append(t(x + pad, ty, ln, "body", 12.5, MUTED))
            ty += 18

        cards_out.append("".join(c))

    total_h = len(config.CERTS) * (ch + gap) - gap if m else ch
    return w, total_h, "".join(cards_out)

