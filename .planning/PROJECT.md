# Provyx Website

## What This Is

Static marketing site for Provyx (getprovyx.com) — a healthcare provider business data company selling verified provider contacts, firmographics, and practice intelligence to healthcare marketing agencies, medical device sales teams, pharma reps, and health IT vendors. 355 pages built with Python build system on GitHub Pages.

## Core Value

Every page that ranks in Google Search results converts searchers into clicks — the site exists to generate inbound leads through organic search.

## Requirements

### Validated

<!-- Shipped and confirmed valuable. -->

- ✓ 355-page static site with programmatic SEO (providers, comparisons, alternatives, glossary, blog, state pages, resources, use-cases, ICP pages)
- ✓ Technical SEO grade A: Article schema, FAQPage schema, BreadcrumbList, HowTo schema, Person schema, Organization schema, OG/Twitter cards, GA4 event tracking, consent mode, robots.txt AI crawlers, RSS feed, image sitemap
- ✓ 13 comparison pages, 11 alternative pages, 33 glossary terms, 50 state pages, 24 use-case pages, 27 resource pages, 7 ICP pages, 135+ provider spoke pages
- ✓ CRO features: scroll-triggered CTA, social proof near conversion points, pricing page enhancements
- ✓ Content quality: zero pages below 500 words, all metas 120-158 chars, no banned words

### Active

<!-- Current scope. Building toward these. -->

- [ ] CTR optimization on top-impression pages (rewrite titles, metas, above-the-fold content)
- [ ] Missing email list resource pages for specialties with search demand
- [ ] Content gap pages (DH pricing, ketamine/TMS CRM, NPPES accuracy, EHR lead gen)
- [ ] Strengthen pricing/cost sections on existing alternative and comparison pages
- [ ] Improve provider spoke pages for "[specialty] email list" query matching

### Out of Scope

<!-- Explicit boundaries. Includes reasoning to prevent re-adding. -->

- Free interactive tools (NPI lookup, provider estimator) — high JS/API effort, separate milestone
- New comparison/alternative pages — already have 13+11, focus on optimizing existing
- New blog articles unrelated to GSC query data — only build content matching proven search demand
- Redesign or visual overhaul — site design is fine, problem is content-market fit

## Context

- GSC data (last 3 months ending 2026-03-13): 29 clicks, 7,514 impressions, 0.39% CTR
- Top impression page: /resources/healthcare-data-vendor-comparison/ (1,681 impr, position 6.0, 0% CTR)
- Definitive Healthcare queries account for ~1,200+ impressions across alternative, comparison, and cost queries
- "[Specialty] email list" queries total 600+ impressions across 15+ specialties, ranking position 15-95
- Healthcare firmographic data queries: 55+ impressions, position 5.9-11.9
- Spravato/ketamine/TMS CRM queries: 50+ impressions, no matching content
- 97% of traffic is desktop, US-focused (5,388 of 7,514 impressions)
- Build system: `python3 scripts/build.py` generates all pages + sitemap
- Key data files: `scripts/build.py`, `scripts/templates.py`, `scripts/nav_config.py`
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
| Prioritize CTR optimization over new pages | 7,500 impressions at 0.39% CTR = massive unrealized value | — Pending |
| Build email list pages from GSC query data | Proven search demand, not speculative content | — Pending |
| Skip research phase | Pure content optimization, no new technology or architecture | — Pending |

---
*Last updated: 2026-03-13 after GSC analysis and milestone v1.0 kickoff*
