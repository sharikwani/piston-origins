"""Generate the crawlable parts of the site from data/site.json + data/youtube.json.

    python tools/fetch_youtube.py   # refresh titles, dates, descriptions (optional)
    python tools/build.py           # rebuild pages, schema, sitemap, llms.txt

Writes: index.html (between <!--build:x--> markers), episodes/**, sitemap.xml,
robots.txt, llms.txt, llms-full.txt.
"""
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")

SITE = json.loads((ROOT / "data/site.json").read_text(encoding="utf-8"))
YT = json.loads((ROOT / "data/youtube.json").read_text(encoding="utf-8"))
BASE = SITE["url"]
LOGO = f"{BASE}/assets/logo.png"
TODAY = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Garage plates on the homepage: name, code, engine, years, episode id
GARAGE = [
    ("Supra Mk4", "JZA80", "2JZ-GTE · 3.0 L I6 twin-turbo", "1993–2002", "18hr_2O-4cg"),
    ("Skyline GT-R", "BNR34", "RB26DETT · 2.6 L I6 twin-turbo", "1999–2002", "_QTVeqC9ARM"),
    ("RX-7", "FD3S", "13B-REW · twin-rotor, sequential turbo", "1992–2002", "R9jLpyg8-3A"),
    ("787B", "Le Mans 1991", "R26B · four-rotor", "1991", "R9jLpyg8-3A"),
    ("NSX", "NA1", "C30A · 3.0 L V6 VTEC", "1990–2005", "LjII0wBnJHA"),
    ("Corolla AE86", "Levin / Trueno", "4A-GE · 1.6 L I4", "1983–1987", "flQ66uxn0DM"),
    ("Lexus LFA", "LFA10", "1LR-GUE · 4.8 L V10", "2010–2012", "NJSd2W415nA"),
    ("GT-R", "R35", "VR38DETT · 3.8 L V6 twin-turbo", "2007–", "u6lgliMatSk"),
    ("Celica GT-Four", "ST205", "3S-GTE · 2.0 L I4 turbo", "1994–1999", "OHUYDjP9DVQ"),
    ("Lamborghini", "350 GTV → 350 GT", "3.5 L V12", "1963–1966", "YPdVXp1ca0c"),
]

EMOJI = re.compile("[\U0001F000-\U0001FFFF☀-➿️]")
URL = re.compile(r"https?://[^\s)]+")
CHAPTER = re.compile(r"^(\d{1,2}:\d{2}(?::\d{2})?)\s+(.+)$")
CTA = re.compile(r"(tell (us|me)|subscribe|watch next|watch all|next episode|more 60-second|new: the|which side|who really won|nsx or)", re.I)

e = lambda s: html.escape(str(s), quote=True)
pad = lambda n: f"{n:02d}"
thumb = lambda vid, q="maxresdefault": f"https://i.ytimg.com/vi/{vid}/{q}.jpg"


def clean_title(t):
    t = re.sub(r"\s#\S+", "", t)
    return re.sub(r"\s{2,}", " ", EMOJI.sub("", t)).strip()


def iso_duration(sec):
    m, s = divmod(sec, 60)
    return f"PT{m}M{s}S" if m else f"PT{s}S"


def human_duration(sec):
    m, s = divmod(sec, 60)
    return f"{m}:{s:02d}"


def human_views(n):
    return f"{n / 1000:.1f}K".replace(".0K", "K") if n >= 1000 else str(n)


def to_seconds(ts):
    parts = [int(p) for p in ts.split(":")]
    return sum(p * 60 ** i for i, p in enumerate(reversed(parts)))


def linkify(text):
    out, last = [], 0
    for m in URL.finditer(text):
        out.append(e(text[last:m.start()]))
        url = m.group(0).rstrip(".,")
        out.append(f'<a href="{e(url)}" rel="nofollow noopener" target="_blank">{e(url)}</a>')
        last = m.start() + len(url)
    out.append(e(text[last:]))
    return "".join(out)


def source_item(line):
    """'Name: https://...' becomes a named link; anything else is linkified."""
    line = line.lstrip("- ").strip()
    m = re.match(r"^(.+?):\s+(https?://\S+)$", line)
    if m:
        return f'<a href="{e(m.group(2))}" rel="nofollow noopener" target="_blank">{e(m.group(1))}</a>'
    return linkify(line)


def parse_description(desc):
    paras = [p.strip().split("\n") for p in re.split(r"\n\s*\n", desc) if p.strip()]
    lede, chapters, sources, credits, disclosure = [], [], [], [], ""
    seen_chapters = False
    for lines in paras:
        head = lines[0].strip().rstrip(":").lower()
        body = "\n".join(lines)
        if any(CHAPTER.match(l.strip()) for l in lines):
            seen_chapters = True
            chapters += [CHAPTER.match(l.strip()).groups() for l in lines if CHAPTER.match(l.strip())]
        elif head == "sources":
            sources += [l for l in lines[1:] if l.strip()]
        elif re.search(r"CC BY|CC0|Public domain|Copyrighted free use", body) or re.match(
                r"^(photos?|stock|music|archival|thumbnail|engine sound|yamaha photos)", head):
            credits.append(body)
        elif "AI-generated" in body:
            disclosure = disclosure or re.sub(r"^About the host\s*", "", body).strip()
            if body.startswith("Facts from") or "Facts from" in body:
                sources.append(re.search(r"Facts from[^\n]*", body).group(0))
        elif body.startswith("Facts from"):
            sources.append(body)
        elif lines[0].startswith("#") or CTA.search(body) or head == "quick answers":
            continue
        elif not seen_chapters:
            lede.append(lines)
    return lede, chapters, sources, credits, disclosure


def render_lede(lede):
    out = []
    for lines in lede:
        items = [l[2:].strip() for l in lines if l.startswith("- ")]
        text = [l for l in lines if not l.startswith("- ")]
        if text:
            out.append(f"<p>{linkify(' '.join(text))}</p>")
        if items:
            out.append("<ul>" + "".join(f"<li>{linkify(i)}</li>" for i in items) + "</ul>")
    return "\n".join(out)


def lede_text(lede):
    return " ".join(l for lines in lede[:1] for l in lines if not l.startswith("- ")).strip()


def jsonld(obj):
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=1) + "\n</script>"


ORG = {
    "@type": "Organization", "@id": f"{BASE}/#org", "name": SITE["name"], "url": f"{BASE}/",
    "logo": {"@type": "ImageObject", "url": LOGO, "width": 256, "height": 256},
    "description": SITE["description"], "sameAs": [SITE["youtube"], SITE["instagram"]],
}


def faq_schema(pairs, page_url):
    return {"@type": "FAQPage", "@id": f"{page_url}#faq", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}


def faq_html(pairs, heading_level="h3"):
    return "\n".join(
        f'<details class="qa"><summary><{heading_level}>{e(q)}</{heading_level}></summary><p>{e(a)}</p></details>'
        for q, a in pairs)


# ---------- Data ----------

EPISODES = []
for ep in SITE["episodes"]:
    y = YT[ep["id"]]
    lede, chapters, sources, credits, disclosure = parse_description(y["description"])
    EPISODES.append({**ep, **y, "title": clean_title(y["title"]), "url": f"{BASE}/episodes/{ep['slug']}/",
                     "lede": lede, "chapters": chapters, "sources": sources, "credits": credits,
                     "disclosure": disclosure, "summary": lede_text(lede)})
EPISODES.sort(key=lambda x: -x["n"])
BY_ID = {x["id"]: x for x in EPISODES}

SHORTS = []
for s in SITE["shorts"]:
    y = YT[s["id"]]
    SHORTS.append({**s, **y, "title": clean_title(y["title"]), "url": f"https://www.youtube.com/shorts/{s['id']}"})
SHORTS.sort(key=lambda x: x["uploadDate"], reverse=True)


def video_object(x, page_url):
    obj = {
        "@type": "VideoObject", "@id": f"{page_url}#video", "name": x["title"],
        "description": x["summary"] or x["title"],
        "thumbnailUrl": [thumb(x["id"]), thumb(x["id"], "hqdefault")],
        "uploadDate": x["uploadDate"], "duration": iso_duration(x["seconds"]),
        "embedUrl": f"https://www.youtube.com/embed/{x['id']}",
        "url": f"https://www.youtube.com/watch?v={x['id']}",
        "interactionStatistic": {"@type": "InteractionCounter", "interactionType": {"@type": "WatchAction"},
                                 "userInteractionCount": x["views"]},
        "publisher": {"@id": f"{BASE}/#org"}, "inLanguage": "en",
    }
    if x.get("car"):
        obj["about"] = {"@type": "Thing", "name": x["car"]}
    if x.get("chapters"):
        starts = [to_seconds(t) for t, _ in x["chapters"]]
        obj["hasPart"] = [{
            "@type": "Clip", "name": label, "startOffset": st,
            "endOffset": starts[i + 1] if i + 1 < len(starts) else x["seconds"],
            "url": f"https://www.youtube.com/watch?v={x['id']}&t={st}s",
        } for i, ((_, label), st) in enumerate(zip(x["chapters"], starts))]
    return obj


# ---------- Shared chrome ----------

def head(title, desc, url, image, extra="", og_type="website"):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<meta name="theme-color" content="#0b0b0c">
<meta property="og:site_name" content="Piston Origins">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{e(title)}">
<meta name="twitter:description" content="{e(desc)}">
<meta name="twitter:image" content="{image}">
<link rel="icon" href="/assets/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="alternate" type="text/plain" title="LLM summary" href="/llms.txt">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Display:wght@500;700;900&family=Inter+Tight:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
{extra}
</head>"""


NAV = """<header class="nav">
  <a href="/" class="brand"><img src="/assets/logo.png" alt="Piston Origins logo" width="32" height="32"><span>Piston Origins</span></a>
  <nav aria-label="Main">
    <a href="/episodes/">Episodes</a>
    <a href="/#secrets">Secrets</a>
    <a href="/#garage">Garage</a>
    <a href="/#faq">FAQ</a>
  </nav>
  <a class="btn btn-sm" href="https://www.youtube.com/@PistonOrigins?sub_confirmation=1" target="_blank" rel="noopener">Subscribe</a>
</header>"""

FOOT = """<footer class="foot wrap">
  <div class="brand"><img src="/assets/logo.png" alt="" width="28" height="28"><span>Piston Origins</span></div>
  <p class="mono small">Every legendary car has an origin story.</p>
  <nav aria-label="Footer">
    <a href="/episodes/">Episodes</a>
    <a href="https://www.youtube.com/@PistonOrigins" target="_blank" rel="noopener">YouTube</a>
    <a href="https://www.instagram.com/pistonorigins/" target="_blank" rel="noopener">Instagram</a>
  </nav>
  <p class="small muted">Vehicle names and marks belong to their owners. Piston Origins is an independent channel and is not affiliated with any manufacturer. The host and voices are AI-generated; the research and sources are real.</p>
</footer>"""


# ---------- Episode pages ----------

EP_SCRIPT = """<script>
document.querySelectorAll('.lite-yt').forEach(b => b.addEventListener('click', () => {
  b.outerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${b.dataset.id}?autoplay=1&rel=0" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen title="${b.dataset.title}"></iframe>`;
}));
</script>"""


def episode_page(x, prev_ep, next_ep):
    url = x["url"]
    desc = (x["summary"] or x["title"])[:300]
    shorts = [s for s in SHORTS if s["ep"] == x["id"]]
    graph = [ORG, {
        "@type": "WebPage", "@id": url, "url": url, "name": x["title"], "isPartOf": {"@id": f"{BASE}/#website"},
        "primaryImageOfPage": thumb(x["id"]), "datePublished": x["uploadDate"], "dateModified": x["uploadDate"],
        "mainEntity": {"@id": f"{url}#video"}, "breadcrumb": {"@id": f"{url}#breadcrumb"}, "inLanguage": "en",
    }, video_object(x, url), {
        "@type": "BreadcrumbList", "@id": f"{url}#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": "Episodes", "item": f"{BASE}/episodes/"},
            {"@type": "ListItem", "position": 3, "name": x["title"], "item": url}]},
    ]
    if x["faq"]:
        graph.append(faq_schema(x["faq"], url))
    ld = jsonld({"@context": "https://schema.org", "@graph": graph})

    date = datetime.fromisoformat(x["uploadDate"]).strftime("%-d %B %Y") if sys.platform != "win32" else \
        datetime.fromisoformat(x["uploadDate"]).strftime("%#d %B %Y")
    chapters = "".join(
        f'<li><a href="https://www.youtube.com/watch?v={x["id"]}&amp;t={to_seconds(t)}s" target="_blank" rel="noopener">'
        f'<span class="mono">{e(t)}</span>{e(label)}</a></li>' for t, label in x["chapters"])
    facts = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in x["facts"])
    sources = "".join(f"<li>{source_item(s)}</li>" for s in x["sources"])
    credits = "".join(f"<p>{linkify(c).replace(chr(10), '<br>')}</p>" for c in x["credits"])
    short_cards = "".join(f"""
      <a class="short" href="{s['url']}" target="_blank" rel="noopener">
        <div class="s-img"><img src="{thumb(s['id'], 'oar2')}" alt="{e(s['title'])}" loading="lazy" width="230" height="409"><span class="views">▶ {human_views(s['views'])} views</span></div>
        <p>{e(s['title'])}</p>
      </a>""" for s in shorts)

    def ep_link(p, label):
        return (f'<a class="ep-nav-link" href="/episodes/{p["slug"]}/"><span class="mono">{label} · EP {pad(p["n"])}</span>'
                f'<strong>{e(p["title"])}</strong></a>') if p else "<span></span>"

    body = f"""
<body class="ep-page">
{NAV}
<main class="wrap ep-main">
  <nav class="crumbs mono" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/episodes/">Episodes</a> / <span>EP {pad(x['n'])}</span></nav>
  <header class="ep-head">
    <p class="eyebrow mono">EP {pad(x['n'])} · {e(x['tag'])} · {e(x['car'])}</p>
    <h1>{e(x['title'])}</h1>
    <p class="ep-meta mono"><time datetime="{x['uploadDate'][:10]}">{date}</time> · {human_duration(x['seconds'])} · {x['views']:,} views on YouTube</p>
  </header>

  <div class="ep-video">
    <button class="lite-yt" data-id="{x['id']}" data-title="{e(x['title'])}" aria-label="Play: {e(x['title'])}">
      <img src="{thumb(x['id'])}" alt="{e(x['title'])} – Piston Origins thumbnail" width="1280" height="720" fetchpriority="high">
      <span class="play">▶</span>
    </button>
  </div>

  <div class="ep-grid">
    <article class="ep-body">
      <section class="ep-lede">{render_lede(x['lede'])}</section>

      {f'<section><h2>Quick answers</h2>{faq_html(x["faq"])}</section>' if x['faq'] else ''}

      {f'<section><h2>Chapters</h2><ol class="chapters">{chapters}</ol></section>' if chapters else ''}

      {f'<section><h2>Sources</h2><ul class="sources">{sources}</ul></section>' if sources else ''}

      <section class="disclose"><p>{e(x['disclosure'] or 'The host and voices are AI-generated. The research, facts and sources are real.')}</p></section>

      {f'<details class="credits"><summary>Photo, footage and music credits</summary>{credits}</details>' if credits else ''}
    </article>

    <aside class="ep-side">
      <h2 class="side-h">Key facts</h2>
      <dl class="facts">{facts}</dl>
      <a class="btn" href="https://www.youtube.com/watch?v={x['id']}" target="_blank" rel="noopener">Watch on YouTube ↗</a>
    </aside>
  </div>

  {f'<section class="ep-shorts"><h2>Car secrets from this story</h2><div class="short-grid">{short_cards}</div></section>' if shorts else ''}

  <nav class="ep-nav" aria-label="More episodes">{ep_link(next_ep, 'Next')}{ep_link(prev_ep, 'Previous')}</nav>
</main>
{FOOT}
{EP_SCRIPT}
</body>
</html>"""
    return head(f"{x['title']} | Piston Origins", desc, url, thumb(x["id"]), ld, "video.episode") + body


def episodes_index():
    url = f"{BASE}/episodes/"
    items = "".join(f"""
    <a class="ep-row" href="/episodes/{x['slug']}/">
      <div class="thumb"><img src="{thumb(x['id'], 'mqdefault')}" alt="{e(x['title'])}" loading="lazy" width="320" height="180"></div>
      <div>
        <p class="eyebrow mono">EP {pad(x['n'])} · {e(x['tag'])} · {human_duration(x['seconds'])}</p>
        <h2>{e(x['title'])}</h2>
        <p class="muted">{e(x['summary'])}</p>
      </div>
    </a>""" for x in EPISODES)
    ld = jsonld({"@context": "https://schema.org", "@graph": [ORG, {
        "@type": "CollectionPage", "@id": url, "url": url, "name": "Piston Origins episodes",
        "isPartOf": {"@id": f"{BASE}/#website"}, "mainEntity": {"@id": f"{url}#list"}}, {
        "@type": "ItemList", "@id": f"{url}#list", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": x["url"], "name": x["title"]} for i, x in enumerate(EPISODES)]}]})
    desc = "Every Piston Origins car-history episode: Toyota Supra Mk4, Nissan Skyline GT-R R34, Mazda rotary RX-7 and 787B, AE86, Honda NSX, Lexus LFA, GT-R vs Porsche, Ferrari vs Lamborghini and Toyota's 1995 WRC ban."
    return head("Car History Episodes | Piston Origins", desc, url, f"{BASE}/assets/og-image.jpg", ld) + f"""
<body class="ep-page">
{NAV}
<main class="wrap ep-main">
  <nav class="crumbs mono" aria-label="Breadcrumb"><a href="/">Home</a> / <span>Episodes</span></nav>
  <header class="ep-head">
    <p class="eyebrow mono">{len(EPISODES)} full stories</p>
    <h1>Car history episodes</h1>
    <p class="ep-meta">The origin stories of legendary cars, the engines behind them, and the rivalries, bans and comebacks that made them. Newest first.</p>
  </header>
  <div class="ep-list">{items}</div>
</main>
{FOOT}
</body>
</html>"""


# ---------- Homepage blocks ----------

def home_blocks():
    cases = "".join(f"""
      <a class="case{' latest' if i == 0 else ''}" href="/episodes/{x['slug']}/" data-vid="{x['id']}">
        <div class="thumb"><img src="{thumb(x['id'])}" alt="{e(x['title'])}" loading="lazy" width="1280" height="720"><span class="play" data-play="{x['id']}" role="button" aria-label="Play {e(x['title'])} here">▶</span></div>
        <div class="c-body">
          <span class="c-num" aria-hidden="true">{pad(x['n'])}</span>
          <div class="meta"><b>EP {pad(x['n'])}</b><span>{e(x['tag'])}</span><span>{e(x['short'])}</span></div>
          <h3>{e(x['title'])}</h3>
        </div>
      </a>""" for i, x in enumerate(EPISODES))
    shorts = "".join(f"""
      <a class="short" href="{s['url']}" data-play="{s['id']}" data-vertical data-make="{e(s['make'])}" target="_blank" rel="noopener">
        <div class="s-img"><img src="{thumb(s['id'], 'oar2')}" alt="" loading="lazy" draggable="false" width="230" height="409"><span class="views">▶ {human_views(s['views'])} views</span></div>
        <p>{e(s['title'])}</p>
      </a>""" for s in SHORTS)
    plates = "".join(f"""
      <a class="plate tilt" href="/episodes/{BY_ID[ep]['slug']}/">
        <div class="bg"><img src="{thumb(ep, 'mqdefault')}" alt="" loading="lazy"></div>
        <span class="code">{e(code)}</span>
        <h3>{e(name)}</h3>
        <dl><dt>Engine</dt><dd>{e(eng)}</dd><dt>Built</dt><dd>{e(era)}</dd></dl>
        <span class="watch">▶ Read the story</span>
      </a>""" for name, code, eng, era, ep in GARAGE)
    total_views = sum(s["views"] for s in SHORTS)
    stats = f"""
      <div><dd data-to="{len(EPISODES)}">{len(EPISODES)}</dd><dt class="mono">Full stories</dt></div>
      <div><dd data-to="{len(SHORTS)}">{len(SHORTS)}</dd><dt class="mono">Car secrets</dt></div>
      <div><dd data-to="{len(GARAGE)}">{len(GARAGE)}</dd><dt class="mono">Legends covered</dt></div>
      <div><dd data-to="{total_views // 1000}" data-suffix="K+">{total_views // 1000}K+</dd><dt class="mono">Shorts views</dt></div>"""
    faq = faq_html(SITE["faq"])

    url = f"{BASE}/"
    ld = jsonld({"@context": "https://schema.org", "@graph": [
        ORG,
        {"@type": "WebSite", "@id": f"{BASE}/#website", "url": url, "name": SITE["name"],
         "description": SITE["description"], "publisher": {"@id": f"{BASE}/#org"}, "inLanguage": "en"},
        {"@type": "WebPage", "@id": url, "url": url, "name": "Piston Origins | Car History Documentaries",
         "isPartOf": {"@id": f"{BASE}/#website"}, "about": {"@id": f"{BASE}/#org"},
         "primaryImageOfPage": f"{BASE}/assets/og-image.jpg", "dateModified": TODAY, "inLanguage": "en"},
        {"@type": "ItemList", "@id": f"{url}#episodes", "name": "Piston Origins episodes", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "url": x["url"], "name": x["title"]} for i, x in enumerate(EPISODES)]},
        faq_schema(SITE["faq"], url),
    ]})
    return {"cases": cases, "shorts": shorts, "plates": plates, "stats": stats, "faq": faq, "jsonld": ld}


def fill(text, name, content):
    pat = re.compile(rf"(<!--build:{name}-->)(.*?)(<!--/build:{name}-->)", re.S)
    if not pat.search(text):
        raise SystemExit(f"index.html is missing <!--build:{name}--> markers")
    return pat.sub(lambda m: m.group(1) + content + "\n" + m.group(3), text)


# ---------- Sitemap, robots, llms ----------

def sitemap():
    latest = max(x["uploadDate"] for x in EPISODES + SHORTS)[:10]
    urls = [f"""  <url><loc>{BASE}/</loc><lastmod>{TODAY}</lastmod><changefreq>weekly</changefreq><priority>1.0</priority></url>""",
            f"""  <url><loc>{BASE}/episodes/</loc><lastmod>{latest}</lastmod><changefreq>weekly</changefreq><priority>0.8</priority></url>"""]
    for x in EPISODES:
        urls.append(f"""  <url>
    <loc>{x['url']}</loc>
    <lastmod>{x['uploadDate'][:10]}</lastmod>
    <priority>0.9</priority>
    <video:video>
      <video:thumbnail_loc>{thumb(x['id'])}</video:thumbnail_loc>
      <video:title>{e(x['title'])}</video:title>
      <video:description>{e((x['summary'] or x['title'])[:2000])}</video:description>
      <video:player_loc>https://www.youtube.com/embed/{x['id']}</video:player_loc>
      <video:duration>{x['seconds']}</video:duration>
      <video:publication_date>{x['uploadDate']}</video:publication_date>
      <video:view_count>{x['views']}</video:view_count>
      <video:family_friendly>yes</video:family_friendly>
    </video:video>
  </url>""")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">\n' + "\n".join(urls) + "\n</urlset>\n")


ROBOTS = f"""# Piston Origins welcomes search engines and AI assistants.
User-agent: *
Allow: /

# Search and AI crawlers, listed explicitly so intent is unambiguous
User-agent: Googlebot
User-agent: Google-Extended
User-agent: Bingbot
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Applebot
User-agent: Applebot-Extended
User-agent: DuckAssistBot
User-agent: CCBot
Allow: /

Sitemap: {BASE}/sitemap.xml
"""


def llms(full=False):
    lines = [f"# {SITE['name']}", "", f"> {SITE['description']}", "",
             f"Piston Origins is on YouTube at {SITE['youtube']} and Instagram at {SITE['instagram']}. "
             f"The host ({SITE['host']}) and narration voice are AI-generated; the research, facts and sources are real "
             "and listed in every video description and on each episode page below.", "",
             "## Episodes (full car stories)", ""]
    for x in EPISODES:
        lines.append(f"- [{x['title']}]({x['url']}): {x['summary']}")
    if not full:
        lines += ["", "## About", "", f"- [Home]({BASE}/): channel overview, all Shorts and FAQ",
                  f"- [All episodes]({BASE}/episodes/)", f"- [Full text for AI]({BASE}/llms-full.txt): every episode's key facts, answers and sources",
                  "", "## FAQ", ""]
        lines += [f"- **{q}** {a}" for q, a in SITE["faq"]]
        return "\n".join(lines) + "\n"
    lines += ["", "---", ""]
    for x in EPISODES:
        lines += [f"## EP {pad(x['n'])}: {x['title']}", "",
                  f"URL: {x['url']}", f"Video: https://www.youtube.com/watch?v={x['id']}",
                  f"Published: {x['uploadDate'][:10]} · Length: {human_duration(x['seconds'])} · Subject: {x['car']}", "",
                  " ".join(" ".join(l for l in p if not l.startswith('- ')) for p in x["lede"]), "", "### Key facts", ""]
        lines += [f"- {k}: {v}" for k, v in x["facts"]]
        if x["faq"]:
            lines += ["", "### Questions and answers", ""]
            for q, a in x["faq"]:
                lines += [f"**{q}**", a, ""]
        if x["chapters"]:
            lines += ["### Chapters", ""] + [f"- {t} {label}" for t, label in x["chapters"]] + [""]
        if x["sources"]:
            lines += ["### Sources", ""] + [f"- {s.lstrip('- ')}" for s in x["sources"]] + [""]
    lines += ["---", "", "## 60-second car secrets (YouTube Shorts)", ""]
    lines += [f"- [{s['title']}]({s['url']}) (from: {BY_ID[s['ep']]['title']})" for s in SHORTS]
    lines += ["", "## FAQ", ""] + [f"**{q}**\n{a}\n" for q, a in SITE["faq"]]
    return "\n".join(lines) + "\n"


# ---------- Write ----------

def main():
    index = ROOT / "index.html"
    text = index.read_text(encoding="utf-8")
    for name, content in home_blocks().items():
        text = fill(text, name, content)
    index.write_text(text, encoding="utf-8")

    (ROOT / "episodes").mkdir(exist_ok=True)
    (ROOT / "episodes/index.html").write_text(episodes_index(), encoding="utf-8")
    for i, x in enumerate(EPISODES):
        newer = EPISODES[i - 1] if i > 0 else None
        older = EPISODES[i + 1] if i + 1 < len(EPISODES) else None
        d = ROOT / "episodes" / x["slug"]
        d.mkdir(exist_ok=True)
        (d / "index.html").write_text(episode_page(x, older, newer), encoding="utf-8")

    (ROOT / "sitemap.xml").write_text(sitemap(), encoding="utf-8")
    (ROOT / "robots.txt").write_text(ROBOTS, encoding="utf-8")
    (ROOT / "llms.txt").write_text(llms(), encoding="utf-8")
    (ROOT / "llms-full.txt").write_text(llms(full=True), encoding="utf-8")
    print(f"Built home, {len(EPISODES)} episode pages, episodes index, sitemap, robots, llms.txt")


if __name__ == "__main__":
    main()
