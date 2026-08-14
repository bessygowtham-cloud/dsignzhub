#!/usr/bin/env python3
"""Generates the abstract project-showcase artwork in assets/work/.

These are SVG mockups drawn from brand colours rather than photographs — nothing
is downloaded, nothing depends on an external host, and they stay crisp at any
size. Swap them for real project screenshots when those exist.

Run: python3 build/make_shots.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "work")

V1, V2, AM = "#6a5cff", "#8b7bff", "#ffb020"
INK, PANEL, LINE = "#0b0b14", "#171728", "rgba(255,255,255,0.10)"


def frame(inner, w=560, h=380, tint=V1):
    """Browser chrome wrapper shared by the desktop-style shots."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="{w}" y2="{h}" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{tint}" stop-opacity=".30"/><stop offset="1" stop-color="{INK}"/>
  </linearGradient>
  <clipPath id="clip"><rect x="26" y="60" width="{w-52}" height="{h-86}" rx="10"/></clipPath>
</defs>
<rect width="{w}" height="{h}" fill="{INK}"/>
<rect width="{w}" height="{h}" fill="url(#bg)"/>
<rect x="26" y="22" width="{w-52}" height="{h-48}" rx="14" fill="{PANEL}" stroke="{LINE}"/>
<circle cx="48" cy="42" r="4.5" fill="#ff5f57"/><circle cx="64" cy="42" r="4.5" fill="#febc2e"/><circle cx="80" cy="42" r="4.5" fill="#28c840"/>
<rect x="100" y="35" width="{w-150}" height="14" rx="7" fill="rgba(255,255,255,.07)"/>
<g clip-path="url(#clip)">{inner}</g>
</svg>
'''


def bars(x, y, widths, gap=13, h=9, fill="rgba(255,255,255,.20)", r=4):
    return "".join(
        f'<rect x="{x}" y="{y + i*gap}" width="{w}" height="{h}" rx="{r}" fill="{fill}"/>'
        for i, w in enumerate(widths)
    )


def shots():
    out = {}

    # 1 — e-commerce: product grid
    cards = ""
    for r in range(2):
        for c in range(4):
            x, y = 46 + c * 122, 82 + r * 132
            cards += (f'<rect x="{x}" y="{y}" width="106" height="116" rx="10" fill="rgba(255,255,255,.05)" stroke="{LINE}"/>'
                      f'<rect x="{x+10}" y="{y+10}" width="86" height="62" rx="7" fill="{V2}" opacity="{0.30 + 0.09*((r+c)%4)}"/>'
                      + bars(x + 10, y + 82, [70, 40]))
    out["ecommerce.svg"] = frame(cards, tint=V1)

    # 2 — analytics dashboard
    pts = [(0, 96), (1, 74), (2, 82), (3, 52), (4, 60), (5, 34), (6, 42), (7, 18)]
    poly = " ".join(f"{62 + p[0]*61},{192 + p[1]*1.42:.0f}" for p in pts)
    dash = (f'<rect x="46" y="78" width="{560-92}" height="70" rx="10" fill="rgba(255,255,255,.05)" stroke="{LINE}"/>'
            + "".join(f'<g><rect x="{62+i*156}" y="94" width="52" height="9" rx="4" fill="rgba(255,255,255,.18)"/>'
                      f'<rect x="{62+i*156}" y="112" width="{86-i*12}" height="18" rx="6" fill="{AM if i==1 else V2}" opacity=".85"/></g>'
                      for i in range(3))
            + f'<rect x="46" y="162" width="{560-92}" height="188" rx="10" fill="rgba(255,255,255,.04)" stroke="{LINE}"/>'
            + "".join(f'<line x1="62" y1="{196+i*36}" x2="498" y2="{196+i*36}" stroke="rgba(255,255,255,.06)"/>' for i in range(5))
            + f'<polyline points="{poly}" fill="none" stroke="{AM}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
            + "".join(f'<circle cx="{62+p[0]*61}" cy="{192+p[1]*1.42:.0f}" r="4" fill="{AM}"/>' for p in pts))
    out["dashboard.svg"] = frame(dash, tint=V2)

    # 3 — brand identity board
    brand = (f'<rect x="46" y="78" width="228" height="150" rx="12" fill="{V1}"/>'
             f'<g transform="translate(122 118) scale(.86)" fill="#fff">'
             f'<path fill-rule="evenodd" d="M26 14H48A36 36 0 0 1 48 86H14V26Z M30 30H66V40L46 60H66V70H30V60L50 40H30Z"/></g>'
             + "".join(f'<rect x="{292+i*57}" y="78" width="47" height="72" rx="9" fill="{c}"/>'
                       for i, c in enumerate([V1, V2, AM, "#f4f4f7"]))
             + f'<rect x="292" y="164" width="218" height="64" rx="9" fill="rgba(255,255,255,.05)" stroke="{LINE}"/>'
             + bars(306, 182, [180, 130], gap=18, h=12)
             + f'<rect x="46" y="244" width="464" height="106" rx="12" fill="rgba(255,255,255,.04)" stroke="{LINE}"/>'
             + bars(66, 268, [300, 240, 180], gap=22, h=11))
    out["branding.svg"] = frame(brand, tint=AM)

    # 4 — mobile app trio
    phones = ""
    for i, (px, py, s) in enumerate([(150, 96, .92), (240, 74, 1.0), (330, 96, .92)]):
        h = int(230 * s)
        phones += (f'<g transform="translate({px} {py})">'
                   f'<rect width="{int(96*s)}" height="{h}" rx="14" fill="{PANEL}" stroke="{LINE}"/>'
                   f'<rect x="6" y="8" width="{int(84*s)}" height="{int(60*s)}" rx="8" fill="{[V1,AM,V2][i]}" opacity=".8"/>'
                   + bars(6, int(78 * s), [int(84*s), int(60*s), int(72*s)], gap=15, h=8)
                   + f'<rect x="6" y="{h-34}" width="{int(84*s)}" height="22" rx="11" fill="{V2}" opacity=".55"/></g>')
    out["mobile-app.svg"] = frame(phones, tint=V2)

    # 5 — search results / SEO
    seo = (f'<rect x="46" y="78" width="{560-92}" height="40" rx="10" fill="rgba(255,255,255,.06)" stroke="{LINE}"/>'
           f'<circle cx="72" cy="98" r="9" fill="none" stroke="{AM}" stroke-width="2.5"/>'
           f'<line x1="79" y1="105" x2="86" y2="112" stroke="{AM}" stroke-width="2.5" stroke-linecap="round"/>'
           + bars(100, 93, [210], h=11))
    for i in range(4):
        y = 138 + i * 56
        hi = i == 0
        seo += (f'<rect x="46" y="{y}" width="{560-92}" height="46" rx="9" '
                f'fill="{"rgba(139,123,255,.14)" if hi else "rgba(255,255,255,.035)"}" '
                f'stroke="{V2 if hi else LINE}"/>'
                + bars(64, y + 11, [250 - i * 26], h=10, fill=AM if hi else "rgba(255,255,255,.22)")
                + bars(64, y + 27, [380 - i * 34], h=7, fill="rgba(255,255,255,.13)"))
    out["seo.svg"] = frame(seo, tint=AM)

    # 6 — social creative set
    social = ""
    for r in range(2):
        for c in range(3):
            x, y = 56 + c * 156, 84 + r * 134
            social += (f'<rect x="{x}" y="{y}" width="140" height="120" rx="12" fill="rgba(255,255,255,.05)" stroke="{LINE}"/>'
                       f'<rect x="{x+12}" y="{y+12}" width="116" height="70" rx="8" fill="{[V1,AM,V2,V2,V1,AM][r*3+c]}" opacity=".7"/>'
                       + bars(x + 12, y + 92, [96, 62], gap=12, h=8))
    out["social.svg"] = frame(social, tint=V1)

    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, svg in shots().items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(svg)
        print("  assets/work/" + name)


if __name__ == "__main__":
    main()
