---
phase: 02-remaining-ctr-and-service-page-depth
verified: 2026-03-14T15:10:00Z
status: passed
score: 8/8 must-haves verified
---

# Phase 2: Remaining CTR and Service Page Depth Verification Report

**Phase Goal:** Every page with 100+ impressions has an optimized title and meta, and service pages have enough content depth to rank for their target queries
**Verified:** 2026-03-14T15:10:00Z
**Status:** passed
**Re-verification:** No -- initial verification

## Goal Achievement

### Observable Truths

| # | Truth | Status | Evidence |
|---|-------|--------|----------|
| 1 | All 6 CTR pages have keyword-first titles under 60 chars matching top GSC queries | VERIFIED | Titles are 38-52 chars (base), all keyword-first: "Practice Location Data...", "Healthcare Data Providers...", "Provyx vs Lusha...", "Oral Pathologists...", "NPPES Data Accuracy...", "ZoomInfo Alternative..." |
| 2 | All 6 CTR pages have meta descriptions 120-158 chars | VERIFIED | Metas range 143-158 chars across all 6 pages |
| 3 | H1 tags updated to match new titles | VERIFIED | H1 matches base title on all 6 pages (verified via HTML extraction) |
| 4 | Site builds successfully with all pages reflecting updated metas | VERIFIED | 381 pages built, all 9 phase pages exist |
| 5 | Technology detection page shows EHR install base examples with sales workflows | VERIFIED | Contains eClinicalWorks targeting, dermatology displacement, pain management examples, ABM workflow section. 2,678 words |
| 6 | Practice firmographics service page has expanded data field descriptions and use-case examples | VERIFIED | Provider headcount, revenue range, ownership classification, years in operation, segmentation examples all present. 2,609 words |
| 7 | Healthcare provider firmographic data resource page has expanded content with practical field descriptions | VERIFIED | HTML reference table with Field Name / What It Tells You / Source Methodology / Sales Application columns. Territory planning, TAM validation, PE due diligence use cases. 3,922 words |
| 8 | All three depth pages meet 1,200+ word minimum | VERIFIED | Tech detection: 2,678. Firmographics svc: 2,609. Firmographics resource: 3,922 |

**Score:** 8/8 truths verified

### Required Artifacts

| Artifact | Expected | Status | Details |
|----------|----------|--------|---------|
| `scripts/build.py` | Updated titles/metas for 6 CTR pages + expanded content for 3 depth pages | VERIFIED | Commits b56ebe9, d20f044, 4a9aed9 modify build.py |
| `services/practice-location-data/index.html` | Rebuilt with keyword-first title | VERIFIED | Title: "Practice Location Data for Healthcare Providers" (47 chars) |
| `resources/healthcare-data-providers-small-teams/index.html` | Rebuilt with keyword-first title | VERIFIED | Title: "Healthcare Data Providers for Small Sales Teams" (47 chars) |
| `compare/provyx-vs-lusha/index.html` | Rebuilt with keyword-first title | VERIFIED | Title: "Provyx vs Lusha: Healthcare Provider Data Compared" (50 chars) |
| `providers/oral-pathologists/index.html` | Rebuilt with email list meta | VERIFIED | Meta leads with "Oral pathologist email list and contact data" (155 chars) |
| `resources/nppes-vs-commercial-provider-data/index.html` | Rebuilt with accuracy-angle title | VERIFIED | Title: "NPPES Data Accuracy vs Commercial Provider Databases" (52 chars) |
| `alternatives/zoominfo-alternative/index.html` | Rebuilt with keyword-first title | VERIFIED | Title: "ZoomInfo Alternative for Healthcare Provider Data" (49 chars) |
| `services/technology-detection/index.html` | EHR install base examples | VERIFIED | eClinicalWorks, ABM, install base, practice size all present |
| `services/practice-firmographics/index.html` | Expanded firmographic content | VERIFIED | Data fields reference + segmentation examples |
| `resources/healthcare-provider-firmographic-data/index.html` | Expanded with field reference table | VERIFIED | HTML table with 4-column field reference |

### Key Link Verification

| From | To | Via | Status | Details |
|------|----|-----|--------|---------|
| `services/technology-detection/index.html` | `/services/practice-firmographics/` | Internal link in content | VERIFIED | "practice-firmographics" found in page |
| `services/practice-firmographics/index.html` | `/resources/healthcare-provider-firmographic-data/` | Internal link in content | VERIFIED | Full path found in page |
| `resources/healthcare-provider-firmographic-data/index.html` | `/services/practice-firmographics/` | Internal link in content | VERIFIED | Full path found in page |
| `scripts/build.py` | HTML output files | Build generates pages | VERIFIED | Build produces all 9 pages, sitemap includes all |

### Requirements Coverage

| Requirement | Source Plan | Description | Status | Evidence |
|-------------|------------|-------------|--------|----------|
| CTR-05 | 02-01 | Title and meta on `/services/practice-location-data/` | SATISFIED | "Practice Location Data for Healthcare Providers" title, 158-char meta |
| CTR-06 | 02-01 | Title and meta on `/resources/healthcare-data-providers-small-teams/` | SATISFIED | "Healthcare Data Providers for Small Sales Teams" title, 151-char meta |
| CTR-07 | 02-01 | Title and meta on `/compare/provyx-vs-lusha/` | SATISFIED | "Provyx vs Lusha: Healthcare Provider Data Compared" title, 156-char meta |
| CTR-08 | 02-01 | Title and meta on `/providers/oral-pathologists/` | SATISFIED | Email list meta, template title retained as keyword-appropriate |
| CTR-09 | 02-01 | Title and meta on `/resources/nppes-vs-commercial-provider-data/` | SATISFIED | "NPPES Data Accuracy vs Commercial Provider Databases" title, 143-char meta |
| CTR-10 | 02-01 | Title and meta on `/alternatives/zoominfo-alternative/` | SATISFIED | "ZoomInfo Alternative for Healthcare Provider Data" title, 151-char meta |
| DEPTH-04 | 02-02 | Add EHR install base examples to `/services/technology-detection/` | SATISFIED | eClinicalWorks, dermatology, pain management examples + ABM workflow. 2,678 words |
| DEPTH-05 | 02-02 | Expand firmographic content on both firmographic pages | SATISFIED | Data field reference, segmentation examples, HTML field table, use cases. 2,609 and 3,922 words |

No orphaned requirements. REQUIREMENTS.md maps CTR-05 through CTR-10 and DEPTH-04/DEPTH-05 to Phase 2, and all are covered by Plans 01 and 02.

### SEO Checklist Compliance

All 9 pages pass the CLAUDE.md SEO checklist:
- CSS version parameter (styles.min.css?v=9)
- Canonical URL (getprovyx.com)
- Open Graph tags (og:title, og:description)
- Twitter Card tags
- BreadcrumbList schema
- FAQPage schema
- H1 present

### Anti-Patterns Found

| File | Line | Pattern | Severity | Impact |
|------|------|---------|----------|--------|
| None found | - | - | - | - |

The only "placeholder" hit in build.py is a form textarea `placeholder` attribute -- standard HTML, not a code placeholder.

### Pre-existing Issue (Not a Phase 2 Gap)

The `resources/healthcare-provider-firmographic-data/` page has a title at 68 chars (exceeds the 50-60 char guideline) and a meta description at 174 chars (exceeds the 158 char max). However, this page's title and meta were not in scope for Phase 2 -- Plan 02 only expanded content depth. This is a pre-existing condition that predates Phase 2 work. It may be worth addressing in a future optimization pass.

### Human Verification Required

None. All verification was performed programmatically against HTML output. Title/meta content quality (whether the rewrites actually match searcher intent better) will be validated by GSC CTR changes over time, but the structural requirements are all met.

### Gaps Summary

No gaps found. All 8 must-have truths verified, all 8 requirements satisfied, all key links wired, all artifacts substantive.

---

_Verified: 2026-03-14T15:10:00Z_
_Verifier: Claude (gsd-verifier)_
