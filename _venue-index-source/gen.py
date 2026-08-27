# -*- coding: utf-8 -*-
import json, sys, io
sys.path.insert(0, '/tmp/cvbs2')
from venues_sydney import VENUES, CITY

VERIFIED = "14 August 2026"

keys = ['n','sp','pr','ty','th','bq','cl','ck','cab','ush','bd','br','gr',
        'area','ceil','ceilq','s_name','s_th','note','worked','seen','visit']

# ---- site visit records ------------------------------------------------------
# visit records live in site_visits.json, NOT in venues_sydney.py, so that the
# photo intake script can rewrite them without ever touching the verified
# capacity data. Written by scripts/site-visit-intake.py. Hand editing is fine
# for captions and the note, never for the date: the date comes off the
# photograph's own metadata, which is the whole point of the record.
import os
VISITS = {}
for _c in (os.path.dirname(os.path.abspath(__file__)), '/tmp/cvbs2', '.',
           os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_venue-index-source')):
    _p = os.path.join(_c, 'site_visits.json')
    if os.path.exists(_p):
        VISITS = json.load(io.open(_p, encoding='utf-8'))
        print('site visits loaded from', _p)
        break

_city_visits = (VISITS.get('cities') or {}).get(CITY, {})
for v in VENUES:
    rec = _city_visits.get(v['n'])
    v['visit'] = rec or None
    # seen is derived from the visit so the two can never drift apart
    if rec and not v.get('seen'):
        v['seen'] = '%s, %s' % (rec.get('by', 'CVBS'), rec.get('when', ''))

island = json.dumps([{k: v.get(k) for k in keys} for v in VENUES], ensure_ascii=False, separators=(',', ':'))

# ---- schema, and the rule that governs it ------------------------------------
# Google: "Don't mark up content that is not visible to readers of the page."
# The filterable table was removed on 27 Aug 2026, so the ItemList may only
# carry venues the page names in visible copy. VISIBLE is that list. If you add
# a venue to the answer block or the featured section, add it here. If you take
# one out of the copy, take it out here too. Never let this list run ahead of
# the page.
VISIBLE = ["Sydney Showground", "ICC Sydney", "Sydney Opera House", "Sydney Town Hall",
           "The Fullerton Hotel Sydney", "Hilton Sydney", "Hyatt Regency Sydney",
           "Shangri-La Sydney", "W Sydney", "Crown Sydney"]
_by = {v['n']: v for v in VENUES}
_missing = [n for n in VISIBLE if n not in _by]
if _missing:
    raise SystemExit("VISIBLE names not in the data: %s" % _missing)

items = []
for i, v in enumerate([_by[n] for n in VISIBLE], 1):
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
  "name":"Conference and event venues named on this page, %s" % CITY,
  "description":"The %s conference and event venues described on this page, with the theatre capacity, ceiling height, floor area and meeting room count each venue publishes for its largest space. Every figure is read from the venue's own capacity chart, fact sheet, floor plan or technical spec, last checked %s." % (CITY, VERIFIED),
  "numberOfItems":len(items),"itemListOrder":"https://schema.org/ItemListOrderDescending",
  "itemListElement":items}

srcs = "\n".join("     %-44s\n       capacities  %s\n       specs       %s" % (v['n'], v['src'], v['src2']) for v in VENUES)

# ---- Block 1: sits HIGH on the page. Short, visual, citable. -----------------
ANSWER = '''<section class="s-stone pad" id="sydney-at-a-glance">
  <div class="wrap">
    <div class="vidx-lede">
    <div class="vidx-answer">
      <span class="vidx-answer__tag">Sydney, in short</span>
      <p><b>{city}'s largest conference venue is ICC Sydney at Darling Harbour.</b> Its Grand Ballroom seats 2,784 theatre style under a 9 metre ceiling and is, on ICC's own description, the largest ballroom in Australia. Above 2,000 delegates seated in one room the market is small, and none of it is a hotel: Sydney Showground's Dome takes 7,000, the Opera House Concert Hall 2,102, and Sydney Town Hall's Centennial Hall 2,008.</p>
      <p><b>Between 500 and 1,500 delegates the constraint becomes accommodation.</b> The Fullerton Hotel Sydney holds 1,400 theatre across 1,058 pillarless square metres, the largest pillarless hotel ballroom in the city. Hilton Sydney at 1,100 and Hyatt Regency at 1,000 are the only other {city} hotels seating a thousand or more in one room, and Hyatt is the one that can run two at once. Below 400 the CBD carries the deepest supply, and the constraint stops being capacity. It becomes availability on your dates, and the rate. <a href="#sydney-venues">See the venues we know well</a>.</p>
    </div>
      <aside class="vidx-stats" id="vidx-stats" aria-label="{city} at a glance"></aside>
    </div>
  </div>
</section>
'''.format(city=CITY)

# ---- Block 2: the site visit records. --------------------------------------
# REPLACED 27 Aug 2026. This used to be the filterable capacity table with a
# search box, five filters and sortable columns. CVBS asked for it out, and they
# were right: the position is that a shortlist from an algorithm is worth less
# than four people who have been in the room, and the biggest object on the page
# was a search tool. The capacity data still exists in venues_sydney.py, still
# feeds the answer block and the at a glance rail, and can be turned back on.
# What replaced it is the firsthand record, which no competitor can copy.
# The section hides itself while no site visit is logged.
INDEX = '''<section class="s-white pad" id="rooms-we-have-walked" data-visit-section hidden>
  <div class="wrap">
    <div class="section-head"><span class="eyebrow">{city} site visits</span>
      <h2 class="h2">The rooms we have stood in.</h2>
      <p class="lead">Not a list of everything in {city}. The rooms one of us has walked, when we were there, and what we noticed that a floor plan will not tell you.</p></div>

    <div class="vidx" id="vidx" data-city="{city}">
      <div class="vidx-recent" id="vidx-recent" hidden></div>
    </div>

    <p class="vidx-method vidx-method--seen"><b>The part a capacity chart cannot tell you.</b> A floor plan will give you the square metres. It will not tell you where the pre-function space bottlenecks once the room is full, which loading dock your production crew will struggle with, or how the light falls in the ballroom at four in the afternoon. That is what we are for, and it is the reason we walk these rooms rather than read about them.</p>
  </div>
</section>
'''.format(city=CITY)

io.open('/tmp/cvbs2/answer.html','w').write(ANSWER)
io.open('/tmp/cvbs2/index.html','w').write(INDEX)
io.open('/tmp/cvbs2/island.html','w').write('<script type="application/json" id="vidx-data">%s</script>' % island)
io.open('/tmp/cvbs2/schema.html','w').write('<script type="application/ld+json">%s</script>' % json.dumps(schema, ensure_ascii=False))
io.open('/tmp/cvbs2/comment.html','w').write(
    "<!-- Venue index source register. Every figure is read off the venue's own published\n"
    "     capacity chart, fact sheet, floor plan or technical spec. Last checked %s.\n"
    "     Generator and data: _venue-index-source/\n\n%s\n-->" % (VERIFIED, srcs))
print("answer", len(ANSWER), "index", len(INDEX), "island", len(island), "venues", len(VENUES))
