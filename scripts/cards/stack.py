#!/usr/bin/env python3
"""Tech stack component: clean, static categorized grid of technologies and tools."""
from kit import BODY, CARD, EDGE, ICONS, TEXT, card, icon, t


CATEGORIES = [
    ("Backend & Data", [
        ("Java", "openjdk", "#f89820"),
        ("Spring Boot", "springboot", "#6db33f"),
        ("Hibernate", "hibernate", "#b7c0c8"),
        ("PostgreSQL", "postgresql", "#4169e1"),
        ("MySQL", "mysql", "#5aa5d6"),
        ("Redis", "redis", "#dc382d"),
    ]),
    ("Systems & Engines", [
        ("C", "c", "#a8b9cc"),
        ("C++", "cplusplus", "#4aa3e0"),
        ("Godot Engine", "godotengine", "#478cbf"),
        ("Linux", "linux", "#fcc624"),
        ("CMake", "cmake", "#3b8fd6"),
        ("Docker", "docker", "#2496ed"),
    ]),
    ("Frontend & Web", [
        ("TypeScript", "typescript", "#3178c6"),
        ("JavaScript", "javascript", "#f7df1e"),
        ("React", "react", "#61dafb"),
        ("Tailwind CSS", "tailwindcss", "#06b6d4"),
        ("Python", "python", "#3776ab"),
        ("HTML5", "html5", "#e34f26"),
    ]),
    ("Workflow & Testing", [
        ("Git", "git", "#f05032"),
        ("GitHub", "github", "#e6edf3"),
        ("Maven", "apachemaven", "#c71a36"),
        ("JUnit 5", "junit5", "#25a162"),
        ("Postman", "postman", "#ff6c37"),
        ("IntelliJ IDEA", "intellijidea", "#fe315d"),
    ]),
]


def marquee(w):
    """Static, non-animated grid of technical skills."""
    m = w < 600
    pad = 16 if m else 20
    gap = 12
    cols = 1 if m else 2
    cw = w if m else (w - gap) / 2
    
    body = []
    card_y = 0
    
    # We display 4 category cards
    for idx, (cat_name, items) in enumerate(CATEGORIES):
        r, c = divmod(idx, cols)
        cx = 0 if m else c * (cw + gap)
        ch = 142
        cy = r * (ch + gap)
        
        cb = [
            card(cx, cy, cw, ch, 8, fill=CARD, stroke=EDGE),
            t(cx + pad, cy + pad + 12, cat_name, "bodyb", 14.5, TEXT),
        ]
        
        # 2 columns of items inside each category
        icols = 2
        iw = (cw - 2 * pad) / icols
        for i, (name, slug, col) in enumerate(items):
            ir, ic = divmod(i, icols)
            ix = cx + pad + ic * iw
            iy = cy + pad + 38 + ir * 30
            
            c_color = col or ("#" + ICONS[slug]["hex"] if slug in ICONS else "#ffffff")
            if slug and slug in ICONS:
                cb.append(icon(slug, ix, iy - 14, 18, c_color))
                cb.append(t(ix + 26, iy, name, "body", 12.5, BODY))
            else:
                cb.append(t(ix, iy, name, "body", 12.5, BODY))
                
        body.append("".join(cb))
        card_y = max(card_y, cy + ch)
        
    total_h = card_y
    return w, total_h, "".join(body)

