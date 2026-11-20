#!/usr/bin/env python3
"""Career and education timeline components."""
from datetime import datetime

import config
import kit
from kit import BLUE, CARD, EDGE, EDGE2, GREEN, MUTED, PURPLE, TEXT, card, fit, label, t, tag, wrap


def _tl_row_desktop(w, y0, title, nodes, pad):
    n = len(nodes)
    colw = (w - 2 * pad) / n
    body = [label(pad, y0, title, BLUE, 11.5)]
    ly = y0 + 46
    xs = [pad + colw * (i + .5) for i in range(n)]
    body.append(f'<line x1="{xs[0]:.1f}" y1="{ly}" x2="{xs[-1]:.1f}" y2="{ly}" stroke="{EDGE2}" stroke-width="2"/>')
    maxy = ly
    for i, (yr, ttl, sub, live) in enumerate(nodes):
        x, col = xs[i], GREEN if live else BLUE
        body.append(t(x, ly - 14, yr, "monob", 11.5, col, "middle", 1.2))
        body.append(f'<circle cx="{x:.1f}" cy="{ly}" r="6" fill="{CARD}" stroke="{col}" stroke-width="2"/>'
                    f'<circle cx="{x:.1f}" cy="{ly}" r="2.5" fill="{col}"/>')
        yy = ly + 28
        for ln in wrap(ttl, "bodyb", 13.5, colw - 12, maxlines=2):
            body.append(t(x, yy, ln, "bodyb", 13.5, TEXT, "middle"))
            yy += 18
        yy += 2
        for ln in wrap(sub, "mono", 11.5, colw - 12, 0.5, 2):
            body.append(t(x, yy, fit(ln, "mono", 11.5, colw - 10, 0.5), "mono", 11.5, MUTED, "middle", 0.5))
            yy += 15
        maxy = max(maxy, yy)
    return "".join(body), maxy + 14


def _tl_row_mobile(w, y0, title, nodes, pad):
    body = [label(pad, y0, title, BLUE, 11)]
    y = y0 + 28
    top = y
    for yr, ttl, sub, live in nodes:
        col = GREEN if live else BLUE
        body.append(f'<circle cx="{pad + 6}" cy="{y - 4}" r="5" fill="{CARD}" stroke="{col}" stroke-width="2"/>'
                    f'<circle cx="{pad + 6}" cy="{y - 4}" r="2" fill="{col}"/>')
        body.append(t(pad + 24, y, yr, "monob", 11, col, ls=1.2))
        y += 20
        for ln in wrap(ttl, "bodyb", 13.5, w - 2 * pad - 28, maxlines=2):
            body.append(t(pad + 24, y, ln, "bodyb", 13.5, TEXT))
            y += 18
        for ln in wrap(sub, "mono", 11.5, w - 2 * pad - 28, 0.5, 2):
            body.append(t(pad + 24, y, fit(ln, "mono", 11.5, w - 2 * pad - 28, 0.5), "mono", 11.5, MUTED, ls=0.5))
            y += 15
        y += 14
    line = f'<line x1="{pad + 6}" y1="{top - 4}" x2="{pad + 6}" y2="{y - 34}" stroke="{EDGE2}" stroke-width="2"/>'
    return line + "".join(body), y


def timeline(w, data):
    m = w < 600
    pad = 22 if m else 30
    row1 = [(yr, ttl, inst, i == len(config.EDU) - 1) for i, (yr, ttl, inst, _, _) in enumerate(config.EDU)]
    row1.append(("2028 EXPECTED", "Graduation", "BCA, Amity University Online", False))
    months = {}
    for p in data.get("merged", []) + data.get("open", []):
        months.setdefault(p["date"][:7], []).append(p["repo"].split("/")[1])
    row2 = []
    for k, repos in sorted(months.items())[-5:]:
        top = max(set(repos), key=repos.count)
        mo = datetime.strptime(k, "%Y-%m").strftime("%b %Y").upper()
        row2.append([mo, f"{len(repos)} upstream PR{'s' if len(repos) > 1 else ''}", top, False])
    if row2:
        row2[-1][3] = True
    fn = _tl_row_mobile if m else _tl_row_desktop
    b1, y1 = fn(w, pad + 6, "EDUCATION", row1, pad)
    b2, y2 = fn(w, y1 + 18, "UPSTREAM CONTRIBUTIONS", [tuple(r) for r in row2], pad) if row2 else ("", y1)
    sep = (f'<line x1="{pad}" x2="{w - pad}" y1="{y1 + 4}" y2="{y1 + 4}" stroke="{EDGE2}" stroke-dasharray="3 5"/>'
           if row2 else "")
    h = y2 + pad - 8
    return w, h, card(0, 0, w, h) + b1 + sep + b2


def education(w):
    m = w < 600
    pad = 22 if m else 30
    body = [label(pad, pad + 10, "EDUCATION", BLUE, 11.5)]
    y = pad + 36
    for i, (_, _, inst, dates, degree) in enumerate(reversed(config.EDU)):
        body.append(f'<circle cx="{pad + 4}" cy="{y - 4}" r="3.5" fill="{[BLUE, GREEN, PURPLE][i % 3]}"/>')
        dw = 0 if m else kit.tw(dates, "mono", 11.5, 1.0) + 20
        if m:
            body.append(t(pad + 18, y, dates, "mono", 11, MUTED, ls=1))
            y += 18
        else:
            body.append(t(w - pad, y, dates, "mono", 11.5, MUTED, "end", 1.0))
        for ln in wrap(degree, "bodyb", 15, w - 2 * pad - 20 - dw):
            body.append(t(pad + 18, y, ln, "bodyb", 15, "#ffffff"))
            y += 20
        body.append(t(pad + 18, y, inst, "body", 13, MUTED))
        y += 30
        if i < len(config.EDU) - 1:
            body.append(f'<line x1="{pad + 18}" x2="{w - pad}" y1="{y - 16}" y2="{y - 16}" stroke="{EDGE}"/>')
    y += 8
    body.append(label(pad, y, "RELEVANT COURSEWORK", BLUE, 11.5))
    cx, cy = pad, y + 16
    for c in config.COURSES:
        s, wd = tag(cx, cy, c, BLUE, 11.5)
        if cx + wd > w - pad and cx > pad:
            cx, cy = pad, cy + 34
            s, wd = tag(cx, cy, c, BLUE, 11.5)
        body.append(s)
        cx += wd + 10
    h = cy + 28 + pad
    return w, h, card(0, 0, w, h) + "".join(body)
