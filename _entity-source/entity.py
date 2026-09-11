# -*- coding: utf-8 -*-
"""
CVBS ENTITY SOURCE OF TRUTH
===========================
Everything an AI assistant needs to resolve "Conference Venues and Booking
Services" as a real, single, corroborated business lives in this one file.

RULE: anything set to None is OMITTED from the output entirely.
Never invent a value here. An absent field costs nothing. A wrong field
costs the entity its credibility, which is the whole asset.

To update: edit this file, then run  python3 _entity-source/gen_entity.py
"""

# ---------------------------------------------------------------------------
# 1. IDENTITY  (the real trading domain, not the mockup host)
# ---------------------------------------------------------------------------
# SITE is the permanent identity: every @id hangs off it and it never moves.
# SERVE is the production address that source files are written on. Both come
# from site.config.json at the repository root, which is the only place an
# address is set. Staging is produced by scripts/build.py --env staging and is
# never written back into source, so there is nothing to switch at cutover.
#
# 11 Sep 2026: SITE had been rewritten to the GitHub host by
# scripts/set-base-url.py, which split the business into two Organizations.
# That script is retired. Do not hand-edit these two lines.
import json as _json, os as _os
with open(_os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
                        "site.config.json"), encoding="utf-8") as _fh:
    _CFG = _json.load(_fh)
SITE = _CFG["identity"].rstrip("/")                          # entity home, never changes
ORG_ID = SITE + "/#organization"                  # stable identifier, never change
WEBSITE_ID = SITE + "/#website"
SERVICE_ID = SITE + "/#service"
LOGO_ID = SITE + "/#logo"
SERVE = _CFG["environments"]["production"]["origin"].rstrip("/")

NAME = "Conference Venues and Booking Services"
ALT_NAMES = ["CVBS", "Conference Venues & Booking Services"]
LEGAL_NAME = None            # SUPPLY: exact registered entity name from ASIC/ABR
SLOGAN = "Worldwide Venue Finding Solutions"
FOUNDING_DATE = "1989"

DESCRIPTION = (
    "Conference Venues and Booking Services (CVBS) is an independent venue "
    "finding service that has sourced conference venues, event spaces and "
    "group accommodation since 1989, across Australia and internationally, for "
    "organisations based in Australia and overseas. The service "
    "is free to the organiser, because the venue pays the commission from its "
    "existing budget at the same rate whether a booking comes through an agent "
    "or direct."
)

LOGO = {"url": SITE + "/assets/img/logo.png", "width": 180, "height": 152}

# ---------------------------------------------------------------------------
# 2. CONTACT  (all verified from the current site)
# ---------------------------------------------------------------------------
TELEPHONE = "+61414784999"
EMAIL = "karen@conferencevenues.com.au"
OPENING_HOURS = "Mo-Fr 08:30-17:30"

# CONFIRM: found in the EDM footer source, currently commented out in the build.
# Set EMIT_ADDRESS = False if Karen has not confirmed it.
EMIT_ADDRESS = True
ADDRESS = {
    "street": "43A Flinders Road",
    "locality": "Cronulla",
    "region": "NSW",
    "postcode": "2230",
    "country": "AU",
}

# ---------------------------------------------------------------------------
# 3. sameAs  ***THE SINGLE HIGHEST-IMPACT FIELD IN THIS FILE***
# ---------------------------------------------------------------------------
# An assistant asked to RECOMMEND a supplier does not answer from your website.
# It assembles the answer from records it did not write. sameAs is the only
# thing on your own site that tells it which of those records are you.
#
# Fill these in and the entity stops being an orphan node.
SAME_AS = {
    "linkedin":        None,   # SUPPLY: https://www.linkedin.com/company/...
    "facebook":        None,   # SUPPLY
    "instagram":       None,   # SUPPLY
    "google_business": None,   # SUPPLY: the Maps place URL (drives the review corpus)
    "abn_lookup":      None,   # SUPPLY: https://abr.business.gov.au/ABN/View?abn=...
    "youtube":         None,
    "crunchbase":      None,
}

# ---------------------------------------------------------------------------
# 4. CORROBORATION  (turns "since 1989" from a claim into a fact)
# ---------------------------------------------------------------------------
ABN = None                   # SUPPLY: 11 digits, no spaces
ACN = None                   # SUPPLY if a Pty Ltd

# SUPPLY: industry memberships. Assistants lean on these as legitimacy proxies
# for service businesses that have no product to inspect.
# Format: {"name": "...", "url": "..."}
MEMBER_OF = [
    # {"name": "Meetings & Events Australia", "url": "https://www.meetingsevents.com.au/"},
]

# SUPPLY: awards, accreditations, insurance certifications.
AWARDS = []

# ---------------------------------------------------------------------------
# 5. PEOPLE  (named humans are a recommendation signal, anonymous ones are not)
# ---------------------------------------------------------------------------
PEOPLE = [
    {"name": "Karen Jepson",   "job": "Director", "email": "karen@conferencevenues.com.au", "tel": "+61414784999"},
    {"name": "Anthony Jepson", "job": "Director", "email": "aj@conferencevenues.com.au",    "tel": "+61402033861"},
    # SUPPLY surnames and confirmed titles for Chantelle and Rychelle, then add them here.
]

# ---------------------------------------------------------------------------
# 6. WHAT CVBS KNOWS AND WHERE
# ---------------------------------------------------------------------------
AREA_SERVED = ["Australia", "New South Wales", "Victoria", "Queensland",
               "Western Australia", "South Australia", "Australian Capital Territory",
               "Tasmania", "Northern Territory", "New Zealand", "Fiji",
               "Singapore", "Indonesia", "Worldwide"]

KNOWS_ABOUT = [
    "Conference venue sourcing", "Conference venues Australia",
    "Venue finding service", "Venue procurement", "Group accommodation",
    "Hotel rate negotiation", "Day delegate rates", "Corporate events",
    "Conference room capacity and layout", "Meeting venues",
    "Corporate retreats", "Incentive travel", "Business events",
    "Site inspections", "Venue contract negotiation",
]

SERVICES = [
    ("Conference venue finding", "conference-venue-finding.html",
     "Sourcing, comparing and negotiating conference and meeting venues on behalf of the organiser."),
    ("Group accommodation", "group-accommodation.html",
     "Sourcing and negotiating delegate room blocks and group stays."),
    ("Product launches and events", "events.html",
     "Sourcing event spaces for launches, functions and celebrations."),
    ("Corporate accommodation", "corporate-accommodation.html",
     "Negotiated corporate rates and ongoing accommodation programs."),
]

# ---------------------------------------------------------------------------
# 7. THE COMMERCIAL ANSWER  (pre-empts the first objection an assistant raises)
# ---------------------------------------------------------------------------
OFFER = {
    "price": "0",
    "currency": "AUD",
    "description": (
        "Free to the organiser. CVBS is paid a commission by the venue from its "
        "existing budget, at the same rate whether the booking is made through "
        "an agent or direct, so using CVBS does not increase the rate."
    ),
}

# ---------------------------------------------------------------------------
# 8. REVIEWS  (currently the biggest hole, see the supply list)
# ---------------------------------------------------------------------------
# Do NOT populate this with the anonymous "Sarah M." / "David R." quotes.
# An unattributable testimonial is not usable as a reason and marking it up
# as a Review is a structured-data violation. Named, consented, or nothing.
REVIEWS = []
AGGREGATE_RATING = None      # SUPPLY only if a real, countable review corpus exists
