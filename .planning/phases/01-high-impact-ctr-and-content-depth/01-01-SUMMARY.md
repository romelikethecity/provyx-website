---
phase: 01-high-impact-ctr-and-content-depth
plan: 01
subsystem: seo
tags: [meta-tags, titles, ctr-optimization, serp]

# Dependency graph
requires: []
provides:
  - CTR-optimized title tags and meta descriptions for 4 highest-impression pages
affects: []

# Tech tracking
tech-stack:
  added: []
  patterns:
    - "Title format: keyword-first, outcome-oriented, 50-60 chars"
    - "Meta format: value-proposition-first, specific deliverables, 120-158 chars"

key-files:
  created: []
  modified:
    - scripts/build.py

key-decisions:
  - "Vendor Comparison: led with '8 Providers Ranked' to signal depth"
  - "DH Alternative: led with cost angle ('Same Data, Lower Cost') since top GSC queries mention cost"
  - "VAC Guide: reframed from 'Winning' to 'Guide for Medical Device Vendors' matching search intent"
  - "Provyx vs DH: added 'Pricing and Data Compared' hook, dropped period from 'vs.'"

patterns-established:
  - "Title tags lead with keyword, end with outcome hook"
  - "Meta descriptions lead with what the reader gets, not what the page is"

requirements-completed: [CTR-01, CTR-02, CTR-03, CTR-04]

# Metrics
duration: 2min
completed: 2026-03-13
---

# Phase 1 Plan 1: CTR-Optimized Titles and Metas Summary

**Rewrote title tags and meta descriptions on 4 highest-impression pages (3,200+ combined GSC impressions) to match top search queries and lead with outcomes**

## Performance

- **Duration:** 2 min
- **Started:** 2026-03-14T06:14:01Z
- **Completed:** 2026-03-14T06:16:30Z
- **Tasks:** 2
- **Files modified:** 1 (scripts/build.py) + 9 HTML output files

## Accomplishments
- All 4 title tags rewritten to 50-60 chars, keyword-first, outcome-oriented
- All 4 meta descriptions rewritten to 120-158 chars, value-proposition-first
- H1 tags updated to match new titles on all 4 pages
- Site rebuilt (381 pages) with updated HTML verified

## Task Commits

Each task was committed atomically:

1. **Task 1: Rewrite titles and metas for all 4 high-impression pages** - `37fb1ad` (feat)
2. **Task 2: Rebuild site and verify updated pages** - `268772d` (chore)

## Files Created/Modified
- `scripts/build.py` - Updated title, meta_description, h1/hero_h1/page_title fields for 4 pages

## Changes by Page

| Page | Old Title | New Title | Title Chars |
|------|-----------|-----------|-------------|
| Vendor Comparison | Healthcare Data Vendor Comparison 2026 | Healthcare Data Vendors Compared: 8 Providers Ranked | 52 |
| DH Alternative | Best Definitive Healthcare Alternative for Data | Definitive Healthcare Alternative: Same Data, Lower Cost | 57 |
| VAC Guide | Winning the Value Analysis Committee: A Vendor Guide | Value Analysis Committee Guide for Medical Device Vendors | 58 |
| Provyx vs DH | Provyx vs. Definitive Healthcare: Provider Data Platforms Compared | Provyx vs Definitive Healthcare: Pricing and Data Compared | 59 |

## Decisions Made
- Led DH Alternative with cost angle since top GSC queries ("definitive healthcare subscription cost") indicate price-sensitive intent
- Dropped period from "vs." in Provyx vs DH title to save a character and match informal search patterns
- VAC Guide reframed from "Winning" (aspirational) to "Guide for Medical Device Vendors" (matches informational search intent)
- Vendor Comparison title added "8 Providers Ranked" to signal completeness and comparison depth

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None.

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Pages ready for deployment via GitHub Pages
- Monitor GSC CTR changes over next 2-4 weeks to measure impact
- Plan 01-02 (content depth) can proceed independently

---
*Phase: 01-high-impact-ctr-and-content-depth*
*Completed: 2026-03-13*
