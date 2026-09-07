# -*- coding: utf-8 -*-
"""Content for the sixteen CVBS destination pages.

Written 6 September 2026 from the research recorded in
_destination-source/RESEARCH-NOTES.md. Every factual claim here is traceable
to a venue's own published material or an official convention bureau, and the
capacity figures are never written here: they are read out of
assets/data/venues.json at build time so a featured card and the index can
never disagree. That was a real bug on the Sydney page in August 2026.

FIELDS
  title / meta    unique per page, no two the same
  h1              written for the search a planner actually types
  lead            hero supporting line, must carry destination, service,
                  48 hours and free to you
  snapshot        the answer block. Two or three paragraphs of market
                  intelligence, written so an answer engine can lift a
                  sentence and be right. Bold the claim, then support it.
  featured        (venue id, what it is particularly suited to). The meta
                  line is generated from the dataset, never typed.
  sources         what we source here, four to six, destination specific
  precincts       the short list for the aside
  start           (need, our steer) for the Where to start table
  local           (area, why you would choose it) for Local knowledge
  tradeoffs       (heading, the honest planning consideration)
  why_h2          the localised heading for the Why CVBS band
  why_lead        the first card body, localised
  faqs            (question, answer html). Six to eight, and the visible
                  question and the schema question are generated from the
                  same string so they can never drift.
  related         (href, label, why a planner would follow it)
"""

# Shared building blocks -----------------------------------------------------

FREE_A = ('Nothing. Our {city} venue finding service is free to you, and the rate we '
          'negotiate is usually better than booking direct. If you would like the detail, '
          'it is set out on <a href="how-we-are-paid.html">how we are paid</a>.')

FAST_A = ('We deliver a shortlist of matching {city} venues within 48 hours of receiving '
          'your brief, with rates and inclusions ready to compare. If your dates are tight '
          'or unusual, tell us in the brief and we will call the venues rather than email them.')

GROUP_A = ('Yes. We can package delegate or group accommodation in {city} with your venue '
           'as a single negotiation, which often strengthens the rate on both. See '
           '<a href="group-accommodation.html">group accommodation</a> for how that works.')

WHY_CARD_2 = ('Every venue has something worth knowing before you sign. A difficult load in, '
              'a low ceiling, a pre function space that struggles once the room is full. '
              'You will hear that from us at shortlist, not on the day.')

WHY_CARD_3 = ('There is no fee for our service. The sourcing, the local knowledge and the '
              'negotiating are all included, and the rate you end up with is usually better '
              'than booking direct.')

DEST = {}

# ------------------------------------------------------------------ MELBOURNE
DEST['Melbourne'] = dict(
  file='venue-finder-melbourne.html', state='VIC',
  title='Conference &amp; Event Venues in Melbourne | CVBS',
  meta=('Melbourne conference and event venue finding. MCEC, Crown, Southbank and CBD '
        'venues with published capacities, precinct guidance and a shortlist within 48 hours, '
        'free to you.'),
  h1='Conference &amp; Event Venues in Melbourne',
  lead='Tell us what you need in Melbourne. Shortlist within 48 hours, free to you.',
  snapshot=[
    '<b>Melbourne’s largest conference venue is the Melbourne Convention and Exhibition '
    'Centre at South Wharf.</b> Its Plenary seats 5,564 theatre style, and MCEC publishes '
    '40,000 square metres of pillarless exhibition space across 26 bays under 11.5 metre '
    'ceilings, which is more exhibition floor than any other Australian convention centre '
    'publishes. Above 2,000 delegates seated in one room the field is four rooms, and three '
    'of them are inside MCEC. The fourth is Crown’s Palladium at 2,300 theatre.',
    '<b>Between 500 and 1,500 delegates the constraint is accommodation, not the room.</b> '
    'The largest single conference hotels in the city publish 419 rooms at Pullman East '
    'Melbourne and 363 at Sofitel Melbourne on Collins, so a 1,500 delegate residential '
    'conference is a multi property block by definition. The exception is Crown at Southbank, '
    'which runs three hotels on one riverside site alongside its event floors and is the '
    'closest Melbourne gets to a self contained conference campus.',
    '<b>The thing worth knowing about Melbourne is that the volume and the character are in '
    'different places.</b> The exhibition floor and the big plenaries are at South Wharf and '
    'Southbank; the laneways, small bars and theatres that delegates actually want in their '
    'free time are in the CBD grid across the river. A South Wharf program needs a deliberate '
    'plan to get people into the city rather than an assumption that they will wander. '
    '<a href="#melbourne-featured">See the venues we would start with</a>.'],
  featured=[
    ('melbourne-convention-and-exhibition-centre',
     'Large association congresses and trade exhibitions running side by side.'),
    ('crown-melbourne',
     'Residential conferences of 500 to 1,500 that want the plenary, the gala and the beds on one site.'),
    ('sofitel-melbourne-on-collins',
     'Premium conferences and launches where the delegate profile matters more than the count.'),
    ('pullman-east-melbourne',
     'Single hotel residential conferences up to 850, and programs with a sporting component.'),
    ('marvel-stadium',
     'Vehicle reveals, consumer launches and very large receptions.'),
    ('melbourne-town-hall',
     'Gala dinners and awards nights where the address does part of the work.')],
  sources=['Convention centre space at South Wharf for plenary and exhibition together',
           'CBD and Southbank conference hotels, and multi property delegate blocks',
           'Heritage and civic rooms for gala dinners and awards nights',
           'Stadium and museum spaces for launches and large receptions',
           'Yarra Valley and Mornington Peninsula offsites within ninety minutes'],
  precincts=['South Wharf', 'Southbank', 'CBD grid and Collins Street', 'Docklands',
             'East Melbourne and Melbourne Park', 'Carlton and Parkville'],
  start=[
    ('Large conferences and exhibitions', 'MCEC, and realistically only MCEC above 2,000 seated'),
    ('Residential conferences', 'Crown Melbourne, Pullman East Melbourne, Sofitel on Collins'),
    ('Premium gala dinners', 'Crown Palladium for volume, Melbourne Town Hall for the address'),
    ('Product launches and brand events', 'Marvel Stadium, Melbourne Museum, Sofitel Grand Ballroom'),
    ('Leadership retreats', 'The <a href="venue-finder-yarra-valley.html">Yarra Valley</a> or the <a href="venue-finder-mornington-peninsula.html">Mornington Peninsula</a>, not the city'),
    ('Fly in, fly out meetings', 'CBD hotels near Southern Cross rather than the airport')],
  local=[
    ('South Wharf', 'The only precinct that does a plenary above 1,500 and a trade floor at the same time. Two hotels connect directly into MCEC, so the delegate experience is genuinely campus like.'),
    ('Southbank', 'Crown puts the room block, the ballroom and the dinner in one complex, which is the strongest single site block in the city. Riverside walking connection to both South Wharf and the CBD.'),
    ('CBD grid', 'Choose it when delegate free time is part of the value. Deep hotel supply at every price point, but no single property holds a large block, and the Metro Tunnel stations opened here in late 2025.'),
    ('Docklands', 'Scale and a waterfront setting rather than a hotel one. Marvel Stadium anchors it for launches and very large receptions, with thinner accommodation than the CBD.'),
    ('East Melbourne', 'A large single hotel block on the quiet edge of the city, with the MCG and Melbourne Park next door. Unusable in January while the Australian Open runs.'),
    ('Carlton and Parkville', 'Character venues and anything with a university, research or cultural association behind it. Almost no hotel supply, so delegates stay in the city and tram across.')],
  tradeoffs=[
    ('January and March are difficult months',
     'The Australian Open absorbs city accommodation for three weeks in January and puts the whole Melbourne Park precinct out of contention. The Formula 1 Grand Prix does something similar to March. Both are worth checking against your dates before you fall in love with a venue.'),
    ('There is no airport rail line yet',
     'Victoria’s own project page puts the first stage of Melbourne Airport Rail at 2030, so every fly in delegate is on a road transfer of roughly half an hour. For a genuine same day in and out meeting we would usually put Sydney or Brisbane in front of you.'),
    ('One large ballroom is currently out of the market',
     'Grand Hyatt Melbourne’s event floor is listed by the hotel as closed for upgrade works with no reopening date, while the guest rooms operate normally. It is worth knowing if a Collins Street ballroom was on your list from a previous year.')],
  why_h2='Melbourne is two markets, and most briefs only need one of them.',
  why_lead='South Wharf and the CBD grid behave completely differently, and the choice between them decides how far delegates walk, what they do at six o’clock and what the accommodation costs. We start there rather than with a list of rooms.',
  faqs=[
    ('How much does it cost to use CVBS to find a venue in Melbourne?', 'FREE'),
    ('How quickly can you find Melbourne venues?', 'FAST'),
    ('What is the largest conference venue in Melbourne?',
     'The Melbourne Convention and Exhibition Centre at South Wharf. Its Plenary seats 5,564 theatre style and it publishes 40,000 square metres of pillarless exhibition space across 26 bays. Above 2,000 seated in one room, MCEC and Crown’s Palladium are the only options in the city.'),
    ('Where should a 500 delegate conference be held in Melbourne?',
     'It depends on whether the delegates are staying overnight. If they are, Crown at Southbank or Pullman East Melbourne will hold the plenary and most of the room block in one building. If they are not, the CBD gives you a much wider choice and puts people into the laneways at the end of the day.'),
    ('Can one Melbourne hotel accommodate a 1,000 delegate residential conference?',
     'Not in a single branded property. The largest conference hotels in the city publish 419 and 363 rooms, so a thousand delegate residential program is a multi property block. Crown is the closest thing to an exception because it operates three hotels on one site.'),
    ('Do you cover group accommodation in Melbourne as well as venues?', 'GROUP'),
    ('Is Melbourne a good choice for a leadership retreat?',
     'Rarely, in the city itself. Melbourne’s strength is scale and urban energy, which is the opposite of what a retreat wants. The Victorian retreat product is regional, in the <a href="venue-finder-yarra-valley.html">Yarra Valley</a>, on the <a href="venue-finder-mornington-peninsula.html">Mornington Peninsula</a> and around Daylesford, all within about ninety minutes of the city.'),
    ('When should we book a Melbourne conference venue?',
     'For anything above 500 delegates at MCEC or Crown, as early as you can. For a CBD hotel conference under 300 the rooms are usually available, and the question becomes the rate and whether your dates collide with the Australian Open in January or the Grand Prix in March.')],
  related=[
    ('venue-finder-yarra-valley.html', 'Yarra Valley',
     'An hour from the city, and where a Melbourne leadership program usually belongs.'),
    ('venue-finder-mornington-peninsula.html', 'Mornington Peninsula',
     'Coast, vineyards and exclusive use properties for an offsite that has to feel separate.'),
    ('conference-venues-with-accommodation.html', 'Venues with accommodation',
     'The venues that hold the plenary and the delegates in the same building.')],
)

# ------------------------------------------------------------------- BRISBANE
DEST['Brisbane'] = dict(
  file='venue-finder-brisbane.html', state='QLD',
  title='Conference &amp; Event Venues in Brisbane | CVBS',
  meta=('Brisbane conference and event venue finding. BCEC, South Bank, Queen’s Wharf and '
        'CBD venues with published capacities, precinct guidance and a shortlist within 48 hours, '
        'free to you.'),
  h1='Conference &amp; Event Venues in Brisbane',
  lead='Tell us what you need in Brisbane. Shortlist within 48 hours, free to you.',
  snapshot=[
    '<b>Brisbane’s largest conference and banqueting room is the Great Hall at the Brisbane '
    'Convention and Exhibition Centre, at 3,958 theatre across 4,088 square metres.</b> BCEC also '
    'carries four exhibition halls of 5,000 square metres each and 44 meeting spaces, which is why '
    'almost every national association conference in the city ends up at South Bank. The Plaza '
    'Ballroom next door takes 2,000.',
    '<b>Above 2,000 seated in one room, Brisbane is a two venue city.</b> BCEC’s Great Hall and '
    'the combined halls at the Royal International Convention Centre in Bowen Hills are the only '
    'rooms that reach it, and there is no third fallback. Lead times for a 2,000 plus plenary are '
    'long as a result. Between 1,000 and 2,000 the choice widens usefully to The Star Brisbane '
    'Event Centre at Queen’s Wharf, Brisbane City Hall and Sofitel Brisbane Central, whose '
    'Ballroom Le Grand at 1,056 theatre is the largest hotel ballroom in the city by published '
    'theatre capacity.',
    '<b>Brisbane’s real advantage is compactness.</b> BCEC, the state galleries, the museum '
    'and a run of hotels sit in one walkable riverfront precinct, twenty minutes from a single '
    'airport by train. The trade off is that the city is in a decade long construction cycle to '
    '2032, and it is removing outdoor and parkland event options rather than adding them: Victoria '
    'Park closed as a function venue on 31 May 2026. <a href="#brisbane-featured">See the venues '
    'we would start with</a>.'],
  featured=[
    ('brisbane-convention-exhibition-centre',
     'National and international association conferences with a trade floor running alongside.'),
    ('sofitel-brisbane-central',
     'A thousand delegate plenary, the breakouts and the beds without crossing a road.'),
    ('the-star-brisbane-event-centre',
     'Gala dinners and awards nights inside a single self contained complex.'),
    ('royal-international-convention-centre',
     'Trade shows and exhibitions, and the alternative when BCEC is held.'),
    ('brisbane-city-hall',
     'Ceremonial plenaries and gala dinners where the room itself is the point.'),
    ('howard-smith-wharves',
     'Welcome functions, riverfront dinners and client entertaining under the Story Bridge.')],
  sources=['Convention centre space at South Bank for plenary and exhibition together',
           'CBD conference hotels and delegate room blocks',
           'Riverfront and heritage venues for dinners, awards and launches',
           'Airport precinct meeting space for fly in, fly out programs',
           'Gold Coast and Sunshine Coast resorts for the reward half of a program'],
  precincts=['South Bank', 'Brisbane CBD', 'Queen’s Wharf', 'Howard Smith Wharves',
             'Fortitude Valley and James Street', 'Bowen Hills', 'Brisbane Airport'],
  start=[
    ('Large conferences and exhibitions', 'BCEC, or Royal ICC at Bowen Hills'),
    ('Residential conferences', 'Sofitel Brisbane Central, Pullman King George Square, The Star Brisbane'),
    ('Premium gala dinners', 'Brisbane City Hall, The Star Brisbane Event Centre, BCEC Great Hall'),
    ('Product launches and brand events', 'Howard Smith Wharves, Brisbane Powerhouse, W Brisbane'),
    ('Fly in, fly out meetings', 'Pullman Brisbane Airport, or Sofitel above Central Station'),
    ('Incentives', 'Brisbane as the gateway, with the reward on the <a href="venue-finder-gold-coast.html">Gold Coast</a> or the <a href="venue-finder-sunshine-coast.html">Sunshine Coast</a>')],
  local=[
    ('South Bank', 'The only precinct that does plenary and exhibition in the same building. Seventeen hectares of riverfront parkland with the galleries, museum and performing arts centre on the same strip, and the Grey Street hotel cluster next door.'),
    ('Brisbane CBD', 'The deepest hotel supply and the shortest walks. Sofitel sits above Central Station, Pullman and Mercure share King George Square, and everything is five to ten minutes on foot.'),
    ('Queen’s Wharf', 'A single building program with gala scale, hotel rooms, restaurants and bars on the river. Walkable to the CBD core and across the footbridge to South Bank.'),
    ('Howard Smith Wharves', 'The evening, not the day. Seventeen riverfront spaces under the Story Bridge, mostly bars, restaurants and heritage sheds, with a hotel on site.'),
    ('Fortitude Valley', 'Smaller premium and design led programs, and the strongest restaurant and bar density in the city. One stop on the rail line from Central.'),
    ('Brisbane Airport', 'When the point is not entering the city. Pullman, Novotel and ibis share the Brisbane Airport Conference Centre, so build the food and drink into the venue.')],
  tradeoffs=[
    ('August is difficult around the Showgrounds',
     'The Ekka runs in the middle of August each year with a Brisbane public holiday inside it, and bump in and bump out extend that window either side. Royal ICC is effectively out of the market for the month.'),
    ('September is the busiest month for accommodation',
     'Brisbane Festival runs through September with Riverfire early in the month, which draws the whole city to the river. Riverfront venues and CBD hotels are hardest hit, and it is the month we most often have to work around.'),
    ('The last airport train leaves at 10:04pm',
     'Airtrain runs every fifteen minutes and puts the terminals twenty minutes from the city, but anyone leaving a gala dinner after about half past nine is on a taxi or a rideshare. It is worth a line in the delegate pack rather than a surprise.')],
  why_h2='Brisbane is compact, and that is the whole argument for it.',
  why_lead='A near 4,000 seat plenary, 20,000 square metres of exhibition and 44 breakout rooms sit in one building, inside a walkable cultural precinct, twenty minutes from one airport. We start with whether your program actually needs that, because if it does not, the CBD gives you a better week.',
  faqs=[
    ('How much does it cost to use CVBS to find a venue in Brisbane?', 'FREE'),
    ('How quickly can you find Brisbane venues?', 'FAST'),
    ('What is the largest conference venue in Brisbane?',
     'The Brisbane Convention and Exhibition Centre at South Bank. Its Great Hall seats 3,958 theatre across 4,088 square metres, and it carries four exhibition halls of 5,000 square metres each alongside 44 meeting spaces.'),
    ('Which Brisbane hotel has the largest ballroom?',
     'Sofitel Brisbane Central, whose Ballroom Le Grand seats 1,056 theatre in a 798 square metre room under a 6.5 metre ceiling. The hotel has 416 rooms above it and sits directly over Central Station.'),
    ('Where should a 500 delegate conference be held in Brisbane?',
     'Sofitel Brisbane Central or Pullman Brisbane King George Square will both hold the plenary, the breakouts and most of the room block in one building. If the program needs an exhibition floor as well, it belongs at BCEC with a South Bank or CBD room block alongside it.'),
    ('Do you cover group accommodation in Brisbane as well as venues?', 'GROUP'),
    ('Is Brisbane a good incentive destination?',
     'Brisbane is usually the arrival and departure city rather than the reward. It is a strong gateway, and most incentive programs we source put the content on the <a href="venue-finder-gold-coast.html">Gold Coast</a>, the <a href="venue-finder-sunshine-coast.html">Sunshine Coast</a> or the reef, with a Brisbane night either side.'),
    ('How far is Brisbane Airport from the conference precinct?',
     'BCEC lists itself as thirteen kilometres from the airport, and Airtrain runs the route in about twenty minutes every fifteen minutes. The last service leaves the airport at 10:04pm, which matters if your program has a late finish.')],
  related=[
    ('venue-finder-gold-coast.html', 'Gold Coast',
     'An hour south, and the answer when the program wants a resort rather than a city.'),
    ('venue-finder-sunshine-coast.html', 'Sunshine Coast',
     'Beachfront residential conferences and a genuine hinterland for smaller retreats.'),
    ('venue-visits/', 'Venues we have walked',
     'Our own photographs and honest notes from the rooms we have been through.')],
)

# ---------------------------------------------------------------------- PERTH
DEST['Perth'] = dict(
  file='venue-finder-perth.html', state='WA',
  title='Conference &amp; Event Venues in Perth | CVBS',
  meta=('Perth conference and event venue finding. PCEC, Crown Perth, Optus Stadium, CBD '
        'hotels, Fremantle and the Swan Valley, with published capacities and a shortlist within '
        '48 hours, free to you.'),
  h1='Conference &amp; Event Venues in Perth',
  lead='Tell us what you need in Perth. Shortlist within 48 hours, free to you.',
  snapshot=[
    '<b>Perth’s largest conference venue is the Perth Convention and Exhibition Centre at the '
    'edge of Elizabeth Quay.</b> Its Riverside Theatre seats up to 2,500 in a tiered auditorium, '
    'the BelleVue Ballroom takes 1,700, and six pavilions combine to 16,644 square metres of '
    'exhibition floor. The state government discontinued the redevelopment in November 2025, so '
    'the building you inspect today is the building you will get.',
    '<b>Above 2,000 seated in one room only three buildings work, and two of them are at '
    'Burswood.</b> PCEC’s Riverside Theatre, Crown Perth’s 2,000 square metre Crown Ballroom at '
    '2,400 theatre, and RAC Arena for a 2,500 person standing reception. Crown is also the only '
    'place in Western Australia where a conference of 1,500 or more can meet, dine and sleep '
    'without leaving the site, with 1,188 rooms across three hotels.',
    '<b>In the city itself, accommodation becomes the constraint well before the room does.</b> '
    'The largest single conference hotels publish 488 rooms at Pan Pacific and 300 at the '
    'Esplanade in Fremantle, so a 2,000 delegate PCEC plenary is a block across five or more '
    'properties. The compensation is geography: almost all the serious capacity sits in two '
    'precincts about four kilometres apart, so once delegates land, Perth is an unusually simple '
    'destination to run. <a href="#perth-featured">See the venues we would start with</a>.'],
  featured=[
    ('perth-convention-and-exhibition-centre',
     'Multi stream conferences with a trade floor, and anything needing a tiered plenary.'),
    ('crown-perth',
     'Residential conferences above 1,000, and the state’s largest gala room.'),
    ('hyatt-regency-perth',
     'City centre residential conferences up to 1,000 in a square, round table friendly ballroom.'),
    ('optus-stadium',
     'Conferences and dinners that want a view and do not need attached accommodation.'),
    ('the-ritz-carlton-perth',
     'Premium headquarters hotel for a PCEC conference, and dinners that should feel considered.'),
    ('esplanade-hotel-fremantle-by-rydges',
     'Residential programs and incentive nights that want the port town rather than the city.')],
  sources=['Convention centre space at Elizabeth Quay for plenary and exhibition together',
           'Perth CBD conference hotels and multi property delegate blocks',
           'Burswood venues for large galas, awards and stadium format events',
           'Fremantle and Swan Valley venues for offsites, dinners and launches',
           'Airport adjacent meeting space for fly in, fly out and resources sector programs'],
  precincts=['Perth CBD', 'Elizabeth Quay', 'Burswood', 'Northbridge', 'Fremantle', 'Swan Valley'],
  start=[
    ('Large conferences and exhibitions', 'Perth Convention and Exhibition Centre'),
    ('Residential conferences', 'Crown Perth, Pan Pacific Perth, Hyatt Regency Perth'),
    ('Premium gala dinners', 'Crown Ballroom for volume, The Ritz-Carlton for a smaller room'),
    ('Leadership retreats', 'The Ritz-Carlton, Swan Valley estates, or Margaret River further south'),
    ('Product launches and brand events', 'RAC Arena, Optus Stadium, Sandalford in the Swan Valley'),
    ('Fly in, fly out meetings', 'Optus Stadium and Crown at Burswood, fifteen minutes from the airport')],
  local=[
    ('Elizabeth Quay', 'Where the event is the reason people came. PCEC anchors it, the Ritz-Carlton is across the road, and Elizabeth Quay station is minutes away. Rooms are spread across several hotels rather than attached.'),
    ('Perth CBD east end', 'Adelaide Terrace and Hibernian Place carry the 300 to 1,000 delegate residential conferences, with Hyatt Regency, Pan Pacific and The Westin close together and the meeting space in the same buildings as the beds.'),
    ('Burswood', 'Everything on one site, or the biggest flat floor room in the state. Crown and Optus Stadium sit side by side, fifteen minutes from the airport. Weekday rail is limited, so delegates drive or shuttle.'),
    ('Northbridge and Wellington Street', 'Large receptions, launches and the delegate social program. RAC Arena brings 2,500 cocktail capacity and 680 car bays, with Northbridge dining immediately north.'),
    ('Fremantle', 'Character and separation without leaving the metro area. The Esplanade carries 300 rooms and a 799 square metre ballroom, about half an hour from both the airport and the city.'),
    ('Swan Valley', 'Dinners, launches and single day offsites in a vineyard setting half an hour from the city. Accommodation is thin at conference scale, so a city hotel usually underwrites it.')],
  tradeoffs=[
    ('Perth is a transcontinental flight and its own time zone',
     'Every east coast delegate is on a long flight into a different clock, which pushes most programs to a two night minimum and lifts the airfare line of the budget. It is the single biggest thing to price honestly at the start rather than discover later.'),
    ('March 2027 is compromised in the city',
     'The World Police and Fire Games run 12 to 21 March 2027 with more than 8,500 participants and PCEC as the Games hub, with the associated convention immediately before. Treat that window as unavailable for both venue and room block.'),
    ('RAC Arena releases dates, you do not choose them',
     'The arena floor and its function rooms are only available on non event days, so availability follows the touring calendar. If it is on your list, we check the release before we let you hold a date around it.')],
  why_h2='Perth is two precincts four kilometres apart, and the choice decides the week.',
  why_lead='Elizabeth Quay and Burswood behave completely differently. One puts delegates into a walkable city with rooms spread across several hotels; the other puts everything on one site with a shuttle to anywhere else. We start with which of those your program actually needs.',
  faqs=[
    ('How much does it cost to use CVBS to find a venue in Perth?', 'FREE'),
    ('How quickly can you find Perth venues?', 'FAST'),
    ('What is the largest conference venue in Perth?',
     'The Perth Convention and Exhibition Centre. Its Riverside Theatre seats up to 2,500 in a tiered auditorium, the BelleVue Ballroom takes 1,700, and six exhibition pavilions combine to 16,644 square metres.'),
    ('Which Perth venue can hold a 1,500 delegate residential conference?',
     'Crown Perth at Burswood is the only one that can do it on a single site. It publishes 1,188 rooms across three hotels alongside the 2,000 square metre Crown Ballroom, which seats 2,400 theatre and divides into five.'),
    ('Do you cover group accommodation in Perth as well as venues?', 'GROUP'),
    ('How far is Perth Airport from the city?',
     'Twelve kilometres. The Airport Line puts Airport Central about eighteen minutes from Perth Station, but it serves terminals one and two directly, so confirm which terminal your delegates arrive at before you promise anyone a train. Burswood is about fifteen minutes from the airport by road.'),
    ('Can we hold a conference in the Swan Valley?',
     'For a dinner, a launch or a single day offsite, comfortably. For a multi day residential program, not really: the estates have function buildings but very little accommodation, so the group ends up coaching back to a city hotel each night. We would usually put the plenary in the city and the Swan Valley in the evening.'),
    ('What is the biggest gala dinner room in Perth?',
     'The Crown Ballroom at Burswood, which publishes 1,510 banquet in a 2,000 square metre pillarless room with eight metre ceilings. In the city itself the largest hotel ballroom that publishes a capacity chart is Hyatt Regency Perth at 870 square metres.')],
  related=[
    ('venue-visits/pullman-bunker-bay/', 'Pullman Bunker Bay',
     'A resort in the Margaret River region we have walked through ourselves.'),
    ('cbd-vs-resort-conference-venues.html', 'City or resort',
     'Whether Burswood, the city or a South West resort is the right base for the program.'),
    ('conference-venues-with-accommodation.html', 'Venues with accommodation',
     'The venues that hold the plenary and the delegates in the same building.')],
)

# ------------------------------------------------------------------- ADELAIDE
DEST['Adelaide'] = dict(
  file='venue-finder-adelaide.html', state='SA',
  title='Conference &amp; Event Venues in Adelaide | CVBS',
  meta=('Adelaide conference and event venue finding. The Riverbank precinct, Adelaide Oval, '
        'the Showground and the wine regions, with published capacities and a shortlist within '
        '48 hours, free to you.'),
  h1='Conference &amp; Event Venues in Adelaide',
  lead='Tell us what you need in Adelaide. Shortlist within 48 hours, free to you.',
  snapshot=[
    '<b>Adelaide’s conference market runs on the Riverbank, and the Adelaide Convention Centre '
    'is the centre of it.</b> Hall ABCD is a tiered plenary seating 3,017 across 2,544 square '
    'metres, and the flat floor Hall H next door takes up to 3,000 theatre and 1,670 banquet in '
    '2,980 square metres. That is where any Adelaide conference over about 800 delegates ends up.',
    '<b>Above roughly 3,000 in one room the venues are at Wayville, not on the Riverbank.</b> '
    'Adelaide Showground’s Jubilee Pavilion is 8,742 square metres seating 7,000, with the Goyder '
    'Pavilion alongside at 8,000 square metres, and the two combine to 17,250. There is no '
    'accommodation on the 27 hectare site, so the trade off for that floor area is shuttles and a '
    'split delegate experience.',
    '<b>No Adelaide hotel publishes a ballroom above 800, which sets the real ceiling on a '
    'single property residential conference.</b> The largest is Amora Hotel Adelaide at 780 theatre '
    'with 380 rooms above it, and the largest city hotels sit around 380 and 367 rooms, so blocks '
    'split early. What Adelaide gives you in return is compactness and three wine regions inside an '
    'hour of the airport, which is why it wins incentive and offsite business well above its size. '
    '<a href="#adelaide-featured">See the venues we would start with</a>.'],
  featured=[
    ('adelaide-convention-centre',
     'Association congresses, government summits and medical conferences up to about 3,000.'),
    ('amora-hotel-adelaide',
     'Single building residential conferences of 200 to 700 with a produced plenary.'),
    ('adelaide-oval',
     'Large dinners and awards nights with the city and the river through the glass.'),
    ('adelaide-showground',
     'Trade exhibitions and expos that need genuine large format floor.'),
    ('national-wine-centre-of-australia',
     'Mid size dinners and conferences that should feel like South Australia.'),
    ('novotel-barossa-valley-resort',
     'Residential offsites and incentives that stay in the Barossa rather than bussing back.')],
  sources=['Riverbank precinct and convention centre space',
           'CBD conference hotels and delegate room blocks',
           'Stadium and civic venues for large dinners and awards',
           'Adelaide Hills, Barossa and McLaren Vale retreat and incentive venues',
           'Exhibition floor at Wayville for trade shows and expos'],
  precincts=['Riverbank and North Terrace', 'Victoria Square', 'East End and Botanic Gardens',
             'Wayville', 'Adelaide Hills', 'Barossa Valley', 'McLaren Vale'],
  start=[
    ('Large conferences and exhibitions', 'Adelaide Convention Centre, or the Showground above 3,000'),
    ('Residential conferences', 'Amora Hotel Adelaide, Adelaide Hills Convention Centre'),
    ('Premium gala dinners', 'Adelaide Oval, ACC Hall H, National Wine Centre'),
    ('Leadership retreats', 'Adelaide Hills estates, Novotel Barossa Valley Resort'),
    ('Incentives', 'Barossa and McLaren Vale winery programs, with Eos as the city base'),
    ('Fly in, fly out meetings', 'Adelaide Oval and Riverbank hotels, fifteen minutes from the airport')],
  local=[
    ('Riverbank and North Terrace', 'Everything a conference needs within a few minutes of itself: the convention centre, InterContinental, SkyCity and Eos, the Festival Centre and Adelaide Oval. Individual hotels are mid sized, so blocks above about 400 rooms split.'),
    ('Victoria Square', 'When the whole event should live in one building. Amora gives you 380 rooms, nineteen meeting rooms and a 780 theatre ballroom on a single conference floor, on the tram line.'),
    ('East End and Botanic Gardens', 'Character rather than scale. The National Wine Centre and the parklands edge, with Rundle Street dining a short walk away and no accommodation on site.'),
    ('Wayville', 'Only when the numbers force it. Two pavilions combining to 17,250 square metres, no accommodation, and shuttles from the city as the price of that floor area.'),
    ('Adelaide Hills', 'A group that should leave the city but stay inside forty minutes. Hahndorf carries a purpose built conference building with accommodation adjacent, and the estates around it suit board offsites.'),
    ('Barossa and McLaren Vale', 'Where wine is the point and the group sleeps on site. Novotel Barossa is the only property in the valley with enough rooms to hold a whole conference, at a stated maximum of 250.')],
  tradeoffs=[
    ('February and March are the hardest dates to hold',
     'Adelaide Fringe, the Adelaide Festival and WOMADelaide overlap across late February and March, and both rates and availability tighten sharply across the city. January carries the Tour Down Under and March also carries LIV Golf. Events do run in those windows, but they are booked earlier and they cost more, so bring us the dates first and we will tell you what is still open rather than guessing from a calendar.'),
    ('Scale and walkability are not available in the same place',
     'Everything above about 3,000 in one room sits at Wayville, outside the walkable Riverbank hotel cluster. Below that threshold Adelaide is unusually compact. Above it, it stops being a walk everywhere city and becomes a coaching exercise.'),
    ('A true single hotel residential conference caps at about 400',
     'No Adelaide hotel publishes a ballroom above 800 theatre, and the largest properties sit around 380 rooms. Above roughly 400 delegates staying overnight, the program is a multi property block whatever the plenary room says.')],
  why_h2='Adelaide punches above its size, and it is worth knowing why.',
  why_lead='Short airport transfers, a genuinely walkable Riverbank and three wine regions inside an hour are why Adelaide wins conference and incentive business against much larger cities. The constraint is hotel scale, and knowing where that bites is most of the job.',
  faqs=[
    ('How much does it cost to use CVBS to find a venue in Adelaide?', 'FREE'),
    ('How quickly can you find Adelaide venues?', 'FAST'),
    ('What is the largest conference venue in Adelaide?',
     'For a conference, the Adelaide Convention Centre, whose Hall ABCD seats 3,017 in tiered seating and whose flat floor Hall H takes up to 3,000 theatre and 1,670 banquet. For pure exhibition floor, the Adelaide Showground at Wayville is larger, with two pavilions combining to 17,250 square metres.'),
    ('Which Adelaide hotel is best for a residential conference?',
     'Amora Hotel Adelaide on Victoria Square is the largest, with 380 rooms, nineteen meeting rooms and a 780 theatre ballroom on one conference floor. It was the Hilton Adelaide until the rebrand, so older venue lists may still carry the previous name.'),
    ('Do you cover group accommodation in Adelaide as well as venues?', 'GROUP'),
    ('Can we run a conference in the Barossa Valley?',
     'Up to about 250 delegates, and only at Novotel Barossa Valley Resort, which is the one property in the valley with enough rooms to hold a whole group on site. Anything larger runs from an Adelaide base with a Barossa day, which is about an hour each way.'),
    ('When should we avoid holding an event in Adelaide?',
     'Late February and March, when Adelaide Fringe, the Adelaide Festival and WOMADelaide overlap and city accommodation tightens sharply. January carries the Tour Down Under. None of these make an event impossible, but they change the rate and the availability, so we check your dates against them first.'),
    ('How close is Adelaide Airport to the conference precinct?',
     'Close enough that a single day fly in and fly out meeting genuinely works, which is unusual. Business Events Adelaide publishes Adelaide Oval on the Riverbank as fifteen minutes from the airport.')],
  related=[
    ('venue-finder-melbourne.html', 'Melbourne',
     'The nearest capital when the numbers outgrow what Adelaide can hold in one room.'),
    ('cbd-vs-resort-conference-venues.html', 'City or resort',
     'When the Hills, the Barossa or McLaren Vale beat a city hotel, and when they do not.'),
    ('conference-venues-with-accommodation.html', 'Venues with accommodation',
     'The Adelaide properties that hold the plenary and the delegates in one building.')],
)

# ------------------------------------------------------------------- CANBERRA
DEST['Canberra'] = dict(
  file='venue-finder-canberra.html', state='ACT',
  title='Conference &amp; Event Venues in Canberra | CVBS',
  meta=('Canberra conference and event venue finding for government and association programs. '
        'The National Convention Centre, Barton hotels and the national institutions, with a '
        'shortlist within 48 hours, free to you.'),
  h1='Conference &amp; Event Venues in Canberra',
  lead='Tell us what you need in Canberra. Shortlist within 48 hours, free to you.',
  snapshot=[
    '<b>Canberra’s purpose built conference building is the National Convention Centre, and '
    'its Royal Theatre is the largest tiered auditorium in the territory at 1,710 raked seats, '
    '2,460 theatre in total.</b> The constraint there is not the plenary, it is the exhibition '
    'floor: the Exhibition Hall is 2,000 square metres with a nine metre ceiling and 120 booths, '
    'which is small by capital city standards. Anything larger goes to Exhibition Park in Mitchell, '
    'a separate site with no adjacent hotels.',
    '<b>Only one Canberra hotel seats a thousand in a single room.</b> QT Canberra’s pillarless '
    'Grand Ballroom takes 1,000 theatre across 830 square metres with 205 rooms above it. The next '
    'tier is Hotel Realm in Barton at 800 theatre and the Hyatt at 500, so a residential conference '
    'much above a thousand delegates is split across four or more properties out of a citywide pool '
    'of roughly 7,500 rooms.',
    '<b>What Canberra does that nowhere else in Australia can is the national institutions.</b> '
    'The National Museum’s Gandel Atrium takes a thousand for a reception or 500 seated, the '
    'National Gallery’s Gandel Hall is the gala dinner room of the Parliamentary Triangle, and '
    'Australian Parliament House hires event space of its own. Combine that with departmental '
    'proximity and a convention centre in a walkable city centre and you have the reason association '
    'boards keep choosing Canberra. <a href="#canberra-featured">See the venues we would start '
    'with</a>.'],
  featured=[
    ('national-convention-centre-canberra',
     'National association and government conferences of 500 to 2,000 delegates.'),
    ('qt-canberra',
     'A thousand seat residential conference with the delegates upstairs.'),
    ('hotel-realm',
     'Anything with a Parliament House, department or peak body agenda.'),
    ('national-museum-of-australia',
     'Conference dinners for 500 and receptions for a thousand on the lake.'),
    ('national-gallery-of-australia',
     'Gala dinners and one day summits with a plenary theatre on the same site.'),
    ('exhibition-park-in-canberra',
     'Trade shows and expos beyond what the convention centre can hold.')],
  sources=['Convention centre space in the city centre for plenary and exhibition',
           'Barton and city hotels for government and association room blocks',
           'National institutions for gala dinners, receptions and launches',
           'Exhibition floor at Mitchell for trade shows and expos',
           'Airport precinct meeting rooms for same day committee meetings'],
  precincts=['City and Civic', 'Parliamentary Triangle', 'Barton', 'Kingston Foreshore',
             'Braddon', 'Canberra Airport and Brindabella Park', 'Mitchell'],
  start=[
    ('Government and association conferences', 'National Convention Centre, Hotel Realm, Australian Parliament House'),
    ('Large conferences and exhibitions', 'National Convention Centre, or Exhibition Park for the floor area'),
    ('Residential conferences', 'QT Canberra, Hotel Realm, Hyatt Hotel Canberra'),
    ('Premium gala dinners', 'National Gallery Gandel Hall, National Museum Gandel Atrium, Hyatt Federation Ballroom'),
    ('Product launches and brand events', 'Kambri at ANU, the National Portrait Gallery, Questacon'),
    ('Fly in, fly out meetings', 'Brindabella Park at the airport, or Barton for a half day')],
  local=[
    ('City and Civic', 'Where the convention centre is the plenary and delegates walk between venue, hotel and dinner. Crowne Plaza sits beside the centre and Novotel is a few blocks up Northbourne, which is the deepest walkable room block in the city.'),
    ('Parliamentary Triangle', 'The venues you cannot get anywhere else: the National Gallery, the National Museum, Old Parliament House, the Portrait Gallery, Questacon. Essentially no hotel accommodation of its own, so delegates sleep in Barton or Civic and coach in.'),
    ('Barton', 'When the agenda is government, defence or peak body and proximity to Parliament House matters more than proximity to the convention centre. Hotel Realm plus the hotels around it give you a conference and its room block in one small pocket.'),
    ('Kingston Foreshore', 'Dining, drinks and the social program rather than plenary space. Accommodation is apartment led rather than large blocks, and it is a short drive from both Barton and the Triangle.'),
    ('Braddon', 'Informal dine arounds, breakout dinners and brand events with a younger audience, five to ten minutes on foot from the city hotels and the convention centre.'),
    ('Mitchell and Bruce', 'Only when the room size forces you out of the city. Exhibition Park for floor beyond 2,000 square metres, AIS Arena for a seated audience above 3,000. Neither has hotels alongside it.')],
  tradeoffs=[
    ('Sitting weeks are the first thing to check',
     'The Canberra Convention Bureau tells planners plainly to work around the Federal Parliament sitting calendar, which is released each November. Accommodation and rates move sharply in a sitting week and a lot of the audience you want in the room is unavailable.'),
    ('Floriade compresses a month of accommodation',
     'Floriade runs from mid September to mid October in Commonwealth Park and draws hundreds of thousands of visitors. It is a wonderful thing to have on a delegate program and a difficult thing to book a room block against.'),
    ('The exhibition floor is the ceiling, not the plenary',
     'The Royal Theatre will hold 2,460, but the Exhibition Hall is 2,000 square metres. If your trade floor needs more than that, the exhibition and the accommodation cannot sit in the same precinct, because Exhibition Park has no hotels beside it. A larger convention centre is planned, but its business case is not expected before mid 2028.')],
  why_h2='Canberra rewards planners who know the parliamentary calendar.',
  why_lead='Departmental proximity, the national institutions and a convention centre in a walkable city centre are why association and government boards choose Canberra. Sitting weeks, Floriade and the exhibition floor limit are the three things that decide whether your dates will work, and we check all three before we shortlist.',
  faqs=[
    ('How much does it cost to use CVBS to find a venue in Canberra?', 'FREE'),
    ('How quickly can you find Canberra venues?', 'FAST'),
    ('What is the largest conference venue in Canberra?',
     'The National Convention Centre Canberra. Its Royal Theatre seats 2,460 theatre style, including 1,710 in tiered seating, which is the largest raked auditorium in the territory. For pure floor area, Exhibition Park’s Budawang Pavilion is larger at 3,310 square metres.'),
    ('Which Canberra hotel can hold a 1,000 delegate conference?',
     'QT Canberra is the only one. Its pillarless Grand Ballroom takes 1,000 theatre across 830 square metres and divides into thirds, with 205 rooms above it and a dedicated events floor for concurrent streams.'),
    ('Do you cover group accommodation in Canberra as well as venues?', 'GROUP'),
    ('Can we hold a conference dinner at a national institution?',
     'Yes, and it is the strongest thing Canberra offers. The National Museum’s Gandel Atrium takes 500 seated or 1,000 standing, the National Gallery’s Gandel Hall seats 360 for dinner with a 244 seat theatre alongside, and the Australian War Memorial hosts evening functions among its large objects. Most of these are after hours propositions around a working institution, so bump in windows are tight.'),
    ('How does the parliamentary sitting calendar affect a Canberra conference?',
     'Materially. Sitting weeks lift accommodation demand and rates across the city and take a lot of the government audience out of the room. The calendar is released each November, and it is the first thing we check against your preferred dates.'),
    ('Is Canberra a good incentive destination?',
     'Not in the classic sense. There is no resort, beach or alpine product, and the appeal is civic and institutional rather than experiential. Where it does work is a government adjacent audience for whom the national institutions themselves are the reward. For a conventional incentive we would point you elsewhere.')],
  related=[
    ('venue-finder-sydney.html', 'Sydney',
     'Three hours by road, and the alternative when the exhibition floor outgrows Canberra.'),
    ('conference-venue-finding.html', 'Conference venue finding',
     'How we source, negotiate and hold a conference venue from brief through to contract.'),
    ('how-to-brief-a-venue-finder.html', 'How to brief a venue finder',
     'What to send us so the first Canberra shortlist is worth reading.')],
)

# --------------------------------------------------------------------- HOBART
DEST['Hobart'] = dict(
  file='venue-finder-hobart.html', state='TAS',
  title='Conference &amp; Event Venues in Hobart | CVBS',
  meta=('Hobart conference and event venue finding. Waterfront venues, Wrest Point, Mona and '
        'the east coast lodges, with published capacities and a shortlist within 48 hours, free '
        'to you.'),
  h1='Conference &amp; Event Venues in Hobart',
  lead='Tell us what you need in Hobart. Shortlist within 48 hours, free to you.',
  snapshot=[
    '<b>The largest single room in Hobart is the Federation Ballroom at Hotel Grand Chancellor, '
    'at 1,200 theatre across 1,225 square metres.</b> The tiered Federation Concert Hall in the same '
    'complex seats 1,100, and because they are separate rooms you can run a plenary and the catering '
    'at the same time rather than turning a room. Wrest Point in Sandy Bay reaches further only by '
    'combining the Tasman Room with its Plenary Hall, at 1,651 theatre.',
    '<b>Accommodation, not floor space, is what actually limits a Hobart conference.</b> The five '
    'main business events hotels publish 271, 243, 241, 152 and 114 rooms between them, so a thousand '
    'delegate residential conference needs close to the entire premium inventory of the city at once. '
    'Business Events Tasmania markets the state’s working ceiling at around 1,100 delegates, and that '
    'is an honest number.',
    '<b>Where Hobart is unusually strong is high value programs under about 300.</b> The city is '
    'small and walkable, the food and drink are genuinely part of the sell, and the Antarctic, marine, '
    'agricultural and renewables research sitting on the doorstep makes site visits and study tours '
    'easy to build in. The practical constraint on delegate numbers is usually flight capacity rather '
    'than venue capacity. <a href="#hobart-featured">See the venues we would start with</a>.'],
  featured=[
    ('hotel-grand-chancellor-hobart',
     'The one complex that takes a full plenary, an exhibition and a gala without moving delegates.'),
    ('wrest-point',
     'Self contained residential conferences of 300 to 1,000 on the largest single site room block.'),
    ('crowne-plaza-hobart',
     'Straightforward mid size residential conferences in the city centre.'),
    ('the-tasman-luxury-collection',
     'Board level programs, incentives and awards dinners in a column free room.'),
    ('princes-wharf-1',
     'Trade exhibitions and gala dinners for 1,200 in a bare waterfront shed you build out.'),
    ('mona',
     'The one night of the program people will remember, reached by catamaran.')],
  sources=['Waterfront and city centre conference hotels',
           'A self contained residential conference campus at Sandy Bay',
           'Bare waterfront exhibition space for builds and trade displays',
           'Gallery, museum and distillery venues for dinners and receptions',
           'East coast and highland lodges for executive retreats and incentive rewards'],
  precincts=['Hobart CBD', 'Sullivans Cove waterfront', 'Salamanca and Battery Point',
             'Sandy Bay', 'Berriedale', 'Regional Tasmania'],
  start=[
    ('Large conferences and exhibitions', 'Hotel Grand Chancellor, Wrest Point, Princes Wharf 1'),
    ('Residential conferences', 'Wrest Point, Hotel Grand Chancellor, Crowne Plaza Hobart'),
    ('Premium gala dinners', 'Federation Ballroom, Wrest Point Tasman Room, Princes Wharf 1'),
    ('Leadership retreats', 'Saffire Freycinet, Peppers Cradle Mountain Lodge, The Tasman'),
    ('Incentives', 'Mona and the catamaran, Saffire on a buyout, waterfront dinners'),
    ('Product launches and brand events', 'Princes Wharf 1, Mona, The Tasman’s LUMINA')],
  local=[
    ('Hobart CBD', 'Where the plenary and the room block sit in the same few blocks. Hotel Grand Chancellor, Crowne Plaza and The Tasman are all within a short walk of each other and of Salamanca, and delegates will not need a car.'),
    ('Sullivans Cove waterfront', 'For a view or a raw space to brand. Princes Wharf 1 takes a full build, and the Mona ferry leaves from Brooke Street Pier, so offsite transfers start here.'),
    ('Salamanca and Battery Point', 'The dine around and the social program rather than the plenary. Very limited large function space and mostly boutique accommodation, walkable from the city and the waterfront, which is precisely its value.'),
    ('Sandy Bay', 'A self contained campus. Wrest Point holds the largest single site room block in Hobart, about five minutes from the city and twenty five from the airport, and the university next door suits academic meetings with tiered seating.'),
    ('Berriedale', 'One high impact evening rather than the working day. Mona takes 450 standing in the Nolan Gallery, about fifteen minutes by road or twenty five by catamaran, and the ferry is part of the experience.'),
    ('Regional Tasmania', 'When the destination is the point and the group is small. Freycinet suits an executive buyout of about forty, Cradle Mountain an offsite up to eighty five, and both are multi hour transfers, so build the flights around the lodge.')],
  tradeoffs=[
    ('Late December is effectively closed',
     'The Sydney to Hobart finishes into the city from 26 December and the summer waterfront festival runs through to early January, which takes Princes Wharf 1 out of the market and puts the whole city on peak rates. It is a wonderful week to be in Hobart and a difficult week to run a conference.'),
    ('Dark Mofo prices mid June like summer',
     'Winter is otherwise the value season here, but the Dark Mofo fortnight in June draws tens of thousands of interstate and overseas visitors and fills the city. Either build the program around it deliberately or avoid it.'),
    ('Air capacity sets the delegate number, not the venue',
     'There is no rail link anywhere in Tasmania and almost every mainland delegate flies. On most Hobart bids the practical ceiling on delegate numbers is seat availability into the city rather than the size of the room, so we look at the flight schedule before we look at floor plans.')],
  why_h2='Hobart is small, and that is exactly why it works for the right program.',
  why_lead='A walkable city, food and drink that carry a program on their own, and research institutions on the doorstep make Hobart unusually strong for high value events under about 300. The honest limit is that above roughly 1,200 in one seated plenary the destination stops working, and we will tell you that before you commit.',
  faqs=[
    ('How much does it cost to use CVBS to find a venue in Hobart?', 'FREE'),
    ('How quickly can you find Hobart venues?', 'FAST'),
    ('What is the largest conference venue in Hobart?',
     'The Federation Ballroom at Hotel Grand Chancellor Hobart is the largest single room, at 1,200 theatre across 1,225 square metres, with the tiered 1,100 seat Federation Concert Hall in the same complex. Wrest Point reaches 1,651 theatre by combining its Tasman Room with the Plenary Hall.'),
    ('How many delegates can Hobart realistically handle?',
     'Business Events Tasmania markets the state at up to about 1,100 delegates, and that is a fair planning number. Above roughly 1,200 in a single seated plenary there is no venue, and well before that the constraint becomes hotel rooms and flight capacity rather than the room itself.'),
    ('Do you cover group accommodation in Hobart as well as venues?', 'GROUP'),
    ('Which Hobart venue has the most rooms on one site?',
     'Wrest Point in Sandy Bay, at 271 rooms with 24 event spaces, a casino and several food outlets on the property. It is about five minutes from the city centre, so delegates tend to stay on site in the evenings rather than walk to Salamanca.'),
    ('When should we avoid holding an event in Hobart?',
     'The week after Christmas, when the Sydney to Hobart finishes and the waterfront festival runs, and the Dark Mofo fortnight in June. Both fill the city and lift rates. Everything either side of those, particularly the shoulder months, is good value.'),
    ('Can we run an event at Mona?',
     'Yes, as a standing event. Mona hires its galleries rather than function rooms, with the Nolan Gallery taking 450 standing, and it is a destination experience rather than a working conference venue. Most programs use it for one evening, arriving by catamaran from Brooke Street Pier.'),
    ('Is Hobart good for a leadership retreat?',
     'It is one of the best in the country for it. Saffire Freycinet on the east coast takes a whole property buyout for about forty, Peppers Cradle Mountain Lodge handles up to eighty five theatre with 86 cabins, and both give a group genuine separation without leaving the state.')],
  related=[
    ('venue-finder-melbourne.html', 'Melbourne',
     'The nearest mainland capital, and the alternative when the numbers outgrow Hobart.'),
    ('cbd-vs-resort-conference-venues.html', 'City or resort',
     'Whether the waterfront, the city or a property outside Hobart suits the program.'),
    ('group-accommodation.html', 'Group accommodation',
     'Where room supply is the constraint, this is the part of the job that decides the event.')],
)

# --------------------------------------------------------------------- DARWIN
DEST['Darwin'] = dict(
  file='venue-finder-darwin.html', state='NT',
  title='Conference &amp; Event Venues in Darwin | CVBS',
  meta=('Darwin conference and event venue finding. The Darwin Convention Centre, Waterfront '
        'and CBD hotels and Top End incentive programs, with a shortlist within 48 hours, free to you.'),
  h1='Conference &amp; Event Venues in Darwin',
  lead='Tell us what you need in Darwin. Shortlist within 48 hours, free to you.',
  snapshot=[
    '<b>The Darwin Convention Centre on the Waterfront is the largest conference and event '
    'facility in the Northern Territory, and the Territory government says so in those words.</b> '
    'Its four exhibition halls combine to 4,000 square metres of column free space at 3,660 theatre, '
    '2,740 banquet and 4,700 cocktail, taking up to 225 booths at 20kPa floor loading. The tiered '
    'Auditorium seats 1,236, so the plenary can run while the halls stay set.',
    '<b>Accommodation is the binding constraint, not the room.</b> The Territory’s convention '
    'bureau puts Darwin’s inventory at up to about 4,500 rooms, and the largest city properties '
    'publish 233, 197 and 140. A 3,660 delegate plenary is physically buildable in those halls; the '
    'room block behind it is not comparable to a mainland capital. Below about 500 delegates you have '
    'genuine choice across the convention centre, the resort and two or three full service hotels.',
    '<b>Two things make Darwin worth choosing rather than settling for.</b> The airport is fifteen '
    'minutes from the city and the Waterfront, and it carries direct international services to '
    'Singapore, Dili, Kuala Lumpur and Guangzhou, which no other Australian conference city of this '
    'size does. And the Territory’s Indigenous cultural programming, defence and resources content '
    'and Top End experiences give an incentive or delegate program something that cannot be '
    'reproduced anywhere else. <a href="#darwin-featured">See the venues we would start with</a>.'],
  featured=[
    ('darwin-convention-centre',
     'The only Territory venue that runs a plenary and a trade exhibition at the same time.'),
    ('doubletree-by-hilton-esplanade-darwin',
     'Residential conferences of 200 to 350 run end to end in one building.'),
    ('hilton-darwin',
     'One of the largest city room blocks, as the accommodation half of a convention centre program.'),
    ('mindil-beach-casino-resort',
     'Beachfront gala dinners and outdoor functions away from the city.'),
    ('vibe-hotel-darwin-waterfront',
     'Convention centre overflow and breakouts, inside the same precinct.'),
    ('magnt-darwin',
     'Coastal, culturally grounded dinners and receptions on the Arafura Sea.')],
  sources=['Convention centre space at the Waterfront for plenary and exhibition',
           'Waterfront and CBD hotels for delegate room blocks',
           'Beachfront and outdoor venues for gala dinners and receptions',
           'Indigenous cultural programming and Top End incentive days',
           'Asia facing meetings using Darwin’s direct international services'],
  precincts=['Darwin Waterfront', 'Darwin CBD and The Esplanade', 'Mindil Beach and The Gardens',
             'Cullen Bay', 'Litchfield and the Top End'],
  start=[
    ('Large conferences and exhibitions', 'Darwin Convention Centre, and in practice only that'),
    ('Residential conferences', 'DoubleTree by Hilton Esplanade, Hilton Darwin, Mindil Beach Casino Resort'),
    ('Premium gala dinners', 'Darwin Convention Centre above 500, Mindil Beach for a beachfront gala'),
    ('Incentives', 'Litchfield day programs, Kakadu and Arnhem Land extensions, Cullen Bay harbour activity'),
    ('Fly in, fly out meetings', 'Novotel Darwin CBD, Vibe Waterfront, convention centre meeting rooms'),
    ('Leadership retreats', 'Mindil Beach Casino Resort, or an Arnhem Land lodge for genuine remoteness')],
  local=[
    ('Darwin Waterfront', 'Where the convention centre is the anchor and delegates walk between plenary, hotel and dinner. Hotel supply inside the precinct is limited, so anything over about 200 rooms spills into the city, which is a walk away.'),
    ('Darwin CBD and The Esplanade', 'Where the room block volume sits. Hilton Darwin at 233 rooms, the DoubleTree Esplanade at 197 and Novotel at 140, with the DoubleTree able to run a 200 to 400 delegate residential conference in house.'),
    ('Mindil Beach and The Gardens', 'The gala dinner, the awards night or the beachfront reception rather than the plenary. A short drive from the city rather than a walk, and a dry season proposition given the outdoor element.'),
    ('Cullen Bay', 'Small group waterside dining and boat departures. No conference scale accommodation, so it is an offsite from a city or Waterfront base, about ten minutes by coach.'),
    ('Litchfield and the Top End', 'The incentive or partner day attached to a Darwin conference, returning to the city the same night. Strictly a dry season option, because wet season road and waterfall access is unreliable.'),
    ('Kakadu and the Arnhem Land gateway', 'When the brief calls for Indigenous cultural content with real depth rather than a photo stop. Accommodation is lodge scale and thins out above about sixty to eighty guests, so it is a pre or post extension.')],
  tradeoffs=[
    ('The season decides the date, not the other way round',
     'The Territory runs two seasons: the dry from about May to October, and the tropical summer from November to April with heat, humidity and wet season disruption. Business events concentrate in the dry, which compresses six months of demand into one booking window and lengthens lead times well beyond what the market’s size suggests.'),
    ('Almost every delegate flies in',
     'Darwin’s population is about 152,000, so the local delegate catchment is small and airfares carry a larger share of the total event budget than in a mainland capital. Single carrier route dependency on some routes is a real risk worth checking against your dates.'),
    ('The exhibition halls are not a uniform height',
     'Hall 1 is 12 metres clear and Halls 2 to 4 are 9.3 metres. If you are rigging a set that spans all four halls, it works to the lower figure. It is the kind of detail that costs money late if nobody raises it early.')],
  why_h2='Darwin is a dry season destination with an Asian front door.',
  why_lead='Fifteen minutes from a terminal that flies direct to Singapore, Dili, Kuala Lumpur and Guangzhou, with a convention centre that runs a plenary and a trade floor at once. The season is the first conversation, because six months of the calendar carry almost all of the demand.',
  faqs=[
    ('How much does it cost to use CVBS to find a venue in Darwin?', 'FREE'),
    ('How quickly can you find Darwin venues?', 'FAST'),
    ('What is the largest conference venue in Darwin?',
     'The Darwin Convention Centre at the Waterfront, which the Northern Territory government describes as the largest conference and event facility in the Territory. Its four exhibition halls combine to 4,000 square metres of column free space seating 3,660 theatre, with a tiered auditorium seating 1,236 alongside.'),
    ('When is the best time of year to hold an event in Darwin?',
     'The dry season, roughly May to October, when the Territory publishes daytime temperatures of 22 to 32 degrees. The tropical summer from November to April brings heat, humidity and wet season disruption, which makes outdoor and touring elements unreliable. Because everyone wants the same six months, lead times are longer than the market size suggests.'),
    ('Do you cover group accommodation in Darwin as well as venues?', 'GROUP'),
    ('Which Darwin hotel is best for a residential conference?',
     'DoubleTree by Hilton Hotel Esplanade Darwin, which has 197 rooms and 908 square metres of event space in the same building. Its ballroom splits in two with four further breakout rooms, so a 200 to 350 delegate conference runs end to end without delegates leaving the property.'),
    ('Is Darwin a good incentive destination?',
     'It is a genuinely strong one, in the dry season. Litchfield National Park day programs, Kakadu and Arnhem Land cultural extensions, Cullen Bay harbour activity and Uluru or Alice Springs as a Central Australia extension all work from a Darwin base. The same program in February is a different and much less reliable proposition.'),
    ('Can Darwin host an international conference?',
     'For an Asia facing program, unusually well for a city of this size. Darwin Airport carries scheduled international services to Singapore, Dili, Kuala Lumpur and Guangzhou, and the convention centre is fifteen minutes from the terminal. The limit is the room block rather than the venue.')],
  related=[
    ('venue-finder-cairns.html', 'Cairns',
     'The other tropical conference city, with the reef and rainforest instead of the Top End.'),
    ('conference-venues-with-accommodation.html', 'Venues with accommodation',
     'The venues that hold the plenary and the delegates in the same building.'),
    ('cbd-vs-resort-conference-venues.html', 'City or resort',
     'Darwin is a small city with resort stock attached, so the choice matters more here.')],
)

# ----------------------------------------------------------------- GOLD COAST
DEST['Gold Coast'] = dict(
  file='venue-finder-gold-coast.html', state='QLD',
  title='Conference &amp; Event Venues on the Gold Coast | CVBS',
  meta=('Gold Coast conference and event venue finding. GCCEC, Broadbeach, Surfers Paradise, '
        'Main Beach and Sanctuary Cove, with published capacities and a shortlist within 48 hours, '
        'free to you.'),
  h1='Conference &amp; Event Venues on the Gold Coast',
  lead='Tell us what you need on the Gold Coast. Shortlist within 48 hours, free to you.',
  snapshot=[
    '<b>Broadbeach is the practical centre of the Gold Coast conference market.</b> The Gold '
    'Coast Convention and Exhibition Centre, The Star Gold Coast and a run of hotels sit close '
    'enough together that a large program can operate all day without moving delegates around the '
    'city. GCCEC’s Full Arena is tiered and seats 6,020 theatre in 2,182 square metres under a '
    '14 metre ceiling, and it is the only room on the coast that seats more than 2,500.',
    '<b>Read the arena figure and the exhibition figure as two different things.</b> The four '
    'exhibition halls are a separate 6,345 square metre flat floor block with ten metre ceilings '
    'taking 330 booths, and they publish no theatre capacity at all. A plenary decision and an '
    'exhibition decision are made in different rooms here, which is easy to miss on a capacity chart.',
    '<b>Where the Gold Coast is strongest is the residential conference.</b> RACV Royal Pines '
    'inland, the Sheraton Grand Mirage and Sea World Resort on The Spit, InterContinental Sanctuary '
    'Cove in a gated estate and the JW Marriott in Surfers Paradise all hold the plenary, the dinner '
    'and the beds on one campus. The honest problem is perception rather than product: a board can '
    'read "Gold Coast" as a holiday choice before it reads the venue, and the way planners handle '
    'that is to anchor in Broadbeach rather than Surfers Paradise and keep the leisure element as an '
    'opt in evening. <a href="#gold-coast-featured">See the venues we would start with</a>.'],
  featured=[
    ('gold-coast-convention-and-exhibition-centre',
     'Anything above 2,500 seated, and exhibitions on a separate 6,345 square metre floor.'),
    ('the-star-gold-coast',
     'A thousand to two thousand delegates living entirely inside one complex.'),
    ('racv-royal-pines-resort',
     'Large residential conferences that want one campus and are not trying to be on the beach.'),
    ('sheraton-grand-mirage-resort-gold-coast',
     'Beachfront residential conferences with lawns that carry a 400 seat dinner.'),
    ('intercontinental-sanctuary-cove-resort',
     'Leadership programs in a gated estate where nobody drifts off into a holiday strip.'),
    ('hota-home-of-the-arts',
     'A plenary that does not look like a conference, and launches needing a stage and a gallery.')],
  sources=['Convention centre space at Broadbeach for plenary and exhibition',
           'Beachfront and inland conference resorts for residential programs',
           'Integrated resort space for galas, awards and self contained conferences',
           'Theme park and arts venues for incentive nights and brand activations',
           'Delegate room blocks across Broadbeach, Surfers Paradise and Main Beach'],
  precincts=['Broadbeach', 'Surfers Paradise', 'Main Beach and The Spit', 'Sanctuary Cove',
             'Benowa and Carrara', 'Bundall', 'Coomera and Oxenford'],
  start=[
    ('Large conferences and exhibitions', 'Gold Coast Convention and Exhibition Centre'),
    ('Residential conferences', 'RACV Royal Pines, Sheraton Grand Mirage, JW Marriott, InterContinental Sanctuary Cove'),
    ('Premium gala dinners', 'GCCEC exhibition halls, The Star Pavilion, Sheraton Mirage ballroom and lawns'),
    ('Leadership retreats', 'InterContinental Sanctuary Cove, The Langham, RACV Royal Pines'),
    ('Incentives', 'The Spit resorts, Sanctuary Cove, and a theme park evening at Oxenford'),
    ('Product launches and brand events', 'HOTA, The Star Gold Coast, Warner Bros. Movie World')],
  local=[
    ('Broadbeach', 'The only genuinely walkable conference precinct, and unusually tight. The convention centre sits 500 metres from the surf and is joined to The Star by a pedestrian bridge, with Sofitel and Dorsett within a short covered walk.'),
    ('Surfers Paradise', 'Delegate volume and the widest rate spread in one strip, from JW Marriott and The Langham down to serviced apartments. On the light rail, so delegates can self transfer to Broadbeach.'),
    ('Main Beach and The Spit', 'When the program should feel like a resort rather than a city. Sheraton Grand Mirage and Sea World Resort put the accommodation inside the venue, with a short road transfer for anything offsite.'),
    ('Sanctuary Cove and Hope Island', 'A closed campus with no leakage. One property, 251 rooms, inside a gated marina and golf estate about half an hour north. That is a feature for retention and a cost for anything offsite.'),
    ('Benowa and Carrara', 'A large residential conference that needs a 1,500 square metre ballroom and 333 rooms under one roof at a lower rate than the beachfront. No light rail, so evenings in Broadbeach mean coaches.'),
    ('Bundall and Coomera', 'The offsite. HOTA for a plenary or a launch that should not look corporate, and the theme parks at Oxenford for an incentive night, roughly half an hour by coach from the beachfront.')],
  tradeoffs=[
    ('Schoolies takes late November out of Surfers Paradise',
     'Schoolies runs for a week in late November and is centred on Surfers Paradise. It is the single most disruptive fixture of the year for that precinct’s accommodation and street amenity, and it is worth planning around rather than discovering.'),
    ('Mid January is the hardest window of the year',
     'The Magic Millions sale at Bundall lands in the middle of January on top of peak summer holiday demand, which makes corporate rates hardest to buy across the whole coast. Early July carries the Gold Coast Marathon, which compresses accommodation for that weekend.'),
    ('Air access is longer than the compactness suggests',
     'The main airport is at Coolangatta, about half an hour from Broadbeach, and Brisbane Airport is roughly ninety minutes away. For a genuine same day fly in and out meeting we would put Brisbane in front of you instead, and say so.')],
  why_h2='On the Gold Coast the precinct decides how a board reads the program.',
  why_lead='Broadbeach reads as a conference destination and Surfers Paradise reads as a holiday, even when the rooms are similar. Choosing the precinct first, and keeping the leisure element as an opt in evening rather than the headline, is what makes a serious corporate program work here.',
  faqs=[
    ('How much does it cost to use CVBS to find a venue on the Gold Coast?', 'FREE'),
    ('How quickly can you find Gold Coast venues?', 'FAST'),
    ('What is the largest conference venue on the Gold Coast?',
     'The Gold Coast Convention and Exhibition Centre at Broadbeach. Its Full Arena is tiered and seats 6,020 theatre in 2,182 square metres under a 14 metre ceiling, and it is the only room on the coast that seats more than 2,500. The four exhibition halls are a separate 6,345 square metre flat floor block taking 330 booths.'),
    ('Where should a 500 delegate residential conference be held on the Gold Coast?',
     'On one campus, which is what the coast does best. RACV Royal Pines at Benowa has 333 rooms behind a 1,500 square metre ballroom, the Sheraton Grand Mirage has 295 rooms on the beachfront at Main Beach, and the JW Marriott has 238 rooms in Surfers Paradise with a three tonne hoist over the ballroom.'),
    ('Do you cover group accommodation on the Gold Coast as well as venues?', 'GROUP'),
    ('Which airport should Gold Coast delegates fly into?',
     'Gold Coast Airport at Coolangatta is roughly half an hour from Broadbeach and is the obvious choice where the routes work. Brisbane Airport is about ninety minutes by road and carries far more capacity, so a national program often splits between the two. The light rail does not reach either airport, so arrivals are always a road transfer.'),
    ('Will a Gold Coast conference look like a holiday to our board?',
     'It can, and it is a fair thing to manage rather than dismiss. The way planners handle it is to anchor the program in Broadbeach rather than Surfers Paradise, run the plenary in the convention centre rather than a resort ballroom, and keep the leisure element as an opt in evening. We will tell you honestly if we think a destination will be read the wrong way.'),
    ('When should we avoid the Gold Coast?',
     'The Schoolies week in late November for anything in Surfers Paradise, mid January when the Magic Millions sale coincides with peak holiday demand, and the Gold Coast Marathon weekend in early July. Outside those, availability is generally good and the shoulder seasons are excellent value.')],
  related=[
    ('venue-finder-brisbane.html', 'Brisbane',
     'An hour north, and the better answer when the program needs a city and one airport.'),
    ('venue-finder-sunshine-coast.html', 'Sunshine Coast',
     'The quieter coast, with a hinterland and lower density.'),
    ('cbd-vs-resort-conference-venues.html', 'City or resort',
     'Broadbeach, Surfers or a hinterland property, and what each one costs you in transfer time.')],
)

# ------------------------------------------------------------- SUNSHINE COAST
DEST['Sunshine Coast'] = dict(
  file='venue-finder-sunshine-coast.html', state='QLD',
  title='Conference &amp; Event Venues on the Sunshine Coast | CVBS',
  meta=('Sunshine Coast conference and event venue finding. Twin Waters, Noosa, Mooloolaba, '
        'Caloundra and the hinterland, with published capacities and a shortlist within 48 hours, '
        'free to you.'),
  h1='Conference &amp; Event Venues on the Sunshine Coast',
  lead='Tell us what you need on the Sunshine Coast. Shortlist within 48 hours, free to you.',
  snapshot=[
    '<b>The Sunshine Coast Convention Centre at Twin Waters is the only property in the region '
    'that seats a four figure plenary and sleeps most of the delegates on the same site.</b> Its '
    'Minyama Ballroom takes 1,000 theatre, 920 banquet and 1,500 cocktail across 1,600 square '
    'metres, with the Wandiny Room alongside at 980, and 373 rooms in the resort around it. The '
    'centre states a working maximum of 1,400 delegates.',
    '<b>Choice narrows sharply above about 350 delegates.</b> Outside Twin Waters the largest '
    'published single rooms are The Events Centre at Caloundra at 820 on a flat floor, Peppers '
    'Noosa at 350 and Elysium Noosa at 300, and the next largest room blocks are 188, 176, 170 and '
    '160 rooms. A 600 delegate residential program is a single property decision here, not a '
    'shortlist.',
    '<b>This is a dispersed coastal region, not a walkable precinct, and that shapes every '
    'program.</b> Noosa, Mooloolaba, Twin Waters and Caloundra each hold their own accommodation, '
    'with the hinterland inland again, so an event spread across two of those centres needs coaches '
    'built into the budget from the start. Sunshine Coast Airport is at Marcoola, eight kilometres '
    'from Twin Waters, with Brisbane Airport about ninety minutes away as the fallback. '
    '<a href="#sunshine-coast-featured">See the venues we would start with</a>.'],
  featured=[
    ('sunshine-coast-convention-centre',
     'The only regional option above 400 seated that also has the accommodation on the same site.'),
    ('the-events-centre-caloundra',
     'Flat floor plenaries and gala dinners with theatre infrastructure already in place.'),
    ('peppers-noosa-resort-villas',
     'Mid size residential conferences and premium programs above Noosa.'),
    ('elysium-noosa',
     'The largest conference capable property on Hastings Street, recently rebranded.'),
    ('spicers-clovelly-estate',
     'Board offsites and executive retreats on exclusive use in the hinterland.'),
    ('australia-zoo',
     'Incentive dinners and team activity inside the zoo after public hours.')],
  sources=['Beachfront and resort conference properties for residential programs',
           'A purpose built convention centre at Twin Waters',
           'Council venues at Caloundra and Kawana for day conferences and expos',
           'Hinterland estates at Montville and Maleny for executive retreats',
           'Delegate room blocks across Noosa, Mooloolaba, Twin Waters and Caloundra'],
  precincts=['Twin Waters and Marcoola', 'Mooloolaba', 'Noosa Heads', 'Caloundra',
             'Kawana and Bokarina', 'Maroochydore and Sippy Downs', 'Montville and Maleny'],
  start=[
    ('Large conferences', 'Sunshine Coast Convention Centre at Twin Waters'),
    ('Residential conferences', 'Novotel Sunshine Coast Resort, Peppers Noosa, Elysium Noosa, Mantra Mooloolaba'),
    ('Premium gala dinners', 'Minyama Ballroom, Peppers Noosa Macquarie, The Events Centre Caloundra'),
    ('Leadership retreats', 'Spicers Clovelly Estate at Montville, and the Maleny properties'),
    ('Incentives', 'Australia Zoo, Noosa programs, and the hinterland'),
    ('Academic and medical conferences', 'University of the Sunshine Coast at Sippy Downs')],
  local=[
    ('Twin Waters and Marcoola', 'When the delegate count decides it. The only precinct with a four figure plenary and 373 rooms on one site, plus AFL and NRL fields for outdoor activation, eight kilometres from the airport.'),
    ('Mooloolaba', 'Mid size residential conferences that want an evening the organiser does not have to program. Beachfront hotels sit opposite the Esplanade strip, so delegates walk out to dinner.'),
    ('Noosa Heads', 'Premium and incentive programs where the destination is part of the sell. The deepest concentration of upper tier rooms, but ballrooms cap around 300 to 350, and it is the furthest point from the airport.'),
    ('Caloundra', 'A large flat floor plenary or theatre infrastructure without resort rates. The Events Centre carries 820 on a flat floor but has no rooms of its own, so accommodation is a separate block.'),
    ('Kawana and Bokarina', 'Exhibitions, expos and community scale events, with Venue 114 and the stadium side by side and accommodation drawn from Mooloolaba.'),
    ('Montville and Maleny', 'Leadership retreats and board offsites of fifteen to forty on exclusive use properties. Closest part of the region to Brisbane Airport, but winding range roads back to the coast.')],
  tradeoffs=[
    ('This is a region, not a precinct',
     'Noosa to Caloundra is a real drive, and Twin Waters sits between them. Any program that uses two centres needs coach transfers written into the budget on day one, and a delegate arriving at Noosa from Brisbane Airport is on a road transfer of well over an hour.'),
    ('There is no exhibition hall',
     'No venue in the region publishes an exhibition floor area or a booth count. If your program needs a serious trade floor alongside the plenary, it belongs in Brisbane or on the Gold Coast, and we would say so rather than make it fit.'),
    ('Above about 400 seated and residential, it is one property',
     'The Sunshine Coast Convention Centre at Twin Waters is the only site we publish that seats more than 400 and sleeps them on the same grounds. The Events Centre at Caloundra takes 820 on a flat floor and the University of the Sunshine Coast 500, but both need a room block negotiated separately across nearby hotels. So a large residential program here has a single answer, which means a long lead time and a second destination held in reserve.')],
  why_h2='The Sunshine Coast is a residential conference destination, and it rewards a single site.',
  why_lead='Almost everything that goes wrong here is a transfer nobody costed. We start with which centre the program belongs in, because Noosa, Mooloolaba, Twin Waters and Caloundra are separate towns with separate accommodation, and choosing one of them well is worth more than shortlisting across all four.',
  faqs=[
    ('How much does it cost to use CVBS to find a venue on the Sunshine Coast?', 'FREE'),
    ('How quickly can you find Sunshine Coast venues?', 'FAST'),
    ('What is the largest conference venue on the Sunshine Coast?',
     'The Sunshine Coast Convention Centre at Twin Waters, integrated into the Novotel resort. Its Minyama Ballroom takes 1,000 theatre and 1,500 cocktail across 1,600 square metres, and the centre states a working maximum of 1,400 delegates across the site.'),
    ('How many delegates can the Sunshine Coast handle?',
     'Comfortably up to about 350 across several properties, and up to about 1,000 seated in one room at Twin Waters only. The region’s convention bureau describes its sweet spot as 50 to 200 delegates, which matches what we see.'),
    ('Do you cover group accommodation on the Sunshine Coast as well as venues?', 'GROUP'),
    ('Which airport should Sunshine Coast delegates fly into?',
     'Sunshine Coast Airport at Marcoola where the routes work: it is eight kilometres from Twin Waters and around 32 to 35 kilometres from Noosa, and its 2020 runway upgrade to 2,450 metres allows wide body aircraft. Brisbane Airport is about ninety minutes by road and carries far more capacity, so national programs often use both.'),
    ('Is the Sunshine Coast better than the Gold Coast for a conference?',
     'For a large conference with an exhibition, no: the Gold Coast has the convention centre and the floor area and the Sunshine Coast has neither. For a residential conference of 100 to 350, or an executive retreat, the Sunshine Coast usually wins on lower density, a genuine hinterland and a quieter delegate experience.'),
    ('Can we hold a leadership retreat in the hinterland?',
     'Yes, and it is one of the region’s strongest cards. Spicers Clovelly Estate at Montville takes a group of about fifteen to forty on exclusive use with the restaurant as the reason most groups choose it, and the Maleny properties work the same way. Both are range road drives from the coast, so build the transfer in.')],
  related=[
    ('venue-finder-brisbane.html', 'Brisbane',
     'Ninety minutes south, and where a program with a trade floor belongs.'),
    ('venue-finder-gold-coast.html', 'Gold Coast',
     'The other Queensland coast, with a convention centre and far more room supply.'),
    ('cbd-vs-resort-conference-venues.html', 'City or resort',
     'What a program gives up moving out of Brisbane, and what it gets back.')],
)

# --------------------------------------------------------------------- CAIRNS
DEST['Cairns'] = dict(
  file='venue-finder-cairns.html', state='QLD',
  title='Conference &amp; Event Venues in Cairns | CVBS',
  meta=('Cairns and Tropical North Queensland conference and event venue finding. The Cairns '
        'Convention Centre, Esplanade hotels, Palm Cove and Port Douglas, with a shortlist within '
        '48 hours, free to you.'),
  h1='Conference, Incentive &amp; Event Venues in Cairns',
  lead='Tell us what you need in Cairns. Shortlist within 48 hours, free to you.',
  snapshot=[
    '<b>The Cairns Convention Centre is the largest single event space in Tropical North '
    'Queensland, and it is the reason the city holds conferences well above its size.</b> The Arena '
    'is 1,470 square metres under a 17 metre roof, seating 5,000 theatre with the tiered seating '
    'deployed and 1,584 on the flat floor in exhibition mode with 98 booths. The Auditorium '
    'alongside seats 2,360 tiered, so the building carries two large plenaries rather than one.',
    '<b>Hotel ballrooms top out around 650, which is where the market actually sits.</b> The '
    'largest is Pullman Cairns International’s Grand Ballroom at 650 theatre in 500 square metres, '
    'with 324 rooms above it. Below about 600 delegates you have a genuine competitive set of hotels; '
    'between about 1,000 and 2,500 the convention centre is effectively the only room, so there is no '
    'competitive tension in that band and lead times are long.',
    '<b>Accommodation is concentrated in the walkable Esplanade and wharf strip, and the reef and '
    'rainforest are the reason to be here.</b> Eight city hotels publish about 2,160 rooms between '
    'them, and past roughly 1,200 to 1,500 delegates you are splitting a group across most of that '
    'inventory. Cairns Airport carries direct services to Singapore, Hong Kong, Tokyo, Osaka, Bali, '
    'Christchurch, Nadi and Port Moresby, which is unusual for a regional airport and is the real '
    'argument for Cairns over a southern capital for an Asian or Pacific audience. '
    '<a href="#cairns-featured">See the venues we would start with</a>.'],
  featured=[
    ('cairns-convention-centre',
     'Anything above about 650 delegates, with two tiered plenaries in one building.'),
    ('pullman-cairns-international',
     'The largest hotel ballroom in the city and the usual conference headquarters hotel.'),
    ('pullman-reef-hotel-casino',
     'Gala dinners that move from ballroom to bars without leaving the building.'),
    ('shangri-la-the-marina-cairns',
     'Conferences with many concurrent breakouts, and reef departures on foot.'),
    ('sheraton-grand-mirage-port-douglas',
     'Premium residential programs and incentives an hour north, with an 800 square metre pavilion.'),
    ('cairns-performing-arts-centre',
     'Awards nights and plenaries that need real staging and sightlines.')],
  sources=['Convention centre space for plenary and exhibition in the city',
           'Esplanade and marina hotels for delegate room blocks',
           'Palm Cove and Port Douglas resorts for incentives and retreats',
           'Reef and rainforest programs as genuine delegate experience',
           'Asia facing meetings using Cairns Airport’s direct international network'],
  precincts=['Cairns CBD and Esplanade', 'Cairns Wharf and Marlin Marina', 'Northern beaches',
             'Palm Cove', 'Port Douglas', 'Kuranda and the Barron Gorge', 'Daintree and Cape Tribulation'],
  start=[
    ('Large conferences and exhibitions', 'Cairns Convention Centre, and in practice only that above 650'),
    ('Residential conferences', 'Pullman Cairns International, Hilton Cairns, Novotel Cairns Oasis Resort'),
    ('Premium gala dinners', 'Pullman Reef Hotel Casino, the Convention Centre Auditorium, Cairns Performing Arts Centre'),
    ('Incentives', 'Sheraton Grand Mirage Port Douglas, reef island programs, Daintree and Kuranda days'),
    ('Leadership retreats', 'Pullman Port Douglas Sea Temple on a buyout, Palm Cove properties'),
    ('Fly in, fly out meetings', 'Any Esplanade hotel, ten minutes from the terminal')],
  local=[
    ('Cairns CBD and Esplanade', 'Where the convention centre is in the program and delegates walk everywhere. Flat, walkable, and the overwhelming majority of conference grade rooms sit here.'),
    ('Cairns Wharf and Marlin Marina', 'Reef access and the casino evening. Shangri-La and Pullman Reef Hotel Casino sit here and the reef departure pontoons are on foot, with no transfer needed.'),
    ('Northern beaches', 'Accommodation relief when a city conference outgrows the CBD, or a lower cost residential block. Meeting space is limited, so the plenary stays in town and delegates coach in.'),
    ('Palm Cove', 'An incentive or leadership retreat where the village is the experience. Very shallow conference grade room stock, so groups above about 150 to 200 start splitting properties.'),
    ('Port Douglas', 'A premium residential retreat or incentive with the reef and rainforest either side. Sheraton Grand Mirage is the only property with real scale, and it is a genuine drive north rather than a short hop.'),
    ('Daintree and Kuranda', 'The delegate experience rather than the base. Kuranda works as a half day by road, cableway or the heritage railway, and the Daintree is a day trip or a very small group base staged out of Port Douglas.')],
  tradeoffs=[
    ('Half the year carries weather risk',
     'The Australian cyclone season officially runs 1 November to 30 April, overlapping the wet summer months, and marine stinger season typically runs November through May, which makes open water swimming a supervised, stinger suit activity rather than a casual one. The dry, mild peak from June to August is also when rates and availability are tightest.'),
    ('It is a single venue market at scale',
     'Between about 650 and 2,500 delegates the convention centre is the only building that works, so there is no competitive tension in that band. Combine that with a narrow weather window and the bookable slot for a large Cairns conference is genuinely tight.'),
    ('Reef and rainforest programs depend on the weather',
     'A ballroom program is weatherproof and a reef day is not. Where the offsite content is the reason the client chose Cairns, we build a contingency into the shortlist rather than into the apology.')],
  why_h2='In Cairns the offsite is the reason, and the logistics are the job.',
  why_lead='Two World Heritage areas within reach of one airport is a genuine delegate experience rather than a brochure line, and it is why an Asian or Pacific audience is easier to attract here than to a southern capital. What we do is make sure the weather window, the room block and the reef program actually line up.',
  faqs=[
    ('How much does it cost to use CVBS to find a venue in Cairns?', 'FREE'),
    ('How quickly can you find Cairns venues?', 'FAST'),
    ('What is the largest conference venue in Cairns?',
     'The Cairns Convention Centre. Its Arena is 1,470 square metres under a 17 metre roof and seats 5,000 theatre with the tiered retractable seating deployed, dropping to 1,584 theatre on the flat floor in exhibition mode with 98 booths. The Auditorium alongside seats 2,360 tiered.'),
    ('Which Cairns hotel has the largest ballroom?',
     'Pullman Cairns International, whose Grand Ballroom seats 650 theatre in 500 square metres with 324 rooms above it. It is the closest hotel to the convention centre, which makes it the usual headquarters property for centre based conferences.'),
    ('Do you cover group accommodation in Cairns as well as venues?', 'GROUP'),
    ('When is the best time of year for a Cairns conference?',
     'June to August is the dry, mild peak, with Cairns averaging about 17.5 to 26.2 degrees, and it is also when rates and availability are tightest. The cyclone season officially runs 1 November to 30 April, and marine stinger season runs roughly November to May, both of which matter if your program has outdoor or reef content.'),
    ('Is Cairns good for an international conference?',
     'For an Asian or Pacific audience it is unusually good for a city of this size. Cairns Airport carries direct services to Singapore, Hong Kong, Tokyo, Osaka, Bali, Christchurch, Nadi and Port Moresby, and the convention bureau puts delegates at their accommodation within about ten minutes of leaving the airport.'),
    ('Should we hold the conference in Cairns or Port Douglas?',
     'Cairns for the conference, Port Douglas for the reward. Cairns has the convention centre, the hotel depth and the airport; Port Douglas has one property with real scale at 295 rooms and eighteen spaces, and it is a genuine drive north. A common structure is a Cairns conference with a Port Douglas or Palm Cove extension for the senior group.')],
  related=[
    ('venue-finder-darwin.html', 'Darwin',
     'The other tropical conference city, with an Asian front door of its own.'),
    ('venue-finder-brisbane.html', 'Brisbane',
     'Where a large trade exhibition belongs when Cairns cannot hold it.'),
    ('events.html', 'Product launches and events',
     'How we source an event space when the experience is the point.')],
)

# -------------------------------------------------------------- HUNTER VALLEY
DEST['Hunter Valley'] = dict(
  file='venue-finder-hunter-valley.html', state='NSW',
  title='Conference, Retreat &amp; Offsite Venues in the Hunter Valley | CVBS',
  meta=('Hunter Valley conference, retreat and winery event venue finding. Pokolbin, Lovedale '
        'and Rothbury resorts with published capacities and a shortlist within 48 hours, free to you.'),
  h1='Conference, Retreat &amp; Offsite Venues in the Hunter Valley',
  lead='Tell us what you need in the Hunter Valley. Shortlist within 48 hours, free to you.',
  snapshot=[
    '<b>The Hunter Valley is a residential conference and offsite region, and one property '
    'carries the top of it.</b> Rydges Resort Hunter Valley at Lovedale publishes a 1,123 square '
    'metre conference centre at 1,160 theatre and 850 banquet with 417 rooms behind it, which is the '
    'only pairing in the region of a four figure plenary and the beds to fill it. Oaks Cypress Lakes '
    'at Pokolbin is next, though its largest space is a marquee and its biggest permanent indoor room '
    'is the Venusta Centre at 450 theatre.',
    '<b>Room count, not meeting space, decides what is possible here.</b> Above about 350 to 450 '
    'delegates in plenary the field narrows to two properties, and above 417 rooms there is no single '
    'site answer at all. That is the number to plan a residential program against, whatever a '
    'capacity chart says about a marquee.',
    '<b>Nothing here is walkable, and that is the single most common budget surprise.</b> Lovedale, '
    'Pokolbin and Rothbury are separate estates on rural roads, so every cellar door visit and offsite '
    'dinner is a coached movement. Sydney is a little over two hours by road on Destination NSW’s own '
    'figure. What you get in exchange is a group that cannot drift home at six o’clock, which is the '
    'whole argument for bringing a leadership program out of the city. '
    '<a href="#hunter-valley-featured">See the venues we would start with</a>.'],
  featured=[
    ('rydges-resort-hunter-valley',
     'The only regional pairing of a four figure plenary with 417 rooms on one site.'),
    ('oaks-cypress-lakes-resort',
     'Residential conferences wanting 24 bookable spaces and outdoor dinners across a golf estate.'),
    ('chateau-elan-at-the-vintage',
     'A residential conference up to 330 that should still feel like a retreat.'),
    ('hope-estate',
     'Offsite galas and concert scale events at a working winery.'),
    ('bimbadgen',
     'Multi site winery hosting with a small retreat and a boardroom attached.'),
    ('spicers-vineyards-estate',
     'Executive teams and board level groups on exclusive use.')],
  sources=['Residential conference resorts with the plenary and the rooms on one site',
           'Winery estates for gala dinners, long table lunches and launches',
           'Small exclusive use properties for board and leadership offsites',
           'Golf and spa programs attached to a multi day conference',
           'Coach logistics between estates, priced before you commit'],
  precincts=['Pokolbin', 'Lovedale', 'Rothbury', 'Broke and Fordwich', 'Cessnock', 'Newcastle'],
  start=[
    ('Residential conferences', 'Rydges Resort Hunter Valley, Oaks Cypress Lakes, Chateau Elan'),
    ('Leadership retreats and board offsites', 'Spicers Vineyards Estate, Chateau Elan, Bimbadgen'),
    ('Premium winery dinners', 'Hope Estate, the Rydges conference centre, the Oaks marquee'),
    ('Incentives', 'Oaks Cypress Lakes, Chateau Elan, Bimbadgen'),
    ('Product launches and brand events', 'Hope Estate and the winery lawns'),
    ('Large exhibitions', 'Not here. <a href="venue-finder-sydney.html">Sydney</a> or Newcastle')],
  local=[
    ('Lovedale', 'When the whole program has to sit on one site. Rydges Resort holds the only verified pairing of a plenary above a thousand and 417 rooms, so coaching is only needed for offsite winery activity.'),
    ('Pokolbin', 'The densest cluster of cellar doors and event estates, and where most dinners end up. Accommodation is spread across resorts, villas and small retreats rather than concentrated, and everything moves by coach.'),
    ('Rothbury', 'The Vintage estate and Chateau Elan. A residential leadership program up to about 330 in plenary that wants golf, a day spa and villa accommodation on one site.'),
    ('Broke and Fordwich', 'A quieter sub region for small exclusive use retreats and scenic dinners. Little conference scale accommodation, and it adds transfer time to a program based at Lovedale or Rothbury.'),
    ('Cessnock', 'The service town rather than a venue precinct. Relevant for coach staging, budget room stock and supplier access.'),
    ('Newcastle', 'Outside the wine country but inside the same catchment, with the airport and the closest urban hotel stock. The fallback when a program needs same day air access.')],
  tradeoffs=[
    ('The summer concert season absorbs the room stock',
     'The major estates run outdoor concerts through summer, and a sold out show at Bimbadgen or Hope Estate will take regional accommodation out of the market for that weekend. It is the first calendar we check against your dates.'),
    ('There is no exhibition floor and no airport',
     'The largest verified room is 1,123 square metres at 4.5 metres, and the exhibition space alongside it is lower again. A program with a trade floor, twenty concurrent breakouts and 800 delegates belongs in Sydney or Newcastle, and a genuine fly in fly out meeting does not belong here at all: this is a two night destination.'),
    ('Coaching is not optional',
     'The regional tourism authority itself says travel is best by vehicle or organised tour. Every off site dinner is a coached movement, and a program that assumes people will wander between cellar doors will run late on the first night.')],
  why_h2='In the Hunter Valley the transfers are the program, so we price them first.',
  why_lead='The estates are separated by rural road, so where you base the group decides how much of each day is spent on a coach. We start with the base and the movements, because that is what actually determines whether a two day agenda is deliverable.',
  faqs=[
    ('How much does it cost to use CVBS to find a venue in the Hunter Valley?', 'FREE'),
    ('How quickly can you find Hunter Valley venues?', 'FAST'),
    ('What is the largest conference venue in the Hunter Valley?',
     'Of the venues we checked, the Hunter Valley Conference and Events Centre at Rydges Resort Hunter Valley in Lovedale. It publishes 1,123 square metres at 1,160 theatre, 850 banquet and 1,750 cocktail, with a 4.5 metre ceiling and 417 guest rooms on the same site.'),
    ('How many delegates can stay on one Hunter Valley property?',
     'Up to 417 rooms at Rydges Resort Hunter Valley, which is the largest published inventory in the region. Chateau Elan and Oaks Cypress Lakes do not publish a total room count, so any block at those properties has to be confirmed directly. Above roughly 400 rooms, a Hunter Valley program becomes a multi property exercise.'),
    ('Do you cover group accommodation in the Hunter Valley as well as venues?', 'GROUP'),
    ('How far is the Hunter Valley from Sydney?',
     'Destination NSW puts it at just over two hours by road. Newcastle Airport serves the catchment but publishes no drive time to Pokolbin or Cessnock, so for an interstate group we cost the transfer explicitly rather than estimating it.'),
    ('Can we run a conference and a winery dinner on the same day?',
     'Yes, and most programs do. The thing to be clear about is that the estates are separate properties on rural roads, so the dinner is a coached movement with a return leg. We build that into the run sheet at shortlist rather than leaving it to the day.'),
    ('Is the Hunter Valley suitable for a large exhibition?',
     'No, and we would tell you so rather than make it fit. The largest verified single room is 1,123 square metres with a 4.5 metre ceiling, and the exhibition space alongside it is lower again. A program with a genuine trade floor belongs in <a href="venue-finder-sydney.html">Sydney</a> or Newcastle.')],
  related=[
    ('venue-finder-sydney.html', 'Sydney',
     'Two hours south, and where a program with a trade floor or air access belongs.'),
    ('venue-finder-blue-mountains.html', 'Blue Mountains',
     'The other Sydney offsite region, higher, cooler and more compact.'),
    ('cbd-vs-resort-conference-venues.html', 'City or resort',
     'The case for a wine country residential over a Sydney hotel, and where it falls down.')],
)

# ------------------------------------------------------------- BLUE MOUNTAINS
DEST['Blue Mountains'] = dict(
  file='venue-finder-blue-mountains.html', state='NSW',
  title='Conference, Retreat &amp; Offsite Venues in the Blue Mountains | CVBS',
  meta=('Blue Mountains conference, retreat and offsite venue finding. Leura, Katoomba and '
        'Medlow Bath properties with published capacities and a shortlist within 48 hours, free to you.'),
  h1='Conference, Retreat &amp; Offsite Venues in the Blue Mountains',
  lead='Tell us what you need in the Blue Mountains. Shortlist within 48 hours, free to you.',
  snapshot=[
    '<b>The largest conference room published by any Blue Mountains hotel or resort is the Grand '
    'Ballroom at Fairmont Resort Blue Mountains in Leura, at 620 theatre.</b> That room is the '
    'Ballroom and Pioneers opened together, so the largest single undivided space is the Ballroom at '
    '364. The Fairmont is also the only property in the region with both a plenary of that size and '
    'the rooms to sleep the group, at 224 rooms and 23 meeting spaces.',
    '<b>Below the Fairmont the market drops sharply and becomes a retreat market.</b> The next '
    'largest published theatre figures are the Hydro Majestic at Medlow Bath at 250 and Mountain '
    'Heritage at Katoomba at 200, and published room counts run 82, 65 and 41. Above about 250 in '
    'plenary you are choosing between one or two properties, and above 620 there is nothing.',
    '<b>What the Blue Mountains does that Sydney cannot is keep the group together.</b> Delegates '
    'do not go home at six o’clock, there is nothing else on, and the evening session actually '
    'happens. The properties publish about ninety minutes from Sydney by road, the rail line runs '
    'direct from Central, and it is genuinely usable for individual arrivals even though every '
    'property sits on an escarpment above its town. <a href="#blue-mountains-featured">See the venues '
    'we would start with</a>.'],
  featured=[
    ('fairmont-resort-blue-mountains',
     'The only property that seats 600 and sleeps the group, at 224 rooms and 23 spaces.'),
    ('hydro-majestic-hotel',
     'A 60 to 200 person residential program in one distinctive clifftop building.'),
    ('mountain-heritage-hotel',
     'A 200 seat day conference above Katoomba with beds sourced alongside.'),
    ('ardour-lilianfels-blue-mountains',
     'Leadership retreats on two acres above the Jamison Valley.'),
    ('the-carrington-hotel-katoomba',
     'Small residential programs and heritage dinners in the middle of Katoomba.'),
    ('blue-mountains-cultural-centre',
     'Offsite dinners, launches and plenary overflow for a group already in town.')],
  sources=['Residential conference and retreat properties with the rooms on site',
           'Heritage hotels for dinners, offsites and smaller programs',
           'Exclusive use houses for board and leadership groups',
           'Council and National Trust venues for offsite dinners and activations',
           'Coach logistics from Sydney and between the mountain villages'],
  precincts=['Leura', 'Katoomba', 'Medlow Bath', 'Blackheath and Mount Victoria',
             'Wentworth Falls and the lower mountains'],
  start=[
    ('Residential conferences', 'Fairmont Resort Blue Mountains, Hydro Majestic, The Carrington'),
    ('Leadership retreats and board offsites', 'Ardour Lilianfels, Echoes, the Blackheath lodges'),
    ('Premium gala dinners', 'Fairmont Grand Ballroom, The Carrington Grand Dining Room'),
    ('Incentives', 'Hydro Majestic, Ardour Lilianfels, Everglades for a daytime activation'),
    ('Product launches and brand events', 'Blue Mountains Cultural Centre, the Hydro Majestic Wintergarden'),
    ('Large exhibitions and fly in meetings', 'Not here. <a href="venue-finder-sydney.html">Sydney</a>')],
  local=[
    ('Leura', 'A full residential conference of 100 to 600 with everything on one site. The Fairmont is the region’s only resort scale conference hotel, and Leura is the first of the upper mountains villages you reach from Sydney, which saves the most transfer time.'),
    ('Katoomba', 'When you want the group dispersed across characterful properties and walking to dinner. The deepest concentration of stock, and the one precinct where individual rail arrivals genuinely work, with the station in the centre of town.'),
    ('Medlow Bath', 'A single building residential program of 60 to 200 that wants a hero property and no distractions. Effectively one venue, with no walkable town, so the coach is not optional and every meal is on site.'),
    ('Blackheath and Mount Victoria', 'Small leadership retreats where the point is that nobody can leave. Guesthouses and lodges rather than conference hotels, so plan for groups under about thirty, and it is the furthest from Sydney.'),
    ('Wentworth Falls and the lower mountains', 'When the priority is minimising drive time from Sydney and the group is small. Conference grade accommodation is thin, so this is usually a day meeting or an arrival day rather than the residential base.'),
    ('Lithgow and the western valleys', 'Genuine remoteness beyond the escarpment for a small, high budget program. Verify the operator before you commit, because at least one well known property in this area is no longer trading under the brand people remember.')],
  tradeoffs=[
    ('Tell delegates to pack a real coat',
     'This is a mountain region at about a thousand metres. Bureau of Meteorology averages for Katoomba put July at a mean maximum of 9.5 degrees and a mean minimum of 2.6, and even January averages a maximum of 23.4. Fog also takes the views away without warning. It is the single most under briefed thing about the destination.'),
    ('It is a national park, and closures happen',
     'NSW National Parks states plainly that the park may close at times due to poor weather or fire danger. Any outdoor or offsite element needs a wet weather and a fire danger fallback written into the run sheet rather than assumed.'),
    ('Above 620 theatre we have not found a room here',
     'Among the Blue Mountains venues we have verified there is no exhibition hall, no convention centre and no pillarless floor plate at exhibition scale. Anything with a trade floor, more than about three concurrent streams or more than 600 delegates is better placed in Sydney, and a same day fly in meeting should not come here at all. If you know of a room up here that changes that, tell us and we will go and look at it.')],
  why_h2='The Blue Mountains works because the group stays together after six.',
  why_lead='Ninety minutes from Sydney, on one road corridor, with almost nothing to do after dark except the program you designed. That is the entire argument for the region, and it is why the retreat and the residential conference are the two things it does properly.',
  faqs=[
    ('How much does it cost to use CVBS to find a venue in the Blue Mountains?', 'FREE'),
    ('How quickly can you find Blue Mountains venues?', 'FAST'),
    ('What is the largest conference venue in the Blue Mountains?',
     'The largest single conference room published by any Blue Mountains hotel or resort is the Fairmont Resort Blue Mountains Grand Ballroom at 620 theatre, which is the Ballroom and Pioneers rooms opened together. The largest single undivided room is the Ballroom at 364 theatre. The Fairmont notes its published capacities do not allow for staging, a dance floor or a buffet.'),
    ('How many delegates can stay on one Blue Mountains property?',
     'Up to 224 rooms at the Fairmont Resort Blue Mountains, which is the largest published room count in the region. The next largest are the Hydro Majestic at 82, The Carrington at 65 and Mountain Heritage at 41, so beyond about 224 a group is split across properties in different towns.'),
    ('Do you cover group accommodation in the Blue Mountains as well as venues?', 'GROUP'),
    ('Can delegates get to the Blue Mountains by train?',
     'Yes. The Blue Mountains line runs direct from Central and is genuinely usable for individual delegates arriving at Katoomba, Leura or Medlow Bath. Stations are not at the venues and every property sits above its town, so for a group we would still budget a coach for the last leg and for any offsite.'),
    ('What is the weather actually like?',
     'Cold in winter and mild in summer, at about a thousand metres. Bureau of Meteorology averages for Katoomba give a July mean maximum of 9.5 degrees and a January mean maximum of 23.4. Fog can remove the views on any day of the year. Tell delegates to bring a coat and closed shoes for anything between May and September.'),
    ('Is the Blue Mountains suitable for a large conference?',
     'Not above about 600 delegates, and not for anything with a trade floor. There is no convention centre and no exhibition hall in the region. It is a retreat and residential conference destination, and where a brief outgrows that we would put <a href="venue-finder-sydney.html">Sydney</a> in front of you instead.')],
  related=[
    ('venue-finder-sydney.html', 'Sydney',
     'Ninety minutes east, and where a program with a trade floor belongs.'),
    ('venue-finder-hunter-valley.html', 'Hunter Valley',
     'The other Sydney offsite region, with more resort scale room supply.'),
    ('cbd-vs-resort-conference-venues.html', 'City or resort',
     'When a mountains property earns the drive, and when Sydney wins on logistics alone.')],
)

# ------------------------------------------------------------------ BYRON BAY
DEST['Byron Bay'] = dict(
  file='venue-finder-byron-bay.html', state='NSW',
  title='Retreat, Incentive &amp; Event Venues in Byron Bay | CVBS',
  meta=('Byron Bay retreat, incentive and event venue finding. Elements of Byron, Crystalbrook '
        'Byron and the Northern Rivers, with published capacities and a shortlist within 48 hours, '
        'free to you.'),
  h1='Retreat, Incentive &amp; Event Venues in Byron Bay',
  lead='Tell us what you need in Byron Bay. Shortlist within 48 hours, free to you.',
  snapshot=[
    '<b>Byron Bay is a small, premium, capacity limited market, and the numbers matter more here '
    'than almost anywhere else.</b> The largest single room in town by published theatre capacity is '
    'Byron Theatre at the Byron Community Centre, at 266 in raked fixed seating with no accommodation '
    'attached. The largest purpose built flat floor conference room is Crystalbrook Byron’s, at 192 '
    'theatre across 216 square metres.',
    '<b>Accommodation is the binding constraint.</b> Elements of Byron holds 202 villas containing '
    '296 bedrooms and is the largest single block in the area; Crystalbrook Byron has 92 suites, so '
    'its conference room seats more people than the resort can sleep. Above roughly 200 delegates in '
    'plenary and roughly 300 residential delegates, no single property in the region works.',
    '<b>Two things have changed recently and both are worth knowing.</b> The Byron at Byron now '
    'trades as Crystalbrook Byron, so treat them as one property rather than two options; and Byron '
    'Shire caps non hosted short term rental accommodation at 60 days a year across most of the '
    'local government area, which has removed a large slice of the whole house inventory planners '
    'used to absorb overflow. What the region is genuinely excellent at is the leadership retreat, '
    'the wellness program, the incentive and the brand event. '
    '<a href="#byron-bay-featured">See the venues we would start with</a>.'],
  featured=[
    ('elements-of-byron',
     'The only single site block big enough for a residential conference of any scale.'),
    ('crystalbrook-byron',
     'The largest purpose built flat floor conference room in the area, with a full setup chart.'),
    ('byron-theatre-community-centre',
     'A presentation led launch or awards night with real theatre sightlines, in town.'),
    ('raes-on-wategos',
     'A whole property buyout on Wategos Beach for a board or a top tier incentive.'),
    ('byron-bay-surf-club',
     'Beachfront welcome functions and brand activations for up to about 150.'),
    ('ramada-ballina-byron',
     'The working sessions and the budget rooms, beside the region’s only airport.')],
  sources=['Beachfront resorts for residential conferences and incentive groups',
           'Exclusive use properties for board and leadership retreats',
           'Town venues for launches, awards nights and brand activations',
           'Hinterland houses around Bangalow, Newrybar and Federal',
           'Ballina and Lennox Head properties when Byron itself is full'],
  precincts=['Byron Bay town centre', 'Belongil', 'Suffolk Park and Broken Head Road',
             'Bangalow', 'Lennox Head', 'Ballina', 'Byron hinterland'],
  start=[
    ('Leadership retreats and offsites', 'Rae’s on Wategos, Crystalbrook Byron, hinterland buyouts'),
    ('Residential conferences', 'Elements of Byron, Crystalbrook Byron with a second town hotel'),
    ('Incentives', 'Rae’s on Wategos, Elements of Byron villas, Crystalbrook Byron'),
    ('Premium dinners', 'Crystalbrook Byron, Elements of Byron, Byron Theatre on a flat floor'),
    ('Product launches and brand events', 'Byron Theatre, Byron Bay Surf Club, the Elements lawns'),
    ('Large conferences and fly in meetings', 'Not here. <a href="venue-finder-gold-coast.html">Gold Coast</a> or Brisbane')],
  local=[
    ('Byron Bay town centre', 'When delegates should walk to dinner, bars and the beach without a transfer. Accommodation is small hotels and apartments rather than one block, and it is one of only two areas retaining year round non hosted short term rental availability.'),
    ('Belongil', 'A single property residential conference, because Elements of Byron’s 202 villas are the only block of that scale in the region. Accommodation and meeting space are on the same site, but delegates are not walking into town.'),
    ('Suffolk Park and Broken Head Road', 'A purpose built conference room in a rainforest setting about ten minutes south of town. Crystalbrook Byron sleeps well under what its conference room seats, so larger groups need a second hotel and a shuttle.'),
    ('Bangalow', 'Hinterland character and a village main street for creative offsites and brand dinners. Limited dispersed accommodation, so it works as a daytime or dinner destination attached to beds in Byron.'),
    ('Lennox Head', 'A quieter coastal alternative between Byron and Ballina for small retreats. Predominantly small scale and holiday let accommodation, and it sits in a different council area with a less restrictive short term rental cap.'),
    ('Ballina', 'Air access and cost control. The airport is here with direct Sydney and Melbourne services, and a 110 room hotel with four meeting rooms half an hour from Byron. A Ballina base with Byron evenings is a real and commonly used structure.')],
  tradeoffs=[
    ('Room supply, not meeting space, is what will stop you',
     'Elements of Byron at 296 bedrooms is the only block of scale in the region, and the Byron Shire 60 day cap on non hosted short term rentals has removed a lot of the whole house inventory planners used to lean on for overflow. Confirm what is legally available before you price the program.'),
    ('Air access is thin',
     'Ballina Byron Gateway Airport flies direct to Sydney and Melbourne only, so delegates from Perth, Adelaide, Canberra or overseas connect and lose most of a travel day each way. Gold Coast Airport and a road transfer is the usual workaround, and Brisbane is under two hours.'),
    ('This is an expensive market and the premium properties know it',
     'Peak season rates are firm and the small properties do not discount. Where the budget will not carry Byron, Lennox Head, Ballina and the hinterland do the same job for less, and we will say so rather than stretch the brief.')],
  why_h2='Byron rewards small and premium, and punishes scale.',
  why_lead='The region has one accommodation block of real size and one purpose built conference room, so most of the work here is matching a brief to what actually exists rather than shortlisting widely. When a brief is too big for Byron we say so early, because finding that out late is expensive.',
  faqs=[
    ('How much does it cost to use CVBS to find a venue in Byron Bay?', 'FREE'),
    ('How quickly can you find Byron Bay venues?', 'FAST'),
    ('What is the largest venue in Byron Bay?',
     'By published theatre capacity, Byron Theatre at the Byron Community Centre, at 266 in raked fixed seating in the middle of town, with no accommodation attached. The largest purpose built flat floor conference room is Crystalbrook Byron’s at 192 theatre across 216 square metres.'),
    ('How many delegates can stay on one property in Byron Bay?',
     'Elements of Byron is the largest single block, at 202 villas containing 296 bedrooms on a beachfront site at Belongil. Crystalbrook Byron has 92 suites and Rae’s on Wategos has 17 keys, so above roughly 300 residential delegates there is no single property answer in the region.'),
    ('Do you cover group accommodation in Byron Bay as well as venues?', 'GROUP'),
    ('Which airport should Byron Bay delegates fly into?',
     'Ballina Byron Gateway Airport is the closest, about thirty minutes from the centre of Byron Bay, but it flies direct to Sydney and Melbourne only. Gold Coast Airport is the common alternative, and Brisbane is under two hours by road. For a national group we usually plan around a mix of the three.'),
    ('Has the accommodation situation in Byron changed?',
     'Yes, and it matters for group bookings. Byron Shire caps non hosted short term rental accommodation at 60 days a year across most of the local government area, with the Byron Bay town centre precinct and Brunswick Heads the exceptions. That has removed a large part of the whole house inventory that used to absorb overflow delegates, so we confirm what is legally available before pricing a block.'),
    ('Is Byron Bay suitable for a large conference?',
     'No, and it is better to hear that now. There is no convention centre, no exhibition hall and no verified pillarless space with exhibition grade floor loading; the largest verified single room is 300 square metres. Anything needing a trade floor or more than about 270 in plenary belongs on the <a href="venue-finder-gold-coast.html">Gold Coast</a> or in Brisbane, both within about two hours.')],
  related=[
    ('venue-finder-gold-coast.html', 'Gold Coast',
     'Under two hours north, with a convention centre and real room supply.'),
    ('cbd-vs-resort-conference-venues.html', 'City or resort',
     'Byron is a resort market with no city fallback, so the trade-offs are sharper.'),
    ('events.html', 'Product launches and events',
     'How we source a space when the setting is doing half the work.')],
)

# ---------------------------------------------------------------- YARRA VALLEY
DEST['Yarra Valley'] = dict(
  file='venue-finder-yarra-valley.html', state='VIC',
  title='Conference, Retreat &amp; Winery Venues in the Yarra Valley | CVBS',
  meta=('Yarra Valley conference, retreat and winery event venue finding. Healesville, Yarra '
        'Glen, Coldstream and Yering venues with published capacities and a shortlist within 48 hours, '
        'free to you.'),
  h1='Conference, Retreat &amp; Winery Venues in the Yarra Valley',
  lead='Tell us what you need in the Yarra Valley. Shortlist within 48 hours, free to you.',
  snapshot=[
    '<b>The Yarra Valley is a leadership retreat and residential offsite region, and the numbers '
    'are small by design.</b> The largest published single room theatre capacity of the venues we '
    'checked is the Marmion Ballroom at Yarra Valley Lodge in Chirnside Park, at 325 across 305 '
    'square metres. RACV Healesville’s Ballroom is close behind at 320 theatre and larger by floor '
    'area at 400 square metres, and it is the only venue in the district that publishes ceiling '
    'heights at all.',
    '<b>Bed count, not meeting space, is the binding constraint.</b> Yarra Valley Lodge publishes '
    '102 rooms, RACV Healesville 80 rooms sleeping 160, Balgownie Estate 70 suites, Chateau Yering '
    '32 and Meletos 23. A 325 seat plenary at Yarra Valley Lodge cannot sleep its own plenary in '
    'single occupancy, which is the sort of thing worth knowing before the agenda is written.',
    '<b>The best winery event capacity in the region carries no guest rooms at all.</b> CHANDON, '
    'Yering Station, TarraWarra Museum of Art and Levantine Hill all publish event spaces and no '
    'accommodation, so a winery based program needs a separate accommodation contract and transfers. '
    'The venues sit across separate towns rather than one precinct, so nothing here is walkable. '
    '<a href="#yarra-valley-featured">See the venues we would start with</a>.'],
  featured=[
    ('racv-healesville-country-club',
     'Multi day residential programs that break out repeatedly, with six syndicate rooms.'),
    ('yarra-valley-lodge',
     'The largest plenary in the district, with 102 rooms and the shortest run from the city.'),
    ('chateau-yering-hotel',
     'A 20 to 40 person exclusive use retreat in a heritage house.'),
    ('levantine-hill-estate',
     'The largest seated winery dinner in the region, with a real conference fit out.'),
    ('tarrawarra-museum-of-art',
     'A forum or a launch inside a public art museum, with fixed AV and a glass wall.'),
    ('balgownie-estate-yarra-valley',
     'The third residential resort of scale, when the other two are held.')],
  sources=['Residential conference and retreat properties with the rooms on site',
           'Working winery estates for dinners, launches and offsite days',
           'A museum plenary for forums and product launches',
           'Heritage houses for board level exclusive use',
           'Coach logistics from Melbourne and between the valley towns'],
  precincts=['Healesville', 'Chirnside Park', 'Coldstream', 'Yering', 'Yarra Glen'],
  start=[
    ('Leadership retreats and offsites', 'Chateau Yering, Meletos, Yering Station’s boardroom'),
    ('Residential conferences', 'RACV Healesville, Yarra Valley Lodge, Balgownie Estate'),
    ('Premium winery dinners', 'Levantine Hill, RACV Healesville Ballroom, Chateau Yering Oak Room'),
    ('Incentives', 'CHANDON, Levantine Hill, Healesville Sanctuary'),
    ('Product launches and brand events', 'TarraWarra Museum of Art, Levantine Hill'),
    ('Large conferences and fly in meetings', 'Not here. <a href="venue-finder-melbourne.html">Melbourne CBD</a>')],
  local=[
    ('Healesville', 'When the program is residential and needs real breakout depth. RACV Healesville has thirteen function rooms including six syndicate rooms, with TarraWarra and Healesville Sanctuary in the same town, so beds, plenary and a distinctive offsite sit together.'),
    ('Chirnside Park', 'The largest single room and the shortest run from the city. Yarra Valley Lodge is self contained with 102 rooms and nine venues inside a private golf estate, and the property publishes about 45 minutes from the Melbourne CBD. It is the gateway rather than wine country.'),
    ('Coldstream', 'Winery dinners, incentives and launches. CHANDON, Levantine Hill and the Meletos estate sit here, which gives the precinct strong event spaces and very shallow beds, so any group above about 25 staying here is split.'),
    ('Yering', 'Boards, executive teams and heritage dinners. Chateau Yering gives 32 suites and an Oak Room seating 130, with Yering Station next door. This is the buyout precinct for a group of 20 to 40 and it does not scale past that.'),
    ('Yarra Glen', 'The third residential resort of scale, at 70 suites, and the fallback when Healesville and Chirnside Park are both held. Its room capacities are not published, so nothing can be quoted without a direct confirmation.')],
  tradeoffs=[
    ('Most wineries have no beds',
     'The venues with the best rooms for a dinner are not the venues with the rooms for the night. That is fine when it is planned and expensive when it is not, so we settle the accommodation contract and the transfers before we get excited about a cellar door.'),
    ('It is a dispersed region with no useful public transport',
     'Healesville, Coldstream, Yering, Yarra Glen and Chirnside Park are separate towns. A delegate cannot get between them without a car or a coach, and neither the tourism authority nor the properties publish reliable town to town drive times, so we cost the transfers explicitly rather than estimating them.'),
    ('Above 325 in plenary we have not verified a room here',
     'Across the Yarra Valley venues we have verified there is no exhibition hall, the largest floor plate is 400 square metres and the largest accommodation base at one address is 102 rooms. Anything above about 325 in plenary or requiring a trade floor is better placed in the Melbourne CBD, and we would say so.')],
  why_h2='The Yarra Valley is where a Melbourne leadership program actually belongs.',
  why_lead='An hour from the city, with exclusive use properties, real breakout depth and a cellar door program on the doorstep. What it is not is a conference destination at scale, and knowing exactly where that line sits is the most useful thing we bring to a Yarra Valley brief.',
  faqs=[
    ('How much does it cost to use CVBS to find a venue in the Yarra Valley?', 'FREE'),
    ('How quickly can you find Yarra Valley venues?', 'FAST'),
    ('What is the largest conference venue in the Yarra Valley?',
     'Of the venues we checked, the Marmion Ballroom at Yarra Valley Lodge in Chirnside Park has the largest published single room theatre capacity at 325, across 305 square metres. RACV Healesville’s Ballroom is larger by floor area at 400 square metres and seats 320 theatre.'),
    ('How many delegates can stay on one Yarra Valley property?',
     'Yarra Valley Lodge publishes 102 rooms, which is the largest inventory of the properties we checked. RACV Healesville publishes 80 rooms sleeping 160, Balgownie Estate 70 suites, Chateau Yering 32 and Meletos 23. Above about 100 delegates in single occupancy a program becomes a two property exercise.'),
    ('Do you cover group accommodation in the Yarra Valley as well as venues?', 'GROUP'),
    ('Can we hold a conference at a Yarra Valley winery?',
     'For the dinner, the launch or an offsite day, yes, and Levantine Hill has the most genuine conference fit out of the working wineries. For a multi day residential program, no: CHANDON, Yering Station, TarraWarra and Levantine Hill all publish event spaces and no accommodation, so the group sleeps elsewhere and coaches in.'),
    ('Yarra Valley or Mornington Peninsula for a leadership program?',
     'The Yarra Valley is closer to the Melbourne CBD and more compact, with better breakout depth at RACV Healesville. The <a href="venue-finder-mornington-peninsula.html">Mornington Peninsula</a> adds coastline, the Sorrento village and a larger single residential property at 204 rooms. If the group is 40 or under and the agenda is dense, we usually lean Yarra Valley.'),
    ('Is the Yarra Valley suitable for a large conference?',
     'Not above about 325 in plenary. There is no exhibition hall, the largest verified floor plate is 400 square metres and the largest single accommodation base is 102 rooms. A program at that scale belongs in the <a href="venue-finder-melbourne.html">Melbourne CBD</a>.')],
  related=[
    ('venue-finder-melbourne.html', 'Melbourne',
     'An hour west, and where a program with a trade floor or air access belongs.'),
    ('venue-finder-mornington-peninsula.html', 'Mornington Peninsula',
     'The other Melbourne offsite region, with coast as well as vineyards.'),
    ('cbd-vs-resort-conference-venues.html', 'City or resort',
     'Whether an hour out of Melbourne buys enough to be worth the coach transfers.')],
)

# --------------------------------------------------------- MORNINGTON PENINSULA
DEST['Mornington Peninsula'] = dict(
  file='venue-finder-mornington-peninsula.html', state='VIC',
  title='Retreat, Offsite &amp; Conference Venues on the Mornington Peninsula | CVBS',
  meta=('Mornington Peninsula retreat, offsite and conference venue finding. Cape Schanck, Red '
        'Hill, Sorrento and Flinders venues with published capacities and a shortlist within 48 hours, '
        'free to you.'),
  h1='Retreat, Offsite &amp; Conference Venues on the Mornington Peninsula',
  lead='Tell us what you need on the Mornington Peninsula. Shortlist within 48 hours, free to you.',
  snapshot=[
    '<b>The Mornington Peninsula is a leadership retreat and incentive region with one property '
    'doing the heavy lifting.</b> RACV Cape Schanck Resort is the largest residential conference '
    'property on published room counts, at 204 rooms with a 483 square metre Great Southern Ballroom '
    'seating 450 theatre across thirteen function rooms. The largest single room in the region is '
    'the Gunnamatta at Mornington Racecourse at 500 theatre and 650 banquet, and it has no '
    'accommodation at all.',
    '<b>Above about 200 rooms on one site there is nothing.</b> After RACV Cape Schanck the '
    'published room counts run 108 at The Continental Sorrento, 65 at Peppers Moonah Links, 44 at '
    'Jackalope, 40 at Lindenderry and 40 at Flinders Hotel. Six verified properties across five '
    'towns hold about 501 rooms between them, so a 250 room residential program is split across '
    'towns and coached to a shared plenary.',
    '<b>Distance and access shape everything here.</b> The regional bureau publishes Mornington at '
    'sixty minutes from the Melbourne CBD, Cape Schanck at seventy five and Flinders and Sorrento at '
    'about ninety, and the official tourism authority states there is no public transport into the '
    'hinterland at all. Coach transfer is effectively mandatory for any Red Hill or winery based '
    'program. <a href="#mornington-peninsula-featured">See the venues we would start with</a>.'],
  featured=[
    ('racv-cape-schanck-resort',
     'The only property that runs a large residential conference on one Peninsula site.'),
    ('mornington-racecourse',
     'The largest single room in the region, when no hotel will seat the group.'),
    ('the-continental-sorrento',
     'A two night senior program with a village, a beach and a spa at the door.'),
    ('lancemore-lindenderry-red-hill',
     'A single cohort leadership group on a working vineyard, with published room dimensions.'),
    ('jackalope-hotel',
     'A design led buyout for an executive team or a board, Monday to Thursday.'),
    ('pt-leo-estate',
     'Incentive hosting, gala dinners and launches on a vineyard and sculpture park.')],
  sources=['Residential conference and retreat resorts with the rooms on site',
           'Golf resorts for programs built around a course',
           'Boutique properties for exclusive use board and executive offsites',
           'Winery and restaurant venues for incentive dinners and launches',
           'Coach logistics from Melbourne and between the Peninsula towns'],
  precincts=['Mornington and Mount Eliza', 'Red Hill and Main Ridge', 'Merricks and Flinders',
             'Cape Schanck and Fingal', 'Sorrento and Portsea', 'Rye and Rosebud'],
  start=[
    ('Leadership retreats and offsites', 'Lancemore Lindenderry, Jackalope, Port Phillip Estate'),
    ('Residential conferences', 'RACV Cape Schanck, The Continental Sorrento, Peppers Moonah Links'),
    ('Premium gala and winery dinners', 'Pt. Leo Estate, Montalto, RACV Cape Schanck, The Continental'),
    ('Incentives', 'Pt. Leo Estate, Peninsula Hot Springs, Jackalope, the Sorrento ferry'),
    ('Large dinners above 450', 'Mornington Racecourse, with accommodation sourced separately'),
    ('Large conferences and fly in meetings', 'Not here. <a href="venue-finder-melbourne.html">Melbourne CBD</a>')],
  local=[
    ('Mornington and Mount Eliza', 'The northern gateway, and the shortest transfer at about sixty minutes from the city. The racecourse holds the largest rooms in the region but no accommodation of scale, so delegates commute from Melbourne or stay further down the Peninsula.'),
    ('Red Hill and Main Ridge', 'A leadership retreat that wants to be off grid and among vines. Lindenderry gives 40 rooms plus a 200 theatre room in one place; Montalto and Port Phillip Estate give dining and boardroom work with no meaningful bed stock. No public transport at all, so coaching is compulsory.'),
    ('Merricks and Flinders', 'Small premium groups and the food and wine element. Jackalope, Pt. Leo Estate and Flinders Hotel sit here. Flinders is the longest drive from the city at about ninety minutes, so a group based here loses most of a working day at each end.'),
    ('Cape Schanck and Fingal', 'When the program is genuinely residential and needs one site. RACV Cape Schanck at 204 rooms and Peppers Moonah Links at 65 are the whole inventory, at about seventy five minutes from the city, which is the best compromise between capacity and transfer time.'),
    ('Sorrento and Portsea', 'A two night senior program that wants a village, a beach and a spa within walking distance of the meeting room. It is the deepest point in the region, and the only precinct where the Queenscliff ferry, a forty minute vehicle crossing, opens a second arrival route.'),
    ('Rye and Rosebud', 'Accommodation overflow and activity supply rather than a conference base. Motel and apartment stock, sitting between the Fingal resorts and Sorrento, which makes it useful for bridging a split group by coach.')],
  tradeoffs=[
    ('The biggest room and the beds are in different places',
     'The highest capacity room in the region sits at a racecourse with no accommodation, and the properties with beds top out at 204 rooms. Any program combining a large plenary with a winery dinner is a two site program with coaching built in from the start.'),
    ('The premium venues restrict weekends by policy, not price',
     'Pt. Leo Estate permits weekend exclusivity on only four days a calendar year, and Jackalope publishes corporate rates Monday to Thursday only. Weekday dates are the realistic ask at the top of this market, and it is better to know that before a board sets a Friday.'),
    ('Melbourne Airport is on the wrong side of the city',
     'The bureau’s sixty to ninety minute drive times are from the CBD, and the airport adds a city crossing on top. For a one day meeting with flown in attendees the Melbourne CBD wins on every measure, and we would tell you so.')],
  why_h2='The Peninsula is an exclusive use region, and that is what it is for.',
  why_lead='At 40 to 65 rooms you can take a whole property, which no Melbourne hotel will offer at that price, and the coast and the vineyards do real work on a group. The constraint is that above about 200 rooms on one site the region simply stops, and knowing where that line falls is most of the job.',
  faqs=[
    ('How much does it cost to use CVBS to find a venue on the Mornington Peninsula?', 'FREE'),
    ('How quickly can you find Mornington Peninsula venues?', 'FAST'),
    ('What is the largest conference venue on the Mornington Peninsula?',
     'The largest single room verified among Peninsula venues is the Gunnamatta at Mornington Racecourse, at 500 theatre, 650 banquet and 800 cocktail, and it has no accommodation. The largest residential conference property is RACV Cape Schanck Resort, at 204 rooms with a 483 square metre ballroom seating 450 theatre across thirteen function rooms.'),
    ('How many delegates can stay on one Peninsula property?',
     'Up to 204 rooms at RACV Cape Schanck Resort. After that the published counts run 108 at The Continental Sorrento, 65 at Peppers Moonah Links, 44 at Jackalope, 40 at Lindenderry and 40 at Flinders Hotel, so above roughly 200 rooms a program is split across towns.'),
    ('Do you cover group accommodation on the Mornington Peninsula as well as venues?', 'GROUP'),
    ('How long does it take to get to the Mornington Peninsula from Melbourne?',
     'The regional bureau publishes Mornington at sixty minutes from the Melbourne CBD, Cape Schanck at seventy five, and Flinders and Sorrento at about ninety. Melbourne Airport sits on the opposite side of the city, so an interstate delegate should expect a city crossing on top of those figures.'),
    ('Can delegates use public transport on the Peninsula?',
     'Not usefully. The official tourism authority states buses run from Frankston station to Portsea and Flinders, and that there is no public transport into the hinterland area. For any Red Hill or winery based program, coach transfer is effectively mandatory, and we cost it at shortlist rather than later.'),
    ('Mornington Peninsula or Yarra Valley for a leadership program?',
     'The Peninsula gives you coastline, the Sorrento village and the Queenscliff ferry as arrival theatre, plus a larger single residential property at 204 rooms. The <a href="venue-finder-yarra-valley.html">Yarra Valley</a> is closer to the city and more compact, with deeper breakout inventory at RACV Healesville. For anything above about 100 rooms on one site, the Peninsula is the answer.')],
  related=[
    ('venue-finder-melbourne.html', 'Melbourne',
     'An hour north, and where a program with a trade floor or air access belongs.'),
    ('venue-finder-yarra-valley.html', 'Yarra Valley',
     'The other Melbourne offsite region, closer to the city and more compact.'),
    ('cbd-vs-resort-conference-venues.html', 'City or resort',
     'What a peninsula property gives a program that a Melbourne hotel cannot.')],
)

# --------------------------------------------------------------------- SYDNEY
# Patch mode. The Sydney page already carries a hero, featured venues with
# photography, a walked-through band, the answer block, the index, where to
# start, local knowledge and the Why CVBS band. It only needs the three things
# the rest of the section gained: the trade-offs, the longer FAQ and the
# related destinations. Nothing else on that page is rebuilt.
DEST['Sydney'] = dict(
  mode='patch',
  file='venue-finder-sydney.html', state='NSW',
  title='Conference &amp; Event Venues in Sydney | CVBS',
  meta=('Sydney conference and event venue finding. Published capacities for the venues we know '
        'across the CBD, Darling Harbour, Barangaroo and the airport precinct, with a shortlist '
        'within 48 hours, free to you.'),
  tradeoffs=[
    ('Above 2,000 seated, none of it is a hotel',
     'ICC Sydney’s Grand Ballroom at 2,784 is the top of the hotel style market. Beyond that you are choosing between Sydney Showground’s Dome, the Opera House Concert Hall and Sydney Town Hall, none of which are conference buildings, and all of which need a room block sourced separately.'),
    ('Between 500 and 1,500 the accommodation decides it',
     'Plenty of Sydney rooms hold those numbers. Far fewer hold the numbers and the delegates in the same building, and the ones that do book out first. If your program is residential in that band, the room block is the thing to secure before the ballroom.'),
    ('Sydney is really six or seven precincts',
     'Darling Harbour, the CBD, Circular Quay, Barangaroo, North Sydney and the airport precinct behave like different cities for the purposes of a program. The precinct decides how far delegates walk, what they do at six o’clock and what dinner costs, and it is a bigger decision than the venue.')],
  faqs=[
    ('How much does it cost to use CVBS to find a venue in Sydney?', 'FREE'),
    ('How quickly can you find Sydney venues?', 'FAST'),
    ('Do you cover group accommodation in Sydney as well as venues?', 'GROUP'),
    ('What is the largest conference venue in Sydney?',
     'ICC Sydney at Darling Harbour. Its Grand Ballroom seats 2,784 theatre style under a nine metre ceiling and is, on ICC’s own description, the largest ballroom in Australia. It sits alongside 32,600 square metres of exhibition halls and 70 meeting rooms.'),
    ('Which Sydney hotel has the largest ballroom?',
     'The Fullerton Hotel Sydney, whose Grand Ballroom holds 1,400 theatre across 1,058 pillarless square metres in the former GPO on Martin Place. Hilton Sydney at 1,100 and Hyatt Regency at 1,000 are the only other Sydney hotels seating a thousand or more in one room, and Hyatt is the one that can run two at once.'),
    ('Where should a 500 delegate conference be held in Sydney?',
     'It depends whether the delegates are staying overnight. If they are, Darling Harbour is usually the answer, because the large conference hotels and ICC sit in the same precinct. If they are not, the CBD gives you a much wider choice and the constraint stops being capacity and becomes availability on your dates.'),
    ('Which Sydney precinct suits a fly in, fly out meeting?',
     'Mascot and the airport precinct, where interstate delegates can land, meet and leave the same day without entering the city. For a half day meeting with a senior audience, North Sydney and the CBD both work if the flights allow it.'),
    ('Can you help with a Sydney offsite outside the city?',
     'Yes. The <a href="venue-finder-hunter-valley.html">Hunter Valley</a> is a little over two hours north and the <a href="venue-finder-blue-mountains.html">Blue Mountains</a> about ninety minutes west, and both do the residential leadership program better than the city does. We source across all three.')],
  related=[
    ('venue-finder-hunter-valley.html', 'Hunter Valley',
     'Two hours north, with the largest regional residential conference resort in the state.'),
    ('venue-finder-blue-mountains.html', 'Blue Mountains',
     'Ninety minutes west, where a group cannot go home at six o’clock.'),
    ('venue-visits/', 'Venues we have walked',
     'Our own photographs and honest notes from the Sydney rooms we have been through.')],
)
