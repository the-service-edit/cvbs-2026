#!/usr/bin/env python3
"""Check every live/preview page carries the exact footer from index.html.

Mel's launch rule, 19 Oct 2026: the home page footer is THE footer, on every page.
Usage:  python3 scripts/check-footer.py            (all pages in _site/pages.csv)
        python3 scripts/check-footer.py some.html  (just those files)
Exit 1 if any page differs. Relative prefixes (../) are normalised before comparing.
"""
import re, csv, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
FOOT = re.compile(r'<footer[\s\S]*?</footer>')
def norm(f, src):
    d = src.count('/')
    if d: f = f.replace('../' * d, '')
    return re.sub(r'\s+', ' ', f).strip()
home = norm(FOOT.search(open('index.html', encoding='utf-8').read()).group(0), 'index.html')
files = sys.argv[1:] or [r['source'] for r in csv.DictReader(open('_site/pages.csv'))
                         if r['status'] in ('live', 'preview')]
bad = []
for s in files:
    if not os.path.exists(s): bad.append((s, 'file missing')); continue
    m = FOOT.findall(open(s, encoding='utf-8').read())
    if not m: bad.append((s, 'no footer'))
    elif len(m) > 1: bad.append((s, f'{len(m)} footers'))
    elif norm(m[0], s) != home: bad.append((s, 'differs from index.html'))
print(f'{len(files) - len(bad)}/{len(files)} pages match the home footer')
for b in bad: print('  FAIL', *b)
sys.exit(1 if bad else 0)
