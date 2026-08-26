/* Shared 3D "clay render" stage used to bake the project showcase images.
 *
 * Matte materials, soft studio key light, contact shadows and a warm-to-cool
 * gradient backdrop — the modern product-render look, built from primitives so
 * nothing depends on downloaded models or photography.
 *
 * The page renders one scene, then sets document.title = 'READY' so the
 * screenshot step knows the frame is complete.
 */
import * as THREE from 'three';
import { RoundedBoxGeometry } from 'three/addons/geometries/RoundedBoxGeometry.js';

export const P = {
  blue: 0x2d69fb, blueLt: 0x7aa2ff,
  purple: 0xd278fe, violet: 0x8b74ff,
  cream: 0xf2eee8, sand: 0xe8dcc8,
  amber: 0xffb020, coral: 0xff8a65,
  ink: 0x1a1b2e, slate: 0x39405e,
};

export function clay(color, opts = {}) {
  return new THREE.MeshStandardMaterial({
    color, roughness: opts.rough ?? 0.82, metalness: opts.metal ?? 0.0,
    ...opts.extra,
  });
}

export function box(w, h, d, color, opts = {}) {
  const g = new RoundedBoxGeometry(w, h, d, 4, opts.r ?? Math.min(w, h, d) * 0.12);
  const m = new THREE.Mesh(g, clay(color, opts));
  m.castShadow = true; m.receiveShadow = true;
  return m;
}

export function cyl(rt, rb, h, color, seg = 40, opts = {}) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(rt, rb, h, seg), clay(color, opts));
  m.castShadow = true; m.receiveShadow = true;
  return m;
}

export function ball(r, color, opts = {}) {
  const m = new THREE.Mesh(new THREE.SphereGeometry(r, 40, 28), clay(color, opts));
  m.castShadow = true; m.receiveShadow = true;
  return m;
}

export function torus(r, tube, color, opts = {}) {
  const m = new THREE.Mesh(new THREE.TorusGeometry(r, tube, 18, 60), clay(color, opts));
  m.castShadow = true; m.receiveShadow = true;
  return m;
}

/** Thin panel with a coloured "screen" inset — used for devices and cards. */
export function panel(w, h, bodyColor, screenColor, depth = 0.16) {
  const g = new THREE.Group();
  const body = box(w, h, depth, bodyColor, { r: 0.09, rough: 0.7 });
  const screen = box(w * 0.9, h * 0.86, depth * 0.5, screenColor, { r: 0.05, rough: 0.35 });
  screen.position.z = depth * 0.55;
  g.add(body, screen);
  return g;
}

export function makeStage({ bg1, bg2, w, h }) {
  const renderer = new THREE.WebGLRenderer({ antialias: true });
  renderer.setSize(w, h, false);
  renderer.setPixelRatio(1);
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFSoftShadowMap;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  document.body.appendChild(renderer.domElement);

  const scene = new THREE.Scene();

  // gradient backdrop as a big sphere painted from a canvas
  const c = document.createElement('canvas');
  c.width = 8; c.height = 256;
  const g2 = c.getContext('2d');
  const grad = g2.createLinearGradient(0, 0, 0, 256);
  grad.addColorStop(0, bg1);
  grad.addColorStop(1, bg2);
  g2.fillStyle = grad; g2.fillRect(0, 0, 8, 256);
  const tex = new THREE.CanvasTexture(c);
  tex.colorSpace = THREE.SRGBColorSpace;
  const sky = new THREE.Mesh(
    new THREE.SphereGeometry(60, 32, 24),
    new THREE.MeshBasicMaterial({ map: tex, side: THREE.BackSide }),
  );
  scene.add(sky);

  // gentle image-based light so matte surfaces don't go flat
  const pmrem = new THREE.PMREMGenerator(renderer);
  const envTex = new THREE.CanvasTexture((() => {
    const e = document.createElement('canvas');
    e.width = 32; e.height = 128;
    const eg = e.getContext('2d');
    const q = eg.createLinearGradient(0, 0, 0, 128);
    q.addColorStop(0, '#ffffff'); q.addColorStop(0.5, '#c9d4ff'); q.addColorStop(1, '#2a2f4a');
    eg.fillStyle = q; eg.fillRect(0, 0, 32, 128);
    return e;
  })());
  envTex.mapping = THREE.EquirectangularReflectionMapping;
  scene.environment = pmrem.fromEquirectangular(envTex).texture;
  pmrem.dispose(); envTex.dispose();

  const camera = new THREE.PerspectiveCamera(30, w / h, 0.1, 200);
  camera.position.set(0, 2.4, 15);
  camera.lookAt(0, 0.9, 0);

  // ---- lighting: broad key + cool fill + rim ----
  const key = new THREE.DirectionalLight(0xffffff, 3.1);
  key.position.set(-7, 11, 9);
  key.castShadow = true;
  key.shadow.mapSize.set(2048, 2048);
  key.shadow.camera.near = 1;
  key.shadow.camera.far = 45;
  const d = 12;
  Object.assign(key.shadow.camera, { left: -d, right: d, top: d, bottom: -d });
  key.shadow.bias = -0.0006;
  key.shadow.radius = 4;
  scene.add(key);

  scene.add(new THREE.HemisphereLight(0xdfe7ff, 0x2a2140, 1.15));
  const fill = new THREE.DirectionalLight(0x9fb6ff, 0.85);
  fill.position.set(8, 4, 6);
  scene.add(fill);
  const rim = new THREE.DirectionalLight(0xffd9a8, 1.0);
  rim.position.set(3, 5, -9);
  scene.add(rim);

  // ---- ground that only catches shadow ----
  const ground = new THREE.Mesh(
    new THREE.PlaneGeometry(80, 80),
    new THREE.ShadowMaterial({ opacity: 0.22 }),
  );
  ground.rotation.x = -Math.PI / 2;
  ground.position.y = -0.02;
  ground.receiveShadow = true;
  scene.add(ground);

  const root = new THREE.Group();
  scene.add(root);

  return { renderer, scene, camera, root };
}

export function finish({ renderer, scene, camera }) {
  renderer.render(scene, camera);
  // second pass so shadow maps are definitely resolved before capture
  requestAnimationFrame(() => {
    renderer.render(scene, camera);
    document.title = 'READY';
  });
}
