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
from content import (SITE, SERVICES, PROCESS, SERVICE_BY_SLUG,  # noqa: E402
                     SHOWCASE, STATS, WHY_US, PILLARS, VOICES,
                     PRICING, SOCIALS)
from icons import sprite, icon  # noqa: E402

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
JS3_V = None


def asset_url(relpath, depth):
    """Asset URL with a content hash. Without this, replacing an image file
    changes nothing for anyone holding a cached copy — the name is identical."""
    try:
        return f"{rel(depth)}{relpath}?v={asset_version(relpath)}"
    except OSError:
        return f"{rel(depth)}{relpath}"


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
    sprite_markup = sprite()
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
<link rel="icon" type="image/svg+xml" href="{asset_url('assets/logo-icon.svg', depth)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;450;500;600&family=Inter:wght@400;450;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}css/style.css?v={CSS_V}">{blocks}
</head>
<body>
{sprite_markup}
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
  <div class="container">
    <div class="header-inner">
      <a href="{r}" class="brand" aria-label="{SITE['name']} home">
        {LOGO}
        <span class="brand-word">Dsignzhub</span>
      </a>

      <nav class="nav-desktop" aria-label="Primary">
        <div class="has-drop">
          <a href="{r}services/"{cls('services')} aria-haspopup="true" aria-expanded="false">Services
            <svg viewBox="0 0 12 8" class="caret" aria-hidden="true"><path d="M1 1.5 6 6.5 11 1.5" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
          </a>
          <div class="drop"><ul>{items}</ul></div>
        </div>
        <a href="{r}#work">Work</a>
        <a href="{r}#process">Process</a>
        <a href="{r}pricing/"{cls('pricing')}>Pricing</a>
        <a href="{r}about/"{cls('about')}>About</a>
        <a href="{r}contact/"{cls('contact')}>Contact Us</a>
      </nav>

      <div class="header-actions">
        <a href="{r}contact/" class="btn btn-primary btn-sm">Book a Call</a>
        <button class="menu-toggle" id="menuToggle" aria-label="Open menu" aria-expanded="false" aria-controls="mobileMenu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </div>
</header>

<div class="mobile-menu" id="mobileMenu">
  <nav aria-label="Mobile primary">
    <a href="{r}">Home</a>
    <button class="m-drop-toggle" id="mDropToggle" aria-expanded="false" aria-controls="mDropList">
      Services
      <svg viewBox="0 0 12 8" aria-hidden="true"><path d="M1 1.5 6 6.5 11 1.5" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
    </button>
    <div class="m-drop" id="mDropList"><ul>{items}</ul></div>
    <a href="{r}#work">Work</a>
    <a href="{r}#process">Process</a>
    <a href="{r}pricing/">Pricing</a>
    <a href="{r}about/">About</a>
    <a href="{r}contact/">Contact Us</a>
  </nav>
  <div class="mobile-menu-footer">
    <a href="{r}contact/" class="btn btn-primary">Book a Call</a>
    <p>{SITE['email']}</p>
  </div>
</div>
<main id="main">
"""


def footer(depth, three=False):
    r = rel(depth)
    # three.js is ~1.3MB, so only the page with the 3D hero loads it
    three_tag = f"""
<script type="importmap">
{{"imports":{{"three":"https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.module.js"}}}}
</script>
<script type="module" src="{r}js/hero3d.js?v={JS3_V}"></script>""" if three else ""
    svc_links = "".join(
        f'<a href="{r}services/{s["slug"]}/">{esc(s["nav"])}</a>' for s in SERVICES[:5]
    )
    socials = "".join(
        f'<a class="social" href="{url}" aria-label="{esc(label)}"'
        f'{" target=_blank rel=noopener" if url.startswith("http") else ""}>{icon(key)}</a>'
        for key, label, url in SOCIALS
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
      <a href="{r}pricing/">Pricing</a>
      <a href="{r}about/">About</a>
      <a href="{r}contact/">Contact Us</a>
    </div>
    <div class="footer-col">
      <h4>Connect</h4>
      <a href="mailto:{SITE['email']}">{SITE['email']}</a>
      <a href="tel:{SITE['phone_href']}">{SITE['phone_display']}</a>
      <div class="socials">{socials}</div>
      <a href="mailto:{SITE['email']}" class="btn btn-primary btn-sm footer-cta">Send Message</a>
    </div>
  </div>
  <div class="container footer-bottom">
    <p>&copy; <span id="year"></span> {SITE['name']}. All rights reserved.</p>
    <p>Made in India</p>
  </div>
</footer>
<script src="{r}js/script.js?v={JS_V}"></script>{three_tag}
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
    lds = [service_ld]

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
  <p class="section-label reveal">Keep exploring</p>
  <h2 class="section-title reveal">Related services</h2>
  <div class="rel-grid">{related}</div>
</section>

{cta(depth, "Ready to get started?", "Tell us about your project and we'll come back with a clear scope, timeline and fixed quote.")}
""" + footer(depth)


def pricing_cards(depth):
    r = rel(depth)
    out = ""
    for tier in PRICING:
        pts = "".join(f"<li>{esc(x)}</li>" for x in tier["points"])
        feat = " is-featured" if tier["featured"] else ""
        tag = '<span class="price-tag">Most popular</span>' if tier["featured"] else ""
        out += f"""
        <article class="price-card{feat} reveal">
          {tag}
          <h3>{esc(tier['name'])}</h3>
          <p class="price-meta">{esc(tier['meta'])}</p>
          <div class="price-discount">
            <span class="price-off">{esc(tier['discount'])}</span>
            <span class="price-was">{esc(tier['original_price'])}</span>
          </div>
          <p class="price-amt">{esc(tier['price'])}<span>{esc(tier['unit'])}</span></p>
          <ul class="price-list">{pts}</ul>
          <a href="{r}contact/" class="btn {'btn-primary' if tier['featured'] else 'btn-ghost'} price-btn">Book a call</a>
        </article>"""
    return out


def pricing_page():
    depth = 1
    title = "Pricing | Website, SEO & Marketing Packages in India | Dsignzhub"
    meta = ("Transparent pricing for website design, e-commerce, SEO, Google Ads and branding. "
            "Fixed quotes in Indian rupees, with no lock-in.")
    return head(title, meta, "pricing/", depth, []) + header(depth, "pricing") + f"""
<section class="svc-hero">
  <div class="container">
    <p class="eyebrow reveal">Pricing</p>
    <h1 class="svc-h1 reveal">Select your plan</h1>
    <p class="svc-lede reveal">Straightforward packages in rupees. Every plan is a fixed quote after a
      short scoping call &mdash; you will never get an invoice you did not expect.</p>
  </div>
</section>

<section class="sec--tight">
  <div class="container">
    <div class="price-grid">{pricing_cards(depth)}</div>
    <p class="price-note reveal">Need something outside these? Most of our work is scoped to the
      brief. Tell us what you need and we will quote it properly.</p>
  </div>
</section>

{cta(depth, "Not sure which plan fits?", "Tell us your goal and budget, and we will tell you honestly what will move the needle.")}
""" + footer(depth)


def services_index():
    depth = 1
    r = rel(depth)
    cards = "".join(f"""
      <a class="s-card reveal" href="{r}services/{s['slug']}/">
        <span class="glass-ico">{icon(s['slug'])}</span>
        <h2>{esc(s['nav'])}</h2>
        <p>{esc(s['lede'][:135].rsplit(' ', 1)[0])}…</p>
        <span class="rel-go">Explore <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      </a>""" for s in SERVICES)

    title = "Our Services | Web, E-commerce, SEO & Branding | Dsignzhub"
    meta = ("End-to-end digital services for Indian businesses — website design and development, "
            "PWAs, e-commerce, digital marketing, SEO, Google Ads, graphic design and branding.")
    return head(title, meta, "services/", depth, []) + header(depth, "services") + f"""
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

    pillars = "".join(f"""
        <article class="pillar reveal">
          <span class="glass-ico">{icon(ic)}</span>
          <h3>{esc(t)}</h3>
          <p>{esc(d)}</p>
        </article>""" for ic, t, d in PILLARS)

    stats = "".join(f"""
        <div class="stat reveal">
          <span class="stat-n">{esc(n)}</span>
          <span class="stat-l">{esc(l)}</span>
          <p>{esc(d)}</p>
        </div>""" for n, l, d in STATS)

    cards = "".join(f"""
      <a class="service-card reveal" href="{r}services/{s['slug']}/">
        <span class="glass-ico">{icon(s['slug'])}</span>
        <h3>{esc(s['nav'])}</h3>
        <p>{esc(s['lede'][:104].rsplit(' ', 1)[0])}&hellip;</p>
        <span class="rel-go">Explore <svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h10M9 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></span>
      </a>""" for s in SERVICES)

    work = "".join(f"""
        <article class="work-card reveal">
          <div class="work-head">
            <h3>{esc(name)}</h3>
            <p>{esc(desc)}</p>
            <div class="work-meta">
              <span class="work-tag">{esc(tag)}</span>
              <svg class="work-go" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 17 17 7M9 7h8v8" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>
            </div>
          </div>
          <div class="work-shot">
            <img src="{asset_url(f'assets/work/{img}', depth)}" alt="{esc(name)}" loading="lazy" width="560" height="380">
          </div>
        </article>""" for name, tag, img, desc in SHOWCASE)

    voices = "".join(f"""
        <blockquote class="voice reveal">
          <svg viewBox="0 0 24 24" aria-hidden="true"><use href="#i-quote"/></svg>
          <p>&ldquo;{esc(v)}&rdquo;</p>
        </blockquote>""" for v in VOICES)

    steps = "".join(f"""
        <div class="step reveal">
          <span class="step-num">{i+1:02d}</span>
          <h3>{esc(t)}</h3>
          <p>{esc(d)}</p>
        </div>""" for i, (t, d) in enumerate(PROCESS))

    marquee_items = "".join(
        f"<span>{esc(s['nav'])}</span><span aria-hidden='true'>&bull;</span>" for s in SERVICES)

    org_ld = {
        "@context": "https://schema.org", "@type": "Organization",
        "name": SITE["name"], "url": SITE["domain"] + "/", "email": SITE["email"],
        "description": SITE["tagline"], "areaServed": {"@type": "Country", "name": "India"},
    }
    site_ld = {"@context": "https://schema.org", "@type": "WebSite",
               "name": SITE["name"], "url": SITE["domain"] + "/"}

    title = "Dsignzhub | Web Design, Development, SEO & Digital Marketing in India"
    meta = ("Dsignzhub builds websites, online stores and marketing that grow Indian businesses. "
            "Website design and development, PWAs, e-commerce, SEO, Google Ads and branding.")

    return head(title, meta, "", depth, [org_ld, site_ld]) + header(depth, "home") + f"""
<section class="hero">
  <div class="container hero-grid">
    <div class="hero-copy">
      <h1 class="display reveal">Every digital service your business needs, <span class="grad-text">under one roof</span></h1>
      <p class="lede reveal">Websites, online stores, SEO, Google Ads and branding &mdash; designed, built and
        marketed by one team, so nothing falls through the gap between agencies.</p>
      <div class="hero-cta reveal">
        <a href="{r}contact/" class="btn btn-primary btn-lg">Book a Call</a>
        <p class="hero-note">Design, build, rank and advertise &mdash;<br>handled by a single team.</p>
      </div>
    </div>

    <div class="hero-art reveal" aria-hidden="true">
      <div class="hero-3d" id="heroStage">
        <canvas id="hero3d"></canvas>
        <svg class="hero-3d-fallback" viewBox="0 0 100 100" fill="none"><path fill="currentColor" fill-rule="evenodd" d="M26 14H48A36 36 0 0 1 48 86H14V26Z M30 30H66V40L46 60H66V70H30V60L50 40H30Z"/></svg>
      </div>
      <div class="hero-badge">
        <span class="hero-badge-n">9</span>
        <span class="hero-badge-l">services<br>on tap</span>
      </div>
    </div>
  </div>
</section>

<section class="stats">
  <div class="container stats-grid">{stats}</div>
</section>

<section class="sec">
  <div class="container">
    <div class="sec-head">
      <span class="eyebrow reveal">Full coverage</span>
      <h2 class="display reveal">One team, not five vendors</h2>
      <p class="lede reveal">Most businesses lose time and money in the gaps between their designer,
        their developer and their marketer. We close those gaps by doing all three.</p>
    </div>
    <div class="pillars">{pillars}</div>
  </div>
</section>

<section class="sec" id="services">
  <div class="container">
    <div class="sec-head">
      <span class="eyebrow reveal">What we do</span>
      <h2 class="display reveal">Services</h2>
      <p class="lede reveal">Everything needed to get found, chosen and remembered online.</p>
    </div>
    <div class="services-grid">{cards}</div>
  </div>
</section>

<section class="sec" id="work">
  <div class="container">
    <div class="sec-head">
      <span class="eyebrow reveal">Selected work</span>
      <h2 class="display reveal">What we build</h2>
    </div>
    <div class="work-grid">{work}</div>
  </div>
</section>

<section class="sec">
  <div class="container">
    <div class="sec-head">
      <span class="eyebrow reveal">Sound familiar?</span>
      <h2 class="display reveal">Problems we hear<br>before people call us</h2>
    </div>
    <div class="voices">{voices}</div>
  </div>
</section>

<section class="sec" id="pricing">
  <div class="container">
    <div class="sec-head">
      <span class="eyebrow reveal">Pricing</span>
      <h2 class="display reveal">Select your plan</h2>
      <p class="lede reveal">Straightforward packages in rupees, billed annually with no hidden invoices.</p>
    </div>
    <div class="price-grid">{pricing_cards(depth)}</div>
  </div>
</section>

<section class="sec" id="process">
  <div class="container">
    <div class="sec-head">
      <span class="eyebrow reveal">How we work</span>
      <h2 class="display reveal">A process without surprises</h2>
    </div>
    <div class="approach-steps">{steps}</div>
  </div>
</section>

{cta(depth, "Ready to build something that works?", "Tell us about your project and we will come back with a clear scope, a timeline and a fixed quote.")}
""" + footer(depth, three=True)


def about():
    depth = 1
    title = "About Dsignzhub | Digital Agency for Indian Businesses"
    meta = ("Dsignzhub is a digital agency combining design, development and marketing to help "
            "Indian businesses build a lasting online presence.")
    steps = "".join(f"""
        <div class="step reveal">
          <span class="step-num">{i+1:02d}</span>
          <h3>{esc(t)}</h3>
          <p>{esc(d)}</p>
        </div>""" for i, (t, d) in enumerate(PROCESS))

    return head(title, meta, "about/", depth, []) + header(depth, "about") + f"""
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
    lds = [{
        "@context": "https://schema.org",
        "@type": "ContactPage",
        "url": f"{SITE['domain']}/contact/",
    }]
    return head(title, meta, "contact/", depth, lds) + header(depth, "contact") + f"""
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
    global CSS_V, JS_V, JS3_V
    CSS_V = asset_version("css/style.css")
    JS_V = asset_version("js/script.js")
    JS3_V = asset_version("js/hero3d.js")
    print(f"asset versions: css={CSS_V} js={JS_V}")

    written = []
    written.append(write("index.html", home()))
    written.append(write("services/index.html", services_index()))
    written.append(write("about/index.html", about()))
    written.append(write("contact/index.html", contact()))
    written.append(write("pricing/index.html", pricing_page()))
    for svc in SERVICES:
        written.append(write(f"services/{svc['slug']}/index.html", service_page(svc)))

    # sitemap + robots
    urls = [""] + ["services/", "pricing/", "about/", "contact/"] + [f"services/{s['slug']}/" for s in SERVICES]
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
