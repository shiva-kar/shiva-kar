#!/usr/bin/env python3
"""Verified certifications component: clean side-by-side credential cards matching portfolio cert boxes."""
import config
import kit
from kit import BODY, CARD, CARD2, EDGE, GREEN, MUTED, TEXT, card, fit, t, wrap


def certs(w):
    m = w < 600
    pad = 16 if m else 20
    gap = 12
    cw = w if m else (w - gap) / 2
    ch = 126 if m else 132

    cards_out = []
    for i, (code, title, issuer, topics) in enumerate(config.CERTS):
        x = 0 if m else i * (cw + gap)
        y = i * (ch + gap) if m else 0

        # Status badge pill matching portfolio (.status-pill / .cert-meta)
        status_text = "Completed"
        status_w = kit.tw(status_text, "bodyb", 11) + 14
        status_x = x + cw - pad - status_w

        c = [
            card(x, y, cw, ch, 8, fill=CARD, stroke=EDGE),
            t(x + pad, y + pad + 13, f"{issuer} (CS50)", "body", 12, MUTED),
            t(x + pad, y + pad + 36, code, "head", 18, "#ffffff"),
            f'<rect x="{status_x:.1f}" y="{y + pad + 22}" width="{status_w:.1f}" height="20" rx="4" fill="{CARD2}" stroke="{EDGE}"/>',
            t(status_x + status_w / 2, y + pad + 36, status_text, "bodyb", 11, GREEN, "middle"),
            t(x + pad, y + pad + 58, fit(title, "bodyb", 13.5, cw - 2 * pad), "bodyb", 13.5, TEXT),
        ]
        ty = y + pad + 78
        for ln in wrap(topics, "body", 12, cw - 2 * pad, maxlines=2):
            c.append(t(x + pad, ty, ln, "body", 12, MUTED))
            ty += 16

        cards_out.append("".join(c))

    total_h = len(config.CERTS) * (ch + gap) - gap if m else ch
    return w, total_h, "".join(cards_out)


