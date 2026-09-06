# -*- coding: utf-8 -*-
"""Venues outside the Sydney index, plus the joins between datasets.

WHY THIS FILE EXISTS
    Until 5 September 2026 CVBS held venue facts in two places that could not
    see each other. venues_sydney.py held 54 Sydney venues with sourced
    capacity figures and no pages. _venue-visits-source/build_venue.py held
    deep, room by room data for the five venues the team has walked through,
    with pages and no shared data. A venue could therefore be on the site twice
    with two different largest room figures and nothing to catch it.

    This file carries the non-Sydney venues in the same shape as the Sydney
    data, plus the joins: which venue has a page, which has a live offer.
    build_dataset.py merges the three and writes one dataset.

THE RULE, UNCHANGED
    Every figure here is read off the venue's own published capacity chart,
    fact sheet or events page, and is already published on that venue's CVBS
    page. Nothing is estimated, inferred or rounded. Where a venue publishes
    nothing for a field it is None and the site prints "Not published".
"""

# --------------------------------------------------------------- non-Sydney
# Same key set as venues_sydney.py, plus city, checked and slug.
# These three are the venues CVBS has walked through outside Sydney. Their
# figures come from the published venue pages under /venue-visits/.

VENUES_OTHER = [

 dict(
   city="Brisbane", slug="the-westin-brisbane", checked="5 September 2026",
   worked=False, seen=None, visit="the-westin-brisbane",
   n="The Westin Brisbane", sp="Westin Ballroom", pr="Brisbane CBD", ty="hotel",
   th=400, bq=280, cl=240, ck=400, cab=None, ush=None, bd=None,
   br=6, gr=298, area=450, ceil=None, ceilq=None,
   s_name="Westin Ballroom 1", s_th=205,
   note="A 298 room hotel on Mary Street with one ballroom of 450 square metres that divides in two, and a pair of smaller Elevate rooms alongside it. Built for a residential conference that never has to leave the building.",
   src="https://www.marriott.com/en-us/hotels/bnewi-the-westin-brisbane/events/stylish-spaces/",
   src2="https://www.marriott.com/en-us/hotels/bnewi-the-westin-brisbane/events/stylish-spaces/"),

 dict(
   city="Melbourne", slug="hotel-indigo-melbourne-little-collins", checked="5 September 2026",
   worked=False, seen=None, visit="hotel-indigo-melbourne-little-collins",
   n="Hotel Indigo Melbourne Little Collins", sp="The Boardroom", pr="Melbourne CBD", ty="hotel",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=12,
   br=2, gr=179, area=None, ceil=None, ceilq=None,
   s_name="Fern's Hidden Winter Garden", s_th=None,
   note="A 179 room lifestyle hotel over ten floors on Little Collins Street. One boardroom for twelve and no conference space, so it works as the accommodation half of a program whose plenary runs elsewhere in the city.",
   src="https://www.ihg.com/hotelindigo/hotels/us/en/melbourne/melgo/hoteldetail/events-facilities",
   src2="https://www.ihg.com/hotelindigo/hotels/us/en/melbourne/melgo/hoteldetail/events-facilities"),

 dict(
   city="Perth", slug="pullman-bunker-bay", checked="5 September 2026",
   worked=False, seen=None, visit="pullman-bunker-bay",
   n="Pullman Bunker Bay Resort", sp="Kaartdijinup I & II", pr="Margaret River region", ty="resort",
   th=140, bq=100, cl=32, ck=180, cab=80, ush=50, bd=None,
   br=7, gr=150, area=144, ceil=None, ceilq=None,
   s_name="Wardan", s_th=50,
   note="A 150 villa resort at Naturaliste, two and a half hours south of Perth, with seven event spaces including an outdoor amphitheatre. Built for a residential program that wants the drive to be part of the point.",
   src="https://www.pullmanbunkerbayresort.com.au/meetings/event-spaces",
   src2="https://www.pullmanbunkerbayresort.com.au/meetings/event-spaces"),
]

# ------------------------------------------------------- Sydney, not yet in
# the index file. Added here rather than to venues_sydney.py so the Sydney
# generator's verified-14-Aug provenance block is not disturbed. Figures are
# Accor's current published set, read 5 September 2026, and already published
# on the venue's own CVBS page.

VENUES_SYDNEY_EXTRA = [
 dict(
   city="Sydney", slug="pullman-quay-grand-sydney", checked="5 September 2026",
   worked=False, seen=None, visit="pullman-quay-grand-sydney",
   n="Pullman Quay Grand Sydney Harbour", sp="Conference Room", pr="Circular Quay", ty="hotel",
   th=70, bq=50, cl=None, ck=None, cab=None, ush=None, bd=30,
   br=3, gr=None, area=85, ceil=None, ceilq=None,
   s_name="Acapulco El Vista Bar + Lounge", s_th=70,
   note="An all suite hotel on East Circular Quay with three small event spaces. The right building for an executive program or a board dinner on the harbour, not for a conference.",
   src="https://pullman.accor.com/en/hotels/sydney/8779/meetings.html",
   src2="https://pullman.accor.com/en/hotels/sydney/8779/meetings.html"),
]

# ------------------------------------------------------------------- joins
# A venue name in venues_sydney.py mapped to the folder under /venue-visits/
# that holds its page. Crown Sydney and Crown Towers Sydney are the same
# building; the index uses the corporate name and the page uses the hotel name.
VISIT_SLUGS = {
  "Crown Sydney": "crown-towers-sydney",
}

# A venue name mapped to its live offer page in the site root. Update whenever
# offers change, alongside the OFFERS map in submit-a-brief.html.
# Empty on 6 September 2026. Kimpton Margot Sydney carried a "Current offer"
# badge pointing at a stub that redirected to offers.html#kimpton-margot, an
# anchor that does not exist. A badge must resolve to a published offer.
OFFER_PAGES = {
}

# Cities that have a destination page but no venue data yet. Listed so the
# build can report the gap rather than the site implying coverage it does not
# have. Adding venue data for one of these removes it from here automatically.
CITY_PAGES = {
  "Sydney": "venue-finder-sydney.html",
  "Melbourne": "venue-finder-melbourne.html",
  "Brisbane": "venue-finder-brisbane.html",
  "Perth": "venue-finder-perth.html",
  "Adelaide": "venue-finder-adelaide.html",
  "Canberra": "venue-finder-canberra.html",
  "Gold Coast": "venue-finder-gold-coast.html",
  "Hobart": "venue-finder-hobart.html",
  "Darwin": "venue-finder-darwin.html",
  "Cairns": "venue-finder-cairns.html",
  "Hunter Valley": "venue-finder-hunter-valley.html",
  "Blue Mountains": "venue-finder-blue-mountains.html",
  "Byron Bay": "venue-finder-byron-bay.html",
  "Sunshine Coast": "venue-finder-sunshine-coast.html",
  "Yarra Valley": "venue-finder-yarra-valley.html",
  "Mornington Peninsula": "venue-finder-mornington-peninsula.html",
}
