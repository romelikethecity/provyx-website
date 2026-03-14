---
phase: 02-remaining-ctr-and-service-page-depth
plan: 01
subsystem: seo
tags: [title-tags, meta-descriptions, ctr-optimization, gsc-queries]

requires:
  - phase: 01-high-impact-ctr-and-content-depth
    provides: "CTR optimization pattern (keyword-first titles, outcome metas)"
provides:
  - "All 6 remaining CTR pages (100+ impressions) have keyword-first titles and GSC-aligned metas"
affects: [03-email-list-pages, 04-content-gap-pages]

tech-stack:
  added: []
  patterns: ["keyword-first title pattern extended to all CTR pages"]

key-files:
  created: []
  modified:
    - scripts/build.py
    - services/practice-location-data/index.html
    - resources/healthcare-data-providers-small-teams/index.html
    - compare/provyx-vs-lusha/index.html
    - providers/oral-pathologists/index.html
    - resources/nppes-vs-commercial-provider-data/index.html
    - alternatives/zoominfo-alternative/index.html

key-decisions:
  - "Kept Oral Pathologists generated title (template pattern) and focused meta on email list angle matching GSC query"
  - "Led NPPES page with accuracy angle matching top GSC query intent rather than generic comparison framing"
  - "Dropped period in vs. for Provyx vs Lusha to match natural search query format"

patterns-established:
  - "GSC query alignment: title leads with exact top query, meta leads with what reader gets"

requirements-completed: [CTR-05, CTR-06, CTR-07, CTR-08, CTR-09, CTR-10]

duration: 3min
completed: 2026-03-14
---

# Phase 02 Plan 01: Remaining CTR Pages Summary

**Keyword-first title/meta rewrites for 6 pages (935 combined impressions) aligned to their top GSC search queries**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-14T14:33:25Z
- **Completed:** 2026-03-14T14:36:30Z
- **Tasks:** 1
- **Files modified:** 7

## Accomplishments
- Rewrote titles, meta descriptions, and H1 tags for all 6 remaining CTR pages
- Titles are keyword-first at 38-52 chars, meta descriptions are 143-158 chars
- H1 tags aligned with new titles across all page types (services, resources, compare, alternatives, providers)
- Site builds successfully with 381 pages

## Task Commits

Each task was committed atomically:

1. **Task 1: Rewrite titles, metas, and H1s for 6 CTR pages** - `b56ebe9` (feat)

## Files Created/Modified
- `scripts/build.py` - Updated title, meta_description, h1/subtitle/hero_h1/hero_headline/page_title fields for 6 pages
- `services/practice-location-data/index.html` - Rebuilt with "Practice Location Data for Healthcare Providers" title
- `resources/healthcare-data-providers-small-teams/index.html` - Rebuilt with "Healthcare Data Providers for Small Sales Teams" title
- `compare/provyx-vs-lusha/index.html` - Rebuilt with "Provyx vs Lusha: Healthcare Provider Data Compared" title
- `providers/oral-pathologists/index.html` - Rebuilt with updated email list meta description
- `resources/nppes-vs-commercial-provider-data/index.html` - Rebuilt with "NPPES Data Accuracy vs Commercial Provider Databases" title
- `alternatives/zoominfo-alternative/index.html` - Rebuilt with "ZoomInfo Alternative for Healthcare Provider Data" title

## Decisions Made
- Kept Oral Pathologists generated title ("Oral Pathologists Data & Contact Lists") since the template pattern is already keyword-appropriate; focused the meta on "email list" angle matching the top GSC query
- Led NPPES page with "accuracy" angle matching top GSC query "nppes database accuracy" rather than generic comparison framing
- Dropped period in "vs." for Provyx vs Lusha to match natural search query format

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- All CTR optimization work complete across both phases (Phase 1 high-impact + Phase 2 remaining)
- Ready for service page depth work (02-02) or email list pages (Phase 3)

---
*Phase: 02-remaining-ctr-and-service-page-depth*
*Completed: 2026-03-14*

## Self-Check: PASSED
