#!/usr/bin/env python3
"""Tech stack marquee and concepts grid components."""
import math

import config
import kit
from kit import BLUE, CARD, CARD2, EDGE, GREEN, ICONS, TEXT, card, fit, icon, label, mix, t


def marquee(w):
    tile, pitch, gapy, pad = 56, 64, 14, 18
    h = 2 * tile + gapy + 2 * pad
    defs = (f'<defs><linearGradient id="fl" x1="0" x2="1"><stop offset="0" stop-color="{CARD}"/><stop offset="1" stop-color="{CARD}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="fr" x1="1" x2="0"><stop offset="0" stop-color="{CARD}"/><stop offset="1" stop-color="{CARD}" stop-opacity="0"/></linearGradient></defs>')
    rows = []
    for ri, items in enumerate(config.MARQUEE):
        seq = len(items) * pitch
        reps = int(math.ceil((w + seq) / seq)) + 1
        tiles = []
        for rep in range(reps):
            for i, (name, slug, col) in enumerate(items):
                x = rep * seq + i * pitch
                c = col or ("#" + ICONS[slug]["hex"] if slug in ICONS else "#ffffff")
                tiles.append(f'<rect x="{x}" y="0" width="{tile}" height="{tile}" rx="12" fill="{mix(c, CARD, .14)}" '
                             f'stroke="{mix(c, CARD, .35)}"/>')
                tiles.append(icon(slug, x + 15, 15, 26, c) if slug and slug in ICONS else t(x + 28, 35, name[:2], "monob", 17, c, "middle"))
        frm, to = (0, -seq) if ri % 2 == 0 else (-seq, 0)
        rows.append(f'<g transform="translate(0 {pad + ri * (tile + gapy)})"><g><animateTransform attributeName="transform" '
                    f'type="translate" from="{frm} 0" to="{to} 0" dur="{len(items) * 3.5:.0f}s" repeatCount="indefinite"/>'
                    f'{"".join(tiles)}</g></g>')
    fade = 60
    body = (defs + card(0, 0, w, h) + f'<g>{"".join(rows)}'
            f'<rect x="1" y="1" width="{fade}" height="{h - 2}" fill="url(#fl)"/>'
            f'<rect x="{w - fade - 1}" y="1" width="{fade}" height="{h - 2}" fill="url(#fr)"/></g>' + card(0, 0, w, h, fill="none"))
    return w, h, body


def concepts(w):
    m = w < 600
    pad = 20 if m else 24
    cols, gap = (2 if m else 5), 8
    bw = (w - 2 * pad - gap * (cols - 1)) / cols
    body = [label(pad, pad + 10, "CORE CONCEPTS AND LIBRARIES", BLUE, 11.5)]
    y0 = pad + 30
    for i, c in enumerate(config.CONCEPTS):
        r, cc = divmod(i, cols)
        x, y = pad + cc * (bw + gap), y0 + r * 46
        body.append(f'<rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="38" rx="8" fill="{CARD2}" stroke="{EDGE}"/>')
        body.append(f'<circle cx="{x + 14:.1f}" cy="{y + 19}" r="2.5" fill="{BLUE if i % 2 == 0 else GREEN}"/>')
        body.append(t(x + 24, y + 23.5, fit(c, "bodyb", 12, bw - 28), "bodyb", 12, TEXT))
    rows = (len(config.CONCEPTS) + cols - 1) // cols
    h = y0 + rows * 46 - 8 + pad
    return w, h, card(0, 0, w, h) + "".join(body)
