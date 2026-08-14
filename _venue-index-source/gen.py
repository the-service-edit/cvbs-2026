# -*- coding: utf-8 -*-
import json, sys, io
sys.path.insert(0, '/tmp/cvbs2')
from venues_sydney import VENUES, CITY

VERIFIED = "14 August 2026"

keys = ['n','sp','pr','ty','th','bq','cl','ck','cab','ush','bd','br','gr',
        'area','ceil','ceilq','s_name','s_th','note']
data = [{k: v[k] for k in keys} for v in VENUES]
island = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

n_ceil = sum(1 for v in VENUES if v['ceil'])
n_second = sum(1 for v in VENUES if v['s_name'])

items = []
for i, v in enumerate(VENUES, 1):
    props = []
    if v['area']: props.append({"@type":"PropertyValue","name":"Largest space floor area","value":v['area'],"unitCode":"MTK"})
    if v['ceil']: props.append({"@type":"PropertyValue","name":"Largest space ceiling height","value":v['ceil'],"unitCode":"MTR"})
    if v['br']:   props.append({"@type":"PropertyValue","name":"Meeting rooms","value":v['br']})
    ev = {"@type":"EventVenue","name":v['n'],"maximumAttendeeCapacity":v['th'],
          "address":{"@type":"PostalAddress","addressLocality":v['pr'],"addressRegion":"NSW","addressCountry":"AU"}}
    if props: ev["additionalProperty"] = props
    items.append({"@type":"ListItem","position":i,"item":ev})
schema = {"@context":"https://schema.org","@type":"ItemList",
  "name":"Conference and event venue capacity index, %s" % CITY,
  "description":"Published theatre, banquet, classroom, cabaret and cocktail capacities for %d major %s conference and event venues, with ceiling heights, floor areas, meeting room and guest room counts. Verified %s." % (len(VENUES), CITY, VERIFIED),
  "numberOfItems":len(VENUES),"itemListOrder":"https://schema.org/ItemListOrderDescending",
  "itemListElement":items}

srcs = "\n".join("     %-38s\n       capacities  %s\n       specs       %s" % (v['n'], v['src'], v['src2']) for v in VENUES)

SECTION = '''<section class="s-stone pad" id="venue-index">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">{city} venue index</span>
      <h2 class="h2">{city}'s {n} principal conference venues, and what they actually hold.</h2>
      <p class="lead">Published capacities, ceiling heights and floor areas, filterable by size, setup, precinct and type. The numbers venues rarely put in one place, in one place.</p></div>

    <div class="vidx-lede">
    <div class="vidx-answer">
      <span class="vidx-answer__tag">The short answer</span>
      <p><b>{city}'s largest conference venue is ICC Sydney at Darling Harbour.</b> Its Grand Ballroom seats 2,784 theatre style under a 9 metre ceiling and is, on ICC's own description, the largest ballroom in Australia. Beside it sit a 2,500 seat tiered theatre, an 8,000 seat plenary theatre and 32,600 square metres of exhibition halls.</p>
      <p><b>Above 2,000 delegates seated in one room, {city} has four options and none of them is a hotel.</b> Sydney Showground's Dome at Olympic Park takes 7,000, ICC Sydney's Grand Ballroom 2,784, the Sydney Opera House Concert Hall 2,102 facing the stage, and Sydney Town Hall's Centennial Hall 2,008 across the floor and galleries. The Hordern Pavilion at Moore Park holds 3,500 standing and 1,400 for dinner.</p>
      <p><b>Between 500 and 1,500 delegates the constraint becomes accommodation.</b> The Fullerton Hotel Sydney's Grand Ballroom holds 1,400 theatre across 1,058 pillarless square metres and is the largest pillarless hotel ballroom in the city. Hilton Sydney at 1,100 and Hyatt Regency Sydney at 1,000 are the only other Sydney hotels that seat more than 1,000 in a single room. Hyatt is the one that can run two of them at once, because its Maritime Ballroom seats another 1,000.</p>
      <p><b>Below 400 delegates the CBD carries the deepest supply</b>, with more than a dozen conference hotels inside a ten minute walk of Wynyard and Town Hall. At that size the constraint is rarely capacity. It is availability on your dates, and the rate you are quoted. That part is not published anywhere, and it is the part we negotiate.</p>
    </div>
      <aside class="vidx-stats" id="vidx-stats" aria-label="{city} venue index at a glance"></aside>
    </div>

    <div class="vidx-scope">
      <p><b>What is in this index, and what is not.</b> This is not every venue in {city}. It is the {n} that a {city} conference brief for 100 or more delegates realistically lands on: every convention and conference centre, the major hotel ballrooms, and the large dedicated event venues. Inclusion is our judgement, built from what we actually book. <b>No venue pays to appear here, and none is left out for not paying</b>, which is why the largest venue in the city is in this index. We add venues as we verify them.</p>
    </div>

    <div class="vidx" id="vidx" data-city="{city}">
      <div class="vidx-controls">
        <div class="vidx-ctl"><label for="vidx-cap">Minimum capacity</label>
          <select id="vidx-cap"><option value="0">Any size</option><option value="50">50+</option><option value="100">100+</option><option value="200">200+</option><option value="400">400+</option><option value="800">800+</option><option value="1500">1,500+</option></select></div>
        <div class="vidx-ctl"><label for="vidx-setup">Room setup</label>
          <select id="vidx-setup"><option value="th">Theatre</option><option value="bq">Banquet</option><option value="cab">Cabaret</option><option value="cl">Classroom</option><option value="ck">Cocktail</option></select></div>
        <div class="vidx-ctl"><label for="vidx-prec">Precinct</label>
          <select id="vidx-prec"><option value="">All precincts</option></select></div>
        <div class="vidx-ctl"><label for="vidx-type">Venue type</label>
          <select id="vidx-type"><option value="">Any type</option><option value="conv">Convention centre</option><option value="hotel">Hotel</option><option value="event">Dedicated event venue</option></select></div>
        <button class="vidx-reset" id="vidx-reset" type="button">Reset filters</button>
      </div>

      <div class="vidx-count" id="vidx-count" role="status" aria-live="polite"></div>
      <p class="vidx-sortnote">Sorted by capacity. Use the filters above to narrow the list.</p>

      <div class="vidx-scroll">
        <table class="vidx-table">
          <caption class="sr-only">{city} conference and event venues with published capacities, sortable by venue, precinct, capacity, meeting rooms and guest rooms. Each row expands to a full specification.</caption>
          <colgroup><col class="c-name"><col class="c-prec"><col class="c-cap"><col class="c-bq"><col class="c-br"><col class="c-gr"><col class="c-suit"><col class="c-enq"></colgroup>
          <thead><tr>
            <th scope="col" class="is-sortable" data-k="n" tabindex="0" role="button" aria-sort="none">Venue<span class="vidx-arr" aria-hidden="true">&#8597;</span></th>
            <th scope="col" class="is-sortable" data-k="pr" tabindex="0" role="button" aria-sort="none">Precinct<span class="vidx-arr" aria-hidden="true">&#8597;</span></th>
            <th scope="col" class="is-sortable num" data-k="cap" tabindex="0" role="button" aria-sort="descending">Largest space<span class="vidx-arr" aria-hidden="true">&#8595;</span></th>
            <th scope="col" class="is-sortable num" data-k="ceil" tabindex="0" role="button" aria-sort="none">Ceiling<span class="vidx-arr" aria-hidden="true">&#8597;</span></th>
            <th scope="col" class="is-sortable num" data-k="br" tabindex="0" role="button" aria-sort="none">Meeting rooms<span class="vidx-arr" aria-hidden="true">&#8597;</span></th>
            <th scope="col" class="is-sortable num" data-k="gr" tabindex="0" role="button" aria-sort="none">Guest rooms<span class="vidx-arr" aria-hidden="true">&#8597;</span></th>
            <th scope="col">Suited to</th>
            <th scope="col"><span class="sr-only">Full specification and enquiry</span></th>
          </tr></thead>
          <tbody id="vidx-body"></tbody>
        </table>
      </div>

      <div class="vidx-method">
        <h3 class="vidx-method__h">How this index is built</h3>
        <p>Every figure is the venue's own published capacity for the space named, read from that venue's own capacity chart, fact sheet, floor plan or technical specification. <b>Last checked {verified}.</b> Where a venue publishes nothing for a setup we print "Not published" rather than estimate it, which is why some cells are empty: ceiling heights are published by {nceil} of the {n}, and a second space is named by {nsecond}.</p>
        <p>Capacities are ceilings, not plans. Staging, catering, AV and dance floors all take seats out of a room, so read these as the most the space has ever been sold at. <b>We do not publish rates</b>, because the rate you are offered depends on your dates, your room nights and who is asking. That is the part we negotiate for you, and it is free to you either way.</p>
      </div>
    </div>
  </div>
</section>
'''.format(city=CITY, n=len(VENUES), verified=VERIFIED, nceil=n_ceil, nsecond=n_second)

island_tag = '<script type="application/json" id="vidx-data">%s</script>' % island
comment = ("<!-- Venue index source register. Every figure above is read off the venue's own\n"
           "     published capacity chart, fact sheet, floor plan or technical spec.\n"
           "     Last checked %s. Re-check before any rebrand or refurbishment.\n"
           "     Generator and data: _venue-index-source/\n\n%s\n-->" % (VERIFIED, srcs))

io.open('/tmp/cvbs2/section.html','w').write(SECTION)
io.open('/tmp/cvbs2/island.html','w').write(island_tag)
io.open('/tmp/cvbs2/schema.html','w').write('<script type="application/ld+json">%s</script>' % json.dumps(schema, ensure_ascii=False))
io.open('/tmp/cvbs2/comment.html','w').write(comment)
print("section", len(SECTION), "island", len(island_tag), "| ceilings", n_ceil, "second rooms", n_second)
