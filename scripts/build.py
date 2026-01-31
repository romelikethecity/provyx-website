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
FORMSPREE_ID = "mrekgwqk"
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
        "intro": "The mental health sector is growing fast, with provider shortages driving demand for accurate contact data. Whether you're selling EHR software to psychiatrists or recruiting therapists for a telehealth platform, you need data that goes beyond a name and address. Our mental health provider database includes practice details, owner contacts, NPI verification, taxonomy codes, and LinkedIn profiles for thousands of verified providers.",
    },
    "chiropractic": {
        "name": "Chiropractic",
        "short": "Chiropractic",
        "description": "Verified chiropractor practice data with NPI, owner contacts, and practice details for targeted outreach.",
        "hero_title": "Chiropractor Data & Contact Lists",
        "intro": "Chiropractors operate independently more often than most provider types, which makes them both easier to reach and harder to find accurate data for. Solo practices change addresses, phone numbers, and email systems frequently. Our chiropractic provider database tracks these changes continuously, giving you verified contact data you can actually use for outreach.",
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
        "intro": "The med spa industry has exploded, with new clinics opening constantly across the country. These businesses blend medical oversight with consumer aesthetics, creating a unique sales environment. Decision-makers are often the medical director or business owner, not a traditional office manager. Our med spa database identifies these contacts directly.",
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
        "intro": "Rheumatologists treat complex autoimmune and inflammatory conditions, making them high-priority targets for pharmaceutical companies and clinical research organizations. With a limited number of practicing rheumatologists in the US, accurate contact data is especially valuable. Our database covers rheumatology practices with verified owner contacts, NPI details, and practice intelligence.",
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
     "Verified psychiatrist practice data including owner contacts, NPI details, taxonomy codes, and practice information for targeted outreach campaigns."),
    ("psychiatric-nurse-practitioners", "Psychiatric Nurse Practitioners", "mental-health", ["MHNP", "psychiatric NP"],
     "Contact data for psychiatric nurse practitioners providing medication management and mental health treatment services."),
    ("psychotherapists", "Psychotherapists", "mental-health", [],
     "Psychotherapist practice data with owner contacts, specialty focus areas, and verified NPI information."),
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
     "Chiropractor practice data with verified owner contacts, NPI records, and practice details."),
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
     "General dentist practice data with verified owner contacts, NPI records, and practice details for the largest dental segment."),
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
     "Dermatologist practice data with specialty focus, practice size, and verified owner contact information."),
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
# ICP audience pages
ICP_PAGES = [
    # ===================================================================
    # 1. Healthcare Marketing Agencies
    # ===================================================================
    {
        "slug": "healthcare-marketing-agencies",
        "title": "Healthcare Provider Data for Marketing Agencies | Provyx",
        "h1": "Healthcare Provider Business Data for Marketing Agencies",
        "subtitle": "Build targeted prospect lists for your healthcare clients. Specialty-segmented, geography-filtered provider contact intelligence sourced from public NPI registries, business listings, and commercial databases.",
        "meta_description": "Get healthcare provider business data built for marketing agencies. Specialty-segmented, geography-filtered lists for dental, med spa, chiropractic, and mental health campaigns.",

        # -- The Pain --
        "pain_heading": "The Data Problem Holding Your Campaigns Back",
        "pain_content": """<p>Your clients hire you because you know healthcare marketing. They expect targeted campaigns that reach the right providers in the right geography with the right message. But the moment you sit down to build a prospect list, the problems start.</p>

<p>Most generic business databases treat "healthcare" as a single category. You get a dump of names and addresses with no way to distinguish a solo chiropractor from a 40-provider orthopedic group. Your dental client doesn't need a list of every provider in Phoenix. They need endodontists and pediatric dentists within a 15-mile radius who own their own practice and have a website worth sending traffic to. That level of specificity is almost impossible to get from the databases most agencies rely on.</p>

<p>Then there's the accuracy problem. Your team pulls a list, loads it into your email platform or direct mail vendor, and 15-20% of records bounce or come back undeliverable. That's not just wasted spend. It damages your sender reputation, tanks your deliverability on future campaigns, and forces an uncomfortable conversation with your client about why the numbers look soft.</p>

<p>Agencies serving dental practices, med spas, chiropractic offices, and mental health providers feel this the hardest. These verticals have high turnover, frequent address changes, and lots of sole proprietors who don't show up in enterprise databases. You end up spending hours manually verifying contacts through the <a href="https://npiregistry.cms.hhs.gov/" target="_blank" rel="noopener">NPI Registry</a> and Google searches, which is time you should be spending on strategy and creative.</p>

<p>The alternative is expensive. Enterprise data providers want annual contracts starting at $20,000 or more, and they're built for pharma companies and hospital systems, not a 12-person agency running campaigns for dental groups. You don't need 10 million records. You need 2,000 accurate ones, segmented exactly the way your campaign requires.</p>""",

        # -- How They Use Provyx --
        "use_heading": "How Healthcare Marketing Agencies Use Provyx",
        "use_content": """<p>Agencies use Provyx to build campaign-ready lists that match the exact targeting criteria their clients need. Here's what that looks like in practice.</p>

<p><strong>Specialty-specific email campaigns.</strong> You're running an email sequence for a dental SaaS client targeting general dentists who own their practice. Provyx delivers a list filtered by taxonomy code, practice ownership, and geography, with verified business email addresses attached. You load it straight into your ESP without a manual scrub step.</p>

<p><strong>Direct mail for med spas and aesthetics.</strong> Med spa marketing is one of the fastest-growing niches in healthcare marketing. You need practice addresses, owner names, and some sense of practice size so you can tailor your mailer. Provyx lists include the practice address, the business phone, the owner or decision-maker name, and the NPI-linked specialty, so your segmentation is clean from the start.</p>

<p><strong>Lookalike audience seeding.</strong> You take a Provyx list of chiropractors in a target market, upload it as a custom audience to your ad platform, and build a lookalike. Because the seed list is tightly targeted by specialty and geography, the lookalike performs significantly better than one built off a broad healthcare list.</p>

<p><strong>Market sizing for client pitches.</strong> Before you even sign a new client, you need to know how large their addressable market is. How many mental health providers are there in the Atlanta metro? How many have a web presence? Provyx data helps you answer that in hours, not days. The <a href="https://www.bls.gov/ooh/healthcare/" target="_blank" rel="noopener">Bureau of Labor Statistics</a> publishes macro-level workforce numbers, but Provyx gives you the practice-level detail you actually need for campaign planning.</p>

<p><strong>Re-engagement and win-back campaigns.</strong> When a client's existing patient outreach list goes stale, you can cross-reference it against Provyx data to identify which practices have moved, closed, or changed ownership. This keeps your client's CRM clean and your campaigns hitting active targets.</p>

<p><strong>Multi-location targeting for franchise clients.</strong> If your client operates across multiple markets, you can pull segmented lists for each location's service area separately, with consistent data fields across every market. No more stitching together data from three different sources with three different formats.</p>""",

        # -- What Data You Get --
        "data_heading": "What Data You Get in Every Record",
        "data_content": """<p>Every Provyx record is built from public NPI registries, business listings, and commercial databases. Here's what a standard record includes:</p>

<ul>
<li><strong>Practice name</strong> and <strong>doing-business-as (DBA)</strong> name where applicable</li>
<li><strong>Full practice address</strong>, geocoded and validated against USPS records</li>
<li><strong>Business phone number</strong>, verified as connected and associated with the practice</li>
<li><strong>Practice website URL</strong> where available</li>
<li><strong>Owner or decision-maker name</strong> linked to the NPI record</li>
<li><strong>NPI number</strong> and <strong>taxonomy codes</strong> for specialty classification</li>
<li><strong>LinkedIn profile URL</strong> for the provider or practice owner where available</li>
</ul>

<p>For agencies that need deeper targeting, we offer add-ons:</p>

<ul>
<li><strong>Direct email addresses</strong> (personal or role-based, depending on availability)</li>
<li><strong>Mobile phone numbers</strong> for decision-makers</li>
<li><strong>Practice firmographics</strong>: estimated revenue range, provider count, years in operation</li>
<li><strong>Technology detection</strong>: what EHR, practice management, or scheduling software the practice runs</li>
</ul>

<p>All fields are delivered in a flat CSV or Excel file, formatted to drop directly into your CRM, ESP, or ad platform.</p>""",

        # -- How It Works --
        "how_heading": "How It Works",
        "how_content": """<p><strong>Step 1: Tell us your target criteria.</strong> Share the specialty, geography, practice size, and any other filters your campaign requires. If you're not sure how to define your targeting, we'll help. Most agency clients send us a brief or a campaign spec, and we translate it into data filters.</p>

<p><strong>Step 2: We build your list.</strong> Our team pulls, matches, and verifies records against multiple sources, including the NPI registry, business directories, and commercial databases. We de-duplicate, validate contact information, and flag any records that don't meet our accuracy threshold.</p>

<p><strong>Step 3: Delivered in days, not weeks.</strong> Standard lists are delivered within 3-5 business days. Rush delivery is available for time-sensitive campaigns. You get a clean, formatted file ready for import, plus a summary of match rates and any records we excluded and why.</p>""",

        # -- FAQs --
        "faqs": [
            {
                "question": "Can I order lists for multiple specialties or geographies at once?",
                "answer": "Yes. Most agency clients order segmented lists covering several specialties or markets in a single request. We deliver them as separate tabs or files so you can load each segment independently into your campaign tools. There's no limit on the number of segments per order, and pricing scales with total record count, not the number of filters."
            },
            {
                "question": "How accurate are the email addresses?",
                "answer": "Business email addresses in our standard records are sourced from public listings and verified against mail server responses. We typically see deliverability rates above 90% on business emails. Direct personal emails, available as an add-on, go through an additional verification step. We don't guarantee 100% deliverability because email infrastructure changes constantly, but we replace or credit any batch that falls below our stated accuracy threshold."
            },
            {
                "question": "Do you offer ongoing or subscription-based list delivery?",
                "answer": "We do. Several agency clients receive refreshed lists on a monthly or quarterly basis, especially those running ongoing campaigns for retainer clients. Subscription pricing is lower per record than one-time orders because we're updating an existing dataset rather than building from scratch each time. Contact us to set up a recurring delivery schedule."
            },
            {
                "question": "Can I white-label Provyx data for my clients?",
                "answer": "The data you purchase is yours to use in campaigns and deliverables for your clients. We don't require Provyx attribution on your reports or exports. Some agencies include our data in market analysis decks or append it to client CRMs as part of their service offering. If you need a specific licensing arrangement for resale, reach out and we'll work through the details."
            },
        ],

        # -- Related Links --
        "related_links": [
            {"text": "Custom List Building", "url": "/services/custom-list-building/"},
            {"text": "Data Enrichment", "url": "/services/data-enrichment/"},
            {"text": "Browse Providers by Specialty", "url": "/providers/"},
            {"text": "Pricing", "url": "/pricing/"},
        ],

        # -- Outbound authority links (used in pain/use sections above) --
        "outbound_links": [
            "https://npiregistry.cms.hhs.gov/",
            "https://www.bls.gov/ooh/healthcare/",
        ],
    },

    # ===================================================================
    # 2. Medical Device Sales Teams
    # ===================================================================
    {
        "slug": "medical-device-sales",
        "title": "Healthcare Provider Data for Medical Device Sales | Provyx",
        "h1": "Healthcare Provider Contact Intelligence for Medical Device Sales Teams",
        "subtitle": "Find the surgeons, physicians, and practice decision-makers your reps actually need to reach. Territory-ready provider business data sourced from public NPI registries, business listings, and commercial databases.",
        "meta_description": "Provider contact intelligence for medical device sales reps. Territory-mapped, specialty-filtered data with decision-maker names, NPI numbers, and practice details.",

        "pain_heading": "Why Your Reps Are Wasting Half Their Week on Bad Data",
        "pain_content": """<p>Medical device sales is a territory game. Your reps live and die by the quality of their contact lists. And right now, too many of them are spending Monday mornings updating spreadsheets instead of booking meetings.</p>

<p>The core problem is data decay. A rep starts the quarter with a territory list pulled from your CRM. Within 60 days, 15-20% of that list is wrong. Physicians change practices. Offices move locations. A surgeon who was at a hospital system six months ago is now at a private ASC across town. Your rep shows up to a call that doesn't exist anymore, or worse, pitches a physician who left the specialty entirely. According to the <a href="https://npiregistry.cms.hhs.gov/" target="_blank" rel="noopener">CMS NPI Registry</a>, there are over 2.2 million active Type 1 (individual) NPIs in the United States, and the churn within that population is constant.</p>

<p>Then there's the targeting gap. Your rep sells a surgical implant used primarily by orthopedic surgeons who perform total joint replacements. But your CRM just says "orthopedic surgery." It doesn't distinguish between the sports medicine orthopod who never touches your product category and the joint replacement specialist who's your ideal buyer. Without subspecialty filtering and procedure-level intelligence, reps burn through their call lists hitting the wrong people.</p>

<p>Competitive intelligence is another blind spot. If a practice already uses your competitor's device, that's either a disqualification or a high-priority conversion target, depending on your strategy. But most sales databases don't tell you what technology or devices a practice currently uses. Your reps discover this during the first call, which means they've already spent the time getting there.</p>

<p>The <a href="https://www.bls.gov/ooh/healthcare/" target="_blank" rel="noopener">Bureau of Labor Statistics</a> projects continued growth in surgical and physician specialties through the end of the decade. The market is getting bigger, which means territory lists need to be refreshed more often, not less. Static annual data pulls don't cut it anymore.</p>""",

        "use_heading": "How Medical Device Sales Teams Use Provyx",
        "use_content": """<p>Device sales organizations use Provyx to build and maintain territory-level contact lists that stay accurate and filter down to the subspecialty level. Here's how.</p>

<p><strong>Territory list builds by subspecialty.</strong> Instead of pulling every orthopedic surgeon in a zip code range, you tell us the exact subspecialty, the procedure types your device supports, and the territory boundaries. We deliver a list of surgeons and physicians who match, with their current practice address, NPI, and direct contact information. Your reps start the quarter with a list they can actually work.</p>

<p><strong>Practice setting filters.</strong> Your device might be used in hospitals, ambulatory surgical centers, or private clinics, but not all three. Provyx lets you filter by practice setting so your reps aren't calling on facilities where your product isn't relevant. This alone can cut wasted outreach by 30-40% for reps covering mixed territories.</p>

<p><strong>Decision-maker identification.</strong> In a group practice or hospital department, the physician who uses your device isn't always the one who makes the purchasing decision. Provyx records include the practice owner or administrator name alongside the clinical provider, so your rep knows who to ask for when they call.</p>

<p><strong>Technology and device detection.</strong> Our technology detection add-on identifies what EHR, practice management software, and in some cases, what device brands a practice is associated with. This helps your team prioritize competitive displacement opportunities or avoid wasting time on practices already locked into long-term contracts with a competitor.</p>

<p><strong>CRM refresh and enrichment.</strong> You don't need to replace your entire CRM dataset. Send us your existing territory list and we'll match it against current records, flag entries that have gone stale, fill in missing fields, and append new contacts that match your criteria but weren't in your system. Most clients do this quarterly.</p>

<p><strong>New market entry planning.</strong> Launching a new product or expanding into a new territory? We can build a ground-up list of every provider in a defined geography who matches your target specialty and practice setting, giving your reps a head start before they make a single call.</p>""",

        "data_heading": "What Data You Get in Every Record",
        "data_content": """<p>Each record is assembled from public NPI registries, business listings, and commercial databases. Standard fields include:</p>

<ul>
<li><strong>Provider name</strong> with credentials and <strong>practice or facility name</strong></li>
<li><strong>Full practice address</strong>, validated and geocoded for territory mapping</li>
<li><strong>Business phone number</strong>, verified as active</li>
<li><strong>Practice website URL</strong></li>
<li><strong>Owner or decision-maker name</strong> at the practice level</li>
<li><strong>NPI number</strong> and <strong>taxonomy codes</strong> for specialty and subspecialty classification</li>
<li><strong>LinkedIn profile URL</strong> where available</li>
</ul>

<p>Add-ons for device sales teams:</p>

<ul>
<li><strong>Direct email addresses</strong> for the provider or practice administrator</li>
<li><strong>Mobile phone numbers</strong> for decision-makers</li>
<li><strong>Practice firmographics</strong>: provider headcount, estimated revenue, practice setting type</li>
<li><strong>Technology detection</strong>: EHR system, practice management software, and associated device or equipment data where available</li>
</ul>

<p>Data is delivered as CSV or Excel, formatted for direct import into Salesforce, HubSpot, Veeva, or whatever CRM your team uses.</p>""",

        "how_heading": "How It Works",
        "how_content": """<p><strong>Step 1: Define your territory and target.</strong> Give us your territory boundaries (zip codes, MSAs, states, or custom polygons), the subspecialties you sell to, and any practice setting or size filters. If your reps have existing territory sheets, send those and we'll work from them.</p>

<p><strong>Step 2: We build and verify your list.</strong> Records are pulled from NPI registries, business directories, and commercial databases, then cross-referenced for accuracy. We validate addresses, phone numbers, and practice associations. Duplicates are removed and records that don't meet our confidence threshold are flagged or excluded.</p>

<p><strong>Step 3: Delivered in days.</strong> Standard territory builds are delivered within 3-5 business days. You get a clean file ready for CRM import, plus a data summary showing record counts by specialty, geography, and practice setting so your sales ops team can allocate territories immediately.</p>""",

        "faqs": [
            {
                "question": "Can you filter by the procedures a surgeon performs?",
                "answer": "We filter primarily by NPI taxonomy codes, which map to specialties and subspecialties recognized by CMS. For surgical specialties, taxonomy codes often align closely with procedure categories. For example, we can separate spine surgeons from sports medicine orthopedists. If you need filtering beyond what taxonomy codes provide, we can layer in additional data points from commercial databases to narrow the list further."
            },
            {
                "question": "How often should we refresh our territory data?",
                "answer": "Most device sales teams see meaningful data decay within 90 days. We recommend quarterly refreshes for active territories. Some clients with high-churn specialties or fast-growing markets refresh monthly. The cost per record drops on refresh orders because we're updating an existing dataset rather than building from scratch. We can set up an automated schedule so your reps start each quarter with a clean list."
            },
            {
                "question": "Can you integrate with Veeva CRM?",
                "answer": "We deliver data in flat file formats that are compatible with Veeva's import tools. We don't offer a direct API integration with Veeva at this time, but the CSV output is structured to match Veeva's standard field mapping. Several of our device sales clients import Provyx data into Veeva without issues. If you need a custom field mapping, we'll adjust the export format to match your configuration."
            },
            {
                "question": "What's the difference between your data and what we get from our existing data vendor?",
                "answer": "Most enterprise healthcare data vendors sell broad, pre-packaged datasets with annual update cycles. Provyx builds targeted lists on demand, filtered to your exact criteria, and verified at the time of delivery. You're not paying for 8 million records when you need 3,000. Our pricing reflects the actual scope of your request, and the data is fresher because it's built to order, not pulled from a static warehouse."
            },
        ],

        "related_links": [
            {"text": "Custom List Building", "url": "/services/custom-list-building/"},
            {"text": "CRM Data Enrichment", "url": "/services/data-enrichment/"},
            {"text": "Browse Providers by Specialty", "url": "/providers/"},
            {"text": "Pricing", "url": "/pricing/"},
        ],

        "outbound_links": [
            "https://npiregistry.cms.hhs.gov/",
            "https://www.bls.gov/ooh/healthcare/",
        ],
    },

    # ===================================================================
    # 3. Healthcare SaaS Vendors
    # ===================================================================
    {
        "slug": "healthcare-saas",
        "title": "Healthcare Provider Data for SaaS Companies | Provyx",
        "h1": "Healthcare Provider Business Data for SaaS Vendors",
        "subtitle": "Identify which practices need your software and who makes the buying decision. Technology-enriched provider contact intelligence sourced from public NPI registries, business listings, and commercial databases.",
        "meta_description": "Provider business data for healthcare SaaS companies. Identify practices by technology stack, size, and specialty. Find decision-makers for EHR, practice management, and telehealth sales.",

        "pain_heading": "You Can't Sell Software to Practices You Can't See",
        "pain_content": """<p>You've built a great product. Maybe it's a practice management platform, a telehealth solution, a patient engagement tool, or a scheduling system. You know which types of practices would benefit most. The problem is finding them and figuring out who to call.</p>

<p>The biggest frustration for healthcare SaaS sales teams is the technology blind spot. You need to know what systems a practice currently runs. If they're on a legacy EHR that's about to lose support, that's a prime prospect. If they just signed a five-year contract with your biggest competitor, that's a waste of your SDR's time. But most provider databases don't include technology data. You find out what a practice uses on the first discovery call, after you've already spent the effort getting there.</p>

<p>Practice size matters too, and it's surprisingly hard to pin down. A solo dermatologist and a 15-provider dermatology group have completely different buying processes, budgets, and implementation requirements. Your product might be built for one and not the other. Generic databases list both under "dermatology" with no way to distinguish them. Your reps end up qualifying practice size manually on every single call.</p>

<p>Then there's the decision-maker problem. In a small practice, the physician owner makes every technology decision. In a mid-size group, it's usually an office manager or practice administrator. In a larger organization, there might be a dedicated IT director. Your outreach needs to reach the right person, but most contact databases only list the NPI-registered provider, not the operational decision-maker. The <a href="https://npiregistry.cms.hhs.gov/" target="_blank" rel="noopener">NPI Registry</a> is a good starting point for identifying practices, but it tells you nothing about who handles technology purchasing.</p>

<p>On top of all this, the healthcare SaaS market is getting crowded. The <a href="https://www.healthit.gov/" target="_blank" rel="noopener">ONC (Office of the National Coordinator for Health IT)</a> tracks certified health IT products, and the number of vendors has grown every year. To compete, you need to prospect more efficiently, not just more aggressively. That means starting with better data.</p>""",

        "use_heading": "How Healthcare SaaS Vendors Use Provyx",
        "use_content": """<p>SaaS sales teams use Provyx to build prospecting lists that go beyond name and address. Here's what that looks like.</p>

<p><strong>Technology-filtered prospecting.</strong> Our technology detection add-on identifies what EHR, practice management, scheduling, and patient communication tools a practice uses. You can build a list of practices running a specific competitor's system, practices using outdated or unsupported software, or practices with no web-visible technology stack at all. Each of these segments represents a different sales motion, and Provyx lets you separate them before your first outreach.</p>

<p><strong>Practice size segmentation.</strong> Filter by estimated provider count, revenue range, or number of locations. If your product is built for practices with 3-20 providers, you don't need to wade through solo practitioners and hospital systems to find your sweet spot. We'll deliver only the records that match your ideal practice profile.</p>

<p><strong>Decision-maker targeting.</strong> Standard records include the NPI-registered provider, but our enrichment identifies practice administrators, office managers, and IT contacts where available. For SaaS sales, reaching the person who evaluates software is often more important than reaching the physician. We help you find both.</p>

<p><strong>Specialty-based product-market fit lists.</strong> If your telehealth platform works best for behavioral health providers, or your scheduling tool is optimized for dental practices, you can build lists filtered by taxonomy code to match your product's strongest use case. This focuses your SDR team on the segments where your conversion rate is highest.</p>

<p><strong>Competitive displacement campaigns.</strong> Targeting practices that use a specific competitor? Combine technology detection with specialty and geography filters to build a highly targeted list for competitive displacement outreach. Some of our SaaS clients run dedicated campaigns against specific competitors and see 2-3x higher response rates compared to broad prospecting.</p>

<p><strong>Territory assignment and capacity planning.</strong> Before you hire your next AE or expand into a new market, use Provyx data to size the opportunity. How many practices in a given metro match your ICP? Is the market big enough to justify a dedicated rep? This kind of analysis takes days with manual research and hours with the right dataset.</p>""",

        "data_heading": "What Data You Get in Every Record",
        "data_content": """<p>Records are built from public NPI registries, business listings, and commercial databases. Standard fields:</p>

<ul>
<li><strong>Practice name</strong> and <strong>DBA name</strong></li>
<li><strong>Full practice address</strong>, geocoded and USPS-validated</li>
<li><strong>Business phone number</strong>, verified active</li>
<li><strong>Practice website URL</strong></li>
<li><strong>Owner or decision-maker name</strong></li>
<li><strong>NPI number</strong> and <strong>taxonomy codes</strong></li>
<li><strong>LinkedIn profile URL</strong> where available</li>
</ul>

<p>Add-ons that matter most for SaaS sales:</p>

<ul>
<li><strong>Technology detection</strong>: EHR vendor, practice management system, scheduling tool, patient portal, telehealth platform, and other web-visible technologies</li>
<li><strong>Direct email addresses</strong> for providers and administrators</li>
<li><strong>Mobile phone numbers</strong> for decision-makers</li>
<li><strong>Practice firmographics</strong>: provider count, estimated revenue, years in operation, number of locations</li>
</ul>

<p>Technology detection is sourced from web crawling, DNS records, job postings, and commercial technology databases. Coverage varies by practice size and web presence; larger practices with active websites have the highest detection rates.</p>""",

        "how_heading": "How It Works",
        "how_content": """<p><strong>Step 1: Define your ideal practice profile.</strong> Tell us the specialty, practice size, geography, and technology criteria that define your best-fit customer. If you've got a scoring model or ICP document, send it over. We'll translate it into data filters.</p>

<p><strong>Step 2: We build your prospecting list.</strong> Records are pulled from NPI registries, business directories, and commercial databases, then enriched with technology detection and firmographic data. Every record is de-duplicated and validated before delivery.</p>

<p><strong>Step 3: Delivered in days.</strong> Standard lists arrive within 3-5 business days. You get a formatted file ready for CRM import, plus a breakdown of record counts by specialty, geography, technology stack, and practice size so your sales ops team can segment and assign immediately.</p>""",

        "faqs": [
            {
                "question": "How accurate is the technology detection data?",
                "answer": "Technology detection accuracy depends on the practice's web presence. For practices with active websites, we detect EHR and practice management systems with high confidence when those systems have web-facing components (patient portals, online scheduling, etc.). Detection rates are lower for practices with minimal web presence or those using systems that don't expose identifiable signatures. We report confidence levels alongside technology data so you can prioritize accordingly."
            },
            {
                "question": "Can I get a list of practices NOT using any EHR?",
                "answer": "We can identify practices where we detect no EHR or practice management system. This could mean they genuinely don't use one, or it could mean their system isn't web-visible. For very small practices, especially solo providers without websites, the absence of detected technology is often a real signal. We'll flag the distinction so your team can interpret it correctly during outreach."
            },
            {
                "question": "Do you track when practices change their technology?",
                "answer": "Our technology detection is run at the time we build your list, not continuously monitored. If you order quarterly refreshes, we'll flag practices where the detected technology has changed since your last order. This is useful for identifying practices that just switched systems (and may be unhappy with their new vendor) or practices that recently adopted their first digital tool."
            },
            {
                "question": "What CRMs can I import Provyx data into?",
                "answer": "We deliver flat CSV or Excel files that work with any CRM that supports standard imports: Salesforce, HubSpot, Pipedrive, Zoho, Close, and others. We can customize column headers and field formatting to match your CRM's import template. If you need a specific format, let us know when you place your order and we'll adjust the output."
            },
        ],

        "related_links": [
            {"text": "Technology Detection Data", "url": "/services/technology-detection/"},
            {"text": "Custom List Building", "url": "/services/custom-list-building/"},
            {"text": "Browse Providers by Specialty", "url": "/providers/"},
            {"text": "Pricing", "url": "/pricing/"},
        ],

        "outbound_links": [
            "https://npiregistry.cms.hhs.gov/",
            "https://www.healthit.gov/",
        ],
    },

    # ===================================================================
    # 4. Pharma Sales Teams
    # ===================================================================
    {
        "slug": "pharma-sales",
        "title": "Healthcare Provider Data for Pharma Sales | Provyx",
        "h1": "Healthcare Provider Business Data for Pharma Sales Teams",
        "subtitle": "Prescriber-level provider contact intelligence for territory planning and outreach. NPI-verified, taxonomy-coded records sourced from public NPI registries, business listings, and commercial databases.",
        "meta_description": "Provider business data for pharma sales teams. NPI-verified prescriber contacts filtered by specialty, geography, and therapeutic area for territory planning and rep outreach.",

        "pain_heading": "Enterprise Data Pricing for Mid-Market Data Needs",
        "pain_content": """<p>Pharma sales teams know the value of good provider data. The problem isn't awareness. It's access and cost.</p>

<p>The dominant healthcare data vendors in pharma, the ones everyone recognizes, charge enterprise-level prices. Annual contracts run into six or seven figures. They bundle prescribing data, claims analytics, and provider demographics into packages designed for the top 20 pharma companies. If you're a mid-size or specialty pharma company, you're paying for a firehose when you need a garden hose.</p>

<p>Your reps need prescriber-level contact data filtered by specialty, geography, and therapeutic relevance. They need to know which physicians in their territory are likely to prescribe in their drug's category. They need accurate practice addresses so they can plan efficient routes. And they need NPI numbers and taxonomy codes for every record because your compliance team requires them for call reporting and sample tracking. The <a href="https://npiregistry.cms.hhs.gov/" target="_blank" rel="noopener">NPI Registry</a> is a free public resource, but extracting, filtering, and enriching that data into something your reps can actually use takes real work.</p>

<p>Territory planning is another pain point. When you're assigning territories or rebalancing after a product launch, you need to know how many target prescribers exist in each geography. Your existing data might be 12-18 months old by the time you use it for planning. Physicians retire, relocate, and change practice affiliations constantly. A territory that looked balanced on paper six months ago might have lost 20% of its target prescribers to normal churn.</p>

<p>The <a href="https://www.bls.gov/ooh/healthcare/" target="_blank" rel="noopener">Bureau of Labor Statistics</a> tracks physician employment trends at the macro level, but territory-level planning needs practice-level data. You need to know that Dr. Smith is still at 456 Oak Street, still practicing in the right subspecialty, and still reachable at the phone number your rep has on file.</p>

<p>Smaller pharma companies also struggle with data coverage in rural and underserved markets. Enterprise vendors optimize for high-prescriber urban markets. If your drug serves a condition that's prevalent in rural areas, you might find your data coverage drops off exactly where you need it most.</p>""",

        "use_heading": "How Pharma Sales Teams Use Provyx",
        "use_content": """<p>Pharma teams use Provyx to fill the gap between expensive enterprise data platforms and doing it manually. Here's how.</p>

<p><strong>Territory list builds by therapeutic area.</strong> Tell us the specialties and subspecialties that prescribe in your therapeutic area, define the territory boundaries, and we'll deliver a list of every matching prescriber with their current practice location, NPI, taxonomy code, and contact details. Your reps get a clean, workable list without your team spending weeks pulling and cleaning data from multiple sources.</p>

<p><strong>Territory rebalancing and planning.</strong> Before you redraw territory lines, you need current data on where target prescribers are located. Provyx delivers territory-level counts and contact lists segmented by geography, so your commercial operations team can model territory assignments based on actual prescriber density, not stale estimates.</p>

<p><strong>Launch lists for new products.</strong> Launching a new drug? You need to identify every prescriber in the target specialty across your launch markets, fast. Provyx builds launch-ready lists within days, filtered to your exact specialty and geography criteria. You can have lists in your reps' hands before launch day.</p>

<p><strong>NPI and taxonomy verification for compliance.</strong> Your compliance team needs accurate NPI numbers and taxonomy codes attached to every provider interaction your reps report. Provyx records are NPI-verified at the time of delivery. If your CRM has records with missing or outdated NPIs, send them to us for enrichment and we'll fill in the gaps.</p>

<p><strong>Call route optimization.</strong> With geocoded practice addresses, your reps can plan efficient daily routes instead of zigzagging across their territory. This is a small thing that adds up. A rep who visits 8 practices a day instead of 6 because of better routing sees 40% more providers per week.</p>

<p><strong>Supplementing your primary data vendor.</strong> You don't have to replace your existing data provider. Many pharma clients use Provyx to fill coverage gaps, especially in rural markets or for newly added specialties that aren't well-covered in their primary dataset. We deliver in the same format your team already works with, so there's no integration headache.</p>""",

        "data_heading": "What Data You Get in Every Record",
        "data_content": """<p>Every record is sourced from public NPI registries, business listings, and commercial databases. Standard fields:</p>

<ul>
<li><strong>Prescriber name</strong> with credentials and <strong>practice name</strong></li>
<li><strong>Full practice address</strong>, geocoded for territory mapping and route planning</li>
<li><strong>Business phone number</strong>, verified active</li>
<li><strong>Practice website URL</strong></li>
<li><strong>NPI number</strong> (Type 1 individual and Type 2 organizational where applicable)</li>
<li><strong>Taxonomy codes</strong> for specialty and subspecialty classification</li>
<li><strong>Owner or decision-maker name</strong> at the practice level</li>
<li><strong>LinkedIn profile URL</strong> where available</li>
</ul>

<p>Add-ons relevant for pharma:</p>

<ul>
<li><strong>Direct email addresses</strong> for prescribers or office contacts</li>
<li><strong>Mobile phone numbers</strong></li>
<li><strong>Practice firmographics</strong>: provider count, estimated patient volume indicators, practice setting type</li>
<li><strong>Technology detection</strong>: EHR system, e-prescribing platform</li>
</ul>

<p>All records include the NPI and taxonomy code fields your compliance team needs for call reporting and sample documentation.</p>""",

        "how_heading": "How It Works",
        "how_content": """<p><strong>Step 1: Define your target prescribers.</strong> Share your target specialties, therapeutic area, and territory boundaries. If you have an existing target list or territory alignment, send it and we'll build from there. We work with commercial ops teams, sales leadership, or directly with reps depending on your organization's structure.</p>

<p><strong>Step 2: We build and verify your list.</strong> Records are sourced from the NPI registry, business directories, and commercial databases. Every record is validated for current practice location and contact accuracy. We attach NPI numbers and taxonomy codes to every record and flag any that don't meet our verification threshold.</p>

<p><strong>Step 3: Delivered in days.</strong> Standard lists are ready within 3-5 business days. You receive a formatted file for CRM import plus a territory summary with record counts by specialty and geography. Rush delivery is available for product launch timelines.</p>""",

        "faqs": [
            {
                "question": "Do you include prescribing data or claims data?",
                "answer": "No. Provyx provides healthcare provider business data: contact information, practice details, NPI numbers, taxonomy codes, and firmographics. We don't sell prescribing volume data, claims data, or patient-level information. If you need prescribing analytics layered on top of accurate contact data, you can combine Provyx records with your existing prescribing data vendor by matching on NPI number."
            },
            {
                "question": "Can you separate individual NPIs from organizational NPIs?",
                "answer": "Yes. NPI records are classified as Type 1 (individual providers) or Type 2 (organizations). We can deliver lists filtered to either type or both. For pharma sales, most clients want Type 1 individual prescriber records. If you also need the organizational NPI for the practice or facility where that prescriber works, we include both in the same record where the association exists."
            },
            {
                "question": "How do you handle providers who practice at multiple locations?",
                "answer": "Providers with multiple practice locations appear in our data with their primary practice address as listed in the NPI registry. If you need all known practice locations for a provider, we can deliver multi-location records as an add-on. This is useful for reps who need to know every office where a prescriber sees patients so they can choose the most convenient location for an in-person visit."
            },
            {
                "question": "What's pricing like compared to the big healthcare data vendors?",
                "answer": "We price per record based on the scope of your request, not on an annual platform license. For a mid-size pharma company that needs territory-level prescriber lists in a few specialties, Provyx typically costs a fraction of what the enterprise vendors charge. We don't require annual commitments, and you only pay for the records and fields you actually need. Contact us for a quote based on your specific requirements."
            },
        ],

        "related_links": [
            {"text": "Custom List Building", "url": "/services/custom-list-building/"},
            {"text": "Data Enrichment", "url": "/services/data-enrichment/"},
            {"text": "Browse Providers by Specialty", "url": "/providers/"},
            {"text": "Pricing", "url": "/pricing/"},
        ],

        "outbound_links": [
            "https://npiregistry.cms.hhs.gov/",
            "https://www.bls.gov/ooh/healthcare/",
        ],
    },

    # ===================================================================
    # 5. Medical Staffing Agencies
    # ===================================================================
    {
        "slug": "medical-staffing",
        "title": "Healthcare Facility Data for Medical Staffing Agencies | Provyx",
        "h1": "Healthcare Facility and Provider Data for Medical Staffing Agencies",
        "subtitle": "Find the facility contacts, administrators, and hiring managers your recruiters need. Facility-level business data sourced from public NPI registries, business listings, and commercial databases.",
        "meta_description": "Facility and provider business data for medical staffing agencies. Administrator contacts, facility type filters, and geographic targeting for recruiter outreach.",

        "pain_heading": "Your Recruiters Are Calling the Wrong People",
        "pain_content": """<p>Medical staffing is a relationship business built on speed. When a hospital needs a travel nurse or a clinic needs a locum tenens physician, the agency that responds fastest with the right candidate wins. But speed doesn't help if your recruiters are calling the wrong person at the wrong facility.</p>

<p>The contact data problem in medical staffing is specific: you don't just need to know that a hospital exists. You need the name and direct line of the person who handles staffing, whether that's a nurse manager, an HR director, a department head, or a practice administrator. Most healthcare databases list the facility and maybe a main phone number. Your recruiter calls, gets routed through a phone tree, leaves a voicemail with someone who has nothing to do with hiring, and moves on to the next number. Multiply that by 50 calls a day across your recruiting team and you're burning enormous amounts of time on dead-end outreach.</p>

<p>Facility type matters too. Your agency might specialize in placing nurses in hospitals and urgent care centers, or you might focus on administrative staff for private practices. A generic list of "healthcare facilities" in a metro area doesn't distinguish between a 500-bed hospital system, a two-provider family medicine clinic, and a dental office. Your recruiters need lists filtered by facility type, size, and specialty focus so they're calling on organizations that actually hire the roles you place.</p>

<p>Tracking facility openings and expansions is another challenge. When a new urgent care opens or a hospital adds a wing, that's a staffing opportunity. But by the time that news shows up in your database, three other agencies have already made contact. The <a href="https://npiregistry.cms.hhs.gov/" target="_blank" rel="noopener">NPI Registry</a> tracks new organizational NPI registrations, which can signal new facilities, but monitoring it manually isn't practical.</p>

<p>The <a href="https://www.bls.gov/ooh/healthcare/" target="_blank" rel="noopener">Bureau of Labor Statistics</a> projects strong growth across most healthcare occupations through the next decade. Demand for staffing services is increasing, which means more facilities to cover and more competition among agencies. Better data isn't optional anymore. It's the difference between your recruiters spending time selling and spending time searching.</p>""",

        "use_heading": "How Medical Staffing Agencies Use Provyx",
        "use_content": """<p>Staffing agencies use Provyx to build and maintain facility-level contact lists that connect recruiters directly to the people who make hiring decisions. Here's how.</p>

<p><strong>Facility-type filtered outreach lists.</strong> Tell us what types of facilities you staff: hospitals, ambulatory surgical centers, urgent care clinics, nursing homes, private practices, or any combination. We deliver a list filtered to those facility types with administrator and decision-maker contacts attached. Your recruiters stop wasting time on facilities that don't match your placement specialties.</p>

<p><strong>Decision-maker identification.</strong> Standard Provyx records include the facility's registered contact, but our enrichment process identifies practice administrators, office managers, HR directors, and department heads where that information is available from public and commercial sources. For a recruiter, reaching the hiring manager on the first call instead of the third is a meaningful time savings.</p>

<p><strong>Geographic territory builds.</strong> Whether your agency covers a single metro area or operates nationally, you can get lists segmented by any geographic filter: zip code, county, MSA, state, or custom radius. Recruiters covering specific territories get only the facilities in their assigned area, which keeps outreach focused and reduces overlap between team members.</p>

<p><strong>New facility monitoring.</strong> We can flag recently registered organizational NPIs in your target geographies, which often correspond to new practice openings or facility expansions. This helps your team reach out to new facilities early, before they've established relationships with competing agencies.</p>

<p><strong>CRM cleanup and enrichment.</strong> Send us your existing facility database and we'll match records against current sources, update stale contacts, fill in missing fields, and identify facilities that have closed or changed ownership. Most staffing agencies accumulate contact data over years, and a significant percentage of it degrades without regular maintenance.</p>

<p><strong>Specialty-specific facility lists.</strong> If you place orthopedic surgeons, you need facilities with orthopedic departments. If you staff behavioral health professionals, you need psychiatric facilities and counseling centers. Provyx filters by the specialties practiced at each facility, not just the facility type, so your lists match the roles you actually place.</p>""",

        "data_heading": "What Data You Get in Every Record",
        "data_content": """<p>Records are assembled from public NPI registries, business listings, and commercial databases. Standard fields include:</p>

<ul>
<li><strong>Facility or practice name</strong> and <strong>DBA name</strong></li>
<li><strong>Full address</strong>, validated and geocoded</li>
<li><strong>Business phone number</strong>, verified active</li>
<li><strong>Facility website URL</strong></li>
<li><strong>Administrator, owner, or decision-maker name</strong></li>
<li><strong>Organizational NPI number</strong> and <strong>taxonomy codes</strong> indicating facility type and specialty focus</li>
<li><strong>LinkedIn profile URL</strong> for decision-makers where available</li>
</ul>

<p>Add-ons for staffing agencies:</p>

<ul>
<li><strong>Direct email addresses</strong> for administrators and hiring contacts</li>
<li><strong>Mobile phone numbers</strong> for decision-makers</li>
<li><strong>Facility firmographics</strong>: bed count (hospitals), provider headcount, estimated revenue, number of locations</li>
<li><strong>Technology detection</strong>: staffing platforms, scheduling software, and credentialing systems in use</li>
</ul>

<p>Data is delivered as CSV or Excel, formatted for import into your ATS, CRM, or staffing platform.</p>""",

        "how_heading": "How It Works",
        "how_content": """<p><strong>Step 1: Tell us what you staff and where.</strong> Share the facility types, specialties, and geographic areas your agency covers. If you have role-specific requirements (e.g., you only place RNs in hospital settings), include that so we can filter accordingly.</p>

<p><strong>Step 2: We build your facility list.</strong> Records are pulled from NPI registries, business directories, state licensing databases, and commercial sources. We identify decision-makers, validate contact information, and remove facilities that have closed or don't match your criteria.</p>

<p><strong>Step 3: Delivered in days.</strong> Standard facility lists are ready within 3-5 business days. You receive a formatted file with a summary of record counts by facility type, geography, and specialty so your team can assign outreach territories immediately.</p>""",

        "faqs": [
            {
                "question": "Can you identify facilities that are actively hiring?",
                "answer": "We don't track real-time job postings, but we can identify signals that correlate with hiring activity: recently registered NPIs (new facilities), facilities in high-growth markets, and organizations that have recently expanded their provider count based on NPI registry updates. Some staffing clients combine Provyx facility data with job board monitoring tools to prioritize outreach to facilities with open positions."
            },
            {
                "question": "Do you cover nursing homes and long-term care facilities?",
                "answer": "Yes. Our data includes nursing homes, skilled nursing facilities, assisted living facilities, and other long-term care settings. These facilities have organizational NPIs and are well-represented in our sources. We can filter specifically for long-term care facility types if that's your agency's focus. Facility firmographic add-ons include bed count for institutional settings."
            },
            {
                "question": "How do you identify the hiring decision-maker at a facility?",
                "answer": "We start with the registered contact on the facility's NPI record, then enrich from business directories, LinkedIn, and commercial databases to identify administrators, HR directors, and department heads. For smaller practices, the decision-maker is often the physician owner. For larger facilities, we look for titles associated with staffing and HR functions. Coverage of decision-maker data varies by facility size. Larger organizations with a web presence have the best coverage."
            },
            {
                "question": "Can I get data for a single metro area or do I need to order nationally?",
                "answer": "You can order data for any geographic scope: a single zip code, a metro area, a state, or the entire country. We price based on record count, not geographic coverage. Most staffing agencies start with their primary market and expand from there. There's no minimum order size and no requirement to purchase national data if you only operate regionally."
            },
        ],

        "related_links": [
            {"text": "Custom List Building", "url": "/services/custom-list-building/"},
            {"text": "Data Enrichment", "url": "/services/data-enrichment/"},
            {"text": "Browse Providers by Specialty", "url": "/providers/"},
            {"text": "Pricing", "url": "/pricing/"},
        ],

        "outbound_links": [
            "https://npiregistry.cms.hhs.gov/",
            "https://www.bls.gov/ooh/healthcare/",
        ],
    },

    # ===================================================================
    # 6. Healthcare Consulting Firms
    # ===================================================================
    {
        "slug": "healthcare-consulting",
        "title": "Healthcare Provider Data for Consulting Firms | Provyx",
        "h1": "Healthcare Provider Business Data for Consulting Firms",
        "subtitle": "Market sizing, competitive analysis, and provider demographics for strategic engagements. Project-scoped provider contact intelligence sourced from public NPI registries, business listings, and commercial databases.",
        "meta_description": "Provider business data for healthcare consulting firms. Market sizing, competitive analysis, M&A due diligence, and provider demographics on a per-project basis.",

        "pain_heading": "You Don't Need an Enterprise License for a Three-Month Project",
        "pain_content": """<p>Healthcare consulting firms need provider data, but they don't need it the way pharma companies or hospital systems do. Your data needs are project-driven. One quarter you're sizing a market for a client entering behavioral health. The next quarter you're doing competitive analysis on primary care groups in the Southeast. Six months later you're supporting M&A due diligence on a portfolio of dental practices.</p>

<p>The problem is that the healthcare data industry is built for enterprise buyers with recurring, high-volume needs. The major vendors want annual contracts, minimum commitments, and platform fees that assume you'll be querying their database every day. For a consulting firm that needs deep data access for 8-12 weeks and then nothing for months, that pricing model is punishing. You end up paying $40,000 a year for a data license you use on three projects.</p>

<p>Some firms try to work around this by pulling data from public sources manually. The <a href="https://npiregistry.cms.hhs.gov/" target="_blank" rel="noopener">NPI Registry</a> is free and searchable, and it contains every registered provider and organization in the country. But extracting, cleaning, and structuring that data into something useful for a market analysis takes a junior analyst a week of work. That's a week of billing you can't pass through to the client, and the output still won't have the practice-level firmographics and contact details your deliverable requires.</p>

<p>Then there's the specificity problem. Your engagement might require provider counts by specialty within specific county boundaries, or practice ownership data for a due diligence target list, or competitive landscape mapping for a specific service line. Generic databases don't slice that way. You end up buying a broad dataset and spending hours filtering it down to the 2,000 records you actually need, while paying for the 200,000 you don't.</p>

<p>The <a href="https://www.bls.gov/ooh/healthcare/" target="_blank" rel="noopener">Bureau of Labor Statistics</a> and CMS data releases are useful for macro-level analysis, but they don't give you practice-level intelligence. For the kind of work your clients expect, you need data that connects the macro numbers to specific practices, providers, and geographies.</p>""",

        "use_heading": "How Healthcare Consulting Firms Use Provyx",
        "use_content": """<p>Consulting firms use Provyx as a project-scoped data source that delivers exactly what an engagement requires, without the overhead of an enterprise data license. Here's what that looks like.</p>

<p><strong>Market sizing and opportunity analysis.</strong> Your client wants to know how many providers of a specific specialty exist in a target geography, what their practice sizes look like, and where the density is highest. Provyx delivers a complete dataset filtered to those parameters: provider counts, practice locations, estimated sizes, and geographic distribution. You get the numbers your strategy deck needs without spending a week building them from scratch.</p>

<p><strong>Competitive landscape mapping.</strong> For engagements that require understanding the competitive environment, whether for a new market entry, a service line expansion, or a payer network analysis, Provyx provides practice-level data that shows who's operating where. Combine specialty filters with geography and practice size to map out the competitive terrain your client faces.</p>

<p><strong>M&A due diligence.</strong> When a private equity firm or health system is evaluating an acquisition target, they need to validate the provider roster, verify practice locations, and understand the competitive context. Provyx delivers NPI-verified provider lists, practice addresses, and market data that supports due diligence without requiring a long-term data subscription. Some firms use us for a single due diligence project and come back whenever the next deal materializes.</p>

<p><strong>Provider demographic analysis.</strong> Your engagement might require understanding the age distribution of providers in a specialty, the geographic clustering of certain practice types, or the ownership patterns in a market. Provyx data, combined with publicly available NPI and workforce data, gives your analysts the raw material for demographic modeling without starting from zero.</p>

<p><strong>Network adequacy and access analysis.</strong> For engagements with payers or state health agencies, you may need to assess provider access in specific geographies. Provyx data provides practice locations and specialty classifications at the granularity needed for access mapping and gap analysis.</p>

<p><strong>Custom data pulls for client deliverables.</strong> Sometimes you just need a specific dataset to support a slide or an appendix. A list of all dermatology practices in Texas with more than 5 providers. Every urgent care facility that opened in the last 3 years in Florida. Provyx builds these one-off pulls quickly and affordably, so you're not spending analyst time on data collection when they should be doing analysis.</p>""",

        "data_heading": "What Data You Get in Every Record",
        "data_content": """<p>Records are sourced from public NPI registries, business listings, and commercial databases. Standard fields:</p>

<ul>
<li><strong>Practice or facility name</strong> and <strong>DBA name</strong></li>
<li><strong>Full address</strong>, geocoded for mapping and geographic analysis</li>
<li><strong>Business phone number</strong></li>
<li><strong>Practice website URL</strong></li>
<li><strong>Owner or principal provider name</strong></li>
<li><strong>NPI number</strong> (Type 1 and Type 2) and <strong>taxonomy codes</strong></li>
<li><strong>LinkedIn profile URL</strong> where available</li>
</ul>

<p>Add-ons that consulting firms frequently request:</p>

<ul>
<li><strong>Practice firmographics</strong>: provider count, estimated revenue range, years in operation, number of locations, practice setting type</li>
<li><strong>Technology detection</strong>: EHR, practice management, and other technology systems in use</li>
<li><strong>Direct email addresses</strong> and <strong>mobile phone numbers</strong> (useful if the engagement includes primary research or outreach)</li>
</ul>

<p>Firmographics are the most requested add-on for consulting engagements. Practice size, revenue indicators, and multi-location data turn a simple provider list into an analytical dataset your team can model with.</p>""",

        "how_heading": "How It Works",
        "how_content": """<p><strong>Step 1: Scope the data need.</strong> Tell us what your engagement requires: the specialties, geographies, practice characteristics, and data fields. We work with partners, analysts, and project managers depending on your firm's structure. If you're not sure exactly what filters you need, we'll help translate your research question into data parameters.</p>

<p><strong>Step 2: We build your dataset.</strong> Records are pulled, matched, and enriched from multiple sources. We structure the output to match your analytical needs, whether that's a flat list, a geographic breakdown, or a multi-tab workbook segmented by market. Quality checks are run on every deliverable before it ships.</p>

<p><strong>Step 3: Delivered in days.</strong> Standard datasets are ready within 3-5 business days. Complex or large-scope requests may take slightly longer. You get a formatted file plus documentation on sources, methodology, and any caveats your team should be aware of when using the data in client deliverables.</p>""",

        "faqs": [
            {
                "question": "Do I need to sign an annual contract?",
                "answer": "No. Provyx is designed for project-based purchasing. You order the data you need for a specific engagement, and that's it. There are no annual commitments, platform fees, or minimum spend requirements. Some consulting firms work with us on multiple projects throughout the year, but each order is independent. If you want a recurring arrangement with volume discounts, we can set that up, but it's not required."
            },
            {
                "question": "Can I include Provyx data in client deliverables?",
                "answer": "Yes. The data you purchase is yours to use in your engagement deliverables: reports, strategy decks, market analyses, and appendices. We don't require attribution in your client-facing materials. If your client wants to license the underlying dataset for their own ongoing use, that's a separate conversation, but your consulting deliverable is fully covered by the purchase."
            },
            {
                "question": "How do you handle data for M&A due diligence?",
                "answer": "For due diligence engagements, we can build targeted datasets around a specific acquisition target or market. This typically includes verifying the target's provider roster against NPI records, mapping their practice locations, and building a competitive dataset for the surrounding market. We work under NDA when required and can accommodate expedited timelines for deal-driven deadlines."
            },
            {
                "question": "What geographic granularity is available?",
                "answer": "We can filter and deliver data at any geographic level: national, state, MSA, county, zip code, or custom radius around a point. For consulting engagements that require geographic analysis, we include geocoded coordinates with every record so your team can run their own mapping and distance calculations. If you need data structured by custom geographic boundaries (e.g., service areas or trade areas), we can accommodate that as well."
            },
        ],

        "related_links": [
            {"text": "Custom List Building", "url": "/services/custom-list-building/"},
            {"text": "Market Analysis Data", "url": "/services/market-analysis/"},
            {"text": "Browse Providers by Specialty", "url": "/providers/"},
            {"text": "Pricing", "url": "/pricing/"},
        ],

        "outbound_links": [
            "https://npiregistry.cms.hhs.gov/",
            "https://www.bls.gov/ooh/healthcare/",
        ],
    },

    # ===================================================================
    # 7. Health IT Companies
    # ===================================================================
    {
        "slug": "health-it",
        "title": "Healthcare Provider Data for Health IT Companies | Provyx",
        "h1": "Healthcare Provider Business Data for Health IT Companies",
        "subtitle": "Find practices that need your technology by seeing what they already use. Technology-enriched provider contact intelligence sourced from public NPI registries, business listings, and commercial databases.",
        "meta_description": "Provider business data with technology detection for health IT companies. Identify practices by current EHR, practice management system, and tech readiness for targeted sales outreach.",

        "pain_heading": "You're Prospecting Blind Without Technology Data",
        "pain_content": """<p>Health IT companies have a unique sales challenge. You're not just selling to healthcare providers. You're selling to providers who have a specific technology problem. Maybe they're on an EHR that's being sunset. Maybe their practice management system can't scale with their growth. Maybe they don't have a patient portal and their patients are asking for one. Whatever the scenario, the first thing you need to know about a prospect isn't their specialty or location. It's what technology they currently use.</p>

<p>And that's the information that's hardest to get. Standard healthcare provider databases will tell you a practice's name, address, NPI number, and specialty. They won't tell you whether that practice runs Epic, Athenahealth, eClinicalWorks, or a paper-based system held together with fax machines. Without that technology layer, your sales team is prospecting blind. Every call starts with discovery that should have happened before the call was made.</p>

<p>Practice size adds another dimension. A solo family medicine provider has different technology needs, budget constraints, and buying processes than a 30-provider multispecialty group. Your product might be perfect for mid-size practices and completely wrong for enterprise health systems. But without firmographic data attached to provider records, your SDRs can't segment their outreach by practice size. They discover they're talking to the wrong-sized organization halfway through the demo.</p>

<p>The <a href="https://npiregistry.cms.hhs.gov/" target="_blank" rel="noopener">NPI Registry</a> is a useful starting point for identifying practices and providers, but it contains zero technology information. The <a href="https://www.healthit.gov/" target="_blank" rel="noopener">ONC's Health IT Dashboard</a> publishes aggregate data on certified EHR adoption, but it doesn't tell you what specific practice at a specific address uses what specific system. That practice-level technology intelligence is the missing piece for health IT sales teams, and it's what most data vendors either don't provide or charge a premium for as part of a large bundled package you don't need.</p>

<p>The competitive landscape in health IT is intense. Hundreds of vendors are selling to the same universe of practices. The companies that win are the ones who show up with relevant outreach: "I noticed you're using [System X], and here's why practices like yours are switching." That message only works if you actually know what System X is before you pick up the phone.</p>""",

        "use_heading": "How Health IT Companies Use Provyx",
        "use_content": """<p>Health IT sales teams use Provyx to add the technology layer that transforms generic provider lists into actionable prospecting data. Here's how.</p>

<p><strong>Competitor install base targeting.</strong> This is the most common use case. You tell us which competitor systems you want to target, and we deliver a list of practices that currently use those systems, filtered by your specialty, geography, and practice size criteria. Your reps reach out with messaging that's specific to the prospect's current technology situation instead of a generic "are you happy with your EHR?" opening.</p>

<p><strong>Greenfield opportunity identification.</strong> Some practices, especially smaller ones, still operate without a modern EHR or practice management system. Our technology detection can identify practices where we find no evidence of a major system in use. These are greenfield opportunities: prospects who haven't committed to a competitor yet and may be more receptive to a first-time purchase than a switching conversation.</p>

<p><strong>Technology readiness scoring.</strong> By combining technology detection with practice firmographics, you can estimate a practice's technology readiness. A 10-provider group with a website, patient portal, and online scheduling is probably more tech-forward (and potentially a faster sales cycle) than a practice with no web presence. Provyx data gives your team the inputs to build this kind of scoring model.</p>

<p><strong>Practice size and specialty filtering.</strong> Your product might be built for dental practices with 3-10 operatories, or behavioral health groups with multiple locations, or primary care practices with a specific provider count. Provyx lets you filter by estimated practice size, specialty (via taxonomy code), and other firmographic attributes so your list matches your product's sweet spot precisely.</p>

<p><strong>Decision-maker identification.</strong> In small practices, the physician owner makes technology decisions. In mid-size groups, it's often a practice administrator or office manager. Provyx records include the NPI-registered provider and, where available, the practice administrator or operational contact. For health IT sales, reaching the person who evaluates and purchases technology is often more valuable than reaching the clinical provider.</p>

<p><strong>Market sizing for investors and board reporting.</strong> If you need to quantify your total addressable market, Provyx data helps you count the number of practices that match your ICP by specialty, size, geography, and technology profile. This is useful for investor decks, board presentations, and strategic planning where you need hard numbers on market size, not estimates.</p>""",

        "data_heading": "What Data You Get in Every Record",
        "data_content": """<p>Records are built from public NPI registries, business listings, and commercial databases. Standard fields:</p>

<ul>
<li><strong>Practice name</strong> and <strong>DBA name</strong></li>
<li><strong>Full practice address</strong>, geocoded and validated</li>
<li><strong>Business phone number</strong>, verified active</li>
<li><strong>Practice website URL</strong></li>
<li><strong>Owner or decision-maker name</strong></li>
<li><strong>NPI number</strong> and <strong>taxonomy codes</strong></li>
<li><strong>LinkedIn profile URL</strong> where available</li>
</ul>

<p>Add-ons that health IT companies rely on most:</p>

<ul>
<li><strong>Technology detection</strong>: EHR vendor, practice management system, scheduling software, patient portal, telehealth platform, billing software, and other web-visible technologies. Detection is sourced from website analysis, DNS records, job postings, and commercial technology databases.</li>
<li><strong>Practice firmographics</strong>: provider count, estimated revenue, years in operation, number of locations</li>
<li><strong>Direct email addresses</strong> for providers and practice administrators</li>
<li><strong>Mobile phone numbers</strong> for decision-makers</li>
</ul>

<p>Technology detection coverage is highest for practices with active websites and web-facing patient tools. Larger and more digitally mature practices have the best detection rates. We include a confidence indicator with each technology data point so your team can prioritize high-confidence records.</p>""",

        "how_heading": "How It Works",
        "how_content": """<p><strong>Step 1: Define your ideal prospect.</strong> Tell us the specialties, practice sizes, geographies, and technology criteria you're targeting. If you want practices using a specific competitor's system, or practices with no detected EHR, include that. We'll build filters that match your sales motion.</p>

<p><strong>Step 2: We build your technology-enriched list.</strong> Records are pulled from NPI registries, business directories, and commercial databases, then enriched with technology detection and firmographic data. Every record is validated and de-duplicated. Technology data is sourced at the time of list build, not pulled from a static snapshot.</p>

<p><strong>Step 3: Delivered in days.</strong> Standard lists arrive within 3-5 business days. Technology-enriched lists may take slightly longer depending on the scope of detection required. You receive a formatted file for CRM import plus a summary of records by technology stack, specialty, and geography.</p>""",

        "faqs": [
            {
                "question": "What technology systems can you detect?",
                "answer": "We detect a wide range of web-visible healthcare technology: EHR platforms (Epic, Athenahealth, eClinicalWorks, NextGen, DrChrono, and dozens of others), practice management systems, patient portals, online scheduling tools, telehealth platforms, billing systems, and marketing tools. Detection is based on web signatures, DNS records, job postings, and commercial technology databases. If you're targeting practices using a specific system, let us know and we'll confirm detection coverage before you order."
            },
            {
                "question": "How current is the technology detection data?",
                "answer": "Technology detection is run at the time we build your list, so the data reflects what we can detect at that point. It's not pulled from a pre-built database that may be months old. If you order quarterly refreshes, we'll re-run detection and flag any changes. Practices don't switch core technology systems frequently, so detection data tends to stay valid for 6-12 months for major systems like EHRs. Ancillary tools like scheduling software change more often."
            },
            {
                "question": "Can you detect technology for practices without websites?",
                "answer": "Detection is significantly harder for practices without a web presence. For those practices, we rely on secondary signals: job postings that mention specific systems, commercial technology databases, and vendor customer lists where available. Coverage for practices without websites is lower, and we'll be transparent about that in your data summary. If your target market includes many small or rural practices with limited web presence, we'll discuss expected coverage upfront."
            },
            {
                "question": "Do you offer an API for ongoing technology data access?",
                "answer": "We don't offer a self-service API at this time. Our technology-enriched data is delivered as flat files (CSV or Excel) built to your specifications. For health IT companies that need regular access, we offer recurring delivery schedules (monthly or quarterly) with updated technology detection on each refresh. If API access is important for your workflow, contact us to discuss what we're planning on that front."
            },
        ],

        "related_links": [
            {"text": "Technology Detection Data", "url": "/services/technology-detection/"},
            {"text": "Custom List Building", "url": "/services/custom-list-building/"},
            {"text": "Browse Providers by Specialty", "url": "/providers/"},
            {"text": "Pricing", "url": "/pricing/"},
        ],

        "outbound_links": [
            "https://npiregistry.cms.hhs.gov/",
            "https://www.healthit.gov/",
        ],
    },
]

# Comparison pages
COMPARISONS = [
    # ======================================================================
    # 1. Provyx vs. ZoomInfo
    # ======================================================================
    {
        "slug": "provyx-vs-zoominfo",
        "competitor_name": "ZoomInfo",
        "page_title": "Provyx vs. ZoomInfo: Healthcare Provider Data Compared",
        "meta_description": (
            "Detailed comparison of Provyx and ZoomInfo for healthcare provider "
            "business data. Pricing, NPI verification, taxonomy filtering, and "
            "data accuracy evaluated side by side."
        ),
        "hero_headline": "Provyx vs. ZoomInfo",
        "hero_subheadline": (
            "ZoomInfo covers 50+ industries. Provyx was built for one: healthcare. "
            "Here's how they compare when you need accurate provider contact intelligence."
        ),

        # -- Intro paragraph (~200 words) --
        "intro": (
            "<p>If you sell software, services, or products to healthcare providers, "
            "you've probably evaluated ZoomInfo. It's the largest general-purpose B2B "
            "contact database on the market, and it shows up on almost every shortlist "
            "for sales intelligence tools. The problem is that \"general-purpose\" "
            "comes with trade-offs when you need healthcare-specific provider data.</p>"
            "<p>This comparison is for marketing and sales leaders at healthcare "
            "technology companies, medical device manufacturers, staffing firms, "
            "pharmaceutical commercial teams, and anyone else whose pipeline depends "
            "on reaching the right physicians, practice managers, or clinical "
            "decision-makers. We'll walk through pricing structures, data depth, "
            "contract terms, and the specific gaps that appear when a horizontal "
            "platform tries to serve a vertical market. We'll also be honest about "
            "where ZoomInfo has advantages, because it does, particularly if your "
            "outreach extends well beyond healthcare.</p>"
            "<p>Everything here is based on publicly available pricing pages, "
            "G2 and Gartner Peer Insights reviews, vendor documentation, and our "
            "own product specs. Where we cite Provyx capabilities, we'll tell you "
            "exactly where that data comes from: public NPI registries, business "
            "listings, and commercial databases.</p>"
            "<p>One note before we start: Provyx is not the right tool for "
            "everyone reading this. If you prospect heavily outside of healthcare, "
            "ZoomInfo may genuinely be the better investment. We'll explain why "
            "in the scenario breakdown toward the end of this page. This isn't "
            "a comparison designed to steer you toward one answer. It's designed "
            "to help you make the call faster.</p>"
        ),

        # -- Quick Comparison Table (8 rows) --
        "comparison_table_rows": [
            ("Starting Price", "$14,995/year (Professional plan)", "Pay-per-record; no annual minimum"),
            ("Contract Terms", "Annual contract, auto-renews, 60-day cancellation notice", "Month-to-month or per-project; cancel anytime"),
            ("Healthcare Focus", "One of 50+ industries covered", "100% healthcare provider focus"),
            ("NPI Verification", "Not available", "Every record matched against the NPI Registry"),
            ("Taxonomy Filtering", "Not available", "Filter by 800+ NUCC taxonomy codes"),
            ("Data Delivery", "Platform access with seat-based licensing", "CSV, API, or direct CRM push"),
            ("Best For", "Multi-industry enterprise sales teams", "Teams selling exclusively into healthcare"),
            ("Key Risk", "High annual cost; data may lack healthcare depth", "Not suitable if you also prospect outside healthcare"),
        ],

        # -- Deep Dive: Competitor (800-1,200 words) --
        "competitor_what_they_offer": (
            "<h3>What ZoomInfo Offers</h3>"
            "<p>ZoomInfo is a publicly traded B2B data and sales intelligence platform "
            "that aggregates contact records, company firmographics, technographic "
            "signals, and intent data across virtually every industry. Its database "
            "includes over 100 million business professional profiles according to "
            "the company's own reporting, and it covers companies ranging from "
            "two-person startups to Fortune 500 enterprises.</p>"
            "<p>The platform's core value proposition is breadth. If you're building "
            "account lists that span manufacturing, financial services, technology, "
            "and healthcare simultaneously, ZoomInfo gives you a single interface "
            "to do that. You get access to org charts, direct-dial phone numbers, "
            "verified email addresses, and website visitor tracking through its "
            "suite of products (SalesOS, MarketingOS, TalentOS).</p>"
            "<p>For healthcare specifically, ZoomInfo does include records for "
            "hospitals, clinics, physician practices, and healthcare executives. "
            "You can filter by SIC and NAICS codes related to healthcare, and you "
            "can layer on intent signals to identify organizations that are actively "
            "researching topics related to your solution. The data is refreshed on "
            "a rolling basis through a combination of web scraping, email pattern "
            "analysis, user-contributed data, and manual research.</p>"
            "<p>ZoomInfo also provides workflow automation tools, conversation "
            "intelligence (through its Chorus acquisition), and engagement tracking. "
            "It's designed to be an all-in-one revenue operations platform, not just "
            "a data vendor. That scope is a genuine strength for organizations whose "
            "go-to-market motion spans multiple verticals.</p>"
            "<p>The platform's data collection methods include a contributor network "
            "of users who install a browser extension or email plugin. In exchange "
            "for free or discounted access, these users share contact data from their "
            "email headers and address books. ZoomInfo also crawls public websites, "
            "SEC filings, job postings, and social media profiles to build and update "
            "its records. For industries where professionals actively maintain public "
            "profiles and change jobs in patterns that leave digital trails, this "
            "methodology works well. For healthcare, where many providers don't have "
            "LinkedIn profiles and practice information is scattered across state "
            "licensing boards and federal registries, the methodology has blind spots.</p>"
            "<p><a href=\"https://www.zoominfo.com/\" target=\"_blank\" rel=\"noopener\">"
            "ZoomInfo's</a> G2 rating sits at approximately 4.4 out of 5 stars, "
            "with over 8,000 reviews. The positive reviews consistently cite the "
            "platform's ease of use for prospecting, the depth of company "
            "information, and the quality of intent data signals. The negative "
            "reviews cluster around pricing complaints, data accuracy for niche "
            "industries, and the auto-renewal contract structure. Healthcare-specific "
            "complaints are harder to find in the review corpus because most "
            "ZoomInfo users are selling into technology, not medicine, but the ones "
            "that do surface tend to mention outdated provider contact information "
            "and difficulty filtering by clinical specialty.</p>"
        ),
        "competitor_pricing": (
            "<h3>Pricing and Contracts</h3>"
            "<p>ZoomInfo doesn't publish a simple pricing grid, but the publicly "
            "available information and user-reported figures paint a consistent "
            "picture. The Professional plan starts at roughly $14,995 per year "
            "for a single user with a set number of credits. The Advanced plan, "
            "which adds intent data and more detailed company attributes, is "
            "typically quoted between $24,995 and $39,995 per year. The Elite "
            "tier, which layers on real-time intent signals and AI-driven "
            "recommendations, has been reported north of $40,000 annually.</p>"
            "<p>All plans operate on annual contracts. Renewals are automatic, and "
            "you're required to give at least 60 days' written notice before the "
            "renewal date to cancel. Multiple <a href=\"https://www.g2.com/products/zoominfo/reviews\" "
            "target=\"_blank\" rel=\"noopener\">G2 reviews</a> mention being caught "
            "off guard by auto-renewal clauses and report annual price increases in "
            "the range of 10% to 30% at renewal. If you miss the cancellation "
            "window, you're locked in for another full year.</p>"
            "<p>Seat-based pricing adds up quickly if multiple team members need "
            "access. Some organizations report total annual costs exceeding "
            "$60,000 to $100,000 when you factor in additional seats, premium "
            "features, and overage charges for exceeding credit allotments. For "
            "a funded startup or mid-market company focused on a single vertical "
            "like healthcare, that price tag can be difficult to justify, "
            "especially when much of the database covers industries you'll never "
            "prospect into.</p>"
            "<p>There's also a credit system within each plan. You get a set "
            "number of contact and company data credits per billing period, and "
            "exceeding those limits triggers overage fees or requires an upgrade. "
            "For teams that run large-volume outbound campaigns, credits can "
            "deplete faster than expected, especially when building initial "
            "target lists for a new market or territory. The combination of "
            "annual commitment, seat-based licensing, and credit-based data "
            "access creates a pricing model that's optimized for predictable, "
            "enterprise-scale usage patterns rather than the variable, "
            "campaign-driven patterns common in healthcare sales.</p>"
        ),
        "competitor_shortcomings": (
            "<h3>Where ZoomInfo Falls Short for Healthcare</h3>"
            "<p>The gaps aren't about data quality in an absolute sense. ZoomInfo "
            "is good at what it does. The gaps are about specificity.</p>"
            "<p><strong>No NPI verification.</strong> The National Provider Identifier "
            "is the universal key for identifying healthcare providers in the United "
            "States. Every physician, nurse practitioner, dentist, and clinical "
            "professional who bills federal programs has one, and it's maintained "
            "by CMS in a <a href=\"https://npiregistry.cms.hhs.gov/\" target=\"_blank\" "
            "rel=\"noopener\">publicly searchable registry</a>. ZoomInfo doesn't "
            "match its records against NPI data. That means you can't confirm "
            "whether a contact is an active, licensed provider, and you can't "
            "cross-reference with the taxonomy codes that define their specialty.</p>"
            "<p><strong>No taxonomy code filtering.</strong> If you need to reach "
            "every interventional cardiologist in Texas, or every pediatric "
            "nurse practitioner in the Mid-Atlantic, you need to filter by NUCC "
            "taxonomy codes. ZoomInfo's filtering relies on job titles and industry "
            "classifications, which are inconsistent across healthcare organizations. "
            "A \"Medical Director\" at a three-physician dermatology practice is a "
            "very different buyer than a \"Medical Director\" at a 400-bed hospital "
            "system. Taxonomy codes eliminate that ambiguity.</p>"
            "<p><strong>Practice-level intelligence is thin.</strong> ZoomInfo's "
            "company records are built around legal entities and corporate "
            "hierarchies. Healthcare doesn't always organize that way. A physician "
            "might practice at two hospitals, own a separate outpatient surgery "
            "center, and bill under a third entity. ZoomInfo's data model isn't "
            "designed to capture those relationships. You often end up with a "
            "hospital system's corporate headquarters address rather than the "
            "actual clinic location where a provider sees patients.</p>"
            "<p><strong>Stale specialty data.</strong> Physicians change practice "
            "locations, retire, or shift specialties more often than executives "
            "change companies. ZoomInfo's refresh cycle, which works well for "
            "tracking job changes at tech companies, doesn't always keep pace "
            "with the churn in healthcare provider directories. Users targeting "
            "healthcare frequently report higher bounce rates on emails and "
            "outdated phone numbers compared to their results in other "
            "industries.</p>"
            "<p><strong>You're paying for industries you don't need.</strong> "
            "This is the fundamental unit economics problem. If 100% of your "
            "revenue comes from healthcare, you're subsidizing ZoomInfo's data "
            "collection across dozens of industries you'll never touch. That's "
            "a real cost, not just a philosophical objection, because it inflates "
            "your per-lead acquisition cost significantly.</p>"
            "<p><strong>Compliance and data sourcing concerns in healthcare.</strong> "
            "ZoomInfo's contributor network model, where users share contact data "
            "from their inboxes in exchange for platform access, raises questions "
            "in regulated industries. Healthcare organizations are often cautious "
            "about how provider contact information is collected and shared. While "
            "ZoomInfo's data collection is legal, the sourcing methodology doesn't "
            "align with the expectations many healthcare compliance teams have about "
            "where their provider contact lists originate. If your compliance team "
            "asks \"where did this data come from,\" the answer with ZoomInfo is "
            "more complex than it is with a platform that sources exclusively from "
            "public registries, business listings, and commercial databases.</p>"
        ),
        "competitor_outbound_links": [
            ("https://www.zoominfo.com/", "ZoomInfo official website"),
            ("https://npiregistry.cms.hhs.gov/", "CMS NPI Registry"),
        ],

        # -- Deep Dive: Provyx (500-800 words) --
        "provyx_what_delivers": (
            "<h3>What Provyx Delivers</h3>"
            "<p>Provyx is a healthcare provider business data platform. That's "
            "all it does. There's no intent data for SaaS companies, no "
            "technographic signals for e-commerce brands, and no org charts "
            "for financial institutions. Every record in the Provyx database "
            "represents a healthcare provider or a practice location, and "
            "every record is verified against the National Provider Identifier "
            "Registry maintained by the Centers for Medicare and Medicaid "
            "Services.</p>"
            "<p>The database covers physicians, nurse practitioners, physician "
            "assistants, dentists, optometrists, chiropractors, physical "
            "therapists, behavioral health providers, and other licensed "
            "clinicians across the United States. Records include NPI numbers, "
            "taxonomy codes (using the NUCC classification system), practice "
            "addresses, phone numbers, email addresses, affiliated organizations, "
            "and, where available, prescribing behavior indicators and "
            "referral patterns.</p>"
            "<p>Data is sourced from public NPI registries, business listings, "
            "state licensing boards, and commercial databases. Provyx doesn't "
            "scrape social media profiles or rely on user-contributed data "
            "from email plugins. The sourcing methodology is designed for "
            "a regulated industry where accuracy matters more than volume.</p>"
        ),
        "provyx_healthcare_handling": (
            "<h3>How Provyx Handles Healthcare Provider Business Data</h3>"
            "<p>Every record in Provyx is anchored to an NPI number. That's "
            "not a feature bolted onto a general database; it's the primary "
            "key around which the entire data model is built. When you search "
            "for records, you're starting from a verified identifier that the "
            "federal government requires every healthcare provider to have.</p>"
            "<p>Taxonomy code filtering lets you target providers by their "
            "actual clinical specialty, not by a job title that might mean "
            "different things at different organizations. There are over 800 "
            "NUCC taxonomy codes, and Provyx supports filtering by any of them, "
            "individually or in combination. You can pull every orthopedic "
            "surgeon within 50 miles of a ZIP code, or every family medicine "
            "physician in a specific state, and know that the specialty "
            "designation comes from their NPI registration rather than a "
            "self-reported LinkedIn profile.</p>"
            "<p>Practice-level data is another differentiator. Provyx maps "
            "providers to their actual practice locations, not just the "
            "corporate entity that employs them. If a cardiologist practices "
            "at two different hospitals and an outpatient clinic, Provyx "
            "shows you all three locations with separate contact details "
            "for each.</p>"
            "<p>There's also the question of data transparency. Every record "
            "in Provyx can be traced back to its source: a public NPI "
            "registry entry, a state licensing board record, or a verified "
            "business listing. When your compliance team or a prospect asks "
            "how you got their information, you have a clear, auditable "
            "answer. That matters in healthcare in ways it doesn't matter "
            "when you're emailing software engineers.</p>"
            "<p>Geographic filtering works at the ZIP code, city, state, and "
            "custom radius level. You can combine geography with taxonomy codes "
            "to build highly specific lists: every ophthalmologist within 30 "
            "miles of Denver, every psychiatrist in the five boroughs of New "
            "York City, or every family medicine physician in rural counties "
            "across three Southern states. This kind of granular targeting is "
            "what makes the difference between a campaign that generates "
            "qualified responses and one that generates unsubscribes.</p>"
        ),
        "provyx_pricing": (
            "<h3>Pricing</h3>"
            "<p>Provyx uses a pay-per-record model. You buy the records you "
            "need, when you need them. There's no annual contract, no "
            "auto-renewal, and no 60-day cancellation notice. If you need "
            "500 records for a regional campaign, you pay for 500 records. "
            "If you need 50,000 records for a national launch, the per-record "
            "price drops with volume, but you're still only paying for what "
            "you actually use.</p>"
            "<p>There are no seat-based licenses. Your entire team can access "
            "the records you've purchased. Data is delivered as a CSV file, "
            "through an API, or pushed directly into your CRM. You own the "
            "records once you've bought them, and there's no recurring "
            "platform fee to keep using them.</p>"
            "<p>This model works especially well for organizations that have "
            "seasonal or campaign-based outreach patterns. Medical device "
            "companies launching into a new territory, staffing firms filling "
            "travel nurse positions, or health-tech startups running their "
            "first outbound campaign can all get started without committing "
            "to a five-figure annual contract.</p>"
            "<p>To put it in concrete terms: a medical device company that "
            "needs to reach 1,500 orthopedic surgeons in the Midwest for a "
            "product launch can buy exactly those 1,500 records. With ZoomInfo, "
            "that same company would pay $14,995 minimum for annual platform "
            "access that includes millions of records they'll never look at. "
            "The math doesn't require a spreadsheet to figure out.</p>"
            "<p>Provyx doesn't pretend to be the right choice for everyone. "
            "If you need intent data, website visitor tracking, or org charts "
            "for non-healthcare companies, you'll need a different tool. But for "
            "the specific job of sourcing accurate healthcare provider business "
            "data at a predictable cost, the pay-per-record model eliminates the "
            "overhead and risk that come with enterprise platform contracts.</p>"
        ),

        # -- Who Should Choose What (3 scenarios) --
        "scenario_general_b2b": (
            "<strong>If you need general B2B data across multiple industries:</strong> "
            "ZoomInfo is the stronger choice. If your sales team prospects into "
            "healthcare, technology, financial services, and manufacturing in the "
            "same quarter, a single horizontal platform will save you from managing "
            "multiple vendor relationships. ZoomInfo's breadth is a genuine asset "
            "when your total addressable market crosses industry boundaries. Just "
            "budget accordingly, as you'll likely spend $15,000 to $60,000 or more "
            "per year depending on your team size and feature requirements. Make "
            "sure your team has the bandwidth to learn the platform thoroughly. "
            "ZoomInfo delivers more value when reps understand its filtering, "
            "intent signals, and workflow tools rather than using it as a simple "
            "contact lookup."
        ),
        "scenario_healthcare_specific": (
            "<strong>If you need healthcare-specific provider contact intelligence:</strong> "
            "Provyx is built for this exact use case. You'll get NPI-verified records, "
            "taxonomy code filtering, practice-level location data, and pricing "
            "that doesn't require you to pay for 50 industries you don't sell into. "
            "If every dollar in your pipeline comes from healthcare organizations "
            "or individual providers, a specialized platform will deliver higher "
            "match rates, lower bounce rates, and a significantly lower cost per "
            "qualified record. The onboarding is also simpler because there's no "
            "complex platform to learn. You tell Provyx what kind of providers "
            "you need, and you get a deliverable dataset back."
        ),
        "scenario_enterprise_budget": (
            "<strong>If you have a large enterprise budget and need both:</strong> "
            "Some organizations use ZoomInfo for broad prospecting and supplement "
            "it with Provyx for healthcare-specific campaigns. This makes sense "
            "if you have a dedicated healthcare vertical team alongside teams that "
            "sell into other industries. The combined cost is still often lower than "
            "upgrading to ZoomInfo's highest tier and trying to force it to do "
            "healthcare-specific filtering it wasn't designed for. Evaluate your "
            "actual usage patterns before assuming one tool can serve every team. "
            "If you go this route, establish clear ownership: one team manages "
            "ZoomInfo for general prospecting, and the healthcare team manages "
            "Provyx for provider-specific campaigns. Shared tools with unclear "
            "ownership tend to be underused by everyone."
        ),

        # -- FAQs (5, each answer 60-100 words) --
        "faqs": [
            {
                "question": "Is ZoomInfo worth the cost for healthcare sales teams?",
                "answer": (
                    "It depends on your market scope. If healthcare is one of "
                    "several industries you sell into, ZoomInfo's breadth can justify "
                    "the cost. If healthcare is your only market, you're paying "
                    "$15,000 or more per year for a database where most of the records "
                    "are irrelevant to you, and the healthcare records lack NPI "
                    "verification and taxonomy code filtering. The per-qualified-lead "
                    "cost tends to be significantly higher than with a healthcare-"
                    "specific platform."
                ),
            },
            {
                "question": "Does ZoomInfo have NPI numbers in its database?",
                "answer": (
                    "ZoomInfo does not include NPI numbers as a standard data "
                    "field, and it does not verify its healthcare contacts against "
                    "the CMS NPI Registry. You can filter healthcare contacts by "
                    "industry codes and job titles, but you can't confirm whether a "
                    "contact is an active, licensed provider using ZoomInfo's "
                    "data alone. If NPI verification matters to your workflow, "
                    "you'll need a supplemental data source or a healthcare-"
                    "focused provider like Provyx."
                ),
            },
            {
                "question": "Can I cancel my ZoomInfo contract early?",
                "answer": (
                    "ZoomInfo contracts are annual with automatic renewal. To "
                    "cancel, you typically need to provide written notice at least "
                    "60 days before your renewal date. If you miss that window, "
                    "you're locked in for another full year. Multiple user reviews "
                    "mention this as a pain point, especially when paired with "
                    "reported annual price increases of 10% to 30%. Read your "
                    "specific contract terms carefully before signing."
                ),
            },
            {
                "question": "How accurate is ZoomInfo's data for physicians and medical practices?",
                "answer": (
                    "ZoomInfo's general data accuracy is well-regarded; the "
                    "platform carries a roughly 4.4 out of 5 rating on G2. However, "
                    "healthcare users frequently report higher bounce rates on "
                    "provider emails and outdated practice addresses. Physicians "
                    "change practice locations more often than corporate executives "
                    "change jobs, and ZoomInfo's refresh cycle doesn't always "
                    "keep pace with that churn. For individual provider outreach, "
                    "NPI-verified data sources tend to deliver better results."
                ),
            },
            {
                "question": "What's the biggest difference between Provyx and ZoomInfo?",
                "answer": (
                    "Scope and specialization. ZoomInfo is a horizontal B2B data "
                    "platform covering 50-plus industries with broad contact and "
                    "company intelligence. Provyx is a vertical platform built "
                    "exclusively for healthcare provider business data. Provyx "
                    "verifies every record against the NPI Registry, supports "
                    "taxonomy code filtering, and maps providers to practice "
                    "locations. ZoomInfo offers none of those healthcare-specific "
                    "capabilities but provides far more data outside of healthcare."
                ),
            },
        ],

        # -- Related links --
        "related_links": [
            {"url": "/comparisons/provyx-vs-definitive-healthcare/", "text": "Provyx vs. Definitive Healthcare"},
            {"url": "/comparisons/provyx-vs-apollo/", "text": "Provyx vs. Apollo.io"},
            {"url": "/healthcare-provider-data/", "text": "Healthcare Provider Data Overview"},
            {"url": "/pricing/", "text": "Provyx Pricing"},
        ],
    },

    # ======================================================================
    # 2. Provyx vs. Definitive Healthcare
    # ======================================================================
    {
        "slug": "provyx-vs-definitive-healthcare",
        "competitor_name": "Definitive Healthcare",
        "page_title": "Provyx vs. Definitive Healthcare: Provider Data Platforms Compared",
        "meta_description": (
            "Side-by-side comparison of Provyx and Definitive Healthcare for "
            "healthcare provider business data. Pricing, NPI coverage, data "
            "depth, and contract terms analyzed in detail."
        ),
        "hero_headline": "Provyx vs. Definitive Healthcare",
        "hero_subheadline": (
            "Definitive Healthcare is the market leader in healthcare commercial "
            "intelligence. Provyx is a leaner alternative built for teams that "
            "need provider contact data without a six-figure platform commitment."
        ),

        # -- Intro paragraph (~200 words) --
        "intro": (
            "<p>Definitive Healthcare is the name that comes up most often when "
            "enterprise healthcare companies talk about commercial intelligence. "
            "It's a deep, well-established platform with data on hospitals, "
            "health systems, physician groups, and clinical affiliations. If "
            "you've been in healthcare sales or marketing for more than a few "
            "years, you've probably seen its reports or used its data.</p>"
            "<p>This comparison is for teams that are evaluating Definitive "
            "Healthcare and wondering whether they need the full platform or "
            "whether a more targeted provider data solution would serve them "
            "better. That's a legitimate question, especially for mid-market "
            "companies, startups, and teams whose primary need is provider "
            "contact intelligence rather than hospital-level analytics.</p>"
            "<p>We'll cover pricing, contract structures, data scope, and the "
            "practical differences in how each platform handles individual "
            "provider records. We'll also acknowledge where Definitive Healthcare "
            "has clear advantages, because there are real use cases where its "
            "depth and breadth are difficult to match. The goal is to help you "
            "figure out which platform fits your actual workflow, not to sell "
            "you on one over the other.</p>"
            "<p>A quick caveat: Provyx does not compete with Definitive Healthcare "
            "across the board. If you need claims analytics, procedure volume "
            "estimates, or hospital referral network mapping, Definitive Healthcare "
            "does things Provyx simply does not do. This comparison focuses on the "
            "overlap: provider contact intelligence for sales and marketing teams. "
            "For that specific use case, the platforms diverge significantly in "
            "price, complexity, and approach.</p>"
        ),

        # -- Quick Comparison Table (8 rows) --
        "comparison_table_rows": [
            ("Starting Price", "$25,000-$100,000+/year (enterprise pricing)", "Pay-per-record; no annual minimum"),
            ("Contract Terms", "Annual contracts with auto-renewal and 5% annual uplifts", "Month-to-month or per-project; cancel anytime"),
            ("Healthcare Focus", "100% healthcare; strong on hospitals and health systems", "100% healthcare; strong on individual providers"),
            ("NPI Verification", "Available for many records", "Every record matched against the NPI Registry"),
            ("Taxonomy Filtering", "Available within the platform", "Filter by 800+ NUCC taxonomy codes on export"),
            ("Data Delivery", "Platform access; Salesforce integration is a $22,000+ add-on", "CSV, API, or direct CRM push included"),
            ("Best For", "Enterprise teams analyzing hospital systems and referral networks", "Sales and marketing teams building provider outreach lists"),
            ("Key Risk", "High cost and steep learning curve for smaller teams", "Less depth on hospital-system-level analytics"),
        ],

        # -- Deep Dive: Competitor (800-1,200 words) --
        "competitor_what_they_offer": (
            "<h3>What Definitive Healthcare Offers</h3>"
            "<p><a href=\"https://www.definitivehc.com/\" target=\"_blank\" "
            "rel=\"noopener\">Definitive Healthcare</a> is a healthcare commercial "
            "intelligence company that provides data, analytics, and insights on "
            "the entire healthcare ecosystem. Its platform covers hospitals, "
            "physician groups, ambulatory surgery centers, imaging centers, long-term "
            "care facilities, health systems, and individual providers. The company "
            "went public in 2021 and has since expanded its product suite through "
            "a series of acquisitions.</p>"
            "<p>The platform is significantly more than a contact database. It "
            "includes claims-based analytics, referral network mapping, patient "
            "volume estimates, technology installation data, and competitive "
            "intelligence on which vendors hospitals are already using. For "
            "enterprise pharmaceutical companies, medical device manufacturers "
            "with national sales forces, and healthcare IT companies selling to "
            "health systems, this breadth of intelligence is genuinely valuable.</p>"
            "<p>Definitive Healthcare's data on hospitals and health systems is "
            "particularly strong. You can identify which facilities perform specific "
            "procedures, estimate their patient volumes for particular conditions, "
            "and map the physician referral relationships that drive volume to "
            "those facilities. This kind of analysis supports strategic territory "
            "planning, key account identification, and market sizing in ways "
            "that a simple contact list cannot.</p>"
            "<p>The platform also includes data on healthcare executives, "
            "clinical leadership, and administrative contacts at institutional "
            "organizations. For selling to C-suite hospital administrators or "
            "department heads at large health systems, Definitive Healthcare "
            "provides organizational context that helps reps understand reporting "
            "structures and decision-making hierarchies.</p>"
            "<p>Definitive Healthcare organizes its product into multiple modules. "
            "HospitalView covers acute care facilities. PhysicianView covers "
            "individual provider records. ClaimsMx provides claims-based analytics. "
            "Other modules cover long-term care, ambulatory surgery centers, imaging "
            "centers, and more. Most contracts involve access to specific modules "
            "rather than the entire platform, which means the data you can access "
            "depends on which modules your organization has purchased. This modular "
            "structure gives you flexibility to buy only what you need, but it also "
            "means that quoting a single price for \"Definitive Healthcare\" is "
            "misleading. Two companies can both be customers and have access to "
            "completely different datasets.</p>"
            "<p>The company has also invested heavily in AI-driven analytics and "
            "predictive modeling. These features help enterprise teams identify "
            "which hospitals are most likely to adopt a new technology, predict "
            "patient volume trends, and model the impact of market shifts on "
            "specific facility types. For strategic planning at pharmaceutical "
            "and medical device companies with nine-figure revenue, these tools "
            "are genuinely differentiated. For a 20-person health-tech company "
            "that needs contact data for its first 500 outbound emails, they're "
            "academic.</p>"
        ),
        "competitor_pricing": (
            "<h3>Pricing and Contracts</h3>"
            "<p>Definitive Healthcare does not publish pricing on its website. "
            "Based on publicly available information from user reviews, industry "
            "reports, and procurement databases, annual contracts typically range "
            "from $25,000 for a limited single-module license to well over "
            "$100,000 for multi-module enterprise access. Organizations with "
            "large sales teams or multiple departments accessing the platform "
            "can spend $200,000 or more annually.</p>"
            "<p>Contracts are annual with auto-renewal clauses. Users report "
            "built-in annual price increases of approximately 5%, which are "
            "written into the contract terms at signing. If you sign at "
            "$50,000 in year one, you should expect to pay $52,500 in year "
            "two and $55,125 in year three without any expansion in usage.</p>"
            "<p>One cost that catches teams off guard is the Salesforce "
            "integration add-on. Pushing Definitive Healthcare data directly "
            "into Salesforce, which is how most sales organizations actually "
            "want to use the data, requires a separate module that has been "
            "reported at $22,000 or more per year. That means the \"real\" "
            "starting price for a sales team that lives in Salesforce is "
            "closer to $47,000 than $25,000.</p>"
            "<p>The platform's depth also creates a learning curve cost that "
            "doesn't show up on the invoice. Definitive Healthcare is a "
            "powerful analytics tool, and getting full value from it requires "
            "training, onboarding, and often a dedicated analyst or operations "
            "person to build and maintain the queries and exports your team "
            "needs. For a 10-person startup or a lean marketing team at a "
            "mid-market company, that operational overhead can be substantial.</p>"
        ),
        "competitor_shortcomings": (
            "<h3>Where Definitive Healthcare Falls Short for Provider Outreach</h3>"
            "<p>Definitive Healthcare is excellent at what it was built for: "
            "institutional healthcare analytics. The gaps appear when you try "
            "to use it primarily as a provider contact intelligence tool for "
            "outbound sales and marketing.</p>"
            "<p><strong>Individual provider data is not the primary focus.</strong> "
            "The platform's strength is hospital and health system data. Individual "
            "physician records exist, but they're often tied to organizational "
            "affiliations rather than mapped independently to practice locations. "
            "If you need to reach a specific orthopedic surgeon at their outpatient "
            "clinic rather than their hospital system's corporate office, Definitive "
            "Healthcare's data model sometimes makes that harder than it should be. "
            "According to the <a href=\"https://www.bls.gov/ooh/healthcare/\" "
            "target=\"_blank\" rel=\"noopener\">Bureau of Labor Statistics</a>, "
            "healthcare employs over 16 million people in the U.S., and the "
            "majority of those providers work in settings smaller than a hospital "
            "system.</p>"
            "<p><strong>Pricing excludes smaller teams.</strong> A $25,000 to "
            "$100,000 annual commitment, plus integration costs, plus analyst time, "
            "means Definitive Healthcare is practically inaccessible to companies "
            "with annual marketing budgets under $200,000. That rules out most "
            "healthcare startups, many regional medical device distributors, and "
            "a large number of staffing firms and consulting practices that sell "
            "into healthcare every day.</p>"
            "<p><strong>Getting data out of the platform is friction-heavy.</strong> "
            "Definitive Healthcare is designed to be used inside its own interface. "
            "Exporting data for use in your CRM, marketing automation tool, or "
            "custom analytics pipeline often requires the paid Salesforce connector "
            "or manual CSV exports with record limits. If your workflow is "
            "\"give me a clean list of 2,000 providers meeting these criteria "
            "and let me load it into HubSpot,\" Definitive Healthcare adds steps "
            "that a simpler data delivery model eliminates.</p>"
            "<p><strong>Steep learning curve absorbs productive hours.</strong> "
            "The platform's analytical depth is an asset for data analysts and "
            "market research teams. It's a liability for sales development reps "
            "who need a list by Thursday. Building effective queries in Definitive "
            "Healthcare takes training, and maintaining those queries as your "
            "targeting criteria evolve takes ongoing attention. Teams without "
            "a dedicated operations resource often end up using a fraction of the platform "
            "significantly, which makes the high annual cost even harder to "
            "justify.</p>"
            "<p><strong>Overkill for contact-level outreach.</strong> If your "
            "primary use case is building targeted contact lists for email "
            "campaigns, phone outreach, or direct mail, you're paying for "
            "claims analytics, referral mapping, and market sizing capabilities "
            "you may never use. That's not a criticism of those features; they're "
            "valuable for the right buyer. But for teams whose daily workflow is "
            "\"find providers, get their contact info, reach out,\" the platform's "
            "complexity works against them.</p>"
            "<p><strong>Procurement timelines don't match sales urgency.</strong> "
            "Getting a Definitive Healthcare contract approved at most organizations "
            "involves procurement review, security assessment, budget approval, and "
            "sometimes legal review of the data usage terms. That process can take "
            "weeks or months. If your VP of Sales needs a provider list for a "
            "campaign launching next month, a multi-week procurement cycle for a "
            "six-figure platform isn't going to work. Faster, lighter alternatives "
            "exist for teams that need data on a shorter timeline.</p>"
        ),
        "competitor_outbound_links": [
            ("https://www.definitivehc.com/", "Definitive Healthcare official website"),
            ("https://www.bls.gov/ooh/healthcare/", "Bureau of Labor Statistics: Healthcare Occupations"),
        ],

        # -- Deep Dive: Provyx (500-800 words) --
        "provyx_what_delivers": (
            "<h3>What Provyx Delivers</h3>"
            "<p>Provyx is a healthcare provider business data platform focused on "
            "one thing: getting you accurate, contactable provider records for "
            "outbound sales and marketing. It doesn't try to be a market analytics "
            "platform. It doesn't include claims data or procedure volume estimates. "
            "What it does is give you clean, NPI-verified contact intelligence "
            "for the specific providers you want to reach.</p>"
            "<p>The database covers physicians, nurse practitioners, physician "
            "assistants, dentists, optometrists, chiropractors, physical therapists, "
            "behavioral health providers, and dozens of other licensed clinician "
            "types. Each record includes the provider's NPI number, taxonomy "
            "code, practice address (mapped to the location, not just the "
            "corporate entity), phone number, email address, and organizational "
            "affiliations.</p>"
            "<p>Data is sourced from public NPI registries, business listings, "
            "state licensing boards, and commercial databases. The sourcing "
            "approach prioritizes accuracy for contact-level outreach rather "
            "than breadth of institutional analytics. If you need to know which "
            "hospital has the highest knee replacement volume in a metro area, "
            "Definitive Healthcare is the better tool. If you need the direct "
            "contact details for every orthopedic surgeon in that metro area, "
            "Provyx is built for that.</p>"
            "<p>Provyx also doesn't try to be a market intelligence platform. "
            "That's a deliberate choice, not a gap. Claims analytics, procedure "
            "volume estimates, and predictive market models are valuable tools "
            "for the right buyer. But building those features into a contact "
            "data platform adds cost and complexity that gets passed on to "
            "every customer, including the ones who just need a clean list of "
            "providers to call. Provyx keeps the product focused so the "
            "pricing stays accessible to teams that don't need, and shouldn't "
            "pay for, enterprise analytics.</p>"
            "<p>Speed of deployment is another practical difference. Provyx "
            "doesn't require a multi-week onboarding process, a dedicated "
            "analyst to build queries, or a training program to get your team "
            "productive. You define your target criteria, Provyx delivers the "
            "records, and your team starts outreach. For companies that are "
            "comparing a 6-week Definitive Healthcare implementation timeline "
            "against a same-week Provyx data delivery, the operational "
            "difference matters, especially when pipeline targets don't wait "
            "for procurement to finish.</p>"
        ),
        "provyx_healthcare_handling": (
            "<h3>How Provyx Handles Healthcare Provider Business Data</h3>"
            "<p>The data model is NPI-first. Every record starts with a verified "
            "NPI number, and every attribute on that record, from specialty "
            "designation to practice address, is anchored to that identifier. "
            "This matters because it means you're not relying on job titles or "
            "self-reported profile information to determine whether someone is "
            "a practicing dermatologist or a retired administrator with "
            "\"dermatology\" in their LinkedIn headline.</p>"
            "<p>Taxonomy code filtering gives you clinical specialty precision "
            "that job-title-based filtering simply can't match. The NUCC "
            "taxonomy system includes over 800 codes, and Provyx lets you "
            "filter by any combination of them. You can pull endocrinologists "
            "and internal medicine physicians in the same query, or narrow "
            "down to a single sub-specialty like pediatric hematology-oncology.</p>"
            "<p>Practice-level mapping means you get the address and phone "
            "number for the location where a provider actually sees patients, "
            "not the billing address of their employer's parent company three "
            "states away. For field sales teams, territory managers, and "
            "regional marketers, this distinction directly affects whether "
            "your outreach lands or bounces.</p>"
            "<p>Data delivery is straightforward. You define your criteria, "
            "Provyx builds the list, and you receive it as a CSV, through an "
            "API call, or pushed directly into Salesforce, HubSpot, or another "
            "CRM. There's no module to purchase, no connector fee, and no "
            "export limit to work around. The entire process, from defining "
            "your target audience to having records in your CRM, can happen "
            "in days rather than the weeks or months that enterprise platform "
            "procurement typically requires.</p>"
        ),
        "provyx_pricing": (
            "<h3>Pricing</h3>"
            "<p>Provyx charges per record with volume-based discounts. There's "
            "no annual contract, no auto-renewal with built-in price increases, "
            "and no separate charge for CRM integration. You request the "
            "records you need, pay for those records, and receive them as a "
            "CSV, through an API, or pushed directly into your CRM.</p>"
            "<p>There's no seat-based licensing. Five people on your team can "
            "use the same dataset without five separate platform licenses. "
            "There's no $22,000 add-on to get data into Salesforce. There's "
            "no training certification required to run a query.</p>"
            "<p>For teams that have been quoted $50,000 to $100,000 for "
            "Definitive Healthcare and primarily need provider contact lists "
            "rather than market analytics, the cost difference is substantial. "
            "Many Provyx customers report spending 70% to 90% less than they "
            "were spending on enterprise healthcare data platforms, while "
            "achieving equal or better results on their provider outreach "
            "campaigns specifically.</p>"
            "<p>Consider the total cost of ownership. With Definitive Healthcare, "
            "you're paying the license fee, the Salesforce integration add-on, "
            "the onboarding time, the ongoing training hours, and the analyst "
            "or operations person who maintains your queries. With Provyx, "
            "you're paying for the records. That's it. For a 50-person company "
            "with a 5-person sales team, the difference in total cost of "
            "ownership over three years can easily exceed $150,000.</p>"
        ),

        # -- Who Should Choose What (3 scenarios) --
        "scenario_general_b2b": (
            "<strong>If you need hospital-level analytics, claims data, and market "
            "sizing:</strong> Definitive Healthcare is the stronger platform. If "
            "your team includes market research analysts, strategic planning "
            "leaders, or enterprise sales reps who need to understand referral "
            "networks and procedure volumes before engaging an account, Definitive "
            "Healthcare's depth is worth the investment. Budget at least $50,000 "
            "annually once you include the Salesforce integration, and plan for "
            "a 2-4 week onboarding period to get full value from the platform. "
            "Assign a dedicated analyst or operations resource to own the platform "
            "and build queries for your team, because the ROI depends heavily on "
            "how well the tool is actually used."
        ),
        "scenario_healthcare_specific": (
            "<strong>If you need healthcare provider contact intelligence for "
            "outbound campaigns:</strong> Provyx delivers the specific data you "
            "need at a fraction of the cost. NPI-verified records, taxonomy code "
            "filtering, practice-level addresses, and flexible data delivery "
            "without a multi-month procurement process. If your team's daily "
            "work is building and executing outreach lists, not running market "
            "analytics, Provyx removes the complexity and cost that come with "
            "an enterprise analytics platform. You can go from \"we need a "
            "list\" to \"we're running the campaign\" in days, not months."
        ),
        "scenario_enterprise_budget": (
            "<strong>If you have the budget for both and different teams with "
            "different needs:</strong> Using Definitive Healthcare for strategic "
            "market analysis and Provyx for tactical outreach list building is a "
            "combination that several organizations have adopted. Your market "
            "research team gets the depth they need for territory planning, and "
            "your sales and marketing teams get clean, actionable contact data "
            "without needing to learn a complex analytics platform. The total "
            "cost of this combination is often comparable to a fully loaded "
            "Definitive Healthcare enterprise license. The key is giving each "
            "team the tool that matches their actual workflow rather than forcing "
            "everyone onto a single platform that serves some teams well and "
            "others poorly."
        ),

        # -- FAQs (5, each answer 60-100 words) --
        "faqs": [
            {
                "question": "Is Definitive Healthcare worth the price for small to mid-size companies?",
                "answer": (
                    "For most small to mid-size companies, the answer is no. "
                    "The starting cost of $25,000 per year, plus $22,000 or more "
                    "for Salesforce integration, plus staff time to learn the "
                    "platform, creates a total investment that's difficult to "
                    "justify unless you're using the claims analytics and market "
                    "sizing features regularly. If your primary need is provider "
                    "contact data for outreach, a specialized and less expensive "
                    "tool will deliver better ROI."
                ),
            },
            {
                "question": "Does Definitive Healthcare have individual provider contact information?",
                "answer": (
                    "Yes, Definitive Healthcare includes individual provider "
                    "records with contact information. However, the platform's "
                    "core strength is institutional data: hospitals, health "
                    "systems, and organizational hierarchies. Individual provider "
                    "records are available but are often presented in the context "
                    "of their organizational affiliations rather than as "
                    "standalone practice-level contacts. For teams that primarily "
                    "need individual provider outreach data, the platform's design "
                    "adds unnecessary complexity."
                ),
            },
            {
                "question": "How does Definitive Healthcare's data accuracy compare to Provyx?",
                "answer": (
                    "Both platforms maintain high data accuracy, but for different "
                    "record types. Definitive Healthcare is exceptionally accurate "
                    "for hospital-level data: bed counts, procedure volumes, "
                    "technology installations, and executive contacts. Provyx "
                    "focuses its accuracy on individual provider records: NPI "
                    "verification, practice-level addresses, and direct contact "
                    "details. The right comparison depends on whether you're "
                    "targeting institutions or individual providers."
                ),
            },
            {
                "question": "Can I export data from Definitive Healthcare into my CRM?",
                "answer": (
                    "You can, but it typically requires a paid add-on. The "
                    "Salesforce integration module has been reported at $22,000 "
                    "or more per year. Without it, you're limited to manual CSV "
                    "exports, which often come with record caps per download. "
                    "Provyx includes data delivery via CSV, API, or direct CRM "
                    "push at no additional cost. If getting data into your CRM "
                    "quickly is a priority, factor the integration cost into your "
                    "Definitive Healthcare budget."
                ),
            },
            {
                "question": "What's the main advantage Definitive Healthcare has over Provyx?",
                "answer": (
                    "Depth of institutional analytics. Definitive Healthcare "
                    "offers claims-based insights, referral network mapping, "
                    "procedure volume estimates, and technology installation "
                    "data that Provyx doesn't provide. If you need to understand "
                    "which hospitals perform the most hip replacements in a "
                    "region, or map referral patterns between primary care "
                    "physicians and specialists, Definitive Healthcare is the "
                    "right tool. Provyx focuses on provider contact intelligence, "
                    "not institutional analytics."
                ),
            },
        ],

        # -- Related links --
        "related_links": [
            {"url": "/comparisons/provyx-vs-zoominfo/", "text": "Provyx vs. ZoomInfo"},
            {"url": "/comparisons/provyx-vs-apollo/", "text": "Provyx vs. Apollo.io"},
            {"url": "/healthcare-provider-data/", "text": "Healthcare Provider Data Overview"},
            {"url": "/pricing/", "text": "Provyx Pricing"},
        ],
    },

    # ======================================================================
    # 3. Provyx vs. Apollo.io
    # ======================================================================
    {
        "slug": "provyx-vs-apollo",
        "competitor_name": "Apollo.io",
        "page_title": "Provyx vs. Apollo.io: Healthcare Provider Data Compared",
        "meta_description": (
            "Comparing Provyx and Apollo.io for healthcare provider business data. "
            "Pricing, email accuracy, NPI verification, and bounce rates "
            "evaluated for healthcare sales teams."
        ),
        "hero_headline": "Provyx vs. Apollo.io",
        "hero_subheadline": (
            "Apollo.io is an affordable sales intelligence tool with a generous free "
            "tier. But when you need accurate healthcare provider contact intelligence, "
            "affordability and accuracy are two very different things."
        ),

        # -- Intro paragraph (~200 words) --
        "intro": (
            "<p>Apollo.io has earned a strong reputation as an accessible sales "
            "intelligence platform, particularly among startups, early-stage "
            "companies, and sales teams that need to get outbound campaigns "
            "running quickly without a large budget. Its free tier, reasonable "
            "paid plans, and built-in engagement tools make it a popular first "
            "stop for teams building their prospecting stack.</p>"
            "<p>This comparison is for healthcare sales and marketing teams that "
            "are considering Apollo.io, either as their primary data source or "
            "as a supplement to other tools. We'll look at where Apollo.io "
            "works well, where it falls short for healthcare-specific outreach, "
            "and how it compares to a purpose-built healthcare provider business "
            "data platform like Provyx.</p>"
            "<p>We'll focus on the data itself: accuracy, healthcare coverage, "
            "bounce rates, and the presence (or absence) of healthcare-specific "
            "identifiers like NPI numbers and taxonomy codes. We'll also cover "
            "pricing, because Apollo.io's cost structure is one of its biggest "
            "advantages in general, even though cost-per-usable-record tells a "
            "different story when you're targeting healthcare providers. All "
            "claims about both platforms are based on publicly available "
            "information, user reviews, and documented product capabilities.</p>"
            "<p>If you're evaluating Apollo.io specifically because of budget "
            "constraints, that's understandable. Healthcare startups and early-stage "
            "companies don't always have $15,000 to $100,000 for a data platform. "
            "The question isn't whether Apollo.io is cheap enough. It's whether "
            "the data quality for healthcare providers is high enough to justify "
            "even the lower price, once you factor in bounce rates, wasted credits, "
            "and the time your team spends cleaning records that should have been "
            "accurate from the start.</p>"
        ),

        # -- Quick Comparison Table (8 rows) --
        "comparison_table_rows": [
            ("Starting Price", "Free tier available; paid plans $49-$119/month per user", "Pay-per-record; no monthly subscription required"),
            ("Contract Terms", "Monthly or annual billing; credit-based system with caps", "Month-to-month or per-project; no credit caps"),
            ("Healthcare Focus", "General sales intelligence; no healthcare specialization", "100% healthcare provider focus"),
            ("NPI Verification", "Not available", "Every record matched against the NPI Registry"),
            ("Taxonomy Filtering", "Not available", "Filter by 800+ NUCC taxonomy codes"),
            ("Data Delivery", "Platform access with built-in email sequencing", "CSV, API, or direct CRM push"),
            ("Best For", "Tech/SaaS sales teams with multi-industry outreach", "Teams selling exclusively into healthcare providers"),
            ("Key Risk", "20-35% email bounce rates reported for healthcare contacts", "Not suitable for non-healthcare prospecting"),
        ],

        # -- Deep Dive: Competitor (800-1,200 words) --
        "competitor_what_they_offer": (
            "<h3>What Apollo.io Offers</h3>"
            "<p><a href=\"https://www.apollo.io/\" target=\"_blank\" rel=\"noopener\">"
            "Apollo.io</a> is a sales intelligence and engagement platform that "
            "combines a B2B contact database with email sequencing, calling, "
            "and task management tools. Its database includes over 270 million "
            "contact records according to the company, spanning industries from "
            "technology and financial services to retail and, yes, healthcare.</p>"
            "<p>The platform's appeal starts with its pricing. Apollo.io offers "
            "a free tier that gives you limited access to the contact database "
            "and basic sequencing tools. Paid plans start at $49 per user per "
            "month for the Basic plan (billed annually) and go up to $119 per "
            "user per month for the Organization plan. Compared to enterprise "
            "sales intelligence platforms that start at five figures annually, "
            "Apollo.io is dramatically more accessible.</p>"
            "<p>Beyond the database, Apollo.io includes a built-in email "
            "sequencing engine, a dialer, LinkedIn integration, and lead "
            "scoring. You can build a prospecting workflow entirely within the "
            "platform: find contacts, enroll them in an email sequence, track "
            "opens and replies, and manage follow-up tasks. For sales teams "
            "that want a single tool for data and outreach, that integration "
            "is a real productivity advantage.</p>"
            "<p>Apollo.io also provides intent data, job change alerts, and "
            "technographic information. These features help prioritize which "
            "accounts to target and when to reach out. For tech and SaaS sales "
            "teams, these signals are genuinely useful for timing outreach "
            "around buying triggers.</p>"
            "<p>The platform has grown rapidly and has a loyal user base, "
            "particularly among startups, SMBs, and growth-stage companies. "
            "Its combination of affordability, ease of use, and all-in-one "
            "functionality makes it a strong choice for teams that need to "
            "move fast across a broad addressable market.</p>"
            "<p>Apollo.io's data is gathered through a mix of web scraping, "
            "public data aggregation, user-contributed information, and email "
            "pattern inference. The email pattern inference is particularly "
            "relevant to this comparison: Apollo.io identifies a company's "
            "email format (for example, first.last@company.com) and then "
            "generates email addresses for contacts at that company based on "
            "the pattern. This works well for companies with standardized "
            "email systems. It works poorly for medical practices, where "
            "email addresses follow no consistent pattern, are often hosted "
            "through EHR vendors, or route through institutional systems "
            "with non-obvious naming conventions.</p>"
            "<p>It's worth noting that Apollo.io is genuinely good at what "
            "it was designed for. The product-market fit for tech sales "
            "teams, startup founders, and growth marketers is strong. The "
            "platform's usability, pricing, and feature set are well-suited "
            "to high-velocity outbound sales motions in industries where "
            "contacts are digitally active and email addresses are "
            "predictable. The question isn't whether Apollo.io is a good "
            "product. It's whether it's the right product for healthcare "
            "provider outreach specifically.</p>"
        ),
        "competitor_pricing": (
            "<h3>Pricing and Credits</h3>"
            "<p>Apollo.io's pricing is credit-based. Each plan comes with a "
            "monthly allotment of credits that you spend when you unlock "
            "contact details (email addresses, phone numbers). The free plan "
            "includes a small number of credits per month. The Basic plan at "
            "$49 per user per month provides more credits and additional "
            "features. The Professional plan at $79 per user per month and "
            "the Organization plan at $119 per user per month increase both "
            "credit allotments and feature access.</p>"
            "<p>On the surface, this looks very affordable, and for many use "
            "cases it is. A single sales rep running outbound into the tech "
            "sector can get meaningful results for under $100 per month. But "
            "the credit system introduces constraints that become visible at "
            "scale. Credits are consumed per contact unlock, and once you hit "
            "your monthly cap, you either wait for the next cycle or pay for "
            "additional credits at a premium rate.</p>"
            "<p>For healthcare-specific outreach, the effective cost per "
            "usable contact is where the math changes. If you're unlocking "
            "100 healthcare provider contacts on Apollo.io and 25 to 35 of "
            "those emails bounce (a range that healthcare users commonly "
            "report), you've spent credits on records that delivered zero "
            "value. Your actual cost per deliverable contact is 30% to 50% "
            "higher than the sticker price suggests.</p>"
            "<p>Annual billing offers a discount, but you're then committing "
            "to 12 months of a platform that may or may not deliver adequate "
            "results for your specific vertical. Monthly billing keeps your "
            "flexibility, but at a higher per-month rate.</p>"
        ),
        "competitor_shortcomings": (
            "<h3>Where Apollo.io Falls Short for Healthcare</h3>"
            "<p>Apollo.io is a good product for the market it was designed to "
            "serve. Healthcare provider outreach is not that market. The gaps "
            "are structural, not incidental, and they affect the metrics that "
            "matter most to healthcare sales teams.</p>"
            "<p><strong>Email bounce rates in healthcare are significantly "
            "higher.</strong> This is the biggest practical problem. Healthcare "
            "providers, particularly physicians in private practice, don't use "
            "their email addresses the same way tech workers do. Many "
            "physicians use institutional email systems that don't follow "
            "standard first.last@domain patterns. Others use personal email "
            "for professional communication, and those addresses change "
            "unpredictably. Apollo.io users targeting healthcare contacts "
            "routinely report bounce rates of 20% to 35%, compared to the "
            "5% to 10% they see when targeting technology companies. At a "
            "25% bounce rate, one in four credits you spend returns nothing.</p>"
            "<p><strong>No NPI data whatsoever.</strong> Apollo.io does not "
            "include NPI numbers in its records, and it does not verify "
            "contacts against the <a href=\"https://npiregistry.cms.hhs.gov/\" "
            "target=\"_blank\" rel=\"noopener\">CMS NPI Registry</a>. This "
            "means you can't confirm that a contact is an active, licensed "
            "healthcare provider. You can't filter by provider type, and "
            "you can't cross-reference records with the taxonomy codes that "
            "define clinical specialties. You're relying entirely on job "
            "titles and company industry tags, which are inconsistent and "
            "often wrong for healthcare contacts.</p>"
            "<p><strong>No taxonomy code filtering.</strong> Without taxonomy "
            "codes, you can't target providers by clinical specialty with any "
            "precision. Searching for \"cardiologist\" as a job title will "
            "miss interventional cardiologists who list themselves as "
            "\"interventional specialist\" and will include cardiac "
            "rehabilitation coordinators who aren't physicians at all. The "
            "NUCC taxonomy system exists precisely to solve this problem, and "
            "Apollo.io doesn't use it.</p>"
            "<p><strong>No practice-level intelligence.</strong> Apollo.io's "
            "company data is oriented around corporate entities. A physician "
            "who practices at a hospital might be listed under the hospital "
            "system's corporate record, with the system's main switchboard "
            "number and headquarters address. That's not useful for field "
            "sales reps who need to show up at the right office, or for "
            "direct mail campaigns that need the actual clinic address.</p>"
            "<p><strong>Engagement tools don't compensate for bad data.</strong> "
            "Apollo.io's built-in sequencing, calling, and LinkedIn tools are "
            "genuinely useful. But they amplify whatever data you feed them. "
            "If 30% of your contact list has invalid email addresses, your "
            "email sequence will damage your sender reputation, trigger spam "
            "filters, and generate vanity metrics (\"we sent 10,000 emails\") "
            "that mask the reality of poor deliverability. Good outreach "
            "tools need good data to work with, and for healthcare, "
            "Apollo.io's data frequently isn't good enough.</p>"
            "<p><strong>Built for velocity, not precision.</strong> Apollo.io's "
            "design philosophy is built around high-volume, multi-channel "
            "outreach. That's perfect for a SaaS company running sequences "
            "to 10,000 software engineering managers. It's a poor fit for "
            "a medical device company that needs to reach 200 specific "
            "interventional cardiologists in the Southeast. Healthcare "
            "provider outreach is a precision game, and Apollo.io is a "
            "volume tool.</p>"
            "<p><strong>Sender reputation damage is a real downstream cost.</strong> "
            "When you send emails to a list with a 25% to 35% bounce rate, "
            "email service providers notice. High bounce rates degrade your "
            "domain's sender reputation, which means your emails to valid "
            "contacts also start landing in spam folders. This creates a "
            "compounding problem: bad data today doesn't just waste today's "
            "outreach effort, it makes tomorrow's outreach less effective too. "
            "For healthcare sales teams running multi-touch campaigns over weeks "
            "or months, protecting sender reputation is critical. Starting with "
            "verified data is the most effective way to do that.</p>"
            "<p><strong>No way to distinguish provider types.</strong> Without "
            "NPI data and taxonomy codes, Apollo.io can't tell you whether a "
            "contact is a physician, a nurse practitioner, a physician assistant, "
            "or a non-clinical administrator with a healthcare job title. If "
            "your product or service is specifically for physicians, you might "
            "be spending credits on contacts who are office managers, billing "
            "coordinators, or clinical research assistants. The title \"healthcare "
            "professional\" in Apollo.io's database could mean almost anyone who "
            "works in a building that provides medical services.</p>"
        ),
        "competitor_outbound_links": [
            ("https://www.apollo.io/", "Apollo.io official website"),
            ("https://npiregistry.cms.hhs.gov/", "CMS NPI Registry"),
        ],

        # -- Deep Dive: Provyx (500-800 words) --
        "provyx_what_delivers": (
            "<h3>What Provyx Delivers</h3>"
            "<p>Provyx is a healthcare provider business data platform. Its "
            "database contains only healthcare providers: physicians, nurse "
            "practitioners, physician assistants, dentists, optometrists, "
            "chiropractors, physical therapists, behavioral health professionals, "
            "and other licensed clinicians. Every record is verified against the "
            "National Provider Identifier Registry, and every record includes "
            "taxonomy codes, practice addresses, and direct contact information.</p>"
            "<p>Provyx doesn't include a built-in email sequencer, a dialer, "
            "or LinkedIn integration. It's a data platform, not an engagement "
            "platform. The trade-off is intentional: instead of building mediocre "
            "versions of tools you probably already have (HubSpot, Outreach, "
            "Salesloft, your CRM's built-in email), Provyx focuses on making "
            "the data itself as accurate and targeted as possible, then delivers "
            "it in the format your existing tools need.</p>"
            "<p>Data is sourced from public NPI registries, business listings, "
            "state licensing boards, and commercial databases. The sourcing "
            "methodology avoids reliance on email pattern guessing or "
            "user-contributed data from browser extensions, which are the "
            "primary sources of the inaccurate healthcare emails that plague "
            "general-purpose platforms.</p>"
            "<p>Where Provyx falls short compared to Apollo.io is in engagement "
            "tooling. If you want a single platform where you can find contacts, "
            "build email sequences, make calls, and track engagement, Provyx "
            "isn't that. You'll need to pair Provyx with your existing outreach "
            "tools. For most healthcare sales teams, that's already how they "
            "work: the CRM and engagement platform are separate from the data "
            "source. But if you're a solo founder or early-stage team looking "
            "for an all-in-one solution, that's a legitimate trade-off to "
            "consider.</p>"
        ),
        "provyx_healthcare_handling": (
            "<h3>How Provyx Handles Healthcare Provider Business Data</h3>"
            "<p>NPI verification is the foundation. Every record in the Provyx "
            "database is matched against the CMS NPI Registry, confirming that "
            "the provider is a real, identifiable healthcare professional with "
            "an active national identifier. This eliminates the \"is this person "
            "actually a doctor?\" problem that plagues outreach lists built from "
            "general databases.</p>"
            "<p>Taxonomy code filtering lets you build lists with clinical "
            "specialty precision. Need every gastroenterologist within 100 miles "
            "of Nashville? Every psychiatric nurse practitioner in California? "
            "Every oral surgeon in the Chicago metro? Taxonomy codes make these "
            "queries straightforward and accurate, because the specialty "
            "designation comes from the provider's NPI registration, not from "
            "a job title field that might say \"specialist\" or \"doctor\" "
            "or \"healthcare professional.\"</p>"
            "<p>Practice-level addressing means your outreach arrives at the "
            "right location. Provyx maps providers to the specific offices, "
            "clinics, and facilities where they practice, with separate contact "
            "details for each location. A physician who works at two hospitals "
            "and a private clinic appears with all three practice locations, "
            "so your field rep or direct mail piece goes to the right place.</p>"
            "<p>Email addresses in the Provyx database are sourced and verified "
            "through methods designed for healthcare's unique email landscape. "
            "The result is measurably lower bounce rates compared to general "
            "platforms: Provyx users typically see bounce rates under 8% for "
            "healthcare provider campaigns, compared to the 20% to 35% range "
            "that Apollo.io users report for the same audience.</p>"
        ),
        "provyx_pricing": (
            "<h3>Pricing</h3>"
            "<p>Provyx uses a pay-per-record model with no monthly subscription, "
            "no credit caps, and no per-seat licensing. You buy the records you "
            "need, receive them in your preferred format (CSV, API, or CRM "
            "push), and use them however you want with your entire team.</p>"
            "<p>There's no free tier, and we won't pretend that \"free\" is "
            "the right comparison point. Apollo.io's free plan gives you limited "
            "credits and limited data. Provyx's model gives you verified, "
            "NPI-matched healthcare provider records at a known cost per record, "
            "with volume discounts for larger orders. You're comparing a small "
            "amount of general data for free versus a specific amount of "
            "verified healthcare data for a transparent price.</p>"
            "<p>When you factor in bounce rates, the cost comparison shifts "
            "further. If you're paying $79 per month on Apollo.io and 30% of "
            "your healthcare emails bounce, your effective cost per deliverable "
            "contact is significantly higher than the nominal credit cost. "
            "Provyx's per-record price reflects records that have been verified "
            "and are deliverable, so the sticker price and the effective price "
            "are much closer together.</p>"
        ),

        # -- Who Should Choose What (3 scenarios) --
        "scenario_general_b2b": (
            "<strong>If you need general B2B data for multi-industry outreach:</strong> "
            "Apollo.io is a strong and affordable option. If you're prospecting into "
            "technology, SaaS, e-commerce, financial services, or any industry where "
            "email patterns are predictable and contacts actively maintain their "
            "professional profiles, Apollo.io's combination of data and engagement "
            "tools delivers good value at a fraction of enterprise pricing. It's "
            "particularly well-suited for startups and growth-stage companies running "
            "high-volume outbound across non-regulated industries. The built-in "
            "engagement tools add genuine value for teams that don't already have "
            "a separate outreach platform."
        ),
        "scenario_healthcare_specific": (
            "<strong>If you need healthcare provider contact intelligence:</strong> "
            "Provyx is the right tool. You'll get NPI-verified records with taxonomy "
            "code filtering, practice-level addresses, and email addresses sourced "
            "through methods designed for healthcare's unique contact landscape. Your "
            "bounce rates will be dramatically lower, your targeting will be more "
            "precise, and every record in your list will be a confirmed healthcare "
            "provider rather than a best-guess match based on job titles and "
            "industry tags."
        ),
        "scenario_enterprise_budget": (
            "<strong>If you're cost-sensitive and need to cover both healthcare and "
            "other industries:</strong> Using Apollo.io for your non-healthcare "
            "outreach and Provyx for your healthcare provider campaigns is a "
            "practical combination. Apollo.io's monthly pricing keeps your "
            "non-healthcare prospecting affordable, and Provyx's pay-per-record "
            "model means you're only paying for verified healthcare data when "
            "you need it. The combined cost for both tools is typically less "
            "than a single ZoomInfo license, and you'll get better results "
            "for healthcare specifically."
        ),

        # -- FAQs (5, each answer 60-100 words) --
        "faqs": [
            {
                "question": "Can I use Apollo.io for healthcare sales outreach?",
                "answer": (
                    "You can, but the results will likely be poor compared to "
                    "other industries. Apollo.io users targeting healthcare "
                    "providers commonly report email bounce rates of 20% to 35%, "
                    "which is two to four times higher than what they see when "
                    "targeting technology or SaaS contacts. The platform lacks NPI "
                    "data and taxonomy codes, so you can't verify that contacts "
                    "are active providers or filter by clinical specialty. For "
                    "occasional healthcare outreach, it might suffice. For "
                    "dedicated healthcare sales, it won't."
                ),
            },
            {
                "question": "Why are healthcare email bounce rates so high on Apollo.io?",
                "answer": (
                    "Healthcare providers don't maintain professional email "
                    "addresses the same way tech workers do. Many use institutional "
                    "email systems with non-standard formats. Others use EHR-linked "
                    "messaging and rarely check external email. Apollo.io infers "
                    "email addresses using pattern matching (first.last@domain), "
                    "which works well for companies with consistent email formats "
                    "but fails frequently for medical practices, hospitals, and "
                    "clinics. Provyx sources healthcare email addresses through "
                    "methods designed for this specific challenge."
                ),
            },
            {
                "question": "Is Apollo.io's free plan enough for healthcare prospecting?",
                "answer": (
                    "The free plan gives you limited credits to unlock contacts "
                    "each month. For healthcare prospecting, the credit limitation "
                    "is less of an issue than the data quality. Even with unlimited "
                    "free credits, you'd still face the same problems: no NPI "
                    "verification, no taxonomy filtering, high bounce rates, and "
                    "no practice-level addressing. The free tier is a reasonable "
                    "way to test Apollo.io for non-healthcare outreach, but it "
                    "won't give you an accurate picture of healthcare results."
                ),
            },
            {
                "question": "Does Provyx have engagement tools like Apollo.io's email sequencer?",
                "answer": (
                    "No. Provyx is a data platform, not an engagement platform. "
                    "It doesn't include email sequencing, a dialer, or LinkedIn "
                    "outreach tools. Provyx delivers verified provider records "
                    "into the tools you already use: HubSpot, Outreach, Salesloft, "
                    "Salesforce, or any other CRM and engagement platform. The "
                    "philosophy is that your outreach tools should work with "
                    "the best available data, rather than relying on a single "
                    "platform to do both jobs adequately."
                ),
            },
            {
                "question": "What's the real cost difference between Apollo.io and Provyx for healthcare?",
                "answer": (
                    "Apollo.io appears cheaper on paper. A Professional plan at "
                    "$79 per month is far less than most data platforms. But "
                    "when 25% to 35% of your healthcare contacts bounce, your "
                    "cost per usable record rises sharply. Provyx's pay-per-record "
                    "pricing is higher per individual record, but virtually every "
                    "record is NPI-verified and deliverable. When you compare "
                    "cost per qualified, contactable healthcare provider, Provyx "
                    "is typically equal to or less expensive than Apollo.io."
                ),
            },
        ],

        # -- Related links --
        "related_links": [
            {"url": "/comparisons/provyx-vs-zoominfo/", "text": "Provyx vs. ZoomInfo"},
            {"url": "/comparisons/provyx-vs-definitive-healthcare/", "text": "Provyx vs. Definitive Healthcare"},
            {"url": "/healthcare-provider-data/", "text": "Healthcare Provider Data Overview"},
            {"url": "/pricing/", "text": "Provyx Pricing"},
        ],
    },
]

# Alternative pages
ALTERNATIVES = [
    # ===================================================================
    # 1. ZoomInfo Alternative
    # ===================================================================
    {
        "slug": "zoominfo-alternative",
        "competitor": "ZoomInfo",
        "competitor_url": "https://www.zoominfo.com/",
        "title": "Best ZoomInfo Alternative for Healthcare Data | Provyx",
        "meta_description": (
            "Provyx is a ZoomInfo alternative built for healthcare. "
            "Get NPI-verified provider contact intelligence with pay-per-record "
            "pricing and no annual contract."
        ),
        "hero_h1": "Best ZoomInfo Alternative for Healthcare Provider Data",
        "hero_subtitle": (
            "ZoomInfo covers every industry. Provyx covers one: healthcare. "
            "If your sales team only sells to physicians, clinics, and health systems, "
            "you don't need a $15K/year general-purpose database. You need provider "
            "contact intelligence sourced from public NPI registries, business listings, "
            "and commercial databases, delivered at a fraction of the cost with no annual "
            "contract and no seat licenses."
        ),

        # Section 2 -- Why Teams Look for an Alternative
        "why_switch_heading": "Why Sales Teams Look for a ZoomInfo Alternative in Healthcare",
        "why_switch_body": (
            "<p>ZoomInfo is the default choice for B2B sales intelligence, and for good reason. "
            "It covers more than 50 industries, integrates with every major CRM, and maintains "
            "one of the largest business contact databases on the market. For a general sales org "
            "prospecting across verticals, it works.</p>"

            "<p>The problems start when your team <em>only</em> sells into healthcare.</p>"

            "<p><strong>Pricing that assumes you need everything.</strong> "
            "<a href=\"https://www.zoominfo.com/\" target=\"_blank\" rel=\"noopener\">ZoomInfo</a> "
            "plans start at roughly $14,995 per year for the SalesOS tier, billed annually. "
            "That price gets you access to its full multi-industry database, intent data signals, "
            "and workflow automation tools. If your reps are calling on orthopedic surgeons and "
            "dental practices, you're paying for millions of records in manufacturing, financial "
            "services, tech, and retail that you'll never open. The per-seat cost rises quickly "
            "once you add users or move to the Advanced or Elite tiers. A three-seat team on the "
            "Advanced plan can easily cross $25,000 per year before adding any integrations or "
            "premium data credits.</p>"

            "<p><strong>Annual contracts with aggressive renewal terms.</strong> "
            "ZoomInfo contracts auto-renew unless you send written cancellation at least 60 days "
            "before the renewal date. Miss that window by a week and you're locked in for another "
            "year. Multiple customer reports cite renewal price increases of 10 to 30 percent, "
            "applied automatically. For a mid-size sales team, that can mean an unexpected jump "
            "from $15K to $18K or more with no new features added. The cancellation process itself "
            "requires written notice sent to a specific address or email, not just a button click "
            "in the dashboard. Teams that don't calendar the deadline in advance often discover "
            "the renewal after the window has already passed.</p>"

            "<p><strong>No NPI verification or taxonomy classification.</strong> "
            "ZoomInfo identifies contacts by company, title, and industry code. It doesn't cross-reference "
            "the <a href=\"https://npiregistry.cms.hhs.gov/\" target=\"_blank\" rel=\"noopener\">National "
            "Plan and Provider Enumeration System (NPPES)</a> to verify that a contact is a licensed "
            "healthcare provider with a valid NPI number. It doesn't attach taxonomy codes that tell you "
            "whether a physician is a family medicine practitioner, an interventional cardiologist, or "
            "a pediatric neurologist. For healthcare sales, that distinction isn't optional. A medical "
            "device rep selling spinal implants can't work from a list that lumps all physicians together. "
            "Without taxonomy codes, your ops team has to manually research each contact's specialty, "
            "which turns a data problem into a labor problem.</p>"

            "<p><strong>Practice-level data gaps.</strong> "
            "ZoomInfo is built around companies and contacts. Healthcare operates around practices, "
            "clinics, and provider groups. You might find a physician's name and a hospital affiliation, "
            "but you won't reliably get the practice's direct phone line, the office address where they "
            "actually see patients, or the practice owner's name. That gap creates friction for reps "
            "who need to reach decision-makers at independent or small group practices, which still "
            "represent a significant share of the "
            "<a href=\"https://www.bls.gov/ooh/healthcare/\" target=\"_blank\" rel=\"noopener\">healthcare "
            "workforce</a>. When a rep dials the main hospital switchboard trying to reach a "
            "dermatologist who sees patients at a separate office three miles away, that's a data "
            "gap costing the rep time and costing you pipeline velocity.</p>"

            "<p><strong>Data freshness for a changing industry.</strong> "
            "Healthcare providers change practice locations, retire, switch specialties, and open new "
            "offices more frequently than contacts in most B2B industries. A physician who was at "
            "a group practice six months ago may now be at a different organization or running their "
            "own practice. ZoomInfo updates its general database on its own cycle, but it doesn't "
            "have a healthcare-specific refresh process tied to NPI registry updates. Stale records "
            "mean bounced mail, disconnected numbers, and wasted rep effort.</p>"

            "<p>None of this makes ZoomInfo a bad product. It makes it a general-purpose product. "
            "If your entire go-to-market motion targets healthcare providers, a general-purpose database "
            "forces your team to do manual enrichment work that a purpose-built source should handle.</p>"
        ),

        # Section 3 -- What Healthcare Teams Actually Need
        "what_teams_need_heading": "What Healthcare Sales Teams Actually Need from Provider Data",
        "what_teams_need_body": (
            "<p>Selling to healthcare providers is different from selling to software companies "
            "or retail chains. The data requirements reflect that difference.</p>"

            "<p><strong>NPI verification.</strong> "
            "Every physician, nurse practitioner, dentist, and allied health professional who bills "
            "a payer has a National Provider Identifier. That 10-digit number is the closest thing "
            "healthcare has to a universal business ID. When your data includes verified NPIs, you "
            "know the contact is a real, credentialed provider, not a retired physician, a student, "
            "or a mismatched record. Databases without NPI verification force your ops team to cross-check "
            "manually, which burns hours and still misses errors.</p>"

            "<p><strong>Taxonomy codes for specialty segmentation.</strong> "
            "Healthcare taxonomy codes (maintained by NUCC) classify providers into more than 800 "
            "specialties and sub-specialties. A taxonomy code tells you not just that someone is a "
            "physician, but that they practice orthopedic surgery, or more specifically, orthopedic "
            "surgery of the spine. If you sell a product that's relevant to 3 specialties out of 800, "
            "taxonomy filtering is the difference between a targeted list and a spray-and-pray campaign.</p>"

            "<p><strong>Practice-level records, not just employer records.</strong> "
            "A cardiologist might be affiliated with a hospital system but see patients at a private "
            "practice three days a week. The practice address, phone number, fax, and office manager "
            "matter more to a sales rep than the hospital system's corporate headquarters. Generic B2B "
            "databases tend to map providers to their largest known affiliation rather than their actual "
            "practice location.</p>"

            "<p><strong>Owner and decision-maker identification.</strong> "
            "In small and mid-size practices, the physician owner is the buyer. There's no VP of "
            "Procurement to route through. Knowing who owns the practice, and being able to reach "
            "them directly, compresses the sales cycle. Generic databases rarely surface ownership "
            "information for medical practices because their data models aren't designed for it.</p>"

            "<p><strong>Specialty-aware geographic filtering.</strong> "
            "Healthcare markets are local. A rep covering Houston needs providers in Houston, not a "
            "national list filtered by state. The ability to filter by specialty, sub-specialty, and "
            "geography simultaneously, down to the ZIP code or metro level, is how teams build "
            "territory-aligned prospect lists that reps can actually work. Generic databases offer "
            "geographic filtering, but combining it with healthcare-specific taxonomy codes is where "
            "most of them fall short.</p>"

            "<p>These aren't nice-to-have features. They're the baseline for any team running "
            "outbound sales or marketing campaigns into the healthcare provider market.</p>"
        ),

        # Section 4 -- Comparison Table
        "comparison_heading": "ZoomInfo vs. Provyx: Quick Comparison",
        "comparison_rows": [
            ("Starting Price", "~$14,995/year", "Pay per record, no minimum"),
            ("Contract Terms", "Annual, auto-renew with 60-day cancellation notice", "Month-to-month or per-list purchase"),
            ("Healthcare Specialties", "General industry tags, no taxonomy codes", "800+ specialties via NUCC taxonomy codes"),
            ("NPI Verification", "Not included", "Every provider record is NPI-verified"),
            ("Taxonomy Codes", "Not available", "Included on all provider records"),
            ("Practice Data", "Company-level records, limited practice detail", "Practice name, address, phone, fax, owner name"),
            ("Data Delivery", "Platform access, CRM sync, API", "CSV, Excel, or API"),
            ("Best For", "Multi-industry B2B sales teams", "Teams that sell exclusively to healthcare providers"),
        ],

        # Section 5 -- How Provyx Works
        "how_it_works_heading": "How Provyx Works as a ZoomInfo Alternative for Healthcare",
        "how_it_works_body": (
            "<p>Provyx is a healthcare provider business data platform. It doesn't try to cover "
            "every industry. It covers one vertical deeply and does it well, combining public "
            "registry data with commercial data sources to build verified, practice-level "
            "provider records that sales teams can act on immediately.</p>"

            "<h3>Where the Data Comes From</h3>"
            "<p>Provyx sources its provider contact intelligence from three categories of data:</p>"
            "<ul>"
            "<li><strong>Public NPI registries.</strong> The NPPES database, maintained by CMS, is the "
            "authoritative source for provider identification. Provyx ingests the full NPI registry and "
            "uses it as the foundation for every record. This gives you verified NPI numbers, taxonomy "
            "codes, enumeration dates, and practice addresses as reported to CMS.</li>"
            "<li><strong>Business listings and public filings.</strong> State licensing boards, secretary "
            "of state filings, business directories, and public web data fill in practice details that "
            "the NPI registry doesn't include: direct phone numbers, websites, office hours, and ownership "
            "information.</li>"
            "<li><strong>Commercial databases.</strong> Third-party data providers contribute firmographic "
            "details, technology stack information, and contact enrichment. This layer adds LinkedIn profile "
            "URLs, estimated practice revenue ranges, and staff size indicators where available.</li>"
            "</ul>"
            "<p>Every record passes through a matching process that links the NPI to the enriched practice "
            "profile. Records that can't be confidently matched are flagged, not shipped.</p>"

            "<h3>NPI Verification Process</h3>"
            "<p>When Provyx delivers a provider record, the NPI on that record has been verified against "
            "the current NPPES data. That means the NPI is active (not deactivated), it matches the "
            "provider's name, and the associated taxonomy code reflects their current reported specialty. "
            "This sounds simple, but it eliminates a common problem: stale records where a provider has "
            "retired, moved, or changed specialties. ZoomInfo's records don't go through this step because "
            "NPI data isn't part of their data model.</p>"

            "<h3>What's in Each Record</h3>"
            "<p>A standard Provyx provider record includes:</p>"
            "<ul>"
            "<li>Provider full name (individual or organization)</li>"
            "<li>NPI number (Type 1 for individuals, Type 2 for organizations)</li>"
            "<li>Primary and secondary taxonomy codes with plain-language specialty labels</li>"
            "<li>Practice name and doing-business-as name</li>"
            "<li>Practice mailing address and practice location address</li>"
            "<li>Phone number and fax number</li>"
            "<li>Practice website URL</li>"
            "<li>Practice owner name (where available from public records)</li>"
            "<li>LinkedIn profile URL (where matched with high confidence)</li>"
            "<li>Enumeration date (when the NPI was first assigned)</li>"
            "</ul>"
            "<p>Not every field is populated on every record. Coverage rates vary by field: NPI and taxonomy "
            "are at 100% by definition, phone numbers are above 85%, websites are around 70%, and LinkedIn "
            "matches are closer to 55%. Provyx publishes its field-level coverage rates so you know what "
            "to expect before you buy.</p>"

            "<h3>Delivery Formats</h3>"
            "<p>You can get your data three ways:</p>"
            "<ul>"
            "<li><strong>CSV download.</strong> Flat file, ready for import into any CRM or spreadsheet. "
            "Most customers start here.</li>"
            "<li><strong>Excel download.</strong> Formatted workbook with column headers and basic filtering. "
            "Useful for handing directly to reps.</li>"
            "<li><strong>API access.</strong> RESTful API for pulling records into your own systems "
            "programmatically. Available on growth plans.</li>"
            "</ul>"

            "<h3>Pricing Model</h3>"
            "<p>Provyx charges per record. You define the specialty, geography, and filters you need, "
            "and you pay for the records that match. There's no annual contract. There's no seat license. "
            "If you need 500 orthopedic surgeon records in Texas, you pay for 500 records. If you need "
            "50,000 primary care providers nationwide, the per-record price drops at volume. You won't "
            "get a surprise renewal invoice 12 months later because there's nothing to renew unless "
            "you choose to reorder.</p>"

            "<p>This model works well for teams with variable data needs. If you're launching into a "
            "new territory, you buy records for that territory. If you're running a one-time campaign "
            "targeting a specific specialty, you buy that list once. There's no pressure to justify "
            "an annual platform cost across months when you aren't actively buying data.</p>"
        ),

        # Section 6 -- What Provyx Doesn't Do
        "limitations_heading": "What Provyx Doesn't Do",
        "limitations_body": (
            "<p>Provyx isn't a drop-in replacement for everything ZoomInfo offers, and it's not trying "
            "to be.</p>"
            "<p>Provyx doesn't cover 50+ industries. If your company sells to healthcare providers "
            "<em>and</em> to financial services firms and tech startups, you'll still need a general "
            "B2B database for those other verticals. Provyx only covers healthcare.</p>"
            "<p>Provyx isn't an all-in-one sales platform. There's no built-in email sequencing, no "
            "phone dialer, no intent data scoring, and no conversation intelligence. It's a data layer. "
            "You plug the data into the outreach tools you already use, whether that's Salesloft, "
            "Outreach, HubSpot, or a basic CRM with email templates.</p>"
            "<p>Provyx doesn't provide hospital financial data, claims volume analytics, or health "
            "system org charts. If you need those things, a platform like Definitive Healthcare is "
            "better suited for that specific job. Provyx focuses on getting you accurate, verified "
            "contact records for individual providers and practices.</p>"
            "<p>It also doesn't provide buyer intent signals, website visitor identification, or "
            "technographic data outside of healthcare practices. If those capabilities drive your "
            "current workflow in ZoomInfo, you'd lose them by switching. For teams where the primary "
            "value was always the healthcare contact data, those features were extras they never adopted.</p>"
            "<p>Knowing what a tool doesn't do saves you as much time as knowing what it does.</p>"
        ),

        # Section 7 -- Who Switches
        "who_switches_heading": "Who Switches from ZoomInfo to Provyx",
        "who_switches_body": (
            "<p>Not every ZoomInfo customer is a good fit for Provyx. The teams that switch tend to "
            "share a common trait: healthcare is their only vertical, not one of many. Here are "
            "the profiles that make the move most often.</p>"

            "<h3>Medical Device Sales Teams</h3>"
            "<p>A spinal implant company with 30 reps doesn't need a database of 200 million contacts "
            "across every industry. They need orthopedic surgeons, neurosurgeons, and pain management "
            "specialists, segmented by taxonomy code and geography. They were paying ZoomInfo $25K or more "
            "per year for a platform where 95% of the records were irrelevant. Provyx gives them exactly "
            "the provider list they need at a fraction of the annual cost, with NPI verification already done. "
            "Device reps also benefit from practice-level data because many purchasing decisions happen at "
            "the practice or ambulatory surgery center level, not at a hospital purchasing department.</p>"

            "<h3>Healthcare Marketing Agencies</h3>"
            "<p>Agencies running campaigns for healthcare clients need specialty-specific lists on a "
            "regular basis. One month it's dermatologists in the Southeast, the next it's pediatric "
            "dentists in the Midwest. ZoomInfo's annual contract and per-seat pricing doesn't fit "
            "an agency model where data needs change per client engagement. Provyx's pay-per-record "
            "model lets agencies buy what they need for each campaign without carrying a fixed annual cost. "
            "Agencies can also pass through the exact data cost to clients on a per-project basis, "
            "keeping margins transparent and predictable.</p>"

            "<h3>Health IT Companies</h3>"
            "<p>Companies selling EHR systems, practice management software, or telehealth platforms "
            "to physician practices need to know what technology a practice currently uses. Provyx's "
            "commercial data layer includes technology detection signals for practice websites, so "
            "health IT sales teams can filter by current EHR vendor, online scheduling presence, or "
            "patient portal adoption. That kind of technographic filtering on healthcare practices "
            "specifically isn't something ZoomInfo exposes at the practice level. A health IT company "
            "targeting practices still running legacy PM software can build that list in Provyx without "
            "manually auditing practice websites one by one.</p>"

            "<h3>Pharma Commercial Teams</h3>"
            "<p>Pharmaceutical sales teams that need prescriber-level data, segmented by specialty and "
            "region, often find ZoomInfo's data too broad and its contracts too rigid. A regional pharma "
            "company doesn't need an enterprise license. They need 2,000 endocrinologists in five states "
            "with verified NPIs and direct office phone numbers. Provyx delivers that as a single list "
            "purchase with no ongoing commitment. The NPI on each record also allows pharma teams to "
            "cross-reference with their own prescriber databases and compliance systems.</p>"
        ),

        # Section 8 -- Migration Guide
        "migration_heading": "How to Switch from ZoomInfo to Provyx",
        "migration_body": (
            "<p>Switching data providers doesn't have to be a six-month project. Here's a practical path.</p>"

            "<p><strong>Step 1: Request a sample list.</strong> "
            "Pick a specialty and geography that your team actively prospects. Ask Provyx for a sample "
            "file of 50 to 100 records. Compare the fields, coverage, and accuracy against what you're "
            "currently pulling from ZoomInfo. Pay attention to phone number accuracy, NPI presence, "
            "and taxonomy detail.</p>"

            "<p><strong>Step 2: Run a side-by-side test.</strong> "
            "Give your reps both lists for the same territory. Track connect rates, bounce rates on "
            "addresses, and time-to-qualification. Provider data quality shows up fast in outbound "
            "metrics. If reps connect with more decision-makers per dial, the data is working.</p>"

            "<p><strong>Step 3: Start with a single list purchase.</strong> "
            "Don't commit to a full migration on day one. Buy one list for one team or one territory. "
            "Import it into your CRM alongside your existing data. Let your reps use it for two to "
            "four weeks and collect feedback.</p>"

            "<p><strong>Step 4: Scale based on results.</strong> "
            "If the data performs, expand to more specialties and geographies. Provyx's per-record "
            "pricing means you can scale up incrementally without negotiating a new contract tier. "
            "If your ZoomInfo renewal is approaching, time your Provyx trial so you have data to "
            "make the decision before the 60-day cancellation window closes.</p>"

            "<p><strong>Step 5: Notify your team and update workflows.</strong> "
            "If you decide to move forward, update your CRM import templates to match Provyx's column "
            "structure. Brief your reps on any new fields like taxonomy codes and NPI numbers that "
            "they weren't seeing in ZoomInfo data. Most teams find that the transition takes one to "
            "two days of admin work, not weeks.</p>"

            "<p>Most teams complete the evaluation in two to three weeks. The ones that plan around "
            "their ZoomInfo renewal date avoid getting locked into another year.</p>"
        ),

        # Section 9 -- FAQs
        "faqs": [
            {
                "question": "Is Provyx a direct replacement for ZoomInfo?",
                "answer": (
                    "Not across the board. ZoomInfo covers 50+ industries and includes sales engagement "
                    "tools like email sequencing and a dialer. Provyx only covers healthcare provider "
                    "business data. If your team sells exclusively to healthcare providers, Provyx replaces "
                    "the data layer at a lower cost with better healthcare-specific fields like NPI numbers "
                    "and taxonomy codes. If you sell into multiple industries, you'd still need a "
                    "general-purpose tool for non-healthcare verticals."
                ),
            },
            {
                "question": "How does Provyx verify its healthcare provider data?",
                "answer": (
                    "Every provider record is matched against the NPPES registry maintained by CMS. "
                    "Provyx confirms that the NPI is active, matches the provider's name, and reflects "
                    "their current taxonomy classification. Practice details like phone numbers and "
                    "addresses are cross-referenced across business listings and public filings. Records "
                    "that can't be confidently verified are excluded from delivery rather than shipped "
                    "with a disclaimer. The goal is accuracy over volume."
                ),
            },
            {
                "question": "What does Provyx cost compared to ZoomInfo?",
                "answer": (
                    "ZoomInfo starts at roughly $14,995 per year on an annual contract with per-seat "
                    "pricing. Provyx uses pay-per-record pricing with no annual contract and no seat "
                    "licenses. A typical list purchase costs a fraction of ZoomInfo's annual fee. Exact "
                    "pricing depends on volume and the filters you apply. You can request a quote on the "
                    "Provyx pricing page for your specific use case."
                ),
            },
            {
                "question": "Can I import Provyx data into my CRM?",
                "answer": (
                    "Yes. Provyx delivers data as CSV or Excel files that import into any CRM, including "
                    "Salesforce, HubSpot, Zoho, and Microsoft Dynamics. The files include standard column "
                    "headers that map to common CRM fields. Most teams complete the import in under an "
                    "hour. If you're on a growth plan with API access, you can also pull records directly "
                    "into your systems programmatically without manual file imports."
                ),
            },
            {
                "question": "How current is the data in Provyx?",
                "answer": (
                    "Provyx refreshes its core NPI registry data in sync with the NPPES weekly update "
                    "cycle. Practice details sourced from business listings and commercial databases are "
                    "updated on a rolling basis, with most records refreshed within a 90-day window. "
                    "When you purchase a list, you're getting data from the most recent available refresh. "
                    "Provyx timestamps every record so you can see when it was last verified."
                ),
            },
        ],

        # Section 10 -- Related Links
        "related_links": [
            {"label": "Compare Provyx vs. ZoomInfo in Detail", "url": "/compare/zoominfo/"},
            {"label": "Compare Provyx vs. Definitive Healthcare", "url": "/compare/definitive-healthcare/"},
            {"label": "Provyx Pricing", "url": "/pricing/"},
            {"label": "Provyx for Medical Device Sales Teams", "url": "/for/medical-device-sales/"},
            {"label": "Provyx for Healthcare Marketing Agencies", "url": "/for/healthcare-marketing-agencies/"},
            {"label": "Provyx for Health IT Companies", "url": "/for/health-it-companies/"},
        ],

        # Outbound reference links for schema / context
        "outbound_links": [
            "https://www.zoominfo.com/",
            "https://npiregistry.cms.hhs.gov/",
            "https://www.bls.gov/ooh/healthcare/",
        ],
    },

    # ===================================================================
    # 2. Definitive Healthcare Alternative
    # ===================================================================
    {
        "slug": "definitive-healthcare-alternative",
        "competitor": "Definitive Healthcare",
        "competitor_url": "https://www.definitivehc.com/",
        "title": "Best Definitive Healthcare Alternative | Provyx",
        "meta_description": (
            "Provyx is a Definitive Healthcare alternative for teams that need "
            "provider contact intelligence without enterprise pricing. NPI-verified "
            "records, pay-per-record, no annual contract."
        ),
        "hero_h1": "Best Definitive Healthcare Alternative for Provider Contact Data",
        "hero_subtitle": (
            "Definitive Healthcare is a powerful analytics platform for hospital and health system "
            "intelligence. But if your team's primary job is reaching individual providers and practices "
            "with outbound sales and marketing, you're paying enterprise prices for capabilities you "
            "don't use. Provyx delivers NPI-verified provider contact intelligence, sourced from public "
            "NPI registries, business listings, and commercial databases, with pay-per-record pricing "
            "and no annual contract. You get the provider data you need without the analytics platform "
            "you don't."
        ),

        # Section 2 -- Why Teams Look for an Alternative
        "why_switch_heading": "Why Teams Look for a Definitive Healthcare Alternative",
        "why_switch_body": (
            "<p><a href=\"https://www.definitivehc.com/\" target=\"_blank\" rel=\"noopener\">Definitive "
            "Healthcare</a> built its reputation on deep intelligence about hospitals, health systems, "
            "and IDNs. If you're mapping referral networks, analyzing claims data, or tracking hospital "
            "capital budgets, it's one of the strongest platforms available. The problems surface when "
            "teams buy Definitive for a different job: building provider contact lists for outbound "
            "sales and marketing.</p>"

            "<p><strong>Enterprise pricing that starts high and climbs.</strong> "
            "Definitive Healthcare pricing isn't published, but industry estimates and customer reports "
            "place entry-level subscriptions between $25,000 and $50,000 per year for basic platform "
            "access. More comprehensive packages with claims data, physician-level intelligence, and "
            "advanced analytics push into the $75,000 to $100,000+ range. CRM integration add-ons "
            "alone can cost $22,000 or more annually. Contracts auto-renew with 5% annual uplifts "
            "built into the terms. For a 10-person sales team that just needs provider phone numbers "
            "and addresses segmented by specialty, that's a significant overspend.</p>"

            "<p><strong>A complex platform with a steep learning curve.</strong> "
            "Definitive Healthcare is built for healthcare analytics professionals. The platform includes "
            "claims analysis tools, affiliation mapping, market share reports, and competitive intelligence "
            "dashboards. That depth is valuable for strategy teams and market access analysts. It's "
            "overwhelming for a sales rep who needs to pull a list of gastroenterologists in Phoenix "
            "and start making calls. Multiple users report that onboarding takes weeks, and many "
            "features go unused because the team only needed the contact data layer.</p>"

            "<p><strong>Strong on hospitals, weaker on individual providers and small practices.</strong> "
            "Definitive Healthcare's core data asset is its hospital and health system intelligence: bed "
            "counts, technology installations, C-suite contacts, financial performance, and claims volume. "
            "When you move down to individual physician contacts and small group practices, the depth "
            "drops off. A two-provider family medicine practice in a suburban office park isn't covered "
            "with the same richness as a 500-bed academic medical center. If your sales motion targets "
            "those small and mid-size practices, which represent a large segment of the "
            "<a href=\"https://www.bls.gov/ooh/healthcare/\" target=\"_blank\" rel=\"noopener\">healthcare "
            "provider workforce</a>, the data you're actually using doesn't justify the price you're paying.</p>"

            "<p><strong>Contract terms that make it hard to leave.</strong> "
            "Auto-renewal with built-in price escalation is standard. If you don't flag your cancellation "
            "within the notice window, you're committed to another year at a higher rate. Teams that "
            "signed up for a pilot or initial evaluation sometimes find themselves locked into multi-year "
            "commitments before they've fully validated ROI. The 5% annual uplift is contractual, not "
            "optional, so a $30,000 subscription becomes $31,500 in year two and $33,075 in year three "
            "without any change in usage or scope.</p>"

            "<p><strong>Export and download limitations.</strong> "
            "Even with a paid subscription, Definitive Healthcare limits how many records you can "
            "export per month or per query. For sales teams that need to pull large lists regularly "
            "and push them into a CRM or outreach tool, these caps create bottlenecks. You may end "
            "up rationing your exports or submitting requests to the platform team for bulk downloads, "
            "adding delays to what should be a straightforward workflow.</p>"

            "<p>Definitive Healthcare is a genuinely strong product for the use cases it was designed "
            "for. The mismatch happens when teams buy it as a provider contact database, because that's "
            "not where its strength is concentrated.</p>"
        ),

        # Section 3 -- What Healthcare Teams Actually Need
        "what_teams_need_heading": "What Healthcare Teams Actually Need from a Provider Data Source",
        "what_teams_need_body": (
            "<p>Teams doing outbound sales and marketing to healthcare providers have a specific set "
            "of data requirements. These requirements look different from what a market access team "
            "or a hospital strategy group needs.</p>"

            "<p><strong>NPI verification on every record.</strong> "
            "The <a href=\"https://npiregistry.cms.hhs.gov/\" target=\"_blank\" rel=\"noopener\">National "
            "Provider Identifier</a> is the standard unique identifier for healthcare providers in the "
            "United States. When your data includes verified NPIs, you can confirm that a contact is a "
            "currently credentialed provider, not a retired physician or a mismatched record. Outbound "
            "campaigns built on unverified data waste rep time and damage your brand when calls go to "
            "wrong numbers or outdated contacts.</p>"

            "<p><strong>Taxonomy codes for precise specialty targeting.</strong> "
            "NUCC taxonomy codes classify providers into more than 800 specialties and sub-specialties. "
            "If you're selling a product relevant to interventional cardiologists, you don't want a list "
            "of all cardiologists. Taxonomy codes give you that level of precision. General analytics "
            "platforms often group providers into broad specialty buckets that aren't granular enough "
            "for targeted outbound.</p>"

            "<p><strong>Practice-level contact information.</strong> "
            "Sales reps don't call hospital systems at their corporate headquarters to reach a physician. "
            "They call the practice where the doctor sees patients. Practice name, direct phone number, "
            "fax number, street address, and website are the fields that drive outbound activity. A platform "
            "optimized for hospital intelligence may not prioritize these practice-level details.</p>"

            "<p><strong>Simple data delivery.</strong> "
            "Not every team needs a full analytics platform. Some teams need a clean CSV they can import "
            "into Salesforce and start working. The ability to get data out of the system quickly, without "
            "training on a complex interface, matters when your reps are measured on activity volume.</p>"

            "<p><strong>Ownership and decision-maker data.</strong> "
            "In a 3-provider dermatology practice, the practice owner is typically the person who "
            "signs vendor contracts. There's no committee, no RFP process. Your rep needs to know "
            "who the owner is and how to reach them. Analytics platforms focused on hospital C-suites "
            "don't always surface this information for small practices. A data source built around "
            "the provider practice model does.</p>"

            "<p><strong>Specialty-aware geographic segmentation.</strong> "
            "Healthcare is local. A sales territory might cover a metro area or a cluster of ZIP codes. "
            "The ability to filter by NUCC taxonomy code and geographic boundary at the same time "
            "is how teams build territory-ready prospect lists. Broad analytics platforms may offer "
            "geographic filtering, but combining it with granular taxonomy codes at the individual "
            "provider level is where many fall short.</p>"

            "<p>If these are your primary requirements, you don't need a $50K analytics suite. You need "
            "a focused provider data source that does these things well.</p>"
        ),

        # Section 4 -- Comparison Table
        "comparison_heading": "Definitive Healthcare vs. Provyx: Quick Comparison",
        "comparison_rows": [
            ("Starting Price", "$25,000-$50,000+/year", "Pay per record, no minimum"),
            ("Contract Terms", "Annual, auto-renew with 5% annual uplifts", "Month-to-month or per-list purchase"),
            ("Healthcare Specialties", "Broad specialty categories with claims-based grouping", "800+ specialties via NUCC taxonomy codes"),
            ("NPI Verification", "NPI data included but primary focus is facility-level", "Every individual provider record is NPI-verified"),
            ("Taxonomy Codes", "Available but secondary to claims-based classification", "Primary classification system on all records"),
            ("Practice Data", "Strong on hospitals/systems, limited on small practices", "Practice name, address, phone, fax, owner name for all sizes"),
            ("Data Delivery", "Platform-based with optional CRM integration ($22K+)", "CSV, Excel, or API included"),
            ("Best For", "Hospital/health system analytics and strategy teams", "Teams running outbound to individual providers and practices"),
        ],

        # Section 5 -- How Provyx Works
        "how_it_works_heading": "How Provyx Works as a Definitive Healthcare Alternative",
        "how_it_works_body": (
            "<p>Provyx is a provider contact intelligence platform. It doesn't replicate Definitive "
            "Healthcare's analytics capabilities, and it doesn't try to. What it does is deliver "
            "accurate, NPI-verified provider records with the fields outbound teams actually use, "
            "at a price point that makes sense for contact data.</p>"

            "<h3>Data Sourcing</h3>"
            "<p>Provyx builds its provider records from three source categories:</p>"
            "<ul>"
            "<li><strong>Public NPI registries.</strong> The NPPES database maintained by CMS provides "
            "the foundation: NPI numbers, taxonomy codes, enumeration dates, provider names, and "
            "practice addresses as reported for Medicare and Medicaid billing. This is the same data "
            "that Definitive Healthcare uses as one of its inputs, but Provyx makes it the primary "
            "layer rather than one of many.</li>"
            "<li><strong>Business listings and public records.</strong> State licensing boards, secretary "
            "of state business filings, public web directories, and healthcare-specific directories add "
            "practice phone numbers, websites, fax numbers, and ownership details. These sources fill "
            "the gaps that the NPI registry doesn't cover, particularly for practice operations data.</li>"
            "<li><strong>Commercial databases.</strong> Third-party data providers contribute technology "
            "detection, LinkedIn profile matching, estimated revenue ranges, and staff size indicators. "
            "This layer adds firmographic and technographic depth to the base contact record.</li>"
            "</ul>"

            "<h3>NPI Verification</h3>"
            "<p>Every individual provider record in Provyx has been matched against the current NPPES "
            "data. The verification checks that the NPI is active and not deactivated, the provider's "
            "name matches the NPI record, and the taxonomy code reflects the provider's current reported "
            "specialty. Definitive Healthcare includes NPI data, but its verification emphasis is on "
            "facility and system identifiers rather than individual provider records. Provyx treats "
            "individual provider NPI verification as a first-class requirement because that's what "
            "outbound sales teams depend on.</p>"

            "<h3>What You Get in Each Record</h3>"
            "<p>A Provyx provider record includes:</p>"
            "<ul>"
            "<li>Provider full name</li>"
            "<li>NPI number (Type 1 for individuals, Type 2 for organizations)</li>"
            "<li>Primary and secondary taxonomy codes with human-readable specialty labels</li>"
            "<li>Practice name and DBA name</li>"
            "<li>Practice mailing address and location address</li>"
            "<li>Direct phone number and fax number</li>"
            "<li>Practice website URL</li>"
            "<li>Practice owner name (from public records where available)</li>"
            "<li>LinkedIn profile URL (where matched with high confidence)</li>"
            "<li>Enumeration date</li>"
            "</ul>"
            "<p>Field coverage varies. NPI and taxonomy are 100%. Phone numbers are above 85%. Website "
            "URLs are around 70%. LinkedIn matches are closer to 55%. Provyx is transparent about "
            "these rates because you should know what you're buying before you buy it.</p>"

            "<h3>Delivery Formats</h3>"
            "<p>Provyx delivers data as:</p>"
            "<ul>"
            "<li><strong>CSV files</strong> for CRM import or custom processing.</li>"
            "<li><strong>Excel workbooks</strong> with formatted columns and headers, ready for reps.</li>"
            "<li><strong>API access</strong> for programmatic integration, available on growth plans.</li>"
            "</ul>"
            "<p>There's no mandatory platform login to access your data. You don't need to learn a new "
            "interface or schedule a training session. You define your filters, receive your file, and "
            "put it to work.</p>"

            "<h3>Pricing</h3>"
            "<p>Provyx charges per record. No annual contract. No seat licenses. No auto-renewal with "
            "built-in escalation. You define your specialty, geography, and practice type filters, and "
            "you pay for the matching records. Volume pricing applies at higher quantities. A team that "
            "would spend $25,000 to $50,000 on a Definitive Healthcare subscription for contact data "
            "can typically get what they need from Provyx for a fraction of that, because they're not "
            "paying for claims analytics, hospital intelligence, and platform features they don't use.</p>"

            "<p>There are no export caps. When you purchase a list, you get the full file. You can "
            "import it into your CRM, share it with your reps, and reuse it as long as it's current. "
            "There's no per-download fee and no monthly limit on how many records you can access from "
            "a purchased list. The data is yours to work with once you've paid for it.</p>"
        ),

        # Section 6 -- What Provyx Doesn't Do
        "limitations_heading": "What Provyx Doesn't Do",
        "limitations_body": (
            "<p>Provyx isn't a replacement for Definitive Healthcare's full platform, and it shouldn't "
            "be evaluated as one.</p>"
            "<p>Provyx doesn't provide claims data analytics. If you need to know how many knee "
            "replacements a hospital performed last year or which physicians have the highest referral "
            "volume for a specific procedure, that's not what Provyx does. Definitive Healthcare is "
            "genuinely better at that job.</p>"
            "<p>Provyx doesn't map health system org charts, track hospital M&A activity, or provide "
            "capital budget intelligence. If your team's workflow depends on understanding health system "
            "hierarchies and affiliate relationships, Provyx isn't the right tool.</p>"
            "<p>Provyx doesn't include an all-in-one sales engagement layer. There's no built-in email "
            "sequencing, no phone dialer, and no intent data scoring. It's a data source that feeds "
            "into whatever outreach tools your team already runs.</p>"
            "<p>Provyx also doesn't cover payer data, ACO network analysis, or facility accreditation "
            "details. Those are specialized data sets that Definitive Healthcare includes for strategy "
            "and market access teams. If your team depends on those data points, removing Definitive "
            "Healthcare entirely would leave a gap.</p>"
            "<p>What Provyx does is deliver verified provider contact records. If that's the specific "
            "job you're hiring a data source to do, it does it well and it does it at a lower cost "
            "than platforms that bundle it with features you aren't using.</p>"
        ),

        # Section 7 -- Who Switches
        "who_switches_heading": "Who Switches from Definitive Healthcare to Provyx",
        "who_switches_body": (
            "<p>The teams that switch share a common pattern: they bought Definitive Healthcare for "
            "contact data and realized they were paying for an analytics platform they didn't need.</p>"

            "<h3>Medical Device Sales Teams</h3>"
            "<p>A surgical device company with a regional sales team doesn't need claims analytics "
            "or hospital market share reports. They need orthopedic surgeons segmented by sub-specialty "
            "and geography, with direct practice phone numbers and NPI verification. They were paying "
            "Definitive Healthcare $40K+ per year and using maybe 20% of the platform. Provyx gives "
            "them the 20% they actually used, with better coverage on small and mid-size practices, "
            "for a fraction of the cost. For device companies selling into ambulatory surgery centers "
            "and outpatient clinics, Provyx's practice-level records are particularly relevant because "
            "those facilities are where the purchasing decisions often happen.</p>"

            "<h3>Healthcare Marketing Agencies</h3>"
            "<p>Agencies managing outbound campaigns for healthcare clients need fresh, specialty-specific "
            "lists on a project basis. Definitive Healthcare's annual contract and enterprise pricing "
            "doesn't match an agency's billing model where data costs need to be scoped per client "
            "engagement. Provyx's per-record pricing lets agencies buy exactly the data each campaign "
            "requires and pass the cost through to the client without absorbing a fixed annual platform fee. "
            "Agencies can also request data for specialties they haven't worked with before without "
            "worrying about whether their subscription tier covers that segment.</p>"

            "<h3>Health IT Companies Selling to Practices</h3>"
            "<p>Companies selling EHR systems, practice management software, revenue cycle management, "
            "or telehealth solutions to physician practices need practice-level data with technology "
            "indicators. Definitive Healthcare is strong on hospital technology installations but thinner "
            "on what a 5-provider family medicine practice is running. Provyx's commercial data layer "
            "includes technology detection on practice websites, which gives health IT sales teams "
            "a way to filter by current tech stack at the practice level. That means a company selling "
            "a modern cloud-based EHR can target practices still running on-premise systems, without "
            "paying for hospital intelligence they don't use.</p>"

            "<h3>Pharma Commercial Teams with Regional Focus</h3>"
            "<p>Not every pharma company is a global enterprise with a seven-figure data budget. Regional "
            "and specialty pharma companies need prescriber data for specific therapeutic areas and "
            "geographies. A company launching a new diabetes drug in 12 states needs endocrinologists "
            "and primary care providers in those states, with verified NPIs and practice contact details. "
            "Definitive Healthcare's entry price is hard to justify for a scoped regional launch. Provyx "
            "delivers the same contact data for a per-list cost that aligns with a regional budget. "
            "The NPI on each record also enables cross-referencing with the pharma company's internal "
            "prescriber tracking and compliance systems.</p>"
        ),

        # Section 8 -- Migration Guide
        "migration_heading": "How to Switch from Definitive Healthcare to Provyx",
        "migration_body": (
            "<p>If you're considering a move, here's a practical evaluation path that doesn't require "
            "canceling anything upfront.</p>"

            "<p><strong>Step 1: Request a sample list.</strong> "
            "Choose a specialty and geography your team is actively working. Request a sample from "
            "Provyx and compare it field-by-field against what you'd pull from Definitive Healthcare "
            "for the same criteria. Focus on phone number accuracy, NPI presence, practice address "
            "completeness, and taxonomy granularity.</p>"

            "<p><strong>Step 2: Test with your reps.</strong> "
            "Give a group of reps the Provyx sample data alongside their current Definitive Healthcare "
            "lists. Track connect rates and the time reps spend researching or correcting records before "
            "making a call. Better data shows up in fewer dead-end calls and less manual lookup time.</p>"

            "<p><strong>Step 3: Buy a single list.</strong> "
            "Don't negotiate a migration plan until you've validated the data in production. Purchase "
            "one list for one territory or specialty segment. Import it into your CRM and let your team "
            "work it for two to four weeks. Collect concrete feedback on data quality and coverage.</p>"

            "<p><strong>Step 4: Time your transition around renewal.</strong> "
            "Definitive Healthcare contracts auto-renew with built-in uplifts. If your evaluation confirms "
            "that Provyx covers your contact data needs, make sure you submit your cancellation notice "
            "before the auto-renewal window closes. Plan your evaluation timeline backward from that date "
            "so you aren't rushing the decision.</p>"

            "<p><strong>Step 5: Scale incrementally.</strong> "
            "Once you've confirmed data quality, expand your Provyx usage to additional specialties and "
            "regions. There's no contract tier to negotiate. You simply order more records as your team "
            "needs them. If some of your teams still need Definitive Healthcare's analytics for strategy "
            "work, you can run both: Provyx for outbound contact data, Definitive Healthcare for "
            "hospital intelligence, each tool doing the job it's best at.</p>"
        ),

        # Section 9 -- FAQs
        "faqs": [
            {
                "question": "Is Provyx a replacement for Definitive Healthcare?",
                "answer": (
                    "Only for the contact data use case. Definitive Healthcare offers claims analytics, "
                    "hospital intelligence, health system mapping, and market research tools that Provyx "
                    "doesn't replicate. If your team's primary need is provider contact records for "
                    "outbound sales and marketing, Provyx covers that at a significantly lower cost. "
                    "If you depend on claims data or hospital financial analysis, Definitive Healthcare "
                    "is still the stronger tool for those jobs."
                ),
            },
            {
                "question": "How does Provyx's data compare to Definitive Healthcare for small practices?",
                "answer": (
                    "This is where Provyx tends to perform well. Definitive Healthcare's data strength is "
                    "concentrated on hospitals, health systems, and large physician groups. Provyx sources "
                    "data from public NPI registries, business listings, and commercial databases, which "
                    "gives it strong coverage on independent and small group practices. Practice phone numbers, "
                    "websites, owner names, and direct addresses are available for practices of all sizes."
                ),
            },
            {
                "question": "What does Provyx cost compared to Definitive Healthcare?",
                "answer": (
                    "Definitive Healthcare subscriptions typically range from $25,000 to $100,000+ per year "
                    "depending on the package, with CRM integration costing $22,000+ extra annually. Provyx "
                    "uses pay-per-record pricing with no annual contract and no seat licenses. A typical list "
                    "purchase for a specific specialty and geography costs a fraction of Definitive Healthcare's "
                    "annual fee. You can request a quote on the Provyx pricing page for your exact requirements."
                ),
            },
            {
                "question": "Can I use Provyx alongside Definitive Healthcare?",
                "answer": (
                    "Yes, and some teams do exactly that. They keep Definitive Healthcare for hospital-level "
                    "analytics and strategy work, and use Provyx for day-to-day outbound prospecting data. "
                    "This approach lets the strategy team keep the analytics they depend on while reducing "
                    "the per-record cost for sales teams that just need contact information. It also reduces "
                    "pressure to put every user on the Definitive Healthcare license."
                ),
            },
            {
                "question": "How long does it take to get data from Provyx?",
                "answer": (
                    "Standard list requests are delivered within one to two business days. You define your "
                    "filters, submit the request, and receive a CSV or Excel file by email or through your "
                    "account dashboard. API access on growth plans provides near-instant results for "
                    "programmatic queries. There's no platform onboarding period, no training requirement, "
                    "and no learning curve before you can start pulling data and putting it to work."
                ),
            },
        ],

        # Section 10 -- Related Links
        "related_links": [
            {"label": "Compare Provyx vs. Definitive Healthcare in Detail", "url": "/compare/definitive-healthcare/"},
            {"label": "Compare Provyx vs. ZoomInfo", "url": "/compare/zoominfo/"},
            {"label": "Provyx Pricing", "url": "/pricing/"},
            {"label": "Provyx for Medical Device Sales Teams", "url": "/for/medical-device-sales/"},
            {"label": "Provyx for Pharma Commercial Teams", "url": "/for/pharma-commercial-teams/"},
            {"label": "Provyx for Health IT Companies", "url": "/for/health-it-companies/"},
        ],

        # Outbound reference links for schema / context
        "outbound_links": [
            "https://www.definitivehc.com/",
            "https://npiregistry.cms.hhs.gov/",
            "https://www.bls.gov/ooh/healthcare/",
        ],
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
         "answer": "We provide verified practice data and owner contacts for healthcare providers across 40+ specialties. Every record includes practice name, address, business phone, website, owner or decision-maker name, NPI number, taxonomy codes, and LinkedIn profile. Direct email and mobile phone enrichment are available as add-ons."},
        {"question": "Where does Provyx source its provider data?",
         "answer": "Our data comes from public registries including the CMS NPI Registry, state licensing boards, commercial databases, and proprietary web intelligence. Every record is verified against multiple sources before delivery."},
        {"question": "How often is the provider data updated?",
         "answer": "We continuously verify and refresh our database. Provider contact information changes frequently as staff turn over and practices move. Our multi-source verification process catches these changes so you're working with current data, not records that are months old."},
        {"question": "Can I get a custom provider list for my specific needs?",
         "answer": "Yes. We build custom lists filtered by specialty, geography, practice size, technology stack, and other criteria. Tell us what you're targeting and we'll build a matched list."},
        {"question": "How is Provyx different from ZoomInfo or Apollo?",
         "answer": "Generic B2B databases treat healthcare as one of many industries. ZoomInfo starts at $15K/year with annual contracts. Apollo isn't built for regulated industries like healthcare. Provyx is built exclusively for healthcare provider data with NPI verification, taxonomy code segmentation, and pay-per-record pricing. We deliver in days, not weeks, with no annual contracts."},
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
                <p class="hero__subtitle">Practice data, owner contacts, and provider intelligence for 40+ healthcare specialties. NPI-verified. Delivered in days, not weeks. No annual contracts.</p>
                <div class="hero__buttons">
                    <a href="/contact/" class="btn btn--primary btn--lg">Get Provider Data</a>
                    <a href="/providers/" class="btn btn--secondary btn--lg">Browse Specialties</a>
                </div>
                <div class="pain-stats">
                    <div class="pain-stat"><span class="pain-stat__number">2.4M+</span><span class="pain-stat__label">Provider Records</span></div>
                    <div class="pain-stat"><span class="pain-stat__number">40+</span><span class="pain-stat__label">Specialties</span></div>
                    <div class="pain-stat"><span class="pain-stat__number">Days</span><span class="pain-stat__label">Not Weeks</span></div>
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
                        <h3 class="problem-card__title">$15K+ Annual Contracts for Bad Data</h3>
                        <p class="problem-card__text">ZoomInfo starts at $15K/year. Definitive Healthcare at $25K+. Both lock you into annual contracts with auto-renewal traps and 10-30% price hikes. And you still get stale provider contacts with bounce rates over 15%.</p>
                    </div>
                    <div class="problem-card">
                        <div class="problem-card__icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9.172 16.172a4 4 0 0 1 5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0z"/></svg></div>
                        <h3 class="problem-card__title">Generic Vendors Don't Get Healthcare</h3>
                        <p class="problem-card__text">You can't filter by NPI taxonomy code in ZoomInfo. Apollo isn't even built for regulated industries. Healthcare provider data requires healthcare-specific infrastructure, not a generic B2B database with healthcare bolted on.</p>
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
                        <p class="service-card__text">Practice details, owner names, business phone, website, and LinkedIn profile for healthcare providers. NPI-verified against the CMS registry.</p>
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
                        <tr><td>Healthcare is one of 50+ industries</td><td>Built exclusively for healthcare</td></tr>
                        <tr><td>No NPI verification</td><td>Every record verified against NPI registry</td></tr>
                        <tr><td>Can't filter by taxonomy code</td><td>Full taxonomy code segmentation</td></tr>
                        <tr><td>Annual contracts starting at $15,000</td><td>Pay per record. Cancel anytime.</td></tr>
                        <tr><td>60-day cancellation windows</td><td>No lock-in. No auto-renewal traps.</td></tr>
                        <tr><td>$22K+ for CRM integration add-ons</td><td>CSV, Excel, or API. No hidden fees.</td></tr>
                    </tbody>
                </table>
            </div>
        </section>

        <section class="section section--fit">
            <div class="container">
                <div class="section__header">
                    <h2 class="section__title">Who It's For</h2>
                </div>
                <div class="fit-grid">
                    <div class="fit-card fit-card--for">
                        <div class="fit-card__icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M19.428 15.428a2 2 0 0 0-1.022-.547l-2.387-.477a6 6 0 0 0-2.038 0l-2.387.477a2 2 0 0 0-1.022.547M8 11V7a4 4 0 1 1 8 0v4m-9 4h10a2 2 0 0 1 2 2v3a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2z"/></svg></div>
                        <h3 class="fit-card__title">Medical Device Sales</h3>
                        <p class="fit-card__text">Territory reps who need to find clinics, identify decision-makers, and know what technology practices already use.</p>
                    </div>
                    <div class="fit-card fit-card--for">
                        <div class="fit-card__icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2z"/></svg></div>
                        <h3 class="fit-card__title">Healthcare SaaS & Health IT</h3>
                        <p class="fit-card__text">EHR, practice management, and patient engagement companies prospecting practices by specialty and tech stack.</p>
                    </div>
                    <div class="fit-card fit-card--for">
                        <div class="fit-card__icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M11 5.882V19.24a1.76 1.76 0 0 1-3.417.592l-2.147-6.15M18 13a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm-1.5-3h.01M5.436 13.683A4.001 4.001 0 0 1 3 10V7a4 4 0 0 1 4-4h9"/></svg></div>
                        <h3 class="fit-card__title">Healthcare Marketing Agencies</h3>
                        <p class="fit-card__text">Agencies running campaigns for dental, med spa, and chiropractic clients who need targeted provider lists.</p>
                    </div>
                    <div class="fit-card fit-card--for">
                        <div class="fit-card__icon"><svg width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M19 21V5a2 2 0 0 0-2-2H7a2 2 0 0 0-2 2v16m14 0H5m14 0h2m-16 0H3m5-10h.01M12 11h.01M8 15h.01M12 15h.01M16 11h.01M16 15h.01"/></svg></div>
                        <h3 class="fit-card__title">Pharmaceutical Sales</h3>
                        <p class="fit-card__text">Reps who need prescriber data by specialty and territory, without paying $15K+ for a platform they barely use.</p>
                    </div>
                </div>
                <div class="fit-not">
                    <p class="fit-not__text"><strong>Not for you?</strong> If you have a $100K+ annual data budget and a 3-year Definitive Healthcare contract, we're probably not your platform. We built Provyx for teams that want healthcare provider data without the enterprise bloat.</p>
                </div>
            </div>
        </section>

        <section class="section section--alt">
            <div class="container">
                <div class="testimonial">
                    <p class="testimonial__quote">"I've been looking for a healthcare data provider for 3 years, and I finally found one."</p>
                    <p class="testimonial__author">Colin, Division Sales Manager, Medical Devices</p>
                </div>
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
        description="Healthcare provider data across 40+ specialties. Practice details, owner contacts, NPI verification. Delivered in days. No annual contracts. Pay per record.",
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
                <p>We built Provyx because healthcare provider data requires healthcare-specific infrastructure. NPI verification. Taxonomy code segmentation. Practice-level intelligence that goes beyond name and email. Continuous verification because provider information changes constantly.</p>

                <h2>Our Approach</h2>
                <p>We source data from public registries (CMS NPI Registry, state licensing boards), commercial databases, and proprietary web intelligence. Every record is verified against multiple sources before it enters our database. We don't scrape and dump. We build verified provider profiles with the data points that matter for B2B outreach.</p>
                <ul>
                    <li>NPI-verified provider records across 40+ specialties</li>
                    <li>Practice details, owner contacts, LinkedIn profiles</li>
                    <li>Practice-level data: size, location, technology, ownership</li>
                    <li>Continuous verification to catch moves, closures, and staff changes</li>
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
        description="Provyx builds healthcare provider databases for B2B teams. NPI-verified contacts across 40+ specialties. No annual contracts.",
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
                        <p>Use the form and we'll get back to you within one business day.</p>
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
        {"question": "What's included in each record?",
         "answer": "Every record includes practice name, address, business phone, website URL, owner or decision-maker name, NPI number, taxonomy codes, and LinkedIn profile. Growth plans add practice firmographics and technology detection."},
        {"question": "Can I get a sample before purchasing?",
         "answer": "Yes. We provide a free sample of 25-50 records matched to your target criteria so you can validate data quality before committing to a purchase."},
        {"question": "Do you offer email or mobile phone data?",
         "answer": "Yes. Direct email and mobile phone enrichment are available as add-ons. Contact us for enrichment pricing based on your volume and match rate requirements."},
        {"question": "How fast can I get my data?",
         "answer": "Most orders ship within a few business days. We routinely turn around 10,000+ records in a single day for standard specialties and geographies. Custom requests with unusual filtering criteria may take longer."},
        {"question": "What if I need a specialty or geography you don't cover?",
         "answer": "Contact us. We can build custom datasets for specialties or regions outside our standard coverage."},
    ]

    extra_schema = get_breadcrumb_schema(breadcrumbs)

    body = f'''
        <section class="page-hero section">
            <div class="container">
                {get_breadcrumb_html(breadcrumbs)}
                <h1 class="page-hero__title">Simple, Transparent Pricing</h1>
                <p class="page-hero__subtitle">Pay per record. No annual contracts. Delivered in days, not weeks.</p>
            </div>
        </section>

        <section class="section">
            <div class="container">
                <div class="pricing-grid">
                    <div class="pricing-card">
                        <h3 class="pricing-card__name">Starter</h3>
                        <div class="pricing-card__price">$750</div>
                        <div class="pricing-card__period">one-time purchase</div>
                        <ul class="pricing-card__features">
                            <li>Up to 1,000 provider records</li>
                            <li>Practice name, address, business phone</li>
                            <li>Owner / decision-maker name</li>
                            <li>NPI number and taxonomy codes</li>
                            <li>Website URL and LinkedIn profile</li>
                            <li>CSV or Excel delivery</li>
                            <li>Delivered in days, not weeks</li>
                        </ul>
                        <a href="/contact/" class="btn btn--primary" style="width:100%">Get Started</a>
                    </div>
                    <div class="pricing-card pricing-card--featured">
                        <h3 class="pricing-card__name">Growth</h3>
                        <div class="pricing-card__price">$2,500</div>
                        <div class="pricing-card__period">5,000 records</div>
                        <ul class="pricing-card__features">
                            <li>Up to 5,000 provider records</li>
                            <li>Everything in Starter</li>
                            <li>Practice firmographics</li>
                            <li>Technology detection</li>
                            <li>Volume pricing at $0.50/record</li>
                            <li>Delivered in days, not weeks</li>
                            <li>Dedicated support</li>
                        </ul>
                        <a href="/contact/" class="btn btn--primary" style="width:100%">Contact Us</a>
                    </div>
                    <div class="pricing-card">
                        <h3 class="pricing-card__name">Enterprise</h3>
                        <div class="pricing-card__price">Custom</div>
                        <div class="pricing-card__period">10,000+ records</div>
                        <ul class="pricing-card__features">
                            <li>10,000+ provider records</li>
                            <li>Everything in Growth</li>
                            <li>API access</li>
                            <li>Custom enrichment fields</li>
                            <li>Ongoing data refresh</li>
                            <li>SLA and priority support</li>
                        </ul>
                        <a href="/contact/" class="btn btn--secondary" style="width:100%">Talk to Sales</a>
                    </div>
                </div>
                <div style="margin-top:2rem;padding:1.5rem 2rem;background:var(--color-bg-secondary);border-radius:var(--radius-md);border-left:4px solid var(--color-teal)">
                    <p style="margin:0;color:var(--color-text-secondary);font-size:0.9375rem"><strong style="color:var(--color-text-primary)">Need verified email or mobile?</strong> Direct email and mobile phone enrichment available as add-ons. <a href="/contact/">Contact us</a> for enrichment pricing based on your volume.</p>
                </div>
            </div>
        </section>

{generate_faq_html(faqs, heading="Pricing FAQ")}
{generate_cta_section()}'''

    html = get_page_wrapper(
        title="Pricing",
        description="Provyx healthcare provider data pricing starting at $0.50/record. Practice data, owner contacts, NPI verification. No annual contracts. Delivered in days.",
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
                <p>You may request access to, correction of, or deletion of any personal information we hold about you. To make a request, <a href="/contact/">contact us through our form</a>.</p>

                <h2>Contact</h2>
                <p>For privacy-related questions, <a href="/contact/">reach out through our contact page</a>.</p>
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
                <p>For questions about these terms, <a href="/contact/">reach out through our contact page</a>.</p>
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
    # ======================================================================
    # 1. PROVIDER CONTACT DATA
    # ======================================================================
    {
        "slug": "provider-contact-data",
        "title": "Verified Healthcare Provider Contact Data Lists",
        "short_title": "Provider Contact Data",
        "subtitle": (
            "Direct-dial phone numbers, verified practice addresses, NPI records, "
            "and decision-maker names for healthcare providers across the United States."
        ),
        "meta_description": (
            "Verified healthcare provider contact data: direct phone numbers, practice "
            "addresses, NPI records, and decision-maker names. Multi-source verified."
        ),
        "outbound_links": [
            {"url": "https://npiregistry.cms.hhs.gov/", "text": "CMS NPI Registry"},
            {"url": "https://nppes.cms.hhs.gov/", "text": "NPPES Data Dissemination"},
        ],
        # --- Section: The Problem ---
        "problem_heading": "Why Provider Contact Data Breaks Outbound Campaigns",
        "problem_body": (
            "Your sales team pulls a list of orthopedic surgeons in Texas. "
            "They start dialing. Half the numbers ring to a hospital switchboard. "
            "A quarter go to fax machines. The rest hit voicemails for providers who "
            "left that practice two years ago. Meanwhile, the mailers your marketing team "
            "sent last month are sitting in a pile at an address the practice vacated in 2022.\n\n"
            "This isn't a hypothetical. It's the default experience when you rely on a single "
            "data source for healthcare provider contact intelligence. The CMS "
            '<a href="https://npiregistry.cms.hhs.gov/">NPI Registry</a> is a solid starting '
            "point, but it only captures what providers self-report during enrollment and "
            "revalidation. Providers aren't required to update their phone numbers when they "
            "change, and many don't. State licensing boards carry different contact details "
            "than commercial databases, and neither one tells you who actually makes purchasing "
            "decisions at a group practice.\n\n"
            "Bad contact data doesn't just waste time. It inflates your cost per acquisition, "
            "tanks sender reputation when emails bounce, and burns through your SDR team's "
            "morale. If you're selling into healthcare, the accuracy of your provider contact "
            "data is the single biggest variable in whether outbound works or doesn't."
        ),
        # --- Section: What's Included ---
        "included_heading": "What's in a Provyx Provider Contact Record",
        "included_features": [
            {
                "name": "Practice Name and Business Address",
                "icon": "building",
                "description": (
                    "Every record includes the full legal practice name and a USPS-standardized "
                    "business address. We differentiate between the practice location where "
                    "patients are seen and the mailing address used for correspondence, because "
                    "they're often different. For multi-site practices, we map each location "
                    "separately so you know exactly which office your contact works from. "
                    "Addresses are verified against postal records quarterly."
                ),
            },
            {
                "name": "Business Phone, Fax, and Website",
                "icon": "phone",
                "description": (
                    "We provide the main business phone line, fax number, and practice website URL "
                    "for each record. Phone numbers are validated against carrier databases to "
                    "confirm they're active and correctly classified as landline, VoIP, or mobile. "
                    "Fax numbers are tested for connectivity. Website URLs are checked for live "
                    "status. If a phone number routes to a call center or answering service rather "
                    "than the practice directly, we flag that in the record."
                ),
            },
            {
                "name": "Owner and Decision-Maker Identification",
                "icon": "user",
                "description": (
                    "Knowing the practice exists isn't enough. You need to know who runs it. We "
                    "identify practice owners, office managers, and clinical directors using a "
                    "combination of state business registration records, NPI enumeration data, and "
                    "web intelligence. For solo practices, the provider is usually the decision-maker. "
                    "For group practices and multi-location organizations, we identify the "
                    "administrative and clinical leadership separately. Each contact includes their "
                    "name, title, and role classification."
                ),
            },
            {
                "name": "NPI Number, Taxonomy Codes, and LinkedIn Profile",
                "icon": "id-card",
                "description": (
                    "Every provider record is anchored to their National Provider Identifier, which "
                    "serves as a unique, permanent key for matching across data systems. We include "
                    "primary and secondary "
                    '<a href="https://taxonomy.nucc.org/">NUCC taxonomy codes</a> '
                    "so you can filter by exact specialty and subspecialty. Where available, we also "
                    "match providers to their LinkedIn profiles using our proprietary identity "
                    "resolution process that cross-references NPI data, name, location, and "
                    "specialty to confirm the match."
                ),
            },
        ],
        "included_addons": (
            "Optional add-ons include verified direct email addresses and mobile phone numbers. "
            "Direct emails bypass the info@ inbox and reach the provider or administrator personally. "
            "Mobile numbers are sourced from commercial consumer databases and validated for "
            "ownership before delivery. Both add-ons are priced separately and available on request."
        ),
        # --- Section: How We Source This Data ---
        "sourcing_heading": "How We Source and Verify Provider Contact Data",
        "sourcing_body": (
            "We start with the "
            '<a href="https://nppes.cms.hhs.gov/">NPPES data dissemination files</a>, '
            "which contain every active NPI record in the United States. That gives us the "
            "baseline: provider name, enumeration type, taxonomy, and self-reported address. "
            "From there, we layer in data from state medical licensing boards, state business "
            "registrations, commercial phone and address databases, and our own web scraping "
            "infrastructure.\n\n"
            "Each data field goes through a multi-source verification process. When two or more "
            "independent sources agree on a phone number or address, we mark that field as "
            "verified. When sources conflict, we flag the discrepancy and use recency signals "
            "to determine which value is most likely current. Phone numbers are validated "
            "against real-time carrier lookups. Addresses are standardized through USPS APIs. "
            "Email addresses are checked for deliverability before they're added to any record.\n\n"
            "The full contact database is refreshed on a rolling 90-day cycle. High-priority "
            "records, like providers in fast-growing specialties or regions with high turnover, "
            "get refreshed more frequently."
        ),
        # --- Section: Who Uses This Data ---
        "users_heading": "Who Uses Provider Contact Data",
        "users_body": (
            '<strong>Healthcare SaaS sales teams</strong> use provider contact data to build '
            "targeted outbound lists by specialty and geography. If you're selling EHR software "
            "to independent primary care practices in the Southeast, you need direct phone "
            'numbers and decision-maker names, not hospital switchboards. '
            'See our <a href="/for/health-tech-companies">health tech</a> page for more.\n\n'
            "<strong>Medical device and pharmaceutical reps</strong> rely on accurate practice "
            "addresses and provider names to plan territory routes and identify new accounts. "
            "Stale address data means wasted windshield time. Updated contact records mean "
            'more meetings per day. Check our <a href="/for/medical-device-companies">medical device</a> solutions.\n\n'
            "<strong>Healthcare staffing agencies</strong> use provider contact intelligence to "
            "reach practice managers who make hiring decisions for locum tenens and permanent "
            "placement roles. Reaching the right person on the first call shortens the sales cycle "
            "dramatically.\n\n"
            "<strong>Managed care organizations</strong> need current provider contact data for "
            "network adequacy reporting and provider directory maintenance. Outdated directories "
            "create regulatory risk and patient frustration."
        ),
        # --- Section: Data Quality ---
        "quality_heading": "Data Quality and Accuracy",
        "quality_body": (
            "We don't claim 100% accuracy because that's not realistic in a dataset of this "
            "size and velocity. Providers move, retire, change phone numbers, and merge practices "
            "constantly. What we do commit to is transparency about our verification status.\n\n"
            "Every field in a provider contact record carries a confidence indicator: verified "
            "(multi-source confirmed), unverified (single source), or flagged (sources conflict). "
            "Our overall verified rate across the full database sits above 85% for core fields "
            "like practice address and business phone. Direct emails and mobile numbers carry "
            "lower confidence rates because they change more often. We publish our methodology "
            "and refresh timelines so you can make informed decisions about how to use the data."
        ),
        # --- Section: FAQs ---
        "faqs": [
            {
                "question": "How often is provider contact data updated?",
                "answer": (
                    "The full database is refreshed on a rolling 90-day cycle. We pull updated "
                    "NPPES files weekly and run phone and address validation monthly. High-churn "
                    "specialties and regions get priority in our refresh queue. If you find a "
                    "stale record, you can flag it and we'll re-verify within five business days."
                ),
            },
            {
                "question": "What's the difference between the base record and the add-ons?",
                "answer": (
                    "The base record includes practice name, business address, business phone, "
                    "fax, website, NPI number, taxonomy codes, decision-maker name, and LinkedIn "
                    "profile where available. Add-ons are direct email addresses and mobile phone "
                    "numbers, which are priced separately because they require additional sourcing "
                    "and validation steps."
                ),
            },
            {
                "question": "Can I get contact data for a specific specialty or region?",
                "answer": (
                    "Yes. You can filter by any combination of taxonomy code, state, city, zip code, "
                    "practice size, and other criteria. If you need a tightly scoped list, our "
                    "custom list building service will handle the filtering and quality checks for "
                    "you. Most filtered lists are delivered within three to five business days."
                ),
            },
            {
                "question": "How do you handle providers who work at multiple locations?",
                "answer": (
                    "We create separate location records for each practice site and link them to the "
                    "provider's NPI. If a cardiologist practices at both a hospital outpatient clinic "
                    "and an independent office, you'll see both addresses with clear primary and "
                    "secondary designations. This prevents duplicate outreach and helps you target "
                    "the right location."
                ),
            },
        ],
        # --- Related links ---
        "related_services": [
            "practice-location-data",
            "social-profiles",
            "custom-list-building",
        ],
        "related_provider_categories": [
            "primary-care-physicians",
            "specialists",
            "dentists",
        ],
    },

    # ======================================================================
    # 2. PRACTICE LOCATION DATA
    # ======================================================================
    {
        "slug": "practice-location-data",
        "title": "Geocoded Healthcare Practice Location Intelligence",
        "short_title": "Practice Location Data",
        "subtitle": (
            "Geocoded practice addresses, multi-site mapping, and location type classification "
            "for every NPI-registered provider in the United States."
        ),
        "meta_description": (
            "Geocoded healthcare practice location data with lat/long coordinates, multi-site mapping, "
            "and practice vs mailing address differentiation. Updated quarterly."
        ),
        "outbound_links": [
            {"url": "https://npiregistry.cms.hhs.gov/", "text": "CMS NPI Registry"},
            {"url": "https://nppes.cms.hhs.gov/", "text": "NPPES Data Dissemination"},
        ],
        "problem_heading": "Why Practice Location Data Is Harder Than It Looks",
        "problem_body": (
            "You'd think addresses would be the easy part. They're not. The NPI Registry contains "
            "two address fields per provider: a practice location address and a mailing address. "
            "For roughly 40% of records, these are different. The mailing address might be a "
            "billing company in another state. The practice address might be a hospital campus "
            "with no suite number. Neither address tells you whether the provider is still "
            "physically seeing patients at that location.\n\n"
            "It gets worse for multi-location providers. A dermatology group with five offices "
            "might list their corporate headquarters as the NPI practice address while patients "
            "are actually seen across town. An urgent care chain might have twenty locations but "
            "only one Type 2 organizational NPI, making it impossible to distinguish sites from "
            'the <a href="https://npiregistry.cms.hhs.gov/">NPI Registry</a> alone.\n\n'
            "For territory planning, network adequacy analysis, and location-based marketing, "
            "approximate addresses aren't good enough. You need geocoded coordinates, site-level "
            "differentiation, and a clear picture of which locations are active patient care sites "
            "versus administrative offices. That's what practice location intelligence provides."
        ),
        "included_heading": "What's in a Provyx Practice Location Record",
        "included_features": [
            {
                "name": "Geocoded Addresses with Latitude and Longitude",
                "icon": "map-pin",
                "description": (
                    "Every practice address is geocoded to rooftop-level precision where possible, "
                    "with latitude and longitude coordinates included in every record. This allows "
                    "you to run radius searches, build heat maps, calculate drive-time polygons, "
                    "and perform spatial analysis without a separate geocoding step. Addresses that "
                    "can only be geocoded to the zip centroid level are flagged so you know the "
                    "precision level of each coordinate pair."
                ),
            },
            {
                "name": "Type 1 and Type 2 NPI Classification",
                "icon": "layers",
                "description": (
                    "We classify every location by its association with Type 1 (individual provider) "
                    "and Type 2 (organizational) NPI records. This matters because an individual "
                    "physician might practice at a location registered under a group's Type 2 NPI. "
                    "Our records link both, so you can see all individual providers associated with "
                    "an organizational location and all locations associated with an individual "
                    "provider. This cross-referencing is sourced from "
                    '<a href="https://nppes.cms.hhs.gov/">NPPES</a> files and supplemented '
                    "with claims-derived affiliation data."
                ),
            },
            {
                "name": "Multi-Location Mapping with Primary and Secondary Designation",
                "icon": "git-branch",
                "description": (
                    "For providers and organizations with multiple practice sites, we map every "
                    "known location and designate which is the primary site. Primary designation "
                    "is based on the address listed on the NPI record, supplemented by web presence "
                    "signals and appointment availability data. Secondary sites are listed with their "
                    "own full address records. This is critical for medical device reps planning "
                    "routes and for payers validating network directory listings at the site level."
                ),
            },
            {
                "name": "Practice Address vs Mailing Address Differentiation",
                "icon": "mail",
                "description": (
                    "We maintain separate fields for practice location address and mailing address, "
                    "and we flag records where these differ. About 40% of NPI records have mismatched "
                    "addresses. If you're sending physical mail, you need the mailing address. If "
                    "you're dispatching a field rep, you need the practice address. Conflating the "
                    "two is one of the most common and costly mistakes in healthcare location data. "
                    "Our records make the distinction explicit."
                ),
            },
        ],
        "included_addons": (
            "Additional location enrichment includes hours of operation, wheelchair accessibility "
            "flags, and public transit proximity scores where available from business listing sources."
        ),
        "sourcing_heading": "How We Build Practice Location Intelligence",
        "sourcing_body": (
            "The foundation is the NPPES data dissemination, which provides the self-reported "
            "practice and mailing addresses for every NPI record. We supplement this with "
            "commercial business listing databases, Google Places data, and state facility "
            "licensing records to validate and enrich each address.\n\n"
            "Geocoding is handled through a multi-provider approach. We run addresses through "
            "two independent geocoding services and compare results. When both agree within a "
            "tight tolerance, we use the higher-precision result. When they diverge, we "
            "flag the record for manual review. This catches common geocoding failures like "
            "addresses that resolve to the wrong side of the street or to a zip centroid "
            "instead of the actual building.\n\n"
            "Multi-location mapping draws from organizational NPI records, practice website "
            "analysis, and appointment booking platforms. If a practice website lists three "
            "office locations, we capture all three and link them to the appropriate NPI records."
        ),
        "users_heading": "Who Uses Practice Location Data",
        "users_body": (
            "<strong>Medical device sales teams</strong> use geocoded location data for territory "
            "planning and route optimization. Knowing the exact coordinates of every orthopedic "
            "practice within a 50-mile radius, along with which are primary vs satellite sites, "
            'makes daily route planning far more efficient. See our <a href="/for/medical-device-companies">'
            "medical device solutions</a>.\n\n"
            "<strong>Health plan network teams</strong> rely on practice location intelligence for "
            "network adequacy reporting. CMS and state regulators require health plans to demonstrate "
            "that members have access to providers within specific distance and drive-time thresholds. "
            "Accurate geocoded data makes those calculations possible.\n\n"
            "<strong>Healthcare real estate developers</strong> use location data to identify "
            "underserved areas and site new facilities. Understanding where existing practices "
            "cluster and where gaps exist drives development strategy. Overlaying provider "
            "density maps with population data reveals opportunities that spreadsheets alone "
            "can't surface.\n\n"
            "<strong>Healthcare marketers</strong> use location data to build geo-targeted campaigns "
            'that reach providers in specific zip codes, counties, or MSAs. Visit our <a href="/for/health-tech-companies">'
            "health tech page</a> for more."
        ),
        "quality_heading": "Data Quality and Accuracy",
        "quality_body": (
            "Practice addresses are the most stable field in our database. Providers move less "
            "often than they change phone numbers. That said, we still see roughly 8-12% of "
            "addresses change annually due to practice relocations, closures, and mergers.\n\n"
            "Every address goes through USPS standardization to correct formatting issues like "
            "misspelled street names, missing suite numbers, and inconsistent abbreviations. "
            "Geocoding accuracy is validated against known reference points. Records where the "
            "geocoded location doesn't match the state or zip code in the address are flagged "
            "for review. We also cross-check against commercial business listing databases to "
            "confirm that the address corresponds to an active healthcare practice and not a "
            "vacant building or unrelated business. "
            "The location database is refreshed quarterly, with NPPES-sourced "
            "updates applied weekly."
        ),
        "faqs": [
            {
                "question": "What's the geocoding precision level?",
                "answer": (
                    "Most addresses are geocoded to rooftop-level precision, meaning the coordinates "
                    "point to the specific building. When rooftop geocoding isn't possible, typically "
                    "for rural addresses or new construction, we fall back to parcel or street-level "
                    "precision. Every record includes a precision indicator so you know the accuracy "
                    "level of the coordinates."
                ),
            },
            {
                "question": "How do you handle practices that have closed?",
                "answer": (
                    "We check NPI deactivation records, business registration status, and web presence "
                    "signals to identify closed practices. Deactivated NPI records are flagged, and "
                    "addresses associated with confirmed closures are marked as inactive. We don't "
                    "remove them from the database because historical location data is valuable for "
                    "market analysis, but they won't appear in active-only data pulls."
                ),
            },
            {
                "question": "Can I get location data in a GIS-compatible format?",
                "answer": (
                    "Yes. We deliver location data in CSV with lat/long columns by default, which "
                    "imports directly into any GIS tool. We can also provide GeoJSON or Shapefile "
                    "formats on request. If you're integrating with a mapping platform like Mapbox "
                    "or Google Maps, the default CSV format with WGS84 coordinates works without "
                    "any conversion."
                ),
            },
            {
                "question": "How many practice locations are in the database?",
                "answer": (
                    "The database covers over 3.5 million practice location records linked to active "
                    "NPI registrations across all 50 states and territories. This includes both Type 1 "
                    "individual provider locations and Type 2 organizational locations. The count "
                    "fluctuates as new providers enumerate and others deactivate, but we track every "
                    "active NPI in the NPPES system."
                ),
            },
        ],
        "related_services": [
            "provider-contact-data",
            "practice-firmographics",
            "custom-list-building",
        ],
        "related_provider_categories": [
            "primary-care-physicians",
            "urgent-care-centers",
            "hospitals",
        ],
    },

    # ======================================================================
    # 3. TECHNOLOGY DETECTION
    # ======================================================================
    {
        "slug": "technology-detection",
        "title": "Healthcare Practice Technology Stack Detection",
        "short_title": "Technology Detection",
        "subtitle": (
            "Identify which EHR, practice management, billing, and telehealth systems "
            "healthcare practices use so you can target, time, and tailor your outreach."
        ),
        "meta_description": (
            "Detect EHR systems, practice management software, and telehealth platforms "
            "used by healthcare practices. Web signals and public records."
        ),
        "outbound_links": [
            {"url": "https://www.healthit.gov/", "text": "ONC Health IT"},
            {"url": "https://npiregistry.cms.hhs.gov/", "text": "CMS NPI Registry"},
        ],
        "problem_heading": "Why Selling Into Healthcare Without Technology Data Is Guesswork",
        "problem_body": (
            "If you sell software or services to healthcare practices, the first question your "
            "sales team needs answered isn't \"who's the decision-maker\" or \"what's their budget.\" "
            "It's \"what are they currently using?\" A practice running Epic isn't a prospect for "
            "your standalone EHR. A clinic that just signed a three-year contract with athenahealth "
            "isn't switching next quarter. But a practice still running an on-premise legacy system "
            "from a vendor that's been acquired twice? That's a live opportunity.\n\n"
            "Without technology detection data, your team is cold-calling blind. They're pitching "
            "billing solutions to practices that already use the same platform. They're offering "
            "patient portal integrations to clinics whose EHR doesn't support them. They're wasting "
            "discovery calls on qualification questions that data could have answered before the "
            "dial.\n\n"
            "The challenge is that healthcare practices don't publish their tech stacks. There's no "
            "central registry of which clinic uses which EHR. The "
            '<a href="https://www.healthit.gov/">ONC certified health IT product list</a> tells you '
            "what's certified, not what's installed. You need a different approach to get this data."
        ),
        "included_heading": "What Technology Data We Detect",
        "included_features": [
            {
                "name": "EHR System Identification",
                "icon": "monitor",
                "description": (
                    "We identify the electronic health record system in use at each practice, covering "
                    "major platforms like Epic, Cerner (now Oracle Health), athenahealth, eClinicalWorks, "
                    "Greenway Health, NextGen, DrChrono, and dozens of smaller vendors. Our detection "
                    "covers both cloud-hosted and on-premise deployments. For larger organizations with "
                    "multiple EHR instances, we identify the primary system and note secondary or "
                    "departmental systems where our signals are strong enough to confirm."
                ),
            },
            {
                "name": "Practice Management Software Detection",
                "icon": "settings",
                "description": (
                    "Practice management software handles scheduling, registration, and administrative "
                    "workflows. Many practices use a PM system from a different vendor than their EHR. "
                    "We detect standalone PM platforms like Kareo, AdvancedMD, and CareCloud, as well "
                    "as integrated EHR/PM suites. Knowing whether a practice uses an integrated or "
                    "best-of-breed stack tells you a lot about their buying patterns and openness to "
                    "new point solutions."
                ),
            },
            {
                "name": "Patient Engagement and Telehealth Platforms",
                "icon": "video",
                "description": (
                    "We detect patient-facing technology including telehealth platforms (Doxy.me, "
                    "Teladoc, Amwell), patient communication tools (Klara, Luma Health, Relatient), "
                    "online scheduling platforms, and patient portal solutions. These signals are "
                    "particularly valuable if you sell competing or complementary patient engagement "
                    "tools. Post-pandemic telehealth adoption varies widely by specialty and practice "
                    "size, and our detection data quantifies that adoption at the practice level."
                ),
            },
            {
                "name": "Billing and Revenue Cycle Management Systems",
                "icon": "dollar-sign",
                "description": (
                    "We identify billing software and revenue cycle management vendors including "
                    "Waystar, Availity, Trizetto, Kareo Billing, and AdvancedMD Billing. We also "
                    "flag practices that appear to use outsourced billing services based on web "
                    "signals and job posting patterns. This data is valuable for RCM vendors, "
                    "clearinghouse companies, and anyone selling into the financial operations "
                    "side of healthcare practices."
                ),
            },
        ],
        "included_addons": (
            "Enhanced technology intelligence includes estimated contract renewal windows based "
            "on install date signals, and technology change alerts that notify you when a practice "
            "switches vendors."
        ),
        "sourcing_heading": "How We Detect Healthcare Technology Stacks",
        "sourcing_body": (
            "Technology detection in healthcare requires a fundamentally different approach than "
            "detecting website technologies like CMS platforms or analytics tools. Healthcare "
            "software often runs behind logins with no public-facing signals. Our methodology "
            "combines four signal sources.\n\n"
            "First, we analyze practice websites for technology signatures: embedded widgets, "
            "patient portal links, booking platform integrations, and JavaScript references that "
            "identify specific vendor platforms. Second, we monitor healthcare job postings, "
            "which frequently name the EHR or PM system candidates will need experience with. "
            "Third, we track vendor directories, partner listings, and case studies published "
            "by technology companies that name their customers. Fourth, we incorporate ONC "
            "certified health IT data and state-level health information exchange participation "
            "records.\n\n"
            "No single source covers every practice. The combination of all four gives us "
            "technology signals for the majority of practices with five or more providers. "
            "Each technology detection is linked to the practice's "
            '<a href="https://npiregistry.cms.hhs.gov/">NPI record</a>, so you can cross-reference '
            "technology data with provider contact information and firmographics. "
            "Solo practices are harder to detect because they have smaller web footprints and "
            "fewer job postings."
        ),
        "users_heading": "Who Uses Technology Detection Data",
        "users_body": (
            "<strong>Healthcare software companies</strong> use technology detection to identify "
            "prospects running competing or complementary platforms. If you sell a patient intake "
            "solution that integrates with athenahealth but not Epic, you can target only "
            "athenahealth practices and skip the rest. That kind of precision transforms conversion "
            'rates. See our <a href="/for/health-tech-companies">health tech solutions</a>.\n\n'
            "<strong>EHR and PM vendors</strong> use competitive intelligence from technology "
            "detection to understand market share by region, specialty, and practice size. This "
            "informs product positioning, pricing strategy, and M&A decisions.\n\n"
            "<strong>Healthcare consultants and advisory firms</strong> use technology data to "
            "benchmark their clients against peers and identify modernization opportunities. "
            'When a practice is running outdated systems, consultants can quantify the gap.\n\n'
            "<strong>Investors evaluating healthcare IT companies</strong> use technology adoption "
            "data to validate vendor claims about market penetration and growth trajectory. "
            "When a vendor says they have 10,000 customers, technology detection data provides "
            "an independent check on that number."
        ),
        "quality_heading": "Data Quality and Accuracy",
        "quality_body": (
            "Technology detection is inherently probabilistic. We're inferring technology usage "
            "from indirect signals, not reading it from a definitive registry. Our confidence "
            "levels reflect that reality.\n\n"
            "For major EHR platforms at medium and large practices, our detection accuracy is "
            "above 80%. For niche PM tools at small practices, accuracy drops because the signals "
            "are weaker. Every technology detection record carries a confidence score: high (multiple "
            "independent signals), medium (single strong signal), or low (inferred from indirect "
            "evidence). We recommend filtering to medium and high confidence for outbound campaigns "
            "and using all confidence levels for market analysis. Technology data is refreshed "
            "on a quarterly cycle."
        ),
        "faqs": [
            {
                "question": "How many EHR vendors can you detect?",
                "answer": (
                    "We currently detect over 80 EHR and PM vendors, covering the vast majority "
                    "of the installed base in the US healthcare market. This includes all top-20 "
                    "vendors by market share and extends to specialty-specific systems used in "
                    "dental, optometry, behavioral health, and other verticals. If you need "
                    "detection for a specific vendor not on our list, contact us and we can "
                    "usually add it."
                ),
            },
            {
                "question": "Can technology detection tell me when a contract is up for renewal?",
                "answer": (
                    "Not directly. We don't have access to contract terms. However, we can provide "
                    "estimated install date ranges based on when we first detected the technology "
                    "at a given practice. If you know a vendor's typical contract length, you can "
                    "estimate renewal windows from our install date signal. Our enhanced tier also "
                    "includes technology change alerts that notify you when a practice switches."
                ),
            },
            {
                "question": "Does technology detection work for solo practices?",
                "answer": (
                    "Coverage is lower for solo practices because they generate fewer web signals "
                    "and rarely post job listings that name their technology. Our detection rate "
                    "for solo practices is roughly 40-50%, compared to 75-85% for group practices "
                    "with five or more providers. We're transparent about this limitation because "
                    "we'd rather you know the coverage rate upfront than discover gaps later."
                ),
            },
            {
                "question": "How current is the technology detection data?",
                "answer": (
                    "Technology data is refreshed quarterly. Healthcare practices don't switch "
                    "EHR systems frequently. The average EHR contract runs three to seven years, "
                    "so quarterly detection catches most transitions. For practices going through "
                    "an active technology change, there may be a lag of one to two quarters before "
                    "the new system appears in our data."
                ),
            },
        ],
        "related_services": [
            "provider-contact-data",
            "practice-firmographics",
            "custom-list-building",
        ],
        "related_provider_categories": [
            "primary-care-physicians",
            "dentists",
            "behavioral-health-providers",
        ],
    },

    # ======================================================================
    # 4. SOCIAL PROFILES
    # ======================================================================
    {
        "slug": "social-profiles",
        "title": "Healthcare Provider Social Media Profile Matching",
        "short_title": "Social Profiles",
        "subtitle": (
            "Matched LinkedIn profiles for physicians and administrators, plus Facebook "
            "and Instagram pages for healthcare practices, verified against NPI records."
        ),
        "meta_description": (
            "Matched LinkedIn profiles for physicians, plus Facebook and Instagram pages "
            "for healthcare practices. Verified against NPI records."
        ),
        "outbound_links": [
            {"url": "https://npiregistry.cms.hhs.gov/", "text": "CMS NPI Registry"},
            {"url": "https://www.bls.gov/ooh/healthcare/", "text": "BLS Healthcare Occupations"},
        ],
        "problem_heading": "Why Finding Healthcare Providers on Social Media Is Unreliable",
        "problem_body": (
            "Search for a physician on LinkedIn and you'll likely find three profiles with the "
            "same name, two of them with incomplete information, and none of them definitively "
            "matched to the provider you're actually looking for. Search for a dental practice "
            "on Facebook and you might find an abandoned page from 2018 alongside an active one "
            "with a slightly different name.\n\n"
            "Healthcare providers are notoriously inconsistent on social media. Many physicians "
            "have LinkedIn profiles they created years ago and never updated. Practice Facebook "
            "pages get created by marketing agencies, then management changes and nobody maintains "
            "them. Instagram is only actively used by certain specialties, primarily dental, "
            "dermatology, plastic surgery, and aesthetics.\n\n"
            "If you're running LinkedIn outreach campaigns, sending Facebook ads targeted at "
            "practice pages, or researching providers before sales calls, you need social profiles "
            "that are actually matched to the right person and practice. Guessing based on name "
            "alone leads to embarrassing misdirected outreach. The "
            '<a href="https://npiregistry.cms.hhs.gov/">NPI Registry</a> gives you the verified identity '
            "anchor. We use it to match providers to their social profiles with confidence."
        ),
        "included_heading": "What Social Profile Data We Provide",
        "included_features": [
            {
                "name": "LinkedIn Profiles for Physicians and Administrators",
                "icon": "linkedin",
                "description": (
                    "We match healthcare providers and practice administrators to their LinkedIn "
                    "profiles using a multi-factor identity resolution process. We cross-reference "
                    "the provider's NPI-registered name, specialty, and practice location against "
                    "LinkedIn profile data to confirm matches. Each match carries a confidence "
                    "score. High-confidence matches are verified against at least three data points. "
                    "This is critical for account-based selling where you need the right profile "
                    "before sending a connection request."
                ),
            },
            {
                "name": "Practice Facebook Business Pages",
                "icon": "facebook",
                "description": (
                    "We identify and link Facebook business pages for healthcare practices, "
                    "distinguishing between active pages with recent posts and dormant pages that "
                    "haven't been updated in over six months. For multi-location practices, we "
                    "match location-specific pages where they exist. Active page status matters "
                    "because targeting ads at a dormant page wastes your budget. We also capture "
                    "follower counts and posting frequency as engagement signals."
                ),
            },
            {
                "name": "Practice Instagram Accounts",
                "icon": "instagram",
                "description": (
                    "Instagram presence varies dramatically by specialty. Dental practices, "
                    "dermatologists, plastic surgeons, and med spas invest heavily in Instagram "
                    "for before-and-after content. Primary care and internal medicine practices "
                    "rarely maintain active accounts. We identify practice Instagram handles and "
                    "flag which ones are actively posting. This data is most valuable for companies "
                    "selling marketing services, patient engagement tools, or aesthetic products "
                    "to visually oriented specialties."
                ),
            },
            {
                "name": "Profile Matching Methodology and Confidence Scoring",
                "icon": "check-circle",
                "description": (
                    "Every social profile match is scored on a three-tier confidence system. High "
                    "confidence means the NPI name, specialty, and practice location all match the "
                    "social profile. Medium confidence means two of three match. Low confidence "
                    "means only the name matches, which is common for providers with common names. "
                    "We recommend using high-confidence matches for direct outreach and medium "
                    "confidence for research purposes. Low-confidence matches are included for "
                    "completeness but should be verified manually before use."
                ),
            },
        ],
        "included_addons": (
            "Enhanced social intelligence includes provider Twitter/X handles, YouTube channels "
            "for practices producing video content, and social engagement metrics for LinkedIn "
            "activity scoring."
        ),
        "sourcing_heading": "How We Match Providers to Social Profiles",
        "sourcing_body": (
            "Matching healthcare providers to social media profiles is fundamentally an identity "
            "resolution problem. We start with the provider's verified identity from NPI records: "
            "their full name, credentials, specialty, and practice location. We then search for "
            "matching profiles across LinkedIn, Facebook, and Instagram using a combination of "
            "API access, web scraping, and manual verification for ambiguous matches.\n\n"
            "The matching algorithm weights multiple factors. An exact name match alone isn't "
            "enough because there are over 20 physicians named \"Michael Smith\" in most large "
            "metros. We require at least two corroborating data points: specialty listed on the "
            "profile, practice name in the work history, geographic match, or credential match. "
            "This multi-factor approach keeps our false positive rate below 5% for high-confidence "
            "matches.\n\n"
            "Social profiles are refreshed semi-annually. LinkedIn profiles change infrequently. "
            "Facebook and Instagram accounts are checked for active status during each refresh "
            "cycle. New providers added to the NPI registry are queued for social matching within "
            "60 days of enumeration."
        ),
        "users_heading": "Who Uses Social Profile Data",
        "users_body": (
            "<strong>Sales development teams</strong> use LinkedIn profile data for personalized "
            "outreach. Knowing a physician's career history, published articles, and professional "
            "interests before the first touchpoint makes your outreach relevant instead of generic. "
            'See our <a href="/for/health-tech-companies">health tech page</a> for use cases.\n\n'
            "<strong>Healthcare marketing agencies</strong> use Facebook and Instagram data to "
            "build targeted ad campaigns. Running Facebook ads to practices with active, engaged "
            "pages delivers better results than spraying ads across every practice in a zip code. "
            "Instagram data helps identify practices already investing in visual content, which "
            "signals receptiveness to marketing services.\n\n"
            "<strong>Recruiting firms</strong> use LinkedIn data to identify physicians and "
            "administrators who might be open to new opportunities. Profile completeness and "
            "activity level serve as proxies for engagement with career content.\n\n"
            "<strong>Conference and event organizers</strong> in healthcare use social profiles "
            "to identify potential speakers, panelists, and attendees who are active in their "
            "professional communities online. According to the "
            '<a href="https://www.bls.gov/ooh/healthcare/">BLS healthcare occupations data</a>, '
            "healthcare is one of the fastest-growing employment sectors, and connecting with "
            "these professionals through the right channels matters."
        ),
        "quality_heading": "Data Quality and Accuracy",
        "quality_body": (
            "Social profile matching has an inherent tension between coverage and accuracy. We "
            "could match more providers if we lowered our confidence thresholds, but that would "
            "increase false positives and erode trust in the data.\n\n"
            "Our current coverage rate for LinkedIn is approximately 55-65% of actively practicing "
            "physicians. For administrators and office managers, coverage is lower at around 35-40% "
            "because many don't maintain LinkedIn profiles. Facebook business page coverage for "
            "practices is approximately 50%. Instagram coverage is highest for aesthetic specialties "
            "(70%+) and lowest for hospital-based specialties (under 15%). We publish these "
            "coverage rates so you can set realistic expectations for campaign reach."
        ),
        "faqs": [
            {
                "question": "How do you avoid matching the wrong provider on LinkedIn?",
                "answer": (
                    "We require at least two corroborating data points beyond name alone. "
                    "These include specialty, practice name, geographic location, and credentials. "
                    "For common names, we apply stricter thresholds and may require three or more "
                    "matching factors. Matches that don't meet our confidence threshold are excluded "
                    "from the high-confidence tier rather than included with a wrong match."
                ),
            },
            {
                "question": "Is social profile data available for non-physician providers?",
                "answer": (
                    "Yes. We match social profiles for nurse practitioners, physician assistants, "
                    "dentists, optometrists, psychologists, physical therapists, and other provider "
                    "types with active NPI registrations. LinkedIn coverage tends to be lower for "
                    "non-physician providers, but Facebook and Instagram coverage for their practices "
                    "is comparable to physician practices."
                ),
            },
            {
                "question": "Can I use social profile data for automated LinkedIn outreach?",
                "answer": (
                    "We provide the data. How you use it is up to you and subject to each platform's "
                    "terms of service. LinkedIn has strict rules about automated outreach and connection "
                    "requests. We recommend using our data for research and personalization rather than "
                    "automated bulk messaging, which risks account restrictions regardless of data quality."
                ),
            },
            {
                "question": "How often are social profiles updated?",
                "answer": (
                    "Social profile data is refreshed semi-annually. LinkedIn profiles don't change "
                    "frequently for most healthcare providers. Facebook and Instagram accounts are "
                    "checked for active status and updated engagement metrics during each cycle. "
                    "If you need a more current check on a specific set of profiles, we can run "
                    "an on-demand refresh for an additional fee."
                ),
            },
        ],
        "related_services": [
            "provider-contact-data",
            "custom-list-building",
            "technology-detection",
        ],
        "related_provider_categories": [
            "dentists",
            "dermatologists",
            "plastic-surgeons",
        ],
    },

    # ======================================================================
    # 5. PRACTICE FIRMOGRAPHICS
    # ======================================================================
    {
        "slug": "practice-firmographics",
        "title": "Healthcare Practice Firmographic Data and Analytics",
        "short_title": "Practice Firmographics",
        "subtitle": (
            "Provider headcount, revenue estimates, years in business, and ownership classification "
            "for healthcare practices across all specialties."
        ),
        "meta_description": (
            "Healthcare practice firmographic data: provider headcount, revenue estimates, "
            "ownership type, and years in business. Updated quarterly."
        ),
        "outbound_links": [
            {"url": "https://npiregistry.cms.hhs.gov/", "text": "CMS NPI Registry"},
            {"url": "https://www.bls.gov/ooh/healthcare/", "text": "BLS Healthcare Occupations"},
        ],
        "problem_heading": "Why Practice Size and Ownership Data Changes Your Sales Strategy",
        "problem_body": (
            "A solo family medicine practice and a 40-provider multi-specialty group both show "
            "up as \"primary care\" in a basic provider database. But they buy differently, budget "
            "differently, and make decisions through completely different processes. Selling the "
            "same way to both is a waste of your team's time and your prospect's patience.\n\n"
            "The solo practitioner makes purchasing decisions over lunch. The group practice has "
            "a committee, an IT director, and a six-month evaluation cycle. A hospital-owned "
            "clinic has no local purchasing authority at all. A private equity-backed dental "
            "service organization might buy for 200 locations at once but route everything "
            "through a corporate procurement team in another state.\n\n"
            "Without practice firmographic data, your team can't segment by practice size, "
            "can't prioritize by revenue potential, and can't adjust messaging for ownership "
            "type. You're forcing a one-size-fits-all approach on a market that's anything but "
            "uniform. According to the "
            '<a href="https://www.bls.gov/ooh/healthcare/">Bureau of Labor Statistics</a>, '
            "healthcare employs over 16 million people across dramatically different organizational "
            "structures, from single-provider offices to integrated health systems."
        ),
        "included_heading": "What's in a Practice Firmographic Record",
        "included_features": [
            {
                "name": "Provider Headcount Estimates",
                "icon": "users",
                "description": (
                    "We estimate the number of licensed providers associated with each practice "
                    "location using NPI affiliation data, web presence analysis, and commercial "
                    "business databases. Headcount is broken into physicians, advanced practice "
                    "providers (NPs and PAs), and total clinical staff where signals are available. "
                    "This allows you to segment by practice size: solo, small group (2-5 providers), "
                    "medium group (6-20), and large group (21+). Size segmentation is the single "
                    "most predictive variable for deal size and sales cycle length."
                ),
            },
            {
                "name": "Revenue Range Modeling",
                "icon": "trending-up",
                "description": (
                    "We model annual revenue ranges for each practice using a combination of "
                    "specialty, provider headcount, geographic cost-of-living adjustments, and "
                    "payer mix indicators. Revenue estimates are expressed as ranges (e.g., $1M-$2.5M) "
                    "rather than precise figures because practice revenue isn't publicly reported. "
                    "The model is calibrated against known revenue data from practices that report "
                    "financials through business credit agencies. Revenue estimates help you "
                    "prioritize high-value targets and size your proposals appropriately."
                ),
            },
            {
                "name": "Years in Business",
                "icon": "clock",
                "description": (
                    "We capture the original NPI enumeration date from "
                    '<a href="https://npiregistry.cms.hhs.gov/">NPPES records</a> '
                    "and supplement it with state business registration dates to estimate how "
                    "long a practice has been operating. Newer practices (under two years) have "
                    "different technology needs, buying urgency, and budget constraints than "
                    "established practices. A practice that's been open for six months is actively "
                    "buying everything. A practice that's been running for 15 years has entrenched "
                    "vendor relationships that are harder to displace."
                ),
            },
            {
                "name": "Ownership Classification",
                "icon": "briefcase",
                "description": (
                    "We classify each practice into ownership categories: solo practitioner, "
                    "independent group, hospital-owned or health system-affiliated, private "
                    "equity-backed, dental service organization (DSO), management services "
                    "organization (MSO), federally qualified health center (FQHC), or government-"
                    "operated. Ownership type determines who makes purchasing decisions and how "
                    "long that process takes. PE-backed practices and DSOs often centralize "
                    "procurement, which means larger deals but longer cycles. Independent groups "
                    "make decisions faster but buy for fewer locations."
                ),
            },
        ],
        "included_addons": (
            "Enhanced firmographic data includes payer mix estimates (commercial vs Medicare vs "
            "Medicaid share), patient volume indicators, and practice growth trajectory based on "
            "headcount changes over time."
        ),
        "sourcing_heading": "How We Build Firmographic Profiles",
        "sourcing_body": (
            "Practice firmographic data is assembled from multiple sources because no single "
            "database captures all of it. NPI records provide the provider count and enumeration "
            "date. State business registrations provide incorporation date, registered agent, and "
            "sometimes ownership entity names. Commercial business credit databases contribute "
            "employee count ranges and revenue estimates. SEC filings and private equity deal "
            "announcements help us classify ownership type for PE-backed practices.\n\n"
            "Revenue modeling uses a specialty-adjusted algorithm. A solo orthopedic surgeon "
            "generates significantly more revenue than a solo family medicine physician, and our "
            "model accounts for that. Geographic adjustments factor in regional reimbursement "
            "rates and cost-of-living differences. The model is validated quarterly against a "
            "holdout set of practices with known financials.\n\n"
            "Ownership classification is the most labor-intensive field. We combine automated "
            "signals (web mentions of parent companies, PE portfolio listings) with manual "
            "research for ambiguous cases. DSO and MSO identification is particularly tricky "
            "because many operate under local brand names that don't reference the parent entity."
        ),
        "users_heading": "Who Uses Practice Firmographic Data",
        "users_body": (
            '<strong>Enterprise sales teams at health tech companies</strong> use firmographics '
            "to segment their total addressable market by practice size, revenue, and ownership "
            "type. This drives territory assignment, quota setting, and account prioritization. "
            'See our <a href="/for/health-tech-companies">health tech page</a> for more.\n\n'
            "<strong>Private equity firms and healthcare investors</strong> use firmographic data "
            "to identify acquisition targets, map competitive landscapes, and perform due diligence "
            "on platform investments. Knowing which practices in a market are independent vs "
            "already PE-owned shapes roll-up strategy.\n\n"
            "<strong>Group purchasing organizations</strong> use practice size and ownership data "
            "to identify potential members and estimate purchasing volume for contract negotiations.\n\n"
            "<strong>Healthcare consultants</strong> use firmographics to benchmark practices "
            "against peers of similar size, specialty, and ownership type. Revenue and headcount "
            'data enables apples-to-apples comparisons. Visit our <a href="/for/consulting-firms">'
            "consulting page</a> for details."
        ),
        "quality_heading": "Data Quality and Accuracy",
        "quality_body": (
            "Firmographic data is inherently estimated. Unlike contact data, where a phone number "
            "is either right or wrong, a revenue estimate is a modeled range and a headcount is "
            "an approximation based on NPI affiliation signals.\n\n"
            "Our provider headcount estimates are within one provider of the actual count for about "
            "70% of practices, based on validation against practices that self-report size on their "
            "websites. Revenue ranges are calibrated to capture the actual figure within the stated "
            "range for approximately 65% of practices. Ownership classification accuracy exceeds "
            "85% for the major categories (solo, group, hospital-owned). PE-backed and DSO "
            "classification is harder and sits around 75% accuracy. We update firmographic data "
            "quarterly."
        ),
        "faqs": [
            {
                "question": "How do you estimate practice revenue when it's not publicly reported?",
                "answer": (
                    "We use a specialty-adjusted model that factors in provider headcount, geographic "
                    "reimbursement rates, payer mix indicators, and practice type. The model is "
                    "calibrated against practices with known financials from business credit agencies. "
                    "Revenue is expressed as a range rather than a point estimate to reflect the "
                    "inherent uncertainty. The model performs best for single-specialty practices and "
                    "less reliably for large multi-specialty groups."
                ),
            },
            {
                "question": "Can you identify which practices are private equity-backed?",
                "answer": (
                    "Yes, but with caveats. We identify PE-backed practices by tracking PE deal "
                    "announcements, portfolio company listings, and parent entity ownership chains. "
                    "Large platform acquisitions are well-documented and we capture those reliably. "
                    "Smaller add-on acquisitions are harder to detect because they often aren't "
                    "publicly announced. Our PE classification covers the majority of large PE-backed "
                    "platforms in dental, dermatology, ophthalmology, and orthopedics."
                ),
            },
            {
                "question": "What's the difference between a DSO and an MSO in your classification?",
                "answer": (
                    "A dental service organization (DSO) typically owns the non-clinical assets and "
                    "employs the administrative staff of dental practices. A management services "
                    "organization (MSO) provides similar administrative services to medical practices. "
                    "In our classification, DSO is used for dental-specific roll-ups and MSO for "
                    "medical practice management entities. Both indicate centralized procurement "
                    "and decision-making."
                ),
            },
            {
                "question": "How often does ownership classification change?",
                "answer": (
                    "Ownership changes happen constantly through acquisitions, mergers, and divestitures. "
                    "We scan for ownership changes quarterly through PE deal monitoring, news alerts, "
                    "and business registration updates. The pace of PE-backed consolidation in "
                    "healthcare means that practices we classified as independent six months ago may "
                    "now be part of a platform. Quarterly updates catch most transitions, but there's "
                    "always a lag."
                ),
            },
        ],
        "related_services": [
            "provider-contact-data",
            "technology-detection",
            "custom-list-building",
        ],
        "related_provider_categories": [
            "dentists",
            "dermatologists",
            "orthopedic-surgeons",
        ],
    },

    # ======================================================================
    # 6. CUSTOM LIST BUILDING
    # ======================================================================
    {
        "slug": "custom-list-building",
        "title": "Custom Healthcare Provider List Building Service",
        "short_title": "Custom List Building",
        "subtitle": (
            "Targeted provider lists built to your specifications. Filter by specialty, geography, "
            "practice size, technology, and ownership type. Delivered in 3-5 business days."
        ),
        "meta_description": (
            "Custom healthcare provider list building filtered by specialty, geography, "
            "practice size, technology, and ownership. Delivered in 3-5 days."
        ),
        "outbound_links": [
            {"url": "https://npiregistry.cms.hhs.gov/", "text": "CMS NPI Registry"},
            {"url": "https://www.bls.gov/ooh/healthcare/", "text": "BLS Healthcare Occupations"},
        ],
        "problem_heading": "Why Off-the-Shelf Provider Lists Underperform",
        "problem_body": (
            "You can download the entire NPPES file from "
            '<a href="https://npiregistry.cms.hhs.gov/">CMS</a> for free. '
            "It contains every NPI-registered provider in the country. And it's almost useless "
            "for targeted outreach in its raw form.\n\n"
            "The NPPES file has no phone numbers, no emails, no practice size indicators, and no "
            "technology data. It doesn't tell you whether a provider is actively practicing or "
            "retired. It doesn't distinguish between a provider's primary practice and a "
            "hospital where they have privileges but never see patients. The taxonomy codes are "
            "self-reported and sometimes inaccurate. The addresses haven't been validated against "
            "anything.\n\n"
            "Generic provider lists from data vendors aren't much better. They're built for broad "
            "use, which means they include everyone and filter for no one. You end up paying for "
            "tens of thousands of records you don't need and still missing the specific segment "
            "you do need. A list of \"dermatologists in Florida\" isn't useful if half of them are "
            "retired, a third are hospital-employed with no purchasing authority, and you really "
            "needed Mohs surgeons within 30 miles of Tampa who use a specific EHR."
        ),
        "included_heading": "How Custom List Building Works",
        "included_features": [
            {
                "name": "Granular Filtering Across All Data Fields",
                "icon": "filter",
                "description": (
                    "Custom lists can be filtered by any combination of the data fields in our "
                    "database: specialty and subspecialty (using "
                    '<a href="https://taxonomy.nucc.org/">NUCC taxonomy codes</a>), '
                    "geography (state, metro area, county, zip code, or radius from a point), "
                    "practice size (solo, small group, medium group, large group), technology "
                    "stack (specific EHR, PM system, or billing platform), ownership type "
                    "(independent, hospital-owned, PE-backed, DSO/MSO), and years in business. "
                    "You define the criteria. We build the list."
                ),
            },
            {
                "name": "Consultation and Criteria Definition",
                "icon": "message-circle",
                "description": (
                    "Every custom list starts with a consultation where we review your ideal "
                    "customer profile and translate it into specific data filters. This matters "
                    "because the criteria you think you want and the criteria that actually "
                    "produce the best list aren't always the same. If you ask for \"primary care "
                    "practices with 5+ providers\" but your real target is practices large enough "
                    "to have a dedicated office manager, we'll help you refine that. The goal is "
                    "a list that converts, not just a list that's long."
                ),
            },
            {
                "name": "Quality Check and Deduplication",
                "icon": "check-square",
                "description": (
                    "Before delivery, every custom list goes through a quality assurance process. "
                    "We deduplicate against multiple match keys (NPI, phone, address, practice name) "
                    "to remove records that appear multiple times due to data source overlap. We "
                    "validate that all records meet the specified filter criteria. We flag any "
                    "records with low confidence scores on key fields so you know where the data "
                    "is strong and where it's approximate. You get a quality summary report with "
                    "every delivery."
                ),
            },
            {
                "name": "Flexible Delivery Formats",
                "icon": "download",
                "description": (
                    "Custom lists are delivered in the format that fits your workflow. Standard "
                    "delivery is a CSV or Excel file sent via secure link. If you prefer direct "
                    "integration, we can push data through our API to your CRM, marketing automation "
                    "platform, or data warehouse. For recurring needs, we set up scheduled deliveries "
                    "that automatically refresh and deliver updated lists on a monthly or quarterly "
                    "cadence. Most one-time lists are delivered within three to five business days."
                ),
            },
        ],
        "included_addons": (
            "For ongoing prospecting, we offer managed list services where we deliver fresh, "
            "deduplicated lists on a recurring schedule based on your standing criteria. This "
            "eliminates the need to re-request similar lists every month."
        ),
        "sourcing_heading": "How We Build Your Custom List",
        "sourcing_body": (
            "Custom lists draw from the same multi-source database that powers all our data "
            "products. The foundation is the NPPES file, enriched with commercial contact data, "
            "technology detection, firmographic modeling, and social profile matching. When you "
            "define your criteria, we query across all of these layers simultaneously.\n\n"
            "The process follows four steps. First, we consult with you to define the criteria "
            "and set expectations on list size and data coverage. Second, we build the initial "
            "list by running your filters against our database. Third, we run quality checks "
            "including deduplication, field validation, and confidence scoring. Fourth, we "
            "deliver the final list in your preferred format with a quality summary.\n\n"
            "For complex criteria that combine multiple filters, the initial query may return "
            "a smaller list than expected. When that happens, we'll tell you before delivery "
            "and discuss whether to relax certain filters to increase volume. We'd rather "
            "deliver a smaller, accurate list than a larger list padded with marginal matches."
        ),
        "users_heading": "Who Uses Custom List Building",
        "users_body": (
            "<strong>Sales teams launching new territories or verticals</strong> use custom lists "
            "to build their initial prospecting pipeline from scratch. Instead of spending weeks "
            "researching and compiling targets, they get a vetted, filtered list delivered in days. "
            'See our <a href="/for/health-tech-companies">health tech solutions</a> for more.\n\n'
            "<strong>Marketing teams running ABM campaigns</strong> need tightly defined target "
            "lists that match their ideal customer profile. Custom lists provide the foundation "
            "for account-based marketing programs that target specific practice types with "
            "personalized messaging.\n\n"
            "<strong>Event and conference organizers</strong> use custom lists to build invitation "
            "lists for regional or specialty-specific events. A custom list of orthopedic surgeons "
            "within 100 miles of a conference venue, filtered by practice size, is more actionable "
            "than a generic attendee database. The "
            '<a href="https://www.bls.gov/ooh/healthcare/">BLS projects</a> continued growth in '
            "healthcare occupations, which means more providers to reach and more reasons to "
            "reach them precisely.\n\n"
            '<strong>Consulting firms</strong> conducting market assessments use custom lists to '
            "quantify market size and segment composition for specific geographies and specialties. "
            'Visit our <a href="/for/consulting-firms">consulting page</a> for details.'
        ),
        "quality_heading": "Data Quality and Delivery Standards",
        "quality_body": (
            "Every custom list comes with a quality summary that reports the total record count, "
            "the number of verified vs unverified records by field, the deduplication rate, and "
            "any records that were excluded during QA. This transparency lets you assess the "
            "list's suitability before you use it.\n\n"
            "Our target is to deliver lists where at least 80% of core contact fields (name, "
            "address, phone) are multi-source verified. For enrichment fields like technology "
            "detection and revenue estimates, coverage rates vary depending on the target segment. "
            "If coverage on a specific field falls below a useful threshold for your list, we'll "
            "flag that during the consultation phase rather than delivering a list that disappoints."
        ),
        "faqs": [
            {
                "question": "How long does it take to get a custom list?",
                "answer": (
                    "Most custom lists are delivered within three to five business days from "
                    "criteria confirmation. Simple lists with standard filters (specialty plus "
                    "geography) are often ready in one to two days. Complex lists that combine "
                    "multiple enrichment filters, like technology plus firmographic criteria, may "
                    "take the full five days because they require additional quality checks."
                ),
            },
            {
                "question": "Is there a minimum list size?",
                "answer": (
                    "There's no hard minimum. We've built lists as small as 50 records for "
                    "hyper-targeted ABM campaigns and as large as 500,000+ for national outreach "
                    "programs. Pricing is based on record count and the number of enrichment fields "
                    "included, so small lists are affordable. If your criteria produce fewer results "
                    "than expected, we'll discuss options before charging anything."
                ),
            },
            {
                "question": "Can I get a sample before committing to a full list?",
                "answer": (
                    "Yes. We provide a sample of 50-100 records based on your criteria so you can "
                    "evaluate data quality, field coverage, and relevance before ordering the full "
                    "list. The sample is free and typically delivered within one business day. We "
                    "want you to see the data quality firsthand rather than taking our word for it."
                ),
            },
            {
                "question": "What formats can I receive the list in?",
                "answer": (
                    "Standard delivery formats are CSV and Excel, sent via a secure download link. "
                    "We also support direct API delivery to CRMs like Salesforce and HubSpot, and "
                    "data warehouse integrations for teams that prefer programmatic access. If you "
                    "need a format not listed here, let us know during the consultation and we'll "
                    "accommodate it if we can."
                ),
            },
        ],
        "related_services": [
            "provider-contact-data",
            "practice-location-data",
            "practice-firmographics",
        ],
        "related_provider_categories": [
            "primary-care-physicians",
            "dentists",
            "specialists",
        ],
    },
]


def _build_related_links_html(svc):
    """Return HTML block with links to related /services/ and /providers/ pages."""
    lines = []
    lines.append('<section class="related-links">')
    lines.append("  <h2>Related Data Products</h2>")
    lines.append("  <ul>")
    for slug in svc.get("related_services", []):
        # Find the matching service for its short_title
        matched = next((s for s in SERVICES if s["slug"] == slug), None)
        label = matched["short_title"] if matched else slug.replace("-", " ").title()
        lines.append(f'    <li><a href="/services/{slug}">{label}</a></li>')
    lines.append("  </ul>")

    provider_cats = svc.get("related_provider_categories", [])
    if provider_cats:
        lines.append("  <h3>Related Provider Categories</h3>")
        lines.append("  <ul>")
        for cat in provider_cats:
            label = cat.replace("-", " ").title()
            lines.append(f'    <li><a href="/providers/{cat}">{label}</a></li>')
        lines.append("  </ul>")

    lines.append("</section>")
    return "\n".join(lines)


def build_service_page(svc):
    """
    Generate a single service page with all required sections:
    1. Hero (page-hero with h1 + subtitle)
    2. The Problem (h2)
    3. What's Included (h2 + feature cards)
    4. How We Source This Data (h2)
    5. Who Uses This Data (h2)
    6. Data Quality (h2)
    7. FAQ section
    8. Related links
    9. CTA section
    """

    slug = svc["slug"]
    url = f"/services/{slug}"
    canonical = f"{BASE_URL}{url}"

    # -- Breadcrumbs --
    breadcrumbs = [
        {"name": "Home", "url": "/"},
        {"name": "Services", "url": "/services"},
        {"name": svc["short_title"], "url": url},
    ]
    breadcrumb_schema = get_breadcrumb_schema(breadcrumbs)
    breadcrumb_html = get_breadcrumb_html(breadcrumbs)

    # -- Outbound link references for schema --
    outbound_links = svc.get("outbound_links", [])

    # -- Hero --
    hero_html = f"""
<section class="page-hero">
  <div class="container">
    {breadcrumb_html}
    <h1>{svc['title']}</h1>
    <p class="subtitle">{svc['subtitle']}</p>
  </div>
</section>
"""

    # -- The Problem --
    problem_html = f"""
<section class="content-section">
  <div class="container">
    <h2>{svc['problem_heading']}</h2>
    {''.join(f'<p>{p.strip()}</p>' for p in svc['problem_body'].split(chr(10) + chr(10)) if p.strip())}
  </div>
</section>
"""

    # -- What's Included --
    features_cards = ""
    for feat in svc["included_features"]:
        features_cards += f"""
    <div class="feature-card">
      <div class="feature-icon"><i data-feather="{feat['icon']}"></i></div>
      <h3>{feat['name']}</h3>
      <p>{feat['description']}</p>
    </div>
"""

    addons_html = ""
    if svc.get("included_addons"):
        addons_html = f'<p class="addons-note"><strong>Add-ons:</strong> {svc["included_addons"]}</p>'

    included_html = f"""
<section class="content-section features-section">
  <div class="container">
    <h2>{svc['included_heading']}</h2>
    <div class="features-grid">
{features_cards}
    </div>
    {addons_html}
  </div>
</section>
"""

    # -- How We Source This Data --
    sourcing_paragraphs = "".join(
        f"<p>{p.strip()}</p>"
        for p in svc["sourcing_body"].split("\n\n")
        if p.strip()
    )
    sourcing_html = f"""
<section class="content-section">
  <div class="container">
    <h2>{svc['sourcing_heading']}</h2>
    {sourcing_paragraphs}
  </div>
</section>
"""

    # -- Who Uses This Data --
    users_paragraphs = "".join(
        f"<p>{p.strip()}</p>"
        for p in svc["users_body"].split("\n\n")
        if p.strip()
    )
    users_html = f"""
<section class="content-section">
  <div class="container">
    <h2>{svc['users_heading']}</h2>
    {users_paragraphs}
  </div>
</section>
"""

    # -- Data Quality --
    quality_paragraphs = "".join(
        f"<p>{p.strip()}</p>"
        for p in svc["quality_body"].split("\n\n")
        if p.strip()
    )
    quality_html = f"""
<section class="content-section">
  <div class="container">
    <h2>{svc['quality_heading']}</h2>
    {quality_paragraphs}
  </div>
</section>
"""

    # -- FAQ section --
    faq_html = generate_faq_html(svc["faqs"])

    # -- Related links --
    related_html = _build_related_links_html(svc)

    # -- CTA --
    cta_html = generate_cta_section()

    # -- Assemble page body --
    body = (
        hero_html
        + problem_html
        + included_html
        + sourcing_html
        + users_html
        + quality_html
        + f'\n<section class="content-section">\n  <div class="container">\n{faq_html}\n  </div>\n</section>\n'
        + f'\n<section class="content-section">\n  <div class="container">\n{related_html}\n  </div>\n</section>\n'
        + cta_html
    )

    # -- Wrap and write --
    page_html = get_page_wrapper(
        title=f"{svc['title']} | Provyx",
        description=svc["meta_description"],
        canonical_path=canonical,
        body_content=body,
        extra_schema=breadcrumb_schema,
    )

    write_page(f"services/{slug}/index.html", page_html)

    # Register in ALL_PAGES
    ALL_PAGES.append((f"/services/{slug}/", 0.8, "monthly"))


def build_services_index():
    """
    Build the /services/ index page with a card grid linking to each service.
    H1: 'Healthcare Provider Data Products & Services' (46 chars)
    """

    url = "/services"
    canonical = f"{BASE_URL}{url}"

    breadcrumbs = [
        {"name": "Home", "url": "/"},
        {"name": "Data Products & Services", "url": "/services"},
    ]
    breadcrumb_schema = get_breadcrumb_schema(breadcrumbs)
    breadcrumb_html = get_breadcrumb_html(breadcrumbs)

    meta_description = (
        "Explore Provyx healthcare provider data products: contact data, practice locations, "
        "technology detection, social profiles, and firmographics."
    )

    # Build service cards
    cards_html = ""
    for svc in SERVICES:
        cards_html += f"""
      <a href="/services/{svc['slug']}" class="service-card">
        <h3>{svc['short_title']}</h3>
        <p>{svc['subtitle']}</p>
      </a>
"""

    body = f"""
<section class="page-hero">
  <div class="container">
    {breadcrumb_html}
    <h1>Healthcare Provider Data Products and Services</h1>
    <p class="subtitle">
      Verified provider contact intelligence, practice location data, technology detection,
      social profiles, firmographic records, and custom-built lists. All sourced from public
      NPI registries, business listings, and commercial databases. All multi-source verified.
    </p>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <h2>Our Data Products</h2>
    <p>
      Every data product in our catalog starts with the
      <a href="https://npiregistry.cms.hhs.gov/">CMS NPI Registry</a> as a foundation and
      layers in enrichment from commercial databases, web intelligence, and public records.
      You can purchase individual data products or combine them into a custom list tailored
      to your exact targeting criteria.
    </p>
    <div class="services-grid">
{cards_html}
    </div>
  </div>
</section>

<section class="content-section">
  <div class="container">
    <h2>How to Get Started</h2>
    <p>
      If you know which data product you need, visit the product page and request a sample.
      If you're not sure where to start, our team can help you define the right combination
      of data fields and filters for your use case. Most samples are delivered within one
      business day, and custom lists are ready in three to five business days.
    </p>
  </div>
</section>

{generate_cta_section()}
"""

    page_html = get_page_wrapper(
        title="Healthcare Provider Data Products and Services | Provyx",
        description=meta_description,
        canonical_path=canonical,
        body_content=body,
        extra_schema=breadcrumb_schema,
    )

    write_page("services/index.html", page_html)

    ALL_PAGES.append(("/services/", 0.9, "monthly"))


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
         "answer": f"We provide verified practice data and owner contacts for {len(cat_subtypes)} types of {cat_data['short'].lower()} providers, including practice details, NPI numbers, taxonomy codes, website, and LinkedIn profile. All records are verified against the CMS NPI Registry. Direct email and mobile enrichment available as add-ons."},
        {"question": f"How is {cat_data['short'].lower()} data different from generic provider databases?",
         "answer": f"Generic databases lump all healthcare providers together without understanding {cat_data['short'].lower()} specialty distinctions. We segment by specific provider subtypes, making it easy to target exactly the right {cat_data['short'].lower()} providers for your campaign."},
        {"question": f"How often is the {cat_data['short'].lower()} provider data updated?",
         "answer": f"Our {cat_data['short'].lower()} provider database is continuously verified against multiple sources. Provider contacts change frequently as staff turns over and practices relocate. Our verification process catches these changes to keep your outreach data current."},
        {"question": f"Can I get a custom {cat_data['short'].lower()} provider list?",
         "answer": f"Yes. We build custom lists filtered by specific {cat_data['short'].lower()} subtypes, geography, practice size, and other criteria. Contact us with your requirements and we'll put together a matched list."},
        {"question": f"What data fields are included for {cat_data['short'].lower()} providers?",
         "answer": "Every record includes practice name, address, business phone, website URL, owner or decision-maker name, NPI number, taxonomy codes, and LinkedIn profile. Growth plans add practice firmographics and technology detection. Direct email and mobile enrichment available as add-ons."},
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
         "answer": f"We provide verified practice data for {name_lower} including owner contacts, NPI details, taxonomy codes, practice addresses, website, and LinkedIn profile. Every record is verified against the CMS NPI Registry. Direct email and mobile enrichment available as add-ons."},
        {"question": f"How accurate is the {name_lower} contact data?",
         "answer": f"Our {name_lower} data is verified against multiple sources including the CMS NPI Registry, state licensing boards, and commercial databases. We continuously verify records to catch moves, closures, and contact changes."},
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

def build_icp_page(icp: dict) -> None:
    """Build a single ICP / audience page from its data dict and write to disk."""

    slug = icp["slug"]
    url_path = f"/for/{slug}/"
    canonical = f"{BASE_URL}{url_path}"

    # -- Breadcrumbs --
    breadcrumbs = [
        {"name": "Home", "url": f"{BASE_URL}/"},
        {"name": "Audiences", "url": f"{BASE_URL}/for/"},
        {"name": icp["h1"], "url": canonical},
    ]
    breadcrumb_schema = get_breadcrumb_schema(breadcrumbs)
    breadcrumb_html = get_breadcrumb_html(breadcrumbs)

    # -- FAQ HTML --
    faq_html = generate_faq_html(icp["faqs"])

    # -- CTA section --
    cta_html = generate_cta_section(
        title="Ready to Build Your List?",
        text="Tell us your target criteria and we'll put together a sample. No commitment, no annual contract.",
        button_text="Get a Sample List",
        button_href="/contact/",
    )

    # -- Related links --
    related_links_html = "".join(
        f'<li><a href="{link["url"]}">{link["text"]}</a></li>'
        for link in icp["related_links"]
    )

    # -- Assemble page body --
    body = f"""
    {breadcrumb_html}

    <!-- Hero -->
    <section class="page-hero">
      <div class="container">
        <h1>{icp["h1"]}</h1>
        <p class="subtitle">{icp["subtitle"]}</p>
      </div>
    </section>

    <!-- The Pain -->
    <section class="content-section">
      <div class="container">
        <h2>{icp["pain_heading"]}</h2>
        {icp["pain_content"]}
      </div>
    </section>

    <!-- How They Use Provyx -->
    <section class="content-section bg-light">
      <div class="container">
        <h2>{icp["use_heading"]}</h2>
        {icp["use_content"]}
      </div>
    </section>

    <!-- What Data You Get -->
    <section class="content-section">
      <div class="container">
        <h2>{icp["data_heading"]}</h2>
        {icp["data_content"]}
      </div>
    </section>

    <!-- How It Works -->
    <section class="content-section bg-light">
      <div class="container">
        <h2>{icp["how_heading"]}</h2>
        {icp["how_content"]}
      </div>
    </section>

    <!-- FAQ -->
    <section class="content-section">
      <div class="container">
        <h2>Frequently Asked Questions</h2>
        {faq_html}
      </div>
    </section>

    <!-- Related Links -->
    <section class="content-section bg-light">
      <div class="container">
        <h2>Related Resources</h2>
        <ul class="related-links">
          {related_links_html}
        </ul>
      </div>
    </section>

    <!-- CTA -->
    {cta_html}
    """

    # -- Wrap in full page template --
    page_html = get_page_wrapper(
        title=icp["title"],
        description=icp["meta_description"],
        canonical_path=f"/for/{slug}/",
        body_content=body,
        extra_schema=breadcrumb_schema,
    )

    # -- Register in ALL_PAGES and write --
    ALL_PAGES.append((f"/for/{slug}/", 0.7, "monthly"))

    write_page(f"for/{slug}/index.html", page_html)


def build_all_icp_pages() -> None:
    """Build every ICP audience page."""
    for icp in ICP_PAGES:
        build_icp_page(icp)


# =============================================================================
# PAGE GENERATORS - COMPARISON & ALTERNATIVE PAGES
# =============================================================================

def build_comparison_page(comp):
    """
    Build a single comparison page from a comparison data dict.

    Assumes the following are importable from the main build script:
        generate_faq_html, generate_cta_section, get_page_wrapper,
        write_page, BASE_URL, get_breadcrumb_schema, get_breadcrumb_html,
        ALL_PAGES
    """

    slug = comp["slug"]
    competitor = comp["competitor_name"]
    canonical = f"{BASE_URL}/compare/{slug}/"

    # -- Breadcrumbs --
    breadcrumb_items = [
        {"name": "Home", "url": f"{BASE_URL}/"},
        {"name": "Comparisons", "url": f"{BASE_URL}/compare/"},
        {"name": f"Provyx vs. {competitor}", "url": canonical},
    ]
    breadcrumb_schema = get_breadcrumb_schema(breadcrumb_items)
    breadcrumb_html = get_breadcrumb_html(breadcrumb_items)

    # -- FAQ schema --
    faq_schema_items = []
    for faq in comp["faqs"]:
        faq_schema_items.append({
            "@type": "FAQPage",
            "mainEntity": [{
                "@type": "Question",
                "name": faq["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["answer"],
                },
            }],
        })

    # -- Build comparison table HTML --
    table_rows_html = ""
    for label, competitor_val, provyx_val in comp["comparison_table_rows"]:
        table_rows_html += (
            f"<tr>"
            f"<td><strong>{label}</strong></td>"
            f"<td>{competitor_val}</td>"
            f"<td>{provyx_val}</td>"
            f"</tr>\n"
        )

    comparison_table_html = (
        f'<div class="comparison-table">\n'
        f"<table>\n"
        f"<thead>\n"
        f"<tr>"
        f"<th>Feature</th>"
        f"<th>{competitor}</th>"
        f"<th>Provyx</th>"
        f"</tr>\n"
        f"</thead>\n"
        f"<tbody>\n"
        f"{table_rows_html}"
        f"</tbody>\n"
        f"</table>\n"
        f"</div>\n"
    )

    # -- Build outbound links reference list --
    outbound_links_html = ""
    if comp.get("competitor_outbound_links"):
        links_li = "".join(
            f'<li><a href="{url}" target="_blank" rel="noopener">{text}</a></li>\n'
            for url, text in comp["competitor_outbound_links"]
        )
        outbound_links_html = (
            f'<div class="outbound-references">\n'
            f"<h4>Sources and References</h4>\n"
            f"<ul>\n{links_li}</ul>\n"
            f"</div>\n"
        )

    # -- Build related links HTML --
    related_links_html = ""
    if comp.get("related_links"):
        links_li = "".join(
            f'<li><a href="{link["url"]}">{link["text"]}</a></li>\n'
            for link in comp["related_links"]
        )
        related_links_html = (
            f'<section class="related-links">\n'
            f"<div class=\"container\">\n"
            f"<h2>Related Comparisons and Resources</h2>\n"
            f"<ul>\n{links_li}</ul>\n"
            f"</div>\n"
            f"</section>\n"
        )

    # -- Build FAQ HTML --
    faq_html = generate_faq_html(comp["faqs"])

    # -- Build CTA section --
    cta_html = generate_cta_section()

    # -- Build who-should-choose section --
    who_should_html = (
        f'<section class="content-section">\n'
        f"<div class=\"container\">\n"
        f"<h2>Who Should Choose What</h2>\n"
        f"<div class=\"scenario-list\">\n"
        f"<div class=\"scenario\">\n"
        f"<p>{comp['scenario_general_b2b']}</p>\n"
        f"</div>\n"
        f"<div class=\"scenario\">\n"
        f"<p>{comp['scenario_healthcare_specific']}</p>\n"
        f"</div>\n"
        f"<div class=\"scenario\">\n"
        f"<p>{comp['scenario_enterprise_budget']}</p>\n"
        f"</div>\n"
        f"</div>\n"
        f"</div>\n"
        f"</section>\n"
    )

    # -- Assemble full page body --
    page_body = f"""
<!-- Hero -->
<section class="page-hero">
    <div class="container">
        {breadcrumb_html}
        <h1>{comp["hero_headline"]}</h1>
        <p class="hero-subheadline">{comp["hero_subheadline"]}</p>
    </div>
</section>

<!-- Intro -->
<section class="content-section">
    <div class="container">
        {comp["intro"]}
    </div>
</section>

<!-- Quick Comparison Table -->
<section class="content-section">
    <div class="container">
        <h2>{competitor} vs. Provyx at a Glance</h2>
        {comparison_table_html}
    </div>
</section>

<!-- Deep Dive: Competitor -->
<section class="content-section">
    <div class="container">
        <h2>Deep Dive: {competitor}</h2>
        {comp["competitor_what_they_offer"]}
        {comp["competitor_pricing"]}
        {comp["competitor_shortcomings"]}
        {outbound_links_html}
    </div>
</section>

<!-- Deep Dive: Provyx -->
<section class="content-section">
    <div class="container">
        <h2>Deep Dive: Provyx</h2>
        {comp["provyx_what_delivers"]}
        {comp["provyx_healthcare_handling"]}
        {comp["provyx_pricing"]}
    </div>
</section>

<!-- Who Should Choose What -->
{who_should_html}

<!-- FAQ -->
<section class="content-section faq-section">
    <div class="container">
        <h2>Frequently Asked Questions</h2>
        {faq_html}
    </div>
</section>

<!-- Related Links -->
{related_links_html}

<!-- CTA -->
{cta_html}
"""

    # -- Wrap page and write --
    full_html = get_page_wrapper(
        title=comp["page_title"],
        description=comp["meta_description"],
        canonical_path=f"/compare/{slug}/",
        body_content=page_body,
        extra_schema=breadcrumb_schema,
    )

    write_page(f"compare/{slug}/index.html", full_html)

    # -- Register page in ALL_PAGES for sitemap --
    ALL_PAGES.append((f"/compare/{slug}/", 0.7, "monthly"))


def build_all_comparison_pages():
    """Build all comparison pages from the COMPARISONS list."""
    for comp in COMPARISONS:
        build_comparison_page(comp)


def build_alternative_page(alt):
    """Build a single alternative page from an ALTERNATIVES dict entry."""

    slug = alt["slug"]
    competitor = alt["competitor"]
    page_url = f"{BASE_URL}/alternative/{slug}/"

    # -- Breadcrumbs -------------------------------------------------------
    breadcrumb_items = [
        {"name": "Home", "url": BASE_URL + "/"},
        {"name": "Alternatives", "url": BASE_URL + "/alternative/"},
        {"name": f"{competitor} Alternative", "url": page_url},
    ]
    breadcrumb_schema = get_breadcrumb_schema(breadcrumb_items)
    breadcrumb_html = get_breadcrumb_html(breadcrumb_items)

    # -- FAQ schema --------------------------------------------------------
    faq_schema_items = "".join(
        f"""
        {{
            "@type": "Question",
            "name": "{faq['question']}",
            "acceptedAnswer": {{
                "@type": "Answer",
                "text": "{faq['answer']}"
            }}
        }}{"," if i < len(alt["faqs"]) - 1 else ""}"""
        for i, faq in enumerate(alt["faqs"])
    )

    faq_schema = f"""
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{faq_schema_items}
        ]
    }}
    </script>"""

    # -- Comparison table --------------------------------------------------
    comparison_rows_html = ""
    for row_label, competitor_val, provyx_val in alt["comparison_rows"]:
        comparison_rows_html += f"""
                    <tr>
                        <td><strong>{row_label}</strong></td>
                        <td>{competitor_val}</td>
                        <td>{provyx_val}</td>
                    </tr>"""

    comparison_table_html = f"""
        <section class="comparison-table-section">
            <div class="container">
                <h2>{alt["comparison_heading"]}</h2>
                <div class="table-responsive">
                    <table class="comparison-table">
                        <thead>
                            <tr>
                                <th>Feature</th>
                                <th>{competitor}</th>
                                <th>Provyx</th>
                            </tr>
                        </thead>
                        <tbody>{comparison_rows_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </section>"""

    # -- Related links section ---------------------------------------------
    related_links_items = ""
    for link in alt["related_links"]:
        related_links_items += f"""
                    <li><a href="{link['url']}">{link['label']}</a></li>"""

    related_links_html = f"""
        <section class="related-links-section">
            <div class="container">
                <h2>Related Resources</h2>
                <ul class="related-links-list">{related_links_items}
                </ul>
            </div>
        </section>"""

    # -- FAQ section -------------------------------------------------------
    faq_section_html = generate_faq_html(alt["faqs"])

    # -- CTA section -------------------------------------------------------
    cta_section_html = generate_cta_section(
        title=f"Ready to See How Provyx Compares to {competitor}?",
        text=(
            f"Request a free sample list for your specialty and geography. "
            f"Compare the data side-by-side with what you're getting from {competitor} today."
        ),
        button_text="Get a Free Sample List",
        button_href="/contact/",
    )

    # -- Assemble full page content ----------------------------------------
    page_content = f"""
    {breadcrumb_schema}
    {faq_schema}

    {breadcrumb_html}

    <!-- Hero -->
    <section class="page-hero alternative-hero">
        <div class="container">
            <h1>{alt["hero_h1"]}</h1>
            <p class="hero-subtitle">{alt["hero_subtitle"]}</p>
        </div>
    </section>

    <!-- Why Teams Look for an Alternative -->
    <section class="content-section why-switch-section">
        <div class="container">
            <h2>{alt["why_switch_heading"]}</h2>
            {alt["why_switch_body"]}
        </div>
    </section>

    <!-- What Healthcare Teams Actually Need -->
    <section class="content-section what-teams-need-section">
        <div class="container">
            <h2>{alt["what_teams_need_heading"]}</h2>
            {alt["what_teams_need_body"]}
        </div>
    </section>

    <!-- Comparison Table -->
    {comparison_table_html}

    <!-- How Provyx Works as an Alternative -->
    <section class="content-section how-it-works-section">
        <div class="container">
            <h2>{alt["how_it_works_heading"]}</h2>
            {alt["how_it_works_body"]}
        </div>
    </section>

    <!-- What Provyx Doesn't Do -->
    <section class="content-section limitations-section">
        <div class="container">
            <h2>{alt["limitations_heading"]}</h2>
            {alt["limitations_body"]}
        </div>
    </section>

    <!-- Who Switches to Provyx -->
    <section class="content-section who-switches-section">
        <div class="container">
            <h2>{alt["who_switches_heading"]}</h2>
            {alt["who_switches_body"]}
        </div>
    </section>

    <!-- Migration Guide -->
    <section class="content-section migration-section">
        <div class="container">
            <h2>{alt["migration_heading"]}</h2>
            {alt["migration_body"]}
        </div>
    </section>

    <!-- FAQ -->
    <section class="faq-section">
        <div class="container">
            <h2>Frequently Asked Questions</h2>
            {faq_section_html}
        </div>
    </section>

    <!-- Related Links -->
    {related_links_html}

    <!-- CTA -->
    {cta_section_html}
    """

    # -- Wrap and write ----------------------------------------------------
    full_html = get_page_wrapper(
        title=alt["title"],
        description=alt["meta_description"],
        canonical_path=f"/alternatives/{slug}/",
        body_content=page_content,
    )

    write_page(f"alternatives/{slug}/index.html", full_html)

    # Register in ALL_PAGES for sitemap
    ALL_PAGES.append((f"/alternatives/{slug}/", 0.7, "monthly"))


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
