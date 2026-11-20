#!/usr/bin/env python3
"""Chrome components: section headers, dividers, connect buttons, and footer."""
import config
import kit
from kit import BLUE, CARD2, EDGE, EDGE2, MUTED, card, icon, t


def divider(w):
    return w, 16, (f'<defs><linearGradient id="d" x1="0" x2="1"><stop offset="0" stop-color="{EDGE}" stop-opacity="0"/>'
                   f'<stop offset=".5" stop-color="{EDGE2}"/><stop offset="1" stop-color="{EDGE}" stop-opacity="0"/></linearGradient></defs>'
                   f'<rect y="7.5" width="{w}" height="1" fill="url(#d)"/>')


def header(key, theme, w):
    m = w < 600
    lab, title = config.HEADERS[key]
    dark = theme == "dark"
    col = "#f0f6fc" if dark else "#1f2328"
    acc = BLUE if dark else "#0969da"
    sub_col = MUTED if dark else "#57606a"
    border_col = EDGE if dark else "#d0d7de"
    h = 50
    body = [
        f'<rect x="0" y="7" width="3.5" height="36" rx="1.75" fill="{acc}"/>',
        t(16, 17, lab, "monob", 11 if m else 11.5, sub_col, ls=2.0),
        t(16, 40, title, "head", 20 if m else 22, col),
        f'<line x1="0" y1="49.5" x2="{w}" y2="49.5" stroke="{border_col}" stroke-width="1"/>'
    ]
    return w, h, "".join(body)


def connect(text, slug):
    wd = 14 + 16 + 10 + kit.tw(text, "monob", 12, 1.2) + 20
    body = (f'<rect x=".5" y=".5" width="{wd - 1:.1f}" height="37" rx="18.5" fill="{CARD2}" stroke="{EDGE2}"/>'
            + icon(slug, 15, 11, 16, kit.TEXT) + t(41, 24, text, "monob", 12, kit.TEXT, ls=1.2))
    return wd, 38, body


def footer(w):
    m = w < 600
    h = 96
    body = [
        card(0, 0, w, h, 12, fill=CARD2, stroke=EDGE2),
        t(w / 2, 32, "SHIVA KAR • BCA STUDENT & DEVELOPER", "monob", 11.5, MUTED, "middle", 2.0),
        t(w / 2, 58, "More at shivakar.me ↗", "bodyb", 18 if m else 20, BLUE, "middle"),
        t(w / 2, 80, "Built with Python SVG generator • Updated daily via GitHub Actions", "body", 12, MUTED, "middle")
    ]
    return w, h, "".join(body)
