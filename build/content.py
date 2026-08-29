# Content source for every generated page.
# Edit copy here, then run `python3 build/build.py` from the repo root.

SITE = {
    "name": "Dsignzhub",
    "domain": "https://www.dsignzhub.com",
    "email": "hello@dsignzhub.com",
    "phone_display": "+91 86672 53891",
    "phone_href": "+918667253891",
    "tagline": "Digital design, development & marketing for Indian businesses.",
    # Web3Forms access key tied to hello@dsignzhub.com — get one free at
    # https://web3forms.com (enter the email, no account/signup needed, key
    # arrives by email in seconds). Paste it here to make the contact form
    # deliver to the inbox; until then it silently falls back to mailto:.
    "web3forms_key": "c6060d64-0474-40b7-b717-5ed761d22485",
}

# Order here drives the nav dropdown, the services index and the footer.
SERVICES = [
    {
        "slug": "website-design-development",
        "nav": "Website Design & Development",
        "h1": "Website Design & Development",
        "title": "Website Design & Development Company in India | Dsignzhub",
        "meta": "Custom website design and development for Indian businesses. Fast, mobile-first, SEO-ready websites built to convert visitors into customers. Get a free quote.",
        "keyword": "website design and development",
        "eyebrow": "Websites that earn their keep",
        "lede": "We design and build fast, mobile-first websites that turn visitors into enquiries. Every site is built on clean code, structured for search engines, and designed around how your customers actually buy.",
        "intro": [
            "Your website is usually the first thing a customer checks before they call you. If it loads slowly, looks dated, or is hard to use on a phone, you lose the enquiry before a conversation ever starts. We build websites that remove that friction.",
            "Every project starts with your business, not a template. We map out who you are selling to, what they need to see before they trust you, and what action you want them to take. Only then do we design a single screen.",
        ],
        "deliverables": [
            ("Custom design, no templates", "Every layout is designed around your content and your customers, not forced into a theme you have to work around."),
            ("Mobile-first build", "Designed for the phone first, because that is where the majority of Indian web traffic actually comes from."),
            ("Core Web Vitals performance", "Optimised images, lean code and fast hosting so pages load quickly and rank better."),
            ("SEO-ready foundation", "Clean heading structure, schema markup, meta tags and sitemaps built in from day one."),
            ("Easy-to-update CMS", "Change text, images and pages yourself without going back to a developer for every edit."),
            ("Analytics & tracking", "Google Analytics and conversion tracking configured so you can see what the site is actually doing."),
        ],
        "benefits": [
            ("Built to convert", "Clear calls to action, fast enquiry forms and trust signals placed where they change decisions."),
            ("Owned, not rented", "You own the code, the domain and the hosting. No lock-in to a platform you cannot leave."),
            ("Ready to grow", "Structured so new pages, services and locations can be added without a rebuild."),
            ("Search-friendly from launch", "Technical SEO handled during the build, not bolted on months later."),
        ],
        "faqs": [
            ("How much does a website cost in India?", "Cost depends on the number of pages, the level of custom design and whether you need e-commerce or custom functionality. A focused business website typically sits in a different bracket to a large catalogue site. We give a fixed quote after a short scoping call, so there are no surprises later."),
            ("How long does it take to build a website?", "A standard business website usually takes four to six weeks from kickoff to launch. Larger builds with custom functionality or e-commerce take longer. The biggest variable is usually how quickly content and approvals come back from your side."),
            ("Will my website work on mobile?", "Yes. We design mobile-first, which means the phone layout is designed before the desktop one, then tested across real screen sizes rather than assumed."),
            ("Can I update the website myself?", "Yes. We build on a content management system and hand over a short training session, so you can edit text, swap images and publish new pages without needing us."),
            ("Do you provide hosting and maintenance?", "We can. We offer ongoing maintenance covering hosting, backups, security updates and small content changes, or we can hand everything over if you prefer to manage it in-house."),
        ],
        "related": ["progressive-web-apps", "ecommerce-development", "seo-services"],
    },
    {
        "slug": "progressive-web-apps",
        "nav": "Progressive Web App Development",
        "h1": "Progressive Web App Development",
        "title": "Progressive Web App (PWA) Development Company | Dsignzhub",
        "meta": "PWA development services in India. Get app-like speed, offline access and home-screen install without the cost of building separate iOS and Android apps.",
        "keyword": "progressive web app development",
        "eyebrow": "App experience, no app store",
        "lede": "A progressive web app gives your customers the speed and feel of a native app — installable, offline-capable, instantly loading — without the cost of building and maintaining separate iOS and Android builds.",
        "intro": [
            "Building a native app means two codebases, two review processes and a customer who has to be persuaded to download something. A progressive web app skips all of that. It runs in the browser, installs to the home screen in one tap, and updates the moment you publish.",
            "For most Indian businesses, a PWA delivers the parts of an app that actually matter — speed, reliability on patchy connections, and a presence on the home screen — at a fraction of the cost.",
        ],
        "deliverables": [
            ("Installable to home screen", "Customers add your app in one tap, with your icon and splash screen, no app store required."),
            ("Works on poor connections", "Service workers cache the important parts, so the app still opens on 3G or when the signal drops."),
            ("Push notifications", "Re-engage customers directly with offers and updates, the same way a native app would."),
            ("Single codebase", "One build serves Android, iOS and desktop, so you are not paying to maintain three products."),
            ("Instant updates", "Publish a change and every user has it immediately, with no app store review delay."),
            ("Fully indexable", "Unlike a native app, every page can be found in Google search."),
        ],
        "benefits": [
            ("Lower build cost", "One codebase instead of separate native iOS and Android development."),
            ("No download friction", "Customers try it instantly from a link rather than committing to an install."),
            ("Reliable on Indian networks", "Built to stay usable when connectivity is slow or intermittent."),
            ("Cheaper to maintain", "One thing to update, test and support instead of three."),
        ],
        "faqs": [
            ("What is a progressive web app?", "A progressive web app is a website built with capabilities that used to belong only to native apps — it can be installed to the home screen, work offline, and send push notifications, while still being just a URL you can share."),
            ("Is a PWA better than a native app?", "It depends on what you need. If you require deep device features like advanced camera control or Bluetooth hardware, native still wins. For most business use cases — catalogues, bookings, ordering, dashboards, content — a PWA delivers the same experience for far less money."),
            ("Do PWAs work on iPhone?", "Yes. iOS supports home-screen installation and offline caching. Some capabilities such as push notifications have historically been more limited on iOS than on Android, so we scope around what your audience actually uses."),
            ("Can an existing website become a PWA?", "Often yes. If the current site is technically sound, we can add the service worker, manifest and caching layer to it. If it is built on aging code, a rebuild may be more cost-effective and we will tell you honestly which applies."),
            ("Will a PWA help my SEO?", "It helps indirectly. PWAs are fast, and speed is a ranking factor. Unlike a native app, all the content stays crawlable and indexable in Google."),
        ],
        "related": ["website-design-development", "ecommerce-development", "seo-services"],
    },
    {
        "slug": "ecommerce-development",
        "nav": "E-commerce Solutions",
        "h1": "E-commerce Website Development",
        "title": "E-commerce Website Development Company in India | Dsignzhub",
        "meta": "Build an online store that sells. E-commerce website development with UPI and payment gateway integration, inventory management and conversion-focused design.",
        "keyword": "ecommerce website development",
        "eyebrow": "Stores built to sell",
        "lede": "We build online stores designed around one job: making it effortless to browse, buy and come back. Payment gateways, inventory, shipping and analytics all wired up and working from day one.",
        "intro": [
            "Most online stores do not fail because of traffic. They fail at the checkout, on the product page, or on a search box that cannot find what the customer typed. We build stores where those moments are designed, not left to a default theme.",
            "From a focused catalogue to thousands of SKUs, we handle the full build — product architecture, payments, shipping logic, tax, and the analytics that tell you what is actually selling.",
        ],
        "deliverables": [
            ("Payment gateway integration", "UPI, cards, net banking, wallets and cash on delivery, set up with the gateway that suits your margins."),
            ("Product & inventory management", "Variants, stock levels and bulk uploads structured so managing the catalogue does not become a full-time job."),
            ("Conversion-focused checkout", "A short, tested checkout flow that reduces the abandonment most stores quietly lose money to."),
            ("Shipping & logistics setup", "Courier integration, zone-based rates and automated tracking updates for customers."),
            ("Search & filtering", "Product search and filters that actually surface the right items, even on a large catalogue."),
            ("Sales analytics", "Enhanced e-commerce tracking so you can see which products, channels and campaigns drive revenue."),
        ],
        "benefits": [
            ("Fewer abandoned carts", "A checkout designed to remove hesitation at the exact point customers usually leave."),
            ("Sell around the clock", "Your storefront keeps taking orders outside business hours and beyond your city."),
            ("Built for repeat purchase", "Accounts, order history and re-order flows that make the second purchase easier than the first."),
            ("Scales with the catalogue", "Architecture that still performs when the catalogue grows from fifty products to five thousand."),
        ],
        "faqs": [
            ("Which e-commerce platform is best?", "There is no single answer. Shopify suits businesses that want speed to launch and low maintenance. WooCommerce suits those who want full ownership and flexibility. A custom build makes sense when your model does not fit either. We recommend based on your catalogue, margins and team, not on what is easiest for us."),
            ("Can you integrate UPI and Indian payment gateways?", "Yes. We work with Razorpay, PayU, CCAvenue, Cashfree and Stripe, including UPI, cards, net banking, wallets and cash on delivery."),
            ("Can you migrate my existing store?", "Yes. We migrate products, customers, orders and SEO URLs, using redirects so you do not lose the search rankings you already have."),
            ("Do you handle GST and invoicing?", "Yes. We configure GST-compliant tax rules and automated invoice generation as part of the build."),
            ("What about ongoing support after launch?", "We offer maintenance plans covering security updates, backups, performance monitoring and catalogue support, so the store keeps running as it grows."),
        ],
        "related": ["website-design-development", "digital-marketing", "google-ads"],
    },
    {
        "slug": "digital-marketing",
        "nav": "Digital Marketing",
        "h1": "Digital Marketing Services",
        "title": "Digital Marketing Agency in India | Dsignzhub",
        "meta": "Data-driven digital marketing services for Indian businesses. Strategy, campaigns and reporting built around leads and revenue, not vanity metrics.",
        "keyword": "digital marketing services",
        "eyebrow": "Marketing measured in revenue",
        "lede": "We build and run digital marketing campaigns that are judged on one thing: what they return. Strategy, execution and honest reporting across the channels where your customers actually spend their time.",
        "intro": [
            "Plenty of agencies will send you a monthly report full of impressions and reach. Very few will tell you what those numbers earned. We work the other way round — starting from the revenue target and working backwards to the channels, budget and creative needed to hit it.",
            "That means we will sometimes recommend spending less on a channel, or dropping one entirely. The goal is a marketing spend that pays for itself, not a bigger retainer.",
        ],
        "deliverables": [
            ("Channel strategy", "A clear plan for where your budget goes and why, based on where your buyers actually are."),
            ("Campaign management", "Day-to-day running and optimisation across search, social and display."),
            ("Content & creative", "Ad creative, landing pages and copy built to convert, not just to fill a slot."),
            ("Marketing automation", "Email and WhatsApp flows that follow up with leads automatically instead of letting them go cold."),
            ("Conversion tracking", "Proper attribution so you know which channel produced which enquiry."),
            ("Transparent reporting", "Monthly reporting focused on cost per lead and return, with the raw data available to you."),
        ],
        "benefits": [
            ("Spend that is accountable", "Every rupee is tracked to an outcome, so underperforming channels get cut early."),
            ("Consistent lead flow", "Campaigns tuned to produce a predictable pipeline rather than unpredictable spikes."),
            ("Compounding results", "Learnings feed back into creative and targeting month over month."),
            ("One team across channels", "Search, social and site all handled together, so the message stays consistent."),
        ],
        "faqs": [
            ("How much should I spend on digital marketing?", "It depends on your margins, your average order value and how competitive your category is. We usually start with a test budget large enough to gather meaningful data, then scale the channels that prove themselves and cut the ones that do not."),
            ("How quickly will I see results?", "Paid channels can produce leads within days of launch. SEO and content compound more slowly, typically showing meaningful movement across three to six months. We set expectations per channel before we start rather than after."),
            ("Do you work with small businesses?", "Yes. A significant part of our work is with small and mid-sized Indian businesses. What matters is that the numbers can work, not the size of the company."),
            ("Will I own my ad accounts and data?", "Yes, always. Accounts are created under your ownership and you keep full access to them and all historical data, including if we stop working together."),
            ("What do you report on?", "Cost per lead, conversion rate, return on ad spend and revenue attributed by channel — plus what we changed that month and what we plan to change next."),
        ],
        "related": ["seo-services", "google-ads", "social-media-marketing"],
    },
    {
        "slug": "seo-services",
        "nav": "SEO Services",
        "h1": "SEO Services",
        "title": "SEO Services Company in India | Dsignzhub",
        "meta": "SEO services that grow qualified organic traffic. Technical SEO, on-page optimisation, content and local SEO for Indian businesses. Transparent monthly reporting.",
        "keyword": "SEO services",
        "eyebrow": "Get found by people ready to buy",
        "lede": "Search visibility that brings in customers who are already looking for what you sell. Technical fixes, content that answers real questions, and the local signals that put you in the map pack.",
        "intro": [
            "SEO works because the intent is already there. Someone searching for your service in your city is far closer to buying than someone who happened to scroll past an ad. The job is making sure you are the business they find.",
            "We work across the three things that actually move rankings: a technically sound site, content that genuinely answers what people are searching for, and authority signals that tell Google you are credible.",
        ],
        "deliverables": [
            ("Technical SEO audit", "Crawl, index, speed and structure issues found and fixed, starting with what is costing you the most."),
            ("Keyword & intent research", "The terms your buyers actually use, mapped to the stage of the buying decision they are at."),
            ("On-page optimisation", "Titles, headings, internal links and schema markup structured for both search engines and readers."),
            ("Content strategy", "A content plan that targets real queries rather than publishing for the sake of a word count."),
            ("Local SEO", "Google Business Profile, local citations and location pages so you show up in map results."),
            ("Link building", "Genuine authority built through relevant, earned placements, not bought link farms."),
        ],
        "benefits": [
            ("Traffic that keeps paying", "Unlike ads, rankings keep delivering after the spend stops."),
            ("Higher-intent visitors", "People searching for a solution convert better than people interrupted by an ad."),
            ("Local visibility", "Show up when nearby customers search, including in the map pack."),
            ("Compounding advantage", "Authority accumulates, making each new page easier to rank than the last."),
        ],
        "faqs": [
            ("How long does SEO take to work?", "Typically three to six months before meaningful movement, longer in competitive categories. Technical fixes can show results faster. Anyone promising first-page rankings in thirty days is either targeting terms nobody searches for or is not being straight with you."),
            ("Can you guarantee a number one ranking?", "No, and neither can anyone else honestly. Google does not sell or guarantee positions. What we do commit to is a clear plan, the work being done properly, and transparent reporting on what is moving."),
            ("What is local SEO?", "Local SEO focuses on showing up when someone searches with local intent — your service plus a city, or simply 'near me'. It involves your Google Business Profile, local citations, reviews and location-specific pages."),
            ("Do I need to keep paying for SEO forever?", "No, though competitors keep working, so rankings do erode if abandoned entirely. Many clients move to a lighter maintenance engagement once they reach their target positions."),
            ("Will you fix my existing website or rebuild it?", "Whichever costs you less for the same result. If the current site is technically sound we optimise it. If its structure is fundamentally limiting, we will say so and show you why."),
        ],
        "related": ["digital-marketing", "google-ads", "website-design-development"],
    },
    {
        "slug": "google-ads",
        "nav": "Google Ads",
        "h1": "Google Ads Management",
        "title": "Google Ads Management Services in India | Dsignzhub",
        "meta": "Google Ads management that generates qualified leads, not wasted clicks. Search, Shopping and Performance Max campaigns with transparent cost-per-lead reporting.",
        "keyword": "Google Ads management",
        "eyebrow": "Leads from day one",
        "lede": "Google Ads is the fastest way to put your business in front of people actively searching to buy. We build and manage campaigns that keep the cost per lead falling instead of the budget rising.",
        "intro": [
            "Most underperforming Google Ads accounts are not failing because of the budget. They are failing because they are paying for broad keywords that were never going to convert, sending clicks to a slow landing page, and measuring success by clicks rather than enquiries.",
            "We rebuild campaigns around tightly-matched search intent, landing pages designed for one action, and conversion tracking that tells the truth about what each lead actually costs.",
        ],
        "deliverables": [
            ("Account structure & setup", "Campaigns organised so budget flows to the terms that convert and away from the ones that drain it."),
            ("Keyword & negative research", "As much work on excluding the wrong searches as on finding the right ones."),
            ("Ad copy & extensions", "Ads written and tested against each other, with every relevant extension in use."),
            ("Landing page optimisation", "Pages built for a single action, because the best campaign cannot rescue a weak page."),
            ("Conversion tracking", "Calls, forms and WhatsApp enquiries all tracked, so reporting reflects reality."),
            ("Shopping & Performance Max", "Product feed setup and management for e-commerce catalogues."),
        ],
        "benefits": [
            ("Immediate visibility", "Live at the top of search results as soon as campaigns launch."),
            ("Pay only for clicks", "Budget goes to people who actively clicked, with a daily cap you control."),
            ("Precise targeting", "Location, device, time of day and search intent all controlled."),
            ("Fully measurable", "Every rupee traceable to a click, a lead and ultimately a sale."),
        ],
        "faqs": [
            ("What is a good budget for Google Ads in India?", "It depends entirely on your category — cost per click varies hugely between industries. We research the actual cost per click for your keywords and work out the realistic budget needed to generate a meaningful number of leads before you commit anything."),
            ("How is your management fee structured?", "A transparent monthly management fee, separate from your ad spend. Your ad budget goes to Google directly from your own account, so you can always see exactly what was spent."),
            ("How soon will I get leads?", "Campaigns can start generating enquiries within days of going live. The first few weeks are about gathering data, then we tighten targeting and cut waste, which is usually where cost per lead drops."),
            ("Do I need a separate landing page?", "Usually yes. Sending paid traffic to a general homepage almost always converts worse than sending it to a page built for that specific search and one clear action."),
            ("Who owns the Google Ads account?", "You do. We set it up under your ownership and you retain full access and all historical data, including if you stop working with us."),
        ],
        "related": ["digital-marketing", "seo-services", "ecommerce-development"],
    },
    {
        "slug": "graphic-design",
        "nav": "Print & Graphic Design",
        "h1": "Print & Graphic Design",
        "title": "Graphic Design & Print Design Services in India | Dsignzhub",
        "meta": "Professional graphic design and print services — brochures, packaging, catalogues, stationery and marketing collateral designed to press-ready standards.",
        "keyword": "graphic design services",
        "eyebrow": "Design that holds up in print",
        "lede": "Brochures, packaging, catalogues and collateral designed with the same care as your digital presence — and prepared properly, so what arrives from the printer matches what you approved.",
        "intro": [
            "Print is unforgiving. A colour that looked right on screen can arrive flat, and a logo placed too close to the trim can come back cut. Good print design is as much about production knowledge as it is about layout.",
            "We design collateral that looks considered and hand over press-ready artwork with the bleed, colour profiles and resolution your printer actually needs.",
        ],
        "deliverables": [
            ("Brochures & catalogues", "Multi-page layouts with a clear reading order, designed to be scanned as well as read."),
            ("Packaging design", "Retail packaging that works on a shelf, with regulatory and barcode requirements handled."),
            ("Corporate stationery", "Letterheads, business cards and templates that stay consistent across your team."),
            ("Marketing collateral", "Flyers, standees, hoardings and exhibition graphics scaled correctly for each format."),
            ("Press-ready artwork", "Correct bleed, crop marks, CMYK profiles and resolution so nothing surprises you at the printer."),
            ("Editable templates", "Templates your team can update in-house for recurring material."),
        ],
        "benefits": [
            ("Consistent brand presence", "Print and digital that clearly belong to the same business."),
            ("Production-ready files", "Artwork prepared to specification, avoiding costly reprints."),
            ("Designed for the format", "A hoarding and a business card are different problems and get treated that way."),
            ("Full source files", "You keep the working files, so you are never locked to one designer."),
        ],
        "faqs": [
            ("Do you provide print-ready files?", "Yes. Every project is handed over as press-ready artwork with correct bleed, crop marks, CMYK colour profiles and image resolution, in the format your printer requires."),
            ("Can you handle the printing too?", "We can coordinate with print vendors and manage quality checks, or supply the files to a printer you already use. Either works."),
            ("How many design revisions are included?", "Our standard projects include multiple structured revision rounds. We agree the number up front so expectations are clear on both sides."),
            ("Do you design packaging with regulatory requirements?", "Yes. We handle mandatory declarations, barcodes, nutritional panels and statutory information as required for your product category."),
            ("Will I get the source files?", "Yes. You receive the editable working files along with the final exports."),
        ],
        "related": ["branding", "social-media-marketing", "website-design-development"],
    },
    {
        "slug": "social-media-marketing",
        "nav": "Social Media & Banners",
        "h1": "Social Media Creative & Banners",
        "title": "Social Media Marketing & Banner Design Services | Dsignzhub",
        "meta": "Social media creative and banner design that stops the scroll. Campaign creative, festive posts and ad banners sized correctly for every platform.",
        "keyword": "social media banner design",
        "eyebrow": "Creative that stops the scroll",
        "lede": "Social creative built for the way people actually use their feeds — designed to be understood in the half-second before a thumb moves, and sized correctly for every placement.",
        "intro": [
            "A post that works on Instagram rarely works unchanged on LinkedIn, and an ad banner has a different job to an organic post. Resizing one design to fit everywhere is why so much social creative underperforms.",
            "We design per platform and per purpose, with a consistent visual system so everything still reads as your brand.",
        ],
        "deliverables": [
            ("Campaign creative", "Coordinated sets that carry one idea across multiple posts and formats."),
            ("Platform-correct sizing", "Every asset exported at the right dimensions for each placement, no awkward crops."),
            ("Ad banner design", "Paid creative built for the metric it is being judged on."),
            ("Festive & seasonal posts", "Timely creative for the festivals and moments that matter to Indian audiences."),
            ("Motion & animated posts", "Short animated formats that earn more attention in a crowded feed."),
            ("Content templates", "Branded templates so your team can produce routine posts without breaking consistency."),
        ],
        "benefits": [
            ("Higher engagement", "Creative designed for the feed, not repurposed from a brochure."),
            ("Consistent identity", "A recognisable look across every platform you post on."),
            ("Faster turnaround", "Templates and systems that shorten the path from idea to published."),
            ("Better ad performance", "Stronger creative lowers the cost of every paid campaign it appears in."),
        ],
        "faqs": [
            ("Which platforms do you design for?", "Instagram, Facebook, LinkedIn, YouTube, X and WhatsApp Business, plus display ad networks. Each gets assets at its correct dimensions rather than one design stretched to fit."),
            ("Do you also manage the accounts?", "We can. Creative design and full social media management are separate services, so you can take just the design work if you already have someone posting."),
            ("How many posts are included monthly?", "Packages are built around your posting frequency and how much of it is campaign work versus routine content. We scope it to what you will realistically publish."),
            ("Can you design in regional languages?", "Yes. We produce creative in English, Hindi and major regional languages, with typography set properly rather than pasted in."),
            ("Do you provide editable templates?", "Yes. We can supply branded templates your team can update in-house for routine posts."),
        ],
        "related": ["graphic-design", "digital-marketing", "branding"],
    },
    {
        "slug": "branding",
        "nav": "Branding",
        "h1": "Branding & Brand Identity",
        "title": "Branding Agency in India | Brand Identity Design | Dsignzhub",
        "meta": "Branding and brand identity design for Indian businesses. Logo design, brand strategy, visual identity systems and brand guidelines that build recognition and trust.",
        "keyword": "branding agency",
        "eyebrow": "Be remembered, not just seen",
        "lede": "A brand is what people say about you when you are not in the room. We build the strategy, the identity and the guidelines that make that description consistent, distinctive and worth repeating.",
        "intro": [
            "Most businesses do not have a brand problem, they have a consistency problem. The logo is fine, but every touchpoint looks like it came from a different company, and nothing is memorable enough to recall a week later.",
            "We start with positioning — who you are for and why you are the better choice — then build a visual and verbal identity that expresses it the same way everywhere.",
        ],
        "deliverables": [
            ("Brand strategy", "Positioning, audience and messaging defined before any visual work begins."),
            ("Logo & identity design", "A primary mark with the variants you need for every real-world context."),
            ("Visual identity system", "Colour, typography, imagery and graphic language that work as a coherent set."),
            ("Brand voice", "How you sound in writing, so your copy is as recognisable as your logo."),
            ("Brand guidelines", "A practical document any designer or printer can follow without guessing."),
            ("Launch collateral", "The core assets needed to put the new identity into the world."),
        ],
        "benefits": [
            ("Instant recognition", "A distinctive identity people recall rather than confuse with a competitor."),
            ("Justifies your pricing", "A considered brand supports a premium position; an inconsistent one undermines it."),
            ("Consistency at scale", "Guidelines that keep everything on-brand as your team and vendors grow."),
            ("Faster trust", "Looking established shortens the distance to a first conversation."),
        ],
        "faqs": [
            ("What is included in a branding project?", "Typically brand strategy and positioning, logo and identity design, a full visual system covering colour and typography, brand voice guidance, and a guidelines document. We scope the exact deliverables to what your business actually needs."),
            ("How long does branding take?", "A full identity project usually runs six to ten weeks depending on scope and how many stakeholders are involved in approvals. A focused logo and identity refresh can be quicker."),
            ("Do I get all the logo file formats?", "Yes. You receive vector source files plus exports in every format you will need for web, print, social and signage, including one-colour and reversed variants."),
            ("Can you refresh our existing brand?", "Yes. A refresh that keeps existing recognition while modernising the execution is often smarter than starting over, and we will tell you if that is the better route."),
            ("Do you help apply the brand afterwards?", "Yes. We regularly carry the new identity through to websites, packaging, print collateral and social templates."),
        ],
        "related": ["graphic-design", "website-design-development", "social-media-marketing"],
    },
]

PROCESS = [
    ("Discover", "We learn your business, your customers and your goals before proposing anything."),
    ("Plan", "You get a clear scope, a fixed quote and a timeline, so there are no surprises later."),
    ("Build", "Design and development run together, with progress you can see rather than wait for."),
    ("Grow", "After launch we measure, refine and keep improving what the numbers tell us to."),
]

SERVICE_BY_SLUG = {s["slug"]: s for s in SERVICES}


# --------------------------------------------------------------------------
# Homepage showcase.
#
# PLACEHOLDER WORK. The artwork is generated abstract mockups, not real client
# projects, and no client names or performance figures are claimed anywhere on
# purpose — publishing invented case studies or metrics would mislead visitors.
# Replace `image` with real screenshots and fill in `client` when you have
# permission to name them.
# --------------------------------------------------------------------------
SHOWCASE = [
    ("E-commerce Website", "Retail", "ecommerce.jpg",
     "A storefront built around fast browsing, filterable catalogues and a short, tested checkout."),
    ("Performance Dashboard", "Analytics", "dashboard.jpg",
     "Campaign and revenue reporting pulled into one screen, so decisions come from data."),
    ("Brand Identity System", "Branding", "branding.jpg",
     "Logo, palette, typography and guidelines built as one coherent, reusable system."),
    ("Progressive Web App", "Mobile", "mobile-app.jpg",
     "App-like speed and home-screen install without the cost of separate native builds."),
    ("Search Visibility", "SEO", "seo.jpg",
     "Technical fixes and content structured to rank for terms real buyers actually search."),
    ("Social Campaign Set", "Creative", "social.jpg",
     "Coordinated creative sized correctly for every platform and placement."),
]

# Trust markers shown under the hero. Numbers are illustrative placeholders —
# replace them with real figures before promoting the site.
STATS = [
    ("9", "Services under one roof"),
    ("100%", "Mobile-first builds"),
    ("24h", "Typical quote turnaround"),
    ("0", "Lock-in — you own everything"),
]

WHY_US = [
    ("mobile", "Mobile-first by default", "Designed for the phone first, because that is where most Indian web traffic comes from."),
    ("team", "One team, every discipline", "Design, development, SEO and marketing under one roof — no handoffs, no gaps."),
    ("data", "Data-driven decisions", "We track what matters and adjust based on real performance, not guesswork."),
    ("shield", "You own everything", "Code, domains, ad accounts and source files stay yours, including if you leave."),
]


# --------------------------------------------------------------------------
# Homepage blocks for the redesign.
# STATS and VOICES are illustrative placeholders — swap in real figures and
# real things clients have said before promoting the site.
# --------------------------------------------------------------------------
PILLARS = [
    ("team", "Every channel, one team",
     "Instead of juggling one agency for SEO, another for design and a freelancer for ads, you get a single team that talks to itself. Strategy and execution stay connected."),
    ("data", "Decisions from data",
     "Tracking is configured properly from day one, so we can tell you which channel produced which enquiry — and cut what isn't working before it drains the budget."),
    ("shield", "Clarity and control",
     "Fixed scope, fixed quote, and work you can see progressing. No hidden hours, no surprise invoices, and everything we build stays yours."),
]

STATS = [
    ("9", "Services on tap", "Design, build and marketing handled by one team."),
    ("100%", "Mobile-first", "Every build starts at the phone, where your customers actually are."),
    ("24h", "Quote turnaround", "Scope, timeline and a fixed price, usually within a working day."),
    ("0", "Lock-in", "Code, domains and ad accounts stay in your name."),
]

# Objections we actually hear — written as the prospect's own words.
VOICES = [
    "Our website looks fine on desktop but falls apart on a phone.",
    "We're paying for ads and have no idea which ones bring enquiries.",
    "Every agency sends a report full of numbers that mean nothing to me.",
    "Our brand looks different on every platform we post to.",
    "We rank nowhere for the things our customers actually search.",
    "The last developer disappeared and we can't edit our own site.",
]


# --------------------------------------------------------------------------
# Pricing.
# Three annual website packages, replacing the earlier four-tier monthly-retainer
# model. original_price/discount drive the strikethrough + badge and are meant
# to stay on permanently, not as a limited-time promo.
PRICING = [
    {
        "name": "Starter Website",
        "meta": "Perfect for Startups and Small Businesses",
        "original_price": "₹13,499",
        "discount": "25% OFF",
        "price": "₹9,999",
        "unit": "/year",
        "featured": False,
        "points": [
            "Up to 5 Pages",
            "Custom Design",
            "Mobile Responsive",
            "Contact Form",
            "WhatsApp Integration",
            "Google Map Integration",
            "Social Media Integration",
            "Basic SEO Setup",
            "Basic Speed Optimization",
            "SSL Installation",
            "Basic Security",
            "Client Content Upload",
            "30 Minutes Training",
            "1 Month Free Support",
        ],
    },
    {
        "name": "Business Website",
        "meta": "Ideal for growing businesses and service providers",
        "original_price": "₹26,665",
        "discount": "25% OFF",
        "price": "₹19,999",
        "unit": "/year",
        "featured": False,
        "points": [
            "Up to 15 Pages",
            "Custom Design",
            "Mobile Responsive",
            "Contact Form",
            "WhatsApp Integration",
            "Google Map Integration",
            "Social Media Integration",
            "Blog Module",
            "SEO Setup",
            "Standard Speed Optimization",
            "SSL + Security",
            "Admin Panel",
            "Dynamic Website",
            "Inquiry Management",
            "Google Analytics",
            "Search Console Setup",
            "30 Minutes Training",
            "1 Month Free Support",
        ],
    },
    {
        "name": "Premium Corporate Website",
        "meta": "Designed for businesses looking for a professional online presence",
        "original_price": "₹39,999",
        "discount": "25% OFF",
        "price": "₹29,999",
        "unit": "/year",
        "featured": False,
        "points": [
            "Up to 25 Premium Pages",
            "Premium UI/UX Design",
            "Mobile Responsive",
            "Contact Form",
            "WhatsApp Integration",
            "Google Map Integration",
            "Social Media Integration",
            "Advanced SEO Setup",
            "Advanced Speed Optimization",
            "Advanced Security",
            "Admin Panel",
            "Dynamic Website",
            "Inquiry Management",
            "Live Chat Integration",
            "Google Analytics",
            "Search Console Setup",
            "2 Hours Training",
            "1 Month Free Support",
        ],
    },
]

# Footer social links. Replace the '#' placeholders with the real profile URLs.
SOCIALS = [
    ("linkedin", "LinkedIn", "#"),
    ("instagram", "Instagram", "#"),
    ("facebook", "Facebook", "#"),
    ("whatsapp", "WhatsApp", "https://wa.me/918667253891"),
]
