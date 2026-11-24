#!/usr/bin/env python3
"""Collects public GitHub data for the profile cards into data/profile.json.
Uses GITHUB_TOKEN when present (higher rate limits); falls back to scraping public pages."""
import html, json, os, re, sys, urllib.parse, urllib.request
from datetime import date, datetime, timedelta

USER = os.environ.get("PROFILE_USER", "shiva-kar")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKEN = os.environ.get("GITHUB_TOKEN")


def get(url, accept=None, api=False):
    h = {"User-Agent": "Mozilla/5.0 profile-card-generator"}
    if accept:
        h["Accept"] = accept
    if api and TOKEN:
        h["Authorization"] = f"Bearer {TOKEN}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=h), timeout=25) as r:
            return r.read().decode("utf-8", "replace")
    except Exception as e:  # noqa
        print("  fetch failed:", url, e, file=sys.stderr)
        return ""


def api(path):
    t = get("https://api.github.com" + path, api=True)
    try:
        return json.loads(t)
    except Exception:
        return {}


def num(s):
    return int(re.sub(r"[^\d]", "", s) or 0)


def profile_page():
    s = get(f"https://github.com/{USER}")
    d = {"login": USER}
    m = re.search(r'itemprop="name"[^>]*>\s*([^<]+?)\s*<', s)
    d["name"] = html.unescape(m.group(1)) if m else USER
    m = re.search(r'itemprop="homeLocation".*?<span class="p-label">([^<]+)', s, re.S)
    d["location"] = html.unescape(m.group(1).strip()) if m else ""
    m = re.search(r'text-bold color-fg-default">([\d.,kK]+)</span>\s*followers', s)
    d["followers"] = num(m.group(1)) if m else 0
    return d


def repos():
    out, page = [], 1
    while page < 6:
        s = get(f"https://github.com/{USER}?tab=repositories&type=source&sort=stargazers&page={page}")
        items = s.split('itemprop="owns"')[1:]
        if not items:
            break
        for b in items:
            n = re.search(r'href="/%s/([^"]+)"' % USER, b)
            if not n:
                continue
            d = re.search(r'itemprop="description">\s*(.*?)\s*</p>', b, re.S)
            l = re.search(r'itemprop="programmingLanguage">([^<]+)', b)
            st = re.search(r'href="/%s/%s/stargazers"[^>]*>(.*?)</a>' % (USER, re.escape(n.group(1))), b, re.S)
            fk = re.search(r'href="/%s/%s/forks"[^>]*>(.*?)</a>' % (USER, re.escape(n.group(1))), b, re.S)
            tp = re.findall(r'title="Topic: ([^"]+)"', b)
            dt = re.search(r'datetime="([^"]+)"', b)
            out.append({"name": n.group(1), "desc": html.unescape(d.group(1).strip()) if d else "",
                        "lang": l.group(1) if l else "", "stars": num(re.sub(r"<[^>]+>", "", st.group(1))) if st else 0,
                        "forks": num(re.sub(r"<[^>]+>", "", fk.group(1))) if fk else 0, "topics": tp,
                        "updated": dt.group(1)[:10] if dt else ""})
        page += 1
    return sorted(out, key=lambda r: (-r["stars"], r["updated"]), reverse=False)


def languages(rs):
    """Code size via REST when available (e.g. in Actions with a token), else primary language per repo."""
    tot = {}
    for r in rs:
        j = api(f"/repos/{USER}/{r['name']}/languages")
        if not (isinstance(j, dict) and j and "message" not in j):
            tot = {}
            break
        for k, v in j.items():
            tot[k] = tot.get(k, 0) + v
    basis = "code size"
    if not tot:
        basis = "repos"
        for r in rs:
            if r["lang"]:
                tot[r["lang"]] = tot.get(r["lang"], 0) + 1
    t = sum(tot.values()) or 1
    return basis, [{"name": k, "pct": round(100 * v / t, 1)} for k, v in sorted(tot.items(), key=lambda x: -x[1])]


def calendar():
    s = get(f"https://github.com/users/{USER}/contributions")
    tips = {}
    for cid, txt in re.findall(r'for="(contribution-day-component-[\d-]+)"[^>]*>([^<]*)<', s):
        m = re.match(r"(\d+) contribution", txt.strip())
        tips[cid] = int(m.group(1)) if m else 0
    days = []
    for d, cid, lv in re.findall(r'data-date="([\d-]+)" id="(contribution-day-component-[\d-]+)" data-level="(\d)"', s):
        days.append({"date": d, "count": tips.get(cid, 0), "level": int(lv)})
    days.sort(key=lambda x: x["date"])
    m = re.search(r">\s*([\d,]+)\s+contributions", s)
    total = num(m.group(1)) if m else sum(x["count"] for x in days)
    # streaks
    longest = cur = best = 0
    for x in days:
        cur = cur + 1 if x["count"] else 0
        longest = max(longest, cur)
    today = date.today().isoformat()
    cur = 0
    for x in reversed([x for x in days if x["date"] <= today]):
        if x["count"]:
            cur += 1
        elif x["date"] != today:
            break
    return {"total": total, "days": days, "current_streak": cur, "longest_streak": longest,
            "active_days": sum(1 for x in days if x["count"])}


def stars_of(repo):
    j = api(f"/repos/{repo}")
    if isinstance(j, dict) and "stargazers_count" in j:
        return j["stargazers_count"]
    s = get(f"https://github.com/{repo}")
    m = re.search(r'"stargazerCount":(\d+)', s)
    return int(m.group(1)) if m else 0


def prs(state):
    q = urllib.parse.quote(f"is:pr author:{USER} is:{state} -user:{USER}")
    j = api(f"/search/issues?q={q}&per_page=100&sort=updated")
    out = []
    for i in j.get("items", []):
        repo = i["repository_url"].split("repos/")[1]
        out.append({"repo": repo, "number": i["number"], "title": i["title"],
                    "date": (i.get("closed_at") or i["created_at"])[:10]})
    return out


def count(path):
    return api(path).get("total_count", 0)


def main():
    data = profile_page()
    rs = repos()
    data["repos"] = rs
    data["stars"] = sum(r["stars"] for r in rs)
    basis, langs = languages(rs)
    data["languages"], data["languages_basis"] = langs[:6], basis
    data["calendar"] = calendar()
    old_data = {}
    if os.path.exists(os.path.join(ROOT, "data", "profile.json")):
        try:
            with open(os.path.join(ROOT, "data", "profile.json"), encoding="utf-8") as f:
                old_data = json.load(f)
        except Exception:
            pass

    merged_data = prs("merged")
    open_data = prs("open")
    data["merged"] = merged_data if merged_data else old_data.get("merged", [])
    data["open"] = open_data if open_data else old_data.get("open", [])
    cache = {}
    for p in data["merged"] + data["open"]:
        cache.setdefault(p["repo"], None)
    for r in cache:
        cache[r] = stars_of(r)
    data["upstream_stars"] = cache
    data["prs_total"] = count(f"/search/issues?q=author:{USER}+type:pr&per_page=1")
    data["issues_total"] = count(f"/search/issues?q=author:{USER}+type:issue&per_page=1")
    data["generated"] = datetime.now().strftime("%Y-%m-%d")
    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    with open(os.path.join(ROOT, "data", "profile.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=1)
    print({k: (v if not isinstance(v, (list, dict)) else len(v)) for k, v in data.items()})


if __name__ == "__main__":
    main()
