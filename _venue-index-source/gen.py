# -*- coding: utf-8 -*-
import json, sys, io
sys.path.insert(0, '/tmp/cvbs2')
from venues_sydney import VENUES, CITY

VERIFIED = "14 August 2026"

keys = ['n','sp','pr','ty','th','bq','cl','ck','cab','ush','bd','br','gr',
        'area','ceil','ceilq','s_name','s_th','note','worked','seen']
island = json.dumps([{k: v[k] for k in keys} for v in VENUES], ensure_ascii=False, separators=(',', ':'))

items = []
for i, v in enumerate(VENUES, 1):
    props = []
    if v['area']: props.append({"@type":"PropertyValue","name":"Largest space floor area","value":v['area'],"unitCode":"MTK"})
    if v['ceil']: props.append({"@type":"PropertyValue","name":"Largest space ceiling height","value":v['ceil'],"unitCode":"MTR"})
    if v['br']:   props.append({"@type":"PropertyValue","name":"Meeting rooms","value":v['br']})
    ev = {"@type":"EventVenue","name":v['n'],
          "address":{"@type":"PostalAddress","addressLocality":v['pr'],"addressRegion":"NSW","addressCountry":"AU"}}
    if v['th']: ev["maximumAttendeeCapacity"] = v['th']
    if props: ev["additionalProperty"] = props
    items.append({"@type":"ListItem","position":i,"item":ev})
schema = {"@context":"https://schema.org","@type":"ItemList",
  "name":"Conference and event venue capacity index, %s" % CITY,
  "description":"Published theatre, banquet, classroom, cabaret and cocktail capacities for the principal %s conference and event venues, with ceiling heights, floor areas, meeting room and guest room counts. Verified %s." % (CITY, VERIFIED),
  "numberOfItems":len(VENUES),"itemListOrder":"https://schema.org/ItemListOrderDescending",
  "itemListElement":items}

srcs = "\n".join("     %-44s\n       capacities  %s\n       specs       %s" % (v['n'], v['src'], v['src2']) for v in VENUES)

# ---- Block 1: sits HIGH on the page. Short, visual, citable. -----------------
ANSWER = '''<section class="s-stone pad" id="sydney-at-a-glance">
  <div class="wrap">
    <div class="vidx-lede">
    <div class="vidx-answer">
      <span class="vidx-answer__tag">Sydney, in short</span>
      <p><b>{city}'s largest conference venue is ICC Sydney at Darling Harbour.</b> Its Grand Ballroom seats 2,784 theatre style under a 9 metre ceiling and is, on ICC's own description, the largest ballroom in Australia. Above 2,000 delegates seated in one room the market is small, and none of it is a hotel: Sydney Showground's Dome takes 7,000, the Opera House Concert Hall 2,102, and Sydney Town Hall's Centennial Hall 2,008.</p>
      <p><b>Between 500 and 1,500 delegates the constraint becomes accommodation.</b> The Fullerton Hotel Sydney holds 1,400 theatre across 1,058 pillarless square metres, the largest pillarless hotel ballroom in the city. Hilton Sydney at 1,100 and Hyatt Regency at 1,000 are the only other {city} hotels seating more than 1,000 in one room, and Hyatt is the one that can run two at once. Below 400 the CBD carries the deepest supply, and the constraint stops being capacity. It becomes availability on your dates, and the rate. <a href="#venue-index">See the room by room numbers</a>.</p>
    </div>
      <aside class="vidx-stats" id="vidx-stats" aria-label="{city} at a glance"></aside>
    </div>
  </div>
</section>
'''.format(city=CITY)

# ---- Block 2: sits BELOW the featured venues. The working tool. --------------
INDEX = '''<section class="s-white pad" id="venue-index">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">{city} venue index</span>
      <h2 class="h2">The {city} rooms we know, and what they actually hold.</h2>
      <p class="lead">Published capacities, ceiling heights and floor areas. Filter by size, setup, precinct and type.</p></div>

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
          <caption class="sr-only">{city} conference and event venues with published capacities, sortable by venue, precinct, capacity, ceiling height, meeting rooms and guest rooms. Each row expands to a full specification.</caption>
          <colgroup><col class="c-name"><col class="c-prec"><col class="c-cap"><col class="c-ceil"><col class="c-br"><col class="c-gr"><col class="c-suit"><col class="c-enq"></colgroup>
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

      <p class="vidx-method">Every figure is the venue's own published capacity for the space named, read from that venue's own capacity chart, floor plan or technical spec, and last checked {verified}. Where a venue publishes nothing we say so rather than estimate. Capacities are ceilings, not plans. <b>Venues appear here on suitability alone.</b> We do not publish rates, because the rate you are offered depends on your dates and your room nights. That is the part we negotiate, and it is free to you.</p>
    </div>
  </div>
</section>
'''.format(city=CITY, verified=VERIFIED)

io.open('/tmp/cvbs2/answer.html','w').write(ANSWER)
io.open('/tmp/cvbs2/index.html','w').write(INDEX)
io.open('/tmp/cvbs2/island.html','w').write('<script type="application/json" id="vidx-data">%s</script>' % island)
io.open('/tmp/cvbs2/schema.html','w').write('<script type="application/ld+json">%s</script>' % json.dumps(schema, ensure_ascii=False))
io.open('/tmp/cvbs2/comment.html','w').write(
    "<!-- Venue index source register. Every figure is read off the venue's own published\n"
    "     capacity chart, fact sheet, floor plan or technical spec. Last checked %s.\n"
    "     Generator and data: _venue-index-source/\n\n%s\n-->" % (VERIFIED, srcs))
print("answer", len(ANSWER), "index", len(INDEX), "island", len(island), "venues", len(VENUES))
