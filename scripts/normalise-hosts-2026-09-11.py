# -*- coding: utf-8 -*-
"""One-off, 11 September 2026. Puts every public source page on the production
host from site.config.json, so source carries production addresses only.

Unlike the retired set-base-url.py this runs once, on a fixed file list (the
site pages check-site.py knows about plus sitemap.xml and the legacy stubs),
and it moves the old hosts TO the identity host rather than between two
arbitrary ones, so an @id can never be pushed onto a staging address again.
Emails, the brief store and internal tools are deliberately not touched: they
still need the staging host until cutover.
"""
import glob, io, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, '_site'))
from siteconf import ORIGIN

SKIP_PREFIX = ('CVBS-', 'cvbs-', 'index-', '_')
files = [p for p in glob.glob(os.path.join(ROOT, '*.html'))
         if not os.path.basename(p).startswith(SKIP_PREFIX)]
files += glob.glob(os.path.join(ROOT, 'venue-visits', '**', '*.html'), recursive=True)
for d in ('about', 'about/reviews', 'bestvenue', 'booking-terms', 'contact-us', 'feed',
          'get-a-quote', 'groups', 'privacy', 'relocation', 'terms', 'venuereviews'):
    files.append(os.path.join(ROOT, d, 'index.html'))
files.append(os.path.join(ROOT, 'sitemap.xml'))

GH = re.compile(r'https://the-service-edit\.github\.io/cvbs-2026')
BARE = re.compile(r'https?://conferencevenues\.com\.au')
total = 0
for p in sorted(set(files)):
    if not os.path.exists(p):
        continue
    s = io.open(p, encoding='utf-8').read()
    n1 = len(GH.findall(s)); s2 = GH.sub(ORIGIN, s)
    n2 = len(BARE.findall(s2)); s2 = BARE.sub(ORIGIN, s2)
    if s2 != s:
        io.open(p, 'w', encoding='utf-8').write(s2)
        total += n1 + n2
        print('%5d %5d  %s' % (n1, n2, os.path.relpath(p, ROOT)))
print('moved %d addresses onto %s' % (total, ORIGIN))
