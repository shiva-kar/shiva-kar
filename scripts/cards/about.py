#!/usr/bin/env python3
"""About Me component: clear, human summary of focus and engineering background."""
import config
import kit
from kit import BODY, CARD, EDGE, TEXT, card, t


def about(w):
    m = w < 600
    pad = 22 if m else 32
    size = 14.5 if m else 15.5
    lh = int(size * 1.65)
    
    # Process text for wrapping
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
    
    maxw = w - 2 * pad
    sp = kit.tw(" ", "body", size)
    lines, cur, cw = [], [], 0
    for u in units:
        ww = sum(kit.tw(x, "bodyb" if b else "body", size) for x, b in u)
        if cur and cw + sp + ww > maxw:
            lines.append(cur)
            cur, cw = [], 0
        cw += (sp if cur else 0) + ww
        cur.append((u, ww))
    if cur:
        lines.append(cur)
    
    y = pad + size + 2
    body = []
    for ln in lines:
        x = pad
        for u, ww in ln:
            ux = x
            for word, bold in u:
                body.append(t(ux, y, word, "bodyb" if bold else "body", size, TEXT if bold else BODY))
                ux += kit.tw(word, "bodyb" if bold else "body", size)
            x += ww + sp
        y += lh
    
    h = y + pad - lh + 6
    return w, h, card(0, 0, w, h, 12, fill=CARD, stroke=EDGE) + "".join(body)

