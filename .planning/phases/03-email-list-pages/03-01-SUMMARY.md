---
phase: 03-email-list-pages
plan: 01
subsystem: seo
tags: [email-list, resource-pages, programmatic-seo, healthcare-data]

requires:
  - phase: 02-remaining-ctr
    provides: existing email list page pattern and build.py RESOURCES structure
provides:
  - 5 new email list resource pages (psychiatrists, therapists, nursing-homes, retirement-communities, pediatric-dentists)
  - 1 renamed/optimized acupuncturists page (singular to plural slug)
affects: [03-email-list-pages]

tech-stack:
  added: []
  patterns: [facility-level resource page pattern (nursing homes, retirement communities)]

key-files:
  created:
    - resources/psychiatrists-email-list/index.html
    - resources/therapists-email-list/index.html
    - resources/nursing-homes-contact-database/index.html
    - resources/retirement-communities-email-list/index.html
    - resources/pediatric-dentists-email-list/index.html
  modified:
    - scripts/build.py
    - resources/acupuncturists-email-list/index.html
    - resources/index.html
    - sitemap.xml
    - feed.xml

key-decisions:
  - "Renamed acupuncturist-email-list to acupuncturists-email-list (plural) to match search query format"
  - "Used facility-level data structure for nursing homes and retirement communities instead of provider-level pattern"

patterns-established:
  - "Facility resource pages: sections focus on facility data (bed count, star rating, ownership) rather than individual NPI data"

requirements-completed: [EMAIL-01, EMAIL-02, EMAIL-03, EMAIL-04, EMAIL-05, EMAIL-06]

duration: 7min
completed: 2026-03-14
---

# Phase 3 Plan 1: Email List Pages Wave 1 Summary

**6 email list resource pages covering psychiatrists, acupuncturists, therapists, nursing homes, retirement communities, and pediatric dentists with 500+ words each and full SEO markup**

## Performance

- **Duration:** 7 min
- **Started:** 2026-03-14T14:56:37Z
- **Completed:** 2026-03-14T15:03:37Z
- **Tasks:** 2
- **Files modified:** 10

## Accomplishments
- Added 5 new email list resource page data dicts to build.py RESOURCES list
- Renamed existing acupuncturist-email-list to plural form matching search queries
- All 6 pages built with FAQPage schema, BreadcrumbList, canonical URLs, and meta descriptions within 120-158 chars
- All 6 URLs present in sitemap.xml

## Task Commits

Each task was committed atomically:

1. **Task 1: Add 6 new email list page data dicts to RESOURCES list** - `172579e` (feat)
2. **Task 2: Build site and verify new pages render** - `86adac7` (feat)

## Files Created/Modified
- `scripts/build.py` - Added 5 new resource page data dicts, renamed acupuncturist slug to plural
- `resources/psychiatrists-email-list/index.html` - New page targeting 37K practicing psychiatrists
- `resources/acupuncturists-email-list/index.html` - Renamed from singular, updated title/meta
- `resources/therapists-email-list/index.html` - New page covering 600K+ licensed therapists (LPC, LCSW, LMFT, PsyD)
- `resources/nursing-homes-contact-database/index.html` - New facility-level page for 15K CMS-certified nursing homes
- `resources/retirement-communities-email-list/index.html` - New page covering ILF, ALF, CCRC, and 55+ communities
- `resources/pediatric-dentists-email-list/index.html` - New page targeting 7,500 board-certified pediatric dental specialists
- `resources/index.html` - Updated resource listing
- `sitemap.xml` - All 6 new URLs added
- `feed.xml` - Updated with new pages

## Decisions Made
- Renamed acupuncturist-email-list to acupuncturists-email-list (plural) to match the actual search query "acupuncturists email list" rather than creating a duplicate page
- Used facility-level framing for nursing homes and retirement communities (administrator/ED contacts, bed counts, star ratings, ownership chains) instead of individual-provider NPI framing

## Deviations from Plan

### Auto-fixed Issues

**1. [Rule 1 - Bug] Fixed meta descriptions exceeding 158 char limit**
- **Found during:** Task 2 (Build and verify)
- **Issue:** 4 of 6 meta descriptions exceeded the 158 character maximum specified in CLAUDE.md
- **Fix:** Shortened all meta descriptions to fit within 120-158 char range
- **Files modified:** scripts/build.py
- **Verification:** Rebuilt site, confirmed all 6 meta descriptions between 120-158 chars
- **Committed in:** 86adac7 (Task 2 commit)

---

**Total deviations:** 1 auto-fixed (1 bug)
**Impact on plan:** Minor fix to meet SEO requirements. No scope creep.

## Issues Encountered
None

## User Setup Required
None - no external service configuration required.

## Next Phase Readiness
- 6 email list pages live and indexed in sitemap
- Pattern established for remaining email list pages in plans 03-02 and 03-03
- Facility-level page pattern (nursing homes, retirement communities) available for future senior care pages

---
*Phase: 03-email-list-pages*
*Completed: 2026-03-14*
