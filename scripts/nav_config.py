#!/usr/bin/env python3
"""
Centralized navigation configuration for Provyx.

Edit this file to update navigation across ALL pages on the site.
After editing, regenerate all pages by running:
    python3 scripts/build.py
"""

# Site info
SITE_NAME = "Provyx"
SITE_URL = "https://getprovyx.com"
SITE_TAGLINE = "Healthcare Provider Intelligence"
COPYRIGHT_YEAR = "2026"

# CTA button
CTA_HREF = "/contact/"
CTA_LABEL = "Get Provider Data"

# Main navigation items (appear in header)
NAV_ITEMS = [
    {
        "href": "/providers/",
        "label": "Data",
        "children": [
            {"href": "/providers/", "label": "All Provider Data"},
            {"href": "/providers/dental/", "label": "Dental"},
            {"href": "/providers/mental-health/", "label": "Mental Health"},
            {"href": "/providers/medical-spas/", "label": "Medical Spas"},
            {"href": "/providers/primary-care/", "label": "Primary Care"},
            {"href": "/providers/chiropractic/", "label": "Chiropractic"},
        ],
    },
    {
        "href": "/services/",
        "label": "Services",
        "children": [
            {"href": "/services/provider-contact-data/", "label": "Provider Contacts"},
            {"href": "/services/practice-location-data/", "label": "Practice Locations"},
            {"href": "/services/technology-detection/", "label": "Technology Detection"},
            {"href": "/services/custom-list-building/", "label": "Custom Lists"},
        ],
    },
    {"href": "/pricing/", "label": "Pricing"},
    {"href": "/about/", "label": "About"},
]

# Footer link columns
FOOTER_COLUMNS = {
    "Data Products": [
        {"href": "/providers/", "label": "Provider Directory"},
        {"href": "/services/provider-contact-data/", "label": "Contact Data"},
        {"href": "/services/practice-location-data/", "label": "Location Data"},
        {"href": "/services/social-profiles/", "label": "Social Profiles"},
        {"href": "/services/practice-firmographics/", "label": "Firmographics"},
        {"href": "/services/technology-detection/", "label": "Technology Data"},
    ],
    "Services": [
        {"href": "/services/", "label": "All Services"},
        {"href": "/services/custom-list-building/", "label": "Custom List Building"},
        {"href": "/pricing/", "label": "Pricing"},
        {"href": "/contact/", "label": "Contact Us"},
    ],
    "Company": [
        {"href": "/about/", "label": "About Provyx"},
        {"href": "/privacy/", "label": "Privacy Policy"},
        {"href": "/terms/", "label": "Terms of Service"},
    ],
}
