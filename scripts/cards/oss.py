#!/usr/bin/env python3
"""Open Source upstream contributions component: 2-column dashboard of merged and open work
with intelligent capping and dynamic repository aggregation to prevent profile sprawl.
"""
import config
import kit
from kit import CARD, EDGE, GREEN, MUTED, ORANGE, TEXT, card, t, wrap


def select_diverse_prs(prs_list, limit):
    """Selects up to `limit` PRs ensuring diversity across repositories,
    prioritizing the most recent PR from each unique repository first,
    then filling remaining slots with the newest PRs overall.
    """
    if len(prs_list) <= limit:
        return prs_list
    
    by_repo = {}
    for p in prs_list:
        r = p.get("repo", "other")
        by_repo.setdefault(r, []).append(p)
    
    selected = []
    # 1. Take latest from each repository
    for r, r_prs in by_repo.items():
        if len(selected) < limit:
            selected.append(r_prs[0])
            
    # 2. Fill remaining slots with newest PRs overall
    seen_keys = {(p["repo"], p["number"]) for p in selected}
    for p in prs_list:
        if len(selected) >= limit:
            break
        key = (p["repo"], p["number"])
        if key not in seen_keys:
            selected.append(p)
            seen_keys.add(key)
            
    return sorted(selected, key=lambda p: p.get("date", ""), reverse=True)


def build_repos_summary(data):
    """Dynamically aggregates merged and open contribution counts per repository."""
    repo_counts = {}
    for p in data.get("merged", []):
        r = p.get("repo", "")
        if r:
            repo_counts.setdefault(r, {"merged": 0, "open": 0})
            repo_counts[r]["merged"] += 1
    for p in data.get("open", []):
        r = p.get("repo", "")
        if r:
            repo_counts.setdefault(r, {"merged": 0, "open": 0})
            repo_counts[r]["open"] += 1

    summary = []
    for r, counts in sorted(repo_counts.items(), key=lambda x: -(x[1]["merged"] + x[1]["open"])):
        m_cnt = counts["merged"]
        o_cnt = counts["open"]
        parts = []
        if m_cnt > 0:
            parts.append(f"{m_cnt} merged")
        if o_cnt > 0:
            parts.append(f"{o_cnt} open")
        stat_str = " · ".join(parts) if parts else "contributor"
        desc = getattr(config, "REPO_DESCRIPTIONS", {}).get(r, "Open-source software contributions and upstream fixes")
        disp_name = r if len(r) <= 35 else r.split("/")[-1]
        summary.append((disp_name, stat_str, desc))
    return summary


def oss(w, data):
    m = w < 600
    pad = 20 if m else 28
    
    all_merged = sorted(data.get("merged", []), key=lambda p: p.get("date", ""), reverse=True)
    all_open = sorted(data.get("open", []), key=lambda p: p.get("date", ""), reverse=True)
    
    limit = getattr(config, "MAX_OSS_PRS_MOBILE", 5) if m else getattr(config, "MAX_OSS_PRS_PER_COL", 6)
    disp_merged = select_diverse_prs(all_merged, limit)
    disp_open = select_diverse_prs(all_open, limit)
    
    repos_summary = build_repos_summary(data)
    
    if not m:
        col_gap = 24
        col_w = (w - 2 * pad - col_gap) / 2
        
        # Left Column: Merged Pull Requests
        left_body = [
            t(pad, pad + 16, f"Merged Upstream ({len(all_merged)})", "bodyb", 16, GREEN)
        ]
        ly = pad + 40
        for i, p in enumerate(disp_merged):
            repo = p["repo"]
            num = f"#{p['number']}"
            title = p["title"]
            
            left_body.append(t(pad, ly, repo, "bodyb", 13.5, TEXT))
            left_body.append(t(pad + col_w, ly, num, "mono", 12, GREEN, "end"))
            ly += 18
            for ln in wrap(title, "body", 13, col_w, maxlines=2):
                left_body.append(t(pad, ly, ln, "body", 13, kit.BODY))
                ly += 17
            ly += 10
            if i < len(disp_merged) - 1:
                left_body.append(f'<line x1="{pad}" x2="{pad + col_w}" y1="{ly - 5}" y2="{ly - 5}" stroke="{EDGE}"/>')
        
        more_merged = len(all_merged) - len(disp_merged)
        if more_merged > 0:
            ly += 2
            left_body.append(t(pad, ly + 10, f"+ {more_merged} more merged pull requests on GitHub ↗", "mono", 11.5, GREEN))
            ly += 20
        
        # Left Bottom: Multi-Repository Ecosystem Breakdown (balances height with right column)
        ly += 8
        left_body.append(f'<line x1="{pad}" x2="{pad + col_w}" y1="{ly}" y2="{ly}" stroke="{EDGE}" stroke-width="1.5"/>')
        ly += 22
        left_body.append(t(pad, ly, "Repositories & Ecosystems", "bodyb", 15, TEXT))
        ly += 22
        for r_name, r_stat, r_desc in repos_summary:
            left_body.append(t(pad, ly, r_name, "bodyb", 13, TEXT))
            left_body.append(t(pad + col_w, ly, r_stat, "mono", 11.5, MUTED, "end"))
            ly += 17
            for ln in wrap(r_desc, "body", 12.5, col_w, maxlines=2):
                left_body.append(t(pad, ly, ln, "body", 12.5, kit.MUTED))
                ly += 16
            ly += 8
        
        # Right Column: Open Pull Requests
        right_x = pad + col_w + col_gap
        right_body = [
            t(right_x, pad + 16, f"Open Pull Requests ({len(all_open)})", "bodyb", 16, ORANGE)
        ]
        ry = pad + 40
        for i, p in enumerate(disp_open):
            repo = p["repo"]
            num = f"#{p['number']}"
            title = p["title"]
            
            right_body.append(t(right_x, ry, repo, "bodyb", 13.5, TEXT))
            right_body.append(t(w - pad, ry, num, "mono", 12, ORANGE, "end"))
            ry += 18
            for ln in wrap(title, "body", 13, col_w, maxlines=2):
                right_body.append(t(right_x, ry, ln, "body", 13, kit.BODY))
                ry += 17
            ry += 10
            if i < len(disp_open) - 1:
                right_body.append(f'<line x1="{right_x}" x2="{w - pad}" y1="{ry - 5}" y2="{ry - 5}" stroke="{EDGE}"/>')
        
        more_open = len(all_open) - len(disp_open)
        if more_open > 0:
            ry += 2
            right_body.append(t(right_x, ry + 10, f"+ {more_open} more open pull requests on GitHub ↗", "mono", 11.5, ORANGE))
            ry += 20
        
        total_h = max(ly, ry) + pad
        vsep = f'<line x1="{pad + col_w + col_gap / 2:.1f}" y1="{pad}" x2="{pad + col_w + col_gap / 2:.1f}" y2="{total_h - pad}" stroke="{EDGE}" stroke-width="1"/>'
        return w, total_h, card(0, 0, w, total_h, 6, fill=CARD, stroke=EDGE) + vsep + "".join(left_body) + "".join(right_body)
    
    else:
        # Mobile: Single-column stacked layout with capped display
        body = []
        cy = pad + 16
        body.append(t(pad, cy, f"Merged Upstream ({len(all_merged)})", "bodyb", 15, GREEN))
        cy += 24
        for i, p in enumerate(disp_merged):
            repo = p["repo"]
            num = f"#{p['number']}"
            title = p["title"]
            
            body.append(t(pad, cy, repo, "bodyb", 13, TEXT))
            body.append(t(w - pad, cy, num, "mono", 11.5, GREEN, "end"))
            cy += 18
            for ln in wrap(title, "body", 12.5, w - 2 * pad, maxlines=2):
                body.append(t(pad, cy, ln, "body", 12.5, kit.BODY))
                cy += 16
            cy += 8
            if i < len(disp_merged) - 1:
                body.append(f'<line x1="{pad}" x2="{w - pad}" y1="{cy - 4}" y2="{cy - 4}" stroke="{EDGE}"/>')
        
        more_merged = len(all_merged) - len(disp_merged)
        if more_merged > 0:
            cy += 2
            body.append(t(pad, cy + 10, f"+ {more_merged} more merged PRs on GitHub ↗", "mono", 11, GREEN))
            cy += 20
        
        cy += 16
        body.append(t(pad, cy, f"Open Pull Requests ({len(all_open)})", "bodyb", 15, ORANGE))
        cy += 24
        for i, p in enumerate(disp_open):
            repo = p["repo"]
            num = f"#{p['number']}"
            title = p["title"]
            
            body.append(t(pad, cy, repo, "bodyb", 13, TEXT))
            body.append(t(w - pad, cy, num, "mono", 11.5, ORANGE, "end"))
            cy += 18
            for ln in wrap(title, "body", 12.5, w - 2 * pad, maxlines=2):
                body.append(t(pad, cy, ln, "body", 12.5, kit.BODY))
                cy += 16
            cy += 8
            if i < len(disp_open) - 1:
                body.append(f'<line x1="{pad}" x2="{w - pad}" y1="{cy - 4}" y2="{cy - 4}" stroke="{EDGE}"/>')
        
        more_open = len(all_open) - len(disp_open)
        if more_open > 0:
            cy += 2
            body.append(t(pad, cy + 10, f"+ {more_open} more open PRs on GitHub ↗", "mono", 11, ORANGE))
            cy += 20
        
        # Mobile: Multi-Repository Ecosystem Breakdown
        cy += 8
        body.append(f'<line x1="{pad}" x2="{w - pad}" y1="{cy}" y2="{cy}" stroke="{EDGE}" stroke-width="1.5"/>')
        cy += 20
        body.append(t(pad, cy, "Repositories & Ecosystems", "bodyb", 14.5, TEXT))
        cy += 20
        for r_name, r_stat, r_desc in repos_summary:
            body.append(t(pad, cy, r_name, "bodyb", 12.5, TEXT))
            body.append(t(w - pad, cy, r_stat, "mono", 11, MUTED, "end"))
            cy += 17
            for ln in wrap(r_desc, "body", 12, w - 2 * pad, maxlines=2):
                body.append(t(pad, cy, ln, "body", 12, kit.MUTED))
                cy += 15
            cy += 8
        
        total_h = cy + pad
        return w, total_h, card(0, 0, w, total_h, 6, fill=CARD, stroke=EDGE) + "".join(body)
