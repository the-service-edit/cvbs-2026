#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rewrite the destination card copy on destinations.html.

    python3 _destination-source/build_hub.py

Only the one sentence inside each card is replaced. The card markup, the
images, the precinct chips, the order and the hero form are left exactly as
they are, because the hub design is signed off and this is a copy change.

The rule for a card sentence: it has to help a planner decide whether to open
that page. Not a description of the place.
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'destinations.html')

CARDS = {
 'venue-finder-sydney.html':
   'The widest choice of large conference floors in the country, and above 2,000 seated in one room, none of it is a hotel.',
 'venue-finder-melbourne.html':
   'The largest published exhibition floor of any Australian convention centre, and a city grid that gives delegates somewhere to go afterwards.',
 'venue-finder-brisbane.html':
   'A near 4,000 seat plenary, four exhibition halls and 44 breakout rooms in one walkable riverside precinct, twenty minutes from the airport.',
 'venue-finder-perth.html':
   'Almost all the serious capacity sits in two precincts four kilometres apart, with Fremantle and the Swan Valley for the evenings.',
 'venue-finder-adelaide.html':
   'A genuinely walkable Riverbank, short airport transfers, and three wine regions inside an hour of the terminal.',
 'venue-finder-canberra.html':
   'Government and association events with the national institutions as your dinner venues, and the sitting calendar as the first question.',
 'venue-finder-hobart.html':
   'Unusually strong for high value programs under 300, where flight capacity matters more than the size of the room.',
 'venue-finder-darwin.html':
   'A convention centre with direct services across South East Asia, and a dry season that decides the date before you do.',
 'venue-finder-gold-coast.html':
   'Broadbeach carries the conference market, and the coast has the deepest run of residential conference resorts in the country.',
 'venue-finder-sunshine-coast.html':
   'One four figure plenary at Twin Waters, four separate coastal towns, and a hinterland built for small high value retreats.',
 'venue-finder-cairns.html':
   'Two World Heritage areas within reach of one airport, and an international network unusual for a city this size.',
 'venue-finder-hunter-valley.html':
   'The largest residential conference resort we have verified in regional New South Wales, a little over two hours from Sydney.',
 'venue-finder-blue-mountains.html':
   'Ninety minutes from Sydney, on one road, where nobody can quietly go home at six o’clock.',
 'venue-finder-byron-bay.html':
   'Small, premium and capacity limited, and one of the best places in the country for a leadership retreat.',
 'venue-finder-yarra-valley.html':
   'An hour from Melbourne, with real breakout depth and a cellar door program, and where a leadership offsite usually belongs.',
 'venue-finder-mornington-peninsula.html':
   'Exclusive use properties on the coast and among vineyards, close enough to Melbourne to be worth the coach.',
}


def main():
    s = io.open(PAGE, encoding='utf-8').read()
    done, missing = 0, []
    for href, copy in CARDS.items():
        pat = (r'(<a class="city-card[^"]*"[^>]*href="%s">.*?<div class="city-card__body">'
               r'<h3 class="h4">[^<]*</h3><p>)(.*?)(</p>)' % re.escape(href))
        m = re.search(pat, s, re.S)
        if not m:
            missing.append(href)
            continue
        s = s[:m.start(2)] + copy + s[m.end(2):]
        done += 1
    io.open(PAGE, 'w', encoding='utf-8').write(s)
    print('destinations.html: %d cards rewritten' % done)
    if missing:
        print('NOT FOUND on the hub: %s' % missing)
        sys.exit(1)


if __name__ == '__main__':
    main()
