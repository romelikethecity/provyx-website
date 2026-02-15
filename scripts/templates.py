#!/usr/bin/env python3
"""
Shared HTML generation module for the Provyx website build system.

This module provides all common HTML template functions used by build.py
to generate static pages. It reads navigation and footer data from
nav_config.py and produces clean, SEO-optimized HTML output.

Usage:
    from templates import get_page_wrapper, write_page

    html = get_page_wrapper(
        title="Dental Provider Data",
        description="Access verified dental provider contact data.",
        canonical_path="/providers/dental/",
        body_content="<section>...</section>",
        active_page="/providers/",
    )
    write_page("providers/dental/index.html", html)
"""

import os
import json
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nav_config import (
    NAV_ITEMS,
    FOOTER_COLUMNS,
    SITE_NAME,
    SITE_URL,
    SITE_TAGLINE,
    COPYRIGHT_YEAR,
    CTA_HREF,
    CTA_LABEL,
)


# =============================================================================
# CONSTANTS
# =============================================================================

BASE_URL = "https://getprovyx.com"
CSS_VERSION = "7"


# =============================================================================
# HTML HEAD
# =============================================================================

OG_IMAGE_MAP = {
    "/providers/": "og-providers.png",
    "/services/": "og-services.png",
    "/compare/": "og-compare.png",
    "/alternatives/": "og-alternatives.png",
    "/resources/": "og-resources.png",
    "/use-cases/": "og-resources.png",
    "/for/": "og-providers.png",
}
DEFAULT_OG_IMAGE = "og-providers.png"


def _get_og_image_url(canonical_path):
    """Return the correct OG image URL (PNG) based on the page section."""
    for prefix, image in OG_IMAGE_MAP.items():
        if canonical_path.startswith(prefix):
            return f"{BASE_URL}/assets/images/{image}"
    return f"{BASE_URL}/assets/images/{DEFAULT_OG_IMAGE}"


def get_html_head(title, description, canonical_path, extra_schema="",
                  noindex=False, og_type="website"):
    """Generate complete <head> section with meta, OG, fonts, favicon, GA4, CSS.

    Args:
        title: Page title (without site name suffix). 50-60 chars target.
        description: Meta description. 120-158 chars target.
        canonical_path: Path for canonical URL, e.g. "/providers/dental/"
        extra_schema: Optional additional JSON-LD schema script tags
        noindex: If True, add robots noindex and omit canonical tag
        og_type: Open Graph type, e.g. "website" or "article"
    """
    canonical = f"{BASE_URL}{canonical_path}"
    full_title = f"{title} | {SITE_NAME}" if title != SITE_NAME else title
    og_image = _get_og_image_url(canonical_path)
    canonical_tag = "" if noindex else f'\n    <link rel="canonical" href="{canonical}">'
    if noindex:
        robots_tag = '\n    <meta name="robots" content="noindex">'
    else:
        robots_tag = '\n    <meta name="robots" content="max-snippet:-1, max-image-preview:large, max-video-preview:-1">'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="theme-color" content="#1B2A4A">
    <title>{full_title}</title>
    <meta name="description" content="{description}">{canonical_tag}{robots_tag}

    <!-- Open Graph -->
    <meta property="og:type" content="{og_type}">
    <meta property="og:url" content="{canonical}">
    <meta property="og:title" content="{full_title}">
    <meta property="og:description" content="{description}">
    <meta property="og:site_name" content="{SITE_NAME}">
    <meta property="og:image" content="{og_image}">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{full_title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{og_image}">
{extra_schema}
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="/assets/favicons/favicon.svg">
    <link rel="icon" type="image/svg+xml" sizes="16x16" href="/assets/favicons/favicon-16.svg">
    <link rel="apple-touch-icon" sizes="180x180" href="/assets/favicons/apple-touch-icon.png">
    <link rel="manifest" href="/site.webmanifest">
    <link rel="alternate" type="application/rss+xml" title="{SITE_NAME} Guides" href="{BASE_URL}/feed.xml">

    <!-- Preconnect to analytics -->
    <link rel="preconnect" href="https://www.googletagmanager.com">
    <link rel="dns-prefetch" href="https://www.googletagmanager.com">
    <link rel="preconnect" href="https://www.google-analytics.com">
    <link rel="dns-prefetch" href="https://www.google-analytics.com">

    <!-- Preload critical resources -->
    <link rel="preload" href="/assets/fonts/plus-jakarta-sans-latin.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="preload" href="/css/styles.min.css?v={CSS_VERSION}" as="style">

    <!-- Fonts (self-hosted) -->
    <link rel="stylesheet" href="/assets/fonts/plus-jakarta-sans.min.css">

    <!-- CSS -->
    <link rel="stylesheet" href="/css/styles.min.css?v={CSS_VERSION}">

    <!-- Google Analytics 4 with Consent Mode v2 -->
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('consent', 'default', {{
        'ad_storage': 'denied',
        'analytics_storage': 'denied',
        'ad_user_data': 'denied',
        'ad_personalization': 'denied'
      }});
      var _pc = localStorage.getItem('provyx-consent');
      if (_pc === 'granted') {{
        gtag('consent', 'update', {{
          'ad_storage': 'granted',
          'analytics_storage': 'granted',
          'ad_user_data': 'granted',
          'ad_personalization': 'granted'
        }});
      }}
    </script>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-QERDPYTQ9D"></script>
    <script>
      gtag('js', new Date());
      gtag('config', 'G-QERDPYTQ9D');
    </script>
</head>'''


# =============================================================================
# NAVIGATION
# =============================================================================

def _build_desktop_nav_items(active_page=None):
    """Build desktop nav list items HTML."""
    items_html = ""
    for item in NAV_ITEMS:
        children = item.get("children")
        is_active = active_page and active_page.startswith(item["href"])

        if children:
            # Dropdown nav item
            chevron_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12" fill="currentColor"><path d="M2 4l4 4 4-4"/></svg>'
            dropdown_items = ""
            for child in children:
                dropdown_items += f'<a href="{child["href"]}" class="nav__dropdown-item">{child["label"]}</a>\n'

            items_html += f'''<li class="nav__item--dropdown">
                    <button class="nav__dropdown-toggle" aria-expanded="false">{item["label"]} {chevron_svg}</button>
                    <div class="nav__dropdown">
                        {dropdown_items}
                    </div>
                </li>'''
        else:
            link_classes = "nav__link nav__link--active" if is_active else "nav__link"
            items_html += f'<li><a href="{item["href"]}" class="{link_classes}">{item["label"]}</a></li>'

    return items_html


def _build_mobile_nav_items():
    """Build mobile nav list items HTML."""
    items_html = ""
    for item in NAV_ITEMS:
        children = item.get("children")

        if children:
            chevron_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 12" fill="currentColor"><path d="M2 4l4 4 4-4"/></svg>'
            dropdown_items = ""
            for child in children:
                dropdown_items += f'<a href="{child["href"]}" class="nav__dropdown-item">{child["label"]}</a>\n'

            items_html += f'''<li class="nav__item--dropdown">
                    <button class="nav__dropdown-toggle" aria-expanded="false">{item["label"]} {chevron_svg}</button>
                    <div class="nav__dropdown">
                        {dropdown_items}
                    </div>
                </li>'''
        else:
            items_html += f'<li><a href="{item["href"]}" class="nav__link">{item["label"]}</a></li>'

    return items_html


def get_nav_html(active_page=None):
    """Generate full header + mobile nav HTML with inline JS toggle.

    Args:
        active_page: Current page path for active state, e.g. "/providers/"
    """
    desktop_items = _build_desktop_nav_items(active_page)
    mobile_items = _build_mobile_nav_items()

    return f'''<body>
    <a href="#main-content" class="sr-only sr-only--focusable">Skip to main content</a>
    <header class="header" role="banner">
        <div class="container header__inner">
            <a href="/" class="header__logo">
                <img src="/assets/favicons/favicon.svg" alt="" class="header__logo-icon" width="32" height="32" fetchpriority="high">
                <span class="header__logo-text">{SITE_NAME}</span>
            </a>

            <nav class="nav--desktop" role="navigation" aria-label="Main navigation">
                <ul class="nav__list">
                    {desktop_items}
                </ul>
            </nav>

            <div class="header__cta">
                <a href="{CTA_HREF}" class="btn btn--primary btn--sm">{CTA_LABEL}</a>
            </div>

            <button class="menu-toggle" aria-label="Open menu" aria-expanded="false">
                <span class="menu-toggle__icon"></span>
            </button>
        </div>
    </header>

    <nav class="nav--mobile" role="navigation" aria-label="Mobile navigation">
        <ul class="nav__list">
            {mobile_items}
        </ul>
        <a href="{CTA_HREF}" class="btn btn--primary">{CTA_LABEL}</a>
    </nav>

    <script>
    (function(){{
        var toggle=document.querySelector('.menu-toggle');
        var mobileNav=document.querySelector('.nav--mobile');
        if(!toggle||!mobileNav)return;
        toggle.addEventListener('click',function(){{
            var open=mobileNav.classList.toggle('active');
            toggle.classList.toggle('active');
            toggle.setAttribute('aria-expanded',open);
            document.body.style.overflow=open?'hidden':'';
        }});
        var dropdowns=document.querySelectorAll('.nav__item--dropdown .nav__dropdown-toggle');
        dropdowns.forEach(function(btn){{
            btn.addEventListener('click',function(e){{
                e.preventDefault();
                var parent=btn.closest('.nav__item--dropdown');
                var wasActive=parent.classList.contains('active');
                if(mobileNav.contains(parent)){{
                    mobileNav.querySelectorAll('.nav__item--dropdown.active').forEach(function(d){{d.classList.remove('active');d.querySelector('.nav__dropdown-toggle').setAttribute('aria-expanded','false');}});
                }}
                if(!wasActive){{
                    parent.classList.add('active');
                    btn.setAttribute('aria-expanded','true');
                }}else{{
                    parent.classList.remove('active');
                    btn.setAttribute('aria-expanded','false');
                }}
            }});
        }});
    }})();
    </script>

    <main id="main-content">'''


# =============================================================================
# FOOTER
# =============================================================================

def get_footer_html():
    """Generate complete footer with logo, tagline, link columns, copyright."""
    columns_html = ""
    for heading, links in FOOTER_COLUMNS.items():
        links_html = ""
        for link in links:
            if link["href"].startswith("http"):
                links_html += f'<li><a href="{link["href"]}" target="_blank" rel="noopener noreferrer">{link["label"]}</a></li>\n'
            else:
                links_html += f'<li><a href="{link["href"]}">{link["label"]}</a></li>\n'

        columns_html += f'''
            <div class="footer__column">
                <h4 class="footer__heading">{heading}</h4>
                <ul class="footer__links">
                    {links_html}
                </ul>
            </div>'''

    return f'''
    </main>

    <footer class="footer" role="contentinfo">
        <div class="container">
            <div class="footer__grid">
                <div class="footer__brand">
                    <a href="/" class="footer__logo">
                        <img src="/assets/favicons/favicon.svg" alt="" class="footer__logo-icon" width="32" height="32" loading="lazy">
                        <span class="footer__logo-text">{SITE_NAME}</span>
                    </a>
                    <p class="footer__tagline">{SITE_TAGLINE}</p>
                </div>
                {columns_html}
            </div>
            <div class="footer__bottom">
                <span>&copy; {COPYRIGHT_YEAR} {SITE_NAME}. All rights reserved.</span>
            </div>
        </div>
    </footer>

    <div id="consent-banner" class="consent-banner" style="display:none">
        <p>We use cookies to analyze site traffic and improve your experience. <a href="/privacy/">Privacy Policy</a></p>
        <div class="consent-banner__actions">
            <button class="consent-banner__btn consent-banner__btn--accept" onclick="provyxConsent('granted')">Accept</button>
            <button class="consent-banner__btn consent-banner__btn--deny" onclick="provyxConsent('denied')">Deny</button>
        </div>
    </div>
    <script>
    function provyxConsent(v){{
      localStorage.setItem('provyx-consent',v);
      if(v==='granted'){{
        gtag('consent','update',{{'ad_storage':'granted','analytics_storage':'granted','ad_user_data':'granted','ad_personalization':'granted'}});
      }}
      document.getElementById('consent-banner').style.display='none';
    }}
    if(!localStorage.getItem('provyx-consent')){{
      document.getElementById('consent-banner').style.display='';
    }}
    </script>
    <script src="/js/main.js" defer></script>
</body>
</html>'''


# =============================================================================
# BREADCRUMBS
# =============================================================================

def get_breadcrumb_schema(breadcrumbs):
    """Generate BreadcrumbList JSON-LD schema.

    Args:
        breadcrumbs: List of dicts with 'name' and 'url' keys.
                    Example: [{"name": "Home", "url": "https://getprovyx.com"},
                             {"name": "Providers", "url": "https://getprovyx.com/providers/"}]
    Returns:
        JSON-LD script tag as string, or empty string if no breadcrumbs.
    """
    if not breadcrumbs:
        return ""

    items = []
    for i, crumb in enumerate(breadcrumbs, 1):
        items.append({
            "@type": "ListItem",
            "position": i,
            "name": crumb.get("name", ""),
            "item": crumb.get("url", "")
        })

    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }

    return f'''
    <script type="application/ld+json">
{json.dumps(schema, indent=2)}
    </script>'''


def get_breadcrumb_html(breadcrumbs):
    """Generate visible breadcrumb navigation HTML.

    Args:
        breadcrumbs: List of dicts with 'name' and 'url' keys.
                    Last item is treated as current page (no link).
    """
    if not breadcrumbs:
        return ""

    crumb_parts = []
    for i, crumb in enumerate(breadcrumbs):
        if i < len(breadcrumbs) - 1:
            crumb_parts.append(f'<a href="{crumb["url"]}">{crumb["name"]}</a>')
            crumb_parts.append('<span class="breadcrumb__separator">/</span>')
        else:
            crumb_parts.append(f'<span class="breadcrumb__current">{crumb["name"]}</span>')

    return f'''<nav class="breadcrumb" aria-label="Breadcrumb">
            {" ".join(crumb_parts)}
        </nav>'''


# =============================================================================
# FAQ
# =============================================================================

def generate_faq_html(faqs, heading="Frequently Asked Questions"):
    """Generate FAQ section HTML with FAQPage schema markup.

    Args:
        faqs: List of dicts with 'question' and 'answer' keys
        heading: Section heading text

    Returns:
        HTML string for FAQ section with schema, or empty string if no FAQs
    """
    if not faqs:
        return ""

    # Build FAQ items HTML (accordion pattern)
    faq_items_html = ""
    for faq in faqs:
        faq_items_html += f'''
                <details class="faq-item">
                    <summary class="faq-item__question">{faq["question"]}</summary>
                    <div class="faq-item__answer"><p>{faq["answer"]}</p></div>
                </details>'''

    # Build FAQPage schema
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["answer"]
                }
            }
            for faq in faqs
        ]
    }
    schema_html = f'<script type="application/ld+json">{json.dumps(faq_schema)}</script>'

    return f'''
        {schema_html}
        <section class="section faq-section">
            <div class="container">
                <h2>{heading}</h2>
                {faq_items_html}
            </div>
        </section>'''


# =============================================================================
# AEO/GEO CONTENT BLOCKS (Answer Engine & Generative Engine Optimization)
# =============================================================================

def generate_definition_block(term, definition, expanded=""):
    """Generate a definition block optimized for featured snippets.

    Targets 'What is [X]?' queries. Structured for extraction by Google
    and AI systems.

    Args:
        term: The term being defined
        definition: 1-sentence concise definition
        expanded: 1-2 sentence expanded explanation (optional)
    """
    expanded_html = f"<p>{expanded}</p>" if expanded else ""
    return f'''<div class="definition-block">
            <h3>What is {term}?</h3>
            <p><strong>{term}</strong> {definition}</p>
            {expanded_html}
        </div>'''


def generate_stat_block(stats):
    """Generate a statistic block optimized for AI citation.

    Stats increase AI citation rates by 15-30%. Include source attribution.

    Args:
        stats: List of dicts with 'value', 'label', and optional 'source' keys
    """
    items = ""
    for stat in stats:
        source = f' <span class="stat-source">({stat["source"]})</span>' if stat.get("source") else ""
        items += f'''<li><strong>{stat["value"]}</strong> {stat["label"]}{source}</li>'''
    return f'''<ul class="stat-block">{items}</ul>'''


def generate_step_block(title, steps):
    """Generate a step-by-step block optimized for list snippet capture.

    Targets 'How to [X]' queries.

    Args:
        title: Process title (e.g. 'How to Build a Provider Contact List')
        steps: List of dicts with 'name' and 'description' keys
    """
    items = ""
    for i, step in enumerate(steps, 1):
        items += f'''<li><strong>{step["name"]}:</strong> {step["description"]}</li>'''
    return f'''<div class="step-block">
            <h3>{title}</h3>
            <ol>{items}</ol>
        </div>'''


def generate_howto_schema(title, steps):
    """Generate HowTo JSON-LD schema for step blocks.

    Args:
        title: Process title (e.g. 'How to Build a Provider Contact List')
        steps: List of dicts with 'name' and 'description' keys
    """
    schema = {
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": title,
        "step": [
            {
                "@type": "HowToStep",
                "position": i,
                "name": step["name"],
                "text": step["description"],
            }
            for i, step in enumerate(steps, 1)
        ],
    }
    return f'\n    <script type="application/ld+json">\n{json.dumps(schema, indent=2)}\n    </script>'


# =============================================================================
# ARTICLE SCHEMA
# =============================================================================

def generate_article_schema(title, description, canonical_path, date_published="2026-02-01",
                            date_modified=None, speakable_selectors=None,
                            author_person=None):
    """Generate Article JSON-LD schema for content pages.

    Args:
        title: Article headline
        description: Article description
        canonical_path: Path e.g. "/compare/provyx-vs-zoominfo/"
        date_published: ISO date string (YYYY-MM-DD)
        date_modified: ISO date string, defaults to date_published
        speakable_selectors: List of CSS selectors for SpeakableSpecification
        author_person: Optional dict with 'name', 'url', 'credentials' for Person author
    """
    url = f"{BASE_URL}{canonical_path}"
    og_image = _get_og_image_url(canonical_path)
    if not date_modified:
        date_modified = date_published

    if author_person:
        author_obj = {
            "@type": "Person",
            "name": author_person["name"],
            "url": author_person.get("url", ""),
            "jobTitle": author_person.get("credentials", ""),
            "worksFor": {
                "@type": "Organization",
                "@id": f"{BASE_URL}/#organization",
                "name": SITE_NAME,
            },
        }
    else:
        author_obj = {
            "@type": "Organization",
            "@id": f"{BASE_URL}/#organization",
            "name": SITE_NAME,
        }

    schema = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": description,
        "url": url,
        "inLanguage": "en-US",
        "image": og_image,
        "datePublished": date_published,
        "dateModified": date_modified,
        "author": author_obj,
        "publisher": {
            "@type": "Organization",
            "@id": f"{BASE_URL}/#organization",
            "name": SITE_NAME,
            "logo": {
                "@type": "ImageObject",
                "url": f"{BASE_URL}/assets/images/og-providers.png",
            },
        },
    }

    if speakable_selectors:
        schema["speakable"] = {
            "@type": "SpeakableSpecification",
            "cssSelector": speakable_selectors,
        }

    return f'''
    <script type="application/ld+json">
{json.dumps(schema, indent=2)}
    </script>'''


# =============================================================================
# TESTIMONIAL / EXPERT QUOTE BLOCKS
# =============================================================================

def generate_testimonial_block(quote, name, title, org):
    """Generate an expert testimonial block with named attribution.

    Named attribution with title/org increases AI citation rates 15-30%.

    Args:
        quote: Direct quote text (no surrounding quotes needed)
        name: Person's full name
        title: Job title/role
        org: Organization/company name
    """
    return f'''<blockquote class="testimonial-block">
            <p class="testimonial-block__text">"{quote}"</p>
            <footer class="testimonial-block__attribution">
                <strong>{name}</strong>, {title} at {org}
            </footer>
        </blockquote>'''


# =============================================================================
# CTA SECTION
# =============================================================================

def generate_cta_section(title="Get the Provider Data You Need",
                         text="Tell us what you're looking for. We'll build a custom list matched to your target market.",
                         button_text=None, button_href=None,
                         include_form=False, formspree_id=""):
    """Generate navy CTA section with button or contact form.

    Args:
        title: CTA heading
        text: CTA description
        button_text: Button label (defaults to CTA_LABEL from nav_config)
        button_href: Button URL (defaults to CTA_HREF from nav_config)
        include_form: If True, render a contact form instead of a button
        formspree_id: Formspree form ID for the action URL
    """
    btn_text = button_text or CTA_LABEL
    btn_href = button_href or CTA_HREF

    if include_form and formspree_id:
        action_url = f"https://formspree.io/f/{formspree_id}"
        inner = f'''
                <form class="form" action="{action_url}" method="POST">
                    <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
                    <div class="form__row">
                        <div class="form__group">
                            <label class="form__label" for="cta-name">Name</label>
                            <input class="form__input" type="text" id="cta-name" name="name" required>
                        </div>
                        <div class="form__group">
                            <label class="form__label" for="cta-email">Email</label>
                            <input class="form__input" type="email" id="cta-email" name="email" required>
                        </div>
                    </div>
                    <div class="form__group">
                        <label class="form__label" for="cta-company">Company</label>
                        <input class="form__input" type="text" id="cta-company" name="company">
                    </div>
                    <div class="form__group">
                        <label class="form__label" for="cta-message">What data do you need?</label>
                        <textarea class="form__textarea" id="cta-message" name="message" rows="3"></textarea>
                    </div>
                    <button type="submit" class="btn btn--white btn--lg form__submit">{btn_text}</button>
                </form>'''
    else:
        inner = f'''
                <a href="{btn_href}" class="btn btn--white btn--lg">{btn_text}</a>'''

    return f'''
        <section class="section cta-section">
            <div class="container">
                <div class="cta-section__header">
                    <h2 class="cta-section__title">{title}</h2>
                    <p class="cta-section__text">{text}</p>
                </div>
                {inner}
                <p class="cta-section__proof">Trusted by healthcare sales teams, medical device companies, and health IT vendors across the US.</p>
            </div>
        </section>'''


# =============================================================================
# PAGE WRAPPER
# =============================================================================

def get_page_wrapper(title, description, canonical_path, body_content,
                     active_page=None, extra_schema="", noindex=False,
                     og_type="website"):
    """Generate a complete HTML page by combining head, nav, content, footer.

    Args:
        title: Page title for <title> tag
        description: Meta description
        canonical_path: Path for canonical URL, e.g. "/providers/dental/"
        body_content: Inner HTML content (sections, etc.)
        active_page: Nav item to highlight, e.g. "/providers/"
        extra_schema: Additional JSON-LD schema script tags
        noindex: If True, add robots noindex and omit canonical tag
        og_type: Open Graph type, e.g. "website" or "article"

    Returns:
        Complete HTML page as string
    """
    head = get_html_head(title, description, canonical_path, extra_schema,
                         noindex=noindex, og_type=og_type)
    nav = get_nav_html(active_page)
    footer = get_footer_html()

    return f'''{head}
{nav}

{body_content}

{footer}'''


# =============================================================================
# FILE WRITER
# =============================================================================

def write_page(path, html):
    """Write an HTML page to disk, creating directories as needed.

    Args:
        path: Relative file path from project root, e.g. "providers/dental/index.html"
        html: Complete HTML content string
    """
    # Determine project root (one level up from scripts/)
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(project_root, path)

    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w") as f:
        f.write(html)

    print(f"  Generated: /{path}")
