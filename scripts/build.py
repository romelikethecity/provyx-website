#!/usr/bin/env python3
"""
Master build script for the Provyx website.

Generates ALL pages (core + programmatic) and sitemap.xml.
Run: python3 scripts/build.py
"""

import os
import sys
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nav_config import (
    NAV_ITEMS, FOOTER_COLUMNS, SITE_NAME, SITE_URL,
    SITE_TAGLINE, COPYRIGHT_YEAR, CTA_HREF, CTA_LABEL,
)
from templates import (
    get_html_head, get_nav_html, get_footer_html,
    get_breadcrumb_schema, get_breadcrumb_html,
    generate_faq_html, generate_cta_section,
    get_page_wrapper, write_page, BASE_URL,
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FORMSPREE_ID = "xpznqkdl"  # placeholder
TODAY = datetime.now().strftime("%Y-%m-%d")

# Track all generated paths for sitemap
ALL_PAGES = []


# =============================================================================
# PROVIDER TAXONOMY DATA
# =============================================================================

CATEGORIES = {
    "mental-health": {
        "name": "Mental Health & Psychiatry",
        "short": "Mental Health",
        "description": "Access verified contact data for psychiatrists, therapists, counselors, and mental health clinics across the US.",
        "hero_title": "Mental Health Provider Data & Contact Lists",
        "intro": "The mental health sector is growing fast, with provider shortages driving demand for accurate contact data. Whether you're selling EHR software to psychiatrists or recruiting therapists for a telehealth platform, you need data that goes beyond a name and address. Our mental health provider database includes direct emails, phone numbers, NPI details, taxonomy codes, and practice information for thousands of verified providers.",
    },
    "chiropractic": {
        "name": "Chiropractic",
        "short": "Chiropractic",
        "description": "Verified chiropractor contact data with NPI, email, phone, and practice details for targeted outreach.",
        "hero_title": "Chiropractor Data & Contact Lists",
        "intro": "Chiropractors operate independently more often than most provider types, which makes them both easier to reach and harder to find accurate data for. Solo practices change addresses, phone numbers, and email systems frequently. Our chiropractic provider database tracks these changes weekly, giving you verified contact data you can actually use for outreach.",
    },
    "dental": {
        "name": "Dental",
        "short": "Dental",
        "description": "Comprehensive dental provider data including general dentists, specialists, and dental labs with verified contacts.",
        "hero_title": "Dental Provider Data & Contact Lists",
        "intro": "Dental practices are among the most fragmented in healthcare. There are over 200,000 practicing dentists in the US, spread across solo practices, group practices, and DSOs. Finding the right contacts with accurate, current information is the difference between a successful campaign and wasted spend. Our dental provider database covers general dentists and every major specialty.",
    },
    "dermatology": {
        "name": "Dermatology",
        "short": "Dermatology",
        "description": "Dermatologist contact data and practice intelligence for medical, cosmetic, and surgical dermatology providers.",
        "hero_title": "Dermatology Provider Data & Contact Lists",
        "intro": "Dermatology sits at the intersection of medical and aesthetic medicine, making it a high-value vertical for device manufacturers, skincare brands, and SaaS vendors. Our dermatology database includes both medical dermatologists and cosmetic-focused practices, with data points that help you segment by practice type, size, and service offerings.",
    },
    "primary-care": {
        "name": "Family & Primary Care",
        "short": "Primary Care",
        "description": "Primary care physician data including family medicine, internal medicine, urgent care, and concierge practices.",
        "hero_title": "Primary Care Provider Data & Contact Lists",
        "intro": "Primary care is the backbone of US healthcare, with hundreds of thousands of family medicine doctors, internists, and urgent care providers. But reaching them is hard. Large health systems gate their providers behind corporate email domains, and independent practices cycle through staff quickly. Our primary care database gives you direct contact paths to decision-makers.",
    },
    "senior-care": {
        "name": "Senior Living & Long Term Care",
        "short": "Senior Care",
        "description": "Senior living facility data including assisted living, memory care, nursing homes, and home health providers.",
        "hero_title": "Senior Care Provider Data & Contact Lists",
        "intro": "The senior care industry spans everything from independent living communities to skilled nursing facilities and hospice providers. Selling into this market requires understanding the difference between facility types and reaching the right administrators. Our senior care database covers the full spectrum with verified decision-maker contacts.",
    },
    "integrative-medicine": {
        "name": "Integrative & Functional Medicine",
        "short": "Integrative Medicine",
        "description": "Functional medicine, naturopathic, and integrative health provider data with verified practice contacts.",
        "hero_title": "Integrative Medicine Provider Data & Contact Lists",
        "intro": "Integrative and functional medicine is one of the fastest-growing segments in healthcare. These providers are early adopters of new therapies, supplements, and technology. They also tend to operate outside traditional health systems, which makes them harder to find in standard provider databases. Our integrative medicine data captures these providers with accurate, verified contact information.",
    },
    "medical-spas": {
        "name": "Medical Spa & Aesthetics",
        "short": "Medical Spas",
        "description": "Medical spa and aesthetic clinic data with owner contacts, service offerings, and practice details.",
        "hero_title": "Medical Spa & Aesthetics Provider Data",
        "intro": "The med spa industry has exploded, with new clinics opening weekly across the country. These businesses blend medical oversight with consumer aesthetics, creating a unique sales environment. Decision-makers are often the medical director or business owner, not a traditional office manager. Our med spa database identifies these contacts directly.",
    },
    "womens-health": {
        "name": "OB/GYN & Women's Health",
        "short": "Women's Health",
        "description": "OB/GYN and women's health provider data including fertility clinics, midwife practices, and specialty care.",
        "hero_title": "Women's Health Provider Data & Contact Lists",
        "intro": "Women's health encompasses OB/GYNs, reproductive endocrinologists, urogynecologists, midwives, and specialty clinics. These providers are high-value targets for medical device companies, pharmaceutical sales teams, and health tech vendors. Our database covers the full spectrum of women's health providers with verified contact data and practice intelligence.",
    },
    "eye-care": {
        "name": "Optometry & Ophthalmology",
        "short": "Eye Care",
        "description": "Optometrist and ophthalmologist data with practice details, specialty focus, and verified contacts.",
        "hero_title": "Eye Care Provider Data & Contact Lists",
        "intro": "Eye care spans two distinct provider types: optometrists who handle routine vision care, and ophthalmologists who perform surgery and treat eye disease. Both are valuable targets for lens manufacturers, ophthalmic device companies, and practice management software vendors. Our eye care database covers both with detailed practice information.",
    },
    "orthopedics": {
        "name": "Orthopedics",
        "short": "Orthopedics",
        "description": "Orthopedic surgeon and sports medicine provider data with subspecialty details and practice contacts.",
        "hero_title": "Orthopedic Provider Data & Contact Lists",
        "intro": "Orthopedic practices are major revenue generators in healthcare, and orthopedic surgeons are among the highest-value contacts for medical device companies. Whether you're selling implants, surgical instruments, or practice management software, reaching the right orthopedic decision-makers requires current, verified data. Our database covers surgeons, sports medicine physicians, and physiatrists.",
    },
    "pain-management": {
        "name": "Pain Management",
        "short": "Pain Management",
        "description": "Pain management clinic and provider data including interventional pain, addiction medicine, and spine specialists.",
        "hero_title": "Pain Management Provider Data & Contact Lists",
        "intro": "Pain management is a complex specialty that spans interventional procedures, medication management, and rehabilitation. These providers are key targets for pharmaceutical companies, medical device manufacturers, and health tech vendors building solutions for chronic pain. Our database covers pain clinics, spine specialists, and addiction medicine providers.",
    },
    "physical-therapy": {
        "name": "Physical Therapy",
        "short": "Physical Therapy",
        "description": "Physical therapy clinic and therapist data with practice details, specialty focus, and verified contacts.",
        "hero_title": "Physical Therapy Provider Data & Contact Lists",
        "intro": "Physical therapy practices range from large multi-location chains to solo practitioners. The industry is highly fragmented, with thousands of independent clinics competing alongside hospital-owned and corporate-backed groups. Our PT database helps you identify and reach practice owners and clinic directors with verified contact information.",
    },
    "plastic-surgery": {
        "name": "Plastic Surgery",
        "short": "Plastic Surgery",
        "description": "Plastic surgeon and cosmetic surgery practice data with verified contacts and practice intelligence.",
        "hero_title": "Plastic Surgery Provider Data & Contact Lists",
        "intro": "Plastic surgeons are high-value contacts for medical device companies, aesthetic product distributors, and marketing agencies. These practices spend significantly on equipment, supplies, and patient acquisition. Reaching the surgeon or practice owner directly is critical. Our database provides verified contact data for cosmetic and reconstructive plastic surgeons.",
    },
    "rheumatology": {
        "name": "Rheumatology",
        "short": "Rheumatology",
        "description": "Rheumatologist contact data for arthritis, autoimmune disease, and inflammatory condition specialists.",
        "hero_title": "Rheumatology Provider Data & Contact Lists",
        "intro": "Rheumatologists treat complex autoimmune and inflammatory conditions, making them high-priority targets for pharmaceutical companies and clinical research organizations. With a limited number of practicing rheumatologists in the US, accurate contact data is especially valuable. Our database covers rheumatology practices with verified emails, phone numbers, and practice details.",
    },
    "weight-loss": {
        "name": "Weight Loss",
        "short": "Weight Loss",
        "description": "Weight loss clinic and bariatric provider data including GLP-1 prescribers, nutritionists, and obesity medicine.",
        "hero_title": "Weight Loss Provider Data & Contact Lists",
        "intro": "The weight loss industry is being transformed by GLP-1 medications like semaglutide and tirzepatide. New clinics and prescribers are entering the market monthly, and existing practices are adding weight management services. Our database tracks this rapidly evolving landscape with verified provider contacts, including GLP-1 prescribers, bariatric surgeons, and obesity medicine specialists.",
    },
    "neurology": {
        "name": "Neurology",
        "short": "Neurology",
        "description": "Neurologist and neurosurgeon contact data with subspecialty details and practice information.",
        "hero_title": "Neurology Provider Data & Contact Lists",
        "intro": "Neurologists treat conditions affecting the brain and nervous system, from epilepsy and multiple sclerosis to headache disorders and neurodegenerative diseases. They are critical contacts for pharmaceutical companies and neurodiagnostic device manufacturers. Our neurology database provides verified contact data for neurologists and neurosurgeons across the US.",
    },
}

# Subtypes: (slug, name, category_key, synonyms_list, description)
SUBTYPES = [
    # Mental Health
    ("psychiatrists", "Psychiatrists", "mental-health", ["psychiatry"],
     "Verified psychiatrist contact data including direct emails, phone numbers, NPI details, and practice information for targeted outreach campaigns."),
    ("psychiatric-nurse-practitioners", "Psychiatric Nurse Practitioners", "mental-health", ["MHNP", "psychiatric NP"],
     "Contact data for psychiatric nurse practitioners providing medication management and mental health treatment services."),
    ("psychotherapists", "Psychotherapists", "mental-health", [],
     "Psychotherapist contact data with practice details, specialty focus areas, and verified email and phone information."),
    ("counselors", "Counselors", "mental-health", ["licensed counselors", "LPC"],
     "Licensed counselor contact data for outreach to individual, family, and group therapy providers."),
    ("therapists", "Therapists", "mental-health", ["licensed therapists"],
     "Therapist directory data including LMFTs, LCSWs, and other licensed mental health professionals."),
    ("ketamine-clinics", "Ketamine Clinics", "mental-health", ["ketamine therapy", "ketamine infusion"],
     "Ketamine clinic and infusion center data for providers offering ketamine-assisted therapy for depression and pain."),
    ("spravato-providers", "Spravato Providers", "mental-health", ["esketamine"],
     "Contact data for REMS-certified Spravato (esketamine) prescribers and treatment centers."),
    ("tms-therapy", "TMS Therapy Providers", "mental-health", ["transcranial magnetic stimulation"],
     "TMS therapy provider data for clinics offering transcranial magnetic stimulation for depression treatment."),
    ("depression-treatment-centers", "Depression Treatment Centers", "mental-health", [],
     "Depression treatment center data including outpatient programs, intensive outpatient, and partial hospitalization."),
    ("anxiety-treatment", "Anxiety Treatment Providers", "mental-health", [],
     "Anxiety treatment provider data for clinics and practitioners specializing in anxiety disorder care."),
    ("mental-health-clinics", "Mental Health Clinics", "mental-health", [],
     "Multi-provider mental health clinic data with administrator contacts and practice details."),
    ("community-mental-health", "Community Mental Health Centers", "mental-health", ["CMHC"],
     "Community mental health center data including federally funded and nonprofit behavioral health organizations."),
    ("crisis-centers", "Crisis Centers", "mental-health", ["crisis intervention"],
     "Crisis center and intervention program data for behavioral health emergency service providers."),
    # Chiropractic
    ("chiropractors", "Chiropractors", "chiropractic", ["chiropractic clinic", "chiropractic wellness"],
     "Chiropractor contact data with verified emails, direct phone numbers, NPI records, and practice details."),
    ("sports-chiropractors", "Sports Chiropractors", "chiropractic", [],
     "Sports chiropractic provider data for practitioners specializing in athletic injury treatment and performance."),
    ("functional-chiropractors", "Functional Chiropractors", "chiropractic", [],
     "Functional chiropractic provider data for practitioners combining chiropractic care with functional medicine."),
    ("integrative-chiropractic", "Integrative Chiropractors", "chiropractic", [],
     "Integrative chiropractic provider data for practices offering holistic and multi-disciplinary care."),
    ("mobile-chiropractors", "Mobile Chiropractors", "chiropractic", [],
     "Mobile chiropractic provider data for practitioners offering on-site and house-call chiropractic services."),
    # Dental
    ("cosmetic-dentists", "Cosmetic Dentists", "dental", ["aesthetic dentist"],
     "Cosmetic dentist contact data for practices specializing in veneers, whitening, smile makeovers, and aesthetic procedures."),
    ("general-dentists", "General Dentists", "dental", ["family dentist", "general dentistry"],
     "General dentist contact data with verified emails, phone numbers, and practice details for the largest dental segment."),
    ("orthodontists", "Orthodontists", "dental", [],
     "Orthodontist contact data for providers offering braces, Invisalign, and other alignment treatments."),
    ("oral-surgeons", "Oral Surgeons", "dental", ["oral and maxillofacial surgery"],
     "Oral surgeon contact data including maxillofacial surgery practices with verified decision-maker contacts."),
    ("tmj-specialists", "TMJ Specialists", "dental", ["TMJ dentist", "TMD treatment"],
     "TMJ specialist contact data for dentists and clinics treating temporomandibular joint disorders."),
    ("holistic-dentists", "Holistic Dentists", "dental", ["biological dentist"],
     "Holistic and biological dentist data for practitioners offering mercury-free, biocompatible dental care."),
    ("dental-spas", "Dental Spas", "dental", [],
     "Dental spa contact data for practices combining dental care with spa-like patient experiences."),
    ("neuromuscular-dentists", "Neuromuscular Dentists", "dental", [],
     "Neuromuscular dentist data for practitioners specializing in jaw alignment and bite optimization."),
    ("sedation-dentistry", "Sedation Dentistry Providers", "dental", [],
     "Sedation dentistry provider data for practices offering IV sedation, oral sedation, and nitrous oxide services."),
    ("periodontists", "Periodontists", "dental", [],
     "Periodontist contact data for gum disease specialists with verified practice contacts."),
    ("endodontists", "Endodontists", "dental", [],
     "Endodontist contact data for root canal specialists with practice details and verified contacts."),
    ("pediatric-dentists", "Pediatric Dentists", "dental", [],
     "Pediatric dentist contact data for children's dental practices with decision-maker information."),
    ("prosthodontists", "Prosthodontists", "dental", [],
     "Prosthodontist data for dental prosthetics specialists including implant, crown, and denture providers."),
    ("oral-pathologists", "Oral Pathologists", "dental", [],
     "Oral pathologist data for providers specializing in diagnosis of oral and maxillofacial diseases."),
    ("dental-laboratories", "Dental Laboratories", "dental", ["dental lab"],
     "Dental laboratory data with owner contacts, services offered, and technology capabilities."),
    ("emergency-dentists", "Emergency Dentists", "dental", [],
     "Emergency dentist data for practices offering same-day and after-hours dental care services."),
    # Dermatology
    ("dermatologists", "Dermatologists", "dermatology", ["dermatology clinic", "medical dermatology"],
     "Dermatologist contact data with specialty focus, practice size, and verified email and phone information."),
    ("cosmetic-dermatologists", "Cosmetic Dermatologists", "dermatology", [],
     "Cosmetic dermatology provider data for practices focused on aesthetic skin treatments and procedures."),
    ("skin-care-clinics", "Skin Care Clinics", "dermatology", [],
     "Skin care clinic data for medical and aesthetic practices offering comprehensive skin treatment services."),
    ("mohs-surgeons", "Mohs Surgeons", "dermatology", ["Mohs micrographic surgery"],
     "Mohs surgery provider data for dermatologists specializing in skin cancer removal with margin control."),
    ("pediatric-dermatologists", "Pediatric Dermatologists", "dermatology", [],
     "Pediatric dermatologist data for providers treating skin conditions in infants, children, and adolescents."),
    ("dermatopathologists", "Dermatopathologists", "dermatology", [],
     "Dermatopathologist data for providers specializing in microscopic diagnosis of skin diseases."),
    # Primary Care
    ("family-medicine", "Family Medicine Physicians", "primary-care", ["family doctor"],
     "Family medicine physician data with verified contacts for providers serving patients of all ages."),
    ("primary-care-physicians", "Primary Care Physicians", "primary-care", ["PCP"],
     "Primary care physician contact data with practice details, panel size indicators, and direct contact paths."),
    ("internal-medicine", "Internal Medicine Physicians", "primary-care", ["internist"],
     "Internal medicine physician data for providers specializing in adult primary and preventive care."),
    ("concierge-medicine", "Concierge Medicine Practices", "primary-care", ["membership medicine"],
     "Concierge medicine practice data for membership-based primary care providers with verified owner contacts."),
    ("direct-primary-care", "Direct Primary Care Practices", "primary-care", ["DPC"],
     "Direct primary care practice data for subscription-based clinics operating outside traditional insurance models."),
    ("urgent-care", "Urgent Care Centers", "primary-care", ["walk-in clinic"],
     "Urgent care center data with administrator contacts, locations, services, and ownership information."),
    ("community-health-centers", "Community Health Centers", "primary-care", ["FQHC"],
     "Federally qualified health center data with administrator contacts and service area details."),
    # Senior Care
    ("independent-living", "Independent Living Communities", "senior-care", ["senior living", "retirement community", "55+ community"],
     "Independent living community data with administrator contacts, capacity, and amenity information."),
    ("assisted-living", "Assisted Living Facilities", "senior-care", [],
     "Assisted living facility data with administrator contacts, bed count, and care level details."),
    ("memory-care", "Memory Care Facilities", "senior-care", ["dementia care", "Alzheimer's care"],
     "Memory care facility data for providers specializing in dementia and Alzheimer's residential care."),
    ("nursing-homes", "Nursing Homes", "senior-care", ["skilled nursing facility", "SNF", "long term care"],
     "Nursing home and skilled nursing facility data with administrator contacts and quality metrics."),
    ("rehabilitation-centers", "Rehabilitation Centers", "senior-care", ["subacute care", "rehab center"],
     "Rehabilitation center data for inpatient and outpatient post-acute care facilities."),
    ("hospice", "Hospice Providers", "senior-care", ["hospice care", "end of life care"],
     "Hospice provider data with director contacts, service areas, and organizational details."),
    ("home-health", "Home Health Agencies", "senior-care", ["home care", "home health care"],
     "Home health agency data with administrator contacts, service areas, and care type details."),
    # Integrative Medicine
    ("integrative-medicine-doctors", "Integrative Medicine Doctors", "integrative-medicine", [],
     "Integrative medicine physician data for MDs and DOs practicing whole-person, evidence-based integrative care."),
    ("functional-medicine-doctors", "Functional Medicine Doctors", "integrative-medicine", [],
     "Functional medicine doctor data for providers focused on root-cause analysis and systems biology approaches."),
    ("naturopathic-doctors", "Naturopathic Doctors", "integrative-medicine", ["naturopath", "ND"],
     "Naturopathic doctor data with verified contacts for licensed naturopathic physicians."),
    ("holistic-medicine", "Holistic Medicine Providers", "integrative-medicine", [],
     "Holistic medicine provider data for practitioners offering whole-body health and wellness services."),
    ("regenerative-medicine", "Regenerative Medicine Providers", "integrative-medicine", ["stem cell therapy"],
     "Regenerative medicine provider data for clinics offering PRP, stem cell, and tissue repair therapies."),
    ("anti-aging-clinics", "Anti-Aging Clinics", "integrative-medicine", ["longevity clinic"],
     "Anti-aging and longevity clinic data for providers offering age management and optimization services."),
    ("wellness-clinics", "Wellness Clinics", "integrative-medicine", ["wellness center"],
     "Wellness clinic data for integrative health centers offering preventive and lifestyle medicine."),
    ("iv-therapy-clinics", "IV Therapy Clinics", "integrative-medicine", ["IV drip bar", "infusion clinic"],
     "IV therapy clinic data for providers offering intravenous vitamin, hydration, and nutrient infusions."),
    ("hormone-therapy", "Hormone Therapy Providers", "integrative-medicine", ["bioidentical hormones", "HRT", "BHRT"],
     "Hormone replacement therapy provider data for clinics offering bioidentical and traditional HRT services."),
    ("peptide-therapy", "Peptide Therapy Providers", "integrative-medicine", [],
     "Peptide therapy provider data for clinics offering therapeutic peptide treatments for health optimization."),
    ("homeopaths", "Homeopaths", "integrative-medicine", ["homeopathic medicine"],
     "Homeopathic provider data for practitioners offering classical and clinical homeopathy services."),
    ("acupuncturists", "Acupuncturists", "integrative-medicine", ["acupuncture clinic"],
     "Acupuncturist contact data with practice details, certifications, and verified contact information."),
    # Medical Spas
    ("med-spas", "Medical Spas", "medical-spas", ["med spa", "medspa", "medical spa"],
     "Medical spa contact data with owner and medical director contacts, service menus, and practice details."),
    ("aesthetic-clinics", "Aesthetic Clinics", "medical-spas", ["cosmetic clinic"],
     "Aesthetic clinic data for practices offering injectable, laser, and non-surgical cosmetic treatments."),
    ("laser-clinics", "Laser Clinics", "medical-spas", ["laser center"],
     "Laser clinic data for providers offering laser hair removal, skin resurfacing, and phototherapy treatments."),
    ("body-contouring", "Body Contouring Providers", "medical-spas", ["CoolSculpting provider"],
     "Body contouring provider data for clinics offering CoolSculpting, lipolysis, and non-surgical fat reduction."),
    ("botox-clinics", "Botox Clinics", "medical-spas", ["neurotoxin injector"],
     "Botox and neurotoxin provider data for clinics offering injectable wrinkle treatments and facial aesthetics."),
    ("iv-lounges", "IV Lounges", "medical-spas", ["IV bar"],
     "IV lounge and hydration bar data for consumer-facing wellness infusion providers."),
    ("skin-clinics", "Skin Clinics", "medical-spas", [],
     "Skin clinic data for medical aesthetics practices focused on comprehensive skin health and treatment."),
    # Women's Health
    ("obgyn", "OBGYNs", "womens-health", ["OB/GYN", "obstetrician gynecologist"],
     "OB/GYN contact data with practice details, subspecialty focus, and verified decision-maker contacts."),
    ("gynecologists", "Gynecologists", "womens-health", [],
     "Gynecologist contact data for providers focused on women's reproductive health and preventive care."),
    ("womens-health-clinics", "Women's Health Clinics", "womens-health", ["women's wellness"],
     "Women's health clinic data for multi-provider practices offering comprehensive women's care services."),
    ("urogynecologists", "Urogynecologists", "womens-health", [],
     "Urogynecologist data for specialists treating pelvic floor disorders and urinary incontinence."),
    ("pelvic-floor-specialists", "Pelvic Floor Specialists", "womens-health", ["incontinence treatment"],
     "Pelvic floor specialist data for providers offering pelvic floor therapy and reconstructive care."),
    ("menopause-clinics", "Menopause Clinics", "womens-health", ["menopause specialist"],
     "Menopause clinic data for providers specializing in perimenopause and menopause management."),
    ("midwife-practices", "Midwife Practices", "womens-health", ["CNM", "certified nurse midwife"],
     "Midwife practice data for certified nurse midwives and midwifery birth centers."),
    ("fertility-clinics", "Fertility Clinics", "womens-health", ["reproductive endocrinology", "IVF clinic"],
     "Fertility clinic data for reproductive endocrinology practices offering IVF, IUI, and fertility treatments."),
    # Eye Care
    ("optometrists", "Optometrists", "eye-care", ["eye doctor", "vision center", "eye care center"],
     "Optometrist contact data with practice type, services offered, and verified contact information."),
    ("dry-eye-specialists", "Dry Eye Specialists", "eye-care", ["dry eye clinic"],
     "Dry eye specialist data for providers offering IPL, LipiFlow, and advanced dry eye treatments."),
    ("ophthalmologists", "Ophthalmologists", "eye-care", ["eye surgeon"],
     "Ophthalmologist data with subspecialty focus, surgical capabilities, and verified practice contacts."),
    ("lasik-centers", "LASIK Centers", "eye-care", ["refractive surgery"],
     "LASIK and refractive surgery center data with surgeon contacts and procedure volume information."),
    ("oculoplastic-surgeons", "Oculoplastic Surgeons", "eye-care", [],
     "Oculoplastic surgeon data for specialists performing eyelid, orbital, and facial cosmetic surgery."),
    # Orthopedics
    ("orthopedic-surgeons", "Orthopedic Surgeons", "orthopedics", ["orthopedic clinic"],
     "Orthopedic surgeon contact data with subspecialty focus, hospital affiliations, and practice details."),
    ("sports-medicine", "Sports Medicine Providers", "orthopedics", ["sports medicine doctor", "sports injury clinic"],
     "Sports medicine provider data for physicians treating athletic injuries and performance conditions."),
    ("spine-surgeons", "Spine Surgeons", "orthopedics", ["spine specialist"],
     "Spine surgeon data for providers performing spinal fusion, disc replacement, and minimally invasive procedures."),
    ("joint-replacement", "Joint Replacement Surgeons", "orthopedics", ["hip replacement", "knee replacement"],
     "Joint replacement surgeon data for providers performing hip, knee, and shoulder arthroplasty."),
    ("physiatrists", "Physiatrists", "orthopedics", ["physical medicine rehabilitation", "PM&R"],
     "Physiatrist data for physical medicine and rehabilitation physicians with practice contacts."),
    # Pain Management
    ("pain-clinics", "Pain Clinics", "pain-management", ["pain management", "pain specialist"],
     "Pain clinic contact data with physician contacts, treatment modalities, and practice details."),
    ("interventional-pain", "Interventional Pain Providers", "pain-management", [],
     "Interventional pain medicine provider data for physicians performing injections, nerve blocks, and spinal procedures."),
    ("chronic-pain-treatment", "Chronic Pain Treatment Centers", "pain-management", ["back pain clinic"],
     "Chronic pain treatment center data for multi-disciplinary practices managing long-term pain conditions."),
    ("spine-clinics", "Spine Clinics", "pain-management", [],
     "Spine clinic data for practices specializing in non-surgical and surgical spine care."),
    ("regenerative-pain", "Regenerative Pain Providers", "pain-management", ["PRP therapy", "stem cell therapy"],
     "Regenerative pain medicine provider data for clinics offering PRP, prolotherapy, and stem cell treatments."),
    ("addiction-medicine", "Addiction Medicine Providers", "pain-management", ["suboxone clinic", "methadone clinic", "MAT provider"],
     "Addiction medicine provider data for MAT clinics and substance use disorder treatment centers."),
    # Physical Therapy
    ("physical-therapists", "Physical Therapists", "physical-therapy", ["PT clinic"],
     "Physical therapist and PT clinic data with practice owner contacts and location details."),
    ("sports-physical-therapy", "Sports Physical Therapy", "physical-therapy", [],
     "Sports physical therapy clinic data for practices specializing in athletic rehabilitation and injury prevention."),
    ("orthopedic-physical-therapy", "Orthopedic Physical Therapy", "physical-therapy", [],
     "Orthopedic PT practice data for clinics focused on post-surgical rehab and musculoskeletal conditions."),
    ("pelvic-floor-physical-therapy", "Pelvic Floor Physical Therapy", "physical-therapy", ["women's health PT"],
     "Pelvic floor physical therapy provider data for clinics treating pelvic pain and incontinence."),
    ("aquatic-therapy", "Aquatic Therapy Providers", "physical-therapy", ["pool therapy"],
     "Aquatic therapy provider data for PT clinics offering pool-based rehabilitation programs."),
    ("manual-therapy", "Manual Therapy Providers", "physical-therapy", [],
     "Manual therapy provider data for physical therapists specializing in hands-on treatment techniques."),
    ("home-health-physical-therapy", "Home Health Physical Therapy", "physical-therapy", [],
     "Home health PT provider data for therapists offering in-home rehabilitation services."),
    # Plastic Surgery
    ("plastic-surgeons", "Plastic Surgeons", "plastic-surgery", ["cosmetic surgeon", "aesthetic surgeon"],
     "Plastic surgeon contact data with subspecialty focus, board certifications, and practice details."),
    ("facial-plastic-surgeons", "Facial Plastic Surgeons", "plastic-surgery", [],
     "Facial plastic surgeon data for providers specializing in rhinoplasty, facelift, and facial rejuvenation."),
    ("body-contouring-surgeons", "Body Contouring Surgeons", "plastic-surgery", ["liposuction"],
     "Body contouring surgeon data for providers offering liposuction, tummy tuck, and body sculpting procedures."),
    ("breast-augmentation", "Breast Augmentation Surgeons", "plastic-surgery", [],
     "Breast augmentation surgeon data for providers performing implant and fat transfer breast procedures."),
    ("tummy-tuck-surgeons", "Tummy Tuck Surgeons", "plastic-surgery", ["abdominoplasty"],
     "Tummy tuck surgeon data for providers performing abdominoplasty and body contouring procedures."),
    ("mommy-makeover", "Mommy Makeover Surgeons", "plastic-surgery", [],
     "Mommy makeover surgeon data for providers offering combined post-pregnancy body restoration procedures."),
    ("reconstructive-surgeons", "Reconstructive Surgeons", "plastic-surgery", [],
     "Reconstructive surgeon data for providers performing post-cancer, trauma, and congenital repair procedures."),
    # Rheumatology
    ("rheumatologists", "Rheumatologists", "rheumatology", ["rheumatology clinic"],
     "Rheumatologist contact data with subspecialty focus, prescribing patterns, and practice details."),
    ("arthritis-specialists", "Arthritis Specialists", "rheumatology", [],
     "Arthritis specialist data for providers treating rheumatoid arthritis, osteoarthritis, and joint diseases."),
    ("autoimmune-specialists", "Autoimmune Specialists", "rheumatology", ["lupus specialist"],
     "Autoimmune disease specialist data for providers treating lupus, scleroderma, and vasculitis."),
    ("fibromyalgia-treatment", "Fibromyalgia Treatment Providers", "rheumatology", [],
     "Fibromyalgia treatment provider data for clinics specializing in chronic widespread pain management."),
    # Weight Loss
    ("weight-loss-clinics", "Weight Loss Clinics", "weight-loss", ["medical weight loss", "weight management"],
     "Medical weight loss clinic data with physician contacts, program details, and treatment modalities."),
    ("bariatric-clinics", "Bariatric Clinics", "weight-loss", [],
     "Bariatric clinic data for non-surgical weight management programs with medical oversight."),
    ("glp1-providers", "GLP-1 Providers", "weight-loss", ["semaglutide", "Ozempic", "Wegovy", "tirzepatide"],
     "GLP-1 medication prescriber data for providers offering semaglutide, tirzepatide, and related weight loss drugs."),
    ("body-transformation-clinics", "Body Transformation Clinics", "weight-loss", [],
     "Body transformation clinic data for medically supervised weight loss and body composition programs."),
    ("obesity-medicine", "Obesity Medicine Specialists", "weight-loss", ["metabolic health"],
     "Obesity medicine specialist data for ABOM-certified physicians treating metabolic and weight conditions."),
    ("bariatric-surgery", "Bariatric Surgery Centers", "weight-loss", ["bariatric surgery center"],
     "Bariatric surgery center data for providers performing gastric bypass, sleeve, and revision procedures."),
    ("nutritionists", "Nutritionists & Dietitians", "weight-loss", ["dietitian", "RD", "registered dietitian"],
     "Nutritionist and registered dietitian data with practice contacts, specialties, and service details."),
    # Neurology
    ("neurologists", "Neurologists", "neurology", ["neurology practice"],
     "Neurologist contact data with subspecialty focus, treatment areas, and verified practice contacts."),
    ("neurosurgeons", "Neurosurgeons", "neurology", ["brain surgeon"],
     "Neurosurgeon contact data with surgical focus areas, hospital affiliations, and practice details."),
]

# ICP audience pages
ICP_PAGES = [
    {
        "slug": "healthcare-marketing-agencies",
        "name": "Healthcare Marketing Agencies",
        "title": "Provider Data for Healthcare Marketing Agencies",
        "description": "Build targeted provider lists for your healthcare marketing clients. Verified emails, phones, and practice data.",
        "intro": "Your clients need patients. You need provider data to build referral networks, run outreach campaigns, and target the right practices. Generic B2B databases don't understand healthcare taxonomy codes, practice types, or provider specialties. Provyx gives you the provider-level data that makes campaigns actually work.",
        "use_cases": ["Build targeted email lists by specialty and geography", "Identify practices for digital advertising campaigns", "Create referral network maps for health systems", "Segment providers by practice size and technology stack"],
    },
    {
        "slug": "medical-device-sales",
        "name": "Medical Device Sales Teams",
        "title": "Provider Data for Medical Device Sales Teams",
        "description": "Find and reach the right physicians and practice decision-makers. NPI-verified provider contact data.",
        "intro": "Medical device sales teams waste hours tracking down the right contact at a practice. Is it the surgeon? The office manager? The purchasing director? Provyx gives you direct contacts for healthcare decision-makers, organized by specialty, procedure volume, and practice type so you can focus on selling instead of prospecting.",
        "use_cases": ["Identify surgeons by subspecialty and procedure focus", "Find practice decision-makers with direct contact paths", "Build territory lists by geography and provider density", "Track provider movements between practices and health systems"],
    },
    {
        "slug": "healthcare-saas",
        "name": "Healthcare SaaS Vendors",
        "title": "Provider Data for Healthcare SaaS Companies",
        "description": "Target the right practices for your healthcare software. Segment by specialty, size, and technology stack.",
        "intro": "Selling software to healthcare practices means understanding which practices are actually a fit for your product. A 2-provider dermatology clinic has different needs than a 50-provider orthopedic group. Provyx helps you segment the market by practice size, specialty, current technology, and decision-maker role so your outreach hits the right targets.",
        "use_cases": ["Segment practices by size, specialty, and EHR system", "Identify practices using competitor technology", "Build ICP-matched prospect lists for SDR teams", "Track new practice openings and ownership changes"],
    },
    {
        "slug": "pharma-sales",
        "name": "Pharma Sales Teams",
        "title": "Provider Data for Pharmaceutical Sales",
        "description": "NPI-verified prescriber data for pharmaceutical sales targeting. Reach the right physicians with accurate contacts.",
        "intro": "Pharmaceutical sales teams need prescriber-level data that's accurate, current, and organized by specialty and prescribing relevance. Provyx provides NPI-verified physician contacts with practice details that help you prioritize the providers most likely to prescribe your products.",
        "use_cases": ["Build prescriber target lists by specialty and geography", "Identify high-volume prescribers in therapeutic areas", "Map provider relationships within health systems", "Track new providers entering your target specialties"],
    },
    {
        "slug": "medical-staffing",
        "name": "Medical Staffing Agencies",
        "title": "Provider Data for Medical Staffing Agencies",
        "description": "Find healthcare facilities and hiring decision-makers. Verified contacts for staffing and recruiting outreach.",
        "intro": "Medical staffing agencies need two things: facilities that hire, and providers available to work. Provyx helps with the first part by giving you verified contacts for practice administrators, office managers, and hiring decision-makers at healthcare facilities across every specialty.",
        "use_cases": ["Identify facilities actively hiring by specialty", "Reach practice administrators and hiring managers directly", "Build prospect lists for new market expansion", "Track facility openings and ownership changes"],
    },
    {
        "slug": "healthcare-consulting",
        "name": "Healthcare Consulting Firms",
        "title": "Provider Data for Healthcare Consulting",
        "description": "Market intelligence for healthcare consulting engagements. Provider demographics, practice data, and market analysis.",
        "intro": "Healthcare consulting firms need reliable market data to size opportunities, benchmark competitors, and support strategic recommendations. Provyx provides the provider-level data that powers market analysis, competitive intelligence, and go-to-market strategy for healthcare-focused engagements.",
        "use_cases": ["Size addressable markets by specialty and geography", "Analyze provider density and competition", "Support M&A due diligence with practice data", "Build market entry strategies for healthcare clients"],
    },
    {
        "slug": "health-it",
        "name": "Health IT Companies",
        "title": "Provider Data for Health IT Companies",
        "description": "Target healthcare practices for your health IT solutions. Technology detection, practice data, and decision-maker contacts.",
        "intro": "Health IT companies selling EHR systems, practice management software, telehealth platforms, or revenue cycle tools need to know what technology practices currently use. Provyx combines provider contact data with technology detection, so you can target practices running your competitors' systems or practices with no system at all.",
        "use_cases": ["Identify practices using specific EHR or PM systems", "Target practices without modern technology infrastructure", "Build competitive displacement campaigns", "Segment by practice size and technology readiness"],
    },
]

# Comparison pages
COMPARISONS = [
    {
        "slug": "provyx-vs-zoominfo",
        "competitor": "ZoomInfo",
        "title": "Provyx vs ZoomInfo for Healthcare Data",
        "description": "Compare Provyx and ZoomInfo for healthcare provider data. See why healthcare-focused data outperforms generic B2B databases.",
        "competitor_cons": ["Generic B2B database not built for healthcare", "Provider data is a small fraction of their total dataset", "No NPI verification or taxonomy code filtering", "Expensive enterprise contracts with healthcare as an add-on"],
        "provyx_pros": ["Built specifically for healthcare provider data", "NPI-verified with taxonomy code segmentation", "Practice-level intelligence beyond basic contacts", "Pricing designed for healthcare data buyers"],
    },
    {
        "slug": "provyx-vs-definitive-healthcare",
        "competitor": "Definitive Healthcare",
        "title": "Provyx vs Definitive Healthcare",
        "description": "Compare Provyx and Definitive Healthcare for provider contact data. Purpose-built intelligence vs enterprise platform.",
        "competitor_cons": ["Enterprise pricing starting at $30K+ annually", "Complex platform with steep learning curve", "Hospital and health system focus over individual providers", "Long sales cycle and annual contract commitments"],
        "provyx_pros": ["Accessible pricing for teams of any size", "Simple data delivery without platform complexity", "Strong individual provider and practice-level data", "Flexible engagement from one-time lists to ongoing feeds"],
    },
    {
        "slug": "provyx-vs-apollo",
        "competitor": "Apollo",
        "title": "Provyx vs Apollo for Healthcare Data",
        "description": "Compare Provyx and Apollo.io for healthcare provider outreach. Specialized healthcare data vs general sales intelligence.",
        "competitor_cons": ["General purpose sales tool not designed for healthcare", "Healthcare provider coverage is shallow and unverified", "No NPI data, taxonomy codes, or practice intelligence", "Email data quality varies significantly for healthcare contacts"],
        "provyx_pros": ["Healthcare-first database with deep provider coverage", "NPI-verified contacts with specialty taxonomy data", "Practice-level details generic tools can't provide", "Data quality validated against public healthcare registries"],
    },
]

# Alternative pages
ALTERNATIVES = [
    {
        "slug": "zoominfo-alternative",
        "competitor": "ZoomInfo",
        "title": "Best ZoomInfo Alternative for Healthcare Data",
        "description": "Looking for a ZoomInfo alternative for healthcare provider data? Provyx offers specialized, NPI-verified provider contacts.",
    },
    {
        "slug": "definitive-healthcare-alternative",
        "competitor": "Definitive Healthcare",
        "title": "Best Definitive Healthcare Alternative",
        "description": "Need a Definitive Healthcare alternative? Provyx provides accessible healthcare provider data without enterprise pricing.",
    },
]


# =============================================================================
# PAGE GENERATORS - CORE PAGES
# =============================================================================

def build_homepage():
    """Generate index.html"""
    schema = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "name": SITE_NAME,
                "url": BASE_URL,
                "description": "Healthcare provider intelligence and contact data for B2B sales, marketing, and analytics teams.",
                "foundingDate": "2026",
                "areaServed": "United States",
                "knowsAbout": ["Healthcare Provider Data", "B2B Data Enrichment", "Provider Contact Intelligence", "Medical Practice Data", "NPI Registry Data"],
            },
            {
                "@type": "WebSite",
                "name": SITE_NAME,
                "url": BASE_URL,
            }
        ]
    }, indent=2)
    extra_schema = f'''
    <script type="application/ld+json">
{schema}
    </script>'''

    faqs = [
        {"question": "What kind of healthcare provider data does Provyx offer?",
         "answer": "We provide verified contact data for healthcare providers across 40+ specialties. This includes direct emails, phone numbers, NPI details, taxonomy codes, practice addresses, and firmographic data like practice size and technology stack."},
        {"question": "Where does Provyx source its provider data?",
         "answer": "Our data comes from public registries including the CMS NPI Registry, state licensing boards, commercial databases, and proprietary web intelligence. Every record is verified against multiple sources before delivery."},
        {"question": "How often is the provider data updated?",
         "answer": "We refresh our database weekly. Provider contact information changes frequently as staff turn over and practices move. Weekly updates ensure you're working with current data, not records that are months old."},
        {"question": "Can I get a custom provider list for my specific needs?",
         "answer": "Yes. We build custom lists filtered by specialty, geography, practice size, technology stack, and other criteria. Tell us what you're targeting and we'll build a matched list."},
        {"question": "How is Provyx different from ZoomInfo or Apollo?",
         "answer": "Generic B2B databases treat healthcare as one of many industries. Provyx is built specifically for healthcare provider data. We verify against NPI registries, segment by medical taxonomy codes, and include practice-level details that general databases don't capture."},
    ]

    # Build category cards for the hub links on homepage
    cat_cards = ""
    for key, cat in list(CATEGORIES.items())[:6]:
        cat_cards += f'''
                <a href="/providers/{key}/" class="service-card">
                    <h3 class="service-card__title">{cat["short"]}</h3>
                    <p class="service-card__text">{cat["description"][:120]}...</p>
                </a>'''

    body = f'''
        <section class="hero section">
            <div class="container hero__content">
                <h1 class="hero__title">Find Any Healthcare Provider. Get Their Data.</h1>
                <p class="hero__subtitle">Verified contact data for 40+ healthcare specialties. NPI-verified emails, phones, practice details, and technology data. Updated weekly.</p>
                <div class="hero__buttons">
                    <a href="/contact/" class="btn btn--primary btn--lg">Get Provider Data</a>
                    <a href="/providers/" class="btn btn--secondary btn--lg">Browse Specialties</a>
                </div>
                <div class="pain-stats">
                    <div class="pain-stat"><span class="pain-stat__number">2.4M+</span><span class="pain-stat__label">Provider Records</span></div>
                    <div class="pain-stat"><span class="pain-stat__number">40+</span><span class="pain-stat__label">Specialties</span></div>
                    <div class="pain-stat"><span class="pain-stat__number">Weekly</span><span class="pain-stat__label">Data Refresh</span></div>
                </div>
            </div>
        </section>

        <section class="section problems">
            <div class="container">
                <div class="problems__header">
                    <h2>Healthcare Data Is Broken</h2>
                    <p class="section__subtitle">Most B2B databases treat healthcare providers like any other industry. That doesn't work.</p>
                </div>
                <div class="problems__grid">
                    <div class="problem-card">
                        <div class="problem-card__icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 9v2m0 4h.01M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z"/></svg></div>
                        <h3 class="problem-card__title">Provider Databases Are a Mess</h3>
                        <p class="problem-card__text">Generic databases lump healthcare providers in with every other industry. No NPI verification, no taxonomy codes, no understanding of how practices actually work.</p>
                    </div>
                    <div class="problem-card">
                        <div class="problem-card__icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z"/></svg></div>
                        <h3 class="problem-card__title">You're Paying Too Much for Bad Data</h3>
                        <p class="problem-card__text">Enterprise data platforms charge $30K+ per year and still deliver stale provider contacts. Bounce rates over 15% are common because the data was never verified against healthcare registries.</p>
                    </div>
                    <div class="problem-card">
                        <div class="problem-card__icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9.172 16.172a4 4 0 0 1 5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z"/></svg></div>
                        <h3 class="problem-card__title">Generic Vendors Don't Get Healthcare</h3>
                        <p class="problem-card__text">You can't filter by NPI taxonomy code in ZoomInfo. You can't segment by practice type in Apollo. Healthcare requires healthcare-specific data infrastructure.</p>
                    </div>
                </div>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <div class="section__header">
                    <h2 class="section__title">What We Deliver</h2>
                    <p class="section__subtitle">Three core data products that cover the full provider intelligence stack.</p>
                </div>
                <div class="services__grid">
                    <a href="/services/provider-contact-data/" class="service-card">
                        <div class="service-card__icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M3 8l7.89 5.26a2 2 0 0 0 2.22 0L21 8M5 19h14a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2z"/></svg></div>
                        <h3 class="service-card__title">Provider Contact Data</h3>
                        <p class="service-card__text">Direct emails, phone numbers, and mailing addresses for healthcare providers. NPI-verified and updated weekly.</p>
                    </a>
                    <a href="/services/practice-location-data/" class="service-card">
                        <div class="service-card__icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 0 1-2.827 0l-4.244-4.243a8 8 0 1 1 11.314 0z"/><path d="M15 11a3 3 0 1 1-6 0 3 3 0 0 1 6 0z"/></svg></div>
                        <h3 class="service-card__title">Practice Intelligence</h3>
                        <p class="service-card__text">Practice locations, NPI taxonomy codes, provider counts, technology stack, and firmographic details.</p>
                    </a>
                    <a href="/services/custom-list-building/" class="service-card">
                        <div class="service-card__icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2M9 5a2 2 0 0 0 2 2h2a2 2 0 0 0 2-2M9 5a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2"/></svg></div>
                        <h3 class="service-card__title">Custom List Building</h3>
                        <p class="service-card__text">Tell us your target market. We build a custom provider list matched to your specialty, geography, and criteria.</p>
                    </a>
                </div>
            </div>
        </section>

        <section class="section section--alt">
            <div class="container">
                <div class="section__header">
                    <h2 class="section__title">Why Teams Switch to Provyx</h2>
                </div>
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>Generic Data Vendors</th>
                            <th>Provyx</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Healthcare is one of 50+ industries</td><td>Healthcare is our only focus</td></tr>
                        <tr><td>No NPI verification</td><td>Every record verified against NPI registry</td></tr>
                        <tr><td>Can't filter by taxonomy code</td><td>Full taxonomy code segmentation</td></tr>
                        <tr><td>Quarterly or monthly refreshes</td><td>Weekly data refresh cycle</td></tr>
                        <tr><td>$25K+ annual enterprise contracts</td><td>Flexible pricing from $500/month</td></tr>
                    </tbody>
                </table>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <div class="section__header">
                    <h2 class="section__title">Browse by Specialty</h2>
                    <p class="section__subtitle">Provider data across every major healthcare category.</p>
                </div>
                <div class="provider-grid">
                    {cat_cards}
                </div>
                <p class="text-center mt-xl"><a href="/providers/" class="btn btn--secondary">View All Specialties</a></p>
            </div>
        </section>

{generate_faq_html(faqs)}
{generate_cta_section(include_form=True, formspree_id=FORMSPREE_ID)}'''

    html = get_page_wrapper(
        title="Healthcare Provider Data & Contact Intelligence",
        description="Verified healthcare provider contact data across 40+ specialties. NPI-verified emails, phones, practice details. Updated weekly. Custom lists available.",
        canonical_path="/",
        body_content=body,
        extra_schema=extra_schema,
    )
    write_page("index.html", html)
    ALL_PAGES.append(("/", 1.0, "daily"))


def build_about():
    """Generate about/index.html"""
    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "About", "url": f"{BASE_URL}/about/"},
    ]
    extra_schema = get_breadcrumb_schema(breadcrumbs)

    body = f'''
        <section class="page-hero section">
            <div class="container">
                {get_breadcrumb_html(breadcrumbs)}
                <h1 class="page-hero__title">About Provyx</h1>
                <p class="page-hero__subtitle">We build healthcare provider databases that B2B teams can actually rely on.</p>
            </div>
        </section>

        <section class="section content">
            <div class="container" style="max-width:800px">
                <h2>Healthcare Data Shouldn't Be This Hard</h2>
                <p>If you've tried to buy healthcare provider contact data, you already know the problem. The big platforms charge enterprise prices for databases that are 30% stale. Generic B2B tools don't understand the difference between an NPI taxonomy code and a SIC code. And the cheap data brokers sell lists that bounce at 20%+.</p>
                <p>We built Provyx because healthcare provider data requires healthcare-specific infrastructure. NPI verification. Taxonomy code segmentation. Practice-level intelligence that goes beyond name and email. Weekly refresh cycles because provider information changes constantly.</p>

                <h2>Our Approach</h2>
                <p>We source data from public registries (CMS NPI Registry, state licensing boards), commercial databases, and proprietary web intelligence. Every record is verified against multiple sources before it enters our database. We don't scrape and dump. We build verified provider profiles with the data points that matter for B2B outreach.</p>
                <ul>
                    <li>NPI-verified provider records across 40+ specialties</li>
                    <li>Direct emails, phone numbers, and mailing addresses</li>
                    <li>Practice-level data: size, location, technology, ownership</li>
                    <li>Weekly refresh to catch moves, closures, and staff changes</li>
                    <li>Custom list building for targeted campaigns</li>
                </ul>

                <h2>Who We Work With</h2>
                <p>Our data is used by healthcare marketing agencies, medical device sales teams, health tech SaaS companies, pharmaceutical sales organizations, staffing agencies, and consulting firms. Anyone who needs to reach healthcare providers with accurate, current contact data.</p>

                <h2>Founded by a Data Operator</h2>
                <p>Provyx was founded by Rome, who spent years building data infrastructure at companies including Datajoy (acquired by Databricks), Microsoft, Salesforce, and Snapdocs. He holds an MBA from UC Berkeley Haas School of Business. The company is built on the principle that healthcare data buyers deserve better than what generic platforms deliver.</p>
            </div>
        </section>

{generate_cta_section()}'''

    html = get_page_wrapper(
        title="About Provyx",
        description="Provyx builds healthcare provider databases for B2B teams. NPI-verified contacts across 40+ specialties, updated weekly.",
        canonical_path="/about/",
        body_content=body,
        active_page="/about/",
        extra_schema=extra_schema,
    )
    write_page("about/index.html", html)
    ALL_PAGES.append(("/about/", 0.8, "monthly"))


def build_contact():
    """Generate contact/index.html"""
    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "Contact", "url": f"{BASE_URL}/contact/"},
    ]
    extra_schema = get_breadcrumb_schema(breadcrumbs)

    body = f'''
        <section class="page-hero section">
            <div class="container">
                {get_breadcrumb_html(breadcrumbs)}
                <h1 class="page-hero__title">Get in Touch</h1>
                <p class="page-hero__subtitle">Tell us what provider data you need. We'll put together a custom quote.</p>
            </div>
        </section>

        <section class="section content">
            <div class="container">
                <div class="contact-grid">
                    <div class="contact-info">
                        <h3>What to expect</h3>
                        <p>Fill out the form with details about the provider data you need. Include the specialties, geography, and volume you're targeting. We'll respond within one business day with a custom quote and sample data overview.</p>
                        <h3>Custom list requests</h3>
                        <p>Need a specific provider list? Tell us your target criteria: specialty, state/region, practice size, technology stack, or any other filters. We'll build a matched list and send you a sample before you commit.</p>
                        <h3>Questions?</h3>
                        <p>Email us directly at <a href="mailto:hello@getprovyx.com">hello@getprovyx.com</a></p>
                    </div>
                    <div class="contact-form">
                        <form class="form" action="https://formspree.io/f/{FORMSPREE_ID}" method="POST">
                            <input type="text" name="_gotcha" style="display:none" tabindex="-1" autocomplete="off">
                            <div class="form__group">
                                <label class="form__label" for="name">Name</label>
                                <input class="form__input" type="text" id="name" name="name" required>
                            </div>
                            <div class="form__group">
                                <label class="form__label" for="email">Work Email</label>
                                <input class="form__input" type="email" id="email" name="email" required>
                            </div>
                            <div class="form__group">
                                <label class="form__label" for="company">Company</label>
                                <input class="form__input" type="text" id="company" name="company">
                            </div>
                            <div class="form__group">
                                <label class="form__label" for="message">What provider data do you need?</label>
                                <textarea class="form__textarea" id="message" name="message" rows="5" placeholder="e.g., I need chiropractor emails in Colorado and Minnesota..."></textarea>
                            </div>
                            <button type="submit" class="btn btn--primary btn--lg form__submit">Send Request</button>
                        </form>
                    </div>
                </div>
            </div>
        </section>'''

    html = get_page_wrapper(
        title="Contact Us",
        description="Request healthcare provider data from Provyx. Tell us what you need and get a custom quote within one business day.",
        canonical_path="/contact/",
        body_content=body,
        extra_schema=extra_schema,
    )
    write_page("contact/index.html", html)
    ALL_PAGES.append(("/contact/", 0.8, "monthly"))


def build_pricing():
    """Generate pricing/index.html"""
    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "Pricing", "url": f"{BASE_URL}/pricing/"},
    ]

    faqs = [
        {"question": "What's included in the per-record price?",
         "answer": "Each record includes the provider's name, NPI number, specialty/taxonomy code, practice name, address, and available contact information (email, phone). Additional data points like technology stack or firmographics may be included depending on your plan."},
        {"question": "Can I get a sample before purchasing?",
         "answer": "Yes. We provide a free sample of 25-50 records matched to your target criteria so you can validate data quality before committing to a purchase."},
        {"question": "Do you offer ongoing data subscriptions?",
         "answer": "Yes. Growth and Enterprise plans include monthly data refreshes. We can also set up custom delivery schedules for teams that need weekly updates."},
        {"question": "What if I need a specialty or geography you don't cover?",
         "answer": "Contact us. We can build custom datasets for specialties or regions outside our standard coverage. Turnaround is typically 5-10 business days for custom requests."},
    ]

    extra_schema = get_breadcrumb_schema(breadcrumbs)

    body = f'''
        <section class="page-hero section">
            <div class="container">
                {get_breadcrumb_html(breadcrumbs)}
                <h1 class="page-hero__title">Simple, Transparent Pricing</h1>
                <p class="page-hero__subtitle">Pay for the data you need. No annual contracts required.</p>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <div class="pricing-grid">
                    <div class="pricing-card">
                        <h3 class="pricing-card__name">Starter</h3>
                        <div class="pricing-card__price">$500</div>
                        <div class="pricing-card__period">one-time purchase</div>
                        <ul class="pricing-card__features">
                            <li>Up to 1,000 provider records</li>
                            <li>Name, NPI, specialty, address</li>
                            <li>Available email and phone</li>
                            <li>CSV or Excel delivery</li>
                            <li>One-time purchase</li>
                        </ul>
                        <a href="/contact/" class="btn btn--primary" style="width:100%">Get Started</a>
                    </div>
                    <div class="pricing-card pricing-card--featured">
                        <h3 class="pricing-card__name">Growth</h3>
                        <div class="pricing-card__price">$2,500</div>
                        <div class="pricing-card__period">per month</div>
                        <ul class="pricing-card__features">
                            <li>Up to 10,000 records/month</li>
                            <li>All Starter data points</li>
                            <li>Practice firmographics</li>
                            <li>Technology detection</li>
                            <li>Monthly data refresh</li>
                            <li>Dedicated support</li>
                        </ul>
                        <a href="/contact/" class="btn btn--primary" style="width:100%">Contact Us</a>
                    </div>
                    <div class="pricing-card">
                        <h3 class="pricing-card__name">Enterprise</h3>
                        <div class="pricing-card__price">Custom</div>
                        <div class="pricing-card__period">annual agreement</div>
                        <ul class="pricing-card__features">
                            <li>Unlimited records</li>
                            <li>All Growth data points</li>
                            <li>API access</li>
                            <li>Custom enrichment fields</li>
                            <li>Weekly data refresh</li>
                            <li>SLA and priority support</li>
                        </ul>
                        <a href="/contact/" class="btn btn--secondary" style="width:100%">Talk to Sales</a>
                    </div>
                </div>
            </div>
        </section>

{generate_faq_html(faqs, heading="Pricing FAQ")}
{generate_cta_section()}'''

    html = get_page_wrapper(
        title="Pricing",
        description="Provyx healthcare provider data pricing. Plans from $500 for starter lists to custom enterprise agreements. No annual contracts required.",
        canonical_path="/pricing/",
        body_content=body,
        active_page="/pricing/",
        extra_schema=extra_schema,
    )
    write_page("pricing/index.html", html)
    ALL_PAGES.append(("/pricing/", 0.8, "monthly"))


def build_privacy():
    """Generate privacy/index.html"""
    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "Privacy Policy", "url": f"{BASE_URL}/privacy/"},
    ]
    extra_schema = get_breadcrumb_schema(breadcrumbs)

    body = f'''
        <section class="page-hero section">
            <div class="container">
                {get_breadcrumb_html(breadcrumbs)}
                <h1 class="page-hero__title">Privacy Policy</h1>
                <p class="page-hero__subtitle">Last updated: January 2026</p>
            </div>
        </section>
        <section class="section content">
            <div class="container" style="max-width:800px">
                <h2>Information We Collect</h2>
                <p>When you visit getprovyx.com, we collect standard web analytics data including pages visited, time on site, and referring URLs through Google Analytics 4. When you submit a form, we collect the information you provide: name, email address, company name, and message content.</p>

                <h2>How We Use Your Information</h2>
                <p>We use your contact information to respond to inquiries, provide quotes, and deliver data products you've requested. We use analytics data to understand how visitors use our website and improve our content and services.</p>

                <h2>Data We Sell</h2>
                <p>Provyx sells business contact information for healthcare providers. This data is sourced from public registries (such as the CMS NPI Registry), state licensing boards, commercial databases, and publicly available business information. This is provider business contact data, not patient health information (PHI). We do not collect, store, or sell any protected health information.</p>

                <h2>Third-Party Services</h2>
                <p>We use the following third-party services:</p>
                <ul>
                    <li><strong>Google Analytics 4</strong> for website analytics</li>
                    <li><strong>Formspree</strong> for form processing</li>
                    <li><strong>GitHub Pages</strong> for website hosting</li>
                    <li><strong>Cloudflare</strong> for DNS and SSL</li>
                </ul>

                <h2>Cookies</h2>
                <p>We use cookies set by Google Analytics to understand website traffic patterns. You can disable cookies in your browser settings without affecting core website functionality.</p>

                <h2>Your Rights</h2>
                <p>You may request access to, correction of, or deletion of any personal information we hold about you. To make a request, email <a href="mailto:hello@getprovyx.com">hello@getprovyx.com</a>.</p>

                <h2>Contact</h2>
                <p>For privacy-related questions, contact us at <a href="mailto:hello@getprovyx.com">hello@getprovyx.com</a>.</p>
            </div>
        </section>'''

    html = get_page_wrapper(
        title="Privacy Policy",
        description="Provyx privacy policy. How we collect, use, and protect your information when you visit getprovyx.com.",
        canonical_path="/privacy/",
        body_content=body,
        extra_schema=extra_schema,
    )
    write_page("privacy/index.html", html)
    ALL_PAGES.append(("/privacy/", 0.5, "yearly"))


def build_terms():
    """Generate terms/index.html"""
    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "Terms of Service", "url": f"{BASE_URL}/terms/"},
    ]
    extra_schema = get_breadcrumb_schema(breadcrumbs)

    body = f'''
        <section class="page-hero section">
            <div class="container">
                {get_breadcrumb_html(breadcrumbs)}
                <h1 class="page-hero__title">Terms of Service</h1>
                <p class="page-hero__subtitle">Last updated: January 2026</p>
            </div>
        </section>
        <section class="section content">
            <div class="container" style="max-width:800px">
                <h2>Acceptance of Terms</h2>
                <p>By accessing and using getprovyx.com and purchasing data products from Provyx, you agree to be bound by these Terms of Service. If you do not agree, please do not use our services.</p>

                <h2>Services</h2>
                <p>Provyx provides healthcare provider business contact data and intelligence services. Our data products include provider contact information, practice details, and related business data sourced from public and commercial records.</p>

                <h2>Permitted Use</h2>
                <p>Data purchased from Provyx may be used for legitimate B2B marketing, sales outreach, market research, and business analytics purposes. You agree not to use our data for:</p>
                <ul>
                    <li>Spam or unsolicited bulk communications that violate CAN-SPAM or similar regulations</li>
                    <li>Any purpose that violates applicable federal, state, or local laws</li>
                    <li>Reselling or redistributing our data to third parties without written permission</li>
                    <li>Harassment, stalking, or any form of abuse directed at data subjects</li>
                </ul>

                <h2>Data Accuracy</h2>
                <p>We make reasonable efforts to ensure data accuracy through verification against public registries and multiple sources. However, provider information changes frequently. We do not guarantee 100% accuracy and recommend verifying critical contacts before high-stakes communications.</p>

                <h2>Payment and Refunds</h2>
                <p>Payment is due upon delivery of data products. For subscription plans, payment is due monthly in advance. We offer a satisfaction guarantee: if delivered data does not meet the specifications agreed upon in your order, we will re-deliver corrected data or issue a credit toward future purchases.</p>

                <h2>Intellectual Property</h2>
                <p>The Provyx website, brand, and proprietary data compilation methods are our intellectual property. Data delivered to you is licensed for your use under the Permitted Use terms above.</p>

                <h2>Limitation of Liability</h2>
                <p>Provyx provides data "as is" and shall not be liable for any indirect, incidental, or consequential damages arising from use of our data products. Our total liability shall not exceed the amount paid for the specific data product in question.</p>

                <h2>Changes to Terms</h2>
                <p>We may update these terms from time to time. Continued use of our services after changes constitutes acceptance of the updated terms.</p>

                <h2>Contact</h2>
                <p>For questions about these terms, contact <a href="mailto:hello@getprovyx.com">hello@getprovyx.com</a>.</p>
            </div>
        </section>'''

    html = get_page_wrapper(
        title="Terms of Service",
        description="Provyx terms of service. Permitted use, data accuracy, payment terms, and liability for healthcare provider data products.",
        canonical_path="/terms/",
        body_content=body,
        extra_schema=extra_schema,
    )
    write_page("terms/index.html", html)
    ALL_PAGES.append(("/terms/", 0.5, "yearly"))


def build_404():
    """Generate 404.html"""
    body = f'''
        <section class="page-hero section" style="min-height:60vh;display:flex;align-items:center">
            <div class="container text-center">
                <h1 class="page-hero__title">Page Not Found</h1>
                <p class="page-hero__subtitle">The page you're looking for doesn't exist or has been moved.</p>
                <div class="hero__buttons" style="margin-top:2rem">
                    <a href="/" class="btn btn--primary btn--lg">Back to Homepage</a>
                    <a href="/providers/" class="btn btn--secondary btn--lg">Browse Providers</a>
                </div>
            </div>
        </section>'''

    html = get_page_wrapper(
        title="Page Not Found",
        description="The page you requested could not be found.",
        canonical_path="/404.html",
        body_content=body,
    )
    write_page("404.html", html)


# =============================================================================
# PAGE GENERATORS - SERVICE PAGES
# =============================================================================

SERVICES = [
    {
        "slug": "provider-contact-data",
        "title": "Provider Contact Data",
        "description": "Verified healthcare provider emails, phone numbers, and mailing addresses. NPI-verified and updated weekly.",
        "intro": "Direct provider contacts are the foundation of healthcare B2B outreach. But generic databases serve up stale records scraped months ago. Our provider contact data is verified against the CMS NPI Registry and refreshed weekly, so you're reaching real providers at their current practice.",
        "features": [
            ("Direct Email Addresses", "Verified provider and practice email addresses, not generic info@ accounts."),
            ("Phone Numbers", "Direct lines and office numbers with extension data where available."),
            ("Mailing Addresses", "Current practice addresses verified against NPI registry records."),
            ("NPI & Taxonomy", "National Provider Identifier and taxonomy classification codes for every record."),
        ],
    },
    {
        "slug": "practice-location-data",
        "title": "Practice Location Data",
        "description": "Healthcare practice addresses, NPI details, taxonomy codes, and multi-location mapping for provider organizations.",
        "intro": "Knowing where providers practice matters as much as knowing how to reach them. Our practice location data maps providers to their current practice sites, with full address details, NPI enumeration data, and taxonomy codes. We also identify multi-location practices and flag the primary vs. secondary sites.",
        "features": [
            ("Geocoded Addresses", "Full street addresses with latitude and longitude for mapping and territory planning."),
            ("NPI Enumeration Data", "Type 1 (individual) and Type 2 (organizational) NPI records with enumeration dates."),
            ("Taxonomy Codes", "Healthcare Provider Taxonomy codes for specialty classification and filtering."),
            ("Multi-Location Mapping", "Identify providers practicing at multiple sites and flag primary locations."),
        ],
    },
    {
        "slug": "technology-detection",
        "title": "Technology Detection",
        "description": "Identify EHR systems, practice management software, and billing platforms used by healthcare practices.",
        "intro": "If you're selling health IT, knowing what technology a practice currently uses is the most valuable data point you can have. Our technology detection identifies EHR systems, practice management platforms, billing software, and patient engagement tools across thousands of healthcare practices.",
        "features": [
            ("EHR Detection", "Identify which electronic health record system each practice uses."),
            ("Practice Management", "Detect practice management and scheduling software platforms."),
            ("Billing Systems", "Identify revenue cycle management and billing platforms in use."),
            ("Patient Engagement", "Detect patient portal, telehealth, and communication tools."),
        ],
    },
    {
        "slug": "social-profiles",
        "title": "Social Profiles",
        "description": "Healthcare provider social media profiles on LinkedIn, Facebook, and Instagram for multi-channel outreach.",
        "intro": "Social selling works in healthcare, but only if you have the right profiles. We match healthcare providers to their professional social media accounts on LinkedIn, Facebook, and Instagram, giving you additional touchpoints for multi-channel outreach campaigns.",
        "features": [
            ("LinkedIn Profiles", "Matched LinkedIn profiles for physicians and practice administrators."),
            ("Facebook Pages", "Practice Facebook business pages with follower counts and activity data."),
            ("Instagram Accounts", "Practice Instagram accounts, especially valuable for aesthetic and dental practices."),
            ("Profile Verification", "Each social profile is matched and verified against NPI and practice records."),
        ],
    },
    {
        "slug": "practice-firmographics",
        "title": "Practice Firmographics",
        "description": "Healthcare practice size, revenue estimates, years in business, and organizational data for targeted segmentation.",
        "intro": "Not all practices are created equal. A solo dermatologist has different buying power than a 20-provider orthopedic group. Our practice firmographic data helps you segment by practice size, estimated revenue, years in business, and organizational structure so you're targeting the right accounts.",
        "features": [
            ("Practice Size", "Provider headcount and staff size estimates for each practice location."),
            ("Revenue Estimates", "Modeled revenue ranges based on specialty, size, and location data."),
            ("Years in Business", "Practice age and establishment dates from business registration records."),
            ("Ownership Type", "Solo practice, group, hospital-owned, PE-backed, or DSO/MSO classification."),
        ],
    },
    {
        "slug": "custom-list-building",
        "title": "Custom List Building",
        "description": "Custom healthcare provider lists built to your exact specifications. Filter by specialty, geography, size, and more.",
        "intro": "Sometimes you don't need a platform. You need a list. Tell us your target criteria and we'll build a custom provider list matched to your specifications. Specialty, geography, practice size, technology stack, ownership type, any filter you need. We deliver clean, verified data in CSV or Excel format.",
        "features": [
            ("Any Specialty", "Filter by one or more of 40+ healthcare specialties and subspecialties."),
            ("Geographic Targeting", "State, metro area, ZIP code, or custom radius targeting."),
            ("Practice Filters", "Segment by practice size, ownership type, years in business, and more."),
            ("Fast Turnaround", "Most custom lists delivered within 3-5 business days."),
        ],
    },
]


def build_services_index():
    """Generate services/index.html"""
    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "Services", "url": f"{BASE_URL}/services/"},
    ]
    extra_schema = get_breadcrumb_schema(breadcrumbs)

    cards = ""
    for svc in SERVICES:
        cards += f'''
                <a href="/services/{svc["slug"]}/" class="service-card">
                    <h3 class="service-card__title">{svc["title"]}</h3>
                    <p class="service-card__text">{svc["description"]}</p>
                </a>'''

    body = f'''
        <section class="page-hero section">
            <div class="container">
                {get_breadcrumb_html(breadcrumbs)}
                <h1 class="page-hero__title">Data Products & Services</h1>
                <p class="page-hero__subtitle">Everything you need to find, reach, and understand healthcare providers.</p>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <div class="services__grid">
                    {cards}
                </div>
            </div>
        </section>

{generate_cta_section()}'''

    html = get_page_wrapper(
        title="Data Products & Services",
        description="Provyx healthcare data products: provider contacts, practice locations, technology detection, social profiles, firmographics, and custom list building.",
        canonical_path="/services/",
        body_content=body,
        active_page="/services/",
        extra_schema=extra_schema,
    )
    write_page("services/index.html", html)
    ALL_PAGES.append(("/services/", 0.9, "monthly"))


def build_service_page(svc):
    """Generate individual service page."""
    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "Services", "url": f"{BASE_URL}/services/"},
        {"name": svc["title"], "url": f"{BASE_URL}/services/{svc['slug']}/"},
    ]
    extra_schema = get_breadcrumb_schema(breadcrumbs)

    features_html = ""
    for feat_title, feat_text in svc["features"]:
        features_html += f'''
                <div class="feature-card">
                    <h3 class="feature-card__title">{feat_title}</h3>
                    <p class="feature-card__text">{feat_text}</p>
                </div>'''

    body = f'''
        <section class="page-hero section">
            <div class="container">
                {get_breadcrumb_html(breadcrumbs)}
                <h1 class="page-hero__title">{svc["title"]}</h1>
                <p class="page-hero__subtitle">{svc["description"]}</p>
            </div>
        </section>

        <section class="section content">
            <div class="container" style="max-width:800px">
                <p>{svc["intro"]}</p>
            </div>
        </section>

        <section class="section section--alt">
            <div class="container">
                <h2 class="text-center mb-xl">What's Included</h2>
                <div class="feature-grid">
                    {features_html}
                </div>
            </div>
        </section>

{generate_cta_section()}'''

    html = get_page_wrapper(
        title=svc["title"],
        description=svc["description"],
        canonical_path=f"/services/{svc['slug']}/",
        body_content=body,
        active_page="/services/",
        extra_schema=extra_schema,
    )
    write_page(f"services/{svc['slug']}/index.html", html)
    ALL_PAGES.append((f"/services/{svc['slug']}/", 0.8, "monthly"))


# =============================================================================
# PAGE GENERATORS - PROVIDER DIRECTORY, HUBS, SPOKES
# =============================================================================

def build_providers_index():
    """Generate providers/index.html - top-level directory."""
    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "Provider Data", "url": f"{BASE_URL}/providers/"},
    ]
    extra_schema = get_breadcrumb_schema(breadcrumbs)

    cards = ""
    for key, cat in CATEGORIES.items():
        count = len([s for s in SUBTYPES if s[2] == key])
        cards += f'''
                <a href="/providers/{key}/" class="provider-card">
                    <h3 class="provider-card__title">{cat["name"]}</h3>
                    <p class="provider-card__count">{count} provider types</p>
                    <p class="provider-card__text">{cat["description"][:100]}...</p>
                </a>'''

    body = f'''
        <section class="page-hero section">
            <div class="container">
                {get_breadcrumb_html(breadcrumbs)}
                <h1 class="page-hero__title">Healthcare Provider Data Directory</h1>
                <p class="page-hero__subtitle">Browse provider data across 17 healthcare categories and 130+ specialties.</p>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <div class="provider-grid">
                    {cards}
                </div>
            </div>
        </section>

{generate_cta_section()}'''

    html = get_page_wrapper(
        title="Healthcare Provider Data Directory",
        description="Browse Provyx healthcare provider data across 17 categories and 130+ specialties. Verified contacts, NPI data, and practice intelligence.",
        canonical_path="/providers/",
        body_content=body,
        active_page="/providers/",
        extra_schema=extra_schema,
    )
    write_page("providers/index.html", html)
    ALL_PAGES.append(("/providers/", 0.9, "weekly"))


def build_hub_page(cat_key, cat_data):
    """Generate a category hub page at /providers/{category}/"""
    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "Providers", "url": f"{BASE_URL}/providers/"},
        {"name": cat_data["name"], "url": f"{BASE_URL}/providers/{cat_key}/"},
    ]

    cat_subtypes = [s for s in SUBTYPES if s[2] == cat_key]

    faqs = [
        {"question": f"What {cat_data['short'].lower()} provider data does Provyx offer?",
         "answer": f"We provide verified contact data for {len(cat_subtypes)} types of {cat_data['short'].lower()} providers, including direct emails, phone numbers, NPI details, taxonomy codes, and practice information. All records are verified against the CMS NPI Registry."},
        {"question": f"How is {cat_data['short'].lower()} data different from generic provider databases?",
         "answer": f"Generic databases lump all healthcare providers together without understanding {cat_data['short'].lower()} specialty distinctions. We segment by specific provider subtypes, making it easy to target exactly the right {cat_data['short'].lower()} providers for your campaign."},
        {"question": f"How often is the {cat_data['short'].lower()} provider data updated?",
         "answer": f"Our {cat_data['short'].lower()} provider database is refreshed weekly. Provider contacts change frequently as staff turns over and practices relocate. Weekly updates keep your outreach data current."},
        {"question": f"Can I get a custom {cat_data['short'].lower()} provider list?",
         "answer": f"Yes. We build custom lists filtered by specific {cat_data['short'].lower()} subtypes, geography, practice size, and other criteria. Contact us with your requirements and we'll put together a matched list."},
        {"question": f"What data fields are included for {cat_data['short'].lower()} providers?",
         "answer": "Every record includes provider name, NPI number, taxonomy code, practice name, address, and available contact information (email, phone). Additional fields like practice size, technology stack, and ownership type are available on Growth and Enterprise plans."},
    ]

    spoke_cards = ""
    for slug, name, _, synonyms, desc in cat_subtypes:
        syn_text = f' <span class="text-muted">Also: {", ".join(synonyms)}</span>' if synonyms else ""
        spoke_cards += f'''
                <a href="/providers/{slug}/" class="provider-card">
                    <h3 class="provider-card__title">{name}</h3>
                    <p class="provider-card__text">{desc[:100]}...{syn_text}</p>
                </a>'''

    extra_schema = get_breadcrumb_schema(breadcrumbs)

    body = f'''
        <section class="page-hero section">
            <div class="container">
                {get_breadcrumb_html(breadcrumbs)}
                <h1 class="page-hero__title">{cat_data["hero_title"]}</h1>
                <p class="page-hero__subtitle">{cat_data["description"]}</p>
            </div>
        </section>

        <section class="section content">
            <div class="container" style="max-width:800px">
                <p>{cat_data["intro"]}</p>
            </div>
        </section>

        <section class="section section--alt">
            <div class="container">
                <h2 class="text-center mb-xl">Browse {cat_data["name"]} Provider Types</h2>
                <div class="provider-grid">
                    {spoke_cards}
                </div>
            </div>
        </section>

{generate_faq_html(faqs)}
{generate_cta_section()}'''

    html = get_page_wrapper(
        title=cat_data["hero_title"],
        description=cat_data["description"],
        canonical_path=f"/providers/{cat_key}/",
        body_content=body,
        active_page="/providers/",
        extra_schema=extra_schema,
    )
    write_page(f"providers/{cat_key}/index.html", html)
    ALL_PAGES.append((f"/providers/{cat_key}/", 0.8, "weekly"))


def build_spoke_page(slug, name, cat_key, synonyms, description):
    """Generate a subtype spoke page at /providers/{slug}/"""
    cat = CATEGORIES[cat_key]

    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": "Providers", "url": f"{BASE_URL}/providers/"},
        {"name": cat["name"], "url": f"{BASE_URL}/providers/{cat_key}/"},
        {"name": name, "url": f"{BASE_URL}/providers/{slug}/"},
    ]

    # Get sibling spokes for related links
    siblings = [s for s in SUBTYPES if s[2] == cat_key and s[0] != slug][:3]

    name_lower = name.lower()

    faqs = [
        {"question": f"What {name_lower} data does Provyx provide?",
         "answer": f"We provide verified contact data for {name_lower} including direct emails, phone numbers, NPI details, taxonomy codes, practice addresses, and available firmographic data. Every record is verified against the CMS NPI Registry and refreshed weekly."},
        {"question": f"How accurate is the {name_lower} contact data?",
         "answer": f"Our {name_lower} data is verified against multiple sources including the CMS NPI Registry, state licensing boards, and commercial databases. We refresh records weekly to catch moves, closures, and contact changes."},
        {"question": f"Can I filter {name_lower} data by geography?",
         "answer": f"Yes. You can filter {name_lower} records by state, metro area, ZIP code, or custom radius. We can build targeted lists for specific regions or provide nationwide coverage."},
    ]

    synonym_text = ""
    if synonyms:
        synonym_text = f'<p class="text-muted">Also known as: {", ".join(synonyms)}</p>'

    related_html = ""
    if siblings:
        links = "".join([f'<a href="/providers/{s[0]}/">{s[1]}</a> ' for s in siblings])
        related_html = f'''
        <section class="section">
            <div class="container">
                <div class="related-links">
                    <p class="related-links__title">Related Provider Types</p>
                    <div class="related-links__list">{links} <a href="/providers/{cat_key}/">All {cat["short"]} Providers</a></div>
                </div>
            </div>
        </section>'''

    extra_schema = get_breadcrumb_schema(breadcrumbs)

    body = f'''
        <section class="page-hero section">
            <div class="container">
                {get_breadcrumb_html(breadcrumbs)}
                <h1 class="page-hero__title">{name} Data & Contact Lists</h1>
                <p class="page-hero__subtitle">{description}</p>
                {synonym_text}
            </div>
        </section>

        <section class="section content">
            <div class="container" style="max-width:800px">
                <h2>Why Bad {name} Data Costs You Money</h2>
                <p>Every bounced email to a {name_lower.rstrip('s')} is wasted time and wasted budget. Every wrong phone number is a missed opportunity. If you're running outreach campaigns targeting {name_lower}, you need data that's verified and current, not scraped from a directory six months ago.</p>
                <p>{description}</p>

                <h2>Data Available for {name}</h2>
                <ul class="data-points">
                    <li>Provider name and credentials</li>
                    <li>NPI number and taxonomy code</li>
                    <li>Practice name and address</li>
                    <li>Direct email address</li>
                    <li>Phone number (direct line where available)</li>
                    <li>Practice size and type</li>
                    <li>State license information</li>
                </ul>

                <h2>Who Buys {name} Data</h2>
                <p>Teams that purchase {name_lower} contact data from Provyx include healthcare marketing agencies building outreach campaigns, medical device and supply companies targeting this specialty, SaaS vendors selling practice management or EHR solutions, pharmaceutical sales teams, and staffing agencies recruiting {name_lower}.</p>

                <h2>How It Works</h2>
                <ol>
                    <li><strong>Tell us what you need.</strong> Specify the {name_lower} subtypes, geography, and any other filters for your target list.</li>
                    <li><strong>We build your list.</strong> We pull matching records from our verified database and deliver a clean CSV or Excel file.</li>
                    <li><strong>Start your outreach.</strong> Use the data for email campaigns, direct mail, phone outreach, or CRM enrichment.</li>
                </ol>
            </div>
        </section>

{generate_faq_html(faqs)}
{related_html}
{generate_cta_section()}'''

    html = get_page_wrapper(
        title=f"{name} Data & Contact Lists",
        description=description,
        canonical_path=f"/providers/{slug}/",
        body_content=body,
        active_page="/providers/",
        extra_schema=extra_schema,
    )
    write_page(f"providers/{slug}/index.html", html)
    ALL_PAGES.append((f"/providers/{slug}/", 0.7, "weekly"))


# =============================================================================
# PAGE GENERATORS - ICP PAGES
# =============================================================================

def build_icp_page(icp):
    """Generate /for/{slug}/ audience page."""
    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": icp["name"], "url": f"{BASE_URL}/for/{icp['slug']}/"},
    ]
    extra_schema = get_breadcrumb_schema(breadcrumbs)

    use_cases_html = ""
    for uc in icp["use_cases"]:
        use_cases_html += f"<li>{uc}</li>\n"

    body = f'''
        <section class="page-hero section">
            <div class="container">
                {get_breadcrumb_html(breadcrumbs)}
                <h1 class="page-hero__title">{icp["title"]}</h1>
                <p class="page-hero__subtitle">{icp["description"]}</p>
            </div>
        </section>

        <section class="section content">
            <div class="container" style="max-width:800px">
                <p>{icp["intro"]}</p>

                <h2>How {icp["name"]} Use Provyx Data</h2>
                <ul class="benefits-list">
                    {use_cases_html}
                </ul>

                <h2>Data You Get</h2>
                <p>Every provider record includes name, NPI, specialty, practice address, and available contact information. Depending on your plan, you also get practice firmographics, technology detection, social profiles, and custom enrichment fields.</p>
                <p><a href="/pricing/">See pricing plans</a> or <a href="/contact/">request a custom list</a> for your specific needs.</p>
            </div>
        </section>

{generate_cta_section()}'''

    html = get_page_wrapper(
        title=icp["title"],
        description=icp["description"],
        canonical_path=f"/for/{icp['slug']}/",
        body_content=body,
        extra_schema=extra_schema,
    )
    write_page(f"for/{icp['slug']}/index.html", html)
    ALL_PAGES.append((f"/for/{icp['slug']}/", 0.7, "monthly"))


# =============================================================================
# PAGE GENERATORS - COMPARISON & ALTERNATIVE PAGES
# =============================================================================

def build_comparison_page(comp):
    """Generate /compare/{slug}/ page."""
    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": f"Provyx vs {comp['competitor']}", "url": f"{BASE_URL}/compare/{comp['slug']}/"},
    ]
    extra_schema = get_breadcrumb_schema(breadcrumbs)

    cons_html = "".join([f"<tr><td>{c}</td><td>{p}</td></tr>" for c, p in zip(comp["competitor_cons"], comp["provyx_pros"])])

    body = f'''
        <section class="page-hero section">
            <div class="container">
                {get_breadcrumb_html(breadcrumbs)}
                <h1 class="page-hero__title">{comp["title"]}</h1>
                <p class="page-hero__subtitle">{comp["description"]}</p>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <table class="comparison-table">
                    <thead>
                        <tr>
                            <th>{comp["competitor"]}</th>
                            <th>Provyx</th>
                        </tr>
                    </thead>
                    <tbody>
                        {cons_html}
                    </tbody>
                </table>
            </div>
        </section>

        <section class="section content section--alt">
            <div class="container" style="max-width:800px">
                <h2>Why Healthcare Teams Choose Provyx Over {comp["competitor"]}</h2>
                <p>{comp["competitor"]} is a well-known platform, but it wasn't built for healthcare provider data. If you're targeting specific medical specialties, need NPI-verified contacts, or want to segment by taxonomy code, you need a database built for healthcare from the ground up.</p>
                <p>Provyx focuses exclusively on healthcare provider data. Every record is verified against the CMS NPI Registry. You can filter by medical specialty, practice type, geography, and technology stack. And you don't need a $30K enterprise contract to get started.</p>
            </div>
        </section>

{generate_cta_section(title=f"Switch from {comp['competitor']} to Better Healthcare Data")}'''

    html = get_page_wrapper(
        title=comp["title"],
        description=comp["description"],
        canonical_path=f"/compare/{comp['slug']}/",
        body_content=body,
        extra_schema=extra_schema,
    )
    write_page(f"compare/{comp['slug']}/index.html", html)
    ALL_PAGES.append((f"/compare/{comp['slug']}/", 0.7, "monthly"))


def build_alternative_page(alt):
    """Generate /alternatives/{slug}/ page."""
    breadcrumbs = [
        {"name": "Home", "url": BASE_URL},
        {"name": f"{alt['competitor']} Alternative", "url": f"{BASE_URL}/alternatives/{alt['slug']}/"},
    ]
    extra_schema = get_breadcrumb_schema(breadcrumbs)

    body = f'''
        <section class="page-hero section">
            <div class="container">
                {get_breadcrumb_html(breadcrumbs)}
                <h1 class="page-hero__title">{alt["title"]}</h1>
                <p class="page-hero__subtitle">{alt["description"]}</p>
            </div>
        </section>

        <section class="section content">
            <div class="container" style="max-width:800px">
                <h2>Why Look for a {alt["competitor"]} Alternative?</h2>
                <p>Teams searching for a {alt["competitor"]} alternative for healthcare data usually have one of three problems: the pricing doesn't fit their budget, the healthcare provider coverage isn't deep enough, or the platform complexity exceeds what they actually need.</p>

                <h2>Provyx: Built for Healthcare Provider Data</h2>
                <p>Provyx is a healthcare-first provider data platform. We don't try to cover every industry. We focus on healthcare providers across 40+ specialties with NPI-verified contacts, taxonomy code segmentation, and practice-level intelligence.</p>

                <h2>What Makes Provyx Different</h2>
                <ul class="benefits-list">
                    <li>NPI-verified provider records across 40+ specialties</li>
                    <li>Weekly data refresh cycle for current contacts</li>
                    <li>Flexible pricing from $500 one-time to enterprise plans</li>
                    <li>Practice-level data: size, technology, ownership</li>
                    <li>Custom list building for targeted campaigns</li>
                </ul>

                <p><a href="/pricing/">See our pricing</a> or <a href="/contact/">request a sample list</a> to compare data quality.</p>
            </div>
        </section>

{generate_cta_section(title=f"Try Provyx as Your {alt['competitor']} Alternative")}'''

    html = get_page_wrapper(
        title=alt["title"],
        description=alt["description"],
        canonical_path=f"/alternatives/{alt['slug']}/",
        body_content=body,
        extra_schema=extra_schema,
    )
    write_page(f"alternatives/{alt['slug']}/index.html", html)
    ALL_PAGES.append((f"/alternatives/{alt['slug']}/", 0.7, "monthly"))


# =============================================================================
# SITEMAP GENERATOR
# =============================================================================

def build_sitemap():
    """Generate sitemap.xml from ALL_PAGES."""
    urls = ""
    for path, priority, changefreq in ALL_PAGES:
        url = f"{BASE_URL}{path}" if not path.endswith(".html") else f"{BASE_URL}/{path}"
        urls += f"""  <url>
    <loc>{url}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>
"""

    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}</urlset>"""

    sitemap_path = os.path.join(PROJECT_ROOT, "sitemap.xml")
    with open(sitemap_path, "w") as f:
        f.write(sitemap)
    print(f"  Generated: /sitemap.xml ({len(ALL_PAGES)} URLs)")


# =============================================================================
# MAIN
# =============================================================================

def main():
    print(f"\n{'='*60}")
    print(f"  Provyx Website Build")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # Core pages
    print("Core pages:")
    build_homepage()
    build_about()
    build_contact()
    build_pricing()
    build_privacy()
    build_terms()
    build_404()

    # Service pages
    print("\nService pages:")
    build_services_index()
    for svc in SERVICES:
        build_service_page(svc)

    # Provider directory
    print("\nProvider directory:")
    build_providers_index()

    # Hub pages
    print("\nCategory hub pages:")
    for cat_key, cat_data in CATEGORIES.items():
        build_hub_page(cat_key, cat_data)

    # Spoke pages
    print("\nSubtype spoke pages:")
    for slug, name, cat_key, synonyms, desc in SUBTYPES:
        build_spoke_page(slug, name, cat_key, synonyms, desc)

    # ICP pages
    print("\nICP audience pages:")
    for icp in ICP_PAGES:
        build_icp_page(icp)

    # Comparison pages
    print("\nComparison pages:")
    for comp in COMPARISONS:
        build_comparison_page(comp)

    # Alternative pages
    print("\nAlternative pages:")
    for alt in ALTERNATIVES:
        build_alternative_page(alt)

    # Sitemap
    print("\nSitemap:")
    build_sitemap()

    print(f"\n{'='*60}")
    print(f"  Build complete: {len(ALL_PAGES)} pages generated")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
