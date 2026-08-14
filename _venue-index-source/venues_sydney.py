# -*- coding: utf-8 -*-
"""Sydney venue index data. Every figure is read off the venue's own published
capacity chart, fact sheet, floor plan or technical spec. Last checked 14 Aug 2026.

src  = source for the capacity figures.
src2 = source for the ceiling height, floor area, extra setups and second space.
ceilq = an honest qualifier where a single ceiling number would mislead a planner.

Deliberately left None, and why:
  ICC Sydney area      - two reads of the same PDF gave 2,880 and 3,100 sqm.
                         Conflict unresolved, so None rather than pick one.
  Pullman Ibis ceiling - the hotel publishes 2.64m against a 264sqm room seating
                         250 theatre. Digit repetition plus implausibility reads
                         as a typo on their site. Ask the venue before publishing.
"""

CITY = "Sydney"

VENUES = [
 dict(
   n="ICC Sydney", sp="Grand Ballroom", pr="Darling Harbour", ty="conv",
   th=2784, bq=2000, cl=1764, ck=2880, cab=1296, ush=None, bd=None,
   br=70, gr=0, area=None, ceil=9.0, ceilq=None,
   s_name="Parkside Ballroom", s_th=1400,
   note="Australia's largest ballroom, beside a 2,500 seat theatre, an 8,000 seat plenary theatre and 32,600 sqm of exhibition halls. The only Sydney venue that runs a plenary, a trade exhibition and concurrent breakouts on the same day.",
   src="https://iccsydney.com.au/wp-content/uploads/2023/05/ICCS_fact-sheets_capacity_1_v1d.pdf",
   src2="https://www.iccsydney.com.au/wp-content/uploads/2023/06/iccs-conv-l5-grand-ballroom-floor-box-and-service-cupboards.pdf"),

 dict(
   n="Sydney Showground", sp="The Dome", pr="Sydney Olympic Park", ty="conv",
   th=7000, bq=4000, cl=None, ck=6000, cab=None, ush=None, bd=None,
   br=None, gr=0, area=7200, ceil=42.0, ceilq="at the dome apex; 9m to the rigging star",
   s_name="Hall 6", s_th=5045,
   note="Thirty thousand square metres of pillar free hall space. Built for trade shows, consumer expos and very large plenaries, with parking and rail at the door.",
   src="https://www.sydneyshowground.com.au/globalassets/document-library/sydney-showground/sydney-showground-brochure.pdf",
   src2="https://www.sydneyshowground.com.au/globalassets/document-library/sydney-showground/fact-sheets/the-dome-ss_venue-fact-sheets_2022.pdf"),

 dict(
   n="Royal Randwick Racecourse", sp="Winx Pavilion", pr="Eastern Suburbs", ty="event",
   th=1692, bq=1300, cl=None, ck=3000, cab=1144, ush=None, bd=None,
   br=17, gr=0, area=None, ceil=6.2, ceilq=None,
   s_name="The Ballroom, Queen Elizabeth II Grandstand", s_th=1100,
   note="A 2,222 sqm ground floor pavilion with tiered gallery rooms above it. Suits gala dinners, expos and awards nights that need parking close to the city.",
   src="https://cdn.australianturfclub.com.au/app/uploads/2025/12/ATC-Meetings-Events-Venue-Brochure.pdf",
   src2="https://www.australianturfclub.com.au/spaces/winx-stand-royal-randwick/"),

 dict(
   n="Sydney Event Centre", sp="Main Room", pr="Pyrmont", ty="event",
   th=1460, bq=960, cl=657, ck=2200, cab=768, ush=None, bd=None,
   br=None, gr=0, area=1077, ceil=12.0, ceilq=None,
   s_name="The Attic", s_th=100,
   note="Purpose built theatre and flat floor hall at The Star, handling awards nights, concerts and large plenaries in the one room. Capacity chart still published under its former name, The Star Event Centre.",
   src="https://www.star.com.au/sites/default/files/2024-06/Event-Centre-SalesKit-Nov-2018.pdf",
   src2="https://www.star.com.au/sites/default/files/2024-06/Event-Centre-SalesKit-Nov-2018.pdf"),

 dict(
   n="The Fullerton Hotel Sydney", sp="The Grand Ballroom", pr="Sydney CBD", ty="hotel",
   th=1400, bq=1000, cl=660, ck=1200, cab=800, ush=None, bd=None,
   br=15, gr=416, area=1058, ceil=6.0, ceilq=None,
   s_name="Heritage Ballroom", s_th=350,
   note="The largest pillarless hotel ballroom in Sydney at 1,058 sqm, in the former GPO on Martin Place. Suits conference plenaries, awards nights and gala dinners in the CBD.",
   src="https://www.fullertonhotels.com/fullerton-hotel-sydney/meetings-and-events/grand-ballroom",
   src2="https://www.fullertonhotels.com/fullerton-hotel-sydney/meetings-and-events/meeting-spaces"),

 dict(
   n="Hyatt Regency Sydney", sp="Grand Ballroom", pr="Darling Harbour", ty="hotel",
   th=1000, bq=750, cl=552, ck=1000, cab=520, ush=None, bd=None,
   br=23, gr=878, area=850, ceil=8.5, ceilq=None,
   s_name="Maritime Ballroom", s_th=1000,
   note="Australia's largest hotel by room count, so a full residential conference and its accommodation sit on the one site. Two ballrooms of near identical size run concurrent streams.",
   src="https://www.hyatt.com/content/dam/hotel/propertysites/assets/regency/sydrs/documents/en_US/special-events/meetings/Capacity-Chart-English.pdf",
   src2="https://www.hyatt.com/content/dam/hotel/propertysites/assets/regency/sydrs/documents/en_US/special-events/meetings/Capacity-Chart-English.pdf"),

 dict(
   n="Doltone House Jones Bay Wharf", sp="Heritage Wharf", pr="Pyrmont", ty="event",
   th=900, bq=680, cl=400, ck=1000, cab=None, ush=None, bd=None,
   br=8, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Loft", s_th=130,
   note="Heritage listed waterfront wharf that splits into two rooms. Suits gala dinners, conferences and exhibitions on the water, without hotel constraints.",
   src="https://doltonehouse.com.au/space/heritage/",
   src2="https://doltonehouse.com.au/space/loft/"),

 dict(
   n="Sheraton Grand Sydney Hyde Park", sp="Grand Ballroom", pr="Sydney CBD", ty="hotel",
   th=850, bq=500, cl=360, ck=900, cab=None, ush=None, bd=None,
   br=20, gr=558, area=650, ceil=4.1, ceilq=None,
   s_name="Castlereagh Room", s_th=200,
   note="4,435 sqm of event space across 20 rooms, the deepest breakout inventory of any CBD hotel. Built for multi day conferences running concurrent streams.",
   src="https://www.marriott.com/en-us/hotels/sydsi-sheraton-grand-sydney-hyde-park/events/",
   src2="https://www.marriott.com/en-us/hotels/sydsi-sheraton-grand-sydney-hyde-park/events/"),

 dict(
   n="Shangri-La Sydney", sp="Grand Ballroom", pr="The Rocks", ty="hotel",
   th=800, bq=500, cl=400, ck=850, cab=410, ush=None, bd=None,
   br=24, gr=564, area=670, ceil=4.15, ceilq=None,
   s_name="Cambridge Rooms", s_th=160,
   note="Views over the bridge and Opera House from a divisible grand ballroom. Suits premium conferences, gala dinners and incentive groups staying in house.",
   src="https://www.shangri-la.com/sydney/shangrila/meetings-events/event-spaces/",
   src2="https://www.shangri-la.com/sydney/shangrila/meetings-events/event-spaces/"),

 dict(
   n="Luna Park Sydney", sp="The Big Top", pr="Milsons Point", ty="event",
   th=750, bq=600, cl=570, ck=1000, cab=None, ush=None, bd=None,
   br=8, gr=0, area=None, ceil=9.0, ceilq="at the eaves; 14m at the centre",
   s_name="Crystal Palace Grand Ballroom", s_th=600,
   note="Harbourside auditorium plus the Crystal Palace ballrooms, with the park available for exclusive use. Conference by day and the evening event on the same site.",
   src="https://www.lunaparksydney.com/corporate-events/immersive-big-top",
   src2="https://www.lunaparksydney.com/corporate-events/immersive-big-top"),

 dict(
   n="Sydney Masonic Centre", sp="Banquet Hall", pr="Sydney CBD", ty="conv",
   th=550, bq=380, cl=300, ck=600, cab=380, ush=60, bd=40,
   br=12, gr=0, area=555, ceil=7.0, ceilq=None,
   s_name="Grand Lodge", s_th=600,
   note="A dedicated CBD conference centre with a 555 sqm flat floor hall and a separate 600 seat tiered auditorium. Plenary and breakouts in one building, no hotel traffic through the foyer.",
   src="https://sydneymasoniccentre.com.au/property/banquet-hall/",
   src2="https://sydneymasoniccentre.com.au/property/banquet-hall/"),

 dict(
   n="W Sydney", sp="Great Room", pr="Darling Harbour", ty="hotel",
   th=500, bq=360, cl=339, ck=600, cab=None, ush=60, bd=None,
   br=8, gr=588, area=592, ceil=5.6, ceilq=None,
   s_name="Studio 2", s_th=100,
   note="A single dedicated event floor on Level 5, design led throughout. Strong for product launches and brand events that need to look current.",
   src="https://www.marriott.com/en-us/hotels/sydwh-w-sydney/events/",
   src2="https://www.marriott.com/en-us/hotels/sydwh-w-sydney/events/"),

 dict(
   n="Rydges World Square", sp="Grand Sydney Ballroom", pr="Sydney CBD", ty="hotel",
   th=500, bq=350, cl=280, ck=550, cab=250, ush=None, bd=None,
   br=12, gr=458, area=500, ceil=3.0, ceilq=None,
   s_name="The Terrace", s_th=86,
   note="A divisible lobby level ballroom with 458 rooms above it. Dependable mid market choice for residential conferences in the CBD.",
   src="https://www.rydges.com/accommodation/sydney-nsw/world-square-sydney-cbd/venues/grand-ballroom/",
   src2="https://www.rydges.com/accommodation/sydney-nsw/world-square-sydney-cbd/meetings-events/all-venues/"),

 dict(
   n="Sofitel Sydney Darling Harbour", sp="Magnifique Ballroom", pr="Darling Harbour", ty="hotel",
   th=450, bq=300, cl=276, ck=450, cab=None, ush=60, bd=80,
   br=7, gr=590, area=497, ceil=5.0, ceilq=None,
   s_name="Byrne", s_th=103,
   note="Directly adjoining ICC Sydney, which makes it the natural accommodation and gala dinner partner for convention centre programs.",
   src="https://www.besydney.com.au/find-a-supplier/accor-sofitel-sydney-darling-harbour/",
   src2="https://sofitel.accor.com/en/hotels/9729/meetings.html"),

 dict(
   n="Aerial UTS Function Centre", sp="Full venue, five rooms combined", pr="Surry Hills & Central", ty="conv",
   th=450, bq=350, cl=270, ck=450, cab=270, ush=None, bd=None,
   br=5, gr=0, area=494, ceil=None, ceilq=None,
   s_name=None, s_th=None,
   note="Five equal rooms on level 7 in Ultimo that open into one 494 sqm pillar free space. Plenary and matching breakouts without moving floors.",
   src="https://aerialfunctioncentre.com.au/venue/",
   src2="https://aerialfunctioncentre.com.au/venue/"),

 dict(
   n="Crown Sydney", sp="Pearl Ballroom", pr="Barangaroo", ty="hotel",
   th=390, bq=340, cl=125, ck=390, cab=280, ush=None, bd=None,
   br=11, gr=349, area=573, ceil=4.7, ceilq=None,
   s_name="Opal Suite", s_th=None,
   note="Six star positioning on the Barangaroo waterfront, with eleven bookable spaces including restaurant private dining rooms. Suits executive programs and prestige dinners rather than large plenaries.",
   src="https://www.crownhotels.com.au/sydney/events-conferences/event-venues/pearl-ballroom",
   src2="https://www.crownsydney.com.au/getmedia/90d6bc48-070b-4095-aa3d-5cc4c3b84dc0/Crown-Sydney-Events-Pearl-Ballroom.pdf"),

 dict(
   n="Novotel Sydney International Airport", sp="Grand Ballroom", pr="Sydney Airport", ty="hotel",
   th=380, bq=260, cl=120, ck=400, cab=208, ush=None, bd=None,
   br=11, gr=271, area=320, ceil=4.0, ceilq=None,
   s_name="Protea Room", s_th=100,
   note="Pillar free ballroom and ten smaller rooms at Wolli Creek, on the airport rail line. Built for fly in, fly out national meetings and training days.",
   src="https://www.novotelsydneyairport.com.au/meetings-and-events/meeting-rooms/grand-ballroom",
   src2="https://www.novotelsydneyairport.com.au/meetings-and-events/meeting-rooms/grand-ballroom"),

 dict(
   n="Amora Hotel Jamison Sydney", sp="Whiteley Ballroom", pr="Sydney CBD", ty="hotel",
   th=370, bq=260, cl=180, ck=350, cab=208, ush=66, bd=None,
   br=8, gr=415, area=None, ceil=None, ceilq=None,
   s_name="Hart Room", s_th=70,
   note="A pillarless ballroom that divides in two, with 415 rooms above it near Wynyard. Good value for mid size residential conferences.",
   src="https://www.amorahotels.com/sydney/meetings-events/venues/whiteley-ballroom",
   src2="https://www.amorahotels.com/sydney/meetings-events/venues/whiteley-ballroom"),

 dict(
   n="InterContinental Sydney", sp="Boronia Ballroom", pr="Circular Quay", ty="hotel",
   th=350, bq=240, cl=150, ck=400, cab=200, ush=57, bd=42,
   br=14, gr=509, area=497, ceil=4.3, ceilq=None,
   s_name="Acacia Room", s_th=232,
   note="2,361 sqm of meeting space across 14 rooms in the heritage Treasury Building. Suits board level programs that want Circular Quay on the invitation.",
   src="https://www.sydney.intercontinental.com/hotel/venues/boronia-ballroom/",
   src2="https://www.sydney.intercontinental.com/hotel/venues/boronia-ballroom/"),

 dict(
   n="Pullman Sydney Hyde Park", sp="Ibis Room", pr="Sydney CBD", ty="hotel",
   th=250, bq=180, cl=150, ck=250, cab=None, ush=80, bd=None,
   br=8, gr=241, area=264, ceil=None, ceilq=None,
   s_name="Cook Room", s_th=100,
   note="A mid size conference floor opposite Hyde Park with 241 rooms above. Suits conferences and dinners to 250 that want the CBD without the harbour premium.",
   src="https://www.pullmansydneyhydepark.com.au/meetings",
   src2="https://www.pullmansydneyhydepark.com.au/en/meeting-rooms/ibis-room.html"),

 dict(
   n="Novotel Sydney Darling Square", sp="Darling Harbour Room", pr="Darling Harbour", ty="hotel",
   th=130, bq=110, cl=66, ck=140, cab=100, ush=None, bd=None,
   br=6, gr=230, area=168, ceil=2.4, ceilq=None,
   s_name="Little Pier Room", s_th=60,
   note="Next door to ICC Sydney. Built for small meetings, training days and delegate accommodation rather than plenaries.",
   src="https://www.novotelsydneydarlingsquare.com.au/meetings/darling-harbour-room",
   src2="https://www.novotelsydneydarlingsquare.com.au/meetings/darling-harbour-room"),

 dict(
   n="View Sydney", sp="Bradfield Rooms", pr="North Sydney", ty="hotel",
   th=120, bq=78, cl=46, ck=120, cab=65, ush=None, bd=None,
   br=7, gr=None, area=162, ceil=None, ceilq=None,
   s_name="Lavender Bay Rooms", s_th=45,
   note="A compact North Sydney conference floor across the bridge. Suits north shore team meetings and seminars under 120.",
   src="https://viewhotels.com.au/wp-content/uploads/2024/10/VS-Floorplans-and-Capacities.pdf",
   src2="https://viewhotels.com.au/sydney/meetings-and-events/rooms-and-spaces/bradfield-rooms/"),

 dict(
   n="Sydney Opera House", sp="Concert Hall", pr="Circular Quay", ty="event",
   th=2102, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=None, gr=0, area=None, ceil=15.0, ceilq="over the centre line",
   s_name="Joan Sutherland Theatre", s_th=1507,
   note="Fixed seat auditorium seating 2,102 facing the stage and 2,664 in the round. Plenaries, keynotes and awards ceremonies only, with no banquet or classroom setup.",
   src="https://www.sydneyoperahouse.com/visit/our-venues/concert-hall",
   src2="https://www.sydneyoperahouse.com/sites/default/files/collaborodam_assets/SOHVenueTechnicalSpecifications_ConcertHall202401.pdf"),

 dict(
   n="Sydney Town Hall", sp="Centennial Hall", pr="Sydney CBD", ty="event",
   th=2008, bq=800, cl=280, ck=1500, cab=580, ush=None, bd=None,
   br=9, gr=0, area=913, ceil=20.0, ceilq=None,
   s_name="Lower Town Hall", s_th=800,
   note="A 1,020 sqm heritage hall seating 2,008 across the floor and first floor galleries. The largest conference plenary in the CBD, and the only one above 2,000.",
   src="https://www.cityofsydney.nsw.gov.au/-/media/corporate/files/places-and-spaces/sydney-town-hall/venue-specifications-2025-06.pdf",
   src2="https://www.cityofsydney.nsw.gov.au/-/media/corporate/files/places-and-spaces/sydney-town-hall/venue-specifications-2025-06.pdf"),

 dict(
   n="Hordern Pavilion", sp="Main Hall", pr="Moore Park", ty="event",
   th=None, bq=1400, cl=None, ck=3500, cab=None, ush=None, bd=None,
   br=None, gr=0, area=3600, ceil=13.0, ceilq="to the dome; 6.2m under the trusses between columns",
   s_name="Foyer", s_th=None,
   note="A single 3,600 sqm hall with 3,100 sqm usable. Built for exhibitions, trade shows, large dinners and standing events rather than multi stream conferences.",
   src="https://playbillvenues.com.au/app/uploads/2025/06/HP_Function-Hire-Pack.pdf",
   src2="https://playbillvenues.com.au/app/uploads/2025/06/HP_Function-Hire-Pack.pdf"),

 dict(
   n="Hilton Sydney", sp="Grand Ballroom", pr="Sydney CBD", ty="hotel",
   th=1100, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=28, gr=None, area=920, ceil=6.0, ceilq=None,
   s_name=None, s_th=None,
   note="An 806 sqm ballroom with six metre ceilings and 28 event spaces across the hotel. One of only three Sydney hotels seating more than 1,000 in a single room.",
   src="https://www.hiltonsydney.com.au/meetings-events/facilities-services/level-3",
   src2="https://www.hilton.com/en/hotels/sydhitw-hilton-sydney/events/"),

 dict(
   n="Sofitel Sydney Wentworth", sp="Wentworth Ballroom", pr="Sydney CBD", ty="hotel",
   th=800, bq=500, cl=462, ck=800, cab=400, ush=None, bd=None,
   br=15, gr=436, area=629, ceil=5.3, ceilq=None,
   s_name="Brisbane Room", s_th=201,
   note="A 629 sqm pillarless ballroom with 15 event spaces and 436 rooms above it on Phillip Street. Suits mid size residential conferences and gala dinners.",
   src="https://www.sofitelsydney.com.au/wentworth-ballroom",
   src2="https://www.sofitelsydney.com.au/wentworth-ballroom"),

]