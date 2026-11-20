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

# Palette: GitHub-native dark tones, restrained semantic accents, zero fluorescent cyan
CARD, CARD2, EDGE, EDGE2 = "#0d1117", "#161b22", "#21262d", "#30363d"
BLUE, GREEN, ORANGE, PURPLE = "#58a6ff", "#3fb950", "#d29922", "#bc8cff"
TEXT, BODY, MUTED = "#f0f6fc", "#c9d1d9", "#8b949e"

FONTS = {
    "body": ("Inter", 400, "inter-latin-400-normal.woff2"),
    "bodyb": ("Inter", 600, "inter-latin-600-normal.woff2"),
    "mono": ("JetBrains Mono", 500, "jetbrains-mono-latin-500-normal.woff2"),
    "monob": ("JetBrains Mono", 700, "jetbrains-mono-latin-700-normal.woff2"),
    "head": ("Archivo Black", 400, "archivo-black-latin-400-normal.woff2"),
}
STACKS = {
    "Inter": "Inter, 'Segoe UI', system-ui, sans-serif",
    "JetBrains Mono": "'JetBrains Mono', ui-monospace, Consolas, monospace",
    "Archivo Black": "'Archivo Black', Impact, 'Arial Black', sans-serif",
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
        font = TTFont(os.path.join(FD, FONTS[k][2]))
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


def t(x, y, s, k="body", size=14, fill=BODY, anchor="start", ls=0.0, extra=""):
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
    css = "".join(face_css(k, c) for k, c in USED.items())
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f'<style>{css}</style>{body}</svg>')


def card(x, y, w, h, r=12, fill=CARD, stroke=EDGE):
    return (f'<rect x="{x + .5:.1f}" y="{y + .5:.1f}" width="{w - 1:.1f}" height="{h - 1:.1f}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}"/>')


def label(x, y, s, color=BLUE, size=11.5, anchor="start"):
    return t(x, y, s, "monob", size, color, anchor, 2.0)


def tag(x, y, text, color=BLUE, size=11.5, h=26, r=6):
    w = tw(text, "monob", size, 0.5) + 20
    svg = (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{r}" fill="{color}" fill-opacity=".1" '
           f'stroke="{color}" stroke-opacity=".35"/>'
           + t(x + w / 2, y + h / 2 + 4, text, "monob", size, color, "middle", 0.5))
    return svg, w


def icon(slug, x, y, size, color):
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({size / 24:.4f})">'
            f'<path d="{ICONS[slug]["path"]}" fill="{color}"/></g>')


def mix(c, base=CARD, a=0.1):
    c, base = c.lstrip("#"), base.lstrip("#")
    return "#" + "".join(f"{round(int(c[i:i + 2], 16) * a + int(base[i:i + 2], 16) * (1 - a)):02x}" for i in (0, 2, 4))


def short(n):
    return f"{n / 1000:.1f}K".replace(".0K", "K") if n >= 1000 else str(n)


def clear_used():
    USED.clear()
