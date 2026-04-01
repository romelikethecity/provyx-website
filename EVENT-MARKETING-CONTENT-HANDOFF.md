# Event Marketing Content Plan — Handoff Doc

## Context
The Provyx event marketing service page (/services/event-marketing/) is live with:
- Hero pain stats (64% mobile, 67% form abandonment, 53% 3s bounce, 84% won't fill mobile forms)
- Data bridge section ("Your Provider Data Is the Unfair Advantage")
- Specialty mockups, pre-fill mockups, analytics dashboard mockup
- BTL Michigan case study callout (17K+ links, 8 specialties, 5 days, ~2hrs relaunch)
- Performance vs industry comparison (38% vs 18% page conversion, 86% vs 33% form completion, etc.)

**Problem:** Zero blog articles target event-related searches. All 11 existing posts are about provider data/NPI/CRM. The event marketing page has no organic search funnel feeding it.

**Goal:** Write 8-10 blog articles targeting event-related keywords, each funneling to /services/event-marketing/. Plus page-level improvements deferred from the ICP review.

---

## Part 1: Page-Level Improvements (Before Articles)

These changes go in `scripts/build.py` event marketing service data (~line 14805):

### 1. Post-Event Deliverable Section
The page promises "closed-loop analytics" and shows a dashboard mockup, but never describes what the client actually receives after the event. Add a section (between analytics mockup and "How It Works") describing:
- Registrant export (CSV/Excel) with specialty tags, registration source, timestamp
- Per-specialty conversion report (which specialties registered at what rate)
- Channel attribution (which outreach method drove which registrations)
- Recommendations for next event targeting based on data
- Optional: dashboard access (if we build this as an add-on)

### 2. Broaden Examples Beyond BTL Devices
The mockups reference Emsella, Emsculpt Neo, Emface, Exion, Emtone exclusively. Add at least one mockup or example for non-med-device audiences:
- Pharma: KOL dinner invitation with speaker bio and CME credits
- Healthcare SaaS: product launch event with demo scheduling
This prevents pharma/SaaS readers from bouncing ("this is only for device companies")

### 3. Rewrite "Who Uses This" with Workflow Scenarios
Current copy is generic paragraphs per audience. Replace with specific workflows:
- **Med device field marketing manager:** "You have a territory event in 6 weeks. You need specialty pages for 5 provider types, 12,000 personalized links from your CRM, and a site that's live in a week. Here's how it works..."
- **Pharma event planner:** "You're running 4 KOL dinners this quarter across 4 cities. Same speaker roster, different metro HCP lists. You need each city live in days, not weeks..."
- **Healthcare SaaS marketing director:** "Your annual user conference is in 3 months. You want specialty-specific tracks with separate registration paths..."

### 4. Add Testimonial
The event marketing page is the only service page without a testimonial. After BTL Detroit (March 21), get a quote from the BTL contact and add it. Structure:
```python
"testimonial": {
    "quote": "[Real quote from BTL contact]",
    "name": "[Name]",
    "title": "[Title]",
    "org": "BTL Industries",
},
```

---

## Part 2: SEO Keywords and Article Plan

### Keyword Map

| # | Primary Keyword | Search Intent | Monthly Volume Est. | Difficulty | Audience |
|---|----------------|---------------|-------------------|------------|----------|
| 1 | how to get doctors to attend events | pain-first, top funnel | 200-400 | Low | All |
| 2 | medical device lunch and learn best practices | how-to, mid funnel | 100-300 | Low | Med device |
| 3 | physician event invitation template | template/lead magnet | 100-200 | Low | All |
| 4 | healthcare event marketing ROI | justification, mid funnel | 50-150 | Med | All |
| 5 | KOL dinner planning healthcare | how-to, mid funnel | 50-150 | Low | Pharma |
| 6 | CME event registration platform | comparison, bottom funnel | 50-100 | Med | CME/associations |
| 7 | medical device territory event planning | workflow, mid funnel | 50-100 | Low | Med device field marketing |
| 8 | how to increase physician event attendance | pain-first, top funnel | 100-300 | Low | All |
| 9 | healthcare conference registration best practices | how-to, mid funnel | 50-100 | Low | All |
| 10 | physician speaker program event planning | how-to, mid funnel | 30-80 | Low | Pharma |

### Article Plan (10 Articles)

---

#### Article 1: "How to Get Doctors to Attend Your Events (Without Begging)"
- **Slug:** how-to-get-doctors-to-attend-events
- **Primary keyword:** how to get doctors to attend events
- **Secondary:** physician event attendance, getting physicians to RSVP, doctor event turnout
- **Intent:** Pain-first funnel entry. This is the #1 search a frustrated field marketer types.
- **Angle:** The real reasons physicians don't show up (friction, irrelevance, generic invitations). Pre-filled links solve the friction problem. Specialty-targeted pages solve the relevance problem. Data on which specialties respond to which channels.
- **Word count:** 1,500-2,000
- **CTA:** Link to /services/event-marketing/ with "See how specialty-targeted registration works"
- **Outbound links:** AMA physician time study, CMS NPI Registry
- **Internal links:** /services/event-marketing/, /services/provider-contact-data/, /blog/healthcare-sales-prospecting-mistakes/

#### Article 2: "Medical Device Lunch and Learn: The Field Marketing Playbook"
- **Slug:** medical-device-lunch-and-learn-playbook
- **Primary keyword:** medical device lunch and learn best practices
- **Secondary:** lunch and learn for physicians, medical device in-service event, device demo event planning
- **Intent:** How-to for field marketing managers running territory events
- **Angle:** Step-by-step from territory selection through post-event follow-up. How to pick the right specialties, size the invite list, choose venues, and build specialty-specific landing pages. Reference the BTL Michigan case study as the worked example.
- **Word count:** 2,000-2,500
- **CTA:** Link to /services/event-marketing/ with "We build the registration site. You focus on the event."
- **Outbound links:** AdvaMed code of ethics (device event compliance), BLS healthcare occupation data
- **Internal links:** /services/event-marketing/, /services/custom-list-building/, /use-cases/physician-outreach/

#### Article 3: "Physician Event Invitation Template (+ Pre-Fill Strategy)"
- **Slug:** physician-event-invitation-template
- **Primary keyword:** physician event invitation template
- **Secondary:** doctor event invite email, healthcare event invitation sample, HCP event email template
- **Intent:** Template seeker. High intent — they're actively planning an event.
- **Angle:** Provide 3-4 actual email templates (by specialty). Then explain why the invitation itself is only half the battle — the registration experience matters more. Introduce pre-filled links as the conversion multiplier. Include the 84% mobile form stat.
- **Word count:** 1,500-2,000
- **Lead magnet potential:** Downloadable template pack (email gate)
- **CTA:** Link to /services/event-marketing/
- **Outbound links:** Mailchimp healthcare email benchmarks, CAN-SPAM compliance
- **Internal links:** /services/event-marketing/, /services/provider-contact-data/, /blog/how-to-build-healthcare-provider-contact-list/

#### Article 4: "Healthcare Event Marketing ROI: How to Measure What Matters"
- **Slug:** healthcare-event-marketing-roi
- **Primary keyword:** healthcare event marketing ROI
- **Secondary:** physician event ROI, medical device event cost per attendee, event marketing metrics healthcare
- **Intent:** Justification for budget. Mid-funnel — they want to prove events are worth the spend.
- **Angle:** Framework for calculating event ROI beyond "attendees." Cost per registration, cost per qualified lead, pipeline generated per event, and how specialty segmentation improves all of these. Reference the analytics dashboard mockup. Show how closed-loop data changes the ROI conversation.
- **Word count:** 1,500-2,000
- **CTA:** Link to /services/event-marketing/ analytics section
- **Outbound links:** Bizzabo event benchmarks report, Forrester event marketing data
- **Internal links:** /services/event-marketing/, /use-cases/healthcare-sales-prospecting/, /pricing/

#### Article 5: "KOL Dinner Planning for Pharma and Medical Device Teams"
- **Slug:** kol-dinner-planning-healthcare
- **Primary keyword:** KOL dinner planning healthcare
- **Secondary:** key opinion leader dinner, KOL advisory board event, pharma speaker program planning
- **Intent:** How-to for pharma/device event planners running intimate HCP events
- **Angle:** KOL dinners are the highest-ROI physician events but the hardest to fill. Typical approach: manual invitations from a rep's personal network. Better approach: data-driven targeting by specialty + geography, personalized invitations, pre-filled registration. Cover venue selection, compliance considerations, and follow-up.
- **Word count:** 1,500-2,000
- **CTA:** Link to /services/event-marketing/
- **Outbound links:** PhRMA code on HCP interactions, OIG compliance guidance
- **Internal links:** /services/event-marketing/, /for/pharma-sales/, /services/provider-contact-data/

#### Article 6: "CME Event Registration: Platforms, Compliance, and What Actually Works"
- **Slug:** cme-event-registration-platform-guide
- **Primary keyword:** CME event registration platform
- **Secondary:** CME registration software, continuing medical education event platform, CME credit tracking registration
- **Intent:** Comparison/evaluation. Bottom funnel — actively shopping for a solution.
- **Angle:** Compare the options: Eventbrite (cheap but generic), Cvent (enterprise but expensive), specialty CME platforms (narrow), vs. custom-built registration with provider data integration. Show why generic platforms fail for CME (credit tracking, specialty segmentation, compliance). Position Provyx as the custom option that combines provider data + registration.
- **Word count:** 2,000-2,500
- **CTA:** Link to /services/event-marketing/
- **Outbound links:** ACCME accreditation standards, AMA CME requirements
- **Internal links:** /services/event-marketing/, /compare/ pages, /alternatives/ pages

#### Article 7: "Territory Event Planning for Medical Device Sales Teams"
- **Slug:** medical-device-territory-event-planning
- **Primary keyword:** medical device territory event planning
- **Secondary:** field marketing event planning, regional physician event, territory lunch and learn strategy
- **Intent:** Workflow-specific. The field marketing manager planning Q2 events.
- **Angle:** How to plan a territory event calendar: which metros to target, how to size invite lists by specialty, how to reuse event sites across cities (the "build once, deploy everywhere" pitch). Include a sample quarterly event calendar. Show the math: first event = $3.5-5K, each additional city = $1.5-2.5K. Compare to agency cost ($15-25K per event).
- **Word count:** 2,000-2,500
- **CTA:** Link to /services/event-marketing/ pricing section
- **Outbound links:** BLS healthcare occupation projections by metro, Census metro population data
- **Internal links:** /services/event-marketing/, /services/custom-list-building/, /use-cases/medical-device-territory-planning/

#### Article 8: "How to Increase Physician Event Attendance by 2x"
- **Slug:** increase-physician-event-attendance
- **Primary keyword:** how to increase physician event attendance
- **Secondary:** improve doctor event turnout, physician no-show rate, event attendance optimization healthcare
- **Intent:** Pain-first. They're already running events but attendance is low.
- **Angle:** Data-backed breakdown of why attendance drops: generic invitations (wrong specialty match), manual registration (friction), no reminders (forgetfulness), irrelevant content (same pitch to all specialties). For each cause, show the solution: specialty targeting, pre-fill, calendar integration + referral sharing, specialty-specific landing pages. Reference the 91% attendance rate from the analytics mockup.
- **Word count:** 1,500-2,000
- **CTA:** Link to /services/event-marketing/
- **Outbound links:** ON24 attendance benchmarks, Bizzabo event data
- **Internal links:** /services/event-marketing/, /blog/how-to-get-doctors-to-attend-events/, /services/provider-contact-data/

#### Article 9: "Healthcare Conference Registration: 9 Best Practices That Actually Move the Needle"
- **Slug:** healthcare-conference-registration-best-practices
- **Primary keyword:** healthcare conference registration best practices
- **Secondary:** medical conference registration optimization, healthcare event registration tips, physician conference signup
- **Intent:** Best practices seeker. Could be association, hospital system, or company.
- **Angle:** 9 specific, actionable best practices: (1) mobile-first design (64% stat), (2) pre-fill from your CRM, (3) specialty-specific landing pages, (4) one-click registration, (5) capacity meters for urgency, (6) calendar integration on confirmation, (7) referral sharing system, (8) exit-intent capture, (9) post-event data for next event targeting. Each practice with a stat or benchmark.
- **Word count:** 2,000-2,500
- **CTA:** Link to /services/event-marketing/
- **Outbound links:** Google page speed insights, Formisimo form benchmarks
- **Internal links:** /services/event-marketing/, /blog/increase-physician-event-attendance/, /blog/physician-event-invitation-template/

#### Article 10: "How to Plan a Physician Speaker Program That Fills the Room"
- **Slug:** physician-speaker-program-planning
- **Primary keyword:** physician speaker program event planning
- **Secondary:** medical speaker series planning, KOL speaker event, healthcare thought leader event
- **Intent:** How-to for pharma/device teams running speaker programs across cities
- **Angle:** Speaker programs are recurring multi-city events — the exact use case where reusable event sites shine. Cover: speaker selection, venue strategy (hotel vs. restaurant vs. office), invitation list building by specialty, how to personalize by city while keeping the program consistent. The "build once, deploy everywhere" story with real cost comparisons.
- **Word count:** 1,500-2,000
- **CTA:** Link to /services/event-marketing/
- **Outbound links:** Sunshine Act reporting requirements, CMS Open Payments
- **Internal links:** /services/event-marketing/, /blog/kol-dinner-planning-healthcare/, /for/pharma-sales/

---

## Article Priority Order

**Phase 1 (highest search volume, broadest audience):**
1. How to Get Doctors to Attend Your Events
2. How to Increase Physician Event Attendance by 2x
3. Physician Event Invitation Template
4. Healthcare Conference Registration Best Practices

**Phase 2 (audience-specific, mid funnel):**
5. Medical Device Lunch and Learn Playbook
6. Territory Event Planning for Medical Device Sales Teams
7. Healthcare Event Marketing ROI

**Phase 3 (niche audiences, bottom funnel):**
8. KOL Dinner Planning for Pharma/Device
9. CME Event Registration Platform Guide
10. Physician Speaker Program Planning

---

## Internal Linking Strategy

Every article links to:
- /services/event-marketing/ (primary conversion page)
- At least 1 other article in this cluster (cross-linking)
- At least 1 existing Provyx page (/services/, /use-cases/, /for/, /providers/)

The event marketing service page should add a "Resources" or "Related Articles" section linking back to all published articles in this cluster.

---

## Key Files
- `scripts/blog_posts.py` — all blog post data (add new articles here)
- `scripts/build.py` — blog builder + event marketing service data (~line 14805)
- `scripts/templates.py` — shared HTML generators, CSS_VERSION
- `css/styles.css` — all styles
- `CLAUDE.md` — full site rules, SEO checklist, writing style, citation requirements

## Existing Blog Posts (11 total, all provider data/NPI/CRM focused)
1. healthcare-provider-data-trends-2026
2. how-to-build-healthcare-provider-contact-list
3. npi-database-vs-commercial-provider-data
4. healthcare-sales-prospecting-mistakes
5. medical-practice-data-quality-checklist
6. what-is-npi-number-guide
7. healthcare-crm-data-enrichment
8. dental-practice-data-sales-guide
9. healthcare-data-vendor-evaluation-guide
10. mental-health-provider-data-guide
11. private-equity-healthcare-data-needs

## Writing Rules (from CLAUDE.md)
- DO: contractions, varied sentence length, specific industry details, second-person "you", admit limitations, pain-first messaging
- DON'T: em-dashes, "leverage/utilize/robust/seamless/cutting-edge", "In today's fast-paced...", "Let's dive in", rhetorical questions, uniform list items, exclamation points
- NEVER use false reframes ("not X, it's Y" / "isn't X. It's Y.")
- Every statistic needs an authoritative source with link
- Author bio: Rome — Datajoy (acquired by Databricks), Microsoft, Salesforce, Snapdocs, UC Berkeley Haas MBA
- 2+ outbound links per article to authoritative sources
- 3+ internal links per article
- FAQPage schema on articles with FAQ sections
