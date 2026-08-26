#!/usr/bin/env python3
"""Renders the project-showcase artwork in assets/work/ as real PNGs.

Each scene is laid out in HTML/CSS inside a proper device frame — browser
chrome, bezels, contact shadows, screen glare — then screenshotted with headless
Chrome at 2x. That reads as a product shot rather than a flat wireframe.

What this cannot do is supply photography. Product tiles and imagery are
rendered as gradient art. Drop real screenshots or licensed photos into
assets/work/ using the same filenames and they take over.

Run: python3 build/make_shots.py
"""
import os
import shutil
import subprocess
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "work")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

W, H = 1120, 760          # rendered at 2x, displayed at 560x380
BLUE, PURPLE = "#2d69fb", "#d278fe"

BASE = """<meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;500;600&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{width:WWpx;height:HHpx;overflow:hidden;font-family:Inter,system-ui,sans-serif;
  background:radial-gradient(120% 100% at 20% 0%,#1b2350 0%,#0a0c1c 45%,#05050a 100%);
  display:flex;align-items:center;justify-content:center}
.stage{position:relative;width:100%;height:100%;display:flex;align-items:center;justify-content:center}
.stage::before{content:'';position:absolute;width:80%;height:70%;top:-12%;left:10%;
  background:radial-gradient(circle,rgba(90,130,255,.30),transparent 65%);filter:blur(30px)}
.stage::after{content:'';position:absolute;width:52%;height:52%;bottom:-8%;right:2%;
  background:radial-gradient(circle,rgba(210,120,254,.26),transparent 65%);filter:blur(34px)}

.win{position:relative;width:84%;border-radius:16px;overflow:hidden;background:#0e1018;
  border:1px solid rgba(255,255,255,.14);
  box-shadow:0 60px 120px -30px rgba(0,0,0,.95),0 20px 50px -20px rgba(0,0,0,.8),
             inset 0 1px 0 rgba(255,255,255,.12)}
.bar{height:44px;display:flex;align-items:center;gap:8px;padding:0 16px;
  background:linear-gradient(180deg,#20232f,#171a24);border-bottom:1px solid rgba(255,255,255,.08)}
.dot{width:11px;height:11px;border-radius:50%}
.url{flex:1;height:24px;margin-left:14px;border-radius:7px;background:#0d0f16;
  border:1px solid rgba(255,255,255,.08);display:flex;align-items:center;padding:0 12px;
  font-size:11.5px;color:#7d8497}
.screen{position:relative;background:#0a0c14;padding:22px}
.win::after{content:'';position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(115deg,rgba(255,255,255,.10) 0%,transparent 34%,transparent 66%,rgba(255,255,255,.045) 100%)}

.phone{position:relative;width:212px;border-radius:34px;padding:9px;background:#15161d;
  border:1px solid rgba(255,255,255,.16);
  box-shadow:0 50px 90px -26px rgba(0,0,0,.95),inset 0 1px 0 rgba(255,255,255,.16)}
.phone .inner{border-radius:26px;overflow:hidden;background:#0a0c14;height:388px;position:relative}
.notch{position:absolute;top:8px;left:50%;transform:translateX(-50%);width:78px;height:20px;
  border-radius:12px;background:#000;z-index:3}
.t{font-family:'Inter Tight',Inter,sans-serif}
</style>
""".replace("WW", str(W)).replace("HH", str(H))


def dots():
    return ('<span class="dot" style="background:#ff5f57"></span>'
            '<span class="dot" style="background:#febc2e"></span>'
            '<span class="dot" style="background:#28c840"></span>')


def win(url, inner):
    return (f'<div class="win"><div class="bar">{dots()}<div class="url">{url}</div></div>'
            f'<div class="screen">{inner}</div></div>')


def tile(i, h=104):
    """Stand-in for a product photo — layered gradient art, not a flat block."""
    hues = [(BLUE, "#7aa2ff"), ("#7d5cff", PURPLE), ("#ff9f45", "#ffd08a"),
            ("#3ddc97", "#9af5cd"), (PURPLE, "#ffb3ff"), ("#4d8dff", "#b9d0ff")]
    a, b = hues[i % len(hues)]
    return (f'<div style="height:{h}px;border-radius:10px;position:relative;overflow:hidden;'
            f'background:linear-gradient(150deg,{a},{b})">'
            f'<div style="position:absolute;inset:0;background:'
            f'radial-gradient(70% 60% at 30% 20%,rgba(255,255,255,.45),transparent 60%),'
            f'radial-gradient(50% 50% at 80% 90%,rgba(0,0,0,.35),transparent 60%)"></div></div>')


def bar(w, h=8, c="rgba(255,255,255,.16)", mb=7):
    return f'<div style="width:{w};height:{h}px;border-radius:4px;background:{c};margin-bottom:{mb}px"></div>'


def scene_ecommerce():
    cards = "".join(
        f'<div style="background:#111420;border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:10px">'
        f'{tile(i)}<div style="margin-top:10px">{bar("74%", 9, "rgba(255,255,255,.28)", 6)}'
        f'{bar("42%", 8, "#7aa2ff", 0)}</div></div>' for i in range(8))
    nav = "".join(bar("52px", 8, "rgba(255,255,255,.22)", 0) for _ in range(4))
    inner = (
        f'<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:18px">'
        f'<div style="display:flex;gap:18px;align-items:center">'
        f'<div style="width:26px;height:26px;border-radius:8px;background:linear-gradient(135deg,{BLUE},{PURPLE})"></div>'
        f'<div style="display:flex;gap:14px">{nav}</div></div>'
        f'<div style="width:74px;height:26px;border-radius:13px;background:linear-gradient(135deg,{BLUE},{PURPLE})"></div></div>'
        f'<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px">{cards}</div>')
    return win("shop.yourbrand.in", inner)


def scene_dashboard():
    pts = [(0, 78), (1, 62), (2, 70), (3, 44), (4, 52), (5, 30), (6, 38), (7, 14)]
    poly = " ".join(f"{40 + p[0] * 108},{170 - p[1] * 1.5:.0f}" for p in pts)
    area = f"{poly} {40 + 7 * 108},175 40,175"
    grid = "".join(f'<line x1="40" y1="{40 + i * 34}" x2="840" y2="{40 + i * 34}" stroke="rgba(255,255,255,.055)"/>'
                   for i in range(5))
    knobs = "".join(f'<circle cx="{40 + p[0] * 108}" cy="{170 - p[1] * 1.5:.0f}" r="4.5" fill="#fff"/>' for p in pts)
    kpis = "".join(
        f'<div style="flex:1;background:#111420;border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:14px 16px">'
        f'<div style="font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:#7d8497">{label}</div>'
        f'<div class="t" style="font-size:26px;font-weight:500;color:{col};margin-top:6px">{val}</div></div>'
        for label, val, col in [("Revenue", "&#8377;18.4L", "#7aa2ff"),
                                ("Orders", "2,318", PURPLE), ("ROAS", "4.2x", "#3ddc97")])
    inner = (
        f'<div style="display:flex;gap:12px;margin-bottom:16px">{kpis}</div>'
        f'<div style="background:#111420;border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:16px">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">'
        f'<div class="t" style="font-size:14px;color:#e7eaf3">Revenue, last 8 weeks</div>'
        f'<div style="font-size:11px;color:#7d8497">Weekly</div></div>'
        f'<svg viewBox="0 0 880 200" style="width:100%;height:190px">'
        f'<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{BLUE}" stop-opacity=".45"/>'
        f'<stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient></defs>'
        f'{grid}<polygon points="{area}" fill="url(#g)"/>'
        f'<polyline points="{poly}" fill="none" stroke="{BLUE}" stroke-width="3" '
        f'stroke-linecap="round" stroke-linejoin="round"/>{knobs}</svg></div>')
    return win("app.yourbrand.in/analytics", inner)


def scene_branding():
    sw = "".join(f'<div style="flex:1;height:78px;border-radius:10px;background:{c}"></div>'
                 for c in [BLUE, "#7d5cff", PURPLE, "#f2f2f7"])
    inner = (
        f'<div style="display:grid;grid-template-columns:1.15fr 1fr;gap:14px">'
        f'<div style="background:linear-gradient(150deg,{BLUE},{PURPLE});border-radius:14px;display:flex;'
        f'align-items:center;justify-content:center;height:186px;position:relative;overflow:hidden">'
        f'<div style="position:absolute;inset:0;background:radial-gradient(60% 60% at 30% 20%,rgba(255,255,255,.35),transparent 60%)"></div>'
        f'<svg viewBox="0 0 100 100" style="width:88px;position:relative"><path fill="#fff" fill-rule="evenodd" '
        f'd="M26 14H48A36 36 0 0 1 48 86H14V26Z M30 30H66V40L46 60H66V70H30V60L50 40H30Z"/></svg></div>'
        f'<div style="display:flex;flex-direction:column;gap:12px">'
        f'<div style="display:flex;gap:10px">{sw}</div>'
        f'<div style="flex:1;background:#111420;border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:14px">'
        f'<div class="t" style="font-size:30px;font-weight:500;color:#fff;letter-spacing:-.02em">Aa</div>'
        f'<div style="margin-top:10px">{bar("85%")}{bar("62%")}</div></div></div></div>'
        f'<div style="margin-top:14px;background:#111420;border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:16px">'
        f'{bar("55%", 10, "rgba(255,255,255,.26)")}{bar("78%")}{bar("40%", 8, "rgba(255,255,255,.12)", 0)}</div>')
    return win("brand guidelines", inner)


def scene_pwa():
    def phone(offset, scale, z):
        rows = "".join(
            f'<div style="display:flex;gap:9px;align-items:center;margin-bottom:11px">'
            f'<div style="width:44px;height:44px;border-radius:10px;'
            f'background:linear-gradient(140deg,{BLUE},{PURPLE});opacity:{0.55 + 0.12 * j}"></div>'
            f'<div style="flex:1">{bar("78%", 8, "rgba(255,255,255,.24)", 5)}'
            f'{bar("48%", 7, "rgba(255,255,255,.12)", 0)}</div></div>' for j in range(4))
        return (
            f'<div class="phone" style="transform:translateY({offset}px) scale({scale});z-index:{z}">'
            f'<div class="notch"></div><div class="inner">'
            f'<div style="height:118px;background:linear-gradient(150deg,{BLUE},{PURPLE});position:relative">'
            f'<div style="position:absolute;inset:0;background:radial-gradient(70% 70% at 30% 20%,rgba(255,255,255,.4),transparent 60%)"></div></div>'
            f'<div style="padding:14px">{rows}</div>'
            f'<div style="position:absolute;left:14px;right:14px;bottom:14px;height:38px;border-radius:19px;'
            f'background:linear-gradient(135deg,{BLUE},{PURPLE})"></div></div></div>')
    return (f'<div style="display:flex;align-items:center;justify-content:center;gap:18px">'
            f'{phone(26, .88, 1)}{phone(-14, 1.0, 3)}{phone(26, .88, 1)}</div>')


def scene_seo():
    rows = ""
    for i in range(4):
        hi = i == 0
        title = ('<div class="t" style="font-size:13.5px;color:#9fc0ff">yourbrand.in &mdash; official site</div>'
                 if hi else bar("46%", 9, "rgba(255,255,255,.2)", 0))
        rows += (
            f'<div style="background:{"rgba(45,105,251,.14)" if hi else "#111420"};'
            f'border:1px solid {"rgba(122,162,255,.45)" if hi else "rgba(255,255,255,.06)"};'
            f'border-radius:11px;padding:14px 16px;margin-bottom:10px">'
            f'<div style="display:flex;align-items:center;gap:9px;margin-bottom:8px">'
            f'<div style="width:18px;height:18px;border-radius:5px;background:linear-gradient(135deg,{BLUE},{PURPLE})"></div>'
            f'{title}</div>{bar("88%", 7, "rgba(255,255,255,.13)", 5)}'
            f'{bar("66%", 7, "rgba(255,255,255,.10)", 0)}</div>')
    inner = (
        f'<div style="display:flex;align-items:center;gap:10px;background:#111420;'
        f'border:1px solid rgba(255,255,255,.08);border-radius:22px;padding:11px 16px;margin-bottom:16px">'
        f'<svg viewBox="0 0 24 24" style="width:16px;height:16px;fill:none;stroke:{PURPLE};stroke-width:2">'
        f'<circle cx="10.5" cy="10.5" r="6.5"/><path d="M21 21l-5.7-5.7"/></svg>'
        f'<div style="font-size:13px;color:#c8cddb">best web design company near me</div></div>{rows}')
    return win("google.co.in/search", inner)


def scene_social():
    tiles = "".join(
        f'<div style="background:#111420;border:1px solid rgba(255,255,255,.07);border-radius:12px;padding:9px">'
        f'{tile(i, 96)}<div style="margin-top:9px;display:flex;align-items:center;gap:7px">'
        f'<div style="width:20px;height:20px;border-radius:50%;background:linear-gradient(135deg,{BLUE},{PURPLE})"></div>'
        f'<div style="flex:1">{bar("70%", 7, "rgba(255,255,255,.22)", 0)}</div></div></div>' for i in range(6))
    return win("campaign creative",
               f'<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:12px">{tiles}</div>')


SCENES = {
    "ecommerce": scene_ecommerce,
    "dashboard": scene_dashboard,
    "branding": scene_branding,
    "mobile-app": scene_pwa,
    "seo": scene_seo,
    "social": scene_social,
}


def main():
    if not os.path.exists(CHROME):
        raise SystemExit("Google Chrome not found — needed to render the mockups.")
    os.makedirs(OUT, exist_ok=True)
    tmp = tempfile.mkdtemp()

    for name, fn in SCENES.items():
        html = os.path.join(tmp, name + ".html")
        with open(html, "w", encoding="utf-8") as f:
            f.write(BASE + f'<div class="stage">{fn()}</div>')
        subprocess.run([
            CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=2", f"--window-size={W},{H}",
            "--virtual-time-budget=5000",
            f"--screenshot={os.path.join(OUT, name + '.png')}", f"file://{html}",
        ], capture_output=True)
        old = os.path.join(OUT, name + ".svg")       # flat version is superseded
        if os.path.exists(old):
            os.remove(old)
        print("  assets/work/" + name + ".png")

    shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
