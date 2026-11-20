#!/usr/bin/env python3
"""About Me component: highlights engineering domains and areas of interest."""
import config
import kit
from kit import BLUE, BODY, card, label, t, tag


def about(w):
    m = w < 600
    pad = 22 if m else 30
    size = 14.5 if m else 15.5
    lh = int(size * 1.6)
    units, glue = [], False
    for i, part in enumerate(config.ABOUT.split("**")):
        bold = i % 2 == 1
        words = part.split()
        if not words:
            continue
        for j, word in enumerate(words):
            attached = j == 0 and glue and not part[:1].isspace()
            if attached and units:
                units[-1].append((word, bold))
            else:
                units.append([(word, bold)])
        glue = not part[-1:].isspace()
    maxw = w - 2 * pad - 8
    sp = kit.tw(" ", "body", size)
    lines, cur, cw = [], [], 0
    for u in units:
        ww = sum(kit.tw(x, "bodyb" if b else "body", size) for x, b in u)
        if cur and cw + sp + ww > maxw:
            lines.append(cur)
            cur, cw = [], 0
        cw += (sp if cur else 0) + ww
        cur.append((u, ww))
    lines.append(cur)
    y = pad + 20
    body = [label(pad + 8, y, "ABOUT", BLUE, 11.5)]
    y += 24
    for ln in lines:
        x = pad + 8
        for u, ww in ln:
            ux = x
            for word, bold in u:
                body.append(t(ux, y, word, "bodyb" if bold else "body", size, "#ffffff" if bold else BODY))
                ux += kit.tw(word, "bodyb" if bold else "body", size)
            x += ww + sp
        y += lh
    tx, ty = pad + 8, y + 6
    for tg in config.TAGS:
        s, wd = tag(tx, ty, tg, BLUE, 11.5)
        if tx + wd > w - pad and tx > pad + 8:
            tx, ty = pad + 8, ty + 34
            s, wd = tag(tx, ty, tg, BLUE, 11.5)
        body.append(s)
        tx += wd + 10
    h = ty + 28 + pad
    return w, h, card(0, 0, w, h) + f'<rect x="0" y="16" width="3.5" height="{h - 32}" rx="1.75" fill="{BLUE}"/>' + "".join(body)
