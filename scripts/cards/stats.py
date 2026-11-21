#!/usr/bin/env python3
"""GitHub activity statistics, contribution heatmap, and language distribution component."""
from datetime import date

import config
import kit
from kit import BODY, CARD, CARD2, EDGE, GREEN, MUTED, ORANGE, TEXT, card, t

LANG_COL = {
    "TypeScript": "#3178c6",
    "JavaScript": "#f1e05a",
    "Java": "#f89820",
    "C": "#a8b9cc",
    "Python": "#3572a5",
    "C++": "#f34b7d",
    "Shell": "#89e051",
    "HTML": "#e34c26",
    "CSS": "#563d7c",
}


def stats(w, data):
    m = w < 600
    pad = 18 if m else 26
    cal = data.get("calendar", {})
    
    body = []
    
    # 1. Headline metrics in a clean row
    metrics = [
        ("Total Contributions", f"{cal.get('total', 0):,}"),
        ("Active Days", f"{cal.get('active_days', 0)} / 365"),
        ("Current Streak", f"{cal.get('current_streak', 0)} days"),
        ("Longest Streak", f"{cal.get('longest_streak', 0)} days"),
    ]
    
    m_cols = 2 if m else 4
    m_w = (w - 2 * pad - (m_cols - 1) * 12) / m_cols
    my = pad + 14
    for i, (lab, val) in enumerate(metrics):
        r, c = divmod(i, m_cols)
        cx = pad + c * (m_w + 12)
        cy = my + r * 50
        body.append(t(cx, cy, val, "bodyb", 17, "#ffffff"))
        body.append(t(cx, cy + 18, lab, "body", 12, MUTED))
    
    y = my + ((len(metrics) + m_cols - 1) // m_cols) * 50 + 10
    body.append(f'<line x1="{pad}" x2="{w - pad}" y1="{y}" y2="{y}" stroke="{EDGE}"/>')
    y += 20
    
    # 2. Contribution Heatmap
    weeks, col = [], None
    for d in cal.get("days", []):
        wd = (date.fromisoformat(d["date"]).weekday() + 1) % 7
        if col is None or wd == 0:
            col = [None] * 7
            weeks.append(col)
        col[wd] = d
    nweeks = 26 if m else 52
    weeks = weeks[-nweeks:]
    
    pitch = (w - 2 * pad) / nweeks
    lv = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    for wi, wk in enumerate(weeks):
        for di, d in enumerate(wk):
            if d:
                body.append(f'<rect x="{pad + wi * pitch:.1f}" y="{y + di * pitch:.1f}" width="{pitch - 2.5:.1f}" '
                            f'height="{pitch - 2.5:.1f}" rx="2" fill="{lv[d["level"]]}"/>')
    y += 7 * pitch + 24
    
    # 3. Language Bar
    languages = data.get("languages", [])
    if languages:
        body.append(f'<line x1="{pad}" x2="{w - pad}" y1="{y - 8}" y2="{y - 8}" stroke="{EDGE}"/>')
        y += 12
        body.append(t(pad, y, "Languages by Repository", "bodyb", 13.5, TEXT))
        y += 16
        
        total = sum(l["pct"] for l in languages) or 1
        bw = w - 2 * pad
        seg, x = [], pad
        for l in languages:
            sw = bw * l["pct"] / total
            seg.append(f'<rect x="{x:.1f}" y="{y}" width="{sw:.1f}" height="8" fill="{LANG_COL.get(l["name"], MUTED)}"/>')
            x += sw
        body.append(f'<defs><clipPath id="lb"><rect x="{pad}" y="{y}" width="{bw}" height="8" rx="4"/></clipPath></defs>'
                    f'<g clip-path="url(#lb)">{"".join(seg)}</g>')
        y += 24
        
        lc = 2 if m else 4
        lw = (w - 2 * pad) / lc
        for i, l in enumerate(languages):
            r, c = divmod(i, lc)
            lx, ly = pad + c * lw, y + r * 22
            body.append(f'<circle cx="{lx + 5}" cy="{ly - 4}" r="4" fill="{LANG_COL.get(l["name"], MUTED)}"/>')
            body.append(t(lx + 16, ly, f'{l["name"]} ({l["pct"]}%)', "body", 12, BODY))
        y += ((len(languages) + lc - 1) // lc) * 22
        
    h = y + pad - 6
    return w, h, card(0, 0, w, h, 10, fill=CARD, stroke=EDGE) + "".join(body)

