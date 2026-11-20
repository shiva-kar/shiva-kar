#!/usr/bin/env python3
"""Verified certifications component: side-by-side credential cards."""
import config
from kit import BLUE, CARD2, EDGE2, GREEN, MUTED, PURPLE, TEXT, card, fit, label, t, wrap


def certs(w):
    m = w < 600
    pad = 20 if m else 26
    gap = 14
    cw = w - 2 * pad if m else (w - 2 * pad - gap) / 2
    ch = 180

    body = [label(pad, pad + 10, "VERIFIED CERTIFICATIONS", BLUE, 11.5)]
    y_cards = pad + 30

    cards_out = []
    for i, (code, title, issuer, topics) in enumerate(config.CERTS):
        acc = BLUE if i == 0 else PURPLE
        x = pad if m else pad + i * (cw + gap)
        y = y_cards + i * (ch + gap) if m else y_cards

        c = [
            f'<rect x="{x + .5:.1f}" y="{y + .5:.1f}" width="{cw - 1:.1f}" height="{ch - 1:.1f}" rx="10" fill="{CARD2}" stroke="{EDGE2}"/>',
            f'<rect x="{x:.1f}" y="{y + 14:.1f}" width="3.5" height="42" rx="1.75" fill="{acc}"/>',
            f'<rect x="{x + 14:.1f}" y="{y + 16:.1f}" width="140" height="22" rx="5" fill="{GREEN}" fill-opacity=".15" stroke="{GREEN}" stroke-opacity=".4"/>',
            t(x + 84, y + 31.5, "VERIFIED CREDENTIAL", "monob", 10.5, GREEN, "middle", 0.5),
            t(x + cw - 14, y + 31.5, issuer.upper(), "monob", 11, MUTED, "end", 1),
            t(x + 14, y + 66, code, "head", 20, "#ffffff"),
            t(x + 14, y + 88, fit(title, "bodyb", 14.5, cw - 28), "bodyb", 14.5, TEXT),
        ]
        ty = y + 116
        for ln in wrap(topics, "body", 12, cw - 28, maxlines=2):
            c.append(t(x + 14, ty, ln, "body", 12, MUTED))
            ty += 18

        cards_out.append("".join(c))

    total_h = y_cards + (len(config.CERTS) * (ch + gap) - gap if m else ch) + pad
    return w, total_h, card(0, 0, w, total_h) + "".join(body) + "".join(cards_out)
