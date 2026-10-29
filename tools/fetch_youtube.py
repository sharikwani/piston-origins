"""Refresh data/youtube.json (titles, dates, durations, views, descriptions) for every
video listed in data/site.json. Run before tools/build.py when videos change:

    python tools/fetch_youtube.py
"""
import concurrent.futures as cf
import json
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout.reconfigure(encoding="utf-8")


def fetch(video_id):
    req = urllib.request.Request(
        f"https://www.youtube.com/watch?v={video_id}",
        headers={"User-Agent": "Mozilla/5.0", "Accept-Language": "en-US"},
    )
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8")
    m = re.search(r"var ytInitialPlayerResponse = (\{.*?\});(?:var|</script>)", html)
    data = json.loads(m.group(1))
    vd = data["videoDetails"]
    mf = data.get("microformat", {}).get("playerMicroformatRenderer", {})
    return video_id, {
        "title": vd["title"],
        "seconds": int(vd["lengthSeconds"]),
        "views": int(vd.get("viewCount", 0)),
        "uploadDate": mf.get("uploadDate") or mf.get("publishDate"),
        "description": vd.get("shortDescription", ""),
        "keywords": vd.get("keywords", []),
    }


def main():
    site = json.loads((ROOT / "data/site.json").read_text(encoding="utf-8"))
    ids = [e["id"] for e in site["episodes"]] + [s["id"] for s in site["shorts"]]
    out = {}
    with cf.ThreadPoolExecutor(8) as ex:
        for vid, meta in ex.map(fetch, ids):
            out[vid] = meta
            print(f"{vid}  {meta['uploadDate'][:10]}  {meta['views']:>6}  {meta['title'][:70]}")
    (ROOT / "data/youtube.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
