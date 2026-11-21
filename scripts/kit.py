#!/usr/bin/env python3
"""Shared design system and SVG drawing primitives.

Contains the GitHub-native dark theme palette, font metrics engine, character subsetting,
and drawing helpers (cards, text, labels, chips, and icons).
"""
import base64
import io
import json
import os
from xml.sax.saxutils import escape as esc

from fontTools import subset as ftsubset
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "svg")
FD = os.path.join(ROOT, "scripts", "fonts")
ICONS = json.load(open(os.path.join(ROOT, "scripts", "icons.json"), encoding="utf-8"))

# Palettes: GitHub-native bluish-dark (#0d1117 / #161b22) and crisp light (#ffffff / #f6f8fa)
THEMES = {
    "dark": {
        "CARD": "#161b22",       # GitHub Dark card / surface (bluish slate)
        "CARD2": "#0d1117",      # GitHub Dark canvas / inner container
        "EDGE": "#30363d",       # GitHub Dark border
        "EDGE2": "#21262d",      # GitHub Dark subtle divider
        "TEXT": "#f0f6fc",       # High contrast off-white text
        "TITLE": "#ffffff",      # Pure white headline
        "BODY": "#c9d1d9",       # Secondary body text
        "MUTED": "#8b949e",      # Muted labels and dates
        "GREEN": "#3fb950",      # GitHub native green
        "ORANGE": "#d29922",     # GitHub native amber
        "BLUE": "#58a6ff",       # GitHub native blue
        "RED": "#f85149",        # Terminal / danger red
        "PURPLE": "#a594f9",
        "HEATMAP": ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"],
    },
    "light": {
        "CARD": "#ffffff",       # GitHub Light card / surface
        "CARD2": "#f6f8fa",      # GitHub Light canvas / inner container
        "EDGE": "#d0d7de",       # GitHub Light border
        "EDGE2": "#d8dee4",      # GitHub Light subtle divider
        "TEXT": "#1f2328",       # High contrast dark text
        "TITLE": "#1f2328",      # Crisp dark headline
        "BODY": "#24292f",       # Secondary body text
        "MUTED": "#656d76",      # Muted labels and dates
        "GREEN": "#1a7f37",      # GitHub light green
        "ORANGE": "#9a6700",     # GitHub light amber
        "BLUE": "#0969da",       # GitHub light blue
        "RED": "#cf222e",        # Terminal / danger red
        "PURPLE": "#8250df",
        "HEATMAP": ["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"],
    },
}

CURRENT_THEME = "dark"
CARD = THEMES["dark"]["CARD"]
CARD2 = THEMES["dark"]["CARD2"]
EDGE = THEMES["dark"]["EDGE"]
EDGE2 = THEMES["dark"]["EDGE2"]
GREEN = THEMES["dark"]["GREEN"]
ORANGE = THEMES["dark"]["ORANGE"]
BLUE = THEMES["dark"]["BLUE"]
RED = THEMES["dark"]["RED"]
PURPLE = THEMES["dark"]["PURPLE"]
TEXT = THEMES["dark"]["TEXT"]
TITLE = THEMES["dark"]["TITLE"]
BODY = THEMES["dark"]["BODY"]
MUTED = THEMES["dark"]["MUTED"]
HEATMAP = THEMES["dark"]["HEATMAP"]


def set_theme(theme_name: str):
    """Sets the active palette and updates imported constants across card modules."""
    global CURRENT_THEME, CARD, CARD2, EDGE, EDGE2, GREEN, ORANGE, BLUE, RED, PURPLE, TEXT, TITLE, BODY, MUTED, HEATMAP
    if theme_name not in THEMES:
        theme_name = "dark"
    CURRENT_THEME = theme_name
    t = THEMES[theme_name]
    CARD = t["CARD"]
    CARD2 = t["CARD2"]
    EDGE = t["EDGE"]
    EDGE2 = t["EDGE2"]
    GREEN = t["GREEN"]
    ORANGE = t["ORANGE"]
    BLUE = t["BLUE"]
    RED = t["RED"]
    PURPLE = t["PURPLE"]
    TEXT = t["TEXT"]
    TITLE = t["TITLE"]
    BODY = t["BODY"]
    MUTED = t["MUTED"]
    HEATMAP = t["HEATMAP"]

    import sys
    for mod_name in list(sys.modules.keys()):
        if mod_name.startswith("cards.") or mod_name == "kit":
            m = sys.modules[mod_name]
            for k, v in t.items():
                if hasattr(m, k):
                    setattr(m, k, v)

FONTS = {
    "body": ("Inter", 400, "inter-latin-400-normal.woff2"),
    "bodyb": ("Inter", 600, "inter-latin-600-normal.woff2"),
    "mono": ("JetBrains Mono", 500, "jetbrains-mono-latin-500-normal.woff2"),
    "monob": ("JetBrains Mono", 700, "jetbrains-mono-latin-700-normal.woff2"),
    "head": ("Archivo Black", 400, "archivo-black-latin-400-normal.woff2"),
}
STACKS = {
    "Inter": "Inter, 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
    "JetBrains Mono": "'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
    "Archivo Black": "'Archivo Black', 'Plus Jakarta Sans', Impact, sans-serif",
}

USED = {}
_metrics, _subs = {}, {}


def sanitize(s: str) -> str:
    """Sanitizes text by converting AI long dashes into standard punctuation."""
    return s.replace("\u2014", " - ").replace("\u2013", "-")


def metrics(k):
    if k not in _metrics:
        f = TTFont(os.path.join(FD, FONTS[k][2]))
        _metrics[k] = (f.getBestCmap(), f["hmtx"].metrics, f["head"].unitsPerEm)
    return _metrics[k]


def tw(s, k, size, ls=0.0):
    s = sanitize(s)
    cmap, hm, upm = metrics(k)
    total = 0
    for c in s:
        g = cmap.get(ord(c))
        total += hm[g][0] if g in hm else upm * 0.6
    return total / upm * size + ls * len(s)


def face_css(k, chars):
    key = (k, "".join(sorted(chars)))
    if key not in _subs:
        opts = ftsubset.Options()
        opts.layout_features = ["kern"]
        font = TTFont(os.path.join(FD, FONTS[k][2]), recalcTimestamp=False)
        sub = ftsubset.Subsetter(opts)
        sub.populate(text="".join(sorted(chars)) + " ")
        sub.subset(font)
        buf = io.BytesIO()
        font.flavor = "woff2"
        font.save(buf)
        _subs[key] = base64.b64encode(buf.getvalue()).decode()
    fam, wt, _ = FONTS[k]
    return (f"@font-face{{font-family:'{fam}';font-weight:{wt};"
            f"src:url(data:font/woff2;base64,{_subs[key]}) format('woff2')}}")


def t(x, y, s, k="body", size=14, fill=None, anchor="start", ls=0.0, extra=""):
    if fill is None:
        fill = BODY
    s = sanitize(s)
    USED.setdefault(k, set()).update(s)
    fam, wt, _ = FONTS[k]
    la = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{STACKS[fam]}" font-weight="{wt}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}"{la} {extra}>{esc(s)}</text>')


def fit(s, k, size, maxw, ls=0.0):
    s = sanitize(s)
    if tw(s, k, size, ls) <= maxw:
        return s
    while s and tw(s + "…", k, size, ls) > maxw:
        s = s[:-1]
    return s.rstrip() + "…"


def wrap(s, k, size, maxw, ls=0.0, maxlines=None):
    s = sanitize(s)
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if cur and tw(trial, k, size, ls) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    if maxlines and len(lines) > maxlines:
        lines = lines[:maxlines]
        lines[-1] = fit(lines[-1] + " …", k, size, maxw, ls)
    return lines


def doc(w, h, body):
    css = "".join(face_css(k, c) for k, c in sorted(USED.items()))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f'<style>{css}</style>{body}</svg>')


def card(x, y, w, h, r=6, fill=None, stroke=None):
    if fill is None:
        fill = CARD
    if stroke is None:
        stroke = EDGE
    return (f'<rect x="{x + .5:.1f}" y="{y + .5:.1f}" width="{w - 1:.1f}" height="{h - 1:.1f}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}"/>')


def label(x, y, s, color=None, size=11.5, anchor="start"):
    if color is None:
        color = MUTED
    return t(x, y, s, "bodyb", size, color, anchor, 0.5)


def tag(x, y, text, color=None, size=11.5, h=26, r=6):
    if color is None:
        color = BLUE
    w = tw(text, "monob", size, 0.5) + 20
    svg = (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{r}" fill="{color}" fill-opacity=".1" '
           f'stroke="{color}" stroke-opacity=".35"/>'
           + t(x + w / 2, y + h / 2 + 4, text, "monob", size, color, "middle", 0.5))
    return svg, w


def icon(slug, x, y, size, color):
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({size / 24:.4f})">'
            f'<path d="{ICONS[slug]["path"]}" fill="{color}"/></g>')


def mix(c, base=None, a=0.1):
    if base is None:
        base = CARD
    c, base = c.lstrip("#"), base.lstrip("#")
    return "#" + "".join(f"{round(int(c[i:i + 2], 16) * a + int(base[i:i + 2], 16) * (1 - a)):02x}" for i in (0, 2, 4))


def short(n):
    return f"{n / 1000:.1f}K".replace(".0K", "K") if n >= 1000 else str(n)


def clear_used():
    USED.clear()
