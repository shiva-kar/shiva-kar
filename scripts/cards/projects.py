#!/usr/bin/env python3
"""Featured projects grid component."""
from datetime import datetime

import config
import kit
from kit import BLUE, BODY, CARD, EDGE, MUTED, ORANGE, card, fit, t, tag, wrap


def projects(w, data):
    m = w < 600
    gap, pad = 12, 18
    cw = w if m else (w - gap) / 2
    repos = [r for r in data.get("repos", []) if r["name"] not in config.EXCLUDE_REPOS and r.get("desc")]
    repos = sorted(repos, key=lambda r: (r.get("stars", 0), r.get("updated", "")), reverse=True)[:6]
    ch = 90 + 4 * 19 + 44
    per = 1 if m else 2
    out = []
    for i, r in enumerate(repos):
        mo = datetime.strptime(r["updated"], "%Y-%m-%d").strftime("%B %Y").upper()
        title = config.PROJECT_TITLES.get(r["name"], r["name"])
        g = [
            f'<rect x="0" y="20" width="3.5" height="18" rx="1.75" fill="{BLUE}"/>',
            t(pad, 33, mo, "monob", 11.5, MUTED, ls=1.2),
            t(cw - pad, 33, f"{r['stars']} STARS" if r["stars"] > 1 else (f"{r['stars']} STAR" if r["stars"] else "SOURCE"),
              "monob", 11.5, ORANGE if r["stars"] else MUTED, "end", 1.0),
            t(pad, 62, fit(title, "head", 17.5, cw - 2 * pad), "head", 17.5, "#ffffff")
        ]
        y = 86
        for ln in wrap(r["desc"], "body", 13.5, cw - 2 * pad - 6, maxlines=4):
            g.append(t(pad, y, ln, "body", 13.5, BODY))
            y += 19
        chips = config.PROJECT_CHIPS.get(r["name"]) or r.get("topics", [])[:3] or ([r["lang"]] if r.get("lang") else [])
        cx = pad
        for c in chips:
            s, wd = tag(cx, ch - 38, c, BLUE, 11, h=24)
            if cx + wd > cw - pad:
                break
            g.append(s)
            cx += wd + 8
        rr, cc = divmod(i, per)
        out.append(f'<g transform="translate({cc * (cw + gap):.1f} {rr * (ch + gap)})">'
                   + card(0, 0, cw, ch, r=10, fill=CARD, stroke=EDGE) + "".join(g) + "</g>")
    rows = (len(repos) + per - 1) // per
    return w, rows * (ch + gap) - gap, "".join(out)
