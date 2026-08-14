# -*- coding: utf-8 -*-
import json, sys, io, re
sys.path.insert(0, '/tmp/cvbs/build')
from venues_sydney import VENUES, CITY

# ---- JSON data island (compact, only what the renderer needs) -------------
keys = ['n','sp','pr','ty','th','bq','cl','ck','br','gr','note']
data = [{k: v[k] for k in keys} for v in VENUES]
island = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

# ---- schema.org ItemList with real capacity ------------------------------
items = []
for i, v in enumerate(VENUES, 1):
    ev = {
        "@type": "EventVenue",
        "name": v['n'],
        "maximumAttendeeCapacity": v['th'],
        "address": {"@type": "PostalAddress", "addressLocality": v['pr'],
                    "addressRegion": "NSW", "addressCountry": "AU"},
    }
    items.append({"@type": "ListItem", "position": i, "item": ev})
schema = {"@context": "https://schema.org", "@type": "ItemList",
          "name": "Conference and event venue capacity index, %s" % CITY,
          "description": "Published theatre, banquet, classroom and cocktail capacities for %d major %s conference and event venues, with meeting room and guest room counts." % (len(VENUES), CITY),
          "numberOfItems": len(VENUES),
          "itemListOrder": "https://schema.org/ItemListOrderDescending",
          "itemListElement": items}
schema_js = json.dumps(schema, ensure_ascii=False)

# ---- source register, kept in an HTML comment for CVBS ---------------------
srcs = "\n".join("     %-38s %s" % (v['n'], v['src']) for v in VENUES)

SECTION = '''<section class="s-stone pad" id="venue-index">
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">{city} venue index</span>
      <h2 class="h2">Every major {city} conference venue, and what it actually holds.</h2>
      <p class="lead">Published capacities for {n} {city} venues, filterable by size, setup, precinct and type. The numbers venues rarely put in one place, in one place.</p></div>

    <div class="vidx-answer">
      <span class="vidx-answer__tag">The short answer</span>
      <p><b>{city}'s largest conference venue is ICC Sydney at Darling Harbour.</b> Its Grand Ballroom seats 2,784 theatre style and is, on ICC's own description, the largest ballroom in Australia. Beside it sit a 2,500 seat tiered theatre, an 8,000 seat plenary theatre and 32,600 square metres of exhibition halls.</p>
      <p><b>Above 2,000 delegates seated in one room, {city} has four options and none of them is a hotel.</b> Sydney Showground's Dome at Olympic Park takes 7,000, ICC Sydney's Grand Ballroom 2,784, the Sydney Opera House Concert Hall 2,102 facing the stage, and Sydney Town Hall's Centennial Hall 2,008 across the floor and galleries. The Hordern Pavilion at Moore Park holds 3,500 standing and 1,400 for dinner.</p>
      <p><b>Between 500 and 1,500 delegates the constraint becomes accommodation.</b> The Fullerton Hotel Sydney's Grand Ballroom holds 1,400 theatre across 1,058 pillarless square metres and is the largest pillarless hotel ballroom in the city. Hilton Sydney at 1,100 and Hyatt Regency Sydney at 1,000, with 878 guest rooms, are the only other Sydney hotels that seat more than 1,000 in a single room.</p>
      <p><b>Below 400 delegates the CBD carries the deepest supply</b>, with more than a dozen conference hotels inside a ten minute walk of Wynyard and Town Hall. At that size the constraint is rarely capacity. It is availability on your dates, and the rate you are quoted. That part is not published anywhere, and it is the part we negotiate.</p>
    </div>

    <div class="vidx" id="vidx" data-city="{city}">
      <div class="vidx-controls">
        <div class="vidx-ctl"><label for="vidx-cap">Minimum capacity</label>
          <select id="vidx-cap"><option value="0">Any size</option><option value="50">50+</option><option value="100">100+</option><option value="200">200+</option><option value="400">400+</option><option value="800">800+</option><option value="1500">1,500+</option></select></div>
        <div class="vidx-ctl"><label for="vidx-setup">Room setup</label>
          <select id="vidx-setup"><option value="th">Theatre</option><option value="bq">Banquet</option><option value="cl">Classroom</option><option value="ck">Cocktail</option></select></div>
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
          <caption class="sr-only">{city} conference and event venues with published capacities, sortable by venue, precinct, capacity, meeting rooms and guest rooms.</caption>
          <thead><tr>
            <th scope="col" class="is-sortable" data-k="n" tabindex="0" role="button" aria-sort="none">Venue<span class="vidx-arr" aria-hidden="true">&#8597;</span></th>
            <th scope="col" class="is-sortable" data-k="pr" tabindex="0" role="button" aria-sort="none">Precinct<span class="vidx-arr" aria-hidden="true">&#8597;</span></th>
            <th scope="col" class="is-sortable num" data-k="cap" tabindex="0" role="button" aria-sort="descending">Largest space<span class="vidx-arr" aria-hidden="true">&#8595;</span></th>
            <th scope="col" class="is-sortable num" data-k="bq" tabindex="0" role="button" aria-sort="none">Banquet<span class="vidx-arr" aria-hidden="true">&#8597;</span></th>
            <th scope="col" class="is-sortable num" data-k="br" tabindex="0" role="button" aria-sort="none">Meeting rooms<span class="vidx-arr" aria-hidden="true">&#8597;</span></th>
            <th scope="col" class="is-sortable num" data-k="gr" tabindex="0" role="button" aria-sort="none">Guest rooms<span class="vidx-arr" aria-hidden="true">&#8597;</span></th>
            <th scope="col">Suited to</th>
            <th scope="col"><span class="sr-only">Enquire</span></th>
          </tr></thead>
          <tbody id="vidx-body"></tbody>
        </table>
      </div>

      <p class="vidx-note"><b>How to read this.</b> Every figure is the venue's own published capacity for its largest single space, checked in August 2026. Where a venue does not publish a figure we say so rather than estimate it. Capacities move with staging, catering and AV, so treat these as the ceiling, not the plan. <b>We do not publish rates</b>, because the rate you are actually offered depends on your dates, your room nights and who is asking. That is the part we negotiate for you, and it is free to you either way.</p>
    </div>
  </div>
</section>
'''.format(city=CITY, n=len(VENUES))

island_tag = '<script type="application/json" id="vidx-data">%s</script>' % island
comment = ("<!-- Venue index source register. Every capacity above is read off the venue's\n"
           "     own published capacity chart. Last checked 14 August 2026.\n"
           "     Re-check before any rebrand, refurbishment or annual copy review.\n\n"
           "%s\n-->" % srcs)

open('/tmp/cvbs/build/section.html','w').write(SECTION)
open('/tmp/cvbs/build/island.html','w').write(island_tag)
open('/tmp/cvbs/build/schema.html','w').write('<script type="application/ld+json">%s</script>' % schema_js)
open('/tmp/cvbs/build/comment.html','w').write(comment)
print("section", len(SECTION), "island", len(island_tag), "schema", len(schema_js))
