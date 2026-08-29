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

// Contact form — delivers via Web3Forms when an access key is configured,
// falling back to the visitor's mail client (mailto:) if the key is missing
// or the request fails, so a submission is never silently lost.
const contactForm = document.getElementById('contactForm');
const formNote = document.getElementById('formNote');

function mailtoFallback(form) {
  const name = form.querySelector('#name').value.trim();
  const email = form.querySelector('#email').value.trim();
  const message = form.querySelector('#message').value.trim();
  const to = form.dataset.toEmail || 'hello@dsignzhub.com';

  const subject = encodeURIComponent(`Project inquiry from ${name}`);
  const body = encodeURIComponent(`${message}\n\nFrom: ${name} (${email})`);
  window.location.href = `mailto:${to}?subject=${subject}&body=${body}`;
  if (formNote) formNote.textContent = 'Opening your email app to send this message…';
}

if (contactForm) {
  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const submitBtn = contactForm.querySelector('button[type="submit"]');

    if (!contactForm.dataset.web3formsKey) {
      mailtoFallback(contactForm);
      return;
    }

    if (submitBtn) submitBtn.disabled = true;
    if (formNote) formNote.textContent = 'Sending…';

    try {
      const res = await fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { Accept: 'application/json' },
        body: new FormData(contactForm),
      });
      const result = await res.json();

      if (result.success) {
        if (formNote) formNote.textContent = "Thanks — we've received your message and will reply within one working day.";
        contactForm.reset();
      } else {
        mailtoFallback(contactForm);
      }
    } catch (err) {
      mailtoFallback(contactForm);
    } finally {
      if (submitBtn) submitBtn.disabled = false;
    }
  });
}

/* ---------------- Mobile services accordion ---------------- */
const mDropToggle = document.getElementById('mDropToggle');
const mDropList = document.getElementById('mDropList');
if (mDropToggle && mDropList) {
  mDropToggle.addEventListener('click', () => {
    const open = mDropList.classList.toggle('open');
    mDropToggle.setAttribute('aria-expanded', String(open));
  });
}

/* ---------------- Service hero spotlight ---------------- */
const svcHero = document.querySelector('.svc-hero');
if (svcHero && window.matchMedia('(hover: hover) and (pointer: fine)').matches
    && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
  svcHero.addEventListener('pointermove', (e) => {
    const r = svcHero.getBoundingClientRect();
    svcHero.style.setProperty('--mx', (e.clientX - r.left) + 'px');
    svcHero.style.setProperty('--my', (e.clientY - r.top) + 'px');
  }, { passive: true });
}

/* ---------------- Staggered reveals ----------------
   Cards inside a grid animate in sequence rather than all at once. */
document.querySelectorAll('.d-grid, .s-grid, .rel-grid, .b-grid, .services-grid').forEach((grid) => {
  Array.from(grid.children).forEach((child, i) => {
    if (child.classList.contains('reveal')) {
      child.classList.add('stagger-' + ((i % 4) + 1));
    }
  });
});
