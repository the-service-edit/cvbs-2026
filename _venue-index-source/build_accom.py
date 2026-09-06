#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build conference-venues-with-accommodation.html.

    python3 _venue-index-source/build_accom.py

WHY THIS PAGE AND NOT TEN OTHERS
    The brief asked for pages built around decision criteria rather than
    keyword repetition, and listed eight candidates. Seven of them were
    rejected, and the reasons are worth keeping:

      "best venue for 300 delegates"      an arbitrary number. The Sydney index
                                          already bands by size, and a page per
                                          number is a doorway farm.
      "large conference venues"           the Sydney index's top band already
                                          does this, on the same data, on a page
                                          that already ranks.
      "venues near Sydney Airport"        one venue in the data. A page of one
                                          is not a page.
      "venues with breakout rooms"        we publish an event room count, not a
                                          breakout room count. Those are not the
                                          same thing and pretending otherwise is
                                          inventing data.
      "venues for executive retreats"     no field in the data supports it.
      "venues suitable for exhibitions"   floor load and rigging are what decide
                                          this and we publish neither.
      "residential conference venues"     the same query as this page, so it is
                                          this page, not a second one.

    What survived is the one question the data can answer better than anybody
    else publishes it: can this building hold my plenary AND my delegates. Two
    numbers, side by side. Cvent, VenueNow and Tagvenue all publish both figures
    and none of them puts them together, because a marketplace sells rooms one
    at a time.

THE HONESTY CONSTRAINT
    Guest room counts are the hotel's total inventory, not availability on any
    date, and the page says so in the copy rather than implying a room block is
    there for the taking. No ratio of delegates to rooms is asserted, because
    single and twin share and partner nights vary by program and we would be
    making it up.
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'faq.html')
DATA = os.path.join(ROOT, 'assets', 'data', 'venues.json')
BASE = 'https://the-service-edit.github.io/cvbs-2026/'
PATH = 'conference-venues-with-accommodation.html'

src = io.open(SRC, encoding='utf-8').read()
chrome = src[src.index('<body>'):src.index('<main')]
footer = src[src.index('<footer class="site-footer">'):src.index('</footer>') + 9]
_ent_m = re.search(r'<script type="application/ld\+json" id="cvbs-entity">(.*?)</script>',
                   src, re.S)
_ent = json.loads(_ent_m.group(1))
_ent['@graph'] = [n for n in _ent['@graph'] if n.get('@type') != 'WebPage']
entity = ('<script type="application/ld+json" id="cvbs-entity">' +
          json.dumps(_ent, ensure_ascii=False, separators=(',', ':')) + '</script>')

payload = json.loads(io.open(DATA, encoding='utf-8').read())
ROWS = [v for v in payload['venues'] if v.get('gr')]
ROWS.sort(key=lambda v: (v['city'], -(v.get('th') or v.get('maxcap') or 0)))

ARROW = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
         'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')
HEART = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" '
         'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M20.8 6.6a5 5 0 0 0-7.1 0L12 8.3l-1.7-1.7a5 5 0 1 0-7.1 7.1l8.8 8.8 8.8-8.8a5 5 0 0 0 0-7.1z"/></svg>')

REGION = {'Sydney': 'NSW', 'Melbourne': 'VIC', 'Brisbane': 'QLD', 'Perth': 'WA'}


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


def n(x):
    return '{:,}'.format(x)


def plen(v):
    if v.get('th'):
        return v['th'], 'theatre'
    for k, w in (('bq', 'banquet'), ('ck', 'cocktail'), ('cl', 'classroom'), ('bd', 'boardroom')):
        if v.get(k):
            return v[k], w
    return None, None


def row(v):
    cap, word = plen(v)
    left = ('%s <span>%s</span>' % (n(cap), word)) if cap else '<em>Not published</em>'
    name = esc(v['n'])
    if v.get('visit'):
        name = '<a href="venue-visits/%s/">%s</a>' % (esc(v['visit']), name)
    tags = ''
    if v.get('visit'):
        tags += '<span class="vf-tag vf-tag--seen">Inspected by CVBS</span>'
    if v.get('worked'):
        tags += '<span class="vf-tag vf-tag--worked">We have booked it</span>'
    return '''      <li class="vres">
        <div class="vres__n"><h4>{name}</h4><p>{pr}</p>{tags}</div>
        <div class="vres__pair">
          <div class="vres__f"><b>{left}</b><span>largest room{sp}</span></div>
          <div class="vres__f"><b>{gr}</b><span>guest rooms</span></div>
        </div>
        <div class="vres__act">
          <button class="vf-save" type="button" data-save="{id}" data-name="{plain}" aria-pressed="false">{heart}<span>Save to your shortlist</span></button>
        </div>
      </li>'''.format(name=name, pr=esc(v['pr']), tags=tags, left=left, gr=n(v['gr']),
                      sp=(', ' + esc(v['sp'])) if v.get('sp') else '',
                      id=esc(v['id']), plain=esc(v['n']), heart=HEART)


def main():
    cities = []
    for c in sorted(set(v['city'] for v in ROWS)):
        vs = [v for v in ROWS if v['city'] == c]
        cities.append((c, vs))
    cities.sort(key=lambda kv: -len(kv[1]))

    # Facts stated in the answer block, all read off the data at build time so
    # the sentence and the list can never drift apart.
    biggest = max(ROWS, key=lambda v: (v.get('th') or 0))
    most_rooms = max(ROWS, key=lambda v: v['gr'])
    both = [v for v in ROWS if (v.get('th') or 0) >= 500 and v['gr'] >= 500]
    both.sort(key=lambda v: -(v.get('th') or 0))

    blocks = ''
    for c, vs in cities:
        blocks += '''    <h3 class="vcx__band">{c} <span>{k} {w}</span></h3>
    <ul class="vres-list">
{rows}
    </ul>
'''.format(c=c, k=len(vs), w='venue' if len(vs) == 1 else 'venues',
           rows='\n'.join(row(v) for v in vs))

    # Every venue that clears the bar is named. A count in the sentence and a
    # shorter list under it would be a quiet lie the moment the data grows.
    # Rooms on site but no published count: real accommodation the page
    # cannot list, and the reason the headline number is not the whole story.
    uncounted = sum(1 for v in payload['venues']
                    if v.get('acc') == 'yes' and not v.get('gr'))
    both_line = ', '.join('%s (%s theatre, %s rooms)' % (v['n'], n(v['th']), n(v['gr']))
                          for v in both)

    faqs = [
        ('What is a residential conference venue?',
         'A venue that holds your sessions and your delegates on the same site, so nobody '
         'has to be moved between a conference centre and a hotel. In practice that means a '
         'hotel or resort with a function floor, rather than a convention centre.'),
        ('How many Australian venues does CVBS publish with rooms on site?',
         '%d, across %s. Every guest room count is the number the venue publishes for its own '
         'inventory.' % (len(ROWS), ', '.join(c for c, _ in cities))),
        ('Which Australian venues hold both a large plenary and a large room block?',
         'On the figures we publish, %s.' % both_line),
        ('Does a published room count mean the rooms are available?',
         'No. The number is the hotel\'s total inventory, not what it can release for your '
         'dates. A hotel with 500 rooms may be able to block 80 of them in March and 300 in '
         'July. That is one of the first things we find out for you, and it is the reason a '
         'room count on any website, including ours, is a starting point rather than an answer.'),
        ('How many rooms will my conference actually need?',
         'It depends on how many delegates are travelling, whether they are in single or twin '
         'share, and how many partner nights you are covering. We would rather ask you than '
         'publish a rule of thumb, because the rule of thumb is what causes a shortfall on the '
         'second night.'),
        ('Can CVBS negotiate the room rate and the day delegate rate together?',
         'Yes, and that is usually where the value is. A venue looks at the whole piece of '
         'business, so the room nights and the conference are worth more to it together than '
         'either is alone. It costs you nothing: the venue pays our commission from the budget '
         'it already holds, at the same rate whether you come through us or direct.'),
    ]
    faq_html = ''.join('<details class="faq"><summary>%s</summary><div><p>%s</p></div></details>'
                       % (q, a) for q, a in faqs)

    title = 'Conference Venues With Accommodation On Site, Australia | CVBS'
    desc = ('%d Australian conference and event venues that publish a guest-room count on site, '
            'with the largest room capacity and the room count each venue publishes. '
            'For residential conferences and multi day programs.' % len(ROWS))

    items = []
    for i, v in enumerate(ROWS, 1):
        props = [{"@type": "PropertyValue", "name": "Guest rooms", "value": v['gr']}]
        if v.get('area'):
            props.append({"@type": "PropertyValue", "name": "Largest space floor area",
                          "value": v['area'], "unitCode": "MTK"})
        if v.get('br'):
            props.append({"@type": "PropertyValue", "name": "Event rooms", "value": v['br']})
        ev = {"@type": "EventVenue", "name": v['n'],
              "address": {"@type": "PostalAddress", "addressLocality": v['pr'],
                          "addressRegion": REGION.get(v['city'], ''), "addressCountry": "AU"}}
        cap, _w = plen(v)
        if cap:
            ev["maximumAttendeeCapacity"] = cap
        if v.get('visit'):
            ev["url"] = BASE + 'venue-visits/' + v['visit'] + '/'
        ev["additionalProperty"] = props
        items.append({"@type": "ListItem", "position": i, "item": ev})

    ld = lambda o: ('<script type="application/ld+json">' +
                    json.dumps(o, ensure_ascii=False, separators=(',', ':')) + '</script>\n')

    schema = ld({"@context": "https://schema.org", "@type": "ItemList",
                 "name": "Australian conference venues with accommodation on site",
                 "description": ("The %d Australian conference and event venues listed on this "
                                 "page that publish a guest-room count on site, with the "
                                 "largest published room capacity and the guest room count for "
                                 "each. Every figure is read from the venue's own published "
                                 "material." % len(items)),
                 "numberOfItems": len(items),
                 "itemListElement": items})
    schema += ld({"@context": "https://schema.org", "@type": "FAQPage",
                  "mainEntity": [{"@type": "Question", "name": q,
                                  "acceptedAnswer": {"@type": "Answer", "text": a}}
                                 for q, a in faqs]})
    schema += ld({"@context": "https://schema.org", "@type": "BreadcrumbList",
                  "itemListElement": [
                      {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
                      {"@type": "ListItem", "position": 2, "name": "Venue results",
                       "item": BASE + 'venue-results.html'},
                      {"@type": "ListItem", "position": 3,
                       "name": "Venues with accommodation", "item": BASE + PATH}]})

    head = '''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{base}{path}">
<meta name="theme-color" content="#0A2C52">
<meta property="og:type" content="website">
<meta property="og:site_name" content="CVBS, Worldwide Venue Finding Solutions">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{base}{path}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.png?v=202608131600" type="image/png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png?v=202608131600">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/finder.css?v=202609060900">
<link rel="stylesheet" href="assets/css/site.css?v=202609061800">
{entity}
{schema}</head>
'''.format(title=title, desc=desc, base=BASE, path=PATH, entity=entity, schema=schema)

    body = '''<main id="main">

<section class="page-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><b style="color:inherit;font-weight:500">With accommodation</b></nav>
    <span class="eyebrow" style="margin-top:1.2rem">Residential conferences</span>
    <h1>Venues where your delegates sleep on site.</h1>
    <p class="lead">Two numbers decide a residential program: how many people the main room holds, and how many beds are upstairs. Here they are side by side, for the {k} venues we publish that have both.</p>
  </div>
</section>

<section class="s-stone pad">
  <div class="wrap">
    <div class="vidx-answer answer-solo">
      <span class="vidx-answer__tag">In short</span>
      <p><b>{k} of the {tot} Australian venues we publish put a number on their guest rooms on site.</b> Another {uncounted} have rooms on site without publishing a count, so they are not listed here and are not excluded from a search. The largest of them for a plenary is {big} at {bigcap} theatre, and the largest for accommodation is {mr} at {mrrooms} rooms. Where a program needs both at scale the field narrows sharply: {both_n} venues we publish seat 500 or more in one room and hold 500 or more guest rooms, and they are {both_line}.</p>
      <p><b>A published room count is inventory, not availability.</b> A hotel with 500 rooms might release 80 for your March dates and 300 for your July ones, and no website can tell you which. That is the first thing we find out, along with what the venue will do on the day delegate rate when the room nights come with it. <a href="submit-a-brief.html">Tell us your dates</a> and we will come back with both.</p>
    </div>
  </div>
</section>

<section class="s-white pad">
  <div class="wrap">
    <span class="eyebrow">The venues</span>
    <h2 class="h2">Largest room, and the rooms above it.</h2>
    <p class="lead" style="max-width:64ch">Grouped by city, largest plenary first. Every figure is the one the venue publishes for itself.</p>
    <p style="margin-top:1rem"><a class="link-arrow" href="venue-results.html?accom=yes" style="color:var(--teal-ink)">Narrow these by your own numbers and layout {arrow}</a></p>
    <div class="vcx" style="margin-top:2rem">
{blocks}
    </div>
    <p class="vcx__foot">Guest room counts are each venue's published total inventory. Largest room figures are the venue's own published capacity for its biggest space, in the layout named. Where a venue publishes no theatre figure we show the largest layout it does publish and say which one. This is not every venue in Australia with rooms on site. It is the part of what we know that we can put a source against.</p>
  </div>
</section>

<section class="s-stone pad">
  <div class="wrap wrap--narrow">
    <span class="eyebrow">Common questions</span>
    <h2 class="h2">Residential conferences, answered</h2>
    <div style="margin-top:2rem">{faqs}</div>
  </div>
</section>

<section class="cta-band pad">
  <div class="wrap" style="text-align:center">
    <h2 class="h2">Tell us the dates and the numbers.</h2>
    <p class="lead" style="max-width:56ch;margin:1rem auto 0">We will find out what each of these can actually release on your dates, and what it will do on the rate when the conference and the rooms come together.</p>
    <div class="btn-row" style="justify-content:center;margin-top:2rem">
      <a class="btn btn--teal" href="submit-a-brief.html">Start your brief {arrow}</a>
      <a class="btn btn--ghost-light" href="venue-results.html">Look at every venue we publish</a>
    </div>
  </div>
</section>
</main>

<div class="vf-tray" id="vf-tray" role="region" aria-label="Your shortlist">
  <div class="vf-tray__in">
    <div>
      <p class="vf-tray__n" data-tray-n></p>
      <p class="vf-tray__names" data-tray-names></p>
    </div>
    <div class="vf-tray__acts">
      <a class="btn btn--teal" data-tray-send href="submit-a-brief.html">Ask CVBS about these {arrow}</a>
      <a class="btn btn--light" data-tray-review href="venue-results.html?view=saved">Review shortlist</a>
      <button class="btn btn--ghost-light" type="button" data-tray-clear>Clear</button>
    </div>
  </div>
</div>
'''.format(k=len(ROWS), tot=payload['meta']['count'], blocks=blocks, faqs=faq_html,
           arrow=ARROW, big=biggest['n'], bigcap=n(biggest['th']),
           mr=most_rooms['n'], mrrooms=n(most_rooms['gr']),
           uncounted=uncounted,
           both_n=len(both), both_line=both_line)

    html = (head + chrome + body + footer +
            '\n<script src="assets/js/site.js?v=202609060900" defer></script>'
            '\n<script src="assets/js/finder.js?v=202609061800" defer></script>'
            '\n</body>\n</html>\n')
    io.open(os.path.join(ROOT, PATH), 'w', encoding='utf-8').write(html)
    print('wrote %s  %d venues across %d cities  %d bytes'
          % (PATH, len(ROWS), len(cities), len(html)))
    print('  answer block facts: largest plenary %s %s theatre, most rooms %s %s'
          % (biggest['n'], n(biggest['th']), most_rooms['n'], n(most_rooms['gr'])))
    print('  both at 500+: %s' % (both_line or 'none'))


if __name__ == '__main__':
    main()
