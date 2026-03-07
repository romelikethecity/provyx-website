# Handoff: Event Marketing Service on Provyx

## What Happened
BTL Industries (medical device manufacturer) hired us to build a high-conversion event registration site for their Detroit physician event (btlmichigan.com). The site drives registrations for a full-day clinical education event + evening party at the Westin Book Cadillac (March 21, 2026). The client is raving about the delivery. This is now a repeatable service we should market.

## What We Built for BTL

### The Site (btlmichigan.com)
- **Custom registration page** — not Eventbrite, not a WordPress plugin, not a Splash page
- **8 specialty landing pages** (Chiro, MedSpa, Derm, Plastic Surgery, Family Practice, Ortho, Cosmetic Dentistry, Neuro/Psychiatry) — each with specialty-specific copy, product stats, testimonials, and talking points
- **Config-driven architecture** — one `config.json` drives event name, date, time, venue, capacity, specialties, agenda, products, FAQ. Spin up a new city by changing the config
- **Real scarcity mechanics** — capacity meter (47/75 spots filled), registration countdown timer
- **Pre-filled registration links** — URL params auto-populate form fields (first name, last name, email, practice name). Generated 17,268 personalized links from the master contact database, split by practice type
- **Confirmation flow** — personalized confirmation page with Google Calendar + .ics download, referral sharing (email, text, native share), Google Maps directions
- **Calendar integration** — timezone-aware Google Calendar links and .ics file generation
- **Static site on GitHub Pages** — zero hosting cost, instant load times, Cloudflare DNS

### The Data Layer (from Provyx pipeline)
- 17,268 MI contacts with best-available email (prioritized across 7 enrichment sources)
- Multi-sheet Excel export split by 22 practice types
- Pre-filled registration URLs for every contact
- Name quality cleanup (Dr. prefix stripping, fn==ln dedup, single-char rejection)

### What Makes It Different from Eventbrite/Splash
| Feature | Eventbrite/Splash | What We Built |
|---------|-------------------|---------------|
| Specialty landing pages | No | 8 pages with tailored copy, testimonials, product data |
| Pre-filled registration from CRM | No | 17K+ personalized links from verified contact DB |
| Scarcity mechanics | Basic countdown | Live capacity meter + countdown, configurable thresholds |
| Calendar integration | Basic | Timezone-aware Google Cal + .ics with 2 reminders |
| Referral system | No | Built into confirmation flow (email, SMS, native share) |
| Per-registrant analytics | Extra cost | Built-in (GA4 ready) |
| Hosting cost | $99-999/mo | $0 (GitHub Pages) |
| Load time | 2-4s | <1s |
| Template reuse | Rebuild each time | Change config.json, done |

---

## Strategy: How to Position This on Provyx

### Positioning
This is a **new service offering** on Provyx, not a new brand. It sits alongside Provider Contact Data, Practice Location Data, Technology Detection, and Custom List Building.

**Service name:** "Event Marketing for Healthcare Companies"
**One-liner:** "We build high-conversion event registration sites for companies that sell to healthcare providers."

### Why It Fits Provyx
Provyx already has the data pipeline (17K+ MI contacts with verified emails), the healthcare provider intelligence, and the ICP pages for Medical Device Sales Teams. Event marketing is the activation layer on top of that data. The pitch is: "We have 100K+ verified healthcare provider contacts. We can build you a registration site that reaches them with personalized links."

### Target Buyers (Outbound List)
Medical device and aesthetics companies that run physician education events:
- **BTL Industries** (current client — proof point)
- **Cutera** — body contouring, laser aesthetics
- **InMode** — minimally invasive aesthetics
- **Alma Lasers** — aesthetic and surgical lasers
- **Candela** — laser and energy-based devices
- **Sciton** — BBL, HALO, laser platforms
- **Galderma** — Restylane, Sculptra, Cetaphil (derm events)
- **Merz Aesthetics** — Xeomin, Radiesse, Ultherapy
- **Allergan Aesthetics** (AbbVie) — Botox, Juvederm, CoolSculpting
- **Venus Concept** — body contouring, skin resurfacing

All of these companies run regional lunch-and-learns, dinner events, and multi-day training sessions for physicians. They all use either generic Eventbrite pages, clunky corporate microsites, or PDF invitations sent via email.

### Pricing (Package, Not Hourly)
- **First event site:** $3,500-5,000 (custom build, specialty pages, config setup)
- **Additional cities (template reuse):** $1,500-2,500 (change config, new city photos, deploy)
- **Pre-filled contact links from Provyx DB:** $1,000-2,000 per event (depends on state/specialty coverage)
- **Ongoing retainer (monthly events):** $2,000/mo for template management + link generation

---

## What to Build on getprovyx.com

### 1. Case Study Page
**URL:** `/case-studies/medical-device-event-registration/`
**Title:** "Medical Device Company Drives 47 Physician Registrations with Personalized Event Site"

**Structure (follow existing SNF case study pattern):**

#### Hero
- H1: "How a Medical Device Manufacturer Replaced Eventbrite with a High-Conversion Registration Site"
- Subtitle: A medical device company needed to fill a 75-seat physician education event in Detroit. Generic event platforms couldn't segment by specialty or pre-fill from their contact database. We built a config-driven registration site with 8 specialty landing pages and 17,000+ personalized registration links.
- Published: March 2026

#### Sections

**The Client**
- Medical device manufacturer running regional physician education events (lunch-and-learns, full-day training, evening events)
- Sells to 8+ specialties: chiropractors, medical spas, dermatologists, plastic surgeons, family practitioners, orthopedic surgeons, cosmetic dentists, neurologists/psychiatrists
- Each specialty has different clinical use cases, different products, different buying motivations
- First event: 75-seat full-day event at a Detroit luxury hotel with evening cocktail party

**The Problem**
- Eventbrite and Splash treat every registrant the same — a chiropractor and a plastic surgeon see identical pages
- No way to pre-fill registration from an existing contact database
- No specialty-specific landing pages with tailored testimonials and product data
- Generic scarcity mechanics (countdown timer) but no real capacity tracking
- $99-999/mo hosting for a single-page form
- No referral system built into the confirmation flow
- Client had 17K+ healthcare contacts in their CRM but no way to generate personalized registration links at scale

**The Solution**
- Config-driven static site: one JSON file controls event name, date, venue, capacity, specialties, agenda, products, FAQ
- 8 specialty landing pages — each with specialty-specific headline, product stats, physician testimonials, and talking points
- Pre-filled registration: URL params auto-populate first name, last name, email, practice name
- 17,268 personalized registration links generated from verified contact database, split by 22 practice types
- Confirmation flow: personalized greeting, calendar integration (Google Cal + .ics), referral sharing (email, SMS, native share), Google Maps
- Real scarcity: live capacity meter shows spots remaining, countdown when < 7 days to close
- Static site on GitHub Pages: zero hosting cost, <1s load time

**What We Delivered**
- Bullet list of deliverables with specifics (8 specialty pages, 17K links, etc.)

**Why This Approach Works**
- A chiropractor evaluating pelvic floor rehabilitation devices has completely different concerns than a plastic surgeon evaluating body contouring
- Pre-filled links remove friction — the registrant sees their name and practice already populated, just hit submit
- The referral system in the confirmation flow turns every registrant into a channel
- Template reuse: the next city is a config change, not a rebuild

**Results**
- 47 registrations (63% of 75 capacity) with 2+ weeks remaining before event
- 8 specialty-specific landing pages with tailored conversion paths
- 17,268 personalized registration links delivered in multi-sheet Excel
- $0/mo hosting cost (vs $99-999/mo for Eventbrite/Splash)
- Template ready for next city — estimated 2-hour turnaround

#### FAQs (5-6)
- How quickly can you build an event registration site?
- Can you generate personalized links from our existing CRM data?
- What specialties can you create landing pages for?
- How does the template reuse work for additional cities?
- Do you handle the contact data or just the website?
- What analytics are included?

#### Related Links
- `/services/custom-list-building/`
- `/for/medical-device-sales/`
- `/use-cases/physician-outreach-campaigns/`

---

### 2. New Service Page (or Add to Existing Services)
**Option A:** New service page at `/services/event-marketing/`
**Option B:** Add a section to the existing Custom List Building service page

Recommend **Option A** — it's a distinct offering with its own pricing and deliverables.

**Service page data structure (matches SERVICES pattern in build.py):**

```python
{
    "slug": "event-marketing",
    "title": "Event Marketing for Healthcare Companies - Provyx",
    "short_title": "Event Marketing",
    "meta_description": "Custom event registration sites for medical device companies and healthcare vendors. Specialty landing pages, pre-filled links from verified contact data, and config-driven templates.",
    "subtitle": "High-conversion event registration sites for companies that sell to healthcare providers. Specialty-specific landing pages, personalized registration links, and real scarcity mechanics.",
    "aeo_definition": {
        "term": "Healthcare Event Marketing",
        "definition": "Custom event registration sites built for medical device companies and healthcare vendors...",
        "context": "..."
    },
    "problem_heading": "Why Generic Event Platforms Fail for Healthcare Events",
    "problem_body": "... Eventbrite treats a chiropractor and a plastic surgeon identically...",
    "included_heading": "What's Included",
    "included_features": [
        "Config-driven registration site (event name, date, venue, capacity, specialties)",
        "Specialty-specific landing pages with tailored copy, testimonials, and product data",
        "Pre-filled registration links from your contact database or Provyx provider data",
        "Confirmation flow with calendar integration, referral sharing, and directions",
        "Real scarcity mechanics (capacity meter, countdown timer)",
        "Static hosting on GitHub Pages ($0/mo)",
        "Template reuse for additional cities/events"
    ],
    "faqs": [...],
    "related_links": [...],
    "outbound_links": [...]
}
```

---

### 3. Update Existing Pages

#### Medical Device Sales ICP Page (`/for/medical-device-sales/`)
Add a section mentioning event marketing as a capability. Something like:
> "Beyond contact data, Provyx builds custom event registration sites for medical device companies running physician education events. Specialty-specific landing pages, pre-filled registration links from verified provider data, and config-driven templates that spin up new cities in hours."

#### Nav Config
Add "Event Marketing" to the Services dropdown in `nav_config.py`:
```python
{"label": "Event Marketing", "href": "/services/event-marketing/"}
```

---

## Screenshots to Capture

Take these from btlmichigan.com (live site) before the event on March 21:

### Must-Have Screenshots
1. **Hero section** — full-width with Detroit skyline background, headline "Grow Your Practice. We'll Show You How.", capacity badge showing "28 spots remaining"
2. **Registration form** — clean form with pre-filled fields visible (use a test URL with `?fn=Sarah&ln=Mitchell&email=sarah@example.com&practice=Lakeside%20Wellness`)
3. **Specialty cards grid** — the 8 specialty boxes on the main page (Chiropractors, Medical Spas, Dermatologists, etc.)
4. **One specialty landing page** — full page screenshot of the Chiropractors specialty page showing tailored headline, testimonial, product stats, talking points
5. **Confirmation page** — showing personalized greeting, event details, calendar buttons, referral sharing
6. **Agenda section** — the full-day timeline from 9 AM to evening party
7. **Mobile view** — responsive layout on phone-width screen

### Nice-to-Have Screenshots
8. **Pre-fill URL in browser bar** — showing the `?fn=...&ln=...` params in the URL
9. **Excel export** — showing the multi-sheet practice type tabs and prefill_url column
10. **Capacity meter** — close-up of the scarcity bar at different fill levels
11. **FAQ section** — showing the accordion-style FAQ component

### Screenshot Specs
- Desktop: 1440px wide, full-height captures
- Mobile: 390px wide (iPhone 14 Pro)
- Format: PNG, no browser chrome (content only)
- Save to: `/Users/rome/Documents/projects/provyx-website/assets/images/case-studies/event-marketing/`

---

## Build Steps

### Phase 1: Content & Screenshots (Do First)
1. Capture all must-have screenshots from btlmichigan.com
2. Save to Provyx assets directory
3. Write the case study copy (follow SNF case study structure and length — ~2,500 words)
4. Write the service page copy (~1,200-1,500 words)

### Phase 2: Add to build.py
1. Add `CASE_STUDIES` data structure to `build.py` (or `case_studies.py` imported file)
   - Follow the pattern: slug, title, meta_description, h1, subtitle, sections[], faqs[], related_links[], outbound_links[]
   - Include image references for screenshots
2. Add `build_case_study_page()` function (similar to `build_resource_page()`)
3. Add `build_case_studies_index()` for `/case-studies/` listing page
4. Add "Event Marketing" service to `SERVICES` list
5. Add "Event Marketing" to `nav_config.py` Services dropdown
6. Update Medical Device Sales ICP page with event marketing mention
7. Wire case studies into `main()` build function and sitemap

### Phase 3: Build & Deploy
1. Run `python3 scripts/build.py`
2. Preview locally: `python3 -m http.server 8000`
3. Visual review of case study page, service page, nav updates
4. Git commit and push to deploy

---

## Copy Guidelines
- Follow Provyx voice: professional, specific, data-driven
- NO false reframes ("not X, it's Y")
- Use specific numbers (17,268 links, 8 specialty pages, 22 practice types, <1s load time)
- Let the comparison table do the work — Eventbrite vs. what we built
- The case study should read like the SNF recruiting case study: real problem, specific solution, concrete deliverables, measurable results
- Don't oversell — state what was built and what it achieved

---

## Files to Reference
- **BTL site:** `/Users/rome/Documents/projects/btl-events/` (full source)
- **BTL config:** `/Users/rome/Documents/projects/btl-events/config.json` (event data)
- **Existing case study:** `/Users/rome/Documents/projects/provyx-website/case-studies/healthcare-recruiting-snf-contacts/index.html`
- **Provyx build.py:** `/Users/rome/Documents/projects/provyx-website/scripts/build.py`
- **Provyx nav:** `/Users/rome/Documents/projects/provyx-website/scripts/nav_config.py`
- **Export script:** `/tmp/btl_prefill_export.py` (pre-fill link generation)
- **MI export:** `/Users/rome/Downloads/mi_contacts_prefill.xlsx` (17,268 contacts)

## Start Prompt
Copy-paste this into a new Claude Code session to pick up the work:

> I'm adding event marketing as a service to the Provyx website (getprovyx.com). Read HANDOFF-EVENT-MARKETING.md in the project root for the full spec — it covers what we built for BTL, the positioning strategy, what pages to create (case study + service page), screenshots needed, and build steps. Start with Phase 2 (adding to build.py) — I'll have screenshots ready. The existing SNF case study at /case-studies/healthcare-recruiting-snf-contacts/index.html is the template to follow for structure and tone.
