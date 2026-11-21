#!/usr/bin/env python3
"""Featured projects grid component: cohesive cards with clear hierarchy and authentic tags."""
import config
import kit
from kit import BODY, CARD, CARD2, EDGE, MUTED, ORANGE, TEXT, card, fit, t, wrap


def projects(w, data):
    m = w < 600
    gap = 12
    pad = 16 if m else 20
    cw = w if m else (w - gap) / 2
    repos = [r for r in data.get("repos", []) if r["name"] not in config.EXCLUDE_REPOS and r.get("desc")]
    repos = sorted(repos, key=lambda r: (r.get("stars", 0), r.get("updated", "")), reverse=True)[:6]
    ch = 152 if m else 156
    per = 1 if m else 2
    out = []
    
    for i, r in enumerate(repos):
        title = config.PROJECT_TITLES.get(r["name"], r["name"])
        star_str = f"★ {r['stars']}" if r.get("stars", 0) > 0 else ""
        
        star_w = kit.tw(star_str, "bodyb", 12.5) if star_str else 0
        title_max_w = cw - 2 * pad - (star_w + 12 if star_str else 0)
        
        g = [
            t(pad, pad + 15, fit(title, "head", 16.5, title_max_w), "head", 16.5, "#ffffff")
        ]
        if star_str:
            g.append(t(cw - pad, pad + 14, star_str, "bodyb", 12.5, ORANGE, "end"))
        
        desc_y = pad + 38
        desc_lines = wrap(r["desc"], "body", 13, cw - 2 * pad, maxlines=3)
        for ln in desc_lines:
            g.append(t(pad, desc_y, ln, "body", 13, BODY))
            desc_y += 18.5
            
        chips = config.PROJECT_CHIPS.get(r["name"]) or r.get("topics", [])[:3] or ([r["lang"]] if r.get("lang") else [])
        if chips:
            chip_x = pad
            for chip in chips:
                tw_val = kit.tw(chip, "body", 11.5)
                chip_w = tw_val + 14
                if chip_x + chip_w > cw - pad:
                    break
                g.append(f'<rect x="{chip_x:.1f}" y="{ch - pad - 19}" width="{chip_w:.1f}" height="22" rx="4" fill="{CARD2}" stroke="{EDGE}"/>')
                g.append(t(chip_x + chip_w / 2, ch - pad - 4, chip, "body", 11.5, MUTED, "middle"))
                chip_x += chip_w + 6
            
        rr, cc = divmod(i, per)
        out.append(f'<g transform="translate({cc * (cw + gap):.1f} {rr * (ch + gap)})">'
                   + card(0, 0, cw, ch, r=8, fill=CARD, stroke=EDGE) + "".join(g) + "</g>")
                   
    rows = (len(repos) + per - 1) // per
    return w, rows * (ch + gap) - gap, "".join(out)


