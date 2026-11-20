#!/usr/bin/env python3
"""Renders every SVG card used by README.md into assets/svg/ and rewrites README.md.

    python scripts/fetch-data.py     # refresh data/profile.json from GitHub
    python scripts/render-svgs.py    # draw the cards + README.md

Profile design adapted from Sagargupta16 (https://github.com/Sagargupta16, MIT licensed).
Logos: simple-icons (CC0). Fonts: Inter, JetBrains Mono, Archivo Black (SIL OFL), embedded per SVG.
"""
import base64
import io
import json
import math
import os
from datetime import date, datetime
from xml.sax.saxutils import escape as esc

from fontTools import subset as ftsubset
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "svg")
FD = os.path.join(ROOT, "scripts", "fonts")
ICONS = json.load(open(os.path.join(ROOT, "scripts", "icons.json"), encoding="utf-8"))
DATA = json.load(open(os.path.join(ROOT, "data", "profile.json"), encoding="utf-8"))
SIZES = {"": 880, "-mobile": 400}

# ----------------------------------------------------------------------------- your content
USER = "shiva-kar"
NAME = "Shiva Kar"
SUBTITLE = "Java backends, systems in C and Godot Engine"
STATUS = "BUILDING BACKENDS IN JAVA"
ABOUT = ("BCA Computer Science student at **Amity University Online**, building **Java backends** with "
         "**Spring Boot**, **Hibernate/JPA**, **PostgreSQL** and **Redis**. I also work with "
         "**React**, **TypeScript** and **Tailwind CSS** when needed on the frontend. "
         "In my own time I contribute bug fixes to **Godot Engine** — working on editor, GUI, "
         "GDScript and web-platform issues in a large **C++** codebase. I've submitted 15 pull requests, "
         "with 6 merged. I'm also interested in **systems programming** with **C** — operating systems, "
         "process management, **POSIX** APIs, networking — and **graphics programming and rendering**.")
TAGS = ["Java Backend", "REST APIs", "Systems Programming", "Open Source"]
LINKS = {"linkedin": ("LinkedIn", "linkedin", "https://www.linkedin.com/in/shiva-kar/"),
         "email": ("Email", "gmail", "mailto:sksmarttech48@gmail.com"),
         "portfolio": ("Portfolio", "googlechrome", "https://shivakar.me"),
         "github": ("GitHub", "github", "https://github.com/shiva-kar"),
         "x": ("X", "x", "https://x.com/sk_shivakar")}
CURRENTLY = [
    "Building backend applications with Java, Spring Boot, PostgreSQL, and Redis",
    "REST API design, database persistence, authentication, transactions, and concurrency",
    "Practicing Data Structures & Algorithms and strengthening CS fundamentals",
    "Contributing bug fixes to Godot Engine and working with its existing codebase",
    "Exploring graphics programming, rendering, and game engine internals",
]
# (year label, short title, institution, dates, full degree name)
EDU = [("2017", "Class X", "Rabindra Bidyalaya High School", "JAN 2017 TO MAR 2022",
        "Secondary Education (Class X)"),
       ("2022", "Class XII, PCM + CS", "Deshabandhu Bidyapeeth HS", "JUL 2022 TO MAR 2025",
        "Higher Secondary (Class XII), Science (PCM + Computer Science)"),
       ("2025", "BCA, Computer Science", "Amity University Online", "JUL 2025 TO NOV 2028",
        "BCA: Computer Science")]
COURSES = ["Object-Oriented Programming (Java)", "Data Structures", "Operating Systems", "DBMS",
           "Computer Networks", "Unix & Shell Programming"]
CERTS = [("CS50x", "Introduction to Computer Science", "Harvard University",
          "C · Python · SQL · Algorithms · Data Structures · Memory"),
         ("CS50 SQL", "Introduction to Databases with SQL", "Harvard University",
          "Relational DBs · PostgreSQL · SQLite · Normalization · Indexing")]
EXCLUDE_REPOS = {USER, "open-source-projects-for-contributions", "Exercism.org", "C-Data-Structures"}
PROJECT_TITLES = {"resume-builder": "Resume Builder", "SXSHELL-unix-like-shell": "SXSHELL",
                  "Custom-HTTP-Server-in-C": "Custom HTTP Server in C", "bank-atm-cli": "Bank ATM CLI",
                  "streetflood-live": "StreetFlood Live", "shiva-kar.github.io": "Personal Portfolio"}
PROJECT_CHIPS = {"resume-builder": ["Next.js 14", "TypeScript", "Tailwind CSS"],
                 "SXSHELL-unix-like-shell": ["C", "Shell", "POSIX"],
                 "Custom-HTTP-Server-in-C": ["C", "POSIX Sockets", "HTTP"],
                 "bank-atm-cli": ["Java", "CLI"],
                 "streetflood-live": ["React", "TypeScript", "OSRM"],
                 "shiva-kar.github.io": ["JavaScript", "Portfolio"]}
MARQUEE = [
    [("Java", "openjdk", "#f89820"), ("Spring Boot", "springboot", None), ("Hibernate", "hibernate", "#b7c0c8"),
     ("PostgreSQL", "postgresql", None), ("MySQL", "mysql", "#5aa5d6"), ("Redis", "redis", None),
     ("JWT", "jsonwebtokens", None), ("C", "c", None), ("C++", "cplusplus", "#4aa3e0"),
     ("Linux", "linux", None), ("CMake", "cmake", "#3b8fd6"), ("Godot", "godotengine", None)],
    [("Git", "git", None), ("GitHub", "github", "#e6edf3"), ("Maven", "apachemaven", "#e0405a"),
     ("Docker", "docker", None), ("Postman", "postman", None), ("JUnit 5", "junit5", None),
     ("IntelliJ", "intellijidea", "#fe315d"), ("VS Code", None, "#3b9cdc"), ("Python", "python", None),
     ("JavaScript", "javascript", None), ("TypeScript", "typescript", None), ("React", "react", None),
     ("Tailwind", "tailwindcss", None), ("HTML", "html5", None)]]
CONCEPTS = ["Spring MVC", "Spring Security", "Spring Data JPA", "REST APIs", "SQL", "Docker Compose", "Mockito",
            "GDScript", "POSIX", "System Calls", "Processes", "Sockets", "Pipes", "Memory Management",
            "Data Structures", "Algorithms", "OOP", "Operating Systems", "DBMS", "Computer Networks",
            "Concurrency", "Networking", "Graphics", "Unity", "Blender"]
HEADERS = {"journey": ("01 / WHERE I LEARN AND WHAT I SHIP", "Journey"),
           "projects": ("02 / WHAT I HAVE BUILT", "Featured Projects"),
           "opensource": ("03 / MERGED UPSTREAM WORK", "Open Source"),
           "certs": ("04 / VERIFIED", "Certifications"),
           "stack": ("05 / WHAT I WORK WITH DAILY", "Tech Stack and Tools"),
           "currently": ("06 / WHAT I AM DOING NOW", "Currently"),
           "stats": ("07 / GITHUB ACTIVITY", "Coding Stats"),
           "education": ("08 / WHERE I STUDIED", "Education")}
# -----------------------------------------------------------------------------

# GitHub-native dark theme palette: balanced, mature, zero neon AI cyan
CARD, CARD2, EDGE, EDGE2 = "#0d1117", "#161b22", "#21262d", "#30363d"
BLUE, GREEN, ORANGE, PURPLE = "#58a6ff", "#3fb950", "#d29922", "#bc8cff"
TEXT, BODY, MUTED = "#f0f6fc", "#c9d1d9", "#8b949e"

FONTS = {"body": ("Inter", 400, "inter-latin-400-normal.woff2"),
         "bodyb": ("Inter", 600, "inter-latin-600-normal.woff2"),
         "mono": ("JetBrains Mono", 500, "jetbrains-mono-latin-500-normal.woff2"),
         "monob": ("JetBrains Mono", 700, "jetbrains-mono-latin-700-normal.woff2"),
         "head": ("Archivo Black", 400, "archivo-black-latin-400-normal.woff2")}
STACKS = {"Inter": "Inter, 'Segoe UI', system-ui, sans-serif",
          "JetBrains Mono": "'JetBrains Mono', ui-monospace, Consolas, monospace",
          "Archivo Black": "'Archivo Black', Impact, 'Arial Black', sans-serif"}
USED = {}
_metrics, _subs = {}, {}


def metrics(k):
    if k not in _metrics:
        f = TTFont(os.path.join(FD, FONTS[k][2]))
        _metrics[k] = (f.getBestCmap(), f["hmtx"].metrics, f["head"].unitsPerEm)
    return _metrics[k]


def tw(s, k, size, ls=0.0):
    cmap, hm, upm = metrics(k)
    total = 0
    for c in s:
        g = cmap.get(ord(c))
        total += hm[g][0] if g in hm else upm * 0.6
    return total / upm * size + ls * len(s)


def face_css(k, chars):
    key = (k, "".join(sorted(chars)))
    if key not in _subs:
        opts = ftsubset.Options()
        opts.layout_features = ["kern"]
        font = TTFont(os.path.join(FD, FONTS[k][2]))
        sub = ftsubset.Subsetter(opts)
        sub.populate(text="".join(sorted(chars)) + " ")
        sub.subset(font)
        buf = io.BytesIO()
        font.flavor = "woff2"
        font.save(buf)
        _subs[key] = base64.b64encode(buf.getvalue()).decode()
    fam, wt, _ = FONTS[k]
    return (f"@font-face{{font-family:'{fam}';font-weight:{wt};"
            f"src:url(data:font/woff2;base64,{_subs[key]}) format('woff2')}}")


def t(x, y, s, k="body", size=14, fill=BODY, anchor="start", ls=0.0, extra=""):
    USED.setdefault(k, set()).update(s)
    fam, wt, _ = FONTS[k]
    la = f' letter-spacing="{ls}"' if ls else ""
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{STACKS[fam]}" font-weight="{wt}" font-size="{size}" '
            f'fill="{fill}" text-anchor="{anchor}"{la} {extra}>{esc(s)}</text>')


def fit(s, k, size, maxw, ls=0.0):
    if tw(s, k, size, ls) <= maxw:
        return s
    while s and tw(s + "…", k, size, ls) > maxw:
        s = s[:-1]
    return s.rstrip() + "…"


def wrap(s, k, size, maxw, ls=0.0, maxlines=None):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if cur and tw(trial, k, size, ls) > maxw:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    if maxlines and len(lines) > maxlines:
        lines = lines[:maxlines]
        lines[-1] = fit(lines[-1] + " …", k, size, maxw, ls)
    return lines


def doc(w, h, body):
    css = "".join(face_css(k, c) for k, c in USED.items())
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img">'
            f'<style>{css}</style>{body}</svg>')


def card(x, y, w, h, r=12, fill=CARD, stroke=EDGE):
    return (f'<rect x="{x + .5:.1f}" y="{y + .5:.1f}" width="{w - 1:.1f}" height="{h - 1:.1f}" rx="{r}" '
            f'fill="{fill}" stroke="{stroke}"/>')


def label(x, y, s, color=BLUE, size=11.5, anchor="start"):
    return t(x, y, s, "monob", size, color, anchor, 2.0)


def tag(x, y, text, color=BLUE, size=11.5, h=26, r=6):
    w = tw(text, "monob", size, 0.5) + 20
    svg = (f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{r}" fill="{color}" fill-opacity=".1" '
           f'stroke="{color}" stroke-opacity=".35"/>' + t(x + w / 2, y + h / 2 + 4, text, "monob", size, color, "middle", 0.5))
    return svg, w


def icon(slug, x, y, size, color):
    return (f'<g transform="translate({x:.1f} {y:.1f}) scale({size / 24:.4f})">'
            f'<path d="{ICONS[slug]["path"]}" fill="{color}"/></g>')


def mix(c, base=CARD, a=0.1):
    c, base = c.lstrip("#"), base.lstrip("#")
    return "#" + "".join(f"{round(int(c[i:i + 2], 16) * a + int(base[i:i + 2], 16) * (1 - a)):02x}" for i in (0, 2, 4))


def short(n):
    return f"{n / 1000:.1f}K".replace(".0K", "K") if n >= 1000 else str(n)


# ----------------------------------------------------------------------------- components
def hero(w):
    m = w < 600
    pad = 24 if m else 48
    big = 42 if m else 56
    sub = 15 if m else 17
    loc = (DATA.get("location") or "").upper()
    sublines = wrap(SUBTITLE, "bodyb", sub, w - 2 * pad - (0 if m else 260))
    stat_w = tw(STATUS, "monob", 11.5, 1.2) + 38
    y = 52 + big + 10
    yy = y + 32
    py = yy + len(sublines) * (sub + 8)
    h = py + 48 if m else 240
    body = [card(0, 0, w, h, 14),
            label(pad, 48, "HI, I AM", BLUE, 11.5),
            t(pad, y, NAME, "head", big, "#ffffff")]
    for ln in sublines:
        body.append(t(pad, yy, ln, "bodyb", sub, MUTED))
        yy += sub + 8
    if not m:
        py = 186
    body.append(f'<rect x="{pad}" y="{py}" width="{stat_w:.1f}" height="28" rx="6" fill="{GREEN}" fill-opacity=".1" '
                f'stroke="{GREEN}" stroke-opacity=".35"/>'
                f'<circle cx="{pad + 14}" cy="{py + 14}" r="3.5" fill="{GREEN}"/>')
    body.append(t(pad + 26, py + 18.5, STATUS, "monob", 11.5, GREEN, ls=1.2))
    if loc:
        body.append(t(pad if m else pad + stat_w + 16, py + (44 if m else 18.5), loc, "mono", 11, MUTED, ls=1.2))
    return w, h, "".join(body)


def pills(w):
    items = [("FOLLOWERS", str(DATA["followers"]), BLUE), ("TOTAL STARS", str(DATA["stars"]), ORANGE),
             ("PULL REQUESTS", str(DATA["prs_total"]), BLUE),
             ("GODOT MERGED", str(sum(1 for p in DATA["merged"] if p["repo"] == "godotengine/godot")), GREEN),
             ("CERTIFIED", "CS50x + CS50 SQL", PURPLE),
             ("CONTRIBUTIONS", f'{DATA["calendar"]["total"]:,}', BLUE), ("PORTFOLIO", "SHIVAKAR.ME", BLUE)]
    gap, ph = 10, 34
    rows, cur, cw = [], [], 0
    for it in items:
        lw = tw(it[0], "mono", 11, 1.2) + 24
        vw = tw(it[1], "monob", 12.5, 0.8) + 24
        pw = lw + vw
        if cur and cw + gap + pw > w:
            rows.append((cur, cw))
            cur, cw = [], 0
        cw += (gap if cur else 0) + pw
        cur.append((it, lw, vw))
    rows.append((cur, cw))
    body = []
    for r, (row, rw) in enumerate(rows):
        x = (w - rw) / 2
        y = r * (ph + 10)
        for (lab, val, col), lw, vw in row:
            pw = lw + vw
            body.append(f'<rect x="{x + .5:.1f}" y="{y + .5}" width="{pw - 1:.1f}" height="{ph - 1}" rx="17" fill="{CARD2}" stroke="{EDGE2}"/>'
                        f'<path d="M{x + 17:.1f} {y} A17 17 0 0 0 {x + 17:.1f} {y + ph} H{x + lw:.1f} V{y} Z" fill="{mix(col, CARD, .12)}"/>'
                        f'<line x1="{x + lw:.1f}" y1="{y}" x2="{x + lw:.1f}" y2="{y + ph}" stroke="{EDGE2}"/>')
            body.append(t(x + 12, y + 21.5, lab, "mono", 11, MUTED, ls=1.2))
            body.append(t(x + lw + 12, y + 22, val, "monob", 12.5, col, ls=0.8))
            x += pw + gap
    return w, len(rows) * (ph + 10) - 10, "".join(body)


def about(w):
    m = w < 600
    pad = 22 if m else 30
    size = 14.5 if m else 15.5
    lh = int(size * 1.6)
    units, glue = [], False
    for i, part in enumerate(ABOUT.split("**")):
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
    sp = tw(" ", "body", size)
    lines, cur, cw = [], [], 0
    for u in units:
        ww = sum(tw(x, "bodyb" if b else "body", size) for x, b in u)
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
                ux += tw(word, "bodyb" if bold else "body", size)
            x += ww + sp
        y += lh
    tx, ty = pad + 8, y + 6
    for tg in TAGS:
        s, wd = tag(tx, ty, tg, BLUE, 11.5)
        if tx + wd > w - pad and tx > pad + 8:
            tx, ty = pad + 8, ty + 34
            s, wd = tag(tx, ty, tg, BLUE, 11.5)
        body.append(s)
        tx += wd + 10
    h = ty + 28 + pad
    return w, h, card(0, 0, w, h) + f'<rect x="0" y="16" width="3.5" height="{h - 32}" rx="1.75" fill="{BLUE}"/>' + "".join(body)


def connect(text, slug):
    wd = 14 + 16 + 10 + tw(text, "monob", 12, 1.2) + 20
    body = (f'<rect x=".5" y=".5" width="{wd - 1:.1f}" height="37" rx="18.5" fill="{CARD2}" stroke="{EDGE2}"/>'
            + icon(slug, 15, 11, 16, TEXT) + t(41, 24, text, "monob", 12, TEXT, ls=1.2))
    return wd, 38, body


def divider(w):
    return w, 16, (f'<defs><linearGradient id="d" x1="0" x2="1"><stop offset="0" stop-color="{EDGE}" stop-opacity="0"/>'
                   f'<stop offset=".5" stop-color="{EDGE2}"/><stop offset="1" stop-color="{EDGE}" stop-opacity="0"/></linearGradient></defs>'
                   f'<rect y="7.5" width="{w}" height="1" fill="url(#d)"/>')


def header(key, theme, w):
    m = w < 600
    lab, title = HEADERS[key]
    dark = theme == "dark"
    col = "#f0f6fc" if dark else "#1f2328"
    acc = BLUE if dark else "#0969da"
    sub_col = MUTED if dark else "#57606a"
    border_col = EDGE if dark else "#d0d7de"
    h = 50
    body = [
        f'<rect x="0" y="7" width="3.5" height="36" rx="1.75" fill="{acc}"/>',
        t(16, 17, lab, "monob", 11 if m else 11.5, sub_col, ls=2.0),
        t(16, 40, title, "head", 20 if m else 22, col),
        f'<line x1="0" y1="49.5" x2="{w}" y2="49.5" stroke="{border_col}" stroke-width="1"/>'
    ]
    return w, h, "".join(body)


def _tl_row_desktop(w, y0, title, nodes, pad):
    n = len(nodes)
    colw = (w - 2 * pad) / n
    body = [label(pad, y0, title, BLUE, 11.5)]
    ly = y0 + 46
    xs = [pad + colw * (i + .5) for i in range(n)]
    body.append(f'<line x1="{xs[0]:.1f}" y1="{ly}" x2="{xs[-1]:.1f}" y2="{ly}" stroke="{EDGE2}" stroke-width="2"/>')
    maxy = ly
    for i, (yr, ttl, sub, live) in enumerate(nodes):
        x, col = xs[i], GREEN if live else BLUE
        body.append(t(x, ly - 14, yr, "monob", 11.5, col, "middle", 1.2))
        body.append(f'<circle cx="{x:.1f}" cy="{ly}" r="6" fill="{CARD}" stroke="{col}" stroke-width="2"/>'
                    f'<circle cx="{x:.1f}" cy="{ly}" r="2.5" fill="{col}"/>')
        yy = ly + 28
        for ln in wrap(ttl, "bodyb", 13.5, colw - 12, maxlines=2):
            body.append(t(x, yy, ln, "bodyb", 13.5, TEXT, "middle"))
            yy += 18
        yy += 2
        for ln in wrap(sub, "mono", 11.5, colw - 12, 0.5, 2):
            body.append(t(x, yy, fit(ln, "mono", 11.5, colw - 10, 0.5), "mono", 11.5, MUTED, "middle", 0.5))
            yy += 15
        maxy = max(maxy, yy)
    return "".join(body), maxy + 14


def _tl_row_mobile(w, y0, title, nodes, pad):
    body = [label(pad, y0, title, BLUE, 11)]
    y = y0 + 28
    top = y
    for yr, ttl, sub, live in nodes:
        col = GREEN if live else BLUE
        body.append(f'<circle cx="{pad + 6}" cy="{y - 4}" r="5" fill="{CARD}" stroke="{col}" stroke-width="2"/>'
                    f'<circle cx="{pad + 6}" cy="{y - 4}" r="2" fill="{col}"/>')
        body.append(t(pad + 24, y, yr, "monob", 11, col, ls=1.2))
        y += 20
        for ln in wrap(ttl, "bodyb", 13.5, w - 2 * pad - 28, maxlines=2):
            body.append(t(pad + 24, y, ln, "bodyb", 13.5, TEXT))
            y += 18
        for ln in wrap(sub, "mono", 11.5, w - 2 * pad - 28, 0.5, 2):
            body.append(t(pad + 24, y, fit(ln, "mono", 11.5, w - 2 * pad - 28, 0.5), "mono", 11.5, MUTED, ls=0.5))
            y += 15
        y += 14
    line = f'<line x1="{pad + 6}" y1="{top - 4}" x2="{pad + 6}" y2="{y - 34}" stroke="{EDGE2}" stroke-width="2"/>'
    return line + "".join(body), y


def timeline(w):
    m = w < 600
    pad = 22 if m else 30
    row1 = [(yr, ttl, inst, i == len(EDU) - 1) for i, (yr, ttl, inst, _, _) in enumerate(EDU)]
    row1.append(("2028 EXPECTED", "Graduation", "BCA, Amity University Online", False))
    months = {}
    for p in DATA["merged"] + DATA["open"]:
        months.setdefault(p["date"][:7], []).append(p["repo"].split("/")[1])
    row2 = []
    for k, repos in sorted(months.items())[-5:]:
        top = max(set(repos), key=repos.count)
        mo = datetime.strptime(k, "%Y-%m").strftime("%b %Y").upper()
        row2.append([mo, f"{len(repos)} upstream PR{'s' if len(repos) > 1 else ''}", top, False])
    if row2:
        row2[-1][3] = True
    fn = _tl_row_mobile if m else _tl_row_desktop
    b1, y1 = fn(w, pad + 6, "EDUCATION", row1, pad)
    b2, y2 = fn(w, y1 + 18, "UPSTREAM CONTRIBUTIONS", [tuple(r) for r in row2], pad) if row2 else ("", y1)
    sep = (f'<line x1="{pad}" x2="{w - pad}" y1="{y1 + 4}" y2="{y1 + 4}" stroke="{EDGE2}" stroke-dasharray="3 5"/>'
           if row2 else "")
    h = y2 + pad - 8
    return w, h, card(0, 0, w, h) + b1 + sep + b2


def projects(w):
    m = w < 600
    gap, pad = 12, 18
    cw = w if m else (w - gap) / 2
    repos = [r for r in DATA["repos"] if r["name"] not in EXCLUDE_REPOS and r["desc"]]
    repos = sorted(repos, key=lambda r: (r["stars"], r["updated"]), reverse=True)[:6]
    ch = 90 + 4 * 19 + 44
    per = 1 if m else 2
    out = []
    for i, r in enumerate(repos):
        mo = datetime.strptime(r["updated"], "%Y-%m-%d").strftime("%B %Y").upper()
        title = PROJECT_TITLES.get(r["name"], r["name"])
        g = [f'<rect x="0" y="20" width="3.5" height="18" rx="1.75" fill="{BLUE}"/>',
             t(pad, 33, mo, "monob", 11.5, MUTED, ls=1.2),
             t(cw - pad, 33, f"{r['stars']} STARS" if r["stars"] > 1 else (f"{r['stars']} STAR" if r["stars"] else "SOURCE"),
               "monob", 11.5, ORANGE if r["stars"] else MUTED, "end", 1.0),
             t(pad, 62, fit(title, "head", 17.5, cw - 2 * pad), "head", 17.5, "#ffffff")]
        y = 86
        for ln in wrap(r["desc"], "body", 13.5, cw - 2 * pad - 6, maxlines=4):
            g.append(t(pad, y, ln, "body", 13.5, BODY))
            y += 19
        chips = PROJECT_CHIPS.get(r["name"]) or r["topics"][:3] or ([r["lang"]] if r["lang"] else [])
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


def oss(w):
    """Balanced, 2-column Open Source dashboard:
    - Upstream repos bar on top
    - Left column: Merged Pull Requests (green status)
    - Right column: Open Pull Requests (amber status)
    """
    m = w < 600
    pad = 18 if m else 24
    stars = DATA["upstream_stars"]
    names = sorted([r for r in stars if stars[r] > 0], key=lambda r: -stars[r])

    pills_body = []
    gap, ph = 8, 28
    sized = []
    for n in names:
        lw = tw(n, "monob", 11.5, .5) + 12
        sw = tw(f"★ {short(stars[n])}", "monob", 11.5, .5) + 12
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
                   for p in sorted(DATA["merged"], key=lambda p: p["date"], reverse=True)]
    
    open_groups = {}
    for p in sorted(DATA["open"], key=lambda p: p["date"], reverse=True):
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
        bw = tw(badge_text, "monob", 11.5, 1) + 20
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
        badge_open = f"{len(DATA['open'])} OPEN PRS"
        obw = tw(badge_open, "monob", 11.5, 1) + 20
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
        bw = tw(badge_text, "monob", 11, 1) + 18
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
        badge_open = f"{len(DATA['open'])} OPEN PRS"
        obw = tw(badge_open, "monob", 11, 1) + 18
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


def oss_repos(w):
    stars = DATA["upstream_stars"]
    names = sorted([r for r in stars if stars[r] > 0], key=lambda r: -stars[r])
    gap, ph = 8, 28
    sized = []
    for n in names:
        lw, sw = tw(n, "monob", 11.5, .5), tw(f"★ {short(stars[n])}", "monob", 11.5, .5)
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
        rw = tw(nums, "mono", 11, .5)
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


def oss_merged(w):
    rows = [(p["repo"], f"#{p['number']}", p["title"])
            for p in sorted(DATA["merged"], key=lambda p: p["date"], reverse=True)]
    return _pr_card(w, f"{len(rows)} MERGED UPSTREAM | NEWEST FIRST", GREEN, rows)


def oss_open(w):
    groups = {}
    for p in sorted(DATA["open"], key=lambda p: p["date"], reverse=True):
        open_groups = groups.setdefault(p["repo"], []).append(p)
    rows = []
    for repo, ps in groups.items():
        nums = ", ".join(f"#{p['number']}" for p in ps[:3]) + (f" +{len(ps) - 3}" if len(ps) > 3 else "")
        rows.append((repo, nums, "; ".join(p["title"] for p in ps)))
    return _pr_card(w, f"{len(DATA['open'])} OPEN PRS", ORANGE, rows)


def certs(w):
    """Refined balanced certifications layout:
    Two balanced credential cards side-by-side on desktop, stacked on mobile.
    Eliminates floating 8px hexagons and provides high-density, professional presentation.
    """
    m = w < 600
    pad = 20 if m else 26
    gap = 14
    cw = w - 2 * pad if m else (w - 2 * pad - gap) / 2
    ch = 180
    
    body = [label(pad, pad + 10, "VERIFIED CERTIFICATIONS", BLUE, 11.5)]
    y_cards = pad + 30

    cards_out = []
    for i, (code, title, issuer, topics) in enumerate(CERTS):
        acc = BLUE if i == 0 else PURPLE
        x = pad if m else pad + i * (cw + gap)
        y = y_cards + i * (ch + gap) if m else y_cards
        
        c = [
            f'<rect x="{x + .5:.1f}" y="{y + .5:.1f}" width="{cw - 1:.1f}" height="{ch - 1:.1f}" rx="10" fill="{CARD2}" stroke="{EDGE2}"/>',
            f'<rect x="{x:.1f}" y="{y + 14:.1f}" width="3.5" height="42" rx="1.75" fill="{acc}"/>',
            f'<rect x="{x + 14:.1f}" y="{y + 16:.1f}" width="140" height="22" rx="5" fill="{GREEN}" fill-opacity=".15" stroke="{GREEN}" stroke-opacity=".4"/>',
            t(x + 84, y + 31.5, "VERIFIED CREDENTIAL", "monob", 10.5, GREEN, "middle", 0.5),
            t(x + cw - 14, y + 31.5, issuer.upper(), "monob", 11, MUTED, "end", 1),
            t(x + 14, y + 66, code, "head", 20, "#ffffff"),
            t(x + 14, y + 88, fit(title, "bodyb", 14.5, cw - 28), "bodyb", 14.5, TEXT),
        ]
        ty = y + 116
        for ln in wrap(topics, "body", 12, cw - 28, maxlines=2):
            c.append(t(x + 14, ty, ln, "body", 12, MUTED))
            ty += 18
        
        cards_out.append("".join(c))
    
    total_h = y_cards + (len(CERTS) * (ch + gap) - gap if m else ch) + pad
    return w, total_h, card(0, 0, w, total_h) + "".join(body) + "".join(cards_out)


def marquee(w):
    tile, pitch, gapy, pad = 56, 64, 14, 18
    h = 2 * tile + gapy + 2 * pad
    defs = (f'<defs><linearGradient id="fl" x1="0" x2="1"><stop offset="0" stop-color="{CARD}"/><stop offset="1" stop-color="{CARD}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="fr" x1="1" x2="0"><stop offset="0" stop-color="{CARD}"/><stop offset="1" stop-color="{CARD}" stop-opacity="0"/></linearGradient></defs>')
    rows = []
    for ri, items in enumerate(MARQUEE):
        seq = len(items) * pitch
        reps = int(math.ceil((w + seq) / seq)) + 1
        tiles = []
        for rep in range(reps):
            for i, (name, slug, col) in enumerate(items):
                x = rep * seq + i * pitch
                c = col or "#" + ICONS[slug]["hex"]
                tiles.append(f'<rect x="{x}" y="0" width="{tile}" height="{tile}" rx="12" fill="{mix(c, CARD, .14)}" '
                             f'stroke="{mix(c, CARD, .35)}"/>')
                tiles.append(icon(slug, x + 15, 15, 26, c) if slug else t(x + 28, 35, name[:2], "monob", 17, c, "middle"))
        frm, to = (0, -seq) if ri % 2 == 0 else (-seq, 0)
        rows.append(f'<g transform="translate(0 {pad + ri * (tile + gapy)})"><g><animateTransform attributeName="transform" '
                    f'type="translate" from="{frm} 0" to="{to} 0" dur="{len(items) * 3.5:.0f}s" repeatCount="indefinite"/>'
                    f'{"".join(tiles)}</g></g>')
    fade = 60
    body = (defs + card(0, 0, w, h) + f'<g>{"".join(rows)}'
            f'<rect x="1" y="1" width="{fade}" height="{h - 2}" fill="url(#fl)"/>'
            f'<rect x="{w - fade - 1}" y="1" width="{fade}" height="{h - 2}" fill="url(#fr)"/></g>' + card(0, 0, w, h, fill="none"))
    return w, h, body


def concepts(w):
    m = w < 600
    pad = 20 if m else 24
    cols, gap = (2 if m else 5), 8
    bw = (w - 2 * pad - gap * (cols - 1)) / cols
    body = [label(pad, pad + 10, "CORE CONCEPTS AND LIBRARIES", BLUE, 11.5)]
    y0 = pad + 30
    for i, c in enumerate(CONCEPTS):
        r, cc = divmod(i, cols)
        x, y = pad + cc * (bw + gap), y0 + r * 46
        body.append(f'<rect x="{x:.1f}" y="{y}" width="{bw:.1f}" height="38" rx="8" fill="{CARD2}" stroke="{EDGE}"/>')
        body.append(f'<circle cx="{x + 14:.1f}" cy="{y + 19}" r="2.5" fill="{BLUE if i % 2 == 0 else GREEN}"/>')
        body.append(t(x + 24, y + 23.5, fit(c, "bodyb", 12, bw - 28), "bodyb", 12, TEXT))
    rows = (len(CONCEPTS) + cols - 1) // cols
    h = y0 + rows * 46 - 8 + pad
    return w, h, card(0, 0, w, h) + "".join(body)


def currently(w):
    m = w < 600
    pad = 22 if m else 30
    body = [label(pad + 8, pad + 20, "CURRENTLY", GREEN, 11.5)]
    y = pad + 44
    lh = 26
    for item in CURRENTLY:
        body.append(f'<circle cx="{pad + 14}" cy="{y - 4}" r="3" fill="{GREEN}"/>')
        for ln in wrap(item, "body", 13.5 if m else 14.5, w - 2 * pad - 30, maxlines=3):
            body.append(t(pad + 26, y, ln, "body", 13.5 if m else 14.5, TEXT))
            y += 20
        y += lh - 20
    h = y + pad - 8
    return w, h, card(0, 0, w, h) + f'<rect x="0" y="16" width="3.5" height="{h - 32}" rx="1.75" fill="{GREEN}"/>' + "".join(body)


LANG_COL = {"TypeScript": "#3178c6", "JavaScript": "#f1e05a", "Java": "#f89820", "C": "#a8b9cc", "Python": "#3572a5",
            "C++": "#f34b7d", "Shell": "#89e051", "HTML": "#e34c26", "CSS": "#563d7c"}


def stats(w):
    m = w < 600
    pad = 20 if m else 28
    cal = DATA["calendar"]
    tiles = [("CONTRIBUTIONS", f"{cal['total']:,}"), ("PULL REQUESTS", str(DATA["prs_total"])),
             ("ISSUES", str(DATA["issues_total"])), ("STARS EARNED", str(DATA["stars"])),
             ("FOLLOWERS", str(DATA["followers"]))]
    body = [label(pad, pad + 10, f"GITHUB | @{USER.upper()}", BLUE, 11.5)]
    cols, gap = (2 if m else 5), 10
    twid = (w - 2 * pad - gap * (cols - 1)) / cols
    y0 = pad + 26
    for i, (lab, val) in enumerate(tiles):
        r, c = divmod(i, cols)
        x, y = pad + c * (twid + gap), y0 + r * 66
        body.append(f'<rect x="{x:.1f}" y="{y}" width="{twid:.1f}" height="56" rx="10" fill="{CARD2}" stroke="{EDGE}"/>')
        body.append(t(x + 14, y + 26, val, "bodyb", 22, "#ffffff"))
        body.append(t(x + 14, y + 44, lab, "mono", 11, MUTED, ls=1.2))
    y = y0 + ((len(tiles) + cols - 1) // cols) * 66 + 8
    weeks, col = [], None
    for d in cal["days"]:
        wd = (date.fromisoformat(d["date"]).weekday() + 1) % 7
        if col is None or wd == 0:
            col = [None] * 7
            weeks.append(col)
        col[wd] = d
    nweeks = 26 if m else 53
    weeks = weeks[-nweeks:]
    sbox = 0 if m else 160
    pitch = (w - 2 * pad - sbox - (0 if m else 14)) / nweeks
    # Authentic GitHub Green Heatmap palette
    lv = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
    for wi, wk in enumerate(weeks):
        for di, d in enumerate(wk):
            if d:
                body.append(f'<rect x="{pad + wi * pitch:.1f}" y="{y + di * pitch:.1f}" width="{pitch - 2.6:.1f}" '
                            f'height="{pitch - 2.6:.1f}" rx="2" fill="{lv[d["level"]]}"/>')
    hm_h = 7 * pitch
    cur = cal["current_streak"]
    unit = "DAY" if cur == 1 else "DAYS"
    if m:
        y += hm_h + 14
        body.append(f'<rect x="{pad}" y="{y}" width="{w - 2 * pad}" height="64" rx="10" fill="{CARD2}" stroke="{EDGE}"/>')
        body.append(label(pad + 14, y + 20, "CURRENT STREAK", GREEN, 11))
        body.append(t(pad + 14, y + 48, f"{cur} {unit}", "bodyb", 20, "#ffffff"))
        body.append(t(w - pad - 14, y + 30, f"LONGEST {cal['longest_streak']}", "mono", 11, MUTED, "end", 1))
        body.append(t(w - pad - 14, y + 48, f"ACTIVE {cal['active_days']}", "mono", 11, MUTED, "end", 1))
        y += 64 + 16
    else:
        sx, bh = w - pad - sbox, max(hm_h, 88)
        body.append(f'<rect x="{sx}" y="{y}" width="{sbox}" height="{bh:.1f}" rx="10" fill="{CARD2}" stroke="{EDGE}"/>')
        body.append(label(sx + 14, y + 22, "CURRENT STREAK", GREEN, 11))
        body.append(t(sx + 14, y + 50, f"{cur} {unit}", "bodyb", 21, "#ffffff"))
        body.append(t(sx + 14, y + 70, f"LONGEST {cal['longest_streak']}", "mono", 11, MUTED, ls=1))
        body.append(t(sx + 14, y + 84, f"ACTIVE {cal['active_days']}", "mono", 11, MUTED, ls=1))
        y += bh + 20
    basis = "REPO" if DATA.get("languages_basis") == "repos" else "CODE SIZE"
    body.append(label(pad, y + 8, f"TOP LANGUAGES BY {basis}", ORANGE, 11.5))
    y += 20
    total = sum(l["pct"] for l in DATA["languages"]) or 1
    bw = w - 2 * pad
    seg, x = [], pad
    for l in DATA["languages"]:
        sw = bw * l["pct"] / total
        seg.append(f'<rect x="{x:.1f}" y="{y}" width="{sw:.1f}" height="8" fill="{LANG_COL.get(l["name"], MUTED)}"/>')
        x += sw
    body.append(f'<defs><clipPath id="lb"><rect x="{pad}" y="{y}" width="{bw}" height="8" rx="4"/></clipPath></defs>'
                f'<g clip-path="url(#lb)">{"".join(seg)}</g>')
    y += 28
    lc = 2 if m else 3
    lw = (w - 2 * pad) / lc
    for i, l in enumerate(DATA["languages"]):
        r, c = divmod(i, lc)
        lx, ly = pad + c * lw, y + r * 22
        body.append(f'<circle cx="{lx + 5}" cy="{ly - 4}" r="4" fill="{LANG_COL.get(l["name"], MUTED)}"/>')
        body.append(t(lx + 16, ly, f'{l["name"]} {l["pct"]}%', "monob", 12, BODY, ls=0.8))
    y += ((len(DATA["languages"]) + lc - 1) // lc) * 22
    h = y + pad - 12
    return w, h, card(0, 0, w, h) + "".join(body)


def education(w):
    m = w < 600
    pad = 22 if m else 30
    body = [label(pad, pad + 10, "EDUCATION", BLUE, 11.5)]
    y = pad + 36
    for i, (_, _, inst, dates, degree) in enumerate(reversed(EDU)):
        body.append(f'<circle cx="{pad + 4}" cy="{y - 4}" r="3.5" fill="{[BLUE, GREEN, PURPLE][i % 3]}"/>')
        dw = 0 if m else tw(dates, "mono", 11.5, 1.0) + 20
        if m:
            body.append(t(pad + 18, y, dates, "mono", 11, MUTED, ls=1))
            y += 18
        else:
            body.append(t(w - pad, y, dates, "mono", 11.5, MUTED, "end", 1.0))
        for ln in wrap(degree, "bodyb", 15, w - 2 * pad - 20 - dw):
            body.append(t(pad + 18, y, ln, "bodyb", 15, "#ffffff"))
            y += 20
        body.append(t(pad + 18, y, inst, "body", 13, MUTED))
        y += 30
        if i < len(EDU) - 1:
            body.append(f'<line x1="{pad + 18}" x2="{w - pad}" y1="{y - 16}" y2="{y - 16}" stroke="{EDGE}"/>')
    y += 8
    body.append(label(pad, y, "RELEVANT COURSEWORK", BLUE, 11.5))
    cx, cy = pad, y + 16
    for c in COURSES:
        s, wd = tag(cx, cy, c, BLUE, 11.5)
        if cx + wd > w - pad and cx > pad:
            cx, cy = pad, cy + 34
            s, wd = tag(cx, cy, c, BLUE, 11.5)
        body.append(s)
        cx += wd + 10
    h = cy + 28 + pad
    return w, h, card(0, 0, w, h) + "".join(body)


def footer(w):
    """Compact, human, respectful footer (96px height) without fake sine waves."""
    m = w < 600
    h = 96
    body = [
        card(0, 0, w, h, 12, fill=CARD2, stroke=EDGE2),
        t(w / 2, 32, "SHIVA KAR • BCA STUDENT & DEVELOPER", "monob", 11.5, MUTED, "middle", 2.0),
        t(w / 2, 58, "More at shivakar.me ↗", "bodyb", 18 if m else 20, BLUE, "middle"),
        t(w / 2, 80, "Built with Python SVG generator • Updated daily via GitHub Actions", "body", 12, MUTED, "middle")
    ]
    return w, h, "".join(body)


# ----------------------------------------------------------------------------- output
def write(name, parts):
    w, h, body = parts
    with open(os.path.join(OUT, name + ".svg"), "w", encoding="utf-8") as f:
        f.write(doc(w, h, body))
    USED.clear()


def picture(name, alt, link=None):
    pic = (f'<picture><source media="(min-width: 1012px)" srcset="assets/svg/{name}.svg" />'
           f'<img src="assets/svg/{name}-mobile.svg" width="100%" alt="{alt}" /></picture>')
    return f'<a href="{link}">{pic}</a>' if link else pic


def head_picture(key):
    return (f'<picture><source media="(prefers-color-scheme: light) and (min-width: 1012px)" srcset="assets/svg/header-{key}-light.svg" />'
            f'<source media="(prefers-color-scheme: dark) and (min-width: 1012px)" srcset="assets/svg/header-{key}-dark.svg" />'
            f'<source media="(prefers-color-scheme: light)" srcset="assets/svg/header-{key}-light-mobile.svg" />'
            f'<source media="(prefers-color-scheme: dark)" srcset="assets/svg/header-{key}-dark-mobile.svg" />'
            f'<img src="assets/svg/header-{key}-dark-mobile.svg" width="100%" alt="{HEADERS[key][1]}" /></picture>')


def write_readme():
    D = '<picture><img src="assets/svg/divider.svg" width="100%" alt="" /></picture>'
    site = "https://shivakar.me"
    prs = f"https://github.com/search?q=is%3Apr+author%3A{USER}+is%3Amerged+-user%3A{USER}&amp;type=pullrequests"
    repos = f"https://github.com/{USER}?tab=repositories"
    btns = "\n".join(f'<a href="{u}"><picture><img src="assets/svg/connect-{k}.svg" height="38" alt="{n.title()}" /></picture></a>'
                     for k, (n, _, u) in LINKS.items())
    raw = f"https://raw.githubusercontent.com/{USER}/{USER}/output"
    snake = (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{raw}/github-snake-dark.svg" />\n'
             f'  <source media="(prefers-color-scheme: light)" srcset="{raw}/github-snake.svg" />\n'
             f'  <img alt="Contribution snake" src="{raw}/github-snake.svg" width="100%" />\n</picture>')
    # Neofetch dark/light block — verbatim from old README, must stay at same paths
    neofetch = ('<picture>\n'
                '  <source media="(prefers-color-scheme: dark)" srcset="dark_mode.svg" />\n'
                '  <source media="(prefers-color-scheme: light)" srcset="light_mode.svg" />\n'
                '  <img alt="shiva-kar\'s GitHub profile" src="dark_mode.svg" width="100%" />\n'
                '</picture>')
    # Old GitHub summary cards (profile-summary-cards) — stats, repos-per-language and profile-details
    summary_cards = ('<div align="center">\n'
                     f'<img src="https://github-profile-summary-cards.vercel.app/api/cards/stats?username={USER}&amp;theme=github_dark&amp;animation=fade" width="48%"/>\n'
                     f'<img src="https://github-profile-summary-cards.vercel.app/api/cards/repos-per-language?username={USER}&amp;theme=github_dark&amp;animation=fade" width="48%"/>\n'
                     '</div>\n\n'
                     '<div align="center">\n'
                     f'<img src="https://github-profile-summary-cards.vercel.app/api/cards/profile-details?username={USER}&amp;theme=github_dark&amp;animation=fade" width="96%"/>\n'
                     '</div>')
    blocks = [
        "<!-- Generated by scripts/render-svgs.py from data/profile.json. Edit the script, not this file.\n"
        "     Profile design adapted from Sagargupta16 (https://github.com/Sagargupta16), MIT licensed. -->",
        neofetch,
        picture("pills", "GitHub followers, stars, pull requests, Godot merges, CS50 certifications, contributions"),
        picture("about", "BCA Computer Science student building Java backends with Spring Boot, PostgreSQL and Redis; Godot Engine contributor"),
        f'<p align="center">\n{btns}\n</p>',
        D, head_picture("journey"), picture("timeline", "Education and upstream contribution timeline"),
        D, head_picture("projects"), picture("projects", "Featured projects", repos),
        D, head_picture("opensource"), picture("oss", "Open source upstream contributions, merged PRs and open PRs", prs),
        D, head_picture("certs"), picture("certs", "CS50x and CS50 SQL certifications"),
        D, head_picture("stack"), picture("marquee", "Tech stack logos"), picture("concepts", "Core concepts and libraries"),
        D, head_picture("currently"), picture("currently", "What I am working on right now"),
        D, head_picture("stats"), picture("stats", "GitHub contribution stats", f"https://github.com/{USER}"),
        summary_cards, snake,
        D, head_picture("education"), picture("education", "Education"),
        D, picture("footer", "More at shivakar.me", site),
        '<p align="center"><sub>Profile design adapted from <a href="https://github.com/Sagargupta16">Sagargupta16</a>. '
        f'Stats refreshed {DATA["generated"]}.</sub></p>']
    with open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n\n".join(blocks) + "\n")


def main():
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith(".svg"):
            os.remove(os.path.join(OUT, f))
    for suf, w in SIZES.items():
        for fn in (hero, pills, about, timeline, projects, oss, oss_repos, oss_merged, oss_open, certs, marquee,
                   concepts, currently, stats, education, footer):
            write(fn.__name__.replace("_", "-") + suf, fn(w))
        for key in HEADERS:
            for theme in ("light", "dark"):
                write(f"header-{key}-{theme}{suf}", header(key, theme, w))
    write("divider", (lambda p: p)(divider(880)))
    for k, (text, slug, _) in LINKS.items():
        write(f"connect-{k}", connect(text, slug))
    write_readme()
    print("wrote", len(os.listdir(OUT)), "SVGs and README.md")


if __name__ == "__main__":
    main()
