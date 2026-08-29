# SVG icon set. Inlined once per page as a <symbol> sprite, referenced with <use>.
# All paths are drawn on a 24x24 grid and stroked (never filled) so one set works
# at any size and inherits colour from CSS.

ICONS = {
    "website-design-development": '<path d="M3 6.5A2.5 2.5 0 0 1 5.5 4h13A2.5 2.5 0 0 1 21 6.5V9H3V6.5Z"/><path d="M3 9h18v8.5a2.5 2.5 0 0 1-2.5 2.5h-13A2.5 2.5 0 0 1 3 17.5V9Z"/><path d="M6 6.5h.01M8.5 6.5h.01M11 6.5h.01"/><path d="M9 13l-2 2 2 2M15 13l2 2-2 2"/>',
    "progressive-web-apps": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M10 18.5h4"/><path d="M12 6.5v5M9.5 9h5"/>',
    "ecommerce-development": '<circle cx="9.5" cy="20" r="1.3"/><circle cx="17.5" cy="20" r="1.3"/><path d="M2.5 3h2.4l2.7 12h10.3l2.6-9H6"/>',
    "digital-marketing": '<path d="M3 11.5 19 4.5l-3 15.5-4.5-5.5L6 13Z"/><path d="M11.5 14.5 19 4.5"/>',
    "seo-services": '<circle cx="10.5" cy="10.5" r="6.5"/><path d="M21 21l-5.7-5.7"/><path d="M8 11.5l2 2 3.5-4"/>',
    "google-ads": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
    "graphic-design": '<rect x="3.5" y="3.5" width="17" height="12.5" rx="1.5"/><path d="M8 20.5h8M9.5 16v4.5h5V16"/><path d="M7 12l3-3.5 2.5 2.5L15 8l2 4"/>',
    "social-media-marketing": '<rect x="3" y="3" width="18" height="18" rx="4.5"/><circle cx="12" cy="12" r="3.6"/><path d="M17 7h.01"/>',
    "branding": '<path d="M12 2.5 2.5 7 12 11.5 21.5 7 12 2.5Z"/><path d="M2.5 16.5 12 21l9.5-4.5M2.5 11.8 12 16.3l9.5-4.5"/>',
    # feature / trust icons
    "mobile": '<rect x="6" y="2" width="12" height="20" rx="2.5"/><path d="M10 18.5h4"/>',
    "team": '<circle cx="9" cy="8.5" r="3.2"/><path d="M2.8 20a6.2 6.2 0 0 1 12.4 0"/><path d="M16 5.6a3.2 3.2 0 0 1 0 6M17.5 14.4A6.2 6.2 0 0 1 21.2 20"/>',
    "data": '<path d="M3 20V11M9 20V4M15 20v-6M21 20V8"/>',
    "india": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a15 15 0 0 1 0 18a15 15 0 0 1 0-18Z"/>',
    "speed": '<path d="M12 21a9 9 0 1 1 9-9"/><path d="M12 12l5-3.5"/><circle cx="12" cy="12" r="1.4"/>',
    "shield": '<path d="M12 2.8 4.5 6v6.2c0 4.4 3.1 8.1 7.5 9 4.4-.9 7.5-4.6 7.5-9V6L12 2.8Z"/><path d="M9 12l2 2 4-4.5"/>',
    "quote": '<path d="M9.5 6.5C6.4 7.8 4.5 10.5 4.5 14v3.5h6V11H7.8c.2-1.6 1-2.7 2.6-3.3l-.9-1.2Z"/><path d="M18.5 6.5c-3.1 1.3-5 4-5 7.5v3.5h6V11h-2.7c.2-1.6 1-2.7 2.6-3.3l-.9-1.2Z"/>',
    # social
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="4"/><path d="M7.5 10.5v6M7.5 7.6v.01M11.5 16.5v-6M11.5 13a2.5 2.5 0 0 1 5 0v3.5"/>',
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="3.8"/><path d="M17 7h.01"/>',
    "facebook": '<rect x="3" y="3" width="18" height="18" rx="4"/><path d="M14.5 8.5h-1.2a1.8 1.8 0 0 0-1.8 1.8V21M9.5 13h5"/>',
    "whatsapp": '<path d="M3.5 20.5l1.3-4.2A8 8 0 1 1 8 19.4l-4.5 1.1Z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5.6 0 1.2-.5 1.2-1.1l-1.6-.8-1 .9a5 5 0 0 1-2.1-2.1l.9-1-.8-1.6c-.6 0-1.1.6-1.1 1.2Z"/>',
    "arrow": '<path d="M3 12h16M13 6l6 6-6 6"/>',
    # contact rows (drawn with pathLength so CSS can animate a stroke draw-in)
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2.5" pathLength="100"/><path d="M4 7l8 6 8-6" pathLength="100"/>',
    "phone-call": '<path d="M6.5 3.5c-1.7 0-3 1.3-3 3 0 8.3 6.7 15 15 15 1.7 0 3-1.3 3-3v-2.2a1.5 1.5 0 0 0-1.2-1.5l-3.6-.8a1.5 1.5 0 0 0-1.5.5l-1 1.2a11.6 11.6 0 0 1-5.4-5.4l1.2-1a1.5 1.5 0 0 0 .5-1.5l-.8-3.6A1.5 1.5 0 0 0 8.7 3.5H6.5Z" pathLength="100"/>',
}


def sprite():
    """One <symbol> per icon, emitted once per page."""
    syms = "".join(
        f'<symbol id="i-{k}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{v}</symbol>'
        for k, v in ICONS.items()
    )
    return f'<svg class="icon-sprite" aria-hidden="true" width="0" height="0">{syms}</svg>'


def icon(name, cls="ico"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'
