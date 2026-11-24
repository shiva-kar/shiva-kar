#!/usr/bin/env python3
"""Configuration file for Shiva Kar's GitHub profile.

Edit this file to update your profile bio, status, milestones, featured projects,
tech stack, developer tools, and certifications. Running `python scripts/render-svgs.py`
will re-render all SVG cards and update README.md automatically.
"""

USER = "shiva-kar"
NAME = "Shiva Kar"
SUBTITLE = "Java Backend Developer · BCA Student"
LOCATION = "Hojai, Assam, India"
CGPA = "8.84/10"

# Bio narrative: human, clear, zero AI em dashes
ABOUT = (
    "Undergraduate at Amity University Online (CGPA: 8.84/10) focused on Java backend engineering "
    "(REST APIs, PostgreSQL, Redis, JPA/Hibernate). Contributor to open-source software across "
    "Godot Engine in C++ (editor, GUI, subsystems), developer tooling, and community ecosystems. "
    "Author of SXSHELL, a modular POSIX shell in C (~550 lines). Based in Hojai, Assam, India."
)


LINKS = {
    "linkedin": ("LinkedIn", "linkedin", "https://www.linkedin.com/in/shiva-kar/"),
    "email": ("Email", "gmail", "mailto:sksmarttech48@gmail.com"),
    "portfolio": ("Portfolio", "googlechrome", "https://shivakar.me"),
    "github": ("GitHub", "github", "https://github.com/shiva-kar"),
    "x": ("X", "x", "https://x.com/sk_shivakar"),
}

METRICS_STRIP = [
    ("BCA Computer Science", "CGPA 8.84/10", "Amity University Online"),
    ("Open Source", "7 Merged PRs", "Upstream contributor"),
    ("Primary Stack", "Java · Spring Boot", "PostgreSQL · Redis · Docker"),
    ("Based in", "Hojai, Assam, India", "Open to Remote / Relocation"),
]

CURRENTLY = [
    "Building backend applications with Java, Spring Boot, PostgreSQL, and Redis",
    "REST API design, database persistence, authentication, transactions, and concurrency",
    "Practicing Data Structures & Algorithms and strengthening CS fundamentals",
    "Contributing bug fixes and improvements to open-source projects (Godot Engine, tools, themes)",
    "Exploring systems programming, networking, and game engine internals",
]

# (year label, short title, institution, dates, full degree name)
EDU = [
    ("2017", "Class X", "Rabindra Bidyalaya High School", "Jan 2017 - Mar 2022",
     "Secondary Education (Class X)"),
    ("2022", "Class XII, PCM + CS", "Deshabandhu Bidyapeeth HS", "Jul 2022 - Mar 2025",
     "Higher Secondary (Class XII), Science (PCM + Computer Science)"),
    ("2025", "BCA, Computer Science", "Amity University Online", "Jul 2025 - Nov 2028 (Expected)",
     "Bachelor of Computer Applications (BCA), Computer Science (CGPA: 8.84/10)"),
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

PROJECTS = [
    {
        "title": "E-Commerce Backend API",
        "category": "Core Java & Spring Boot",
        "stack": "Java · Spring Boot · Spring Security · Spring Data JPA · Hibernate · PostgreSQL · Docker · JUnit 5 · Mockito",
        "desc": "An e-commerce backend providing REST APIs for product management, shopping carts, orders, and user accounts with PostgreSQL persistence and secure JWT authentication.",
        "highlights": [
            "Layered controller-service-repository architecture with DTO pattern and centralized error handling",
            "Spring Security with JWT authentication, password hashing, and role-based endpoint authorization",
            "PostgreSQL persistence with Spring Data JPA/Hibernate, transactional integrity, and Docker environment",
        ],
    },
    {
        "title": "API Rate Limiter & Metering Service",
        "category": "Distributed Systems",
        "stack": "Java · Spring Boot · Redis · PostgreSQL · Bucket4j · Docker Compose",
        "desc": "A distributed rate limiting and API usage metering service providing sliding-window and token-bucket algorithms with Redis atomic operations and client tier quotas.",
        "highlights": [
            "Token-bucket and sliding-window rate limiting algorithms backed by Redis atomic operations",
            "Client tier quotas and distributed rate enforcement across high-concurrency endpoints",
            "Header-based rate limit feedback (X-RateLimit-*) and usage metering analytics",
        ],
    },
    {
        "title": "SXSHELL (Unix-like POSIX Shell)",
        "category": "Systems Programming in C",
        "stack": "C · POSIX APIs · GCC · Make",
        "desc": "A modular POSIX shell in C (~550 lines) implementing command parsing, fork/exec process management, I/O redirection, and pipelines.",
        "highlights": [
            "Modular architecture with 7 distinct C units and clean subsystem separation (~550 lines)",
            "Process lifecycle management using fork, execvp, and waitpid system calls",
            "I/O redirection (<, >, >>) and multi-command pipeline execution (|)",
        ],
    },
]

DISCIPLINES = [
    ("Languages", [
        ("Java", "openjdk", "#f89820"),
        ("C", "c", "#a8b9cc"),
        ("SQL", "postgresql", "#4169e1"),
        ("C++", "cplusplus", "#4aa3e0"),
        ("Python", "python", "#3776ab"),
        ("TypeScript", "typescript", "#3178c6"),
    ]),
    ("Backend & Persistence", [
        ("Spring Boot", "springboot", "#6db33f"),
        ("Spring Data JPA", "hibernate", "#b7c0c8"),
        ("Hibernate", "hibernate", "#b7c0c8"),
        ("PostgreSQL", "postgresql", "#4169e1"),
        ("Redis", "redis", "#dc382d"),
        ("MySQL", "mysql", "#5aa5d6"),
    ]),
    ("Systems & DevOps", [
        ("POSIX APIs", "linux", "#fcc624"),
        ("Linux", "linux", "#fcc624"),
        ("Docker", "docker", "#2496ed"),
        ("Git", "git", "#f05032"),
        ("Maven", "apachemaven", "#c71a36"),
        ("CMake", "cmake", "#3b8fd6"),
    ]),
    ("Testing & Environment", [
        ("JUnit 5", "junit5", "#25a162"),
        ("Mockito", "junit5", "#25a162"),
        ("IntelliJ IDEA", "intellijidea", "#fe315d"),
        ("Postman", "postman", "#ff6c37"),
        ("VS Code", None, "#3b9cdc"),
        ("GitHub", "github", "#e6edf3"),
    ]),
]

HEADERS = {
    "projects": ("What I've built.",),
    "opensource": ("Open source contributions.",),
    "certs": ("Verified certifications.",),
    "stack": ("Technologies & tools.",),
    "currently": ("Current focus.",),
    "stats": ("Contribution activity.",),
    "education": ("Education & coursework.",),
}
