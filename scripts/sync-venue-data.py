#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Push venues_sydney.py into the page's data island.

WHY THIS EXISTS
    The venue data lives in _venue-index-source/venues_sydney.py. The page
    carries a copy of it in a JSON island, which feeds the at a glance rail and
    the site visit records. Adding a venue to the data file does nothing until
    that island is rebuilt, and the site visit intake script matches folder
    names against the island, so a new venue is invisible to it until then.

    Run this after editing venues_sydney.py, then run site-visit-intake.py.

WHAT IT PROTECTS
    Site visit records already published stay exactly where they are. This only
    ever rewrites capacity data, never a visit. If a venue disappears from the
    data file while it still holds a visit record, this refuses to run rather
    than silently deleting the record.
"""

import io, json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_venue-index-source')
PAGE = os.path.join(ROOT, 'venue-finder-sydney.html')

KEYS = ['n','sp','pr','ty','th','bq','cl','ck','cab','ush','bd','br','gr',
        'area','ceil','ceilq','s_name','s_th','note','worked','seen','visit']

sys.path.insert(0, SRC)
try:
    from venues_sydney import VENUES
except ImportError:
    sys.exit('Could not import venues_sydney.py from %s' % SRC)

s = io.open(PAGE, encoding='utf-8').read()
m = re.search(r'(<script type="application/json" id="vidx-data">)(.*?)(</script>)', s, re.S)
if not m:
    sys.exit('No data island in %s' % os.path.basename(PAGE))
current = {v['n']: v for v in json.loads(m.group(2))}

names = set(v['n'] for v in VENUES)
orphans = [n for n, v in current.items() if v.get('visit') and n not in names]
if orphans:
    sys.exit('Refusing to run. These venues hold a site visit record but are no '
             'longer in venues_sydney.py:\n  ' + '\n  '.join(orphans) +
             '\nPut them back, or clear the record first.')

out, added, kept = [], [], 0
for v in VENUES:
    row = {k: v.get(k) for k in KEYS}
    old = current.get(v['n'])
    if old is None:
        added.append(v['n'])
    elif old.get('visit'):
        row['visit'] = old['visit']                      # the record wins
        row['seen'] = old.get('seen') or row.get('seen')
        kept += 1
    out.append(row)

shutil.copyfile(PAGE, PAGE + '.bak')
io.open(PAGE, 'w', encoding='utf-8').write(
    s[:m.start(2)] + json.dumps(out, ensure_ascii=False, separators=(',', ':')) + s[m.end(2):])

print('%d venues written to %s' % (len(out), os.path.basename(PAGE)))
if added:
    print('added: %s' % ', '.join(added))
print('site visit records preserved: %d' % kept)
print('previous version kept as %s.bak' % os.path.basename(PAGE))
print()
print('Remember: a venue only belongs in the ItemList schema once the page names')
print('it in visible copy. See VISIBLE in _venue-index-source/gen.py.')
