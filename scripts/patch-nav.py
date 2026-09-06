#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add "Find a venue" to the primary and mobile navigation on every site page.

    python3 scripts/patch-nav.py

WHY IT IS FIRST IN THE NAV
    Until now the only thing a visitor could DO on the site was start a brief.
    Everything else was reading. The finder is the one navigation item that
    answers "what can I do here", so it sits ahead of "How it works", which is
    a page about us.

Idempotent. Run it again after any nav change and it will not double up.
"""

import sys
sys.exit("patch-nav.py is retired. The Find a venue nav item was removed from the site on 6 Sep 2026. Running this would put it back.")
import io, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ARROW = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
         'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')

DESK_ANCHOR = '<a href="{p}how-it-works.html">How it works</a>'
DESK_NEW = '<a href="{p}find-a-venue.html">Find a venue</a>'
MOB_ANCHOR = '<a href="{p}how-it-works.html">How it works ' + ARROW + '</a>'
MOB_NEW = '<a href="{p}find-a-venue.html">Find a venue ' + ARROW + '</a>'

SKIP = ('_backup', '_original-backup', '_preview', '_vvcheck', '_hero-review',
        'presentation/', 'CVBS-', 'cvbs-strategy', 'cvbs-landing',
        'cvbs-services-ecosystem', 'index-pro', 'index-video', 'index-strip',
        'index-everlab', '_superseded', 'Quote-Generator', 'Post-Designer',
        'EDM-Designer', 'email-templates', 'instagram-carousels', 'hub/')


def targets():
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        b = os.path.basename(p)
        if any(b.startswith(s) or s in b for s in SKIP):
            continue
        out.append((p, ''))
    for p in sorted(glob.glob(os.path.join(ROOT, 'venue-visits', '*', 'index.html'))):
        out.append((p, '../../'))
    p = os.path.join(ROOT, 'venue-visits', 'index.html')
    if os.path.exists(p):
        out.append((p, '../'))
    return out


def main():
    changed, already, nonav = [], [], []
    for path, pre in targets():
        s = io.open(path, encoding='utf-8').read()
        if 'find-a-venue.html' in s:
            already.append(os.path.relpath(path, ROOT))
            continue
        orig = s
        da, dn = DESK_ANCHOR.format(p=pre), DESK_NEW.format(p=pre)
        ma, mn = MOB_ANCHOR.format(p=pre), MOB_NEW.format(p=pre)
        if ma in s:
            s = s.replace(ma, mn + ma, 1)
        if da in s:
            s = s.replace(da, dn + da, 1)
        if s == orig:
            nonav.append(os.path.relpath(path, ROOT))
            continue
        io.open(path, 'w', encoding='utf-8').write(s)
        changed.append(os.path.relpath(path, ROOT))

    print('nav updated on %d pages' % len(changed))
    if already:
        print('already had it: %d' % len(already))
    if nonav:
        print('\nno matching nav found on these, check by hand:')
        for n in nonav:
            print('  ' + n)


if __name__ == '__main__':
    main()

