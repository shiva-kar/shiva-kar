#!/usr/bin/env python3
"""Configuration file for Shiva Kar's GitHub profile.

Edit this file to update your profile bio, status, milestones, featured projects,
tech stack, developer tools, and certifications. Running `python scripts/render-svgs.py`
will re-render all SVG cards and update README.md automatically.
"""

USER = "shiva-kar"
NAME = "Shiva Kar"
SUBTITLE = "Java backends, systems in C and Godot Engine"
LOCATION = "Hojai, Assam, India"
CGPA = "8.84/10"

# Bio narrative: human, clear, zero AI em dashes
ABOUT = (
    "BCA Computer Science student at Amity University Online (CGPA 8.84/10), building Java backends with "
    "Spring Boot, PostgreSQL, and Redis. I also work with React and TypeScript on the frontend when needed. "
    "In my own time, I contribute bug fixes to Godot Engine across editor, GUI, GDScript, and web-platform "
    "subsystems in C++ (13 pull requests submitted, 6 merged). I am also interested in systems programming "
    "in C, POSIX APIs, and graphics rendering."
)


LINKS = {
    "linkedin": ("LinkedIn", "linkedin", "https://www.linkedin.com/in/shiva-kar/"),
    "email": ("Email", "gmail", "mailto:sksmarttech48@gmail.com"),
    "portfolio": ("Portfolio", "googlechrome", "https://shivakar.me"),
    "github": ("GitHub", "github", "https://github.com/shiva-kar"),
    "x": ("X", "x", "https://x.com/sk_shivakar"),
}

CURRENTLY = [
    "Building backend applications with Java, Spring Boot, PostgreSQL, and Redis",
    "REST API design, database persistence, authentication, transactions, and concurrency",
    "Practicing Data Structures & Algorithms and strengthening CS fundamentals",
    "Contributing bug fixes to Godot Engine and working with its existing codebase",
    "Exploring graphics programming, rendering, and game engine internals",
]

# (year label, short title, institution, dates, full degree name)
EDU = [
    ("2017", "Class X", "Rabindra Bidyalaya High School", "JAN 2017 TO MAR 2022",
     "Secondary Education (Class X)"),
    ("2022", "Class XII, PCM + CS", "Deshabandhu Bidyapeeth HS", "JUL 2022 TO MAR 2025",
     "Higher Secondary (Class XII), Science (PCM + Computer Science)"),
    ("2025", "BCA, Computer Science", "Amity University Online", "JUL 2025 TO NOV 2028",
     "BCA: Computer Science (CGPA: 8.84/10)"),
]

COURSES = [
    "Object-Oriented Programming (Java)",
    "Data Structures",
    "Operating Systems",
    "DBMS",
    "Computer Networks",
    "Unix & Shell Programming",
]

CERTS = [
    ("CS50x", "Introduction to Computer Science", "Harvard University",
     "C · Python · SQL · Algorithms · Data Structures · Memory"),
    ("CS50 SQL", "Introduction to Databases with SQL", "Harvard University",
     "Relational DBs · PostgreSQL · SQLite · Normalization · Indexing"),
]

EXCLUDE_REPOS = {USER, "open-source-projects-for-contributions", "Exercism.org", "C-Data-Structures"}

PROJECT_TITLES = {
    "resume-builder": "Resume Builder",
    "SXSHELL-unix-like-shell": "SXSHELL",
    "Custom-HTTP-Server-in-C": "Custom HTTP Server in C",
    "bank-atm-cli": "Bank ATM CLI",
    "streetflood-live": "StreetFlood Live",
    "shiva-kar.github.io": "Personal Portfolio",
}

PROJECT_CHIPS = {
    "resume-builder": ["Next.js 14", "TypeScript", "Tailwind CSS"],
    "SXSHELL-unix-like-shell": ["C", "Shell", "POSIX"],
    "Custom-HTTP-Server-in-C": ["C", "POSIX Sockets", "HTTP"],
    "bank-atm-cli": ["Java", "CLI"],
    "streetflood-live": ["React", "TypeScript", "OSRM"],
    "shiva-kar.github.io": ["JavaScript", "Portfolio"],
}

# Developer Tools & Daily Workflow setup
TOOLS = [
    ("Languages", ["Java", "C", "SQL", "C++", "Python", "TypeScript"]),
    ("Backend & Data", ["Spring Boot", "Hibernate/JPA", "PostgreSQL", "MySQL", "Redis"]),
    ("Systems & DevOps", ["Linux", "POSIX APIs", "Docker", "Git", "Maven", "CMake"]),
    ("Environment", ["IntelliJ IDEA", "VS Code", "JUnit 5", "Mockito", "Postman"]),
]

MARQUEE = [
    [("Java", "openjdk", "#f89820"), ("Spring Boot", "springboot", None), ("Hibernate", "hibernate", "#b7c0c8"),
     ("PostgreSQL", "postgresql", None), ("MySQL", "mysql", "#5aa5d6"), ("Redis", "redis", None),
     ("JWT", "jsonwebtokens", None), ("C", "c", None), ("C++", "cplusplus", "#4aa3e0"),
     ("Linux", "linux", None), ("CMake", "cmake", "#3b8fd6"), ("Godot", "godotengine", None)],
    [("Git", "git", None), ("GitHub", "github", "#e6edf3"), ("Maven", "apachemaven", "#e0405a"),
     ("Docker", "docker", None), ("Postman", "postman", None), ("JUnit 5", "junit5", None),
     ("IntelliJ", "intellijidea", "#fe315d"), ("VS Code", None, "#3b9cdc"), ("Python", "python", None),
     ("JavaScript", "javascript", None), ("TypeScript", "typescript", None), ("React", "react", None),
     ("Tailwind", "tailwindcss", None), ("HTML", "html5", None)],
]

CONCEPTS = []

HEADERS = {
    "projects": ("Featured Projects",),
    "opensource": ("Open Source",),
    "certs": ("Certifications",),
    "stack": ("Tech Stack",),
    "currently": ("Currently",),
    "stats": ("GitHub Activity",),
    "education": ("Education",),
}
