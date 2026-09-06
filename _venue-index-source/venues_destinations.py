# -*- coding: utf-8 -*-
"""Venue data for the fifteen destinations outside Sydney.

Researched and written 6 September 2026, in the same shape as venues_sydney.py.

THE RULE, UNCHANGED FROM venues_extra.py
    Every figure here is read off the venue's own published capacity chart,
    fact sheet, floor plan or events page, or where the venue publishes none,
    off the official convention bureau listing for that venue. Nothing is
    estimated, inferred or rounded. Where a venue publishes nothing for a
    field it is None and the site prints "Not published".

    Directories (Cvent, VenueNow, Tagvenue, wedding sites) were used to
    discover venue names and never as the source of a figure.

WHAT WAS DELIBERATELY LEFT None, AND WHY
    Ceiling heights are absent across most of the market. BCEC publishes none
    at all. Every Hobart hotel except Crowne Plaza publishes none. Wrest Point
    prints a ceiling column with no units and implausible values, so it is
    nulled rather than guessed.

    Setup breakdowns are absent at most regional and winery venues, which
    publish a single "up to N guests" figure without naming the layout. Those
    are recorded against the layout the venue names, or not at all.

    Melbourne: Sofitel Melbourne on Collins publishes two conflicting capacity
    sets through two of its own channels, so only theatre, floor area and
    ceiling survive. MCG function capacities are not published anywhere, so
    the MCG has no row.

    Brisbane: InterContinental Brisbane publishes a floor area and "up to
    1,000 guests" but no setup breakdown, and began a two year transformation
    in 2026, so it has no row. Victoria Park closed as an event venue on
    31 May 2026 and is deliberately absent.

    Adelaide: Stamford Plaza publishes no capacities and has no row.
    233 Victoria Square is Amora Hotel Adelaide, not Hilton Adelaide.

    Hunter Valley: Crowne Plaza Hunter Valley could not be confirmed as
    trading from any IHG source and has no row. Tonic Hunter Valley does not
    resolve and has no row.

    Blue Mountains: Wolgan Valley is absent from One&Only's current
    destination list and has no row. Scenic World publishes no venue hire.

    Byron Bay: Harvest Newrybar closed in December 2024 and has no row.

    Cairns: Hilton Cairns figures come from the convention bureau because
    every Hilton.com URL returned 404 or was blocked.
"""

VENUES_DESTINATIONS = [

# ------------------------------------------------------------------ MELBOURNE
 dict(
   city="Melbourne", slug="melbourne-convention-and-exhibition-centre", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Melbourne Convention and Exhibition Centre", sp="Plenary", pr="South Wharf", ty="conv",
   th=5564, bq=1270, cl=846, ck=1500, cab=1016, ush=None, bd=None,
   br=None, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Melbourne Room", s_th=2232,
   note="The only building in Victoria that runs a multi thousand delegate plenary and a large trade exhibition on the same site on the same day. The Plenary is a fixed tiered auditorium with a balcony, so it behaves like a theatre rather than a flat ballroom, and the 40,000 square metres of pillarless exhibition bays next door are where the flat floor and the loading docks are.",
   src="https://www.mcec.com.au/room-and-spaces/plenary-entire",
   src2="https://www.mcec.com.au/room-and-spaces/exhibition-bays"),

 dict(
   city="Melbourne", slug="crown-melbourne", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Crown Melbourne", sp="Palladium", pr="Southbank", ty="hotel",
   th=2300, bq=1500, cl=1100, ck=2300, cab=1200, ush=None, bd=None,
   br=28, gr=None, area=None, ceil=7.0, ceilq="as the venue describes the room, not a rigging height",
   s_name="Conference Hall", s_th=840,
   note="The one Melbourne address where a large gala dinner, the conference sessions and most of the room block sit inside a single complex with three hotels on it. The Palladium is a pillarless flat floor ballroom, so it takes staging and vehicle reveals that a tiered auditorium cannot, and the separate Conference Hall carries the daytime program.",
   src="https://www.crownhotels.com.au/melbourne/events-conferences/venues/palladium",
   src2="https://www.crownmelbourne.com.au/events-and-conferences/corporate-events/conference-hall"),

 dict(
   city="Melbourne", slug="sofitel-melbourne-on-collins", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Sofitel Melbourne on Collins", sp="Grand Ballroom", pr="Collins Street east", ty="hotel",
   th=1000, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=12, gr=363, area=796, ceil=5.0, ceilq=None,
   s_name="La Trobe Ballroom", s_th=350,
   note="The top of town option, at the Paris end of Collins Street rather than in the convention precinct, and the right building when the delegate profile matters more than the delegate count. The Grand Ballroom is pillarless with a permanent 18 metre LED wall and a car hoist, which removes most of a launch build before you start.",
   src="https://accorevents.com/venues/sofitel-melbourne-on-collins",
   src2="https://www.sofitel-melbourne.com.au/conferences-and-events/grand-ballroom/"),

 dict(
   city="Melbourne", slug="pullman-east-melbourne", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Pullman East Melbourne", sp="Grand Ballroom", pr="East Melbourne", ty="hotel",
   th=850, bq=510, cl=400, ck=None, cab=None, ush=None, bd=None,
   br=11, gr=419, area=707, ceil=4.0, ceilq=None,
   s_name="Ballroom 3", s_th=320,
   note="Rebranded from Pullman Melbourne on the Park, this sits on the edge of the city facing Fitzroy Gardens with 419 rooms behind an 850 seat ballroom. It is a walk from the MCG and Melbourne Park, which makes it the default when the program has a sporting or stadium component attached, and unusable in January while the Australian Open runs.",
   src="https://accorevents.com/venues/pullman-melbourne-on-the-park",
   src2="https://www.pullmaneastmelbourne.com.au/"),

 dict(
   city="Melbourne", slug="marvel-stadium", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Marvel Stadium", sp="Victory Room", pr="Docklands", ty="event",
   th=1400, bq=1200, cl=None, ck=2000, cab=800, ush=None, bd=None,
   br=None, gr=0, area=2188, ceil=4.39, ceilq=None,
   s_name="Medallion Club", s_th=500,
   note="A working stadium in Docklands with more than twenty function spaces wrapped around the bowl. The Victory Room is a flat floor function room of stadium proportions and the arena itself can be hired for very large receptions, so the building scales in a way no hotel does.",
   src="https://www.marvelstadium.com.au/elevate",
   src2="https://www.melbournecb.com.au/plan-an-event/find-a-supplier/marvel-stadium/395"),

 dict(
   city="Melbourne", slug="melbourne-town-hall", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Melbourne Town Hall", sp="Main Hall", pr="Swanston Street", ty="event",
   th=1100, bq=720, cl=None, ck=1500, cab=576, ush=None, bd=None,
   br=None, gr=0, area=1006, ceil=None, ceilq=None,
   s_name="Yarra Room", s_th=None,
   note="A civic hall in the middle of the city grid with a purpose built stage, an organ and an upper gallery seating 800. It suits award nights, conference gala dinners and single day plenaries where the address and the room are doing the work, and it puts delegates straight into the laneway dining district afterwards.",
   src="https://showtimeeventgroup.com.au/venues/melbourne-town-hall/main-hall/",
   src2="https://showtimeeventgroup.com.au/venues/"),

 dict(
   city="Melbourne", slug="melbourne-museum", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Melbourne Museum", sp="Main Foyer and Walk", pr="Carlton", ty="event",
   th=600, bq=600, cl=None, ck=2000, cab=None, ush=None, bd=None,
   br=6, gr=0, area=3151, ceil=None, ceilq=None,
   s_name="Melbourne Gallery", s_th=100,
   note="A museum in the Carlton Gardens whose main foyer takes 2,000 standing but only 600 seated, which makes it a launch and reception building rather than a dinner building. Galleries can be opened to guests during an event and there is a fixed 214 seat theatre on site for the presentation part of the evening.",
   src="https://museumsvictoria.com.au/venues-and-events/spaces-for-hire/melbourne-museum/",
   src2="https://museumsvictoria.com.au/venues-and-events/spaces-for-hire/melbourne-museum/"),

 dict(
   city="Melbourne", slug="royal-exhibition-building", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Royal Exhibition Building", sp="Ground Floor", pr="Carlton", ty="event",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=3, gr=0, area=6400, ceil=None, ceilq=None,
   s_name="Museum Plaza", s_th=None,
   note="A heritage exhibition hall in the Carlton Gardens with roughly 6,400 square metres of ground floor across the naves, transept and dome, plus nearly 7,850 square metres of open air plaza outside. Museums Victoria publishes floor areas and no setup capacities at all, so you will need a drawn floor plan from the venue before you can commit to a number.",
   src="https://museumsvictoria.com.au/venues-and-events/spaces-for-hire/royal-exhibition-building/ground-floor/",
   src2="https://museumsvictoria.com.au/venues-and-events/spaces-for-hire/royal-exhibition-building/"),

# ------------------------------------------------------------------- BRISBANE
 dict(
   city="Brisbane", slug="brisbane-convention-exhibition-centre", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Brisbane Convention & Exhibition Centre", sp="Great Hall", pr="South Bank", ty="conv",
   th=3958, bq=2800, cl=None, ck=4000, cab=None, ush=None, bd=None,
   br=44, gr=0, area=4088, ceil=None, ceilq=None,
   s_name="Plaza Ballroom", s_th=2000,
   note="The only building in Brisbane that puts a near 4,000 seat plenary, four exhibition halls of 5,000 square metres each and dozens of breakout rooms under one roof. It is the default for national and international association conferences that need the plenary and the trade floor running side by side.",
   src="https://bcec.com.au/wp-content/uploads/BCEC-Floor-plan-brochure.pdf",
   src2="https://bcec.com.au/organise/rooms-spaces/"),

 dict(
   city="Brisbane", slug="royal-international-convention-centre", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Royal International Convention Centre", sp="Halls A, B & C combined", pr="Bowen Hills", ty="conv",
   th=3176, bq=2080, cl=None, ck=3213, cab=1664, ush=None, bd=None,
   br=None, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Hall C", s_th=1080,
   note="A pillarless three hall conference and exhibition floor a kilometre and a half from the city, with a Rydges hotel on the same site. It is the practical alternative when BCEC is held, and the only large Brisbane conference venue with accommodation attached. Its diary is normally taken around the Ekka each August, so bring those dates to us early.",
   src="https://www.brisbaneshowgrounds.com.au/event-type/spaces/halls-a-b-c-combined/",
   src2="https://www.brisbaneshowgrounds.com.au/event-type/spaces/hall-c/"),

 dict(
   city="Brisbane", slug="the-star-brisbane-event-centre", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="The Star Brisbane Event Centre", sp="Event Centre Ballroom", pr="Queen's Wharf", ty="event",
   th=1800, bq=1440, cl=None, ck=1800, cab=None, ush=None, bd=None,
   br=None, gr=340, area=2000, ceil=6.0, ceilq=None,
   s_name="Event Centre breakout rooms", s_th=120,
   note="A pillarless ballroom that splits into five serviceable spaces, inside an integrated resort with a 340 room hotel, restaurants and bars in the same complex. It suits large gala dinners, awards nights and conferences where delegates never need to cross a road all week.",
   src="https://queenswharfbrisbane.com.au/wp-content/uploads/2024/08/240822_-The-Star-reveals-first-look-at-Event-Centre-with-one-week-until-opening.pdf",
   src2="https://queenswharfbrisbane.com.au/explore/event-centre/"),

 dict(
   city="Brisbane", slug="brisbane-city-hall", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Brisbane City Hall", sp="Main Auditorium", pr="King George Square", ty="event",
   th=1178, bq=660, cl=None, ck=1200, cab=594, ush=None, bd=None,
   br=11, gr=0, area=928, ceil=None, ceilq=None,
   s_name="Ithaca Auditorium", s_th=370,
   note="A 1930 heritage civic building with a domed auditorium in the middle of the city, run for events by a contract caterer. It is chosen for gala dinners, awards and ceremonial plenaries where the room itself is the point, and it is the wrong building for exhibition or a multi day breakout program.",
   src="https://www.epicure.com.au/brisbane-city-hall",
   src2="https://www.brisbane.qld.gov.au/things-to-see-and-do/council-venues-and-precincts/brisbane-city-hall"),

 dict(
   city="Brisbane", slug="sofitel-brisbane-central", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Sofitel Brisbane Central", sp="Ballroom Le Grand", pr="Brisbane CBD", ty="hotel",
   th=1056, bq=580, cl=550, ck=None, cab=440, ush=None, bd=None,
   br=11, gr=416, area=798, ceil=6.5, ceilq=None,
   s_name="Lyon 1 & 2", s_th=230,
   note="The largest hotel ballroom in Brisbane by published theatre capacity, in a 416 room hotel sitting directly above Central Station. It is the one building that runs a thousand delegate plenary, the breakouts and the accommodation without anyone crossing a road, and the station puts the airport 23 minutes away.",
   src="https://www.sofitelbrisbane.com.au/meetings-and-events/ballroom-le-grand",
   src2="https://www.sofitelbrisbane.com.au/meetings-and-events/our-spaces"),

 dict(
   city="Brisbane", slug="pullman-brisbane-king-george-square", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Pullman Brisbane King George Square", sp="Presidential Ballroom", pr="King George Square", ty="hotel",
   th=730, bq=500, cl=270, ck=1000, cab=None, ush=None, bd=None,
   br=11, gr=438, area=None, ceil=6.2, ceilq=None,
   s_name="Grand Windsor Ballroom", s_th=500,
   note="Two hotels, Pullman and Mercure, sharing one conference floor with 438 rooms between them and a ballroom that divides into three and takes 110 exhibition booths. It is the workhorse for a 400 to 700 delegate residential conference in the city centre.",
   src="https://www.pullmanbrisbanekgs.com.au/meetings/presidential-ballroom",
   src2="https://www.pullmanbrisbanekgs.com.au/meetings"),

 dict(
   city="Brisbane", slug="w-brisbane", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="W Brisbane", sp="Great Room", pr="North Quay", ty="hotel",
   th=600, bq=350, cl=333, ck=639, cab=None, ush=None, bd=None,
   br=9, gr=312, area=595, ceil=4.8, ceilq=None,
   s_name="SUN Deck", s_th=70,
   note="A 312 room design hotel on the river edge of the city with a divisible ballroom and an outdoor deck that takes 300 standing. It suits brand events, product launches and incentive dinners where the look of the room is doing part of the work.",
   src="https://www.marriott.com/en-us/hotels/bnewh-w-brisbane/events/",
   src2="https://www.marriott.com/en-us/hotels/bnewh-w-brisbane/overview/"),

 dict(
   city="Brisbane", slug="brisbane-powerhouse", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Brisbane Powerhouse", sp="Powerhouse Theatre", pr="New Farm", ty="event",
   th=525, bq=320, cl=None, ck=500, cab=None, ush=None, bd=None,
   br=8, gr=0, area=1320, ceil=None, ceilq=None,
   s_name="Turbine Platform", s_th=150,
   note="A former power station on the river at New Farm, run as an arts venue with a proper theatre and a fully retractable seating bank that reveals a 458 square metre flat floor. It suits conferences and launches that want a raw industrial room with real theatre infrastructure behind it, and it cannot be a raked theatre and a dinner room at the same time.",
   src="https://brisbanepowerhouse.org/events-functions/spaces/",
   src2="https://brisbanepowerhouse.org/for-artists/theatre-hire/"),

 dict(
   city="Brisbane", slug="howard-smith-wharves", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Howard Smith Wharves", sp="Felons Barrel Hall", pr="Howard Smith Wharves", ty="event",
   th=None, bq=424, cl=None, ck=800, cab=None, ush=None, bd=None,
   br=17, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Rivershed", s_th=None,
   note="Seventeen riverfront spaces under the Story Bridge, most of them bars, restaurants and heritage sheds rather than conference rooms. It is where the welcome function, the gala dinner or the launch goes, not the daytime plenary, and it publishes seated and standing numbers only.",
   src="https://howardsmithwharves.com/events/corporate-meetings-events/",
   src2="https://howardsmithwharves.com/events/venues/"),

 dict(
   city="Brisbane", slug="pullman-brisbane-airport", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Pullman Brisbane Airport", sp="LAX Gates 1-3", pr="Brisbane Airport", ty="hotel",
   th=330, bq=220, cl=100, ck=None, cab=None, ush=None, bd=None,
   br=12, gr=132, area=307, ceil=3.0, ceilq="low by conference standards, so check a staging plan first",
   s_name="JFK Gates 1-3", s_th=200,
   note="A 132 room hotel attached to the Brisbane Airport Conference Centre, sharing the site with the ibis and Novotel airport properties. It exists for fly in fly out board meetings, national sales conferences and training days where nobody needs to see the city.",
   src="https://accorevents.com/venues/pullman-brisbane-airport",
   src2="https://bneacc.com.au/meetings-events/"),

# ---------------------------------------------------------------------- PERTH
 dict(
   city="Perth", slug="perth-convention-and-exhibition-centre", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Perth Convention and Exhibition Centre", sp="Riverside Theatre", pr="Elizabeth Quay", ty="conv",
   th=2500, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=23, gr=0, area=None, ceil=10.0, ceilq="maximum clearance over the staging area, not across the seating bowl",
   s_name="BelleVue Ballroom", s_th=1700,
   note="The only building in Western Australia that combines a 2,500 seat tiered auditorium, a 1,700 seat ballroom and 16,644 square metres of exhibition pavilion under one roof, so a multi stream conference with a trade floor starts and usually ends here. The state government discontinued the redevelopment in November 2025, so what you inspect today is what you will get.",
   src="https://www.pcec.com.au/organisers/our-spaces/",
   src2="https://www.pcec.com.au/riverside-theatre/"),

 dict(
   city="Perth", slug="crown-perth", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Crown Perth", sp="Crown Ballroom", pr="Burswood", ty="resort",
   th=2400, bq=1510, cl=1150, ck=2400, cab=1216, ush=None, bd=None,
   br=None, gr=1188, area=2000, ceil=8.0, ceilq=None,
   s_name="Grand Ballroom", s_th=1800,
   note="The one place in Western Australia where a conference of 1,500 or more can meet, dine and sleep without leaving the site, with 1,188 rooms across three hotels and 33 food and drink outlets. The Crown Ballroom is a 2,000 square metre pillarless flat floor that splits into five, which makes it the default Perth gala room once the numbers pass what a city hotel can hold.",
   src="https://www.crownhotels.com.au/perth/events-conferences/venues/crown-ballroom",
   src2="https://www.crownperth.com.au/general/about-us"),

 dict(
   city="Perth", slug="optus-stadium", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Optus Stadium", sp="River View Rooms", pr="Burswood", ty="event",
   th=1500, bq=1200, cl=None, ck=2100, cab=800, ush=None, bd=None,
   br=None, gr=0, area=2121, ceil=6.0, ceilq="4.9m to 6m across the three sections",
   s_name="Black Swan Room", s_th=None,
   note="A stadium function floor on Level 3 West with floor to ceiling glass over the Swan River, three private bars and three private kitchens, splitting into three rooms from 557 up to 2,121 square metres. It is 15 minutes from Perth Airport with guaranteed car bays, which makes it work for conferences and dinners that do not need attached accommodation.",
   src="https://optusstadium.com.au/venue-hire-perth/perth-function-spaces/river-view-rooms",
   src2="https://optusstadium.com.au/venue-hire-perth/conferences"),

 dict(
   city="Perth", slug="hyatt-regency-perth", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Hyatt Regency Perth", sp="Grand Ballroom", pr="Adelaide Terrace", ty="hotel",
   th=1000, bq=600, cl=450, ck=950, cab=480, ush=None, bd=None,
   br=15, gr=None, area=870, ceil=6.0, ceilq=None,
   s_name="North Ballroom", s_th=350,
   note="An 870 square metre ballroom of 29.5 by 29.5 metres that divides into north and south halves, inside a hotel carrying more than 3,000 square metres of meeting space across fifteen rooms. The square footprint suits round table conferences better than a long room, and it is the largest hotel ballroom in the Perth city centre among properties that publish a capacity chart.",
   src="https://www.hyatt.com/content/dam/hotel/propertysites/assets/regency/perth/documents/en_us/home/PERTHCapacityChart.pdf",
   src2="https://www.hyatt.com/content/dam/hotel/propertysites/assets/regency/perth/documents/en_us/home/PERTHFacilityGuide.pdf"),

 dict(
   city="Perth", slug="the-westin-perth", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="The Westin Perth", sp="Grand Ballroom", pr="Hibernian Place", ty="hotel",
   th=840, bq=520, cl=540, ck=840, cab=None, ush=None, bd=None,
   br=11, gr=None, area=800, ceil=6.2, ceilq=None,
   s_name="Grand Ballroom 2", s_th=326,
   note="An 800 square metre ballroom that divides into three, supported by ten smaller rooms across 2,370 square metres of event space at the east end of the city. The 540 classroom figure is unusually high for the room size, which makes this a sensible pick for training format conferences that need desks rather than rounds.",
   src="https://www.marriott.com/en-us/hotels/perwi-the-westin-perth/events/",
   src2="https://www.marriott.com/en-us/hotels/perwi-the-westin-perth/overview/"),

 dict(
   city="Perth", slug="pan-pacific-perth", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Pan Pacific Perth", sp="Golden Ballroom", pr="Adelaide Terrace", ty="hotel",
   th=600, bq=320, cl=309, ck=600, cab=None, ush=None, bd=None,
   br=None, gr=488, area=560, ceil=4.0, ceilq=None,
   s_name="Grand River Ballroom", s_th=450,
   note="At 488 rooms this is one of the largest single property room blocks in the Perth city centre, with two separate pillarless ballrooms on a dedicated convention floor. A big block plus two independent plenary rooms is what makes it a working residential conference hotel rather than a hotel that also does meetings.",
   src="https://www.panpacific.com/en/hotels-and-resorts/pp-perth/meetings/meet-venues/golden-ballroom.html",
   src2="https://www.businesseventsperth.com/listing/pan-pacific-perth/1024/"),

 dict(
   city="Perth", slug="the-ritz-carlton-perth", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="The Ritz-Carlton, Perth", sp="Elizabeth Quay Ballroom", pr="Elizabeth Quay", ty="hotel",
   th=640, bq=400, cl=182, ck=500, cab=None, ush=62, bd=120,
   br=8, gr=205, area=550, ceil=5.0, ceilq=None,
   s_name="Bell Tower 1 & 2", s_th=100,
   note="A 550 square metre ballroom splitting into three, in a 205 room hotel on Elizabeth Quay across the road from the convention centre. It is the room to use when a 300 to 400 person dinner has to feel considered rather than large, and it doubles as the premium headquarters hotel for a convention centre conference.",
   src="https://www.ritzcarlton.com/en/hotels/perrz-the-ritz-carlton-perth/events/",
   src2="https://www.ritzcarlton.com/en/hotels/perrz-the-ritz-carlton-perth/events/"),

 dict(
   city="Perth", slug="rac-arena", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="RAC Arena", sp="Main Arena", pr="Wellington Street", ty="event",
   th=None, bq=None, cl=None, ck=2500, cab=None, ush=None, bd=None,
   br=5, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Granite Room", s_th=420,
   note="The arena floor is one of very few Perth spaces that will hold a 2,500 person standing reception, and it sits in the city with 680 car bays underneath it. Function rooms and the arena floor are released on non event days only, so availability follows the touring calendar rather than your date.",
   src="https://www.racarena.com.au/functions-venue-hire/",
   src2="https://www.racarena.com.au/functions-venue-hire/function-faqs/"),

 dict(
   city="Perth", slug="esplanade-hotel-fremantle-by-rydges", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Esplanade Hotel Fremantle by Rydges", sp="Southern Cross Gala Ballroom", pr="Fremantle", ty="hotel",
   th=1000, bq=700, cl=399, ck=1000, cab=560, ush=None, bd=None,
   br=None, gr=300, area=799, ceil=6.0, ceilq=None,
   s_name="Sirius Room", s_th=340,
   note="A 799 square metre ballroom with 300 rooms behind it, about half an hour from both Perth Airport and the city centre. It is the only Fremantle property we can verify at 1,000 theatre in a single room, so it is the answer when a client wants the port town rather than the city.",
   src="https://www.rydges.com/accommodation/perth-wa/esplanade-hotel-fremantle-by-rydges/meetings-events/all-venues/",
   src2="https://www.rydges.com/accommodation/perth-wa/esplanade-hotel-fremantle-by-rydges/"),

 dict(
   city="Perth", slug="sandalford-wines-swan-valley", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Sandalford Wines Swan Valley", sp="The Estate Room", pr="Swan Valley", ty="event",
   th=None, bq=350, cl=None, ck=400, cab=None, ush=None, bd=None,
   br=None, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Sandalera Room", s_th=None,
   note="A working winery estate about half an hour from the city with two indoor function rooms and open lawns, used for dinners, launches and day conferences rather than multi day residential programs. There is no accommodation on site, so an overnight program runs on coaches back to the city or to the Swan Valley properties nearby.",
   src="http://www.sandalford.com/images/F069_214848_SANDWIN_Wedding_Package_Feb_2024_Web.pdf",
   src2="https://www.sandalford.com/functions/corporate"),

# ------------------------------------------------------------------- ADELAIDE
 dict(
   city="Adelaide", slug="adelaide-convention-centre", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Adelaide Convention Centre", sp="Hall ABCD", pr="Riverbank", ty="conv",
   th=3017, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=27, gr=0, area=2544, ceil=None, ceilq=None,
   s_name="Hall H", s_th=3000,
   note="The state's only purpose built convention centre, and where any Adelaide conference over about 800 delegates ends up. Hall ABCD is the tiered plenary for the big general sessions, while the flat floor Hall H next door at 2,980 square metres is the room you use for the exhibition and the gala banquet.",
   src="https://www.adelaidecc.com.au/spaces/hall-abcd/",
   src2="https://www.adelaidecc.com.au/wp-content/uploads/2025/07/Exhibition-Handbook-2025-2026.pdf"),

 dict(
   city="Adelaide", slug="adelaide-showground", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Adelaide Showground", sp="Jubilee Pavilion", pr="Wayville", ty="event",
   th=7000, bq=None, cl=None, ck=3000, cab=None, ush=None, bd=None,
   br=None, gr=0, area=8742, ceil=None, ceilq=None,
   s_name="Goyder Pavilion", s_th=5000,
   note="The only site in Adelaide with genuine large format exhibition floor, and the two main pavilions combine to 17,250 square metres. It is a hall and hardstand operation on a 27 hectare site rather than a delegate experience building, so plan for shuttles and a build rather than a walk from a hotel.",
   src="https://www.adelaideshowground.com.au/jubilee-pavilion",
   src2="https://www.adelaideshowground.com.au/goyder-pavilion"),

 dict(
   city="Adelaide", slug="adelaide-oval", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Adelaide Oval", sp="William Magarey Room", pr="Riverbank", ty="event",
   th=1450, bq=800, cl=None, ck=1500, cab=600, ush=None, bd=None,
   br=25, gr=138, area=None, ceil=None, ceilq=None,
   s_name="Ian McLachlan Room", s_th=700,
   note="A stadium with 25 function spaces stacked through the stands and a 138 room hotel built into the building. The Magarey Room on Level 3 of the Riverbank Stand is the room people actually book for large dinners and awards nights, and it will take a conference plenary up to 1,450.",
   src="https://www.adelaideoval.com.au/venues/william-magarey-room/",
   src2="https://www.adelaideoval.com.au/our-venues/"),

 dict(
   city="Adelaide", slug="amora-hotel-adelaide", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Amora Hotel Adelaide", sp="Grand Ballroom", pr="Victoria Square", ty="hotel",
   th=780, bq=570, cl=342, ck=800, cab=440, ush=None, bd=None,
   br=19, gr=380, area=None, ceil=5.8, ceilq=None,
   s_name="Victoria Room", s_th=200,
   note="The largest residential conference hotel in the Adelaide city centre, with 380 rooms and nineteen meeting rooms on one conference floor. This was the Hilton Adelaide until the rebrand, and the ballroom carries 500kg rigging points and motorised screens, so it handles a produced plenary without an external build.",
   src="https://www.amorahotels.com/adelaide/meetings-events/venues/grand-ballroom",
   src2="https://www.amorahotels.com/adelaide"),

 dict(
   city="Adelaide", slug="intercontinental-adelaide", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="InterContinental Adelaide", sp="The Ballroom", pr="Riverbank", ty="hotel",
   th=500, bq=360, cl=255, ck=500, cab=288, ush=63, bd=42,
   br=6, gr=367, area=480, ceil=None, ceilq=None,
   s_name="Banksia 1, 2 & Terrace", s_th=160,
   note="A 367 room hotel on North Terrace beside the Torrens, and the closest full service accommodation block to the convention centre and Adelaide Oval. The pillarless ballroom with its 280 square metre prefunction area is the standard choice for a hosted dinner attached to a conference held elsewhere on the Riverbank.",
   src="https://icadelaide.com.au/meeting-spaces-adelaide/",
   src2="https://southaustralia.com/products/adelaide/accommodation/intercontinental-adelaide"),

 dict(
   city="Adelaide", slug="eos-by-skycity", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Eos by SkyCity", sp="SkyCity Ballroom", pr="Festival Plaza", ty="hotel",
   th=None, bq=450, cl=None, ck=600, cab=None, ush=None, bd=None,
   br=None, gr=120, area=None, ceil=None, ceilq=None,
   s_name="SouthWest Suite", s_th=None,
   note="A 120 room luxury hotel above SkyCity on Festival Plaza, next to the Festival Centre and a short walk from the convention centre. The ballroom divides in two and is used mainly for premium dinners and receptions rather than as a working conference floor.",
   src="https://skycityadelaide.com.au/events-ballroom-meeting-rooms/",
   src2="https://southaustralia.com/products/adelaide/accommodation/eos-by-skycity"),

 dict(
   city="Adelaide", slug="national-wine-centre-of-australia", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="National Wine Centre of Australia", sp="Hickinbotham Hall", pr="Botanic Gardens", ty="event",
   th=450, bq=350, cl=None, ck=600, cab=280, ush=None, bd=None,
   br=6, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Exhibition Hall", s_th=238,
   note="A dedicated events building on the edge of the Botanic Gardens, built around wine as its subject, with six function spaces and no accommodation. It is the room to use when you want a mid size Adelaide dinner or conference to feel like South Australia rather than like a hotel.",
   src="https://www.nationalwinecentre.com.au/venues/hickinbotham-hall",
   src2="https://www.nationalwinecentre.com.au/venues/exhibition-hall"),

 dict(
   city="Adelaide", slug="adelaide-hills-convention-centre", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Adelaide Hills Convention Centre", sp="Upper Level", pr="Hahndorf", ty="conv",
   th=350, bq=250, cl=None, ck=400, cab=200, ush=None, bd=None,
   br=7, gr=None, area=409, ceil=None, ceilq=None,
   s_name="Lower Level", s_th=None,
   note="A purpose built conference building at Hahndorf with accommodation at the adjacent holiday park and a stated maximum of 400. It exists for residential conferences and multi day workshops that want to be out of the city without losing proper breakout rooms.",
   src="https://discoveryevents.com.au/venues/adelaide-hills-convention-centre",
   src2="https://discoveryevents.com.au/venues/adelaide-hills-convention-centre"),

 dict(
   city="Adelaide", slug="novotel-barossa-valley-resort", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Novotel Barossa Valley Resort", sp="Shiraz Room", pr="Barossa Valley", ty="resort",
   th=250, bq=180, cl=None, ck=250, cab=None, ush=None, bd=None,
   br=9, gr=140, area=None, ceil=None, ceilq=None,
   s_name="Cabernet Room", s_th=None,
   note="The property in the Barossa with enough rooms to hold a whole conference on site, at 140 rooms and nine meeting rooms looking over the vineyards at Rowland Flat. The stated maximum is 250 delegates, so it is a leadership offsite and mid size residential venue rather than a conference centre.",
   src="https://www.novotelbarossa.com/meetings",
   src2="https://www.novotelbarossa.com/"),

 dict(
   city="Adelaide", slug="serafino-mclaren-vale", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Serafino McLaren Vale", sp="McLarens Room", pr="McLaren Vale", ty="resort",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=6, gr=30, area=None, ceil=None, ceilq=None,
   s_name="The Courtyard", s_th=None,
   note="A working winery about forty minutes south of the city with 30 self contained rooms and six function spaces, the largest published only as 300 people without a stated setup. It is the McLaren Vale option when you want the group to stay on the estate rather than bus back to Adelaide.",
   src="https://serafinowines.com.au/functions/conferences",
   src2="https://serafinowines.com.au/accommodation/"),

# ------------------------------------------------------------------- CANBERRA
 dict(
   city="Canberra", slug="national-convention-centre-canberra", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="National Convention Centre Canberra", sp="Royal Theatre", pr="City / Civic", ty="conv",
   th=2460, bq=540, cl=400, ck=750, cab=432, ush=None, bd=None,
   br=None, gr=0, area=749, ceil=None, ceilq=None,
   s_name="Exhibition Hall", s_th=1775,
   note="Canberra's purpose built conference building and the default home for national association and government conferences of 500 to 2,000 delegates. The Royal Theatre gives you 1,710 tiered seats that no Canberra hotel can match, but the 2,000 square metre Exhibition Hall is the ceiling on any trade display running alongside it.",
   src="https://nccc.com.au/convention-venue-canberra/",
   src2="https://nccc.com.au/event-venues/royal-theatre/"),

 dict(
   city="Canberra", slug="exhibition-park-in-canberra", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Exhibition Park in Canberra", sp="Budawang Pavilion", pr="Mitchell", ty="event",
   th=3000, bq=1900, cl=None, ck=3310, cab=None, ush=None, bd=None,
   br=None, gr=0, area=3310, ceil=7.5, ceilq=None,
   s_name="Coorong Pavilion", s_th=1800,
   note="A showground pavilion complex rather than a conference centre, and the answer for trade shows, expos and large format events that will not fit inside the convention centre. You bring in everything including the fit out, and there is no accommodation or walkable dining on site.",
   src="https://exhibitionparkincanberra.com.au/planning/venues-and-spaces/",
   src2="https://exhibitionparkincanberra.com.au/planning/venues-and-spaces/"),

 dict(
   city="Canberra", slug="qt-canberra", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="QT Canberra", sp="QT Grand Ballroom", pr="City / New Acton", ty="hotel",
   th=1000, bq=600, cl=336, ck=1000, cab=550, ush=None, bd=None,
   br=None, gr=205, area=830, ceil=None, ceilq=None,
   s_name="Eureka", s_th=200,
   note="The only Canberra hotel that seats a thousand in one pillarless room and puts a meaningful share of the delegates upstairs, which makes it the standard choice for a residential conference under one roof. The ballroom divides into thirds and there is a dedicated events floor with further rooms for concurrent streams.",
   src="https://cdn.qthotels.com/wp-content/uploads/sites/95/2026/02/16142844/QTC_CEKit_2026-1.pdf",
   src2="https://www.qthotels.com/canberra/venues-events/meetings-events/"),

 dict(
   city="Canberra", slug="hotel-realm", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Hotel Realm", sp="National Ballroom", pr="Barton", ty="hotel",
   th=800, bq=500, cl=400, ck=800, cab=400, ush=None, bd=None,
   br=None, gr=163, area=690, ceil=None, ceilq=None,
   s_name="National Ballroom 2 & 3", s_th=550,
   note="The working conference hotel for anything with a Parliament House, department or peak body agenda, sitting in Barton a few minutes from the Parliamentary Triangle. The ballroom divides four ways and has floor to ceiling windows and terraces, so it runs a conference by day and a dinner the same night without a reset elsewhere.",
   src="https://hotelrealm.com.au/functions/national-ballroom/",
   src2="https://hotelrealm.com.au/"),

 dict(
   city="Canberra", slug="hyatt-hotel-canberra", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Hyatt Hotel Canberra", sp="Federation Ballroom", pr="Yarralumla", ty="hotel",
   th=500, bq=340, cl=260, ck=600, cab=None, ush=100, bd=None,
   br=9, gr=None, area=504, ceil=5.5, ceilq=None,
   s_name="Centenary Ballroom", s_th=200,
   note="The heritage property Canberra uses when the occasion has to feel formal, and the usual answer for a gala dinner, an awards night or a small ministerial gathering. It is a five minute drive from the Parliamentary Triangle rather than a walk from Civic, so it works better as a self contained residential venue than as overflow for a convention centre conference.",
   src="https://www.hyatt.com/content/dam/hotel/propertysites/assets/park/canbe/documents/en_US/home/CANBECapacityChart.pdf",
   src2="https://www.hyatt.com/park-hyatt/en-US/canbe-hyatt-hotel-canberra-a-park-hyatt-hotel/meetings"),

 dict(
   city="Canberra", slug="national-museum-of-australia", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="National Museum of Australia", sp="Gandel Atrium", pr="Acton Peninsula", ty="event",
   th=500, bq=500, cl=None, ck=1000, cab=None, ush=None, bd=None,
   br=None, gr=0, area=1543, ceil=None, ceilq=None,
   s_name="Peninsula Room", s_th=250,
   note="The largest single function room among the national institutions, and the one that takes a 500 seat conference dinner or a thousand guest reception on the lake. It is an after hours proposition around a working museum, so bump in windows are tight and it belongs in the program as a dinner venue rather than a conference base.",
   src="https://www.nma.gov.au/about/venue-hire",
   src2="https://www.nma.gov.au/about/venue-hire"),

 dict(
   city="Canberra", slug="national-gallery-of-australia", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="National Gallery of Australia", sp="Gandel Hall", pr="Parliamentary Triangle", ty="event",
   th=400, bq=360, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=None, gr=0, area=None, ceil=None, ceilq=None,
   s_name="James Fairfax Theatre", s_th=244,
   note="The gala dinner room of the Parliamentary Triangle, with a built in stage, a ramp and floor to ceiling windows onto the Australian Garden. Pairing Gandel Hall with the 244 seat James Fairfax Theatre gives you a plenary and a dinner on one site, which suits a one day summit or an awards program more than a multi day conference.",
   src="https://nga.gov.au/about-us/venue-hire/",
   src2="https://nga.gov.au/about-us/venue-hire/"),

 dict(
   city="Canberra", slug="australian-war-memorial", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Australian War Memorial", sp="Anzac Atrium", pr="Campbell", ty="event",
   th=None, bq=400, cl=None, ck=700, cab=None, ush=None, bd=None,
   br=None, gr=0, area=None, ceil=None, ceilq=None,
   s_name="BAE Systems Theatre", s_th=251,
   note="An evening only venue set among large military objects, used for commemorative programs, defence sector functions and corporate dinners where the setting carries the meaning. The Memorial declines celebratory bookings and the site has been through a multi year redevelopment, so confirm current space availability at the time of enquiry.",
   src="https://www.awm.gov.au/venue-hire",
   src2="https://www.awm.gov.au/venue-hire"),

 dict(
   city="Canberra", slug="museum-of-australian-democracy", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Museum of Australian Democracy at Old Parliament House", sp="King's Hall", pr="Parliamentary Triangle", ty="event",
   th=None, bq=None, cl=None, ck=500, cab=None, ush=None, bd=None,
   br=None, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Members' Dining Room", s_th=230,
   note="The old federal chamber building, where King's Hall is a standing reception space quoted from 80 to 500 guests rather than a conference room. The Members' Dining Rooms and the two courtyards give you seated dinners and breakout sessions on the same site, which suits association and government programs that want the political setting.",
   src="https://www.moadoph.gov.au/venue-hire",
   src2="https://www.moadoph.gov.au/venue-hire"),

 dict(
   city="Canberra", slug="national-arboretum-canberra", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="National Arboretum Canberra", sp="Village Centre", pr="Molonglo Valley", ty="event",
   th=None, bq=500, cl=None, ck=700, cab=None, ush=None, bd=None,
   br=None, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Margaret Whitlam Pavilion", s_th=None,
   note="An after hours venue only, because the site closes to the public at four and setup starts from then, which rules it out for a daytime conference. What it gives you is a 500 seat dinner room with a panorama over Lake Burley Griffin and the city, about ten minutes from Civic by car.",
   src="https://www.nationalarboretum.act.gov.au/venue-hire/village-centre",
   src2="https://www.nationalarboretum.act.gov.au/venue-hire/margaret-whitlam-pavilion"),

# --------------------------------------------------------------------- HOBART
 dict(
   city="Hobart", slug="hotel-grand-chancellor-hobart", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Hotel Grand Chancellor Hobart", sp="Federation Ballroom", pr="Hobart CBD", ty="conv",
   th=1200, bq=770, cl=528, ck=1000, cab=None, ush=None, bd=None,
   br=11, gr=243, area=1225, ceil=5.2, ceilq=None,
   s_name="Federation Concert Hall", s_th=1100,
   note="The one building in Hobart that takes a full scale conference plenary, an exhibition and a gala in the same complex without moving delegates. The flat floor Federation Ballroom and the tiered Federation Concert Hall are separate spaces, so you can run the plenary and the catering at the same time rather than turning a room.",
   src="https://www.grandchancellorhotels.com/hotel-grand-chancellor-hobart/meetings-events/venues",
   src2="https://hcecgrandchancellor.com/floorplan/"),

 dict(
   city="Hobart", slug="wrest-point", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Wrest Point", sp="Tasman Room", pr="Sandy Bay", ty="hotel",
   th=1000, bq=540, cl=300, ck=800, cab=320, ush=120, bd=None,
   br=24, gr=271, area=691, ceil=None, ceilq=None,
   s_name="Plenary Hall", s_th=651,
   note="A self contained residential conference campus with the largest single site room block in Hobart, a casino and several food outlets on the property. Combining the Tasman Room with the tiered Plenary Hall gives 1,651 theatre, the largest configuration in the state, and it is in Sandy Bay rather than the city, so delegates stay on site in the evenings.",
   src="https://wrestpoint.com.au/hobart-venues/tasman-room/",
   src2="https://wrestpoint.com.au/wp-content/uploads/2026/05/MAR2-2278_WP_Conference-Events-26_27.pdf"),

 dict(
   city="Hobart", slug="crowne-plaza-hobart", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Crowne Plaza Hobart", sp="Centurion Ballroom", pr="Hobart CBD", ty="hotel",
   th=600, bq=350, cl=282, ck=600, cab=280, ush=None, bd=None,
   br=8, gr=241, area=600, ceil=3.5, ceilq=None,
   s_name="Centurion 1", s_th=210,
   note="The most straightforward mid size residential conference hotel in the city, with eight event spaces on one property and 241 rooms above them. The ballroom divides into three, which suits a plenary plus concurrent breakouts without booking a second building.",
   src="https://hobart.crowneplaza.com/conference-and-events/",
   src2="https://betasmania.com.au/suppliers/crowne-plaza/"),

 dict(
   city="Hobart", slug="the-tasman-luxury-collection", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="The Tasman, a Luxury Collection Hotel", sp="LUMINA", pr="Parliament Square", ty="hotel",
   th=180, bq=190, cl=156, ck=220, cab=None, ush=60, bd=None,
   br=5, gr=152, area=270, ceil=4.0, ceilq=None,
   s_name="Drawing Room", s_th=110,
   note="A premium hotel for board level and incentive programs rather than volume conferences, combining 1840s Georgian and 1940s Art Deco buildings with a 2020 pavilion. LUMINA is column free, so sightlines and staging are clean for an awards dinner or a launch.",
   src="https://www.marriott.com/en-us/hotels/hbalc-the-tasman-a-luxury-collection-hotel-hobart/events/",
   src2="https://betasmania.com.au/suppliers/the-tasman-a-luxury-collection-hotel-hobart/"),

 dict(
   city="Hobart", slug="princes-wharf-1", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Princes Wharf 1", sp="The Shed", pr="Sullivans Cove", ty="event",
   th=None, bq=1200, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=3, gr=0, area=None, ceil=None, ceilq=None,
   s_name="The Forecourt", s_th=None,
   note="A bare waterfront shed on Sullivans Cove taking up to 200 trade booths and a gala dinner for 1,200, with three phase power and a commercial kitchen. Everything else is a build, so budget for full production, and check the calendar because the venue hosts the summer waterfront festival over the New Year period.",
   src="https://www.princeswharf1.com.au/venue-hire/",
   src2="https://betasmania.com.au/suppliers/princes-wharf-no-1/"),

 dict(
   city="Hobart", slug="mona", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Mona", sp="The Nolan Gallery", pr="Berriedale", ty="event",
   th=None, bq=None, cl=None, ck=450, cab=None, ush=None, bd=8,
   br=None, gr=8, area=None, ceil=None, ceilq=None,
   s_name="The Void", s_th=None,
   note="A museum that hires its galleries for standing events, reached by road in about fifteen minutes or by catamaran from Brooke Street Pier in about twenty five. It is a destination experience rather than a working conference venue, so use it for the one night of the program people will remember.",
   src="https://mona.net.au/eat-drink/functions",
   src2="https://betasmania.com.au/suppliers/mona/"),

 dict(
   city="Hobart", slug="macq-01-hotel", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="MACq 01 Hotel", sp="The Promenade Room", pr="Hunter Street", ty="hotel",
   th=None, bq=60, cl=None, ck=100, cab=None, ush=None, bd=None,
   br=None, gr=114, area=None, ceil=None, ceilq=None,
   s_name="Old Wharf Restaurant", s_th=None,
   note="A waterfront hotel with function capability sized for hosted dinners and small breakouts rather than conference sessions. Use it as the delegate hotel or the private dining venue on a program whose plenary sits elsewhere.",
   src="https://www.macq01.com.au/plan-an-event/",
   src2="https://betasmania.com.au/suppliers/macq-01-hotel/"),

 dict(
   city="Hobart", slug="utas-university-centre", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="University of Tasmania University Centre", sp="Stanley Burbury Theatre", pr="Sandy Bay", ty="uni",
   th=349, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=4, gr=0, area=422, ceil=None, ceilq=None,
   s_name="Theatre 2", s_th=220,
   note="The largest lecture theatre on the Sandy Bay campus, bookable with an adjoining overflow theatre for a combined 569 and a foyer for catering. It suits academic and association meetings that want fixed tiered seating and a campus setting rather than hotel function rooms.",
   src="https://www.utas.edu.au/campus-services/venue-hire/available-venues/sandy-bay/university-centre",
   src2="https://www.utas.edu.au/campus-services/venue-hire/available-venues"),

 dict(
   city="Hobart", slug="saffire-freycinet", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Saffire Freycinet", sp="The Boardroom", pr="Freycinet", ty="resort",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=24,
   br=None, gr=20, area=None, ceil=None, ceilq=None,
   s_name=None, s_th=None,
   note="A twenty suite lodge on the east coast that works as a whole property buyout for an executive group of about forty, roughly two and a half hours from Hobart by road. The meeting space is a boardroom for 24, so this is a leadership retreat or an incentive reward rather than a conference.",
   src="https://betasmania.com.au/suppliers/saffire-freycinet/",
   src2="https://www.saffire-freycinet.com.au/all-inclusive-suites/"),

 dict(
   city="Hobart", slug="peppers-cradle-mountain-lodge", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Peppers Cradle Mountain Lodge", sp="Cradle Room", pr="Cradle Mountain", ty="resort",
   th=85, bq=68, cl=60, ck=None, cab=None, ush=30, bd=None,
   br=3, gr=86, area=85, ceil=None, ceilq=None,
   s_name="Pencil Pine Room", s_th=40,
   note="An 86 cabin wilderness lodge with three meeting rooms, the largest taking 85 theatre, used for offsites that want the national park on the doorstep. It is a long transfer from Hobart and closer to Launceston, so it works as a standalone retreat rather than a Hobart conference extension.",
   src="https://www.cradlemountainlodge.com.au/meetings-and-weddings/conferences/",
   src2="https://www.peppers.com.au/cradle-mountain-lodge/conferences/"),

# --------------------------------------------------------------------- DARWIN
 dict(
   city="Darwin", slug="darwin-convention-centre", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Darwin Convention Centre", sp="Exhibition Halls 1 to 4", pr="Darwin Waterfront", ty="conv",
   th=3660, bq=2740, cl=None, ck=4700, cab=2024, ush=None, bd=None,
   br=None, gr=0, area=4000, ceil=9.3, ceilq="in Halls 2 to 4; Hall 1 is 12m",
   s_name="Auditorium", s_th=1236,
   note="The only building in the Territory that holds a full plenary and a trade exhibition under one roof at the same time. The halls take 225 booths at 20kPa floor loading with a 1,500 square metre dock, and the tiered auditorium runs the plenary while the halls stay set.",
   src="https://www.darwinconvention.com.au/plan-an-event/capacities/",
   src2="https://www.darwinconvention.com.au/plan-an-event/capacities/"),

 dict(
   city="Darwin", slug="doubletree-by-hilton-esplanade-darwin", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="DoubleTree by Hilton Hotel Esplanade Darwin", sp="Grand Ballroom", pr="The Esplanade", ty="hotel",
   th=410, bq=320, cl=100, ck=410, cab=None, ush=60, bd=None,
   br=None, gr=197, area=502, ceil=None, ceilq=None,
   s_name="Reflections Room", s_th=120,
   note="The residential conference hotel in Darwin, with 197 rooms and 908 square metres of event space in the same building. The ballroom splits into two halves and there are four further breakout rooms, so a 200 to 350 delegate conference runs end to end without delegates leaving the property.",
   src="https://www.hilton.com/en/hotels/drweddi-doubletree-esplanade-darwin/events/",
   src2="https://www.hilton.com/en/hotels/drweddi-doubletree-esplanade-darwin/events/"),

 dict(
   city="Darwin", slug="hilton-darwin", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Hilton Darwin", sp="Grand Ballroom", pr="Mitchell Street", ty="hotel",
   th=250, bq=150, cl=120, ck=320, cab=None, ush=40, bd=None,
   br=4, gr=233, area=251, ceil=None, ceilq=None,
   s_name="Signatures", s_th=160,
   note="One of the largest room blocks in the Darwin city centre at 233 rooms, on Mitchell Street rather than at the Waterfront. Four event rooms totalling 663 square metres make it a room block partner for a convention centre conference more often than a standalone conference venue.",
   src="https://www.hilton.com/en/hotels/drwhdhi-hilton-darwin/events/",
   src2="https://www.hilton.com/en/hotels/drwhdhi-hilton-darwin/hotel-location/"),

 dict(
   city="Darwin", slug="mindil-beach-casino-resort", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Mindil Beach Casino Resort", sp="Beachside Pavilion", pr="Mindil Beach", ty="resort",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=9, gr=None, area=800, ceil=None, ceilq=None,
   s_name="Grand Ballroom", s_th=None,
   note="The resort option, on Mindil Beach away from the city, and the property to look at when the brief calls for a gala dinner or an outdoor beachfront element rather than a plenary. It states it caters for conferences up to 500 delegates and publishes floor areas rather than per setup capacities, so every layout needs confirming.",
   src="https://www.mindilbeachcasinoresort.com.au/functions/venues",
   src2="https://www.mindilbeachcasinoresort.com.au/functions/meetings-and-conferences"),

 dict(
   city="Darwin", slug="vibe-hotel-darwin-waterfront", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Vibe Hotel Darwin Waterfront", sp="Neptuna and Mavie", pr="Darwin Waterfront", ty="hotel",
   th=100, bq=80, cl=50, ck=100, cab=64, ush=36, bd=None,
   br=4, gr=120, area=None, ceil=None, ceilq=None,
   s_name="Mavie", s_th=50,
   note="The walk to the convention centre hotel, with 120 rooms inside the Waterfront precinct. Its four meeting rooms are breakout scale at fifty theatre each, pairing to a hundred, so it works as convention centre overflow and accommodation rather than as a main conference venue.",
   src="https://meetings.tfehotels.com/darwin-city--northern-territory/vibe-hotel-darwin-waterfront.html",
   src2="https://www.tfehotels.com/en/hotels/vibe-hotels/darwin-waterfront/conferences-events/"),

 dict(
   city="Darwin", slug="novotel-darwin-cbd", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Novotel Darwin CBD", sp="Brolga Room", pr="The Esplanade", ty="hotel",
   th=110, bq=100, cl=60, ck=None, cab=None, ush=40, bd=45,
   br=2, gr=140, area=116, ceil=3.0, ceilq=None,
   s_name="Billabong Room", s_th=70,
   note="A 140 room hotel with two ground floor function rooms, both opening onto the pool terrace. This is the size that suits a single stream meeting of a hundred or a board and executive session, not a multi stream conference.",
   src="https://accorevents.com/venues/novotel-darwin-cbd",
   src2="https://www.novoteldarwinatrium.com.au/meetings-events/"),

 dict(
   city="Darwin", slug="magnt-darwin", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Museum and Art Gallery of the Northern Territory", sp="MAGNT Theatrette", pr="Bullocky Point", ty="event",
   th=115, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=4, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Maritime Undercroft", s_th=None,
   note="The cultural venue in the market, on the coast at Bullocky Point, used for the evening and offsite parts of a program rather than the conference itself. It publishes a 115 seat theatrette, an undercroft taking up to 150 guests, an amphitheatre and front lawns over the Arafura Sea for larger receptions.",
   src="https://www.magnt.net.au/venue-hire",
   src2="https://www.magnt.net.au/venue-hire"),

# ----------------------------------------------------------------- GOLD COAST
 dict(
   city="Gold Coast", slug="gold-coast-convention-and-exhibition-centre", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Gold Coast Convention and Exhibition Centre", sp="Full Arena", pr="Broadbeach", ty="conv",
   th=6020, bq=1640, cl=1620, ck=2600, cab=None, ush=None, bd=157,
   br=22, gr=0, area=2182, ceil=14.0, ceilq="in the arena; the four exhibition halls are 10m",
   s_name="Exhibition Halls 1 to 4", s_th=None,
   note="The only building on the Gold Coast that seats several thousand delegates in one room, and the arena is tiered so the sightlines hold at full capacity. The four exhibition halls are a separate 6,345 square metre flat floor block taking 330 booths, so treat the plenary and the exhibition as two different decisions.",
   src="https://www.gccec.com.au/event-spaces-and-places.html",
   src2="https://www.gccec.com.au/virtual-floor-plan.html"),

 dict(
   city="Gold Coast", slug="the-star-gold-coast", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="The Star Gold Coast", sp="The Pavilion Convention Centre", pr="Broadbeach", ty="hotel",
   th=2300, bq=1200, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=13, gr=830, area=1600, ceil=None, ceilq=None,
   s_name=None, s_th=None,
   note="An integrated resort with a 1,600 square metre pillarless convention floor sitting on top of its own accommodation, restaurants and casino, joined to the convention centre by a pedestrian bridge. It is the practical choice when a thousand to two thousand delegates should live entirely inside one complex.",
   src="https://www.star.com.au/goldcoast/functions/conference-venues",
   src2="https://experiencegoldcoast.com/business-events/find-a-supplier/the-star-entertainment-group"),

 dict(
   city="Gold Coast", slug="racv-royal-pines-resort", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="RACV Royal Pines Resort", sp="Royal Benowa Ballroom", pr="Benowa", ty="resort",
   th=1540, bq=880, cl=None, ck=1800, cab=None, ush=None, bd=None,
   br=15, gr=333, area=1500, ceil=None, ceilq=None,
   s_name="Monarch", s_th=None,
   note="A self contained inland conference resort on a golf course, built around a 1,500 square metre pillarless ballroom that divides into three. It is the Gold Coast's main option for a large residential conference that wants everything on one campus and is not trying to be on the beach.",
   src="https://www.racv.com.au/travel-experiences/venue-hire/conferences/royal-pines-gold-coast/events-spaces.html",
   src2="https://experiencegoldcoast.com/business-events/find-a-supplier/racv-royal-pines-resort-gold-coast"),

 dict(
   city="Gold Coast", slug="hota-home-of-the-arts", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="HOTA, Home of the Arts", sp="Theatre 1", pr="Bundall", ty="event",
   th=1121, bq=180, cl=None, ck=250, cab=None, ush=None, bd=None,
   br=15, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Lakeside Room", s_th=500,
   note="A purpose built arts campus with a 1,121 seat theatre in fixed tiered seating, a flat floor function room, galleries, cinemas and an outdoor stage that holds up to 5,000 standing. It is the venue to use when a conference wants a plenary that does not look like a conference, or a brand event needs a stage and a gallery on one site.",
   src="https://www.hota.com.au/venue-hire/",
   src2="https://www.hota.com.au/venue-hire/"),

 dict(
   city="Gold Coast", slug="sheraton-grand-mirage-resort-gold-coast", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Sheraton Grand Mirage Resort, Gold Coast", sp="Mirage Grand Ballroom", pr="Main Beach", ty="resort",
   th=1000, bq=550, cl=None, ck=1000, cab=None, ush=None, bd=None,
   br=12, gr=295, area=None, ceil=None, ceilq=None,
   s_name="Horizons", s_th=None,
   note="A beachfront resort on The Spit with 1,335 square metres of event space and a ballroom that divides into five breakout rooms. It suits a residential conference of a few hundred that wants the plenary, the accommodation and the beach on one site, with outdoor lawns that carry a 400 seat dinner.",
   src="https://www.marriott.com/en-us/hotels/oolgs-sheraton-grand-mirage-resort-gold-coast/events/",
   src2="https://experiencegoldcoast.com/business-events/find-a-supplier/sheraton-grand-mirage-resort-gold-coast"),

 dict(
   city="Gold Coast", slug="sea-world-resort", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Sea World Resort", sp="Conference Centre", pr="Main Beach", ty="resort",
   th=1000, bq=450, cl=None, ck=1000, cab=None, ush=None, bd=None,
   br=10, gr=403, area=750, ceil=None, ceilq=None,
   s_name=None, s_th=None,
   note="A 403 room resort on The Spit with a 750 square metre pillarless conference centre that divides into three rooms. Its real value to a planner is the theme park attached to it, which gives a residential conference an exclusive access evening without a coach transfer.",
   src="https://experiencegoldcoast.com/business-events/find-a-supplier/sea-world-resort",
   src2="https://seaworldresort.com.au/conferences"),

 dict(
   city="Gold Coast", slug="jw-marriott-gold-coast-resort-and-spa", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="JW Marriott Gold Coast Resort & Spa", sp="JW Grand Ballroom", pr="Surfers Paradise", ty="resort",
   th=800, bq=500, cl=460, ck=1000, cab=320, ush=110, bd=None,
   br=13, gr=238, area=680, ceil=5.3, ceilq=None,
   s_name="Tamborine Gallery", s_th=220,
   note="A 238 room resort on Ferny Avenue with a 680 square metre pillarless ballroom rigged with a three tonne hoist, plus ten breakout rooms. It is the strongest Surfers Paradise option for a residential conference in the 300 to 700 range that also needs a serious gala dinner in the same building.",
   src="https://www.marriott.com/content/dam/marriott-digital/jw/apec/hws/o/oolsp/en_us/document/assets/jw-oolsp-meeting-planner-guide-22-35162.pdf",
   src2="https://www.marriott.com/en-us/hotels/oolsp-jw-marriott-gold-coast-resort-and-spa/overview/"),

 dict(
   city="Gold Coast", slug="the-langham-gold-coast", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="The Langham, Gold Coast", sp="Diamond Ballroom", pr="Surfers Paradise", ty="hotel",
   th=576, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=11, gr=169, area=618, ceil=6.0, ceilq=None,
   s_name=None, s_th=None,
   note="A 169 room beachfront hotel on Old Burleigh Road with a 618 square metre ballroom under six metre ceilings and ten breakout rooms. The ceiling height and the room count together make it a sensible fit for a mid size executive conference or an awards dinner where production values matter more than headcount.",
   src="https://www.langhamhotels.com/en/the-langham/gold-coast/events/meetings/",
   src2="https://www.langhamhotels.com/en/the-langham/gold-coast/"),

 dict(
   city="Gold Coast", slug="intercontinental-sanctuary-cove-resort", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="InterContinental Sanctuary Cove Resort", sp="MacArthur's Ballroom", pr="Sanctuary Cove", ty="resort",
   th=500, bq=250, cl=300, ck=400, cab=240, ush=80, bd=80,
   br=15, gr=251, area=437, ceil=None, ceilq=None,
   s_name="The Grange", s_th=300,
   note="A 251 room resort inside a gated marina and golf estate on 4.2 hectares, roughly half an hour north of the beachfront precincts. The closed campus is the point: it suits leadership programs and multi day residential conferences that want delegates to stay put rather than disperse into a holiday strip.",
   src="https://www.sanctuarycove.intercontinental.com/wp-content/uploads/2026/03/InterContinental-Sanctuary-Cove-Resort-Meetings-Events-2026.pdf",
   src2="https://www.sanctuarycove.intercontinental.com/meetings-and-events/venue-collection/macarthurs-ballroom/"),

 dict(
   city="Gold Coast", slug="sofitel-gold-coast-broadbeach", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Sofitel Gold Coast Broadbeach", sp="Grand Ballroom", pr="Broadbeach", ty="hotel",
   th=350, bq=220, cl=170, ck=350, cab=None, ush=66, bd=60,
   br=10, gr=296, area=312, ceil=4.5, ceilq=None,
   s_name="Sorrento", s_th=200,
   note="A 296 room hotel a short walk from the convention centre with ten event spaces topping out at 350. It works as the headquarters hotel for a convention centre congress and handles the committee meetings, satellite sessions and speaker dinners in its own rooms.",
   src="https://sofitel.accor.com/en/hotels/0454/meetings.html",
   src2="https://experiencegoldcoast.com/business-events/find-a-supplier/sofitel-gold-coast-broadbeach"),

# ------------------------------------------------------------- SUNSHINE COAST
 dict(
   city="Sunshine Coast", slug="sunshine-coast-convention-centre", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Sunshine Coast Convention Centre", sp="Minyama Ballroom", pr="Twin Waters", ty="conv",
   th=1000, bq=920, cl=None, ck=1500, cab=736, ush=None, bd=None,
   br=14, gr=373, area=1600, ceil=None, ceilq=None,
   s_name="Wandiny Room", s_th=980,
   note="The one property in the region that seats a four figure plenary and sleeps most of the delegates on the same site, integrated into the Novotel resort at Twin Waters. It is a low rise resort campus rather than a city convention centre, so allow walking time between rooms and build the outdoor space into the program.",
   src="https://sunshinecoastconventioncentre.com/organisers/venues-capabilities-floor-plans/",
   src2="https://sunshinecoastconventioncentre.com/organisers/venues-capabilities-floor-plans/minyama-ballroom/"),

 dict(
   city="Sunshine Coast", slug="the-events-centre-caloundra", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="The Events Centre, Caloundra", sp="Kings Theatre", pr="Caloundra", ty="event",
   th=820, bq=400, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=5, gr=0, area=669, ceil=None, ceilq=None,
   s_name="Playhouse Theatre", s_th=300,
   note="A council performing arts venue that takes conferences and gala dinners on a flat floor, with theatre infrastructure and staging already in place. It has no accommodation, so it only works if you are block booking Caloundra hotels alongside it.",
   src="https://theeventscentre.com.au/venue-hire",
   src2="https://businesseventssunshinecoast.com/supplier/the-events-centre-caloundra/"),

 dict(
   city="Sunshine Coast", slug="unisc-sunshine-coast", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="University of the Sunshine Coast", sp="UniSC Auditorium", pr="Sippy Downs", ty="uni",
   th=500, bq=350, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=10, gr=0, area=500, ceil=None, ceilq=None,
   s_name="Lecture theatre", s_th=295,
   note="A pillarless 500 square metre auditorium plus a run of lecture theatres, which is the practical option for academic and medical conferences needing many concurrent breakouts. There is no accommodation on campus and it is twenty kilometres from the airport, so delegates stay on the coast and coach in.",
   src="https://businesseventssunshinecoast.com/supplier/university-of-the-sunshine-coast/",
   src2="https://www.unisc.edu.au/about/locations/venue-and-event-services/events-at-unisc-sunshine-coast"),

 dict(
   city="Sunshine Coast", slug="peppers-noosa-resort-villas", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Peppers Noosa Resort & Villas", sp="Macquarie Ballroom", pr="Noosa Heads", ty="resort",
   th=350, bq=220, cl=150, ck=400, cab=None, ush=None, bd=None,
   br=5, gr=160, area=None, ceil=None, ceilq=None,
   s_name="Rainforest Room", s_th=200,
   note="A pillarless ballroom for up to 350 delegates sitting above Noosa on Viewland Drive, with a dedicated theatrette for smaller plenaries. It is a hillside villa resort, so delegates need the shuttle to reach Hastings Street and the beach.",
   src="https://businesseventssunshinecoast.com/supplier/peppers-noosa-resort-villas/",
   src2="https://www.peppers.com.au/noosa/"),

 dict(
   city="Sunshine Coast", slug="elysium-noosa", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Elysium Noosa", sp="Hastings Ballroom", pr="Noosa Heads", ty="resort",
   th=300, bq=180, cl=200, ck=300, cab=153, ush=None, bd=None,
   br=8, gr=176, area=None, ceil=None, ceilq=None,
   s_name="Haven One", s_th=106,
   note="The largest conference capable property on Hastings Street, with the ballroom and the guest rooms on the same site and the Noosa River across the road. The rebrand from Sofitel is recent, so check what contracted inclusions carried across before you commit.",
   src="https://businesseventssunshinecoast.com/supplier/elysium-noosa/",
   src2="https://www.elysiumnoosa.com.au/conference-meetings-events/"),

 dict(
   city="Sunshine Coast", slug="mantra-mooloolaba-beach", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Mantra Mooloolaba Beach", sp="Mantra Room", pr="Mooloolaba", ty="hotel",
   th=250, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=7, gr=188, area=None, ceil=None, ceilq=None,
   s_name="Coral and Harbour", s_th=130,
   note="A beachfront hotel directly opposite the Mooloolaba Esplanade, which puts restaurants and bars within a two minute walk of the meeting rooms. It suits mid size residential conferences that want delegates to be able to leave the property on foot in the evening.",
   src="https://businesseventssunshinecoast.com/supplier/mantra-mooloolaba-beach/",
   src2="https://businesseventssunshinecoast.com/supplier/mantra-mooloolaba-beach/"),

 dict(
   city="Sunshine Coast", slug="australia-zoo", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Australia Zoo", sp="Crikey Cafe Event Space", pr="Beerwah", ty="other",
   th=None, bq=300, cl=None, ck=300, cab=300, ush=None, bd=None,
   br=2, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Wildlife Hospital Conference Room", s_th=40,
   note="An incentive and brand event site rather than a conference venue, used for dinners and team activities inside the zoo after public hours. It is at Beerwah, closer to Brisbane than to Noosa, so it usually pairs with a coastal hotel base and a coach.",
   src="https://businesseventssunshinecoast.com/supplier/australia-zoo/",
   src2="https://australiazoo.com.au/weddings-functions/corporate-functions/"),

 dict(
   city="Sunshine Coast", slug="venue-114", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Venue 114", sp="Hall 1", pr="Bokarina", ty="event",
   th=None, bq=None, cl=None, ck=700, cab=None, ush=None, bd=None,
   br=15, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Halls 1, 2 and 3 combined", s_th=None,
   note="A multi purpose lakeside venue used for expos, trade displays and large cocktail functions where a resort ballroom is the wrong shape. Accommodation is off site at Kawana and Mooloolaba, so it suits day programs and local delegates.",
   src="https://businesseventssunshinecoast.com/supplier/venue-114/",
   src2="https://businesseventssunshinecoast.com/supplier/venue-114/"),

 dict(
   city="Sunshine Coast", slug="spicers-clovelly-estate", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Spicers Clovelly Estate", sp="Library Deck", pr="Montville", ty="resort",
   th=40, bq=80, cl=None, ck=80, cab=None, ush=None, bd=26,
   br=2, gr=19, area=None, ceil=None, ceilq=None,
   s_name="Montville House", s_th=20,
   note="A nineteen suite hinterland estate used for board offsites and executive retreats where the whole property is taken exclusively. Numbers are small by design and the restaurant on site is the reason most groups choose it.",
   src="https://businesseventssunshinecoast.com/supplier/spicers-clovelly-estate/",
   src2="https://spicersretreats.com/spicers-clovelly-estate/"),

# --------------------------------------------------------------------- CAIRNS
 dict(
   city="Cairns", slug="cairns-convention-centre", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Cairns Convention Centre", sp="Arena", pr="Cairns CBD", ty="conv",
   th=5000, bq=910, cl=792, ck=1180, cab=728, ush=None, bd=None,
   br=None, gr=0, area=1470, ceil=17.0, ceilq="to the roof structure",
   s_name="Auditorium", s_th=2360,
   note="The only building in the region that holds a plenary above about 1,000, and it carries two tiered rooms rather than one. Cairns Performing Arts Centre reaches 941 and the Sheraton Grand Mirage at Port Douglas 850, so between 650 and 1,000 you do have a choice. The 5,000 theatre figure needs the retractable tiered seating deployed; on the flat floor in exhibition mode the same room seats 1,584 and takes 98 booths.",
   src="https://www.cairnsconvention.com.au/wp-content/uploads/2025/06/Cairns-Convention-Centre-Capacity-Chart-2025-Dance-Floor-Updated-Measurements.pdf",
   src2="https://www.cairnsconvention.com.au/plan/rooms-and-spaces/arena/"),

 dict(
   city="Cairns", slug="cairns-performing-arts-centre", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Cairns Performing Arts Centre", sp="Theatre", pr="Cairns CBD", ty="event",
   th=941, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=None, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Studio", s_th=None,
   note="A council owned proscenium theatre a little over a kilometre from the convention centre, used for awards nights, plenaries and productions that need real staging and sightlines rather than a flat ballroom. The 941 seats are fixed, and the adjoining Studio takes up to 400 for the dinner afterwards.",
   src="https://businesseventscairns.org.au/offsite-venues/cairns-performing-arts-centre/",
   src2="https://businesseventscairns.org.au/offsite-venues/cairns-performing-arts-centre/"),

 dict(
   city="Cairns", slug="sheraton-grand-mirage-port-douglas", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Sheraton Grand Mirage Resort, Port Douglas", sp="The Glade Pavilion", pr="Port Douglas", ty="resort",
   th=850, bq=500, cl=800, ck=1000, cab=None, ush=None, bd=None,
   br=18, gr=295, area=800, ceil=None, ceilq=None,
   s_name="Mirage Ballroom", s_th=300,
   note="The only Port Douglas property with an event footprint reaching into the high hundreds, and it does so through an outdoor pavilion rather than a ballroom. Plan the wet season carefully, because the capacity that makes this resort interesting is the capacity exposed to weather, and the largest permanent indoor room is the Mirage Ballroom at 300.",
   src="https://www.marriott.com/en-us/hotels/cnssi-sheraton-grand-mirage-resort-port-douglas/events/",
   src2="https://businesseventscairns.org.au/conference-venue/sheraton-grand-mirage-resort-port-douglas/"),

 dict(
   city="Cairns", slug="pullman-cairns-international", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Pullman Cairns International", sp="Grand Ballroom", pr="Cairns CBD", ty="hotel",
   th=650, bq=350, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=11, gr=324, area=500, ceil=None, ceilq=None,
   s_name="Mossman Ballroom", s_th=None,
   note="The largest hotel ballroom in Cairns and the default choice for a conference that wants everything in one building rather than splitting between a hotel and the convention centre. It is the closest hotel to the convention centre, which makes it the usual headquarters property for centre based conferences.",
   src="https://www.pullmancairnsinternational.com.au/meetings-events/",
   src2="https://www.pullmancairnsinternational.com.au/"),

 dict(
   city="Cairns", slug="pullman-reef-hotel-casino", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Pullman Reef Hotel Casino", sp="Michaelmas Cay Ballroom", pr="Cairns Wharf", ty="hotel",
   th=400, bq=450, cl=300, ck=500, cab=192, ush=72, bd=None,
   br=12, gr=128, area=None, ceil=None, ceilq=None,
   s_name="Urchins Ballroom", s_th=None,
   note="An integrated hotel, casino and entertainment complex on Wharf Street, so a dinner can move from ballroom to gaming floor and bars without leaving the building. The room block is small at 128, so it works better as the dinner and function venue for a larger conference than as the sole accommodation property.",
   src="https://businesseventscairns.org.au/conference-venue/pullman-reef-hotel-casino/",
   src2="https://www.reefcasino.com.au/venue/events-and-conferences/"),

 dict(
   city="Cairns", slug="shangri-la-the-marina-cairns", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Shangri-La The Marina, Cairns", sp="Shangri-La Ballroom", pr="Cairns Marina", ty="hotel",
   th=380, bq=300, cl=150, ck=400, cab=None, ush=None, bd=None,
   br=19, gr=255, area=None, ceil=None, ceilq=None,
   s_name="Trinity Rooms", s_th=None,
   note="Sits directly on the Marlin Marina, which puts delegates at the reef departure pontoons on foot rather than by coach. Nineteen separate spaces across the property make it workable for a conference wanting many concurrent breakouts on a moderate plenary.",
   src="https://businesseventscairns.org.au/conference-venue/shangri-la-the-marina-cairns/",
   src2="https://www.shangri-la.com/cairns/shangrila/meetings-events/"),

 dict(
   city="Cairns", slug="hilton-cairns", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Hilton Cairns", sp="Grand Ballroom", pr="Cairns Esplanade", ty="hotel",
   th=300, bq=250, cl=200, ck=400, cab=180, ush=100, bd=None,
   br=10, gr=263, area=None, ceil=None, ceilq=None,
   s_name=None, s_th=None,
   note="A waterfront residential conference hotel on the Esplanade with ten meeting rooms against 263 rooms, which is a workable ratio for a self contained program of two to three hundred. Walking distance to the convention centre makes it a common overflow or secondary block.",
   src="https://businesseventscairns.org.au/conference-venue/hilton-cairns/",
   src2="https://businesseventscairns.org.au/conference-venue/hilton-cairns/"),

 dict(
   city="Cairns", slug="novotel-cairns-oasis-resort", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Novotel Cairns Oasis Resort", sp="Abercrombie Room", pr="Cairns CBD", ty="resort",
   th=200, bq=100, cl=99, ck=200, cab=96, ush=33, bd=None,
   br=7, gr=314, area=None, ceil=None, ceilq=None,
   s_name="McKenzie Room", s_th=120,
   note="A resort format property inside the city grid, so a residential conference gets a lagoon pool and lawn without leaving town. Meeting space is modest against 314 rooms, which makes it stronger as an accommodation block with breakouts than as a plenary venue.",
   src="https://www.novotelcairnsresort.com.au/meetings-events/abercrombie-room/",
   src2="https://www.novotelcairnsresort.com.au/meetings-events/mckenzie-room/"),

 dict(
   city="Cairns", slug="pullman-port-douglas-sea-temple", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Pullman Port Douglas Sea Temple Resort & Spa", sp="Temple Room", pr="Port Douglas", ty="resort",
   th=162, bq=120, cl=100, ck=180, cab=80, ush=39, bd=None,
   br=6, gr=84, area=None, ceil=None, ceilq=None,
   s_name="Lagoon View Terrace", s_th=None,
   note="An 84 room beachfront resort on Four Mile Beach built for groups small enough to take the whole property. The resort states it works for groups up to about 150, which is the honest ceiling whatever the theatre figure says.",
   src="https://www.pullmanportdouglas.com.au/meetings",
   src2="https://businesseventscairns.org.au/conference-venue/pullman-port-douglas-sea-temple-resort-spa/"),

 dict(
   city="Cairns", slug="crystalbrook-riley", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Crystalbrook Riley", sp="Zone I-III", pr="Cairns Esplanade", ty="hotel",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=6, gr=311, area=366, ceil=3.0, ceilq=None,
   s_name="Zone IV-VI", s_th=None,
   note="The largest of the three Crystalbrook hotels on the Esplanade and the only one with a meeting floor that takes a few hundred people. It publishes floor area and a maximum of 420 for the combined zones rather than a per setup breakdown, so confirm theatre and banquet with the venue.",
   src="https://www.crystalbrookcollection.com/riley/riley-event-spaces",
   src2="https://www.crystalbrookcollection.com/riley/rooms"),

# ------------------------------------------------------------- HUNTER VALLEY
 dict(
   city="Hunter Valley", slug="rydges-resort-hunter-valley", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Rydges Resort Hunter Valley", sp="Hunter Valley Conference and Events Centre", pr="Lovedale", ty="resort",
   th=1160, bq=850, cl=740, ck=1750, cab=664, ush=123, bd=None,
   br=None, gr=417, area=1123, ceil=4.5, ceilq=None,
   s_name="Exhibition Centre", s_th=750,
   note="The one property in the Hunter Valley that puts a large residential conference plenary and its delegates on the same site, with 417 rooms behind a 1,123 square metre conference centre. It is a big rural resort campus rather than a boutique wine experience, so it suits volume programs and gala dinners more than intimate leadership retreats.",
   src="https://www.rydges.com/accommodation/regional-nsw/hunter-valley/venues-events/corporate-events/",
   src2="https://www.rydges.com/accommodation/regional-nsw/hunter-valley"),

 dict(
   city="Hunter Valley", slug="oaks-cypress-lakes-resort", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Oaks Cypress Lakes Resort", sp="Cypress Lakeside Marquee", pr="Pokolbin", ty="resort",
   th=672, bq=470, cl=None, ck=800, cab=376, ush=None, bd=None,
   br=24, gr=None, area=800, ceil=None, ceilq=None,
   s_name="Venusta Centre", s_th=450,
   note="A villa based golf resort over 300 acres with 24 bookable spaces, which gives unusual flexibility for concurrent breakouts and outdoor dinners. The headline 800 square metre space is a marquee, so the largest permanent indoor room is the 435 square metre Venusta Centre at 450 theatre, and that is the number to plan a plenary around.",
   src="https://www.oakshotels.com/en/oaks-cypress-lakes-resort/meetings-and-events",
   src2="https://www.oakshotels.com/en/oaks-cypress-lakes-resort"),

 dict(
   city="Hunter Valley", slug="chateau-elan-at-the-vintage", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Chateau Elan at The Vintage", sp="The Founders Room", pr="Rothbury", ty="resort",
   th=330, bq=172, cl=100, ck=330, cab=None, ush=68, bd=54,
   br=6, gr=None, area=269, ceil=3.4, ceilq=None,
   s_name="Barrington Room", s_th=200,
   note="The property to use when a client wants a residential conference that still feels like a retreat, with a golf course, a day spa and villa accommodation behind six event rooms. The Founders Room divides into two halves, so it handles a 330 plenary with breakouts, and above that number the program has to move.",
   src="https://chateauelan.com.au/events/hunter-valley-conference-venues/",
   src2="https://chateauelan.com.au/hunter-valley-accommodation/"),

 dict(
   city="Hunter Valley", slug="hope-estate", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Hope Estate", sp="The Winery", pr="Pokolbin", ty="event",
   th=None, bq=550, cl=None, ck=850, cab=None, ush=None, bd=None,
   br=None, gr=0, area=None, ceil=None, ceilq=None,
   s_name="The Great Cask Hall", s_th=None,
   note="A working winery built to absorb crowds, with a 550 seat winery space and an outdoor amphitheatre the estate lists at up to 20,000 for concerts. There is no delegate accommodation on site, so it works as an offsite gala or a concert scale destination rather than as a conference base.",
   src="https://www.hopeestate.com.au/pages/functions-new",
   src2="https://www.hopeestate.com.au/"),

 dict(
   city="Hunter Valley", slug="bimbadgen", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Bimbadgen", sp="Palmers Lane", pr="Pokolbin", ty="event",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=10,
   br=5, gr=59, area=None, ceil=None, ceilq=None,
   s_name="The Wine Shed", s_th=None,
   note="A multi site wine estate with an indoor venue and lawns at Palmers Lane, a restaurant private room, a wine shed and a ten seat boardroom, backed by 59 studios at the retreat. It publishes no configuration capacities, so every space has to be confirmed with the venue before a floor plan is drawn.",
   src="https://www.bimbadgen.com.au/business-meetings-retreats/",
   src2="https://www.bimbadgen.com.au/"),

 dict(
   city="Hunter Valley", slug="spicers-vineyards-estate", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Spicers Vineyards Estate", sp=None, pr="Pokolbin", ty="hotel",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=None, gr=None, area=None, ceil=None, ceilq=None,
   s_name=None, s_th=None,
   note="A small luxury retreat on Hermitage Road used for executive teams and board level groups rather than delegate conferences. It publishes no suite count and no meeting room capacities, so size and exclusive use terms have to be established with the property directly.",
   src="https://spicersretreats.com/spicers-vineyards-estate/",
   src2="https://spicersretreats.com/spicers-vineyards-estate/"),

# ------------------------------------------------------------- BLUE MOUNTAINS
 dict(
   city="Blue Mountains", slug="fairmont-resort-blue-mountains", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Fairmont Resort Blue Mountains MGallery", sp="Grand Ballroom", pr="Leura", ty="resort",
   th=620, bq=380, cl=246, ck=380, cab=304, ush=None, bd=None,
   br=23, gr=224, area=None, ceil=None, ceilq=None,
   s_name="Ballroom", s_th=364,
   note="The only Blue Mountains property that seats a 600 person plenary and sleeps the whole group on site, with 224 rooms and 23 meeting spaces. The Grand Ballroom is the Ballroom and Pioneers rooms opened together, so the largest single undivided room is the Ballroom at 364 theatre, and the resort notes its published capacities exclude staging, dance floor and buffet.",
   src="https://www.fairmontresort.com.au/conferences-events/event-spaces/grand-ballroom/",
   src2="https://www.fairmontresort.com.au/conferences-events/event-spaces/ballroom/"),

 dict(
   city="Blue Mountains", slug="hydro-majestic-hotel", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Hydro Majestic Hotel", sp="Majestic Ballroom", pr="Medlow Bath", ty="hotel",
   th=250, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=None, gr=82, area=380, ceil=None, ceilq=None,
   s_name="Wintergarden", s_th=None,
   note="A 1904 clifftop hotel over the Megalong Valley, now operated within the Worlds Apart collection, with 82 rooms and a domed ballroom. It suits a 60 to 200 person residential program that wants a single distinctive building rather than a purpose built conference floor.",
   src="https://www.worldsapart.club/independents/hydromajestic/events/meetings",
   src2="https://www.worldsapart.club/independents/hydromajestic/weddings"),

 dict(
   city="Blue Mountains", slug="mountain-heritage-hotel", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Mountain Heritage Hotel", sp="Main conference room", pr="Katoomba", ty="hotel",
   th=200, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=None, gr=41, area=None, ceil=None, ceilq=None,
   s_name="Tower Room", s_th=None,
   note="A 41 room hotel above Katoomba with a main conference room seating 200 theatre and a Tower Room for 20 to 50. The meeting space outruns the room stock, so anything over about forty rooms becomes a day conference with beds sourced elsewhere.",
   src="https://mountainheritage.com.au/conferences/event-space/",
   src2="https://mountainheritage.com.au/"),

 dict(
   city="Blue Mountains", slug="ardour-lilianfels-blue-mountains", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Ardour Lilianfels Blue Mountains", sp="Banksia Room", pr="Katoomba", ty="resort",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=4, gr=None, area=120, ceil=2.7, ceilq="low for a raised stage or a large rear projection screen",
   s_name="Wollemi Pine Room", s_th=None,
   note="Rebranded from Lilianfels Blue Mountains Resort and Spa, sitting on two acres above the Jamison Valley next to Echoes. The property publishes its largest room as holding 30 to 120 guests without naming the setup, so treat it as a leadership retreat house rather than a conference hotel.",
   src="https://www.worldsapart.club/ardour/lilianfels/events/meetings",
   src2="https://www.worldsapart.club/ardour/lilianfels/weddings"),

 dict(
   city="Blue Mountains", slug="the-carrington-hotel-katoomba", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="The Carrington Hotel", sp="The Grand Dining Room", pr="Katoomba", ty="hotel",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=None, gr=65, area=None, ceil=None, ceilq=None,
   s_name="The Ballroom", s_th=None,
   note="A heritage listed hotel on Katoomba Street with 65 rooms, none configured alike, and a spread of period rooms including the Grand Dining Room, the Ballroom, the Library and the Old City Bank. The hotel takes corporate groups of up to 200 and sets an 80 guest minimum on the Grand Dining Room, and publishes no per setup capacity chart.",
   src="https://thecarrington.com.au/meetings-and-events/the-spaces/",
   src2="https://thecarrington.com.au/meetings-and-events/meetings-and-corporate-events/"),

 dict(
   city="Blue Mountains", slug="echoes-boutique-hotel", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Echoes Boutique Hotel", sp="Meeting room", pr="Katoomba", ty="hotel",
   th=None, bq=None, cl=25, ck=None, cab=None, ush=19, bd=16,
   br=None, gr=None, area=None, ceil=None, ceilq=None,
   s_name=None, s_th=None,
   note="An adults only clifftop hotel on Lilianfels Avenue publishing meeting capacities of 16 boardroom, 25 classroom and 19 u-shape, with minimum numbers applying. This is an executive team offsite property rather than a conference venue, and it does not name its meeting room or publish a room count.",
   src="https://www.worldsapart.club/independents/echoes/events/meetings",
   src2="https://www.worldsapart.club/independents/echoes"),

 dict(
   city="Blue Mountains", slug="blue-mountains-cultural-centre", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Blue Mountains Cultural Centre", sp="Viewing Platform", pr="Katoomba", ty="event",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=7, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Gallery", s_th=None,
   note="A council venue in central Katoomba whose venue hire booklet lists seven bookable spaces with maximum capacities only and no setup breakdown, the largest being the Viewing Platform at 400. It works as an offsite dinner, launch or plenary overflow space for a group already housed in Katoomba, and it has no accommodation.",
   src="https://bluemountainsculturalcentre.com.au/venue-hire/",
   src2="https://bluemountainsculturalcentre.com.au/venue-hire/"),

 dict(
   city="Blue Mountains", slug="everglades-house-and-gardens", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Everglades House & Gardens", sp="The Gallery", pr="Leura", ty="other",
   th=None, bq=50, cl=None, ck=60, cab=None, ush=None, bd=None,
   br=None, gr=0, area=None, ceil=None, ceilq=None,
   s_name=None, s_th=None,
   note="A National Trust house and terraced garden in Leura hiring the Gallery for private events at 50 seated or 60 standing, and the garden for ceremonies of up to 120, in two hour blocks between nine and five. It is a daytime activation or partner program stop, and the Trust does not currently offer evening receptions.",
   src="https://www.nationaltrust.org.au/places/everglades-house-gardens/venue-hire/",
   src2="https://www.nationaltrust.org.au/places/everglades-house-gardens/"),

# ------------------------------------------------------------------ BYRON BAY
 dict(
   city="Byron Bay", slug="byron-theatre-community-centre", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Byron Theatre, Byron Community Centre", sp="Byron Theatre", pr="Byron Bay town centre", ty="event",
   th=266, bq=None, cl=None, ck=None, cab=160, ush=None, bd=None,
   br=5, gr=0, area=300, ceil=None, ceilq=None,
   s_name="Wategos Room", s_th=100,
   note="The largest single room in Byron Bay for a seated plenary, in the middle of town on Jonson Street so delegates walk to it. It is raked fixed seating rather than a flat floor conference room, and there is no accommodation attached, so it works as the general session or awards room bolted onto hotel rooms elsewhere.",
   src="https://www.byroncentre.com.au/spaces/theatre",
   src2="https://www.byroncentre.com.au/spaces/wategos-room"),

 dict(
   city="Byron Bay", slug="crystalbrook-byron", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Crystalbrook Byron", sp="Entire Conference Room", pr="Broken Head Road", ty="resort",
   th=192, bq=150, cl=120, ck=180, cab=120, ush=45, bd=44,
   br=4, gr=92, area=216, ceil=3.76, ceilq=None,
   s_name="Tallow Creek", s_th=80,
   note="The property formerly trading as The Byron at Byron, and the largest purpose built flat floor conference room in the area with a full published setup chart. Ninety two suites means the conference room seats more people than the resort can sleep, so anything near 192 needs a second accommodation property in town.",
   src="https://www.crystalbrookcollection.com/byron/events",
   src2="https://www.crystalbrookcollection.com/byron"),

 dict(
   city="Byron Bay", slug="elements-of-byron", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Elements of Byron", sp="Banksia Pavilion", pr="Belongil", ty="resort",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=5, gr=202, area=330, ceil=None, ceilq=None,
   s_name="Belongil Pavilion", s_th=None,
   note="The biggest single accommodation block in the area, 202 villas holding 296 bedrooms on a beachfront site at Belongil, which makes it the default for a residential conference that needs everyone on one property. The resort publishes a single maximum per space rather than a setup chart, with Banksia Pavilion listed at 160 across 330 square metres, so confirm the plenary set before committing.",
   src="https://elementsofbyron.com.au/events-and-groups/41-or-more-people/",
   src2="https://elementsofbyron.com.au/events-and-groups/41-or-more-people/"),

 dict(
   city="Byron Bay", slug="ramada-ballina-byron", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Ramada Hotel Ballina Byron", sp="The Fenwick Room", pr="Ballina", ty="hotel",
   th=110, bq=64, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=4, gr=110, area=None, ceil=None, ceilq=None,
   s_name="The Kingsford Room", s_th=40,
   note="One hundred and ten rooms in Ballina with four meeting rooms, the largest seating 110 theatre, near the only airport in the region with direct capital city services. It is a conventional business hotel rather than a Byron retreat property, so use it for the working sessions and the budget rooms, not for the destination experience.",
   src="https://ramadaballina.com.au/events/",
   src2="https://ramadaballina.com.au/events/"),

 dict(
   city="Byron Bay", slug="raes-on-wategos", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Rae's on Wategos", sp="Rae's Dining Room", pr="Wategos Beach", ty="hotel",
   th=None, bq=50, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=2, gr=17, area=None, ceil=None, ceilq=None,
   s_name="Rae's Cellar Bar", s_th=None,
   note="Seventeen keys on Wategos Beach, taken whole for a board offsite, an executive retreat or a top tier incentive reward group. The published ceiling is 50 seated or 75 standing on hotel exclusivity, so it is a small numbers, high spend property rather than a conference venue.",
   src="https://raes.com.au/events/",
   src2="https://raes.com.au/"),

 dict(
   city="Byron Bay", slug="byron-bay-surf-club", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Byron Bay Surf Life Saving Club", sp="Function Room", pr="Byron Bay town centre", ty="event",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=1, gr=0, area=None, ceil=None, ceilq=None,
   s_name=None, s_th=None,
   note="A beachfront function room in town with a published capacity of up to 150 people, used for welcome functions, brand activations and casual dinners where the view is the whole point. It publishes no setup breakdown or floor area, and it is a volunteer surf club rather than a commercial conference operator, so confirm exclusive use and supplier access early.",
   src="https://byronbaysurfclub.org/function-room/",
   src2="https://byronbaysurfclub.org/function-room/"),

# ---------------------------------------------------------------- YARRA VALLEY
 dict(
   city="Yarra Valley", slug="yarra-valley-lodge", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Yarra Valley Lodge", sp="Marmion Ballroom", pr="Chirnside Park", ty="resort",
   th=325, bq=200, cl=150, ck=400, cab=140, ush=60, bd=70,
   br=9, gr=102, area=305, ceil=None, ceilq=None,
   s_name="Birrarung Room", s_th=100,
   note="The largest residential conference property in the district, with 102 rooms and a ballroom that divides into two, inside the grounds of the Heritage Golf and Country Club at Chirnside Park. It is the gateway option rather than the valley floor, so it suits programs that want scale and a short run from town more than programs that want to be among the vines.",
   src="https://www.yarravalleylodge.com/wp-content/uploads/sites/189/2026/07/Yarra-Valley-Lodge-Venue-Guide.pdf",
   src2="https://www.yarravalleylodge.com/venues-events/corporate/"),

 dict(
   city="Yarra Valley", slug="racv-healesville-country-club", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="RACV Healesville Country Club", sp="Ballroom", pr="Healesville", ty="resort",
   th=320, bq=240, cl=150, ck=320, cab=192, ush=63, bd=52,
   br=13, gr=80, area=400, ceil=3.7, ceilq="in the Ballroom; the syndicate rooms are 2.7m",
   s_name="James Room", s_th=180,
   note="The region's most complete residential conference plant, with thirteen function rooms, six dedicated syndicate rooms and the only published ceiling heights in the district. It is built for multi day residential programs that break out repeatedly, and its 80 rooms sleeping 160 are the real limit on group size rather than the ballroom.",
   src="https://www.racv.com.au/content/dam/racv-assets/documents/travel-experiences/club/healesville/conferences-events/healesville-conferences-and-events-brochure.pdf",
   src2="https://www.racv.com.au/travel-experiences/conferences-venues-events/healesville/venue-hire.html"),

 dict(
   city="Yarra Valley", slug="levantine-hill-estate", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Levantine Hill Estate", sp="Winery Banquet Hall", pr="Coldstream", ty="event",
   th=None, bq=250, cl=None, ck=500, cab=None, ush=None, bd=None,
   br=None, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Winery Pavilion", s_th=100,
   note="The working winery with the most genuine conference fit out, with a fixed LED screen, lectern, house sound and breakout space in the Pavilion and a mezzanine boardroom. The banquet hall carries the largest seated dinner capacity of any winery we checked in the region, and its theatre figure is published only as a range.",
   src="https://www.levantinehill.com.au/pages/corporate-events",
   src2="https://www.levantinehill.com.au/pages/corporate-events"),

 dict(
   city="Yarra Valley", slug="tarrawarra-museum-of-art", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="TarraWarra Museum of Art", sp="Eva and Marc Besen Centre", pr="Healesville", ty="other",
   th=200, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=None, gr=0, area=None, ceil=None, ceilq=None,
   s_name=None, s_th=None,
   note="A 200 seat multi purpose space inside a public art museum, with AV, lectern, a small stage, drop down screens, modular tables and a 46 metre glass wall onto the permanent collection. It is the strongest non hotel plenary in the region for a forum or a launch, and it has no accommodation, so it only works paired with beds elsewhere.",
   src="https://www.twma.com.au/venue-hire/",
   src2="https://www.twma.com.au/venue-hire/"),

 dict(
   city="Yarra Valley", slug="chateau-yering-hotel", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Chateau Yering Hotel", sp="The Oak Room", pr="Yering", ty="hotel",
   th=None, bq=130, cl=None, ck=None, cab=None, ush=60, bd=None,
   br=None, gr=32, area=160, ceil=None, ceilq=None,
   s_name="The Library", s_th=None,
   note="The heritage house option, a 32 suite property whose largest room seats 130 for dinner and 60 in u-shape, with a library and a twelve seat private dining room behind it. It is sized for boards, executive teams and small leadership groups that want the whole property to themselves, not for a conference with a plenary.",
   src="https://chateauyering.com.au/yarra-valley-conference-venue/",
   src2="https://chateauyering.com.au/facilities/"),

 dict(
   city="Yarra Valley", slug="balgownie-estate-yarra-valley", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Balgownie Estate Vineyard Resort & Spa", sp=None, pr="Yarra Glen", ty="resort",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=None, gr=70, area=None, ceil=None, ceilq=None,
   s_name=None, s_th=None,
   note="The third residential resort of scale in the valley, with 70 suites and its own conference packages. Its room by room capacities are not published, so every setup number has to be confirmed with the venue before it goes into a proposal.",
   src="https://www.balgownieestate.com.au/",
   src2="https://www.balgownieestate.com.au/"),

 dict(
   city="Yarra Valley", slug="domaine-chandon-australia", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="CHANDON Australia", sp="The Riddling Hall", pr="Coldstream", ty="event",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=12,
   br=4, gr=0, area=None, ceil=None, ceilq=None,
   s_name="The Homestead", s_th=None,
   note="A sparkling wine estate hiring three guest spaces plus a twelve seat boardroom, with the Riddling Hall quoted for 20 to 100 guests and the Homestead and Restaurant each for up to 50. It publishes headcount ranges rather than setup capacities, so treat it as a dinner, incentive and small plenary venue rather than a conference room.",
   src="https://www.chandon.com/en-au/private-events",
   src2="https://www.chandon.com/en-au/private-events"),

 dict(
   city="Yarra Valley", slug="yering-station", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Yering Station", sp="Historic Barn", pr="Yering", ty="event",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=24,
   br=None, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Devaux Room", s_th=None,
   note="A working winery and restaurant whose Historic Barn takes 30 to 100 guests as an open multi purpose room, backed by a boardroom seating 24 and the Devaux Room for 8 to 20. Setup specific capacities are not published, so it is a dinner, offsite day and small meeting venue rather than something to size a conference against.",
   src="https://www.yering.com/corporate-events",
   src2="https://www.yering.com/visit-us/weddings-and-functions/"),

 dict(
   city="Yarra Valley", slug="meletos", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Meletos", sp="The Warehouse", pr="Coldstream", ty="hotel",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=4, gr=23, area=None, ceil=None, ceilq=None,
   s_name=None, s_th=None,
   note="A 23 room boutique hotel on the same Coldstream estate as Stones of the Yarra Valley, with four event spaces including The Warehouse. The room count makes it a buyout property for a single leadership team rather than a conference host, and its per space capacities are not published.",
   src="https://www.meletos.com/thewarehouse",
   src2="https://www.meletos.com/"),

# --------------------------------------------------------- MORNINGTON PENINSULA
 dict(
   city="Mornington Peninsula", slug="mornington-racecourse", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Mornington Racecourse", sp="Gunnamatta", pr="Mornington", ty="event",
   th=500, bq=650, cl=300, ck=800, cab=None, ush=None, bd=None,
   br=6, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Final Furlong", s_th=300,
   note="Where you go when the room has to hold more people than any hotel on the Peninsula can seat, at the northern end of the region and the closest large venue to Melbourne. There is no accommodation on site, so every delegate has to be housed and coached from elsewhere.",
   src="https://www.businesseventsmorningtonpeninsula.com.au/portals/1/Publications/BEMPPlanner2024/index.html",
   src2="https://www.businesseventsmorningtonpeninsula.com.au/portals/1/Publications/BEMPPlanner2024/index.html"),

 dict(
   city="Mornington Peninsula", slug="racv-cape-schanck-resort", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="RACV Cape Schanck Resort", sp="Great Southern Ballroom", pr="Cape Schanck", ty="resort",
   th=450, bq=300, cl=200, ck=450, cab=240, ush=None, bd=None,
   br=13, gr=204, area=483, ceil=None, ceilq=None,
   s_name="Horizon Ballroom", s_th=340,
   note="The only property on the Peninsula that runs a large residential conference on one site, with 204 rooms and a ballroom that divides in two. It is a golf resort at the exposed southern end, so delegates are committed to the site once they arrive, and it takes 26 exhibition booths for a trade display alongside the conference.",
   src="https://www.racv.com.au/content/dam/racv-assets/documents/travel-experiences/resorts/cape-schanck/conferences-events/cape-schanck-conference-and-events-brochure.pdf",
   src2="https://www.racv.com.au/travel-experiences/conferences-venues-events/cape-schanck.html"),

 dict(
   city="Mornington Peninsula", slug="the-continental-sorrento", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="The Continental Sorrento", sp="Halcyon Hall", pr="Sorrento", ty="hotel",
   th=200, bq=None, cl=None, ck=230, cab=96, ush=None, bd=None,
   br=6, gr=108, area=None, ceil=None, ceilq=None,
   s_name="Grand Ballroom", s_th=120,
   note="A hotel, bar, restaurant and spa precinct on the Sorrento foreshore with 108 rooms and six bookable event spaces, so a mid size residential program can stay and meet in one place. It is the furthest of the large properties from Melbourne, which makes it a two night proposition rather than a day return one.",
   src="https://thecontinentalsorrento.com.au/gather/corporate/",
   src2="https://www.thecontinentalsorrento.com.au/"),

 dict(
   city="Mornington Peninsula", slug="lancemore-lindenderry-red-hill", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Lancemore Lindenderry Red Hill", sp="Lakeview", pr="Red Hill", ty="hotel",
   th=200, bq=150, cl=100, ck=220, cab=110, ush=None, bd=None,
   br=4, gr=40, area=340, ceil=3.0, ceilq=None,
   s_name="Woodclyff", s_th=72,
   note="A 40 room property on a working vineyard with four dedicated conference rooms and published dimensions for all of them, which is unusual in this region. The 40 rooms cap it at a single cohort leadership group rather than a full residential conference, even though the Lakeview room seats 200.",
   src="https://www.lancemore.com.au/lindenderry-red-hill/conferences/",
   src2="https://www.lancemore.com.au/lindenderry-red-hill/accommodation/"),

 dict(
   city="Mornington Peninsula", slug="flinders-hotel", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Flinders Hotel", sp="Peninsula and Lounge", pr="Flinders", ty="hotel",
   th=120, bq=120, cl=50, ck=200, cab=None, ush=36, bd=None,
   br=4, gr=40, area=None, ceil=None, ceilq=None,
   s_name="Peninsula 2 and 3", s_th=80,
   note="A pub hotel with 40 rooms in its Quarters wing and a soundproofed room that divides into three plus an adjoining lounge, which covers plenary and breakouts for a group of about a hundred. It sits in the village at Flinders, the furthest southern point of the region and the longest transfer from Melbourne.",
   src="https://flindershotel.com.au/wp-content/uploads/2026/03/Editable_FLI_Corporate-Pack_Feb-26.pdf",
   src2="https://flindershotel.com.au/accommodation/"),

 dict(
   city="Mornington Peninsula", slug="pt-leo-estate", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Pt. Leo Estate", sp="Whole estate, exclusive", pr="Merricks", ty="event",
   th=None, bq=150, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=3, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Pt. Leo Restaurant", s_th=None,
   note="A vineyard, restaurant and sculpture park used for incentive hosting, gala dinners and product launches, with whole estate exclusive hire published at up to 150 seated. Weekend exclusivity is limited to four days a calendar year, so weekday dates are the realistic ask.",
   src="https://www.ptleoestate.com.au/wp-content/uploads/2024/09/Events-at-Pt.-Leo-Estate-2024.pdf",
   src2="https://ptleoestate.com.au/events/private-events/"),

 dict(
   city="Mornington Peninsula", slug="montalto", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Montalto", sp="The Restaurant", pr="Red Hill South", ty="event",
   th=None, bq=90, cl=None, ck=130, cab=None, ush=None, bd=None,
   br=3, gr=0, area=None, ceil=None, ceilq=None,
   s_name="Private Dining Room", s_th=30,
   note="A working vineyard and restaurant with a sculpture trail, used for winery dinners and daytime group hosting rather than plenary sessions. There is no accommodation and no published theatre capacity, so it is the dinner half of a program housed somewhere else.",
   src="https://montalto.com.au/pages/functions",
   src2="https://montalto.com.au/pages/functions"),

 dict(
   city="Mornington Peninsula", slug="jackalope-hotel", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Jackalope Hotel", sp="Jackyak and Jenka", pr="Merricks North", ty="hotel",
   th=None, bq=60, cl=None, ck=100, cab=None, ush=None, bd=None,
   br=2, gr=44, area=None, ceil=None, ceilq=None,
   s_name="Private Dining by Doot Doot Doot", s_th=None,
   note="A 44 room design hotel on an eleven hectare vineyard, sized for an executive team or a board rather than a conference. Whole property buyout is published at 140 seated or 250 cocktail, and corporate rates are Monday to Thursday only.",
   src="https://www.jackalopehotels.com/events",
   src2="https://www.jackalopehotels.com/events"),

 dict(
   city="Mornington Peninsula", slug="peppers-moonah-links-resort", checked="6 September 2026",
   worked=False, seen=None, visit=None,
   n="Peppers Moonah Links Resort", sp="Thomson Room", pr="Fingal", ty="resort",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=16,
   br=7, gr=65, area=None, ceil=None, ceilq=None,
   s_name="AGU Boardroom", s_th=None,
   note="A 65 room golf resort with seven purpose built event spaces including a divisible main room, executive lodges and a marquee, aimed at golf anchored corporate programs. The resort does not publish a capacity chart, so every room number has to be confirmed with the venue before it goes in a proposal.",
   src="https://www.moonahlinks.com.au/cms/conference-and-events/",
   src2="https://www.moonahlinks.com.au/cms/hotel/accommodation-and-packages/"),
]
