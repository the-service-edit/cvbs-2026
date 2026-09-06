# -*- coding: utf-8 -*-
"""One pass over the shared header and footer, 6 September 2026.

Four changes, all from the consolidated audit:

1. venue-results.html, the filter over all 190 venues, had no navigation entry
   anywhere after find-a-venue.html was removed. An organiser browsing the nav
   could only reach venues through Destinations. It is now the last item in the
   Destinations dropdown and the mobile Destinations group, labelled
   "Browse all venues".

2. The client stories page was labelled "Results" in the nav while the venue
   filter is venue-results.html. Two different things called results. The nav
   label is now "Client stories". The filename does not change, so no link
   breaks and nothing needs redirecting.

3. Privacy and Terms exist now, so they belong in the footer where people look
   for them.

4. The brief page called it "Corporate relocation" where every other template
   says "Corporate accommodation".

Safe to re-run. Every change is skipped if it has already been made.

Usage: python3 scripts/patch-nav-2026-09.py
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = ('_backup', '_to_delete', '_hero-review', '_original-backup', '_preview',
        '_vvcheck', '_superseded', 'Claude outputs', 'public-dist', '.git',
        '_destination-source', '_venue-index-source', '_venue-visits-source')

BROWSE = 'Browse all venues'


def pages():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not any(s in d for s in SKIP)]
        if any(s in dirpath for s in SKIP):
            continue
        for fn in filenames:
            if fn.endswith('.html'):
                yield os.path.join(dirpath, fn)


def up_to_root(path):
    depth = os.path.relpath(path, ROOT).count(os.sep)
    return '../' * depth


counts = {k: 0 for k in ('browse-desktop', 'browse-mobile', 'label', 'footer', 'relocation')}

for path in pages():
    s = io.open(path, encoding='utf-8').read()
    orig = s
    up = up_to_root(path)

    # 1a. desktop Destinations dropdown
    tail = '<a href="%sdestinations.html">All destinations</a></div>' % up
    if tail in s and BROWSE not in s:
        s = s.replace(tail,
                      '<a href="%sdestinations.html">All destinations</a>'
                      '<a href="%svenue-results.html">%s</a></div>' % (up, up, BROWSE), 1)
        counts['browse-desktop'] += 1

    # 1b. mobile Destinations group
    mtail = '<a href="%sdestinations.html">All destinations</a></div></div>' % up
    if mtail in s and s.count('<a href="%svenue-results.html">%s</a>' % (up, BROWSE)) < 2:
        s = s.replace(mtail,
                      '<a href="%sdestinations.html">All destinations</a>'
                      '<a href="%svenue-results.html">%s</a></div></div>' % (up, up, BROWSE), 1)
        counts['browse-mobile'] += 1

    # 2. the ambiguous nav label
    for a, b in (('<a href="%sresults.html">Results</a>' % up,
                  '<a href="%sresults.html">Client stories</a>' % up),
                 ('<a href="%sresults.html" aria-current="page">Results</a>' % up,
                  '<a href="%sresults.html" aria-current="page">Client stories</a>' % up),
                 ('<a href="%sresults.html">Results </a>' % up,
                  '<a href="%sresults.html">Client stories </a>' % up)):
        if a in s:
            counts['label'] += s.count(a)
            s = s.replace(a, b)

    # 3. legal links in the footer bottom
    if 'Worldwide Venue Finding Solutions.</span>' in s and 'footer-legal' not in s:
        s = s.replace(
            'Worldwide Venue Finding Solutions.</span>',
            'Worldwide Venue Finding Solutions.</span>\n'
            '      <span class="footer-legal"><a href="%sprivacy.html">Privacy</a> '
            '<a href="%sterms.html">Terms</a></span>' % (up, up), 1)
        counts['footer'] += 1

    # 4. one name for the service
    if 'Corporate relocation' in s:
        n = s.count('Corporate relocation')
        s = s.replace('Corporate relocation', 'Corporate accommodation')
        counts['relocation'] += n

    if s != orig:
        io.open(path, 'w', encoding='utf-8').write(s)

for k, v in counts.items():
    print('  %-16s %d' % (k, v))
