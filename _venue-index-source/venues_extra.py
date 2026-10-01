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

 # ---- 1 Oct 2026: AJ's featured venues. Researched to RESEARCH-PROMPT v2,
 # or carried from the published venue visit page where one exists.
 dict(
   city="Sydney", slug="pier-one-sydney-harbour", checked="22 September 2026",
   worked=False, seen=None, visit="pier-one-sydney-harbour",
   n="Pier One Sydney Harbour, Autograph Collection", sp="Water Room", pr="Walsh Bay", ty="hotel",
   th=200, bq=180, cl=127, ck=350, cab=None, ush=None, bd=None,
   br=9, gr=189, area=315, ceil=7.0, ceilq=None,
   s_name="Bridge Marquee", s_th=150,
   note="A heritage finger wharf at Walsh Bay, beside the southern end of the Harbour Bridge, with 189 rooms upstairs and the harbour at the door. The Water Room takes 200 theatre or 180 for dinner under a seven metre ceiling, and the seven Dawes Point rooms carry the breakouts. It is lovely for a dinner, a launch or a residential meeting that can live inside 200 seats, and the whole venue takes 1,500 for a standing reception.",
   src="https://www.marriott.com/en-us/hotels/sydak-pier-one-sydney-harbour-autograph-collection/events/",
   src2="https://www.marriott.com/en-us/hotels/sydak-pier-one-sydney-harbour-autograph-collection/events/"),

 dict(
   city="Sydney", slug="intercontinental-sydney-coogee-beach", checked="22 September 2026",
   worked=False, seen=None, visit="intercontinental-sydney-coogee-beach",
   n="InterContinental Sydney Coogee Beach", sp="Grand Ballroom", pr="Coogee", ty="hotel",
   th=300, bq=260, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=7, gr=198, area=None, ceil=None, ceilq=None,
   s_name=None, s_th=None,
   note="The former Crowne Plaza Coogee Beach, refurbished and reopened as an InterContinental from December 2025, across the road from the sand. The pillar free Grand Ballroom takes 300 theatre or 260 for dinner, with six smaller rooms alongside and 198 rooms upstairs. It suits a board, a sales meeting or an incentive group that would rather have the ocean than the CBD. A plenary above 300 is better placed in the city or at Randwick.",
   src="https://www.ihg.com/intercontinental/hotels/us/en/sydney/sydcb/hoteldetail/meetings-events",
   src2="https://www.ihg.com/intercontinental/hotels/us/en/sydney/sydcb/hoteldetail/meetings-events"),

 dict(
   city="Sydney", slug="the-brighton-hotel-sydney-mgallery", checked="1 October 2026",
   worked=False, seen=None, visit=None,
   n="The Brighton Hotel Sydney, MGallery Collection", sp="The Brighton Ballroom", pr="Brighton-Le-Sands", ty="hotel",
   th=600, bq=420, cl=252, ck=550, cab=None, ush=45, bd=None,
   br=8, gr=307, area=675, ceil=2.9, ceilq=None,
   s_name="Endeavour Grand Ballroom", s_th=550,
   note="A beachfront hotel on Botany Bay with two plenary sized ballrooms under one roof, so a main session and a gala dinner can run without turning a room over. The Brighton Ballroom faces the water, and the Endeavour Ballroom on level two divides into three for breakouts. It relaunched in October 2025 after a long renovation and sits about ten minutes from the airport. There is no station at the door, so city delegates usually need transfers.",
   src="https://mgallery.accor.com/en/hotels/1656/meetings.html",
   src2="https://thebrightonsydney.com.au/event/brighton-ballroom/"),

 dict(
   city="Sydney", slug="elysium-manly", checked="1 October 2026",
   worked=False, seen=None, visit=None,
   n="Elysium Manly", sp="Pacific Ballroom", pr="Manly", ty="hotel",
   th=500, bq=350, cl=220, ck=500, cab=240, ush=None, bd=None,
   br=5, gr=213, area=512, ceil=None, ceilq=None,
   s_name="Fairy Bower", s_th=160,
   note="The former Manly Pacific, renamed Elysium Manly in August 2026 after a refurbishment of its rooms and restaurant. The Pacific Ballroom looks straight onto the ocean and divides into smaller rooms, with Fairy Bower and the Cove Rooms taking the breakouts. It suits residential conferences and incentive groups who want the beach on the doorstep. Delegates coming from the city usually arrive by ferry from Circular Quay, so allow for that in the run sheet.",
   src="https://www.elysiumhotels.com/manly/meetings-events/pacific-ballroom",
   src2="https://www.elysiumhotels.com/manly/meetings-events"),
]

# ------------------------------------------------------------------- joins
# A venue name in venues_sydney.py mapped to the folder under /venue-visits/
# that holds its page. Crown Sydney and Crown Towers Sydney are the same
# building; the index uses the corporate name and the page uses the hotel name.
VISIT_SLUGS = {
  "Crown Sydney": "crown-towers-sydney",
  # 1 Oct 2026: published visit pages the dataset was not pointing at
  # (cvbs-visit-flag-drift step 3).
  "Hilton Sydney": "hilton-sydney",
  "Sofitel Sydney Wentworth": "sofitel-sydney-wentworth",
  "The EVE Hotel Sydney": "the-eve-hotel-sydney",
  "The Star Gold Coast": "the-star-gold-coast",
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
