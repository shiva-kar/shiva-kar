#!/usr/bin/env python3
"""Open Source upstream contributions dashboard and standalone cards."""
import kit
from kit import BLUE, CARD, CARD2, EDGE, EDGE2, GREEN, MUTED, ORANGE, TEXT, card, fit, label, short, t, wrap


def oss(w, data):
    m = w < 600
    pad = 18 if m else 24
    stars = data.get("upstream_stars", {})
    names = sorted([r for r in stars if stars[r] > 0], key=lambda r: -stars[r])

    pills_body = []
    gap, ph = 8, 28
    sized = []
    for n in names:
        lw = kit.tw(n, "monob", 11.5, .5) + 12
        sw = kit.tw(f"★ {short(stars[n])}", "monob", 11.5, .5) + 12
        sized.append((n, lw, sw, lw + sw + 16))

    rows, cur, cw_acc = [], [], 0
    max_w = w - 2 * pad
    for it in sized:
        if cur and cw_acc + gap + it[3] > max_w:
            rows.append((cur, cw_acc))
            cur, cw_acc = [], 0
        cw_acc += (gap if cur else 0) + it[3]
        cur.append(it)
    rows.append((cur, cw_acc))

    py = pad + 18
    pills_body.append(label(pad, py - 4, "UPSTREAM REPOSITORIES", BLUE, 11.5))
    py += 12
    for r, (row, rw) in enumerate(rows):
        x = pad
        for n, lw, sw, pw in row:
            pills_body.append(f'<rect x="{x + .5:.1f}" y="{py + .5}" width="{pw - 1:.1f}" height="{ph - 1}" rx="14" fill="{CARD2}" stroke="{EDGE2}"/>')
            pills_body.append(t(x + 12, py + 18.5, n, "monob", 11.5, TEXT, ls=.5))
            pills_body.append(t(x + lw + 8, py + 18.5, f"★ {short(stars[n])}", "monob", 11.5, ORANGE, ls=.5))
            x += pw + gap
        py += ph + 8

    divider_y = py + 6
    pills_body.append(f'<line x1="{pad}" y1="{divider_y}" x2="{w - pad}" y2="{divider_y}" stroke="{EDGE2}" stroke-width="1"/>')
    y_content = divider_y + 16

    merged_rows = [(p["repo"], f"#{p['number']}", p["title"], p.get("date", ""))
                   for p in sorted(data.get("merged", []), key=lambda p: p.get("date", ""), reverse=True)]

    open_groups = {}
    for p in sorted(data.get("open", []), key=lambda p: p.get("date", ""), reverse=True):
        open_groups.setdefault(p["repo"], []).append(p)
    open_rows = []
    for repo, ps in open_groups.items():
        nums = ", ".join(f"#{p['number']}" for p in ps[:3]) + (f" +{len(ps) - 3}" if len(ps) > 3 else "")
        open_rows.append((repo, nums, "; ".join(p["title"] for p in ps)))

    if not m:
        col_gap = 20
        col_w = (w - 2 * pad - col_gap) / 2

        # Left: Merged
        left_body = []
        ly = y_content
        badge_text = f"{len(merged_rows)} MERGED UPSTREAM"
        bw = kit.tw(badge_text, "monob", 11.5, 1) + 20
        left_body.append(f'<rect x="{pad}" y="{ly}" width="{bw:.1f}" height="24" rx="6" fill="{GREEN}" fill-opacity=".15" stroke="{GREEN}" stroke-opacity=".4"/>'
                         + t(pad + bw / 2, ly + 16, badge_text, "monob", 11.5, GREEN, "middle", 1))
        ly += 36
        for i, (repo, num, desc, dt) in enumerate(merged_rows):
            left_body.append(f'<circle cx="{pad + 4}" cy="{ly + 2}" r="3.5" fill="{GREEN}"/>')
            left_body.append(t(pad + 16, ly + 6, f"{repo} {num}", "bodyb", 13.5, TEXT))
            ly += 22
            for ln in wrap(desc, "body", 12, col_w - 20, maxlines=2):
                left_body.append(t(pad + 16, ly, ln, "body", 12, MUTED))
                ly += 16
            ly += 8
            if i < len(merged_rows) - 1:
                left_body.append(f'<line x1="{pad + 16}" x2="{pad + col_w}" y1="{ly - 4}" y2="{ly - 4}" stroke="{EDGE}"/>')

        # Right: Open
        right_x = pad + col_w + col_gap
        right_body = []
        ry = y_content
        badge_open = f"{len(data.get('open', []))} OPEN PRS"
        obw = kit.tw(badge_open, "monob", 11.5, 1) + 20
        right_body.append(f'<rect x="{right_x}" y="{ry}" width="{obw:.1f}" height="24" rx="6" fill="{ORANGE}" fill-opacity=".15" stroke="{ORANGE}" stroke-opacity=".4"/>'
                          + t(right_x + obw / 2, ry + 16, badge_open, "monob", 11.5, ORANGE, "middle", 1))
        ry += 36
        for i, (repo, nums, desc) in enumerate(open_rows):
            right_body.append(f'<circle cx="{right_x + 4}" cy="{ry + 2}" r="3.5" fill="{ORANGE}"/>')
            right_body.append(t(right_x + 16, ry + 6, repo, "bodyb", 13.5, TEXT))
            right_body.append(t(w - pad, ry + 6, nums, "mono", 11.5, MUTED, "end", .5))
            ry += 22
            for ln in wrap(desc, "body", 12, col_w - 20, maxlines=2):
                right_body.append(t(right_x + 16, ry, ln, "body", 12, MUTED))
                ry += 16
            ry += 8
            if i < len(open_rows) - 1:
                right_body.append(f'<line x1="{right_x + 16}" x2="{w - pad}" y1="{ry - 4}" y2="{ry - 4}" stroke="{EDGE}"/>')

        total_h = max(ly, ry) + pad
        vsep = f'<line x1="{pad + col_w + col_gap / 2:.1f}" y1="{y_content}" x2="{pad + col_w + col_gap / 2:.1f}" y2="{total_h - pad}" stroke="{EDGE2}" stroke-width="1"/>'
        return w, total_h, card(0, 0, w, total_h) + "".join(pills_body) + vsep + "".join(left_body) + "".join(right_body)
    else:
        m_body = []
        cy = y_content
        badge_text = f"{len(merged_rows)} MERGED UPSTREAM"
        bw = kit.tw(badge_text, "monob", 11, 1) + 18
        m_body.append(f'<rect x="{pad}" y="{cy}" width="{bw:.1f}" height="24" rx="6" fill="{GREEN}" fill-opacity=".15" stroke="{GREEN}" stroke-opacity=".4"/>'
                      + t(pad + bw / 2, cy + 16, badge_text, "monob", 11, GREEN, "middle", 1))
        cy += 34
        for i, (repo, num, desc, _) in enumerate(merged_rows):
            m_body.append(f'<circle cx="{pad + 4}" cy="{cy + 2}" r="3" fill="{GREEN}"/>')
            m_body.append(t(pad + 16, cy + 6, f"{repo} {num}", "bodyb", 13, TEXT))
            cy += 20
            for ln in wrap(desc, "body", 11.5, w - 2 * pad - 16, maxlines=2):
                m_body.append(t(pad + 16, cy, ln, "body", 11.5, MUTED))
                cy += 15
            cy += 8
            if i < len(merged_rows) - 1:
                m_body.append(f'<line x1="{pad + 16}" x2="{w - pad}" y1="{cy - 4}" y2="{cy - 4}" stroke="{EDGE}"/>')

        cy += 14
        badge_open = f"{len(data.get('open', []))} OPEN PRS"
        obw = kit.tw(badge_open, "monob", 11, 1) + 18
        m_body.append(f'<rect x="{pad}" y="{cy}" width="{obw:.1f}" height="24" rx="6" fill="{ORANGE}" fill-opacity=".15" stroke="{ORANGE}" stroke-opacity=".4"/>'
                      + t(pad + obw / 2, cy + 16, badge_open, "monob", 11, ORANGE, "middle", 1))
        cy += 34
        for i, (repo, nums, desc) in enumerate(open_rows):
            m_body.append(f'<circle cx="{pad + 4}" cy="{cy + 2}" r="3" fill="{ORANGE}"/>')
            m_body.append(t(pad + 16, cy + 6, repo, "bodyb", 13, TEXT))
            cy += 20
            for ln in wrap(desc, "body", 11.5, w - 2 * pad - 16, maxlines=2):
                m_body.append(t(pad + 16, cy, ln, "body", 11.5, MUTED))
                cy += 15
            cy += 8
            if i < len(open_rows) - 1:
                m_body.append(f'<line x1="{pad + 16}" x2="{w - pad}" y1="{cy - 4}" y2="{cy - 4}" stroke="{EDGE}"/>')

        total_h = cy + pad
        return w, total_h, card(0, 0, w, total_h) + "".join(pills_body) + "".join(m_body)


def oss_repos(w, data):
    stars = data.get("upstream_stars", {})
    names = sorted([r for r in stars if stars[r] > 0], key=lambda r: -stars[r])
    gap, ph = 8, 28
    sized = []
    for n in names:
        lw, sw = kit.tw(n, "monob", 11.5, .5), kit.tw(f"★ {short(stars[n])}", "monob", 11.5, .5)
        sized.append((n, lw, sw, lw + sw + 36))
    rows, cur, cw = [], [], 0
    for it in sized:
        if cur and cw + gap + it[3] > w:
            rows.append((cur, cw))
            cur, cw = [], 0
        cw += (gap if cur else 0) + it[3]
        cur.append(it)
    rows.append((cur, cw))
    body = []
    for r, (row, rw) in enumerate(rows):
        x, y = (w - rw) / 2, r * (ph + 8)
        for n, lw, sw, pw in row:
            body.append(f'<rect x="{x + .5:.1f}" y="{y + .5}" width="{pw - 1:.1f}" height="{ph - 1}" rx="14" fill="{CARD2}" stroke="{EDGE2}"/>')
            body.append(t(x + 12, y + 18.5, n, "monob", 11.5, TEXT, ls=.5))
            body.append(t(x + 12 + lw + 8, y + 18.5, f"★ {short(stars[n])}", "monob", 11.5, ORANGE, ls=.5))
            x += pw + gap
    return w, len(rows) * (ph + 8) - 8, "".join(body)


def _pr_card(w, head, color, rows):
    pad = 18 if w < 600 else 22
    y = pad + 14
    body = [t(pad, y, head, "monob", 11.5, color, ls=1.5)]
    y += 14
    for i, (repo, nums, desc) in enumerate(rows):
        y += 10
        body.append(f'<circle cx="{pad + 3}" cy="{y + 2}" r="3.5" fill="{color}"/>')
        rw = kit.tw(nums, "mono", 11, .5)
        body.append(t(w - pad, y + 6, nums, "mono", 11, MUTED, "end", .5))
        body.append(t(pad + 16, y + 7, fit(repo, "bodyb", 14, w - 2 * pad - 30 - rw), "bodyb", 14, TEXT))
        y += 24
        for ln in wrap(desc, "body", 12, w - 2 * pad - 16, maxlines=2):
            body.append(t(pad + 16, y, ln, "body", 12, MUTED))
            y += 16
        y += 8
        if i < len(rows) - 1:
            body.append(f'<line x1="{pad + 16}" x2="{w - pad}" y1="{y - 8}" y2="{y - 8}" stroke="{EDGE}"/>')
    h = y + pad - 8
    return w, h, card(0, 0, w, h) + "".join(body)


def oss_merged(w, data):
    rows = [(p["repo"], f"#{p['number']}", p["title"])
            for p in sorted(data.get("merged", []), key=lambda p: p.get("date", ""), reverse=True)]
    return _pr_card(w, f"{len(rows)} MERGED UPSTREAM | NEWEST FIRST", GREEN, rows)


def oss_open(w, data):
    groups = {}
    for p in sorted(data.get("open", []), key=lambda p: p.get("date", ""), reverse=True):
        open_groups = groups.setdefault(p["repo"], []).append(p)
    rows = []
    for repo, ps in groups.items():
        nums = ", ".join(f"#{p['number']}" for p in ps[:3]) + (f" +{len(ps) - 3}" if len(ps) > 3 else "")
        rows.append((repo, nums, "; ".join(p["title"] for p in ps)))
    return _pr_card(w, f"{len(data.get('open', []))} OPEN PRS", ORANGE, rows)
