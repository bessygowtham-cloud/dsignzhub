#!/usr/bin/env python3
"""Static site generator for dsignzhub.com.

Run from the repo root:  python3 build/build.py

Every page shares one header, footer and <head> block, so nav changes and SEO
tags stay consistent across all of them. Page copy lives in content.py.
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import SITE, SERVICES, PROCESS, SERVICE_BY_SLUG  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def asset_version(relpath):
    """Short content hash, appended to CSS/JS URLs.

    Without this, browsers keep serving a stale stylesheet after a deploy —
    the file name never changes, so nothing tells the cache to refetch.
    """
    full = os.path.join(ROOT, relpath)
    with open(full, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()[:8]


CSS_V = None
JS_V = None


def rel(depth):
    """Relative path back to site root from a page nested `depth` folders deep."""
    return "../" * depth or "./"


def esc(text):
    return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace('"', "&quot;"))


LOGO = """<svg class="brand-icon" viewBox="0 0 100 100" fill="none" aria-hidden="true">
<path fill="currentColor" fill-rule="evenodd" d="M26 14H48A36 36 0 0 1 48 86H14V26Z M30 30H66V40L46 60H66V70H30V60L50 40H30Z"/></svg>"""


def head(title, meta, canonical_path, depth, jsonld=None, og_type="website"):
    r = rel(depth)
    url = f"{SITE['domain']}/{canonical_path}".rstrip("/") + ("/" if canonical_path else "")
    blocks = ""
    for block in (jsonld or []):
        blocks += f'\n<script type="application/ld+json">{json.dumps(block, ensure_ascii=False)}</script>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(meta)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(meta)}">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="{SITE['name']}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(meta)}">
<link rel="icon" type="image/svg+xml" href="{r}assets/logo-icon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}css/style.css?v={CSS_V}">{blocks}
</head>
<body>
<div class="noise"></div>
<a href="#main" class="skip-link">Skip to content</a>
"""


def header(depth, active=""):
    r = rel(depth)
    active_attr = ' class="is-active"'

    def cls(name):
        return active_attr if active == name else ""

    items = "".join(
        '<li><a href="{r}services/{slug}/"{a}><span>{nav}</span></a></li>'.format(
            r=r, slug=s["slug"], a=cls(s["slug"]), nav=esc(s["nav"]))
        for s in SERVICES
    )
    return f"""<header class="site-header" id="siteHeader">
  <div class="container header-inner">
    <a href="{r}" class="brand" aria-label="{SITE['name']} home">
      {LOGO}
      <span class="brand-word">Dsignzhub</span>
    </a>

    <nav class="nav-desktop" aria-label="Primary">
      <div class="has-drop">
        <a href="{r}services/"{cls('services')} aria-haspopup="true" aria-expanded="false">Services
          <svg viewBox="0 0 12 8" class="caret" aria-hidden="true"><path d="M1 1.5 6 6.5 11 1.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
        </a>
        <div class="drop">
          <ul>{items}</ul>
        </div>
      </div>
      <a href="{r}about/"{cls('about')}>About</a>
      <a href="{r}contact/"{cls('contact')}>Contact</a>
    </nav>

    <div class="header-actions">
      <a href="{r}contact/" class="btn btn-primary btn-sm">Get In Touch</a>
      <button class="menu-toggle" id="menuToggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>

<div class="mobile-menu" id="mobileMenu">
  <nav aria-label="Mobile primary">
    <a href="{r}">Home</a>
    <button class="m-drop-toggle" id="mDropToggle" aria-expanded="false" aria-controls="mDropList">
      Services
      <svg viewBox="0 0 12 8" aria-hidden="true"><path d="M1 1.5 6 6.5 11 1.5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>
    </button>
    <ul class="m-drop" id="mDropList">{items}</ul>
    <a href="{r}about/">About</a>
    <a href="{r}contact/">Contact</a>
  </nav>
  <div class="mobile-menu-footer">
    <a href="{r}contact/" class="btn btn-primary">Start a Project</a>
    <p>{SITE['email']}</p>
  </div>
</div>
<main id="main">
"""


def footer(depth):
    r = rel(depth)
    svc_links = "".join(
        f'<a href="{r}services/{s["slug"]}/">{esc(s["nav"])}</a>' for s in SERVICES[:5]
    )
    return f"""</main>
<footer class="site-footer">
  <div class="container footer-inner">
    <div class="footer-brand">
      <a href="{r}" class="brand">{LOGO}<span class="brand-word">Dsignzhub</span></a>
      <p>{SITE['tagline']}</p>
    </div>
    <div class="footer-col">
      <h4>Services</h4>
      {svc_links}
      <a href="{r}services/">All services</a>
    </div>
    <div class="footer-col">
      <h4>Company</h4>
      <a href="{r}about/">About</a>
      <a href="{r}contact/">Contact</a>
    </div>
    <div class="footer-col">
      <h4>Connect</h4>
      <a href="mailto:{SITE['email']}">{SITE['email']}</a>
      <a href="tel:{SITE['phone_href']}">{SITE['phone_display']}</a>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>&copy; <span id="year"></span> {SITE['name']}. All rights reserved.</p>
    <p>Made in India</p>
  </div>
</footer>
<script src="{r}js/script.js?v={JS_V}"></script>
</body>
</html>
"""


def cta(depth, heading, sub):
    r = rel(depth)
    return f"""<section class="cta-band">
  <div class="container">
    <div class="cta-inner reveal">
      <h2>{esc(heading)}</h2>
      <p>{esc(sub)}</p>
      <div class="cta-actions">
        <a href="{r}contact/" class="btn btn-primary">Start a Project</a>
        <a href="mailto:{SITE['email']}" class="btn btn-ghost">{SITE['email']}</a>
      </div>
    </div>
  </div>
</section>
"""


def breadcrumb(depth, trail):
    """trail: list of (label, href-or-None). Renders markup + JSON-LD."""
    r = rel(depth)
    parts = [f'<a href="{r}">Home</a>']
    for label, href in trail:
        if href:
            parts.append(f'<a href="{r}{href}">{esc(label)}</a>')
        else:
            parts.append(f'<span aria-current="page">{esc(label)}</span>')
    return ('<nav class="crumbs" aria-label="Breadcrumb"><div class="container">'
            + '<span class="sep">/</span>'.join(parts) + '</div></nav>')


def crumb_jsonld(trail_abs):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": f"{SITE['domain']}/{path}".rstrip("/") + ("/" if path else "")}
            for i, (name, path) in enumerate(trail_abs)
        ],
    }


def faq_block(faqs):
    items = ""
    for i, (q, a) in enumerate(faqs):
        items += f"""
      <div class="faq-item reveal">
        <button class="faq-q" aria-expanded="false" aria-controls="faq-a-{i}" id="faq-q-{i}">
          <span>{esc(q)}</span>
          <svg viewBox="0 0 14 14" aria-hidden="true"><path d="M7 1v12M1 7h12" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>
        </button>
        <div class="faq-a" id="faq-a-{i}" role="region" aria-labelledby="faq-q-{i}"><p>{esc(a)}</p></div>
      </div>"""
    return items


def faq_jsonld(faqs):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in faqs
        ],
    }


# --------------------------------------------------------------------------
# pages
# --------------------------------------------------------------------------
def service_page(svc):
    depth = 2
    r = rel(depth)
    path = f"services/{svc['slug']}"

    service_ld = {
        "@context": "https://schema.org",
        "@type": "Service",
        "name": svc["h1"],
        "serviceType": svc["keyword"],
        "description": svc["meta"],
        "provider": {"@type": "Organization", "name": SITE["name"], "url": SITE["domain"] + "/"},
        "areaServed": {"@type": "Country", "name": "India"},
        "url": f"{SITE['domain']}/{path}/",
    }
    lds = [service_ld, faq_jsonld(svc["faqs"]),
           crumb_jsonld([("Home", ""), ("Services", "services"), (svc["nav"], path)])]

    intro = "".join(f"<p>{esc(p)}</p>" for p in svc["intro"])

    deliverables = "".join(f"""
        <article class="d-card reveal">
          <h3>{esc(t)}</h3>
          <p>{esc(d)}</p>
        </article>""" for t, d in svc["deliverables"])

    benefits = "".join(f"""
        <div class="b-item reveal">
          <h3>{esc(t)}</h3>
          <p>{esc(d)}</p>
        </div>""" for t, d in svc["benefits"])

    steps = "".join(f"""
        <div class="step reveal">
          <span class="step-num">{i+1:02d}</span>
          <h3>{esc(t)}</h3>
          <p>{esc(d)}</p>
        </div>""" for i, (t, d) in enumerate(PROCESS))

    related = "".join(f"""
        <a class="rel-card reveal" href="{r}services/{SERVICE_BY_SLUG[s]['slug']}/">
          <h3>{esc(SERVICE_BY_SLUG[s]['nav'])}</h3>
          <span class="rel-go">Explore <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
        </a>""" for s in svc["related"])

    return head(svc["title"], svc["meta"], path + "/", depth, lds) + header(depth, svc["slug"]) + f"""
{breadcrumb(depth, [("Services", "services/"), (svc["nav"], None)])}

<section class="svc-hero">
  <div class="container">
    <p class="eyebrow reveal">{esc(svc['eyebrow'])}</p>
    <h1 class="svc-h1 reveal">{esc(svc['h1'])}</h1>
    <p class="svc-lede reveal">{esc(svc['lede'])}</p>
    <div class="hero-cta reveal">
      <a href="{r}contact/" class="btn btn-primary">Get a Free Quote</a>
      <a href="#what" class="btn btn-ghost">What's Included</a>
    </div>
  </div>
</section>

<section class="svc-intro container">
  <div class="prose reveal">{intro}</div>
</section>

<section class="svc-section container" id="what">
  <p class="section-label reveal">What's included</p>
  <h2 class="section-title reveal">Everything you get</h2>
  <div class="d-grid">{deliverables}</div>
</section>

<section class="svc-benefits">
  <div class="container">
    <p class="section-label reveal">Why it matters</p>
    <h2 class="section-title reveal">What this actually changes</h2>
    <div class="b-grid">{benefits}</div>
  </div>
</section>

<section class="svc-section container">
  <p class="section-label reveal">How we work</p>
  <h2 class="section-title reveal">A process without surprises</h2>
  <div class="approach-steps">{steps}</div>
</section>

<section class="svc-section container">
  <p class="section-label reveal">Questions</p>
  <h2 class="section-title reveal">Frequently asked</h2>
  <div class="faq">{faq_block(svc['faqs'])}</div>
</section>

<section class="svc-section container">
  <p class="section-label reveal">Keep exploring</p>
  <h2 class="section-title reveal">Related services</h2>
  <div class="rel-grid">{related}</div>
</section>

{cta(depth, "Ready to get started?", "Tell us about your project and we'll come back with a clear scope, timeline and fixed quote.")}
""" + footer(depth)


def services_index():
    depth = 1
    r = rel(depth)
    cards = "".join(f"""
      <a class="s-card reveal" href="{r}services/{s['slug']}/">
        <h2>{esc(s['nav'])}</h2>
        <p>{esc(s['lede'][:135].rsplit(' ', 1)[0])}…</p>
        <span class="rel-go">Explore <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      </a>""" for s in SERVICES)

    title = "Our Services | Web, E-commerce, SEO & Branding | Dsignzhub"
    meta = ("End-to-end digital services for Indian businesses — website design and development, "
            "PWAs, e-commerce, digital marketing, SEO, Google Ads, graphic design and branding.")
    lds = [crumb_jsonld([("Home", ""), ("Services", "services")])]

    return head(title, meta, "services/", depth, lds) + header(depth, "services") + f"""
{breadcrumb(depth, [("Services", None)])}

<section class="svc-hero">
  <div class="container">
    <p class="eyebrow reveal">What we do</p>
    <h1 class="svc-h1 reveal">Our Services</h1>
    <p class="svc-lede reveal">Nine services, one team. Everything needed to build a digital presence that gets your business found, chosen and remembered — design, development and marketing under one roof.</p>
  </div>
</section>

<section class="svc-section container">
  <div class="s-grid">{cards}</div>
</section>

{cta(depth, "Not sure which you need?", "Tell us the problem and we'll tell you honestly what will move the needle — and what won't.")}
""" + footer(depth)


def home():
    depth = 0
    r = rel(depth)
    cards = "".join(f"""
      <a class="service-card reveal" href="{r}services/{s['slug']}/">
        <h3>{esc(s['nav'])}</h3>
        <p>{esc(s['lede'][:105].rsplit(' ', 1)[0])}…</p>
        <span class="rel-go">Explore <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      </a>""" for s in SERVICES)

    steps = "".join(f"""
        <div class="step reveal">
          <span class="step-num">{i+1:02d}</span>
          <h3>{esc(t)}</h3>
          <p>{esc(d)}</p>
        </div>""" for i, (t, d) in enumerate(PROCESS))

    marquee_items = "".join(f"<span>{esc(s['nav'])}</span><span aria-hidden='true'>•</span>" for s in SERVICES)

    org_ld = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE["name"],
        "url": SITE["domain"] + "/",
        "email": SITE["email"],
        "description": SITE["tagline"],
        "areaServed": {"@type": "Country", "name": "India"},
    }
    site_ld = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE["name"],
        "url": SITE["domain"] + "/",
    }

    title = "Web Design, Development, SEO & Marketing in India | Dsignzhub"
    meta = ("Dsignzhub builds websites, online stores and marketing that grow Indian businesses. "
            "Website design and development, PWAs, e-commerce, SEO, Google Ads and branding.")

    return head(title, meta, "", depth, [org_ld, site_ld]) + header(depth, "home") + f"""
<section class="hero">
  <div class="container hero-inner">
    <p class="eyebrow reveal">Digital solutions for Indian businesses</p>
    <h1 class="hero-title reveal">WE BUILD DIGITAL<br>PRESENCE THAT <span class="text-gradient">GROWS</span><br>YOUR BUSINESS</h1>
    <p class="hero-sub reveal">Website &amp; app development, e-commerce, SEO, Google Ads and branding — combined into one digital system that gets Indian businesses found, chosen and remembered.</p>
    <div class="hero-cta reveal">
      <a href="{r}contact/" class="btn btn-primary">Start a Project</a>
      <a href="{r}services/" class="btn btn-ghost">Explore Services</a>
    </div>
  </div>

  <div class="hero-visual" aria-hidden="true">
    <div class="orbit-card">
      <svg class="orbit-ring" viewBox="0 0 200 200" fill="none">
        <circle cx="100" cy="100" r="94" stroke="rgba(255,255,255,0.14)" stroke-width="1" stroke-dasharray="3 9"/>
        <circle cx="100" cy="100" r="68" stroke="rgba(139,123,255,0.28)" stroke-width="1"/>
      </svg>
      <img src="{r}assets/logo-icon.svg" alt="" class="orbit-mark">
      <span class="orbit-node n1">Web</span>
      <span class="orbit-node n2">SEO</span>
      <span class="orbit-node n3">Ads</span>
      <span class="orbit-node n4">Brand</span>
      <span class="orbit-node n5">Shop</span>
      <span class="orbit-node n6">Social</span>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true">
  <div class="marquee-track">{marquee_items}{marquee_items}</div>
</div>

<section class="about container">
  <div class="about-grid">
    <p class="section-label reveal">Who we are</p>
    <div class="about-content">
      <h2 class="about-statement reveal">End-to-end digital solutions for businesses that want to be found, chosen and remembered online.</h2>
      <p class="about-text reveal">We combine creative design, strategic thinking and data-driven marketing to help Indian businesses build a powerful and lasting online presence — from engaging websites and high-performing online stores to stronger search visibility, qualified leads and memorable brands.</p>
    </div>
  </div>
</section>

<section class="services container" id="services">
  <p class="section-label reveal">What we do</p>
  <h2 class="section-title reveal">Our Services</h2>
  <div class="services-grid">{cards}</div>
</section>

<section class="svc-section container">
  <p class="section-label reveal">How we work</p>
  <h2 class="section-title reveal">Our Approach</h2>
  <div class="approach-steps">{steps}</div>
</section>

{cta(depth, "Let's build something great for your business.", "Tell us a bit about your project and we'll get back to you shortly.")}
""" + footer(depth)


def about():
    depth = 1
    title = "About Dsignzhub | Digital Agency for Indian Businesses"
    meta = ("Dsignzhub is a digital agency combining design, development and marketing to help "
            "Indian businesses build a lasting online presence.")
    lds = [crumb_jsonld([("Home", ""), ("About", "about")])]
    steps = "".join(f"""
        <div class="step reveal">
          <span class="step-num">{i+1:02d}</span>
          <h3>{esc(t)}</h3>
          <p>{esc(d)}</p>
        </div>""" for i, (t, d) in enumerate(PROCESS))

    return head(title, meta, "about/", depth, lds) + header(depth, "about") + f"""
{breadcrumb(depth, [("About", None)])}

<section class="svc-hero">
  <div class="container">
    <p class="eyebrow reveal">Who we are</p>
    <h1 class="svc-h1 reveal">One team, every discipline</h1>
    <p class="svc-lede reveal">We are a digital agency built around a simple idea: design, development and marketing work better when the same team does all three.</p>
  </div>
</section>

<section class="svc-intro container">
  <div class="prose reveal">
    <p>Most businesses end up with a designer who does not talk to the developer, and a marketing agency that inherits a website neither of them built. Things get lost in those gaps — usually speed, consistency, and the tracking that would have told you what was working.</p>
    <p>We keep it under one roof. The people designing your brand are the people building your site and running your campaigns, so the message stays consistent from the logo through to the ad copy.</p>
    <p>We work with businesses across India, from first websites to full rebrands and ongoing marketing. What we care about is whether the work produced something measurable — enquiries, orders, rankings — not whether it merely looked good in a presentation.</p>
  </div>
</section>

<section class="svc-benefits">
  <div class="container">
    <p class="section-label reveal">How we think</p>
    <h2 class="section-title reveal">What you can expect</h2>
    <div class="b-grid">
      <div class="b-item reveal"><h3>Straight answers</h3><p>If something will not work, we say so before you spend money on it, not after.</p></div>
      <div class="b-item reveal"><h3>Fixed scope, fixed quote</h3><p>You know the cost and the timeline before we start. Changes get discussed, not invoiced quietly.</p></div>
      <div class="b-item reveal"><h3>You own everything</h3><p>Code, domains, ad accounts and source files are all yours, including if you decide to leave.</p></div>
      <div class="b-item reveal"><h3>Measured, not guessed</h3><p>Tracking is set up properly, so decisions come from data rather than opinion.</p></div>
    </div>
  </div>
</section>

<section class="svc-section container">
  <p class="section-label reveal">How we work</p>
  <h2 class="section-title reveal">Our Approach</h2>
  <div class="approach-steps">{steps}</div>
</section>

{cta(depth, "Let's talk about your project.", "No pressure and no obligation — just a straight conversation about what you need.")}
""" + footer(depth)


def contact():
    depth = 1
    title = "Contact Dsignzhub | Get a Free Quote"
    meta = ("Get in touch with Dsignzhub for website design and development, SEO, Google Ads, "
            "e-commerce and branding. Tell us about your project and get a free quote.")
    lds = [crumb_jsonld([("Home", ""), ("Contact", "contact")]), {
        "@context": "https://schema.org",
        "@type": "ContactPage",
        "url": f"{SITE['domain']}/contact/",
    }]
    return head(title, meta, "contact/", depth, lds) + header(depth, "contact") + f"""
{breadcrumb(depth, [("Contact", None)])}

<section class="svc-hero">
  <div class="container">
    <p class="eyebrow reveal">Get started</p>
    <h1 class="svc-h1 reveal">Tell us about your project</h1>
    <p class="svc-lede reveal">Send us a few details and we'll come back with a clear scope, a timeline and a fixed quote — usually within one working day.</p>
  </div>
</section>

<section class="contact container">
  <div class="contact-panel">
    <form class="contact-form reveal" id="contactForm">
      <div class="form-row">
        <div class="field"><label for="name">Full Name*</label><input type="text" id="name" name="name" required></div>
        <div class="field"><label for="email">Email*</label><input type="email" id="email" name="email" required></div>
      </div>
      <div class="form-row">
        <div class="field"><label for="phone">Phone / WhatsApp</label><input type="tel" id="phone" name="phone"></div>
        <div class="field"><label for="company">Company</label><input type="text" id="company" name="company"></div>
      </div>
      <div class="field">
        <label for="service">What do you need?</label>
        <select id="service" name="service">
          <option value="">Select a service</option>
          {"".join(f'<option value="{esc(s["nav"])}">{esc(s["nav"])}</option>' for s in SERVICES)}
          <option value="Not sure yet">Not sure yet</option>
        </select>
      </div>
      <div class="field"><label for="message">About your project</label><textarea id="message" name="message" rows="5"></textarea></div>
      <button type="submit" class="btn btn-primary">Send Message</button>
      <p class="form-note" id="formNote"></p>
    </form>

    <div class="contact-direct reveal">
      <a href="mailto:{SITE['email']}">{SITE['email']}</a>
      <span class="dot">•</span>
      <a href="tel:{SITE['phone_href']}">{SITE['phone_display']}</a>
    </div>
  </div>
</section>
""" + footer(depth)


# --------------------------------------------------------------------------
# write
# --------------------------------------------------------------------------
def write(path, html):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def main():
    global CSS_V, JS_V
    CSS_V = asset_version("css/style.css")
    JS_V = asset_version("js/script.js")
    print(f"asset versions: css={CSS_V} js={JS_V}")

    written = []
    written.append(write("index.html", home()))
    written.append(write("services/index.html", services_index()))
    written.append(write("about/index.html", about()))
    written.append(write("contact/index.html", contact()))
    for svc in SERVICES:
        written.append(write(f"services/{svc['slug']}/index.html", service_page(svc)))

    # sitemap + robots
    urls = [""] + ["services/", "about/", "contact/"] + [f"services/{s['slug']}/" for s in SERVICES]
    body = "".join(
        f"\n  <url><loc>{SITE['domain']}/{u}</loc><priority>{'1.0' if u == '' else '0.8'}</priority></url>"
        for u in urls
    )
    write("sitemap.xml",
          f'<?xml version="1.0" encoding="UTF-8"?>\n'
          f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{body}\n</urlset>\n')
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE['domain']}/sitemap.xml\n")

    print(f"Generated {len(written)} pages + sitemap.xml + robots.txt")
    for p in written:
        print("  ", p)


if __name__ == "__main__":
    main()
