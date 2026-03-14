# Provyx Website

## What This Is

Static marketing site for Provyx (getprovyx.com) — a healthcare provider business data company selling verified provider contacts, firmographics, and practice intelligence to healthcare marketing agencies, medical device sales teams, pharma reps, and health IT vendors. 396 pages built with Python build system on GitHub Pages.

## Core Value

Every page that ranks in Google Search results converts searchers into clicks — the site exists to generate inbound leads through organic search.

## Requirements

### Validated

<!-- Shipped and confirmed valuable. -->

- ✓ 396-page static site with programmatic SEO (providers, comparisons, alternatives, glossary, blog, state pages, resources, use-cases, ICP pages) — v1.0
- ✓ Technical SEO grade A: Article schema, FAQPage schema, BreadcrumbList, HowTo schema, Person schema, Organization schema, OG/Twitter cards, GA4 event tracking, consent mode, robots.txt AI crawlers, RSS feed, image sitemap
- ✓ 13 comparison pages, 11 alternative pages, 33 glossary terms, 50 state pages, 25 use-case pages, 38 resource pages, 7 ICP pages, 135+ provider spoke pages
- ✓ CRO features: scroll-triggered CTA, social proof near conversion points, pricing page enhancements
- ✓ Content quality: zero pages below 500 words, all metas 120-158 chars, no banned words
- ✓ CTR optimization on 10 highest-impression pages (titles, metas, H1s rewritten to match GSC query intent) — v1.0
- ✓ 11 new email list resource pages + 8 existing pages rewritten for "[specialty] email list" query intent — v1.0
- ✓ 5 content gap pages (DH pricing guide, NPPES accuracy guide, ketamine CRM, TMS CRM, EHR lead gen) — v1.0
- ✓ Pricing comparison section on DH alternative page + comparison table on vendor comparison page — v1.0
- ✓ EHR install base examples on technology detection + expanded firmographic content — v1.0

### Active

<!-- Current scope. Building toward these. -->

(None — next milestone not yet defined)

### Out of Scope

<!-- Explicit boundaries. Includes reasoning to prevent re-adding. -->

- Free interactive tools (NPI lookup, provider estimator) — high JS/API effort, separate milestone
- New comparison/alternative pages — already have 13+11, focus on optimizing existing
- Redesign or visual overhaul — site design is fine, problem is content-market fit

## Context

- GSC data (last 3 months ending 2026-03-13): 29 clicks, 7,514 impressions, 0.39% CTR — baseline before v1.0 optimizations
- v1.0 shipped 2026-03-14: 10 CTR pages optimized, 19 email list pages (11 new + 8 rewritten), 5 content gap pages
- Site: 396 pages (up from 355), 69 files changed, +14,021 / -820 lines
- Build system: `python3 scripts/build.py` generates all pages + sitemap
- Key data files: `scripts/build.py`, `scripts/blog_posts.py`, `scripts/templates.py`, `scripts/nav_config.py`
- Reference frameworks: coreyhaines31/marketingskills (SEO audit, copywriting, competitor-alternatives, programmatic SEO)

## Constraints

- **Tech stack**: Pure static HTML/CSS/JS, Python build system, GitHub Pages — no server-side rendering
- **Build**: All page changes go through `scripts/build.py` — no hand-editing HTML files
- **Brand**: Light theme, Plus Jakarta Sans, Navy #1B2A4A + Teal #0EA5E9, CLAUDE.md rules apply
- **Content**: No fabricated stats, every claim needs authoritative source, YMYL messaging rules
- **SEO**: Title 50-60 chars, meta 120-158 chars, 3+ internal links, 2+ outbound authority links per content page

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Prioritize CTR optimization over new pages | 7,500 impressions at 0.39% CTR = massive unrealized value | ✓ Good — 10 pages optimized, titles matched GSC query intent |
| Build email list pages from GSC query data | Proven search demand, not speculative content | ✓ Good — 19 pages covering all specialties with GSC demand |
| Skip research phase | Pure content optimization, no new technology or architecture | ✓ Good — saved time, all 4 phases completed in single session |
| Source DH pricing from G2/Capterra reviews | No fabricated stats rule, DH doesn't publish pricing | ✓ Good — credible sourcing without making up numbers |
| Content gap pages last | New pages need more research per page than optimizing existing ones | ✓ Good — existing page patterns informed new page creation |

---
*Last updated: 2026-03-14 after v1.0 milestone completion*
