#!/usr/bin/env python3
"""Open Source upstream contributions component: 2-column dashboard of merged and open work."""
import kit
from kit import CARD, EDGE, GREEN, MUTED, ORANGE, TEXT, card, t, wrap


def oss(w, data):
    m = w < 600
    pad = 20 if m else 28
    
    merged_prs = sorted(data.get("merged", []), key=lambda p: p.get("date", ""), reverse=True)
    open_prs = sorted(data.get("open", []), key=lambda p: p.get("date", ""), reverse=True)
    
    if not m:
        col_gap = 24
        col_w = (w - 2 * pad - col_gap) / 2
        
        # Left: Merged
        left_body = [
            t(pad, pad + 16, f"Merged Upstream ({len(merged_prs)})", "bodyb", 16, GREEN)
        ]
        ly = pad + 40
        for i, p in enumerate(merged_prs):
            repo = p["repo"]
            num = f"#{p['number']}"
            title = p["title"]
            dt = p.get("date", "")
            
            num_w = kit.tw(num, "mono", 12)
            left_body.append(t(pad, ly, repo, "bodyb", 13.5, TEXT))
            left_body.append(t(pad + col_w, ly, num, "mono", 12, MUTED, "end"))
            ly += 18
            for ln in wrap(title, "body", 12.5, col_w, maxlines=2):
                left_body.append(t(pad, ly, ln, "body", 12.5, MUTED))
                ly += 16
            ly += 10
            if i < len(merged_prs) - 1:
                left_body.append(f'<line x1="{pad}" x2="{pad + col_w}" y1="{ly - 5}" y2="{ly - 5}" stroke="{EDGE}"/>')
        
        # Right: Open
        right_x = pad + col_w + col_gap
        right_body = [
            t(right_x, pad + 16, f"Open Pull Requests ({len(open_prs)})", "bodyb", 16, ORANGE)
        ]
        ry = pad + 40
        for i, p in enumerate(open_prs):
            repo = p["repo"]
            num = f"#{p['number']}"
            title = p["title"]
            
            right_body.append(t(right_x, ry, repo, "bodyb", 13.5, TEXT))
            right_body.append(t(w - pad, ry, num, "mono", 12, MUTED, "end"))
            ry += 18
            for ln in wrap(title, "body", 12.5, col_w, maxlines=2):
                right_body.append(t(right_x, ry, ln, "body", 12.5, MUTED))
                ry += 16
            ry += 10
            if i < len(open_prs) - 1:
                right_body.append(f'<line x1="{right_x}" x2="{w - pad}" y1="{ry - 5}" y2="{ry - 5}" stroke="{EDGE}"/>')
        
        total_h = max(ly, ry) + pad
        vsep = f'<line x1="{pad + col_w + col_gap / 2:.1f}" y1="{pad}" x2="{pad + col_w + col_gap / 2:.1f}" y2="{total_h - pad}" stroke="{EDGE}" stroke-width="1"/>'
        return w, total_h, card(0, 0, w, total_h, 12, fill=CARD, stroke=EDGE) + vsep + "".join(left_body) + "".join(right_body)
    else:
        body = []
        cy = pad + 16
        body.append(t(pad, cy, f"Merged Upstream ({len(merged_prs)})", "bodyb", 15, GREEN))
        cy += 24
        for i, p in enumerate(merged_prs):
            repo = p["repo"]
            num = f"#{p['number']}"
            title = p["title"]
            
            body.append(t(pad, cy, repo, "bodyb", 13, TEXT))
            body.append(t(w - pad, cy, num, "mono", 11.5, MUTED, "end"))
            cy += 18
            for ln in wrap(title, "body", 12, w - 2 * pad, maxlines=2):
                body.append(t(pad, cy, ln, "body", 12, MUTED))
                cy += 16
            cy += 8
            if i < len(merged_prs) - 1:
                body.append(f'<line x1="{pad}" x2="{w - pad}" y1="{cy - 4}" y2="{cy - 4}" stroke="{EDGE}"/>')
        
        cy += 16
        body.append(t(pad, cy, f"Open Pull Requests ({len(open_prs)})", "bodyb", 15, ORANGE))
        cy += 24
        for i, p in enumerate(open_prs):
            repo = p["repo"]
            num = f"#{p['number']}"
            title = p["title"]
            
            body.append(t(pad, cy, repo, "bodyb", 13, TEXT))
            body.append(t(w - pad, cy, num, "mono", 11.5, MUTED, "end"))
            cy += 18
            for ln in wrap(title, "body", 12, w - 2 * pad, maxlines=2):
                body.append(t(pad, cy, ln, "body", 12, MUTED))
                cy += 16
            cy += 8
            if i < len(open_prs) - 1:
                body.append(f'<line x1="{pad}" x2="{w - pad}" y1="{cy - 4}" y2="{cy - 4}" stroke="{EDGE}"/>')
        
        total_h = cy + pad
        return w, total_h, card(0, 0, w, total_h, 12, fill=CARD, stroke=EDGE) + "".join(body)

