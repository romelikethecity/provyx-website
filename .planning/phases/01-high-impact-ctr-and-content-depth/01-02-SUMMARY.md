---
phase: 01-high-impact-ctr-and-content-depth
plan: 02
subsystem: seo
tags: [comparison-table, faq-schema, pricing, structured-data, html-table]

requires:
  - phase: 01-high-impact-ctr-and-content-depth
    provides: Updated titles and meta descriptions for vendor comparison and DH alternative pages
provides:
  - Structured comparison table on vendor comparison page (8 vendors, 6 columns)
  - FAQPage schema with 6 FAQs on vendor comparison page
  - Pricing comparison table on DH alternative page (DH vs Provyx, 6 rows)
  - Conditional pricing_comparison section support in build_alternative_page template
affects: []

tech-stack:
  added: []
  patterns:
    - comparison-table HTML class for structured vendor tables
    - Conditional section rendering in alternative page template via .get() check

key-files:
  created: []
  modified:
    - scripts/build.py

key-decisions:
  - "Added pricing comparison as new template section rather than appending to why_switch_body for cleaner separation"
  - "Used conditional rendering in template so other alternative pages without pricing comparison are unaffected"
  - "Replaced 4 generic FAQs with 6 GSC-query-targeted FAQs for better search alignment"

patterns-established:
  - "comparison-table class: use for any side-by-side vendor/pricing table across the site"
  - "Optional named sections in alternative template: use .get() guard for sections not all pages have"

requirements-completed: [DEPTH-01, DEPTH-02]

duration: 3min
completed: 2026-03-14
---

# Phase 01 Plan 02: Content Depth Summary

**Structured comparison table + 6 targeted FAQs on vendor comparison page, pricing breakdown table on DH alternative page**

## Performance

- **Duration:** 3 min
- **Started:** 2026-03-14T06:18:26Z
- **Completed:** 2026-03-14T06:21:43Z
- **Tasks:** 3
- **Files modified:** 3

## Accomplishments
- Added at-a-glance HTML comparison table with 8 vendors across coverage, pricing, commitment, healthcare-specific, and best-for columns
- Replaced 4 generic FAQs with 6 FAQs targeting actual GSC queries (pricing comparison, small teams, NPI verification, accuracy, features, free NPI)
- Added side-by-side pricing comparison table to DH alternative page covering entry price, full platform, CRM integration, contract terms, per-seat licensing, and data export
- Added conditional section rendering in alternative page template for pricing comparison

## Task Commits

Each task was committed atomically:

1. **Task 1: Add comparison table and FAQ schema to vendor comparison page** - `722f652` (feat)
2. **Task 2: Add pricing comparison section to DH alternative page** - `e59f90b` (feat)
3. **Task 3: Rebuild site and verify both pages** - `7d8eca3` (chore)

## Files Created/Modified
- `scripts/build.py` - Added comparison table section, 6 FAQs to vendor comparison data dict; added pricing_comparison fields to DH alternative data dict; added conditional pricing comparison section to build_alternative_page template
- `resources/healthcare-data-vendor-comparison/index.html` - Rebuilt with comparison table + FAQPage schema
- `alternatives/definitive-healthcare-alternative/index.html` - Rebuilt with pricing comparison section

## Decisions Made
- Added pricing comparison as a new named section in the alternative page template rather than appending to why_switch_body, keeping content sections cleanly separated
- Used conditional rendering so the pricing comparison section only appears on alternative pages that define it
- Replaced all 4 existing FAQs with 6 new ones targeting GSC queries rather than appending, since the old questions were generic and the new ones better match search intent

## Deviations from Plan

None - plan executed exactly as written.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- Phase 01 complete (both plans executed)
- Vendor comparison page has structured table content for rich result eligibility
- DH alternative page directly addresses "definitive healthcare subscription cost" query with pricing table
- Ready to proceed to Phase 02

---
*Phase: 01-high-impact-ctr-and-content-depth*
*Completed: 2026-03-14*
