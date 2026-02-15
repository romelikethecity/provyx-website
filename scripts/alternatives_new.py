#!/usr/bin/env python3
"""
New alternative pages data for Provyx website.
4 additional alternative pages for competitors with existing comparison pages.
Imported by build.py.
"""

NEW_ALTERNATIVES = [
    # ===================================================================
    # 3. Apollo Alternative
    # ===================================================================
    {
        "slug": "apollo-alternative",
        "competitor": "Apollo.io",
        "competitor_url": "https://www.apollo.io/",
        "title": "Best Apollo.io Alternative for Healthcare Data",
        "meta_description": (
            "Looking for an Apollo.io alternative for healthcare provider data? "
            "Provyx delivers NPI-verified contacts with taxonomy filtering and no "
            "annual contract."
        ),
        "hero_h1": "Best Apollo.io Alternative for Healthcare Provider Data",
        "hero_subtitle": (
            "Apollo.io is a popular sales engagement platform with a built-in B2B contact database. "
            "It works well for general sales teams prospecting across industries. But if your team "
            "sells exclusively to healthcare providers, Apollo's generic contact data misses critical "
            "fields like NPI numbers, taxonomy codes, and practice-level details. Provyx fills that gap "
            "with healthcare-specific provider intelligence sourced from public NPI registries, business "
            "listings, and commercial databases."
        ),

        "why_switch_heading": "Why Healthcare Sales Teams Look for an Apollo.io Alternative",
        "why_switch_body": (
            "<p>Apollo.io has built an impressive product for outbound sales teams. Its free tier gives you "
            "access to a large B2B contact database, email sequencing, and basic CRM functionality. For a "
            "startup selling SaaS to tech companies, it's a solid starting point.</p>"

            "<p>The problems emerge when you try to use Apollo for healthcare provider prospecting.</p>"

            "<p><strong>No NPI verification.</strong> "
            "<a href=\"https://www.apollo.io/\" target=\"_blank\" rel=\"noopener noreferrer\">Apollo</a> "
            "doesn't include National Provider Identifiers on its records. That means you can't verify "
            "whether a contact is actually a licensed, actively practicing healthcare provider. You might "
            "find a person listed as working at a hospital, but you won't know if they're a practicing "
            "physician, an administrator, a contractor, or someone who left six months ago. For healthcare "
            "sales teams, NPI verification is the baseline for data quality, and Apollo doesn't offer it.</p>"

            "<p><strong>No taxonomy code filtering.</strong> "
            "Apollo lets you filter by industry and job title. It doesn't support NUCC healthcare taxonomy codes, "
            "which are the standardized system for classifying providers by specialty. If you need a list of "
            "interventional cardiologists versus general cardiologists, Apollo can't make that distinction. "
            "Title-based filtering is unreliable in healthcare because the same person might have a title of "
            "\"Physician,\" \"Attending,\" \"Partner,\" or \"Medical Director\" depending on the context.</p>"

            "<p><strong>Email accuracy concerns for healthcare.</strong> "
            "Apollo's email data is sourced through web scraping, pattern matching, and user contributions. "
            "For healthcare providers, this approach produces mixed results. Physicians often don't have "
            "LinkedIn profiles that match their practice email. Office email addresses change when providers "
            "switch practices. Multiple "
            "<a href=\"https://www.g2.com/products/apollo-io/reviews\" target=\"_blank\" rel=\"noopener noreferrer\">G2 reviews</a> "
            "report bounce rates above 10% for healthcare contacts, which is enough to damage your email "
            "sender reputation.</p>"

            "<p><strong>Company-level records, not practice-level.</strong> "
            "Apollo maps contacts to companies. Healthcare operates around practices, clinics, and provider "
            "groups. A dermatologist who practices at two locations and has a hospital affiliation might "
            "show up under the hospital's name, not their actual practice where they see patients four days "
            "a week. For reps who need to reach providers at specific practice locations, Apollo's data model "
            "creates friction.</p>"

            "<p><strong>Credit system adds up quickly.</strong> "
            "Apollo's free tier is genuinely useful for small teams, but the credit system means you burn through "
            "your allocation fast when prospecting at scale. Exporting contacts, viewing emails, and running "
            "sequences all consume credits. Teams that start on the free tier often find themselves upgrading "
            "to a $49-99/month plan within weeks, and from there to a $79-149/user/month plan once they need "
            "full functionality. For a 5-person sales team focused on healthcare, that's $4,740-8,940/year "
            "for data that still lacks NPI verification.</p>"

            "<p>Apollo is a strong product for what it was designed to do: general B2B sales engagement. "
            "It wasn't designed for healthcare-specific provider targeting, and it shows in the data model.</p>"
        ),

        "what_teams_need_heading": "What Healthcare Sales Teams Need That Apollo Doesn't Provide",
        "what_teams_need_body": (
            "<p>Healthcare B2B prospecting has different data requirements than selling to tech companies or "
            "professional services firms. The core differences come down to provider identity verification "
            "and specialty-based targeting.</p>"

            "<p><strong>NPI-verified provider identity.</strong> "
            "Every healthcare provider who bills insurance has a National Provider Identifier. This 10-digit "
            "number is assigned by CMS and stays with the provider for life. When your data includes NPI "
            "verification, you know the contact is a real, active provider. Without NPI, you're guessing.</p>"

            "<p><strong>Taxonomy code segmentation.</strong> "
            "The NUCC maintains over 800 taxonomy codes that classify providers by specialty and sub-specialty. "
            "A taxonomy code tells you whether someone is a general dentist or an oral surgeon, a family "
            "medicine physician or a rheumatologist. Title-based filtering can't make these distinctions "
            "reliably because titles are inconsistent across organizations.</p>"

            "<p><strong>Practice-level contact data.</strong> "
            "Healthcare decisions are made at the practice level, not the enterprise level (except for large "
            "health systems). You need the practice's direct phone line, the office address where the provider "
            "sees patients, and ideally the name of the practice owner or office manager. Company-level records "
            "from general B2B databases rarely include this information.</p>"

            "<p><strong>Data sourced from healthcare registries.</strong> "
            "The most reliable healthcare provider data starts with the "
            "<a href=\"https://npiregistry.cms.hhs.gov/\" target=\"_blank\" rel=\"noopener noreferrer\">NPPES NPI Registry</a> "
            "and enriches from there. Web-scraped data and user-contributed records are supplementary at best. "
            "When the foundation of your provider data isn't the NPI registry, accuracy suffers.</p>"

            "<p>These requirements aren't unique to large enterprise sales teams. Even a 3-person SDR team "
            "calling on dental practices needs NPI-verified data with taxonomy filtering to avoid wasting "
            "half their calls on wrong contacts.</p>"
        ),

        "comparison_heading": "Apollo.io vs. Provyx: Quick Comparison",
        "comparison_rows": [
            ("Starting Price",
             'Free tier, then $49-149/user/mo <span class="tag tag--amber">Per User</span>',
             'Pay per record <span class="tag tag--green">No Minimum</span>'),
            ("Contract Terms",
             'Monthly or annual <span class="tag tag--green">Flexible</span>',
             'Month-to-month <span class="tag tag--green">Cancel Anytime</span>'),
            ("NPI Verification",
             'Not included <span class="tag tag--red">No NPI</span>',
             'Every record <span class="tag tag--green">NPI-Verified</span>'),
            ("Taxonomy Filtering",
             'Not available <span class="tag tag--red">Title Only</span>',
             '800+ NUCC codes <span class="tag tag--green">Taxonomy</span>'),
            ("Healthcare Focus",
             'General B2B <span class="tag tag--amber">All Industries</span>',
             '100% healthcare <span class="tag tag--green">Provider-Specific</span>'),
            ("Email Accuracy",
             'Pattern-matched <span class="tag tag--amber">Variable</span>',
             'Verified against registries <span class="tag tag--green">Verified</span>'),
            ("Data Delivery",
             'Platform + API <span class="tag tag--green">Integrated</span>',
             'CSV, Excel, API <span class="tag tag--green">Flexible</span>'),
            ("Best For",
             "General B2B outbound sales at scale",
             "Teams selling exclusively to healthcare providers"),
        ],

        "how_it_works_heading": "How Provyx Works as an Apollo.io Alternative for Healthcare",
        "how_it_works_body": (
            "<p>Provyx is a healthcare provider business data platform. It covers one vertical: healthcare. "
            "Every record is built from the "
            "<a href=\"https://npiregistry.cms.hhs.gov/\" target=\"_blank\" rel=\"noopener noreferrer\">NPPES NPI Registry</a>, "
            "enriched with contact data from business listings and commercial databases, and verified against "
            "the NPI registry before delivery.</p>"

            "<h3>Data Sources and Verification</h3>"
            "<p>Provyx starts with the full NPPES database (8M+ NPI records) and enriches with three layers:</p>"
            "<ul>"
            "<li><strong>Public registries.</strong> NPI numbers, taxonomy codes, enumeration dates, and practice "
            "addresses from CMS. This is the identity foundation.</li>"
            "<li><strong>Business data.</strong> State licensing boards, business directories, and public filings "
            "fill in direct phone numbers, websites, ownership information, and practice details.</li>"
            "<li><strong>Commercial enrichment.</strong> Third-party data adds email addresses, LinkedIn profiles, "
            "technology stack information, and estimated practice size.</li>"
            "</ul>"

            "<h3>What You Get That Apollo Doesn't Provide</h3>"
            "<p>Every Provyx record includes an NPI number verified as active in the current NPPES data. "
            "Taxonomy codes are included on all records, letting you filter by any of 800+ specialties and "
            "sub-specialties. Practice-level addresses reflect where the provider actually sees patients, "
            "not just their hospital affiliation. And pricing is pay-per-record with no annual contract, "
            "so you pay for the exact records you need.</p>"

            "<h3>What Provyx Doesn't Do</h3>"
            "<p>Provyx is not a sales engagement platform. It doesn't include email sequencing, phone dialers, "
            "or CRM functionality. If you need those tools, you'll use Provyx data inside your existing "
            "sales stack (Salesforce, HubSpot, Outreach, etc.). Provyx also covers US healthcare only. "
            "If your team prospects outside of healthcare or outside the US, you'll need an additional data "
            "source for those markets.</p>"
        ),

        "limitations_heading": "What Provyx Doesn't Do",
        "limitations_body": (
            "<p>Provyx covers US healthcare providers. It doesn't include international provider data, "
            "non-healthcare businesses, or sales engagement tools like email sequencing and dialers. "
            "If you prospect across multiple industries, you'll need Provyx for healthcare data and "
            "another source for non-healthcare contacts. If you need a full sales engagement platform, "
            "you'll use Provyx data inside tools like Outreach, Salesloft, or HubSpot sequences.</p>"
        ),

        "who_switches_heading": "Who Switches from Apollo to Provyx",
        "who_switches_body": (
            "<p><strong>Healthcare SaaS companies</strong> that started prospecting with Apollo's free tier and hit the ceiling on healthcare-specific data quality. "
            "They need NPI verification and taxonomy filtering that Apollo can't provide.</p>"
            "<p><strong>Medical device sales teams</strong> that need practice-level data for field reps. Apollo maps contacts to companies, "
            "but device reps need to know which office a surgeon operates from, who manages the practice, and what the direct phone line is.</p>"
            "<p><strong>Healthcare marketing agencies</strong> building targeted campaigns for clients. When a client asks for \"a list of 3,000 dermatologists in the Southeast,\" "
            "they need NPI-verified records with taxonomy-confirmed specialties, not title-filtered contacts from a general B2B database.</p>"
            "<p><strong>Teams that outgrew Apollo's credit system.</strong> Once you need thousands of healthcare contacts per quarter, "
            "Apollo's credit-based pricing makes less sense than Provyx's pay-per-record model.</p>"
        ),

        "migration_heading": "How to Switch from Apollo.io to Provyx for Healthcare Data",
        "migration_body": (
            "<p><strong>Step 1: Export your current healthcare contacts from Apollo.</strong> "
            "Download your Apollo healthcare contact lists as CSV. Note which fields you're currently using and which are missing.</p>"
            "<p><strong>Step 2: Define your healthcare data requirements.</strong> "
            "Identify the specialties (taxonomy codes), geographies, and practice types you need. Be specific: \"oral surgeons in Texas with 3+ providers\" "
            "is a better request than \"dental practices.\"</p>"
            "<p><strong>Step 3: Request a Provyx sample list.</strong> "
            "Start with a small list for one specialty or territory. Compare it side-by-side with your Apollo data. Check for NPI verification, "
            "practice-level addresses, and contact accuracy.</p>"
            "<p><strong>Step 4: Import into your sales stack.</strong> "
            "Provyx delivers CSV files that import directly into Salesforce, HubSpot, Apollo (yes, you can use Apollo's sequencing with Provyx data), "
            "or any other CRM. Map the NPI and taxonomy fields to custom fields in your CRM.</p>"
            "<p><strong>Step 5: Keep Apollo for non-healthcare.</strong> "
            "If your team also sells outside healthcare, keep Apollo for those verticals. Use Provyx for healthcare-specific data. "
            "Most teams find this hybrid approach gives them the best of both worlds.</p>"
        ),

        "faqs": [
            {"question": "Is Provyx cheaper than Apollo.io for healthcare data?",
             "answer": "For healthcare-specific data, yes. Apollo's paid plans range from $49-149/user/month. A 5-person team pays $2,940-8,940/year. Provyx charges per record with no user fees, so a team buying 5,000 NPI-verified provider records pays significantly less than an annual Apollo subscription while getting healthcare-specific fields Apollo doesn't include."},
            {"question": "Can I use Provyx data inside Apollo.io?",
             "answer": "Yes. Export Provyx records as CSV and import them into Apollo or any other sales engagement platform. You get the healthcare-specific fields (NPI, taxonomy, practice details) while using Apollo's sequencing and workflow tools."},
            {"question": "Does Apollo.io have healthcare provider data?",
             "answer": "Apollo includes some healthcare contacts, but they're sourced through general web scraping and pattern matching rather than NPI registry verification. The records lack NPI numbers, taxonomy codes, and practice-level detail that healthcare sales teams need for targeted outreach."},
            {"question": "What if I sell to both healthcare and non-healthcare?",
             "answer": "Use Provyx for healthcare provider contacts and Apollo (or another general B2B tool) for non-healthcare. Many teams run both, using Provyx's verified data for their healthcare pipeline and a general tool for other verticals."},
        ],

        "related_links": [
            {"url": "/compare/provyx-vs-apollo/", "label": "Provyx vs. Apollo.io Detailed Comparison"},
            {"url": "/compare/provyx-vs-zoominfo/", "label": "Provyx vs. ZoomInfo Comparison"},
            {"url": "/services/provider-contact-data/", "label": "Provider Contact Data"},
            {"url": "/pricing/", "label": "Provyx Pricing"},
        ],
        "outbound_links": [
            ("https://www.apollo.io/", "Apollo.io official website"),
            ("https://npiregistry.cms.hhs.gov/", "CMS NPI Registry"),
            ("https://www.g2.com/products/apollo-io/reviews", "Apollo.io G2 Reviews"),
        ],
    },
    # ===================================================================
    # 4. IQVIA Alternative
    # ===================================================================
    {
        "slug": "iqvia-alternative",
        "competitor": "IQVIA OneKey",
        "competitor_url": "https://www.iqvia.com/",
        "title": "Best IQVIA OneKey Alternative for Healthcare Data",
        "meta_description": (
            "Looking for an IQVIA OneKey alternative? Provyx delivers NPI-verified "
            "provider data with pay-per-record pricing, no enterprise contract, and "
            "no minimum commitment."
        ),
        "hero_h1": "Best IQVIA OneKey Alternative for Healthcare Provider Data",
        "hero_subtitle": (
            "IQVIA OneKey is the dominant provider reference database for large pharma. "
            "It's also expensive, slow to implement, and designed for enterprise procurement "
            "cycles. If your team needs verified healthcare provider data without a six-figure "
            "contract and a 90-day implementation, Provyx delivers NPI-verified provider "
            "intelligence at a fraction of the cost."
        ),

        "why_switch_heading": "Why Teams Look for an IQVIA OneKey Alternative",
        "why_switch_body": (
            "<p>IQVIA is the 800-pound gorilla in healthcare data. Their OneKey product has been the reference "
            "database for pharmaceutical commercial operations for decades. If you work at a top-20 pharma "
            "company, you probably already have an IQVIA contract.</p>"

            "<p>The challenge is that IQVIA was built for large enterprise pharma, and it shows in the pricing, "
            "contract structure, and implementation process.</p>"

            "<p><strong>Enterprise pricing that excludes smaller teams.</strong> "
            "<a href=\"https://www.iqvia.com/\" target=\"_blank\" rel=\"noopener noreferrer\">IQVIA</a> doesn't "
            "publish pricing. Based on industry reports and customer feedback, OneKey contracts start in the "
            "mid-five-figures annually and scale well into six figures for full access. The pricing model is "
            "designed for pharma companies with commercial operations budgets measured in millions. If you're "
            "a 20-person medical device company or a healthcare SaaS startup, IQVIA isn't built for your "
            "budget or your procurement process.</p>"

            "<p><strong>Long implementation timelines.</strong> "
            "Getting IQVIA data into your systems isn't a same-day process. Implementation typically involves "
            "data integration work, CRM mapping, and configuration cycles that take weeks to months. For teams "
            "that need provider data this quarter, not next quarter, the implementation timeline is a dealbreaker.</p>"

            "<p><strong>Rigid data delivery.</strong> "
            "OneKey data is delivered through IQVIA's platforms and APIs, often with restrictions on how you "
            "can use, store, and redistribute the data. License agreements can limit your ability to share data "
            "across teams or integrate it freely into your tech stack. These restrictions make sense for IQVIA's "
            "enterprise pharma customers who have dedicated data operations teams. They're burdensome for smaller "
            "organizations that need flexible data access.</p>"

            "<p><strong>More data than you need.</strong> "
            "OneKey is a comprehensive reference database covering prescribers, affiliations, institutional "
            "hierarchies, and claims-derived data. If your use case is straightforward, getting 5,000 verified "
            "provider contacts with emails and phones for your sales territory, you're paying for capabilities "
            "and data dimensions you'll never use. The total cost of ownership goes well beyond the license fee "
            "when you factor in implementation, training, and ongoing data management.</p>"

            "<p>IQVIA is the right choice for large pharma companies that need the full depth of prescriber "
            "data, claims analytics, and institutional mapping. For teams with more targeted needs and smaller "
            "budgets, the IQVIA model is overkill.</p>"
        ),

        "what_teams_need_heading": "What Mid-Market Healthcare Teams Actually Need",
        "what_teams_need_body": (
            "<p>The gap in the market isn't between IQVIA and nothing. It's between IQVIA-grade enterprise data "
            "and the practical data needs of mid-market healthcare sales teams.</p>"

            "<p><strong>Verified provider records with NPI.</strong> "
            "You need to know that each record represents a real, active provider. NPI verification against "
            "the <a href=\"https://npiregistry.cms.hhs.gov/\" target=\"_blank\" rel=\"noopener noreferrer\">NPPES registry</a> "
            "is the standard. Every record should include the NPI number, current taxonomy code, and a verified "
            "practice address.</p>"

            "<p><strong>Contact information for sales outreach.</strong> "
            "Email addresses and direct phone numbers that your reps can use immediately. Not just the "
            "provider's name and affiliation, but actual communication channels verified within the last "
            "90 days.</p>"

            "<p><strong>Specialty filtering by taxonomy code.</strong> "
            "If you sell to dermatologists, you need to filter for dermatology taxonomy codes, not search by "
            "keyword and hope for the best. NUCC taxonomy codes are the standard classification system, and "
            "your data should support filtering by any of the 800+ codes.</p>"

            "<p><strong>Fast delivery without implementation.</strong> "
            "Your team shouldn't wait 6 weeks for data integration. Custom lists delivered as CSV or pushed "
            "directly to your CRM within days, not months.</p>"

            "<p><strong>Transparent, predictable pricing.</strong> "
            "Pay-per-record or fixed-price custom lists that you can budget for in advance. No surprise "
            "renewal increases, no per-seat fees, no minimum spend requirements that force you to buy more "
            "than you need.</p>"
        ),

        "comparison_heading": "IQVIA OneKey vs. Provyx: Quick Comparison",
        "comparison_rows": [
            ("Starting Price",
             'Not public, ~$50K+/year <span class="tag tag--red">Enterprise</span>',
             'Pay per record <span class="tag tag--green">No Minimum</span>'),
            ("Contract Terms",
             'Multi-year, enterprise <span class="tag tag--red">Long-Term</span>',
             'Month-to-month <span class="tag tag--green">Cancel Anytime</span>'),
            ("Implementation",
             'Weeks to months <span class="tag tag--red">Complex</span>',
             'Days <span class="tag tag--green">Immediate</span>'),
            ("NPI Verification",
             'Included <span class="tag tag--green">Verified</span>',
             'Every record <span class="tag tag--green">NPI-Verified</span>'),
            ("Taxonomy Filtering",
             'Full NUCC <span class="tag tag--green">Complete</span>',
             '800+ NUCC codes <span class="tag tag--green">Taxonomy</span>'),
            ("Data Depth",
             'Claims, Rx, affiliations <span class="tag tag--green">Deep</span>',
             'Contacts, firmographics, tech <span class="tag tag--green">Sales-Ready</span>'),
            ("Best For",
             "Large pharma commercial operations",
             "Mid-market teams selling to healthcare providers"),
        ],

        "how_it_works_heading": "How Provyx Works as an IQVIA Alternative",
        "how_it_works_body": (
            "<p>Provyx is built for teams that need healthcare provider data for sales and marketing "
            "without the enterprise overhead of IQVIA. The data is sourced from the same public registries "
            "(NPPES, state licensing boards) and enriched with commercial data for contact information and "
            "practice details.</p>"

            "<h3>What You Get</h3>"
            "<p>Every Provyx record includes: NPI number (verified active), provider name and credentials, "
            "taxonomy code(s), current practice address, phone number, and verified email where available. "
            "Additional fields include practice size indicators, technology stack data, website URLs, and "
            "owner/decision-maker identification for independent practices.</p>"

            "<h3>What's Different from IQVIA</h3>"
            "<p>Provyx doesn't include claims-derived data, prescribing patterns, or the deep institutional "
            "affiliation mapping that IQVIA provides. Those capabilities require access to claims data that "
            "only IQVIA-scale companies can acquire. What Provyx does provide is the sales-ready contact "
            "intelligence that most healthcare sales teams actually use day-to-day: who to call, how to reach "
            "them, what specialty they practice, and where they see patients.</p>"

            "<h3>Pricing and Delivery</h3>"
            "<p>Pay per record. No annual contract. No implementation project. Tell Provyx what you need "
            "(specialty, geography, practice type) and receive a custom list within days. Import into your "
            "CRM, sales engagement tool, or marketing automation platform.</p>"
        ),

        "limitations_heading": "What Provyx Doesn't Do",
        "limitations_body": (
            "<p>Provyx doesn't offer claims data, prescribing data, or the depth of institutional affiliation "
            "mapping that IQVIA provides. If your use case requires knowing how many prescriptions a physician "
            "wrote for a specific drug class last year, or mapping every provider in a 15-hospital IDN's "
            "hierarchy, IQVIA's data depth is necessary. Provyx covers the contact intelligence and practice "
            "data layer, not the clinical and claims analytics layer.</p>"
        ),

        "who_switches_heading": "Who Switches from IQVIA to Provyx",
        "who_switches_body": (
            "<p><strong>Mid-market medical device companies</strong> that need provider contact data but can't justify a $50K+ IQVIA contract. "
            "Their use case is straightforward: build territory-specific lists of target providers with email and phone contact data.</p>"
            "<p><strong>Healthcare SaaS startups</strong> that need provider data for their first sales hires. IQVIA's implementation timeline "
            "and contract structure doesn't match startup velocity. They need data this week, not next quarter.</p>"
            "<p><strong>Teams supplementing IQVIA.</strong> Some organizations maintain IQVIA for analytics and prescribing data but use Provyx "
            "for day-to-day sales contact data because it's faster to get a fresh list and cheaper per record.</p>"
            "<p><strong>Consulting firms</strong> doing healthcare market assessments that need provider counts and contact data by specialty and geography "
            "without committing to an enterprise data license.</p>"
        ),

        "migration_heading": "How to Start Using Provyx Instead of IQVIA",
        "migration_body": (
            "<p><strong>Step 1: Identify your core data use case.</strong> "
            "If you use IQVIA primarily for claims/prescribing analytics, Provyx isn't a replacement. If you use IQVIA primarily for sales contact data "
            "(provider names, emails, phones, addresses), Provyx covers that need at a fraction of the cost.</p>"
            "<p><strong>Step 2: Start with one territory or specialty.</strong> "
            "Request a Provyx list for one sales territory or one target specialty. Compare the coverage and contact accuracy "
            "against what you're getting from IQVIA for the same segment.</p>"
            "<p><strong>Step 3: Test in your workflow.</strong> "
            "Import the Provyx data into your CRM or sales tool. Have your reps work the list for 2-4 weeks. Track deliverability rates, "
            "connect rates, and data accuracy feedback from the field.</p>"
            "<p><strong>Step 4: Scale or supplement.</strong> "
            "If the data performs, expand to more territories. Some teams fully replace IQVIA for sales data while keeping it for analytics. "
            "Others use Provyx for territory-level lists while using IQVIA for enterprise-level market insights.</p>"
        ),

        "faqs": [
            {"question": "Is Provyx as comprehensive as IQVIA OneKey?",
             "answer": "No, and it's not trying to be. IQVIA offers claims data, prescribing patterns, and deep institutional mapping that Provyx doesn't include. Provyx focuses on the provider contact intelligence that sales teams use daily: verified NPI data, practice contacts, specialty filtering, and firmographics. If your use case is sales outreach rather than clinical analytics, Provyx provides what you need at a fraction of the cost."},
            {"question": "How does Provyx pricing compare to IQVIA?",
             "answer": "IQVIA contracts typically start at $50,000+ annually. Provyx charges per record with no minimum. A team buying 10,000 provider records from Provyx spends a fraction of what an IQVIA license costs. The tradeoff is data depth: IQVIA includes claims and prescribing data that Provyx doesn't offer."},
            {"question": "Can I switch from IQVIA to Provyx?",
             "answer": "If your primary use case is sales prospecting and outreach, yes. Many teams use IQVIA for analytics and market insights while using Provyx (or similar services) for day-to-day sales data. If you depend on IQVIA's claims data for commercial operations, you'll likely need to keep some IQVIA access."},
            {"question": "Does Provyx cover the same providers as IQVIA?",
             "answer": "Both source from the NPPES registry, so the underlying provider identity data overlaps significantly. Provyx covers US healthcare providers with NPI numbers. IQVIA also covers international markets and includes non-NPI data dimensions. For US provider contacts, the coverage is comparable."},
        ],

        "related_links": [
            {"url": "/compare/provyx-vs-iqvia/", "label": "Provyx vs. IQVIA Detailed Comparison"},
            {"url": "/compare/provyx-vs-definitive-healthcare/", "label": "Provyx vs. Definitive Healthcare"},
            {"url": "/services/provider-contact-data/", "label": "Provider Contact Data"},
            {"url": "/pricing/", "label": "Provyx Pricing"},
        ],
        "outbound_links": [
            ("https://www.iqvia.com/", "IQVIA official website"),
            ("https://npiregistry.cms.hhs.gov/", "CMS NPI Registry"),
        ],
    },
    # ===================================================================
    # 5. Lusha Alternative
    # ===================================================================
    {
        "slug": "lusha-alternative",
        "competitor": "Lusha",
        "competitor_url": "https://www.lusha.com/",
        "title": "Best Lusha Alternative for Healthcare Provider Data",
        "meta_description": (
            "Looking for a Lusha alternative for healthcare contacts? Provyx delivers "
            "NPI-verified provider data with taxonomy filtering, practice-level details, "
            "and pay-per-record pricing."
        ),
        "hero_h1": "Best Lusha Alternative for Healthcare Provider Data",
        "hero_subtitle": (
            "Lusha is a B2B contact enrichment tool that works well for general sales teams. "
            "For healthcare, it lacks the provider-specific data points that make the difference "
            "between productive outreach and wasted calls. Provyx provides NPI-verified provider "
            "contacts with taxonomy codes, practice-level data, and healthcare-specific enrichment."
        ),

        "why_switch_heading": "Why Healthcare Teams Outgrow Lusha",
        "why_switch_body": (
            "<p><a href=\"https://www.lusha.com/\" target=\"_blank\" rel=\"noopener noreferrer\">Lusha</a> "
            "built its reputation on making B2B contact data accessible. The browser extension lets reps "
            "find direct dials and email addresses while browsing LinkedIn, and the platform pricing starts "
            "lower than enterprise alternatives. For a sales team calling on tech companies or professional "
            "services firms, Lusha's model works.</p>"

            "<p>Healthcare teams hit limits quickly.</p>"

            "<p><strong>No NPI numbers.</strong> "
            "Lusha provides name, email, phone, company, and title. It doesn't include NPI numbers because "
            "its data model isn't healthcare-aware. Without NPI verification, you can't confirm whether a "
            "contact is a licensed, active healthcare provider. This matters when your compliance team asks "
            "how you verified the recipients on your email campaign were real physicians.</p>"

            "<p><strong>No specialty filtering.</strong> "
            "Lusha's contact search uses company name, job title, industry, and location. There's no way to "
            "filter by NUCC taxonomy code, which means you can't build a list of oral surgeons versus general "
            "dentists, or interventional pain specialists versus general pain management physicians. Title-based "
            "searches return inconsistent results because healthcare providers have non-standardized titles.</p>"

            "<p><strong>Company-centric data model.</strong> "
            "Lusha maps contacts to companies. Healthcare providers work at practices, and many providers "
            "practice at multiple locations. Lusha might show a physician as working at \"Regional Medical Center\" "
            "when they actually see patients at their own practice four days a week. The practice-level address "
            "and phone number are what sales reps need, and Lusha's data model doesn't prioritize them.</p>"

            "<p><strong>Credit-based pricing at scale.</strong> "
            "Lusha's pricing starts at $29/user/month for 480 credits annually on the Pro plan. Each contact "
            "reveal costs credits. For a healthcare sales team that needs to build lists of thousands of providers, "
            "the credit system means you either upgrade quickly to a higher tier or run out of reveals before "
            "the month is over. The Enterprise plan removes credit limits but requires a custom contract.</p>"

            "<p>Lusha does what it was built to do: fast B2B contact enrichment across all industries. "
            "It wasn't built for healthcare-specific data needs.</p>"
        ),

        "what_teams_need_heading": "What Healthcare Sales Teams Need Beyond Lusha",
        "what_teams_need_body": (
            "<p>The gap between general B2B contact enrichment and healthcare-ready data comes down to a "
            "few specific capabilities.</p>"

            "<p><strong>Provider identity verification.</strong> "
            "NPI numbers confirm that a contact is a licensed, active healthcare provider. This isn't just "
            "a nice-to-have for compliance. It's how you prevent sending product emails to retired physicians, "
            "administrative staff who happen to have clinical-sounding titles, or providers who've moved to "
            "a different state.</p>"

            "<p><strong>Specialty-level targeting.</strong> "
            "Healthcare taxonomy codes let you build lists at the exact specialty level you need. A medical "
            "device company selling orthopedic implants needs orthopedic surgeons specifically, not all "
            "physicians at hospitals with orthopedic departments. The "
            "<a href=\"https://nucc.org/\" target=\"_blank\" rel=\"noopener noreferrer\">NUCC taxonomy system</a> "
            "provides over 800 specialty and sub-specialty codes for this purpose.</p>"

            "<p><strong>Practice-level contact information.</strong> "
            "The practice address, direct phone line, fax number, and office manager name. These are the "
            "data points that get reps through to decision-makers at independent and small group practices. "
            "A hospital switchboard number isn't useful when the provider sees patients at a standalone office.</p>"

            "<p><strong>Data from healthcare registries.</strong> "
            "The <a href=\"https://npiregistry.cms.hhs.gov/\" target=\"_blank\" rel=\"noopener noreferrer\">NPPES NPI Registry</a> "
            "is the authoritative source for provider identity. Provider data that doesn't start with NPI "
            "verification is built on a weaker foundation. Healthcare-specific enrichment adds practice "
            "details, ownership information, and technology data that general B2B sources don't capture.</p>"
        ),

        "comparison_heading": "Lusha vs. Provyx: Quick Comparison",
        "comparison_rows": [
            ("Starting Price",
             '$29/user/mo (Pro) <span class="tag tag--amber">Credit-Based</span>',
             'Pay per record <span class="tag tag--green">No Minimum</span>'),
            ("NPI Verification",
             'Not included <span class="tag tag--red">No NPI</span>',
             'Every record <span class="tag tag--green">NPI-Verified</span>'),
            ("Taxonomy Filtering",
             'Not available <span class="tag tag--red">Title Only</span>',
             '800+ NUCC codes <span class="tag tag--green">Taxonomy</span>'),
            ("Healthcare Focus",
             'General B2B <span class="tag tag--amber">All Industries</span>',
             '100% healthcare <span class="tag tag--green">Provider-Specific</span>'),
            ("Data Model",
             'Contact + Company <span class="tag tag--amber">Company-Centric</span>',
             'Provider + Practice <span class="tag tag--green">Practice-Level</span>'),
            ("Data Delivery",
             'Browser extension + export <span class="tag tag--green">Fast</span>',
             'CSV, Excel, API <span class="tag tag--green">Flexible</span>'),
            ("Best For",
             "Quick contact lookup across industries",
             "Healthcare provider targeting at scale"),
        ],

        "how_it_works_heading": "How Provyx Works as a Lusha Alternative for Healthcare",
        "how_it_works_body": (
            "<p>Provyx replaces the healthcare-specific data gap that Lusha leaves. Instead of looking up "
            "contacts one at a time through a browser extension, you tell Provyx what you need and receive "
            "a complete, NPI-verified provider list.</p>"

            "<h3>Built from Healthcare Data Sources</h3>"
            "<p>Every Provyx record starts with the NPPES NPI Registry. Provider identity is verified against "
            "CMS data before any enrichment is applied. From there, practice details, contact information, and "
            "firmographic data are compiled from state licensing boards, business directories, and commercial "
            "databases.</p>"

            "<h3>List-Based vs. Lookup-Based</h3>"
            "<p>Lusha's strength is individual contact lookups. You find someone on LinkedIn, click the extension, "
            "and get their email. That works for account-based outbound. Provyx's strength is building complete "
            "target lists: give us a specialty, geography, and practice type, and we deliver thousands of verified "
            "records ready for CRM import. Different models for different use cases.</p>"

            "<h3>No Credit System</h3>"
            "<p>Provyx charges per record. No credits to track, no monthly limits to manage, no surprise "
            "overages. You buy the records you need and use them without restrictions on how many team members "
            "access them.</p>"
        ),

        "limitations_heading": "What Provyx Doesn't Do",
        "limitations_body": (
            "<p>Provyx doesn't have a browser extension for real-time contact lookups. If you need to find "
            "a single person's email while browsing LinkedIn, Lusha is faster for that use case. Provyx is "
            "designed for building targeted lists, not individual lookups. Provyx also covers US healthcare "
            "only. For international contacts or non-healthcare industries, you'll need a different data source.</p>"
        ),

        "who_switches_heading": "Who Switches from Lusha to Provyx",
        "who_switches_body": (
            "<p><strong>Healthcare sales teams that outgrew Lusha's credit system.</strong> Individual contact lookups work for small-volume prospecting. "
            "Once you need to build lists of 1,000+ providers per quarter, the credit model becomes expensive relative to pay-per-record alternatives.</p>"
            "<p><strong>Teams that need specialty-level targeting.</strong> If your reps need to reach specific provider types (not just \"physicians\" "
            "but \"interventional cardiologists\" or \"pediatric dentists\"), Lusha's title-based filtering isn't precise enough.</p>"
            "<p><strong>Marketing teams running email campaigns.</strong> Lusha's email data for healthcare providers has variable accuracy. "
            "Teams seeing bounce rates above 5% on Lusha-sourced healthcare contacts often switch to NPI-verified data sources.</p>"
            "<p><strong>Medical device reps needing practice data.</strong> Field reps need practice addresses, direct office phone numbers, "
            "and owner/decision-maker names. Lusha provides contact-level data but not the practice-level detail that healthcare field sales requires.</p>"
        ),

        "migration_heading": "How to Switch from Lusha to Provyx for Healthcare",
        "migration_body": (
            "<p><strong>Step 1: Audit your Lusha healthcare usage.</strong> "
            "Check how many Lusha credits you spend monthly on healthcare contacts. Note the bounce rates and connect rates on Lusha-sourced healthcare records. "
            "This gives you a baseline for comparison.</p>"
            "<p><strong>Step 2: Request a Provyx sample for your target specialty.</strong> "
            "Pick your highest-priority specialty and geography. Compare the Provyx sample against your Lusha data for the same segment: "
            "check for NPI verification, email accuracy, and practice-level details.</p>"
            "<p><strong>Step 3: Import and test.</strong> "
            "Load the Provyx data into your CRM alongside your Lusha contacts. Run a head-to-head test: same campaign, different data sources. "
            "Track deliverability, connect rates, and response rates.</p>"
            "<p><strong>Step 4: Decide your workflow.</strong> "
            "Many teams keep Lusha for ad-hoc lookups (quick email finds during calls) and use Provyx for structured list building "
            "(quarterly territory refreshes, campaign lists). The tools complement each other because they serve different workflows.</p>"
        ),

        "faqs": [
            {"question": "Is Provyx more expensive than Lusha?",
             "answer": "It depends on your use case. Lusha Pro costs $29/user/month with credit limits. A 5-person team pays $1,740/year. Provyx charges per record with no user fees. If you need a few hundred lookups per month, Lusha is cheaper. If you need thousands of verified healthcare provider records, Provyx is more cost-effective because you're paying for data, not seats."},
            {"question": "Can I use both Lusha and Provyx?",
             "answer": "Yes. Some teams use Lusha for ad-hoc contact lookups (finding someone's email during a call) and Provyx for building targeted healthcare prospect lists (quarterly territory refreshes, campaign lists). The tools serve different workflows."},
            {"question": "Does Lusha have healthcare-specific data?",
             "answer": "Lusha includes healthcare contacts in its general database, but without NPI verification, taxonomy codes, or practice-level data. You can find a person listed at a hospital, but you won't get the healthcare-specific fields that verify their identity and classify their specialty."},
        ],

        "related_links": [
            {"url": "/compare/provyx-vs-lusha/", "label": "Provyx vs. Lusha Detailed Comparison"},
            {"url": "/alternatives/zoominfo-alternative/", "label": "ZoomInfo Alternative"},
            {"url": "/services/provider-contact-data/", "label": "Provider Contact Data"},
            {"url": "/pricing/", "label": "Provyx Pricing"},
        ],
        "outbound_links": [
            ("https://www.lusha.com/", "Lusha official website"),
            ("https://npiregistry.cms.hhs.gov/", "CMS NPI Registry"),
        ],
    },
    # ===================================================================
    # 6. Cognism Alternative
    # ===================================================================
    {
        "slug": "cognism-alternative",
        "competitor": "Cognism",
        "competitor_url": "https://www.cognism.com/",
        "title": "Best Cognism Alternative for Healthcare Provider Data",
        "meta_description": (
            "Looking for a Cognism alternative for healthcare data? Provyx delivers "
            "NPI-verified US provider contacts with taxonomy filtering, no per-seat "
            "pricing, and no annual contract."
        ),
        "hero_h1": "Best Cognism Alternative for Healthcare Provider Data",
        "hero_subtitle": (
            "Cognism is a European-headquartered B2B data platform known for phone-verified "
            "mobile numbers and GDPR compliance. It works well for European and multi-region "
            "sales teams. For US healthcare provider data, Cognism lacks the NPI verification, "
            "taxonomy filtering, and practice-level detail that specialized teams require. "
            "Provyx fills that gap."
        ),

        "why_switch_heading": "Why US Healthcare Teams Look Beyond Cognism",
        "why_switch_body": (
            "<p><a href=\"https://www.cognism.com/\" target=\"_blank\" rel=\"noopener noreferrer\">Cognism</a> "
            "has carved out a strong position in the European B2B data market. Their Diamond Data product "
            "provides phone-verified mobile numbers, and their GDPR-first approach makes them a natural "
            "choice for teams selling into European markets. They've expanded into the US market, but "
            "healthcare-specific use cases expose their limitations.</p>"

            "<p><strong>Limited US healthcare coverage.</strong> "
            "Cognism's strength is European contact data. Their US database has grown, but healthcare "
            "provider coverage is thinner than US-focused competitors. Healthcare providers often don't "
            "appear in Cognism's database at all, particularly physicians at small and mid-size independent "
            "practices that make up a large share of the US provider market.</p>"

            "<p><strong>No NPI verification.</strong> "
            "Like other general B2B data platforms, Cognism doesn't integrate with the US NPI registry. "
            "Records don't include NPI numbers, so you can't verify that a contact is a licensed healthcare "
            "provider. For teams targeting specific provider types, this is a fundamental gap.</p>"

            "<p><strong>No taxonomy code support.</strong> "
            "Cognism uses job titles and industry codes for filtering, not NUCC healthcare taxonomy codes. "
            "This means you can search for \"physician\" or \"dentist\" by title, but you can't filter for "
            "the specific specialty and sub-specialty codes that healthcare sales teams need for targeted lists.</p>"

            "<p><strong>Pricing designed for enterprise.</strong> "
            "Cognism doesn't publish pricing, but industry reports suggest starting contracts in the range of "
            "$15,000-35,000 annually depending on the package. The platform is seat-based with credit allocations. "
            "For mid-market healthcare sales teams, the cost relative to healthcare-specific value is hard to justify.</p>"

            "<p><strong>European focus doesn't help US healthcare teams.</strong> "
            "Cognism's GDPR expertise and European data strength are irrelevant if your sales territory is "
            "the United States. The platform's core differentiators (phone-verified European mobile numbers, "
            "GDPR compliance workflows) don't translate into healthcare-specific value for US-focused teams.</p>"
        ),

        "what_teams_need_heading": "What US Healthcare Sales Teams Need",
        "what_teams_need_body": (
            "<p>If your team sells to US healthcare providers, your data requirements center on "
            "provider identity, specialty classification, and practice-level contact information.</p>"

            "<p><strong>NPI-verified provider records.</strong> "
            "The <a href=\"https://npiregistry.cms.hhs.gov/\" target=\"_blank\" rel=\"noopener noreferrer\">NPPES NPI Registry</a> "
            "is the source of truth for US healthcare provider identity. Records verified against NPPES "
            "confirm that each contact is a real, licensed provider with an active NPI.</p>"

            "<p><strong>Taxonomy-based specialty filtering.</strong> "
            "800+ NUCC taxonomy codes let you target the exact provider type you need. Title-based "
            "filtering misses providers with non-standard titles and includes false matches.</p>"

            "<p><strong>Practice-level data.</strong> "
            "Direct phone numbers, practice addresses, and office manager contacts for the location "
            "where the provider actually sees patients. Hospital corporate data is insufficient for "
            "reaching providers at independent and small group practices.</p>"

            "<p><strong>US-focused depth over global breadth.</strong> "
            "If your sales territory is the US healthcare market, you need a data source that goes "
            "deep on US providers rather than spreading coverage across 40+ countries. One NPI-verified "
            "US provider record is worth more than 10 unverified European contacts if your team only "
            "sells in the US.</p>"
        ),

        "comparison_heading": "Cognism vs. Provyx: Quick Comparison",
        "comparison_rows": [
            ("Starting Price",
             'Not public, ~$15K+/year <span class="tag tag--red">Enterprise</span>',
             'Pay per record <span class="tag tag--green">No Minimum</span>'),
            ("Geographic Focus",
             'Europe-first, expanding US <span class="tag tag--amber">Global</span>',
             'US healthcare only <span class="tag tag--green">Deep US Coverage</span>'),
            ("NPI Verification",
             'Not included <span class="tag tag--red">No NPI</span>',
             'Every record <span class="tag tag--green">NPI-Verified</span>'),
            ("Taxonomy Filtering",
             'Not available <span class="tag tag--red">Title Only</span>',
             '800+ NUCC codes <span class="tag tag--green">Taxonomy</span>'),
            ("Phone Verification",
             'Diamond Data verified <span class="tag tag--green">Phone-Verified</span>',
             'Practice phone numbers <span class="tag tag--green">Verified</span>'),
            ("Data Model",
             'Contact + Company <span class="tag tag--amber">Company-Centric</span>',
             'Provider + Practice <span class="tag tag--green">Practice-Level</span>'),
            ("Best For",
             "European and multi-region B2B sales",
             "US healthcare provider targeting"),
        ],

        "how_it_works_heading": "How Provyx Works as a Cognism Alternative for US Healthcare",
        "how_it_works_body": (
            "<p>Provyx focuses exclusively on US healthcare provider data. Every record is built from "
            "the NPPES NPI Registry and enriched with practice-level contact information from business "
            "listings and commercial databases.</p>"

            "<h3>US Healthcare Depth</h3>"
            "<p>Where Cognism spreads coverage across industries and geographies, Provyx concentrates on "
            "US healthcare. The result is deeper coverage of the specific provider types that healthcare "
            "sales teams target: physicians, dentists, chiropractors, nurse practitioners, therapists, "
            "and the practices where they work.</p>"

            "<h3>No Platform Required</h3>"
            "<p>Provyx doesn't require you to learn a new platform or pay for seats. Tell us what you need "
            "(specialty, geography, practice type) and receive a custom list delivered as CSV, Excel, or "
            "pushed directly to your CRM. No implementation, no training, no ongoing platform fees.</p>"

            "<h3>Transparent Pricing</h3>"
            "<p>Pay per record. No annual contract. No credit system. No seat-based pricing. "
            "Your entire team can access the data without per-user charges.</p>"
        ),

        "limitations_heading": "What Provyx Doesn't Do",
        "limitations_body": (
            "<p>Provyx covers US healthcare only. If you need European contact data, international "
            "provider information, or GDPR-specific compliance workflows, Cognism is better suited. "
            "Provyx also doesn't offer a sales engagement platform with calling features. For teams "
            "that need an integrated platform with phone verification and dialing tools, Cognism's "
            "all-in-one approach may be preferable.</p>"
        ),

        "who_switches_heading": "Who Switches from Cognism to Provyx",
        "who_switches_body": (
            "<p><strong>US-focused healthcare sales teams</strong> that signed up for Cognism expecting strong provider coverage and found that "
            "US healthcare is a weak spot in Cognism's otherwise solid database. European coverage is strong, but US provider data lacks depth.</p>"
            "<p><strong>Teams that need NPI verification.</strong> Any healthcare sales operation that reports on data quality metrics "
            "needs NPI-verified records. Cognism can't provide this because it doesn't integrate with the US NPI registry.</p>"
            "<p><strong>Medical device and pharma teams</strong> targeting specific specialties. Without taxonomy code support, "
            "Cognism forces these teams to use imprecise title-based filtering that produces noisy, poorly-targeted lists.</p>"
            "<p><strong>Budget-conscious teams.</strong> Cognism's pricing is designed for enterprise buyers. "
            "Mid-market healthcare teams with focused data needs find better value in pay-per-record pricing.</p>"
        ),

        "migration_heading": "How to Switch from Cognism to Provyx for US Healthcare",
        "migration_body": (
            "<p><strong>Step 1: Evaluate your US healthcare data needs.</strong> "
            "If you use Cognism primarily for US healthcare contacts, Provyx is a direct replacement with better healthcare-specific data. "
            "If you use Cognism for European or multi-industry contacts, you'll want to keep it for those use cases.</p>"
            "<p><strong>Step 2: Request a Provyx sample.</strong> "
            "Choose your primary US healthcare specialty and geography. Compare the sample against your Cognism data: "
            "look for NPI verification, taxonomy codes, and practice-level contact details that Cognism doesn't include.</p>"
            "<p><strong>Step 3: Test with your sales team.</strong> "
            "Import Provyx data into your CRM or sales engagement tool. Have reps work both datasets for 2 weeks and compare "
            "connect rates, email deliverability, and lead quality.</p>"
            "<p><strong>Step 4: Adjust your data stack.</strong> "
            "Most teams keep Cognism for European and non-healthcare US contacts while switching to Provyx for US healthcare. "
            "This gives you the best coverage across all markets without paying enterprise pricing for healthcare data "
            "that doesn't meet your quality requirements.</p>"
        ),

        "faqs": [
            {"question": "Is Cognism better than Provyx for healthcare data?",
             "answer": "For US healthcare specifically, no. Cognism's strengths are European coverage and phone-verified mobile numbers. Provyx provides NPI-verified US healthcare data with taxonomy codes and practice-level details that Cognism doesn't offer. For European healthcare or multi-region needs, Cognism may be the better choice."},
            {"question": "Does Cognism have US healthcare provider data?",
             "answer": "Cognism has some US healthcare contacts in their database, but without NPI verification, taxonomy codes, or practice-level data. Coverage is thinner for US healthcare than for European B2B contacts, which is Cognism's primary strength."},
            {"question": "How does pricing compare?",
             "answer": "Cognism contracts reportedly start at $15,000+ annually with seat-based pricing. Provyx charges per record with no annual commitment. For US healthcare data, Provyx delivers more relevant data at a lower total cost. Cognism's pricing makes more sense if you also need European data."},
        ],

        "related_links": [
            {"url": "/compare/provyx-vs-cognism/", "label": "Provyx vs. Cognism Detailed Comparison"},
            {"url": "/alternatives/zoominfo-alternative/", "label": "ZoomInfo Alternative"},
            {"url": "/services/provider-contact-data/", "label": "Provider Contact Data"},
            {"url": "/pricing/", "label": "Provyx Pricing"},
        ],
        "outbound_links": [
            ("https://www.cognism.com/", "Cognism official website"),
            ("https://npiregistry.cms.hhs.gov/", "CMS NPI Registry"),
        ],
    },
]
