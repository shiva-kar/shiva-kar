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
    t_cfg = kit.THEMES.get(theme, kit.THEMES["dark"])
    col = t_cfg["TEXT"]
    border_col = t_cfg["EDGE"]
    h = 38
    body = [
        t(0, 24, title, "head", 17 if m else 19, col),
        f'<line x1="0" y1="35.5" x2="{w}" y2="35.5" stroke="{border_col}" stroke-width="1"/>'
    ]
    return w, h, "".join(body)


def connect(text, slug, theme="dark"):
    t_cfg = kit.THEMES.get(theme, kit.THEMES["dark"])
    bg = t_cfg["CARD2"] if theme == "dark" else t_cfg["CARD"]
    border = t_cfg["EDGE"]
    fg = t_cfg["TEXT"]
    wd = 14 + 16 + 8 + kit.tw(text, "bodyb", 12.5, 0.2) + 16
    body = (f'<rect x=".5" y=".5" width="{wd - 1:.1f}" height="35" rx="6" fill="{bg}" stroke="{border}"/>'
            + icon(slug, 13, 10, 16, fg) + t(36, 22.5, text, "bodyb", 12.5, fg, ls=0.2))
    return wd, 36, body


def footer(w):
    m = w < 600
    h = 60
    body = [
        card(0, 0, w, h, 6, fill=kit.CARD, stroke=kit.EDGE),
        t(w / 2, 26, "Shiva Kar", "bodyb", 14, kit.TEXT, "middle"),
        t(w / 2, 46, "shivakar.me ↗", "body", 12.5, kit.GREEN, "middle"),
    ]
    return w, h, "".join(body)

