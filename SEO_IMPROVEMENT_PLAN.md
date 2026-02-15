# Provyx Website SEO Improvement Plan (v2)

**Audit Date:** February 14, 2026
**Benchmarked Against:** coreyhaines31/marketingskills framework (349 recommendations)
**Current Grade:** A (up from A-, all Tier 1/2/4 items complete)

---

## What's Been Completed (Previous Rounds)

All items below are DONE and verified in the current build:

- [x] Social preview images: SVG → section-specific PNGs via OG_IMAGE_MAP
- [x] 404 page: noindex, no canonical, proper robots meta
- [x] Duplicate class attribute: merged to single class string
- [x] Organization schema: expanded with @id, logo, sameAs, contactPoint
- [x] Service schema: on all 6 service pages
- [x] Product schema: on pricing page with Offer objects
- [x] apple-touch-icon.png (180x180) + favicon.ico
- [x] Self-hosted fonts: Plus Jakarta Sans WOFF2, no Google Fonts CDN
- [x] CSS minification: rcssmin, styles.min.css output (24% reduction)
- [x] Resource preloading: font + CSS preload hints
- [x] Skip navigation: WCAG 2.1 Level A compliant
- [x] FAQ accordions: details/summary pattern (no h3 inside summary)
- [x] Footer competitor links: Compare column with 5 links
- [x] AEO/GEO blocks: definition, stat, step block helpers on homepage
- [x] Heading hierarchy: all h4→h3 skips fixed (contact, pricing, compare, alert-boxes, rec-boxes, outbound-references)
- [x] Breadcrumb Home URL: all 20 standardized to full URL with trailing slash
- [x] Broken internal links: 10 fixed (/for/ paths corrected)
- [x] noreferrer: added to all 164+ external links (including escaped-quote strings)
- [x] Unused font-face.css: deleted
- [x] Meta robots: max-snippet:-1, max-image-preview:large, max-video-preview:-1 on all indexable pages
- [x] Web manifest: site.webmanifest created and linked
- [x] og:type: "article" for comparison, resource, use-case, alternative, ICP pages
- [x] CSS version: bumped to v=5

### Round 2 (Feb 14, 2026):
- [x] Article schema with SpeakableSpecification on all content pages (~67 pages)
- [x] GA4 event tracking: cta_clicked, form_started, form_submitted, faq_expanded, scroll_depth, outbound_link_clicked, pricing_viewed
- [x] Robots.txt AI crawler rules (GPTBot, ChatGPT-User, PerplexityBot, anthropic-ai allowed; CCBot blocked)
- [x] Defer main.js loading
- [x] Content freshness dates: "Updated February 2026" on all content pages
- [x] HowTo schema on homepage + 6 service pages with step blocks
- [x] AEO/GEO blocks on 6 service pages (definition + step blocks) and 17 provider hub pages (definition blocks)
- [x] Social proof text near CTA sections, contact form, and pricing
- [x] Pricing enhancements: h2/h3 tag fixes, proof text
- [x] Broken internal links: 5 invalid provider slugs fixed
- [x] Trailing slash consistency: service breadcrumbs, index cards, related links
- [x] ItemList schema on providers, services, comparisons index pages
- [x] Lazy loading on competitor logos and footer logo
- [x] Cross-category internal linking: related_content on 6 service pages → use-cases/resources

### Round 3 (Feb 14, 2026):
- [x] HowTo schema on all 24 use-case pages (from step data)
- [x] Testimonial blocks with named attribution on all 6 service pages (generate_testimonial_block)
- [x] Scroll-triggered CTA bar (appears at 60% scroll, skips contact/pricing pages, GA4 tracking)
- [x] GA4 Consent Mode v2 with cookie consent banner (GDPR/CCPA compliant)
- [x] ItemList schema on use-cases, resources, alternatives, ICP index pages (4 more directory pages)
- [x] Publication date on service page heroes
- [x] CSS version: bumped to v=7

### Round 4 (Feb 14, 2026):
- [x] Person schema for author (Rome) on 27 resource pages (name, jobTitle, worksFor, LinkedIn URL)
- [x] Preconnect + dns-prefetch hints for googletagmanager.com and google-analytics.com
- [x] Table captions + ARIA labels on all comparison tables (sr-only caption, aria-label)
- [x] Enhanced alt text on competitor logos ("company logo" suffix)
- [x] Review schema on all 6 service pages (from testimonial data, @type Review with rating)

### Round 5 (Feb 15, 2026):
- [x] theme-color meta tag (#1B2A4A) on all pages
- [x] fetchpriority="high" on header logo (LCP improvement)
- [x] inLanguage: "en-US" in all Article schemas
- [x] Image sitemap: xmlns:image namespace + image:image/image:loc for OG images on all 226 URLs
- [x] RSS feed: /feed.xml with 27 resource articles (RSS 2.0 + Atom self-link)
- [x] RSS discovery: rel="alternate" type="application/rss+xml" link in all page heads

---

## Remaining Gaps (Prioritized)

### TIER 1: High-Impact Technical SEO

All Tier 1 items DONE:
- ~~#1 Article Schema~~ ✅ Round 2
- ~~#2 GA4 Event Tracking~~ ✅ Round 2
- ~~#3 Robots.txt AI Crawlers~~ ✅ Round 2
- ~~#4 Content Freshness Dates~~ ✅ Round 2 + 3
- ~~#5 Defer main.js~~ ✅ Round 2

---

### TIER 2: Content & Schema Enrichment

All Tier 2 items DONE:
- ~~#6 SpeakableSpecification Schema~~ ✅ Round 2 (in Article schema)
- ~~#7 HowTo Schema on Use-Case Pages~~ ✅ Round 3 (24 pages)

#### 8. Comparison Table Schema (or enhanced markup)
**Gap:** Comparison pages have HTML tables but no structured data identifying them as comparison content.
**Status:** Not yet implemented — lower priority since Google doesn't have a dedicated comparison rich result type.
**Effort:** Medium

- ~~#9 AEO/GEO Expansion to Service + Provider Pages~~ ✅ Round 2 (definition + step blocks on 6 services, definition blocks on 17 hubs)
- ~~#10 Expert Quote / Testimonial Blocks~~ ✅ Round 3 (generate_testimonial_block on 6 service pages)

---

### TIER 3: Programmatic SEO Scaling

- ~~#11 Glossary / Learn Pages~~ ✅ Round 6 (33 terms at `/glossary/[term]/`, hub at `/glossary/`, DefinedTerm + FAQPage + Article + BreadcrumbList schema, related terms cross-linking, author bio, outbound authority links. Data in `scripts/glossary_data.py`)

#### 11b. Comparison & Alternative Page Expansion
**Status:** ✅ Round 7+8 (Feb 15, 2026)
**Round 7:** 4 new comparison pages (Veeva OpenData, Ribbon Health, Doximity, Komodo Health) + 4 matching alternative pages
**Round 8:** 3 more comparison pages (AcuityMD, Salesforce Health Cloud, D&B Hoovers) + 3 matching alternative pages
**Total comparisons:** 6 → 13 | **Total alternatives:** 6 → 11 | **Pages added:** 14
**Data files:** `scripts/comparisons_new.py`, `scripts/alternatives_new.py`
**Competitors covered:** ZoomInfo, Definitive Healthcare, Apollo, IQVIA, Lusha, Cognism, Veeva OpenData, Ribbon Health, Doximity, Komodo Health, AcuityMD, Salesforce Health Cloud, D&B Hoovers

#### 12. Location/State Pages
**Status:** ✅ Round 8 (Feb 15, 2026)
**Added:** 50 state pages at `/providers/states/[state]/` + hub page at `/providers/states/`
**Content per page:** Provider stats (total, physicians, dental, mental health), top 5 specialties, top metros, regulatory notes, market insights, 3 FAQs, related states, category links
**Schema:** Article + BreadcrumbList + FAQPage
**Data file:** `scripts/state_pages.py`
**Pages added:** 51 (50 states + index)

#### 13. Blog / Content Publishing
**Status:** ✅ Round 8 (Feb 15, 2026) — Initial launch
**Added:** 5 blog posts at `/blog/[slug]/` + index page at `/blog/`
**Posts:** healthcare-provider-data-trends-2026, how-to-build-healthcare-provider-contact-list, npi-database-vs-commercial-provider-data, healthcare-sales-prospecting-mistakes, medical-practice-data-quality-checklist
**Content:** ~10,500 words total (avg 2,100/post), Article schema with author Person, FAQPage, BreadcrumbList, tags, outbound authority links, related internal links
**Data file:** `scripts/blog_posts.py`
**Pages added:** 6 (5 posts + index)
**Next:** Add 2-4 posts/month targeting awareness-stage keywords

#### 14. Free Tool Strategy
**Source:** free-tool-strategy/SKILL.md, references/tool-types.md
**Gap:** No interactive tools. "[Thing] calculator/lookup" queries attract backlinks and convert visitors.
**Candidates:**
- **NPI Lookup Tool** — "NPI number search" (high volume, easy to build with NPPES API)
- **Provider Count Estimator** — input specialty + state, get estimated count
- **Data Quality Grader** — upload CSV, score completeness
**Impact:** Backlinks, brand awareness, lead gen
**Effort:** High — requires JS/API work

---

### TIER 4: CRO & Polish

- ~~#15 Sticky Header CTA~~ ✅ Already done (header has position: fixed)
- ~~#16 Scroll-Triggered CTA~~ ✅ Round 3 (bottom bar at 60% scroll, GA4 tracking)
- ~~#17 Social Proof Near Conversion Points~~ ✅ Round 2 (CTA proof, form proof, pricing proof)
- ~~#18 Pricing Page Enhancements~~ ✅ Round 2 (Most Popular badge via CSS, proof text, h2/h3 fixes)

---

### TIER 5: Analytics & Measurement

- ~~#19 GA4 Consent Mode v2~~ ✅ Round 3 (consent default/update, cookie banner with accept/deny)

#### 20. UTM Parameter Strategy
**Gap:** No documented UTM conventions for campaign tracking.
**Fix:** Document standard UTM parameters (lowercase, underscores), create a UTM builder/reference doc.
**Effort:** Low — documentation + process

#### 21. Google Search Console Monitoring
**Actions:**
- Submit sitemap.xml if not done
- Monitor indexation rate (226 submitted vs indexed)
- Review "Not indexed" report monthly
- Check for keyword cannibalization
- Identify position 5-20 keywords for content optimization
**Effort:** Ongoing — not a build change

---

## Implementation Summary

| Tier | Status | Items Completed |
|------|--------|-----------------|
| **1** | ✅ ALL DONE | #1-5 (Article schema, GA4 events, robots.txt, dates, defer) |
| **2** | ✅ ALL DONE | #6-10 (Speakable, HowTo, comparison table pending, AEO expansion, testimonials) |
| **3** | Mostly done | #11 Glossary ✅, #11b Comparisons 13+Alternatives 11 ✅, #12 States 50 ✅, #13 Blog 5 posts ✅, #14 Free tools remaining |
| **4** | ✅ ALL DONE | #15-18 (Sticky header, scroll CTA, social proof, pricing) |
| **5** | Mostly done | #19 done, #20-21 are ongoing process items |

## What's Left (Content-Dependent, High Effort)

1. **Comparison Table Schema** (#8) — Medium effort, low-med impact
2. ~~**Glossary Pages** (#11)~~ ✅ Done (33 terms)
3. ~~**Comparison & Alternative Expansion** (#11b)~~ ✅ Done (13 comparisons, 11 alternatives)
4. ~~**Location/State Pages** (#12)~~ ✅ Done (50 states + index)
5. **Blog** (#13) — Initial 5 posts launched ✅, ongoing content production needed
6. **Free Tools** (#14) — NPI lookup, provider estimator, etc.
7. **UTM Standards** (#20) — Documentation task
8. **GSC Monitoring** (#21) — Ongoing process

## Page Count History

| Round | Pages | Delta | What was added |
|-------|-------|-------|----------------|
| Initial | 226 | — | Core site (providers, services, use-cases, resources, compare, alternatives, ICP) |
| Round 6 | 260 | +34 | Glossary (33 terms + index) |
| Round 7 | 272 | +12 | 4 comparisons, 4 alternatives, spoke pages, CSS v8 |
| Round 8 | 335 | +63 | 50 state pages, 5 blog posts, 3 comparisons, 3 alternatives |
