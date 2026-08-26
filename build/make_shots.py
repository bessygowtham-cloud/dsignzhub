#!/usr/bin/env python3
"""Bakes the project-showcase images as 3D clay renders.

Each scene is composed from three.js primitives — matte materials, a broad
studio key light, real cast shadows and a gradient backdrop — then rendered in
headless Chrome and screenshotted. That gives the modern 3D product-render look
rather than flat vector art, without needing downloaded models or photography.

Software rendering (SwiftShader) is slow, so expect ~30-60s per scene.

Run: python3 build/make_shots.py [scene ...]
"""
import http.server
import os
import shutil
import socketserver
import subprocess
import sys
import tempfile
import threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "work")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
W, H = 1120, 760
PORT = 4771

IMPORTMAP = """
<script type="importmap">
{"imports":{
  "three":"https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.module.js",
  "three/addons/":"https://cdn.jsdelivr.net/npm/three@0.169.0/examples/jsm/"
}}
</script>"""

PAGE = """<!doctype html><meta charset="utf-8"><title>rendering</title>
<style>html,body{margin:0;background:#000;overflow:hidden}canvas{display:block}</style>
%(map)s
<script type="module">
import * as THREE from 'three';
import { makeStage, finish, box, cyl, ball, torus, panel, clay, P } from './scene3d.js';
const W=%(W)s, H=%(H)s;
%(body)s
</script>
"""

# ---------------------------------------------------------------- scenes
# Palette stays in the site's blue/violet family with warm accents, so the
# renders sit on the dark UI instead of fighting it.
BG1, BG2 = "'#efeaff'", "'#c4b8e4'"

SCENES = {}

SCENES["ecommerce"] = """
const S = makeStage({bg1:__BG1__, bg2:__BG2__, w:W, h:H});
const g = S.root;

// --- shopping bag: reads instantly, unlike a cart built from primitives ---
const bag = new THREE.Group();
const body2 = box(2.5,2.6,1.35,P.coral,{r:0.1,rough:0.75});
body2.position.y = 1.3; bag.add(body2);
const lip = box(2.56,0.22,1.42,P.cream,{r:0.07}); lip.position.y=2.6; bag.add(lip);
[[-0.62],[0.62]].forEach(([x])=>{
  const hd = torus(0.42,0.07,P.cream); hd.position.set(x,2.72,0);
  hd.rotation.x = Math.PI/2; hd.scale.set(1,0.75,1); bag.add(hd); });
bag.position.set(-1.0,0,2.4); bag.rotation.y=0.38; g.add(bag);

// items peeking out of the bag
const it1 = box(0.62,0.9,0.62,P.blue,{r:0.09}); it1.position.set(-1.5,3.0,2.35); it1.rotation.set(0.1,0.4,0.12); g.add(it1);
const it2 = cyl(0.26,0.26,0.8,P.amber,28); it2.position.set(-0.6,2.95,2.2); it2.rotation.z=0.2; g.add(it2);

// --- parcels, fanned so each one reads ---
const b1 = box(2.3,2.3,2.3,P.coral,{r:0.14}); b1.position.set(-3.7,1.15,-0.6); b1.rotation.y=0.34; g.add(b1);
const b2 = box(1.6,1.6,1.6,P.sand,{r:0.12});  b2.position.set(-1.9,0.8,-1.9); b2.rotation.y=-0.25; g.add(b2);
const b3 = box(1.35,1.35,1.35,P.violet,{r:0.1}); b3.position.set(1.7,0.68,-2.5); b3.rotation.y=0.5; g.add(b3);
const b4 = box(1.0,1.0,1.0,P.amber,{r:0.09}); b4.position.set(0.2,0.5,-1.4); b4.rotation.y=-0.55; g.add(b4);

// --- tablet, angled into the light ---
const tab = panel(2.7,3.5,P.slate,P.blue,0.22);
tab.position.set(3.5,1.75,0.4); tab.rotation.set(-0.07,-0.5,0.03); g.add(tab);

// --- card + coin stack in front ---
const card = box(1.5,0.1,1.0,P.purple,{r:0.06});
card.position.set(1.9,0.06,2.9); card.rotation.y=-0.4; g.add(card);
[0,1,2,3].forEach(i=>{ const c2=cyl(0.32,0.32,0.1,P.amber,32);
  c2.position.set(-3.1,0.06+i*0.11,2.6); c2.rotation.y=i*0.3; g.add(c2); });

g.position.y = -0.8;
finish(S);
"""

SCENES["dashboard"] = """
const S = makeStage({bg1:__BG1__, bg2:__BG2__, w:W, h:H});
const g = S.root;

// main screen
const scr = panel(6.6,4.3,P.slate,P.ink,0.26);
scr.position.set(0,2.9,0); scr.rotation.set(-0.05,0.16,0); g.add(scr);

// 3D bars rising out of the screen
const vals=[1.1,1.8,1.4,2.5,2.1,3.2];
vals.forEach((v,i)=>{
  const c = i===3||i===5 ? P.amber : (i%2 ? P.blueLt : P.blue);
  const b = box(0.62,v,0.62,c,{r:0.1});
  b.position.set(-2.1+i*0.85, v/2+0.9, 1.9); g.add(b);
});
// platform under the bars
const plate = box(6.2,0.3,1.5,P.cream,{r:0.1}); plate.position.set(0.05,0.75,1.9); g.add(plate);

// floating KPI cards
const c1 = box(1.9,1.1,0.14,P.cream,{r:0.12}); c1.position.set(-3.9,4.4,2.2); c1.rotation.set(0.05,0.5,0.06); g.add(c1);
const c2 = box(1.7,1.0,0.14,P.violet,{r:0.12}); c2.position.set(4.0,3.6,2.0); c2.rotation.set(-0.05,-0.5,-0.05); g.add(c2);

// arrow ball trail
[0,1,2].forEach(i=>{ const s=ball(0.2-i*0.04,P.amber); s.position.set(2.6+i*0.7,4.7+i*0.55,1.4); g.add(s); });

g.position.y=-1.4;
finish(S);
"""

SCENES["branding"] = """
const S = makeStage({bg1:__BG1__, bg2:__BG2__, w:W, h:H});
const g = S.root;

// logo plinth
const plinth = box(3.2,3.2,0.5,P.blue,{r:0.18});
plinth.position.set(-1.5,2.0,0); plinth.rotation.set(-0.04,0.3,0); g.add(plinth);
// extruded Z sitting proud of it
const zShape = new THREE.Shape();
[[-0.9,0.9],[0.75,0.9],[0.75,0.45],[-0.2,-0.45],[0.75,-0.45],[0.75,-0.9],[-0.9,-0.9],[-0.9,-0.45],[0.05,0.45],[-0.9,0.45]]
 .forEach((p,i)=> i? zShape.lineTo(p[0],p[1]) : zShape.moveTo(p[0],p[1]));
zShape.closePath();
const zGeo = new THREE.ExtrudeGeometry(zShape,{depth:0.34,bevelEnabled:true,bevelSize:0.05,bevelThickness:0.05,bevelSegments:3});
zGeo.center();
const zMesh = new THREE.Mesh(zGeo, clay(P.cream,{rough:0.5}));
zMesh.castShadow=true; zMesh.position.set(-1.5,2.0,0.45); zMesh.rotation.set(-0.04,0.3,0); g.add(zMesh);

// paint-pot swatches
[[P.blue,0],[P.violet,1],[P.purple,2],[P.amber,3]].forEach(([c,i])=>{
  const pot = cyl(0.52,0.46,1.5-i*0.12,c,36);
  pot.position.set(1.9+i*1.15, (1.5-i*0.12)/2, 1.3-i*0.5); g.add(pot);
  const lid = cyl(0.55,0.55,0.1,P.cream,36); lid.position.set(1.9+i*1.15,(1.5-i*0.12)+0.05,1.3-i*0.5); g.add(lid);
});

// stacked brand cards
[0,1,2].forEach(i=>{
  const card = box(2.6,0.12,1.7,i===0?P.cream:(i===1?P.sand:P.coral),{r:0.07});
  card.position.set(-3.0,0.07+i*0.16,2.5); card.rotation.y=-0.32+i*0.06; g.add(card);
});

g.position.y=-1.0;
finish(S);
"""

SCENES["mobile-app"] = """
const S = makeStage({bg1:__BG1__, bg2:__BG2__, w:W, h:H});
const g = S.root;

function phone(x,y,z,ry,scale,screen){
  const p = new THREE.Group();
  const body = box(2.5,5.0,0.30,P.slate,{r:0.32,rough:0.55});
  const sc = box(2.25,4.6,0.16,screen,{r:0.26,rough:0.3}); sc.position.z=0.13;
  const notch = box(0.9,0.16,0.1,P.ink,{r:0.05}); notch.position.set(0,2.1,0.2);
  p.add(body,sc,notch);
  p.position.set(x,y,z); p.rotation.set(-0.03,ry,0); p.scale.setScalar(scale);
  return p;
}
g.add(phone(-3.3,2.7,-0.6,0.42,0.86,P.blue));
g.add(phone(0,3.0,0.9,0.0,1.0,P.violet));
g.add(phone(3.3,2.7,-0.6,-0.42,0.86,P.purple));

// floating UI chips around the middle phone
const chips=[[-1.9,5.3,2.0,P.cream,1.5],[2.0,5.0,2.1,P.amber,1.2],[2.3,1.4,2.3,P.cream,1.3],[-2.2,1.1,2.2,P.blueLt,1.0]];
chips.forEach(([x,y,z,c,w])=>{ const ch=box(w,0.5,0.14,c,{r:0.2});
  ch.position.set(x,y,z); ch.rotation.set(0.06,x>0?-0.3:0.3,0); g.add(ch); });

// install badge
const badge = cyl(0.62,0.62,0.16,P.amber,40); badge.rotation.x=Math.PI/2;
badge.position.set(3.6,5.3,1.6); g.add(badge);

g.position.y=-1.6;
finish(S);
"""

SCENES["seo"] = """
const S = makeStage({bg1:__BG1__, bg2:__BG2__, w:W, h:H});
const g = S.root;

// search field slab
const field = box(6.4,1.1,0.4,P.cream,{r:0.5});
field.position.set(-0.2,3.9,0.6); field.rotation.set(-0.04,0.1,0); g.add(field);
const pill = box(3.4,0.34,0.12,P.blueLt,{r:0.17}); pill.position.set(-1.1,3.9,0.85); pill.rotation.y=0.1; g.add(pill);

// magnifier
const glass = torus(0.95,0.16,P.amber); glass.position.set(3.3,3.9,1.3); glass.rotation.set(0.1,0.1,0);
g.add(glass);
const lens = cyl(0.82,0.82,0.08,P.blueLt,36,{extra:{transparent:true,opacity:0.55}});
lens.rotation.x=Math.PI/2; lens.position.set(3.3,3.9,1.3); g.add(lens);
const grip = cyl(0.12,0.12,1.2,P.coral,20); grip.position.set(4.2,3.05,1.3); grip.rotation.z=-0.75; g.add(grip);

// ranking podium — position 1 tallest
const hs=[2.8,2.0,1.4];
hs.forEach((h,i)=>{
  const c = i===0?P.amber:(i===1?P.violet:P.slate);
  const b = box(1.7,h,1.5,c,{r:0.12});
  b.position.set(-2.4+i*2.0, h/2, 1.2); g.add(b);
  const num = box(0.7,0.7,0.1,P.cream,{r:0.1}); num.position.set(-2.4+i*2.0,h-0.55,2.0); g.add(num);
});

// result rows floating behind
[0,1,2].forEach(i=>{ const r=box(4.6,0.7,0.14,i?P.slate:P.cream,{r:0.12});
  r.position.set(1.6,1.5+i*0.95,-1.6); r.rotation.y=-0.3; g.add(r); });

g.position.y=-1.4;
finish(S);
"""

SCENES["social"] = """
const S = makeStage({bg1:__BG1__, bg2:__BG2__, w:W, h:H});
const g = S.root;

// phone at centre
const body = box(2.7,5.4,0.32,P.slate,{r:0.34,rough:0.55});
const sc = box(2.45,5.0,0.16,P.violet,{r:0.28,rough:0.3}); sc.position.z=0.14;
const ph = new THREE.Group(); ph.add(body,sc);
ph.position.set(-0.2,3.0,0.6); ph.rotation.set(-0.04,0.22,0); g.add(ph);

// post cards fanning out
const cards=[[-3.6,4.6,1.2,P.coral,0.42],[-4.0,2.0,1.6,P.cream,0.3],[3.3,4.9,1.0,P.amber,-0.4],[3.7,2.3,1.5,P.blueLt,-0.28]];
cards.forEach(([x,y,z,c,ry])=>{ const cd=box(2.1,2.1,0.16,c,{r:0.16});
  cd.position.set(x,y,z); cd.rotation.set(0.05,ry,0); g.add(cd); });

// engagement bubbles
const hearts=[[-1.9,6.3,2.2,0.34,P.coral],[1.5,6.6,2.0,0.28,P.amber],[2.6,5.7,2.4,0.22,P.purple],[-2.7,5.6,2.3,0.2,P.blueLt]];
hearts.forEach(([x,y,z,r,c])=>{ const s=ball(r,c); s.position.set(x,y,z); g.add(s); });

// speech bubble slab
const bub = box(2.4,1.3,0.2,P.cream,{r:0.35}); bub.position.set(0.2,6.6,1.6); bub.rotation.z=0.05; g.add(bub);

g.position.y=-1.9;
finish(S);
"""


def serve(directory):
    handler = lambda *a, **k: http.server.SimpleHTTPRequestHandler(*a, directory=directory, **k)
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), handler)
    httpd.allow_reuse_address = True
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


def main():
    if not os.path.exists(CHROME):
        raise SystemExit("Google Chrome not found — needed to render the scenes.")
    wanted = sys.argv[1:] or list(SCENES)
    os.makedirs(OUT, exist_ok=True)

    tmp = tempfile.mkdtemp()
    shutil.copy(os.path.join(ROOT, "build", "scene3d.js"), os.path.join(tmp, "scene3d.js"))
    httpd = serve(tmp)                     # modules need http, not file://

    try:
        for name in wanted:
            body = SCENES[name].replace("__BG1__", BG1).replace("__BG2__", BG2)
            with open(os.path.join(tmp, name + ".html"), "w", encoding="utf-8") as f:
                f.write(PAGE % {"map": IMPORTMAP, "W": W, "H": H, "body": body})
            dest = os.path.join(OUT, name + ".png")
            subprocess.run([
                CHROME, "--headless", "--disable-gpu", "--use-gl=swiftshader",
                "--enable-unsafe-swiftshader", "--hide-scrollbars",
                f"--window-size={W},{H}", "--virtual-time-budget=90000",
                f"--screenshot={dest}", f"http://127.0.0.1:{PORT}/{name}.html",
            ], capture_output=True, timeout=300)
            size = os.path.getsize(dest) if os.path.exists(dest) else 0
            print(f"  assets/work/{name}.png  ({size // 1024} KB)")
    finally:
        httpd.shutdown()
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
