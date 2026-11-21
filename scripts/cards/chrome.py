#!/usr/bin/env python3
"""Chrome components: section headers, dividers, connect buttons, and footer."""
import config
import kit
from kit import BLUE, CARD2, EDGE, EDGE2, MUTED, TEXT, card, icon, t


def divider(w):
    return w, 16, f'<line x1="0" y1="8" x2="{w}" y2="8" stroke="{EDGE}" stroke-width="1"/>'


def header(key, theme, w):
    m = w < 600
    val = config.HEADERS.get(key, ("", key))
    title = val[0] if isinstance(val, (tuple, list)) else val
    dark = theme == "dark"
    col = "#f0f6fc" if dark else "#1f2328"
    border_col = EDGE if dark else "#d0d7de"
    h = 44
    body = [
        t(0, 26, title, "head", 18 if m else 21, col),
        f'<line x1="0" y1="41.5" x2="{w}" y2="41.5" stroke="{border_col}" stroke-width="1"/>'
    ]
    return w, h, "".join(body)


def connect(text, slug):
    wd = 14 + 16 + 10 + kit.tw(text, "bodyb", 12.5, 0.4) + 20
    body = (f'<rect x=".5" y=".5" width="{wd - 1:.1f}" height="37" rx="18.5" fill="{CARD2}" stroke="{EDGE}"/>'
            + icon(slug, 15, 11, 16, kit.TEXT) + t(41, 24, text, "bodyb", 12.5, kit.TEXT, ls=0.4))
    return wd, 38, body


def footer(w):
    m = w < 600
    h = 84
    body = [
        card(0, 0, w, h, 10, fill=CARD2, stroke=EDGE),
        t(w / 2, 34, "Shiva Kar", "bodyb", 15, TEXT, "middle"),
        t(w / 2, 58, "shivakar.me ↗", "body", 13.5, BLUE, "middle"),
    ]
    return w, h, "".join(body)

