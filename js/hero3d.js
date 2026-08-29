/* Interactive 3D hero.
 *
 * The object is the Dsignzhub monogram itself — the same D outline with a Z
 * counter used everywhere else — extruded and lit, rather than a generic blob.
 * Everything degrades safely: no WebGL, a blocked CDN, or reduced-motion all
 * leave the static SVG mark visible and this module simply never starts.
 */
import * as THREE from 'three';

const canvas = document.getElementById('hero3d');
const stage = document.querySelector('.hero-3d');
if (canvas && stage) start();

function start() {
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({
      canvas, alpha: true, antialias: true, powerPreference: 'high-performance',
    });
  } catch (e) {
    return;                        // no WebGL — SVG fallback stays put
  }

  stage.classList.add('is-live');  // hides the fallback, reveals the canvas

  const scene = new THREE.Scene();

  // Studio-ish environment built from a gradient canvas. Physical materials need
  // something to reflect; without this the mark reads as a flat dark silhouette.
  scene.environment = (() => {
    const c = document.createElement('canvas');
    c.width = 64; c.height = 256;
    const g = c.getContext('2d');
    const grad = g.createLinearGradient(0, 0, 0, 256);
    grad.addColorStop(0.00, '#ffffff');
    grad.addColorStop(0.28, '#9fb4ff');
    grad.addColorStop(0.52, '#2d69fb');
    grad.addColorStop(0.74, '#d278fe');
    grad.addColorStop(1.00, '#05050a');
    g.fillStyle = grad; g.fillRect(0, 0, 64, 256);
    const tex = new THREE.CanvasTexture(c);
    tex.mapping = THREE.EquirectangularReflectionMapping;
    tex.colorSpace = THREE.SRGBColorSpace;
    const pmrem = new THREE.PMREMGenerator(renderer);
    const env = pmrem.fromEquirectangular(tex).texture;
    pmrem.dispose(); tex.dispose();
    return env;
  })();
  const camera = new THREE.PerspectiveCamera(38, 1, 0.1, 100);
  camera.position.set(0, 0, 7.4);

  renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.15;

  // ---------- the monogram ----------
  // Drawn in the SVG's 100x100 grid, recentred and y-flipped for 3D space.
  const shape = new THREE.Shape();
  shape.moveTo(-24, 36);
  shape.lineTo(-2, 36);
  shape.absarc(-2, 0, 36, Math.PI / 2, -Math.PI / 2, true);
  shape.lineTo(-36, -36);
  shape.lineTo(-36, 24);
  shape.closePath();

  const hole = new THREE.Path();
  [[-20, 20], [16, 20], [16, 10], [-4, -10], [16, -10],
   [16, -20], [-20, -20], [-20, -10], [0, 10], [-20, 10]]
    .forEach(([x, y], i) => (i ? hole.lineTo(x, y) : hole.moveTo(x, y)));
  hole.closePath();
  shape.holes.push(hole);

  const geo = new THREE.ExtrudeGeometry(shape, {
    depth: 16, bevelEnabled: true, bevelThickness: 2.4,
    bevelSize: 2, bevelSegments: 6, curveSegments: 48,
  });
  geo.center();
  geo.computeVertexNormals();

  const mat = new THREE.MeshPhysicalMaterial({
    color: 0xb9a8ff,
    metalness: 0.9,
    roughness: 0.12,
    envMapIntensity: 1.5,
    clearcoat: 1,
    clearcoatRoughness: 0.12,
    iridescence: 0.75,
    iridescenceIOR: 1.5,
    reflectivity: 0.7,
    emissive: 0x2a1a5e,
    emissiveIntensity: 0.35,
  });

  const mark = new THREE.Mesh(geo, mat);
  mark.scale.setScalar(0.036);

  const group = new THREE.Group();
  group.add(mark);
  scene.add(group);

  // ---------- soft lighting ----------
  scene.add(new THREE.AmbientLight(0x5a63a0, 1.5));
  scene.add(new THREE.HemisphereLight(0x6f8cff, 0x0a0a12, 0.85));

  const key = new THREE.PointLight(0x4d8dff, 260, 60);      // brand blue
  key.position.set(-5, 4, 6);
  const fill = new THREE.PointLight(0xd278fe, 200, 60);     // brand purple
  fill.position.set(5.5, -2.5, 4.5);
  const rim = new THREE.DirectionalLight(0xffffff, 2.6);   // edge definition
  rim.position.set(2, 6, -5);
  scene.add(key, fill, rim);

  // ---------- floating elements ----------
  // Spread is tightened in x/y and pushed behind the object (negative z, away
  // from camera) rather than spanning ±z through it — points that far off-axis
  // this close to the camera fell outside the frustum entirely and never
  // rendered, reading as dust stopping dead at an invisible box edge instead
  // of receding naturally into the background.
  const dust = new THREE.Points(
    (() => {
      const g = new THREE.BufferGeometry();
      const n = 420;
      const pos = new Float32Array(n * 3);
      for (let i = 0; i < n; i++) {
        pos[i * 3] = (Math.random() - 0.5) * 16;
        pos[i * 3 + 1] = (Math.random() - 0.5) * 10;
        pos[i * 3 + 2] = (Math.random() - 0.5) * 16 - 9;
      }
      g.setAttribute('position', new THREE.BufferAttribute(pos, 3));
      return g;
    })(),
    new THREE.PointsMaterial({
      size: 0.035, color: 0xbfc6ff, transparent: true,
      opacity: 0.75, depthWrite: false, blending: THREE.AdditiveBlending,
    }),
  );
  scene.add(dust);

  // Two thin orbit rings, tilted, for depth — drawn at their full, prominent
  // design radii and then scaled down (never up) per-container in resize(),
  // just enough to guarantee they stay inside that container's own frustum
  // at every rotation angle. A fixed radius forces a compromise between
  // "fits the narrowest phone" and "fills the desktop frame"; scaling
  // relative to each container's actual bounds gets both at once.
  const RING_OUTER_R = 3.7;
  const rings = new THREE.Group();
  [[2.9, 0x2d69fb, 0.38], [3.7, 0xd278fe, 0.26]].forEach(([r, c, o], i) => {
    const ring = new THREE.Mesh(
      new THREE.TorusGeometry(r, 0.008, 8, 180),
      new THREE.MeshBasicMaterial({ color: c, transparent: true, opacity: o }),
    );
    ring.rotation.x = Math.PI / 2.6 + i * 0.35;
    ring.rotation.y = i * 0.5;
    rings.add(ring);
  });
  scene.add(rings);

  // ---------- responsive sizing ----------
  let wide = false;
  function resize() {
    const r = stage.getBoundingClientRect();
    const w = Math.max(1, r.width);
    const h = Math.max(1, r.height);
    renderer.setSize(w, h, false);
    camera.aspect = w / h;

    // On desktop the copy occupies the left half, so push the object right and
    // pull the camera back a little to keep it clear of the text.
    wide = w > 900;
    group.position.x = wide ? 1.7 : 0;
    camera.position.z = wide ? 7.4 : 8.6;
    camera.updateProjectionMatrix();

    // Fit the orbit rings to this container: the frustum's half-height/width
    // at the object's depth (z=0), take whichever is tighter, and scale the
    // rings to fill ~88% of that — full-size design radius capped down only
    // on containers narrow/short enough to need it.
    const halfH = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)) * camera.position.z;
    const halfW = halfH * camera.aspect;
    const bound = Math.min(halfH, halfW);
    rings.scale.setScalar(Math.min(1, (bound * 0.88) / RING_OUTER_R));
  }
  resize();
  addEventListener('resize', resize, { passive: true });

  // ---------- interaction ----------
  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
  if (matchMedia('(hover: hover) and (pointer: fine)').matches) {
    addEventListener('pointermove', (e) => {
      pointer.tx = (e.clientX / innerWidth - 0.5) * 2;
      pointer.ty = (e.clientY / innerHeight - 0.5) * 2;
    }, { passive: true });
  }

  let scrollP = 0;                                  // 0 at top of hero, 1 past it
  function readScroll() {
    const r = stage.getBoundingClientRect();
    scrollP = Math.min(1, Math.max(0, -r.top / Math.max(1, r.height)));
  }
  readScroll();
  addEventListener('scroll', readScroll, { passive: true });

  // ---------- loop ----------
  let visible = true;
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; })
    .observe(stage);

  const clock = new THREE.Clock();
  let spin = -0.55;   // start angled so the extruded edge reads

  function frame() {
    requestAnimationFrame(frame);
    if (!visible || document.hidden) return;

    const dt = Math.min(clock.getDelta(), 0.05);
    const t = clock.elapsedTime;

    pointer.x += (pointer.tx - pointer.x) * 0.05;
    pointer.y += (pointer.ty - pointer.y) * 0.05;

    if (!reduced) spin += dt * 0.16;

    // pointer parallax + a slow idle turn, plus extra rotation as you scroll
    group.rotation.y = spin + pointer.x * 0.5 + scrollP * 1.1;
    group.rotation.x = pointer.y * 0.28 + Math.sin(t * 0.4) * 0.05;
    group.position.y = Math.sin(t * 0.6) * 0.12 - scrollP * 0.7;

    rings.rotation.z = -spin * 0.6;
    rings.rotation.x = Math.sin(t * 0.25) * 0.12;
    dust.rotation.y = spin * 0.25;

    // scroll-driven camera dolly + slight rise
    const baseZ = wide ? 7.4 : 8.6;
    camera.position.z = baseZ + scrollP * 2.2;
    camera.position.y = scrollP * 0.9;
    camera.lookAt(group.position.x * 0.5, 0, 0);

    renderer.render(scene, camera);
  }
  frame();
}
