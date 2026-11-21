#!/usr/bin/env python3
"""Career and education components: clean academic background and coursework."""
import config
from kit import CARD, EDGE, MUTED, TEXT, card, t, wrap


def education(w):
    m = w < 600
    pad = 18 if m else 26
    body = []
    y = pad + 14
    
    for i, (_, _, inst, dates, degree) in enumerate(reversed(config.EDU)):
        # Date
        if m:
            body.append(t(pad, y, dates, "body", 11.5, MUTED))
            y += 18
        else:
            body.append(t(w - pad, y + 2, dates, "body", 12, MUTED, "end"))
            
        # Degree / School
        dw = 0 if m else 160
        for ln in wrap(degree, "bodyb", 14.5, w - 2 * pad - dw):
            body.append(t(pad, y, ln, "bodyb", 14.5, TEXT))
            y += 20
        body.append(t(pad, y, inst, "body", 13, MUTED))
        y += 24
        
        if i < len(config.EDU) - 1:
            body.append(f'<line x1="{pad}" x2="{w - pad}" y1="{y - 8}" y2="{y - 8}" stroke="{EDGE}"/>')
            y += 12
            
    # Coursework as clean, plain text
    if config.COURSES:
        body.append(f'<line x1="{pad}" x2="{w - pad}" y1="{y - 4}" y2="{y - 4}" stroke="{EDGE}"/>')
        y += 16
        body.append(t(pad, y, "Coursework", "bodyb", 13, TEXT))
        y += 20
        course_text = " · ".join(config.COURSES)
        for ln in wrap(course_text, "body", 12.5, w - 2 * pad):
            body.append(t(pad, y, ln, "body", 12.5, MUTED))
            y += 18
            
    h = y + pad - 6
    return w, h, card(0, 0, w, h, 6, fill=CARD, stroke=EDGE) + "".join(body)
