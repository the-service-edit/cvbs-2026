#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish the full venue index onto a destination page, as a reference, not a tool.

    python3 _venue-index-source/build_city_index.py Sydney

WHAT THIS IS, AND WHY IT IS NOT THE TABLE THAT WAS REMOVED
    On 27 August 2026 the filterable capacity table came off the Sydney page,
    and that was the right call. It was a search box with a sort order sitting
    as the largest object on the flagship page, which is the algorithm CVBS's
    whole position argues against.

    This is a different object.
      - It has no search box, no filters and no sort controls. It cannot be
        rearranged by the reader. It is a published reference.
      - It is not the largest thing on the page. It sits below the featured
        venues and below the venues we have walked through, so the photography
        and the firsthand work still lead.
      - It is organised by the decision, not by the data. The bands are the
        question an organiser actually arrives with, which is how many people
        are coming, and each venue carries CVBS's own sentence about what the
        building is for. That sentence is the part no marketplace has.

    The filtering tool lives on venue-results.html, which is noindex, exactly
    so that this page can stay a page and that page can stay a tool.

WHAT IT FIXES
    Before this, the answer block at the top of the Sydney page asserted facts
    about venues the page never showed, and 45 of 55 venues in the dataset were
    invisible to a reader and to an answer engine. The ItemList had to be
    trimmed to the ten venues named in prose. Now every venue in the schema is
    one a reader can see, at full size, which is what Google's guidance asks
    for and what makes the page worth citing.

GATE
    Only runs for a city with at least MIN_VENUES rows. A "full index" of one
    venue is not an index, it is a venue, and it belongs in the walked through
    section instead.
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'assets', 'data', 'venues.json')
MIN_VENUES = 6

sys.path.insert(0, os.path.join(ROOT, '_venue-index-source'))
from venues_extra import CITY_PAGES

BANDS = [
    (1000, None, 'A thousand delegates and above',
     'The top of the market, and it is small. Above a thousand seated in one room you are choosing '
     'between a handful of buildings, and most of them are not hotels.'),
    (500, 999, 'Five hundred to a thousand',
     'The band where accommodation usually decides it. Plenty of rooms hold the numbers; far fewer '
     'hold the numbers and the delegates in the same building.'),
    (250, 499, 'Two hundred and fifty to five hundred',
     'The deepest supply in the city, and the band where the decision stops being about capacity. '
     'It becomes availability on your dates, and what the venue will do on the rate.'),
    (1, 249, 'Under two hundred and fifty',
     'Board programs, executive meetings, training and private dinners. Smaller rooms, and the '
     'building around them matters more than the seat count.'),
]

SAVE_SVG = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" '
            'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            '<path d="M20.8 6.6a5 5 0 0 0-7.1 0L12 8.3l-1.7-1.7a5 5 0 1 0-7.1 7.1l8.8 8.8 8.8-8.8a5 5 0 0 0 0-7.1z"/></svg>')
ARROW = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
         'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')

SETUP_LABEL = [('th', 'theatre'), ('bq', 'banquet'), ('ck', 'cocktail'),
               ('cl', 'classroom'), ('cab', 'cabaret'), ('bd', 'boardroom')]


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


def n(x):
    return '{:,}'.format(x) if isinstance(x, (int, float)) else x


def venue_row(v, city_file):
    figs = []
    if v.get('th'):
        figs.append(('%s theatre' % n(v['th']), 'in ' + esc(v.get('sp') or 'its largest room')))
    else:
        for k, label in SETUP_LABEL[1:]:
            if v.get(k):
                figs.append(('%s %s' % (n(v[k]), label), 'in ' + esc(v.get('sp') or 'its largest room')))
                break
    if v.get('area'):
        figs.append(('%s sqm' % n(v['area']), 'floor area'))
    if v.get('ceil') and not v.get('ceilq'):
        figs.append(('%s m' % v['ceil'], 'ceiling'))
    elif v.get('ceil') and v.get('ceilq'):
        figs.append(('%s m' % v['ceil'], esc(v['ceilq'])))
    if v.get('gr'):
        figs.append((n(v['gr']), 'guest rooms'))
    if v.get('br'):
        figs.append((n(v['br']), 'event rooms'))
    if v.get('s_name') and v.get('s_th'):
        figs.append(('%s theatre' % n(v['s_th']), 'in ' + esc(v['s_name'])))

    if not figs:
        # The venue publishes nothing we can put a source against. Say so in
        # words rather than leaving a blank box or inventing a figure.
        figs = [('Not published', 'by the venue')]
    figs_html = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (a, b) for a, b in figs)

    tags = ''
    if v.get('visit'):
        tags += '<span class="vf-tag vf-tag--seen">Inspected by CVBS</span>'
    if v.get('worked'):
        tags += '<span class="vf-tag vf-tag--worked">We have booked it</span>'
    if v.get('offer'):
        tags += '<span class="vf-tag vf-tag--offer">Current offer</span>'

    name = esc(v['n'])
    if v.get('visit'):
        name = '<a href="venue-visits/%s/">%s</a>' % (esc(v['visit']), name)

    enq = 'submit-a-brief.html?venue=%s&amp;dest=%s' % (
        v['n'].replace(' ', '%20').replace('&', '%26'), v['city'].replace(' ', '%20'))

    return '''      <li class="vcx__v">
        <div class="vcx__main">
          <h4 class="vcx__n">{name}</h4>
          <p class="vcx__loc">{pr}</p>
          <p class="vcx__note">{note}</p>
          {tags}
        </div>
        <div class="vcx__side">
          <dl class="vcx__figs">{figs}</dl>
          <div class="vcx__acts">
            <button class="vf-save" type="button" data-save="{id}" data-name="{plain}" aria-pressed="false"><span>Save to your shortlist</span>{heart}</button>
            <a class="vcx__enq" href="{enq}">Ask us about it</a>
          </div>
        </div>
      </li>'''.format(name=name, pr=esc(v['pr']), note=esc(v.get('note') or ''),
                      tags=('<div class="vf-tags">%s</div>' % tags) if tags else '',
                      figs=figs_html, id=esc(v['id']), plain=esc(v['n']),
                      heart=SAVE_SVG, enq=enq)


def build(city):
    payload = json.loads(io.open(DATA, encoding='utf-8').read())
    rows = [v for v in payload['venues'] if v['city'] == city]
    if len(rows) < MIN_VENUES:
        sys.exit('%s has %d venues. Below the %d row gate, so no index section is '
                 'published. Add venue data first.' % (city, len(rows), MIN_VENUES))

    page = CITY_PAGES.get(city)
    if not page or not os.path.exists(os.path.join(ROOT, page)):
        sys.exit('No destination page for %s' % city)

    used, blocks = set(), []
    for lo, hi, title, lead in BANDS:
        band = [v for v in rows
                if v.get('th') and v['th'] >= lo and (hi is None or v['th'] <= hi)]
        band.sort(key=lambda v: -v['th'])
        if not band:
            continue
        for v in band:
            used.add(v['id'])
        blocks.append('''    <h3 class="vcx__band">{title}</h3>
    <p class="vcx__bandlead">{lead}</p>
    <ul class="vcx__list">
{rows}
    </ul>'''.format(title=title, lead=lead,
                    rows='\n'.join(venue_row(v, page) for v in band)))

    rest = [v for v in rows if v['id'] not in used]
    rest.sort(key=lambda v: -(v.get('maxcap') or 0))
    if rest:
        for v in rest:
            used.add(v['id'])
        blocks.append('''    <h3 class="vcx__band">No theatre figure published</h3>
    <p class="vcx__bandlead">These venues publish capacities for other layouts but not for theatre seating. We would rather show you the gap than fill it with a number the venue has never put its name to. If one of these is on your list, ask us and we will get the figure from them.</p>
    <ul class="vcx__list">
{rows}
    </ul>'''.format(rows='\n'.join(venue_row(v, page) for v in rest)))

    checked = sorted(set(v.get('checked') for v in rows if v.get('checked')))
    section = '''<section class="s-stone pad" id="{slug}-index">
  <div class="wrap">
    <span class="eyebrow">By delegate numbers</span>
    <h2 class="h2">Every {city} venue we publish, and what each one is for.</h2>
    <p class="lead" style="max-width:66ch">Grouped by the only question you can answer on day one, which is how many people are coming. Every figure is the one the venue publishes for itself, read off its own capacity chart, fact sheet or floor plan. The sentence under each name is ours.</p>
    <p style="margin-top:1rem"><a class="link-arrow" href="venue-results.html?dest={city_q}" style="color:var(--teal-deep)">Narrow these by your numbers and your layout {arrow}</a></p>
    <div class="vcx">
{blocks}
    </div>
    <p class="vcx__foot">Sources last read {checked}. This is not every venue in {city}. It is the part of what we know that we can put a source against, and we book venues every week that are not on it. <a href="submit-a-brief.html?dest={city_q}">Tell us what you are planning</a> and we will go looking.</p>
  </div>
</section>

'''.format(slug=city.lower().replace(' ', '-'), city=city,
           city_q=city.replace(' ', '%20'), arrow=ARROW,
           blocks='\n\n'.join(blocks),
           checked=' and '.join(checked) if checked else 'August 2026')

    # ------------------------------------------------------------- schema
    # Every venue in this list is now visible on the page, so the ItemList may
    # carry all of them. Google: do not mark up content that is not visible to
    # readers. This is the first time that has been true here.
    items = []
    ordered = []
    for lo, hi, _t, _l in BANDS:
        band = [v for v in rows if v.get('th') and v['th'] >= lo and (hi is None or v['th'] <= hi)]
        band.sort(key=lambda v: -v['th'])
        ordered += band
    ordered += rest
    region = {'Sydney': 'NSW', 'Melbourne': 'VIC', 'Brisbane': 'QLD', 'Perth': 'WA',
              'Adelaide': 'SA', 'Canberra': 'ACT', 'Hobart': 'TAS', 'Darwin': 'NT',
              'Gold Coast': 'QLD', 'Sunshine Coast': 'QLD', 'Cairns': 'QLD',
              'Hunter Valley': 'NSW', 'Blue Mountains': 'NSW', 'Byron Bay': 'NSW',
              'Yarra Valley': 'VIC', 'Mornington Peninsula': 'VIC'}.get(city, '')
    for i, v in enumerate(ordered, 1):
        props = []
        if v.get('area'):
            props.append({"@type": "PropertyValue", "name": "Largest space floor area",
                          "value": v['area'], "unitCode": "MTK"})
        if v.get('ceil'):
            props.append({"@type": "PropertyValue", "name": "Largest space ceiling height",
                          "value": v['ceil'], "unitCode": "MTR"})
        if v.get('br'):
            props.append({"@type": "PropertyValue", "name": "Event rooms", "value": v['br']})
        if v.get('gr'):
            props.append({"@type": "PropertyValue", "name": "Guest rooms", "value": v['gr']})
        if v.get('bq'):
            props.append({"@type": "PropertyValue", "name": "Banquet capacity", "value": v['bq']})
        ev = {"@type": "EventVenue", "name": v['n'],
              "address": {"@type": "PostalAddress", "addressLocality": v['pr'],
                          "addressRegion": region, "addressCountry": "AU"}}
        if v.get('th'):
            ev["maximumAttendeeCapacity"] = v['th']
        if v.get('note'):
            ev["description"] = v['note']
        if v.get('visit'):
            ev["url"] = ('https://the-service-edit.github.io/cvbs-2026/venue-visits/%s/'
                         % v['visit'])
        if props:
            ev["additionalProperty"] = props
        items.append({"@type": "ListItem", "position": i, "item": ev})

    schema = {"@context": "https://schema.org", "@type": "ItemList",
              "name": "Conference and event venues published on this page, %s" % city,
              "description": ("The %d %s conference and event venues listed on this page, with the "
                              "theatre capacity, floor area, ceiling height, event room count and "
                              "guest room count each venue publishes for its largest space. Every "
                              "figure is read from the venue's own capacity chart, fact sheet, "
                              "floor plan or technical specification. Where a venue publishes "
                              "nothing for a field, no figure is given."
                              % (len(items), city)),
              "numberOfItems": len(items),
              "itemListOrder": "https://schema.org/ItemListOrderDescending",
              "itemListElement": items}

    # ------------------------------------------------------------- inject
    p = os.path.join(ROOT, page)
    s = io.open(p, encoding='utf-8').read()

    marker = '<!-- city index, generated by build_city_index.py -->'
    s = re.sub(re.escape(marker) + r'.*?' + re.escape('<!-- /city index -->') + r'\s*',
               '', s, flags=re.S)

    anchor = '<section class="s-white pad" id="rooms-we-have-walked"'
    if anchor in s:
        # goes after that whole section
        i = s.index(anchor)
        j = s.index('</section>', i) + len('</section>')
        block = '\n\n' + marker + '\n' + section + '<!-- /city index -->\n'
        s = s[:j] + block + s[j:]
    else:
        anchor2 = '<section class="cta-band pad">'
        if anchor2 not in s:
            sys.exit('Could not find an insertion point in %s' % page)
        i = s.index(anchor2)
        block = marker + '\n' + section + '<!-- /city index -->\n\n'
        s = s[:i] + block + s[i:]

    # Replace the trimmed ItemList with the full one.
    blob = ('<script type="application/ld+json">' +
            json.dumps(schema, ensure_ascii=False) + '</script>')
    old = re.search(r'<script type="application/ld\+json">\{"@context": "https://schema\.org", '
                    r'"@type": "ItemList".*?</script>', s, re.S)
    if old:
        s = s[:old.start()] + blob + s[old.end():]
    else:
        s = s.replace('</head>', blob + '\n</head>', 1)

    # The page now needs the finder stylesheet and script, for the save buttons.
    if 'assets/css/finder.css' not in s:
        s = s.replace('<link rel="stylesheet" href="assets/css/site.css',
                      '<link rel="stylesheet" href="assets/css/finder.css?v=202609060900">\n'
                      '<link rel="stylesheet" href="assets/css/site.css', 1)
    if 'assets/js/finder.js' not in s:
        s = re.sub(r'(<script src="assets/js/site\.js[^"]*"[^>]*></script>)',
                   r'\1\n<script src="assets/js/finder.js?v=202609060900" defer></script>', s, 1)

    io.open(p, 'w', encoding='utf-8').write(s)
    print('%s: published %d venues in %d bands, ItemList now %d items'
          % (page, len(rows), len(blocks), len(items)))


if __name__ == '__main__':
    build(sys.argv[1] if len(sys.argv) > 1 else 'Sydney')
