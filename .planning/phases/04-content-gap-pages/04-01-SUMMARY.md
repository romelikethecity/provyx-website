---
phase: 04-content-gap-pages
plan: 01
subsystem: content
tags: [blog, seo, definitive-healthcare, nppes, pricing, data-quality]

requires:
  - phase: none
    provides: n/a
provides:
  - DH pricing guide blog post targeting "definitive healthcare pricing" queries
  - NPPES accuracy guide blog post targeting "NPPES data accuracy" queries
affects: [04-content-gap-pages]

tech-stack:
  added: []
  patterns: [blog post data dict schema in blog_posts.py]

key-files:
  created:
    - blog/definitive-healthcare-pricing-guide/index.html
    - blog/nppes-database-accuracy-guide/index.html
  modified:
    - scripts/blog_posts.py
    - sitemap.xml
    - blog/index.html

key-decisions:
  - "Sourced DH pricing from G2/Capterra reviews rather than fabricating specific numbers"
  - "Structured NPPES guide around 6 specific accuracy gaps with concrete examples"

patterns-established:
  - "Content gap blog posts: keyword-first titles, sourced claims, Provyx positioning via internal links"

requirements-completed: [GAP-01, GAP-02]

duration: 4min
completed: 2026-03-14
---

# Phase 4 Plan 1: Content Gap Blog Posts Summary

**Two SEO blog posts targeting high-intent queries: DH pricing guide (1,622 words, sourced tier breakdowns) and NPPES accuracy guide (1,835 words, 6 specific data gaps)**

## Performance

- **Duration:** 4 min
- **Started:** 2026-03-14T15:34:04Z
- **Completed:** 2026-03-14T15:38:30Z
- **Tasks:** 2
- **Files modified:** 5

## Accomplishments
- DH pricing guide covers tiers, contract structure, negotiation tips, and Provyx positioning as lower-cost alternative for contact-data-only buyers
- NPPES accuracy guide details 6 specific gaps (stale addresses, billing/practice mismatch, missing emails, deactivated NPIs, broad taxonomy, no practice context) with concrete examples
- Both pages have Article + FAQPage + BreadcrumbList schema, canonical URLs, OG/Twitter tags, 2+ outbound links, 3+ related internal links

## Task Commits

1. **Task 1: Add blog post data dicts** - `9ab803c` (feat)
2. **Task 2: Build and verify pages** - `9a438e8` (feat)

## Files Created/Modified
- `scripts/blog_posts.py` - Two new blog post data dicts appended to BLOG_POSTS list
- `blog/definitive-healthcare-pricing-guide/index.html` - DH pricing guide page (1,622 words)
- `blog/nppes-database-accuracy-guide/index.html` - NPPES accuracy guide page (1,835 words)
- `sitemap.xml` - Both new URLs added
- `blog/index.html` - Blog index updated with both posts

## Decisions Made
- Sourced all DH pricing claims from G2/Capterra reviews and industry positioning rather than fabricating specific dollar amounts
- Structured NPPES guide around 6 concrete accuracy gaps with real-world examples rather than generic "data quality" talking points
- Fixed NPPES title from 45 to 55 chars to meet H1 minimum (46-60 char requirement)

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] NPPES title too short for H1 requirement**
- **Found during:** Task 1 (verification)
- **Issue:** Title "NPPES Database Accuracy: Known Gaps and Fixes" was 45 chars, below 46-char H1 minimum
- **Fix:** Changed to "NPPES Database Accuracy: Known Gaps and How to Fix Them" (55 chars)
- **Files modified:** scripts/blog_posts.py
- **Verification:** Python check confirmed 55 chars in range
- **Committed in:** 9ab803c (Task 1 commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Minor title length fix. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Both content gap blog posts are built and ready for deployment
- Phase 04 plans 02 and 03 can proceed independently

---
*Phase: 04-content-gap-pages*
*Completed: 2026-03-14*
