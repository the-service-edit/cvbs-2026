#!/usr/bin/env python3
"""
DO NOT RE-RUN. 8 Sep 2026: the venue finder is not shipping at launch.
It was renamed to venue-finder-preview-4f9c2e.html and every route to it was
removed from the 62 shipping pages. Running this script re-injects those
routes and re-exposes the finder to CVBS. See cvbs-launch-scope-truth.
"""
# -*- coding: utf-8 -*-
"""Connect the venue pages to the finder.

    python3 scripts/patch-venue-pages.py

WHAT IT ADDS TO EACH /venue-visits/<slug>/ PAGE
    1. Save to your shortlist, beside Start your brief in the sidebar card. A
       venue page was previously a dead end for anyone not ready to enquire
       that minute: read it, admire it, leave. Now it can be kept.
    2. A line into the finder, filtered to that venue's own city and its own
       largest published capacity, so "this one is close but not quite" has
       somewhere to go that is not the back button.
    3. The finder stylesheet and script, which the two above need.

WHAT IT DELIBERATELY DOES NOT DO
    Invent a "similar venues" list. Similarity would have to be computed from
    capacity alone, which would put a zoo and a hotel side by side and call
    them alternatives. The finder does that job honestly, with the organiser's
    own numbers, so the page hands over to the finder instead of guessing.

Idempotent. Re-run after re-running build_venue.py or build_westin.py.
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'assets', 'data', 'venues.json')
VV = os.path.join(ROOT, 'venue-visits')

HEART = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" '
         'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M20.8 6.6a5 5 0 0 0-7.1 0L12 8.3l-1.7-1.7a5 5 0 1 0-7.1 7.1l8.8 8.8 8.8-8.8a5 5 0 0 0 0-7.1z"/></svg>')
ARROW = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" '
         'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')


def main():
    payload = json.loads(io.open(DATA, encoding='utf-8').read())
    by_visit = dict((v['visit'], v) for v in payload['venues'] if v.get('visit'))
    cities = {}
    for v in payload['venues']:
        cities[v['city']] = cities.get(v['city'], 0) + 1

    done, skipped = [], []
    for slug in sorted(os.listdir(VV)):
        p = os.path.join(VV, slug, 'index.html')
        if not os.path.isfile(p):
            continue
        v = by_visit.get(slug)
        if not v:
            skipped.append(slug + ' (no data row)')
            continue
        s = io.open(p, encoding='utf-8').read()
        before = s

        if 'assets/css/finder.css' not in s:
            s = s.replace('<link rel="stylesheet" href="../../assets/css/site.css',
                          '<link rel="stylesheet" href="../../assets/css/finder.css?v=202609060900">\n'
                          '<link rel="stylesheet" href="../../assets/css/site.css', 1)
        if 'assets/js/finder.js' not in s:
            s = re.sub(r'(<script src="\.\./\.\./assets/js/site\.js[^"]*"[^>]*></script>)',
                       r'\1\n<script src="../../assets/js/finder.js?v=202609061800" defer></script>',
                       s, 1)

        cap = v.get('maxcap')
        others = cities.get(v['city'], 1) - 1
        finder = '../../venue-results.html?dest=' + v['city'].replace(' ', '%20')
        if cap:
            finder += '&amp;guests=' + str(cap)
        if others > 0:
            line = ('<a class="vcx__enq" href="%s">See what else we publish in %s %s</a>'
                    % (finder, v['city'], ARROW))
        else:
            line = ('<a class="vcx__enq" href="../../venue-results.html">'
                    'Look at every venue we publish %s</a>' % ARROW)

        # The shortlist link only shows itself once something is on it, so a
        # first time reader never sees an empty widget.
        pip = ('<a class="vf-pip" data-vf-pip="../../venue-results.html?view=saved" '
               'href="../../venue-results.html?view=saved">Your shortlist <b>0</b></a>')

        block = ('\n        <div class="vf-onpage">'
                 '<button class="vf-save" type="button" data-save="%s" data-name="%s" '
                 'aria-pressed="false">%s<span>Save to your shortlist</span></button>'
                 '%s%s</div>' % (v['id'], v['n'].replace('"', '&quot;'), HEART, pip, line))

        if 'data-save=' not in s:
            m = re.search(r'(<div class="vg-card__body">\s*<a class="btn btn--teal"[^>]*>.*?</a>)',
                          s, re.S)
            if not m:
                skipped.append(slug + ' (no sidebar CTA found)')
                continue
            s = s[:m.end(1)] + block + s[m.end(1):]
        elif 'data-vf-pip' not in s:
            s = re.sub(r'(<div class="vf-onpage">.*?</button>)', r'\1' + pip, s, 1, re.S)

        if s == before:
            skipped.append(slug + ' (already done)')
            continue
        io.open(p, 'w', encoding='utf-8').write(s)
        done.append(slug)

    print('venue pages wired to the finder: %d' % len(done))
    for d in done:
        print('  /venue-visits/%s/' % d)
    for k in skipped:
        print('  skipped: ' + k)


if __name__ == '__main__':
    main()
