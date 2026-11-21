#!/usr/bin/env python3
"""Featured projects component: in-depth engineering case studies with clear technical breakdowns."""
import config
import kit
from kit import BODY, CARD, CARD2, EDGE, GREEN, MUTED, TEXT, card, fit, t, wrap


def projects(w, data):
    m = w < 600
    gap = 10 if m else 12
    out = []
    cur_y = 0

    if not m:
        pad_x = 24
        pad_y = 18
        cw = w
        ch = 152

        for i, p in enumerate(config.PROJECTS):
            cy = i * (ch + gap)
            g = [card(0, cy, cw, ch, r=6, fill=CARD, stroke=EDGE)]

            # Title
            g.append(t(pad_x, cy + pad_y + 13, p["title"], "head", 16, "#ffffff"))

            # Category pill on right
            cat = p["category"]
            cat_w = kit.tw(cat, "mono", 11) + 16
            cat_x = cw - pad_x - cat_w
            g.append(f'<rect x="{cat_x:.1f}" y="{cy + pad_y:.1f}" width="{cat_w:.1f}" height="20" rx="4" fill="{CARD2}" stroke="{EDGE}"/>')
            g.append(t(cat_x + cat_w / 2, cy + pad_y + 14, cat, "mono", 11, GREEN, "middle"))

            # Tech stack line in clean monospace
            stack_text = p["stack"]
            g.append(t(pad_x, cy + pad_y + 34, fit(stack_text, "mono", 11.2, cw - 2 * pad_x), "mono", 11.2, GREEN))

            # Hairline divider
            div_y = cy + pad_y + 44
            g.append(f'<line x1="{pad_x}" x2="{cw - pad_x}" y1="{div_y}" y2="{div_y}" stroke="{EDGE}" stroke-width="1"/>')

            # Description
            desc_y = div_y + 18
            for ln in wrap(p["desc"], "body", 13, cw - 2 * pad_x, maxlines=1):
                g.append(t(pad_x, desc_y, ln, "body", 13, BODY))
                desc_y += 18

            # Highlights bullets
            hl_y = desc_y + 2
            for hl in p["highlights"][:2]:
                g.append(t(pad_x, hl_y, "◆", "body", 10.5, GREEN))
                g.append(t(pad_x + 14, hl_y, fit(hl, "body", 12.2, cw - 2 * pad_x - 14), "body", 12.2, MUTED))
                hl_y += 18

            out.append("".join(g))
            cur_y = cy + ch

        return w, cur_y, "".join(out)
    else:
        pad_x = 16
        pad_y = 16
        cw = w

        for i, p in enumerate(config.PROJECTS):
            card_start_y = cur_y
            g = []

            y = card_start_y + pad_y + 13
            # Title
            g.append(t(pad_x, y, p["title"], "head", 15, "#ffffff"))
            y += 20

            # Category pill
            cat = p["category"]
            cat_w = kit.tw(cat, "mono", 10.5) + 14
            g.append(f'<rect x="{pad_x}" y="{y - 12:.1f}" width="{cat_w:.1f}" height="18" rx="4" fill="{CARD2}" stroke="{EDGE}"/>')
            g.append(t(pad_x + cat_w / 2, y + 1, cat, "mono", 10.5, GREEN, "middle"))
            y += 18

            # Stack
            for ln in wrap(p["stack"], "mono", 10.5, cw - 2 * pad_x, maxlines=2):
                g.append(t(pad_x, y, ln, "mono", 10.5, GREEN))
                y += 15

            # Hairline divider
            y += 2
            g.append(f'<line x1="{pad_x}" x2="{cw - pad_x}" y1="{y}" y2="{y}" stroke="{EDGE}" stroke-width="1"/>')
            y += 16

            # Description
            for ln in wrap(p["desc"], "body", 12.5, cw - 2 * pad_x, maxlines=2):
                g.append(t(pad_x, y, ln, "body", 12.5, BODY))
                y += 17

            # Highlights
            y += 2
            for hl in p["highlights"][:2]:
                g.append(t(pad_x, y, "◆", "body", 10.5, GREEN))
                hl_lines = wrap(hl, "body", 11.5, cw - 2 * pad_x - 14, maxlines=2)
                for hll in hl_lines:
                    g.append(t(pad_x + 14, y, hll, "body", 11.5, MUTED))
                    y += 16

            card_h = y + pad_y - 10 - card_start_y
            out.append(card(0, card_start_y, cw, card_h, r=6, fill=CARD, stroke=EDGE) + "".join(g))
            cur_y = card_start_y + card_h + gap

        return w, cur_y - gap, "".join(out)



