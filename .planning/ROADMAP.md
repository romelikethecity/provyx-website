# Roadmap: Provyx Website

## Overview

Turn 7,500 monthly impressions at 0.39% CTR into clicks by optimizing existing high-impression pages first, then expanding coverage with new pages targeting proven search demand. Phases ordered by impression volume -- fix the pages Google already shows before building new ones.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions (marked with INSERTED)

Decimal phases appear between their surrounding integers in numeric order.

- [x] **Phase 1: High-Impact CTR and Content Depth** - Rewrite titles/metas and deepen content on the 4 highest-impression pages (3,200+ impressions combined) (completed 2026-03-14)
- [x] **Phase 2: Remaining CTR and Service Page Depth** - Optimize remaining 6 CTR pages and strengthen service page content (completed 2026-03-14)
- [ ] **Phase 3: Email List Pages** - Create 11 new specialty email list pages and rewrite existing ones to match query intent
- [ ] **Phase 4: Content Gap Pages** - Create 5 new blog and use-case pages targeting unserved search queries

## Phase Details

### Phase 1: High-Impact CTR and Content Depth
**Goal**: Searchers seeing the top 4 pages in Google results get compelling titles, accurate descriptions, and deeper content that earns the click
**Depends on**: Nothing (first phase)
**Requirements**: CTR-01, CTR-02, CTR-03, CTR-04, DEPTH-01, DEPTH-02
**Success Criteria** (what must be TRUE):
  1. Vendor comparison page (/resources/healthcare-data-vendor-comparison/) has a rewritten title under 60 chars with primary keyword first, meta description 120-158 chars with clear value proposition, and a new FAQ schema + comparison table section
  2. DH alternative page (/alternatives/definitive-healthcare-alternative/) has rewritten title/meta plus a new pricing comparison section showing DH vs Provyx costs
  3. VAC guide and Provyx-vs-DH comparison pages have rewritten titles and metas that match their top-ranking queries
  4. All 4 pages pass the SEO checklist in CLAUDE.md (title 50-60 chars, meta 120-158 chars, schema valid, 2+ outbound links)
**Plans:** 2/2 plans complete

Plans:
- [x] 01-01-PLAN.md — Rewrite titles and meta descriptions on all 4 high-impression pages
- [x] 01-02-PLAN.md — Add comparison table + FAQ schema to vendor comparison page and pricing comparison section to DH alternative page

### Phase 2: Remaining CTR and Service Page Depth
**Goal**: Every page with 100+ impressions has an optimized title and meta, and service pages have enough content depth to rank for their target queries
**Depends on**: Phase 1
**Requirements**: CTR-05, CTR-06, CTR-07, CTR-08, CTR-09, CTR-10, DEPTH-04, DEPTH-05
**Success Criteria** (what must be TRUE):
  1. All 6 remaining CTR pages (practice-location-data, small-teams resource, provyx-vs-lusha, oral-pathologists, NPPES resource, zoominfo-alternative) have rewritten titles and metas matching their top GSC queries
  2. Technology detection page includes EHR install base examples showing how the data applies to real sales workflows
  3. Firmographic content on both /services/practice-firmographics/ and /resources/healthcare-provider-firmographic-data/ is expanded with specific data field descriptions and use-case examples
  4. All updated pages pass the SEO checklist in CLAUDE.md
**Plans:** 2/2 plans complete

Plans:
- [ ] 02-01-PLAN.md — Rewrite titles, metas, and H1s on 6 remaining CTR pages (practice-location-data, small-teams, provyx-vs-lusha, oral-pathologists, NPPES resource, zoominfo-alternative)
- [ ] 02-02-PLAN.md — Add EHR install base examples to technology detection page and expand firmographic content on service and resource pages

### Phase 3: Email List Pages
**Goal**: Searchers looking for "[specialty] email list" find a dedicated Provyx page with specialty-specific content, data field descriptions, and clear CTA
**Depends on**: Phase 1
**Requirements**: EMAIL-01, EMAIL-02, EMAIL-03, EMAIL-04, EMAIL-05, EMAIL-06, EMAIL-07, EMAIL-08, EMAIL-09, EMAIL-10, EMAIL-11, DEPTH-03
**Success Criteria** (what must be TRUE):
  1. 11 new email list resource pages exist at /resources/{specialty}-email-list/ (or equivalent slug), each with 500+ words, specialty-specific content, data field descriptions, and FAQ schema
  2. Existing email list pages (oral pathologists, chiropractor, naturopathic, periodontist, physiatrist, IV infusion, lasik, med spa) are rewritten so H1 and content match "[specialty] email list" query intent
  3. Every new and rewritten page has 3+ internal links to related provider/resource pages and 2+ outbound links to specialty associations
  4. All pages are registered in the build system (build.py data structures, sitemap, nav where appropriate)
**Plans**: TBD

Plans:
- [ ] 03-01: TBD
- [ ] 03-02: TBD

### Phase 4: Content Gap Pages
**Goal**: Searchers with purchase-intent queries about DH pricing, NPPES accuracy, ketamine/TMS CRM, and EHR lead gen land on relevant Provyx content instead of bouncing to competitors
**Depends on**: Phase 2
**Requirements**: GAP-01, GAP-02, GAP-03, GAP-04, GAP-05
**Success Criteria** (what must be TRUE):
  1. DH pricing guide (/blog/definitive-healthcare-pricing-guide/) exists with sourced pricing data, tier breakdowns, and Provyx positioned as lower-cost alternative
  2. NPPES accuracy guide (/blog/nppes-database-accuracy-guide/) exists with specific accuracy gap examples and how commercial data supplements NPPES
  3. Ketamine clinic CRM and TMS therapy CRM pages exist with specialty-specific CRM workflow content connecting provider data to marketing/sales use cases
  4. EHR lead generation use-case page exists at /use-cases/ehr-lead-generation/ following the existing use-case template pattern
  5. All 5 new pages pass the SEO checklist, are in the sitemap, and have proper schema markup
**Plans**: TBD

Plans:
- [ ] 04-01: TBD

## Progress

**Execution Order:**
Phases execute in numeric order: 1 → 2 → 3 → 4
Note: Phase 3 depends on Phase 1 (not Phase 2), so Phases 2 and 3 could run in parallel after Phase 1.

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. High-Impact CTR and Content Depth | 2/2 | Complete    | 2026-03-14 |
| 2. Remaining CTR and Service Page Depth | 1/2 | Complete    | 2026-03-14 |
| 3. Email List Pages | 0/2 | Not started | - |
| 4. Content Gap Pages | 0/1 | Not started | - |
