#!/usr/bin/env python3
"""Featured projects grid component."""
import config
import kit
from kit import BODY, CARD, CARD2, EDGE, MUTED, ORANGE, TEXT, card, fit, t, wrap


def projects(w, data):
    m = w < 600
    gap = 12
    pad = 18 if m else 22
    cw = w if m else (w - gap) / 2
    repos = [r for r in data.get("repos", []) if r["name"] not in config.EXCLUDE_REPOS and r.get("desc")]
    repos = sorted(repos, key=lambda r: (r.get("stars", 0), r.get("updated", "")), reverse=True)[:6]
    ch = 180 if m else 190
    per = 1 if m else 2
    out = []
    
    for i, r in enumerate(repos):
        title = config.PROJECT_TITLES.get(r["name"], r["name"])
        star_str = f"★ {r['stars']}" if r.get("stars", 0) > 0 else ""
        
        star_w = kit.tw(star_str, "bodyb", 12.5) if star_str else 0
        title_max_w = cw - 2 * pad - (star_w + 12 if star_str else 0)
        
        g = [
            t(pad, pad + 16, fit(title, "head", 17, title_max_w), "head", 17, "#ffffff")
        ]
        if star_str:
            g.append(t(cw - pad, pad + 15, star_str, "bodyb", 12.5, ORANGE, "end"))
        
        desc_y = pad + 40
        desc_lines = wrap(r["desc"], "body", 13, cw - 2 * pad, maxlines=3)
        for ln in desc_lines:
            g.append(t(pad, desc_y, ln, "body", 13, BODY))
            desc_y += 18
            
        chips = config.PROJECT_CHIPS.get(r["name"]) or r.get("topics", [])[:3] or ([r["lang"]] if r.get("lang") else [])
        if chips:
            tech_line = " · ".join(chips)
            g.append(t(pad, ch - pad, fit(tech_line, "body", 12, cw - 2 * pad), "body", 12, MUTED))
            
        rr, cc = divmod(i, per)
        out.append(f'<g transform="translate({cc * (cw + gap):.1f} {rr * (ch + gap)})">'
                   + card(0, 0, cw, ch, r=10, fill=CARD, stroke=EDGE) + "".join(g) + "</g>")
                   
    rows = (len(repos) + per - 1) // per
    return w, rows * (ch + gap) - gap, "".join(out)

