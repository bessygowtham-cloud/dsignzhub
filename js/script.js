// Mobile menu toggle
const menuToggle = document.getElementById('menuToggle');
const mobileMenu = document.getElementById('mobileMenu');

if (menuToggle && mobileMenu) {
  menuToggle.addEventListener('click', () => {
    const isOpen = mobileMenu.classList.toggle('open');
    menuToggle.setAttribute('aria-expanded', String(isOpen));
    document.body.style.overflow = isOpen ? 'hidden' : '';
  });

  mobileMenu.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      mobileMenu.classList.remove('open');
      menuToggle.setAttribute('aria-expanded', 'false');
      document.body.style.overflow = '';
    });
  });
}

// Header shadow on scroll
const header = document.getElementById('siteHeader');
window.addEventListener('scroll', () => {
  if (header) header.style.boxShadow = window.scrollY > 10 ? '0 8px 24px -12px rgba(0,0,0,0.6)' : 'none';
});

// Scroll reveal
const revealEls = document.querySelectorAll('.reveal');
if ('IntersectionObserver' in window) {
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
  revealEls.forEach((el) => io.observe(el));
} else {
  revealEls.forEach((el) => el.classList.add('is-visible'));
}

// Footer year
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

// Contact form (no backend yet — hands off to the visitor's mail client)
const contactForm = document.getElementById('contactForm');
const formNote = document.getElementById('formNote');

if (contactForm) {
  contactForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const name = document.getElementById('name').value.trim();
    const email = document.getElementById('email').value.trim();
    const message = document.getElementById('message').value.trim();

    const subject = encodeURIComponent(`Project inquiry from ${name}`);
    const body = encodeURIComponent(`${message}\n\nFrom: ${name} (${email})`);
    window.location.href = `mailto:hello@dsignzhub.com?subject=${subject}&body=${body}`;

    if (formNote) formNote.textContent = 'Opening your email app to send this message…';
  });
}

/* ---------------- Pointer-driven motion ----------------
   Everything below is desktop-mouse only. Touch devices and anyone who asked
   for reduced motion keep the plain native experience. */
const finePointer = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (finePointer && !reducedMotion) {
  const dot = document.createElement('div');
  dot.className = 'cursor-dot';
  const ring = document.createElement('div');
  ring.className = 'cursor-ring';
  const label = document.createElement('span');
  label.className = 'cursor-label';
  ring.appendChild(label);
  document.body.append(dot, ring);

  // Target = true pointer position. Ring eases toward it for the trailing feel.
  let targetX = window.innerWidth / 2;
  let targetY = window.innerHeight / 2;
  let ringX = targetX;
  let ringY = targetY;
  let started = false;

  window.addEventListener('pointermove', (e) => {
    targetX = e.clientX;
    targetY = e.clientY;
    if (!started) {
      started = true;
      ringX = targetX;
      ringY = targetY;
      document.documentElement.classList.add('cursor-active');
    }
  }, { passive: true });

  document.addEventListener('pointerleave', () => document.documentElement.classList.remove('cursor-active'));
  document.addEventListener('pointerenter', () => document.documentElement.classList.add('cursor-active'));

  const magnets = [];

  const tick = () => {
    // Dot is pinned to the pointer; ring lerps 18% of the remaining gap per frame.
    dot.style.transform = `translate(${targetX}px, ${targetY}px)`;
    ringX += (targetX - ringX) * 0.18;
    ringY += (targetY - ringY) * 0.18;
    ring.style.transform = `translate(${ringX}px, ${ringY}px)`;

    // Magnetic pull: buttons drift toward the cursor while it's near them.
    magnets.forEach((m) => {
      const r = m.el.getBoundingClientRect();
      const cx = r.left + r.width / 2;
      const cy = r.top + r.height / 2;
      const dx = targetX - cx;
      const dy = targetY - cy;
      const dist = Math.hypot(dx, dy);
      const range = Math.max(r.width, r.height) * 0.9 + 40;

      const pull = dist < range ? (1 - dist / range) * 0.34 : 0;
      m.x += (dx * pull - m.x) * 0.16;
      m.y += (dy * pull - m.y) * 0.16;

      m.el.style.transform = Math.abs(m.x) < 0.1 && Math.abs(m.y) < 0.1
        ? ''
        : `translate(${m.x.toFixed(2)}px, ${m.y.toFixed(2)}px)`;
    });

    requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);

  // Register magnetic elements
  document.querySelectorAll('.btn, .menu-toggle').forEach((el) => {
    el.classList.add('magnetic');
    magnets.push({ el, x: 0, y: 0 });
  });

  // Cursor state changes over interactive things
  const setRing = (state, text) => {
    ring.classList.toggle('is-link', state === 'link');
    ring.classList.toggle('is-label', state === 'label');
    dot.classList.toggle('is-link', state !== null);
    if (text) label.textContent = text;
  };

  document.querySelectorAll('a, button').forEach((el) => {
    el.addEventListener('pointerenter', () => setRing('link'));
    el.addEventListener('pointerleave', () => setRing(null));
  });

  document.querySelectorAll('.service-card').forEach((card) => {
    card.addEventListener('pointerenter', () => setRing('label', 'Explore'));
    card.addEventListener('pointerleave', () => setRing(null));
    card.addEventListener('pointermove', (e) => {
      const r = card.getBoundingClientRect();
      card.style.setProperty('--cx', `${e.clientX - r.left}px`);
      card.style.setProperty('--cy', `${e.clientY - r.top}px`);
    }, { passive: true });
  });

  // Hero ambient spotlight
  const hero = document.querySelector('.hero');
  if (hero) {
    hero.addEventListener('pointermove', (e) => {
      const r = hero.getBoundingClientRect();
      hero.style.setProperty('--mx', `${e.clientX - r.left}px`);
      hero.style.setProperty('--my', `${e.clientY - r.top}px`);
    }, { passive: true });
  }

  // Parallax drift on the hero mark
  const orbit = document.querySelector('.orbit-card');
  if (orbit) {
    window.addEventListener('pointermove', (e) => {
      const nx = (e.clientX / window.innerWidth - 0.5) * 2;
      const ny = (e.clientY / window.innerHeight - 0.5) * 2;
      orbit.style.transform = `translate(${nx * 14}px, ${ny * 14}px)`;
    }, { passive: true });
  }
}
