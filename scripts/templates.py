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
CSS_VERSION = "1"


# =============================================================================
# HTML HEAD
# =============================================================================

def get_html_head(title, description, canonical_path, extra_schema=""):
    """Generate complete <head> section with meta, OG, fonts, favicon, GA4, CSS.

    Args:
        title: Page title (without site name suffix). 50-60 chars target.
        description: Meta description. 120-158 chars target.
        canonical_path: Path for canonical URL, e.g. "/providers/dental/"
        extra_schema: Optional additional JSON-LD schema script tags
    """
    canonical = f"{BASE_URL}{canonical_path}"
    full_title = f"{title} | {SITE_NAME}" if title != SITE_NAME else title

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{full_title}</title>
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical}">

    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical}">
    <meta property="og:title" content="{full_title}">
    <meta property="og:description" content="{description}">
    <meta property="og:site_name" content="{SITE_NAME}">
    <meta property="og:image" content="{BASE_URL}/assets/logos/logo-social-og.svg">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{full_title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{BASE_URL}/assets/logos/logo-social-og.svg">
{extra_schema}
    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="/assets/logos/favicon.svg">
    <link rel="icon" type="image/png" sizes="16x16" href="/assets/logos/favicon-16.png">

    <!-- Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">

    <!-- CSS -->
    <link rel="stylesheet" href="/css/styles.css?v={CSS_VERSION}">

    <!-- GA4 (placeholder) -->
    <!-- <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script> -->
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
            active_class = ' class="nav__link--active"' if is_active else ''
            items_html += f'<li><a href="{item["href"]}" class="nav__link"{active_class}>{item["label"]}</a></li>'

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
    <header class="header" role="banner">
        <div class="container header__inner">
            <a href="/" class="header__logo">
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

    <main>'''


# =============================================================================
# FOOTER
# =============================================================================

def get_footer_html():
    """Generate complete footer with logo, tagline, link columns, copyright."""
    columns_html = ""
    for heading, links in FOOTER_COLUMNS.items():
        links_html = ""
        for link in links:
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
                    <a href="/" class="footer__logo-text">{SITE_NAME}</a>
                    <p class="footer__tagline">{SITE_TAGLINE}</p>
                </div>
                {columns_html}
            </div>
            <div class="footer__bottom">
                <span>&copy; {COPYRIGHT_YEAR} {SITE_NAME}. All rights reserved.</span>
            </div>
        </div>
    </footer>

    <script src="/js/main.js"></script>
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

    # Build FAQ items HTML
    faq_items_html = ""
    for faq in faqs:
        faq_items_html += f'''
                <h3>{faq["question"]}</h3>
                <p>{faq["answer"]}</p>'''

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
            </div>
        </section>'''


# =============================================================================
# PAGE WRAPPER
# =============================================================================

def get_page_wrapper(title, description, canonical_path, body_content,
                     active_page=None, extra_schema=""):
    """Generate a complete HTML page by combining head, nav, content, footer.

    Args:
        title: Page title for <title> tag
        description: Meta description
        canonical_path: Path for canonical URL, e.g. "/providers/dental/"
        body_content: Inner HTML content (sections, etc.)
        active_page: Nav item to highlight, e.g. "/providers/"
        extra_schema: Additional JSON-LD schema script tags

    Returns:
        Complete HTML page as string
    """
    head = get_html_head(title, description, canonical_path, extra_schema)
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
