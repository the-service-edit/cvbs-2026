#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the single CVBS venue dataset.

    python3 _venue-index-source/build_dataset.py

WHAT IT DOES
    Merges venues_sydney.py, venues_extra.py and the venue pages into one
    dataset and writes it to assets/data/venues.json. That file is the only
    place the website reads venue facts from: the finder, the results page, the
    comparison, the shortlist and the destination counts all consume it.

WHAT IT WILL NOT DO
    Invent a value. Every field is either present in a source file or null.
    Where a venue publishes nothing, the site prints "Not published" rather
    than guessing, and the build prints the gap in the DATA REQUIRED report at
    the end so it can be chased.

PROVENANCE
    Every venue carries src (the source for the capacity figures), src2 (the
    source for ceiling height, floor area, extra setups and the second space)
    and checked (the date those sources were last read). Provenance does not
    render to the customer. It exists so a figure can always be traced back.

PHOTOGRAPHS
    A venue only gets a photograph on a result card if CVBS took one, which
    means the venue has a page under /venue-visits/. The lead image is read
    off that page rather than guessed, so the card and the page can never show
    different photographs. Stock and generated imagery is deliberately not
    used here: on a result card a picture is a claim about the room.
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, '_venue-index-source')
OUT  = os.path.join(ROOT, 'assets', 'data', 'venues.json')
sys.path.insert(0, SRC)

from venues_sydney import VENUES as SYD
from venues_extra import (VENUES_OTHER, VENUES_SYDNEY_EXTRA, VISIT_SLUGS,
                          OFFER_PAGES, CITY_PAGES)
from venues_destinations import VENUES_DESTINATIONS

SYDNEY_CHECKED = "14 August 2026"
BUILT = "5 September 2026"

KEYS = ['id', 'n', 'city', 'pr', 'ty', 'sp', 'th', 'bq', 'cl', 'ck', 'cab',
        'ush', 'bd', 'br', 'gr', 'area', 'ceil', 'ceilq', 's_name', 's_th',
        'note', 'worked', 'seen', 'visit', 'offer', 'src', 'src2', 'checked',
        'acc', 'accq']

SETUPS = ['th', 'bq', 'cl', 'ck', 'cab', 'ush', 'bd']


def slugify(s):
    out = []
    for ch in s.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in ' -_&/':
            out.append('-')
    slug = ''.join(out)
    while '--' in slug:
        slug = slug.replace('--', '-')
    return slug.strip('-')


def lead_photo(slug):
    """First gallery photograph on the venue's own page, or None."""
    p = os.path.join(ROOT, 'venue-visits', slug, 'index.html')
    if not os.path.exists(p):
        return None
    s = io.open(p, encoding='utf-8').read()
    m = re.search(r'(?:\.\./\.\./)?(assets/img/venue-visits/[^"\']+?\.(?:jpg|webp))', s)
    if not m:
        return None
    rel = m.group(1)
    return rel if os.path.exists(os.path.join(ROOT, rel)) else None


def normalise(v, city, checked):
    r = {k: v.get(k) for k in KEYS}
    r['city'] = v.get('city') or city
    r['checked'] = v.get('checked') or checked
    r['id'] = v.get('slug') or slugify(v['n'])
    r['visit'] = v.get('visit') or VISIT_SLUGS.get(v['n'])
    r['offer'] = v.get('offer') or OFFER_PAGES.get(v['n'])
    r['worked'] = bool(v.get('worked'))
    r['photo'] = lead_photo(r['visit']) if r['visit'] else None
    # Largest published capacity across every setup the venue publishes. This
    # is what an organiser sorts on before they know their room layout.
    caps = [r[k] for k in SETUPS if r.get(k)]
    r['maxcap'] = max(caps) if caps else None

    # ---- accommodation: existence is not the same thing as inventory.
    #
    # Until 6 September 2026 the accommodation filter tested the guest-room
    # COUNT. 88 of 190 venues have no published count, so a venue with rooms
    # but no number vanished from a search for venues with accommodation.
    # Crown Melbourne and Hyatt Hotel Canberra were among them.
    #
    # 'acc' answers "are there rooms here", 'gr' answers "how many". A hotel
    # or a resort has guest rooms: that is what those words mean, and the
    # type is read off the venue's own material like every other field, so
    # this infers nothing that is not already published. Anything else with
    # no count stays 'unknown', which is not 'no'.
    #
    # 'accq' records how we know, so the card can say so rather than implying
    # a number we do not have.
    if r.get('gr'):
        r['acc'], r['accq'] = 'yes', 'counted'
    elif r.get('ty') in ('hotel', 'resort'):
        r['acc'], r['accq'] = 'yes', 'category'
    else:
        r['acc'] = 'unknown'
    # Drop the empty keys. On 58 venues this takes the shipped file down by
    # about a third, and the renderer treats missing and null identically.
    return dict((k, val) for k, val in r.items() if val not in (None, '', False))


def main():
    rows = []
    for v in SYD:
        rows.append(normalise(v, 'Sydney', SYDNEY_CHECKED))
    for v in VENUES_SYDNEY_EXTRA + VENUES_OTHER + VENUES_DESTINATIONS:
        rows.append(normalise(v, v.get('city'), v.get('checked')))

    # A duplicate id would silently overwrite a venue in the browser shortlist,
    # which is stored by id.
    ids = collections.Counter(r['id'] for r in rows)
    dupes = [i for i, c in ids.items() if c > 1]
    if dupes:
        sys.exit('Duplicate venue ids: %s' % dupes)
    names = collections.Counter(r['n'] for r in rows)
    dupe_names = [n for n, c in names.items() if c > 1]
    if dupe_names:
        sys.exit('The same venue appears twice under one name: %s' % dupe_names)

    vv = os.path.join(ROOT, 'venue-visits')
    on_disk = set(d for d in os.listdir(vv)
                  if os.path.isdir(os.path.join(vv, d))) if os.path.isdir(vv) else set()
    linked = set(r.get('visit') for r in rows if r.get('visit'))
    orphans = sorted(on_disk - linked)
    missing = sorted(linked - on_disk)
    if missing:
        sys.exit('These venues point at a venue page that does not exist: %s' % missing)

    rows.sort(key=lambda r: (r['city'], -(r.get('maxcap') or 0), r['n']))

    by_city = collections.Counter(r['city'] for r in rows)
    meta = {
        'built': BUILT,
        'cities': dict(by_city),
        'count': len(rows),
        'withVisit': sum(1 for r in rows if r.get('visit')),
        'withAccom': sum(1 for r in rows if r.get('gr')),
        'sourceNote': ("Every capacity figure is read from the venue's own published "
                       "capacity chart, fact sheet, floor plan or technical spec. "
                       "Where a venue publishes nothing for a field, the field is "
                       "absent and the site says so."),
    }
    payload = {'meta': meta, 'venues': rows}

    d = os.path.dirname(OUT)
    if not os.path.isdir(d):
        os.makedirs(d)
    blob = json.dumps(payload, ensure_ascii=False, separators=(',', ':'))
    io.open(OUT, 'w', encoding='utf-8').write(blob)

    print('wrote %s  %d venues  %d bytes' % (
        os.path.relpath(OUT, ROOT), len(rows), len(blob.encode('utf-8'))))
    print('cities: ' + ', '.join('%s %d' % (c, n) for c, n in sorted(by_city.items())))
    print('photographs on cards: %d (only where CVBS has walked the venue)' %
          sum(1 for r in rows if r.get('photo')))
    if orphans:
        print('\nVENUE PAGES WITH NO DATA ROW (they will not appear in results):')
        for o in orphans:
            print('  /venue-visits/%s/' % o)

    print('\nDATA REQUIRED')
    gaps = collections.Counter()
    for r in rows:
        for k, label in (('th', 'theatre capacity'), ('gr', 'guest rooms'),
                         ('area', 'largest space floor area'),
                         ('ceil', 'ceiling height'),
                         ('br', 'number of event rooms')):
            if not r.get(k):
                gaps[label] += 1
    for label, n in gaps.most_common():
        print('  %-32s missing on %d of %d venues' % (label, n, len(rows)))
    nocity = [c for c in CITY_PAGES if c not in by_city]
    print('\n  Destination pages with no venue data at all (%d of %d):' % (
        len(nocity), len(CITY_PAGES)))
    for c in nocity:
        print('    %-24s %s' % (c, CITY_PAGES[c]))
    print('\n  Venues with a firsthand record on file: %d' %
          sum(1 for r in rows if r.get('seen')))
    print('  Venues CVBS has confirmed it has worked with: %d' %
          sum(1 for r in rows if r.get('worked')))


if __name__ == '__main__':
    main()
