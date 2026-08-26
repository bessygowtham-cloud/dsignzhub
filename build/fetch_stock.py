#!/usr/bin/env python3
"""Downloads the showcase photography from Unsplash into assets/work/.

Unsplash photos are free for commercial use and need no attribution
(https://unsplash.com/license) — but check any image you swap in yourself, and
replace these with your own project screenshots as soon as you have them, since
real work beats stock on an agency site.

Each entry is pinned to a specific photo id so a rebuild is reproducible.
Re-run after editing PHOTOS:  python3 build/fetch_stock.py
"""
import os
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "work")

W, H = 1200, 815          # 560x380 card, retina

# showcase slug -> (unsplash photo id, what it shows)
PHOTOS = {
    "ecommerce":  ("1556742049-0cfed4f6a45d", "customer paying by phone at a retail counter"),
    "dashboard":  ("1551288049-bebda4e38f71", "analytics dashboard on screen"),
    "branding":   ("1626785774573-4b799315345d", "design tools and colour swatches on a desk"),
    "mobile-app": ("1563986768609-322da13575f3", "hand using a phone beside a laptop"),
    "seo":        ("1460925895917-afdab827c52f", "laptop showing charts and reporting"),
    "social":     ("1542744173-8e7e53415bb0", "team working through a campaign"),
}

URL = ("https://images.unsplash.com/photo-{pid}"
       "?w={w}&h={h}&fit=crop&crop=entropy&q=80&fm=jpg")


def main():
    os.makedirs(OUT, exist_ok=True)
    wanted = sys.argv[1:] or list(PHOTOS)
    for slug in wanted:
        pid, desc = PHOTOS[slug]
        url = URL.format(pid=pid, w=W, h=H)
        dest = os.path.join(OUT, slug + ".jpg")
        req = urllib.request.Request(url, headers={"User-Agent": "dsignzhub-build"})
        with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
            f.write(r.read())
        # the 3D renders these replace are no longer referenced
        old = os.path.join(OUT, slug + ".png")
        if os.path.exists(old):
            os.remove(old)
        print(f"  assets/work/{slug}.jpg  {os.path.getsize(dest)//1024} KB  — {desc}")


if __name__ == "__main__":
    main()
