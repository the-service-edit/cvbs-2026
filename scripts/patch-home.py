#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Give the homepage a second door: the venue finder.

    python3 scripts/patch-home.py

WHY
    Until now the only thing a first time visitor could DO on this site was
    start a brief. That is the right primary action, because the brief is the
    event that earns the commission, and the hero form stays exactly as it is.
    But a person who is not ready to hand over their event yet had nowhere to
    go except reading, and a person who arrives cold from an AI answer, which
    is where 59 per cent of AI referred traffic lands, could not see that CVBS
    knows anything specific about any venue.

    One line under the hero form, and one link in the destinations band, is the
    whole change. It is deliberately secondary to the brief.

Idempotent.
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'index.html')
DEST = os.path.join(ROOT, 'destinations.html')
DATA = os.path.join(ROOT, 'assets', 'data', 'venues.json')

payload = json.loads(io.open(DATA, encoding='utf-8').read())
N = payload['meta']['count']

ARROW = ('<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" '
         'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')

HERO_LINE = ('\n<p class="hero-alt reveal" data-d="3">Not ready to hand it over yet? '
             '<a href="venue-results.html">Look through the %d venues we publish, '
             'with the capacity figures they put out themselves %s</a></p>' % (N, ARROW))

CSS = '''
/* One quiet second door under the hero brief form. It has to read clearly on
   the scrim without competing with the primary action beside it. */
.hero-alt{margin:1.1rem 0 0;font-size:.95rem;line-height:1.5;color:rgba(255,255,255,.78)}
.hero-alt a{color:#fff;font-weight:600;text-decoration:none;
  border-bottom:1px solid rgba(255,255,255,.45);padding-bottom:2px}
.hero-alt a:hover{border-color:var(--teal)}
.hero-alt svg{vertical-align:-3px;margin-left:.15rem}
@media(max-width:700px){.hero-alt{font-size:.88rem}}
'''


def main():
    s = io.open(PAGE, encoding='utf-8').read()
    changed = []

    if 'hero-alt' not in s:
        anchor = '        </form>\n<div class="hero-proofs reveal"'
        if anchor not in s:
            sys.exit('Could not find the hero form on index.html')
        s = s.replace(anchor, '        </form>' + HERO_LINE + '\n<div class="hero-proofs reveal"', 1)
        changed.append('hero line')

    # 7 Sep: the "Or search every venue we publish..." link under the homepage
    # destinations band was removed at Mel's request. Do not reinstate it.
    # The band keeps its "See all destinations" link, and venue-results.html is
    # still reachable from the nav as "Browse all venues".

    io.open(PAGE, 'w', encoding='utf-8').write(s)

    css = os.path.join(ROOT, 'assets', 'css', 'site.css')
    c = io.open(css, encoding='utf-8').read()
    if '.hero-alt' not in c:
        io.open(css, 'a', encoding='utf-8').write(CSS)
        changed.append('site.css .hero-alt')

    # destinations.html gets the same route, high on the page.
    if os.path.exists(DEST):
        d = io.open(DEST, encoding='utf-8').read()
        if 'venue-results.html' not in d:
            m = re.search(r'(<p class="lead">.*?</p>)', d, re.S)
            if m:
                link = ('\n    <p style="margin-top:1.2rem"><a class="link-arrow" '
                        'href="venue-results.html" style="color:var(--teal-ink)">'
                        'Search the %d venues we publish by destination, numbers and layout %s</a></p>'
                        % (N, ARROW))
                d = d[:m.end(1)] + link + d[m.end(1):]
                io.open(DEST, 'w', encoding='utf-8').write(d)
                changed.append('destinations.html link')

    print('index.html and destinations.html: ' + (', '.join(changed) if changed else 'already done'))


if __name__ == '__main__':
    main()
