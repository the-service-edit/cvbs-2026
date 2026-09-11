#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build venue-results.html.

    find-a-venue.html was removed from the site on 6 Sep 2026. build_find()
    is kept for reference only and is deliberately not called.

    python3 _venue-index-source/build_finder.py

Chrome, nav, mobile menu, footer and the entity graph are lifted out of
faq.html at build time, exactly as the venue page builders lift theirs, so
these two pages can never drift from the rest of the site. Re-run after any
nav or footer change.

THE SPLIT THAT MATTERS, AND WHY
    find-a-venue.html   indexable. Static HTML, real sentences, real numbers,
                        schema that matches what a reader can see. This is the
                        page Google and the answer engines are meant to read.
    venue-results.html  noindex. A tool. Its content is rendered from a data
                        island against URL parameters, so its output changes
                        with every filter combination. Letting a crawler index
                        that is how a site ends up with thousands of near
                        duplicate URLs, and Google's own guidance says not to
                        mark up content a reader cannot see. So it carries no
                        ItemList, no FAQ and no canonical of its own.

    The filter tool and the landing pages are two different jobs. Keeping them
    on two different URLs is the whole of the indexation strategy.
"""
import io, json, os, re, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'faq.html')
import sys as _sys
_sys.path.insert(0, os.path.join(ROOT, '_site'))
from siteconf import BASE, ORG_ID, WEBSITE_ID  # site.config.json, never hardcode a host
DATA = os.path.join(ROOT, 'assets', 'data', 'venues.json')

sys.path.insert(0, os.path.join(ROOT, '_venue-index-source'))
from venues_extra import CITY_PAGES

src = io.open(SRC, encoding='utf-8').read()
chrome = src[src.index('<body>'):src.index('<main')]
footer = src[src.index('<footer class="site-footer">'):src.index('</footer>') + 9]
_ent_m = re.search(r'<script type="application/ld\+json" id="cvbs-entity">(.*?)</script>',
                   src, re.S)
_ent = json.loads(_ent_m.group(1))
# The lifted graph carries faq.html's own WebPage node. Left in, it tells a
# parser that these pages ARE the FAQ page. gen_entity.py writes the correct
# WebPage back onto every page in the sitemap, and venue-results.html is
# deliberately not in the sitemap, so it simply carries no WebPage node.
_ent['@graph'] = [n for n in _ent['@graph'] if n.get('@type') != 'WebPage']
entity = ('<script type="application/ld+json" id="cvbs-entity">' +
          json.dumps(_ent, ensure_ascii=False, separators=(',', ':')) + '</script>')

payload = json.loads(io.open(DATA, encoding='utf-8').read())
VENUES = payload['venues']
META = payload['meta']
CITIES = sorted(META['cities'].items(), key=lambda kv: -kv[1])
N = len(VENUES)
N_VISIT = META['withVisit']
N_ACCOM = META['withAccom']
CITY_WORDS = ', '.join(c for c, _ in CITIES[:-1]) + ' and ' + CITIES[-1][0]

ARROW = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
         'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')
CHEV = ('<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" '
        'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<path d="M6 9l6 6 6-6"/></svg>')
X = ('<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" '
     'stroke-width="1.8" stroke-linecap="round" aria-hidden="true">'
     '<path d="M6 6l12 12M18 6L6 18"/></svg>')

EVENT_TYPES = ['Conference or seminar', 'Meeting or board session',
               'Gala dinner or awards night', 'Cocktail function or launch',
               'Training or workshop', 'Not sure yet']


def head(title, desc, path, robots=None, extra=''):
    r = ('<meta name="robots" content="%s">\n' % robots) if robots else ''
    return '''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
{r}<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{base}{path}">
<meta name="theme-color" content="#0A2C52">
<meta property="og:type" content="website">
<meta property="og:site_name" content="CVBS, Worldwide Venue Finding Solutions">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{base}{path}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/img/favicon.png?v=202608131600" type="image/png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png?v=202608131600">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/site.css?v=202609061800">
<link rel="stylesheet" href="assets/css/finder.css?v=202609060900">
{entity}
{extra}</head>
'''.format(r=r, title=title, desc=desc, base=BASE, path=path, entity=entity, extra=extra)


def ld(obj):
    return ('<script type="application/ld+json">' +
            json.dumps(obj, ensure_ascii=False, separators=(',', ':')) + '</script>\n')


def ask_form(action, submit_label, ids_prefix='vf'):
    """The three questions that decide a shortlist, plus accommodation.

    Nothing else belongs here. Precinct, venue type and whether we have walked
    the building are all real filters, but they are refinements a person makes
    once they can see results, not questions they can answer before they have
    seen any. That is the whole of the progressive disclosure argument.
    """
    opts = ''.join('<option value="%s">%s</option>' % (c, c) for c, _ in
                   sorted(CITY_PAGES.items()))
    types = ''.join('<option value="%s">%s</option>' % (t, t) for t in EVENT_TYPES)
    return '''<form class="vf-ask" id="{p}-ask" action="{action}" method="get">
        <div class="vf-ask__row">
          <div class="vf-f">
            <label for="{p}-dest">Where</label>
            <select id="{p}-dest" name="dest"><option value="">Any destination</option>{opts}</select>
          </div>
          <div class="vf-f">
            <label for="{p}-guests">How many people</label>
            <input id="{p}-guests" name="guests" type="number" min="1" max="20000" inputmode="numeric" placeholder="e.g. 250">
          </div>
          <div class="vf-f vf-f--wide">
            <label for="{p}-type">What are you planning</label>
            <select id="{p}-type" name="type"><option value="">Choose one</option>{types}</select>
          </div>
          <div class="vf-go">
            <button class="btn btn--teal" type="submit">{label} {arrow}</button>
          </div>
        </div>
        <p class="vf-ask__note">Every capacity here is the one the venue publishes for itself. Nothing is estimated. <a href="how-it-works.html">See how we work</a>.</p>
      </form>'''.format(p=ids_prefix, action=action, opts=opts, types=types,
                        label=submit_label, arrow=ARROW)


# ============================================================ find-a-venue
def build_find():
    path = 'find-a-venue.html'
    title = 'Find a Conference Venue in Australia | CVBS'
    desc = ('Search %d Australian conference and event venues by destination, delegate '
            'numbers and room layout, using each venue’s own published capacity '
            'figures. Save a shortlist, compare venues side by side, and hand it to CVBS.' % N)

    city_cards = ''
    for city, count in CITIES:
        page = CITY_PAGES.get(city, '')
        walked = sum(1 for v in VENUES if v['city'] == city and v.get('visit'))
        line = '%d %s with published capacities' % (count, 'venue' if count == 1 else 'venues')
        if walked:
            line += ', %d we have walked through' % walked
        city_cards += (
            '<a class="vf-city" href="venue-results.html?dest=%s">'
            '<span class="vf-city__n">%s</span>'
            '<span class="vf-city__c">%s</span>'
            '<span class="vf-city__t">%s</span></a>'
            % (city.replace(' ', '%20'), city, count, line))

    faqs = [
        ('What can I actually do on this page?',
         'You can filter %d Australian conference and event venues by destination, by how '
         'many people are coming and by the way you want the room set up, save the ones '
         'worth a look to a shortlist, put two to four side by side, and send the whole '
         'lot to us in one message. Nothing asks you to register.' % N),
        ('Where do the capacity figures come from?',
         'Each venue’s own published capacity chart, fact sheet, floor plan or technical '
         'specification. Where a venue publishes nothing for a layout, the page says '
         '“not published” rather than estimating it. We would rather show you a gap than '
         'a guess.'),
        ('Is this every conference venue in Australia?',
         'No, and it is not meant to be. It is %d venues across %s, which is the part of '
         'what we know that we can put a source against. We book venues every week that '
         'are not on this page, so if nothing here fits, tell us what you are planning and '
         'we will go looking.' % (N, CITY_WORDS)),
        ('What does it cost to use CVBS?',
         'Nothing. The venue pays us a commission out of the budget it already holds for '
         'that booking, at the same rate whether you come through us or go direct, so '
         'using us does not put your rate up.'),
        ('Can I book a venue here?',
         'No. We are not a booking platform and we do not hold live availability. What we '
         'do is take your brief to the venues, get the rates and the inclusions in writing, '
         'and put the comparison in front of you. The room is booked by you, on the '
         'venue’s own contract, with the terms we have negotiated.'),
        ('Why not just contact the hotels myself?',
         'You can, and for one meeting in a city you know well it is often the right call. '
         'It stops being the right call when the number of venues you have to chase, and '
         'the number of times you have to chase them, is bigger than the time you have. '
         'Our page on <a href="how-to-choose-a-venue-finder.html">how to choose a venue '
         'finder</a> is deliberately honest about where the line sits.'),
    ]
    faq_html = ''.join(
        '<details class="faq"><summary>%s</summary><div><p>%s</p></div></details>' % (q, a)
        for q, a in faqs)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer",
                                                 "text": re.sub(r'<[^>]+>', '', a)}}
                             for q, a in faqs]}
    crumb_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE},
                    {"@type": "ListItem", "position": 2, "name": "Find a venue",
                     "item": BASE + path}]}
    # No WebPage node here on purpose. gen_entity.py owns the WebPage,
    # Organization, WebSite and Service nodes on every page in the sitemap and
    # strips any it finds, so emitting one would be writing something that gets
    # deleted on the next entity run. Run gen_entity.py after this builder.

    body = '''<main id="main">

<section class="page-hero" style="padding-bottom:clamp(2rem,4vh,3rem)">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><b style="color:inherit;font-weight:500">Find a venue</b></nav>
    <span class="eyebrow" style="margin-top:1.2rem">Venue finder</span>
    <h1>Find a conference venue in Australia.</h1>
    <p class="lead">Tell us where you are going, how many are coming and what you are planning. We will show you the venues whose own published figures say the room holds it, and you can keep the ones worth a look.</p>
    <div style="max-width:900px;margin-top:1.8rem">
      {ask}
    </div>
  </div>
</section>

<section class="s-stone pad" id="whats-here">
  <div class="wrap">
    <div class="vidx-lede">
      <div class="vidx-answer">
        <span class="vidx-answer__tag">What is on this page</span>
        <p><b>CVBS publishes the capacity figures for {n} conference and event venues across {cities}</b>, each one read from the venue&rsquo;s own capacity chart, fact sheet or floor plan rather than from a directory. {nv} of them we have walked through ourselves. {na} have guest rooms in the same building, which is usually the question that decides a residential program.</p>
        <p><b>This is not every venue in Australia, and it is not trying to be.</b> Karen and Anthony have been sourcing venues since 1989 and book rooms every week that are not on this page. What is published here is the part we can put a source against, and it is enough to get you from &ldquo;somewhere in Sydney for 250&rdquo; to three or four buildings worth a real conversation. <a href="venue-results.html">Start with all {n}</a>.</p>
      </div>
      <aside class="vidx-stats" aria-label="What CVBS publishes">
        <span class="vidx-stats__tag">What we publish</span>
        <div class="vidx-stat"><div class="vidx-stat__n">{n}</div><div class="vidx-stat__l">venues with published capacities</div></div>
        <div class="vidx-stat"><div class="vidx-stat__n">{nv}</div><div class="vidx-stat__l">we have walked through ourselves</div></div>
        <div class="vidx-stat"><div class="vidx-stat__n">{na}</div><div class="vidx-stat__l">with guest rooms in the building</div></div>
        <div class="vidx-stat"><div class="vidx-stat__n">1989</div><div class="vidx-stat__l">the year we started sourcing venues</div></div>
      </aside>
    </div>
  </div>
</section>

<section class="s-white pad" id="destinations">
  <div class="wrap">
    <span class="eyebrow">Start with a city</span>
    <h2 class="h2">Where is it happening?</h2>
    <p class="lead" style="max-width:62ch">Each of these opens the venues we publish in that destination, largest room first, with the layout figures the venue itself puts out.</p>
    <div class="vf-cities">{cards}</div>
    <p style="margin-top:1.6rem"><a class="link-arrow" href="destinations.html" style="color:var(--teal-ink)">All the destinations we source in {arrow}</a></p>
  </div>
</section>

<section class="s-stone pad" id="by-need">
  <div class="wrap">
    <span class="eyebrow">Or start with the constraint</span>
    <h2 class="h2">The three questions that decide it.</h2>
    <div class="grid" style="margin-top:2rem">
      <article class="card">
        <h3 class="h4">Does the room hold them?</h3>
        <p>A gala dinner for 300 and a plenary for 300 are two different buildings. Tell us which one you are running and we will show you the layout figure that matters, not the biggest number the venue publishes.</p>
        <p style="margin-top:1rem"><a class="link-arrow" href="venue-results.html?type=Gala%20dinner%20or%20awards%20night" style="color:var(--teal-ink)">Venues by room layout {arrow}</a></p>
      </article>
      <article class="card">
        <h3 class="h4">Do they sleep there too?</h3>
        <p>{na} of the venues here have guest rooms in the same building. For a two day program that is usually the whole decision, because the alternative is a coach at 7.30 in the morning.</p>
        <p style="margin-top:1rem"><a class="link-arrow" href="conference-venues-with-accommodation.html" style="color:var(--teal-ink)">Venues with rooms on site {arrow}</a></p>
      </article>
      <article class="card">
        <h3 class="h4">Has anyone actually been?</h3>
        <p>{nv} of these we have walked through ourselves, with a straight answer about what the building is good for and where it stops working.</p>
        <p style="margin-top:1rem"><a class="link-arrow" href="venue-visits/" style="color:var(--teal-ink)">Venues we have walked through {arrow}</a></p>
      </article>
    </div>
  </div>
</section>

<section class="s-white pad" id="then-what">
  <div class="wrap">
    <span class="eyebrow">When you have a shortlist</span>
    <h2 class="h2">This is where handing it over gets easier than carrying on.</h2>
    <p class="lead" style="max-width:64ch">Finding four venues that fit is the quick part. What takes the week is everything after it, and that is the part we do.</p>
    <ol class="steps" style="margin-top:2.2rem">
      <li class="step"><h3 class="h4">You send us the shortlist</h3><p>Save the venues worth a look, add your dates and your numbers, and send the lot in one message. We already have the capacities, so you do not have to retype them.</p></li>
      <li class="step"><h3 class="h4">We go to the venues</h3><p>We put your brief to each one, hold space where it is tight, and come back with day delegate rates, room rates, inclusions and the terms in writing. Same rate as going direct, because the venue pays us out of a budget it already holds.</p></li>
      <li class="step"><h3 class="h4">You choose, on real numbers</h3><p>One comparison, one conversation, and a straight recommendation from whichever of us knows the building. Then you sign with the venue on its own contract.</p></li>
    </ol>
    <div class="btn-row" style="margin-top:2.2rem">
      <a class="btn btn--teal" href="submit-a-brief.html">Tell us about your event {arrow}</a>
      <a class="btn btn--ghost" href="how-it-works.html">How it works</a>
    </div>
  </div>
</section>

<section class="s-stone pad" id="faq">
  <div class="wrap wrap--narrow">
    <span class="eyebrow">Common questions</span>
    <h2 class="h2">Using the venue finder</h2>
    <div style="margin-top:2rem">{faqs}</div>
  </div>
</section>
</main>
'''.format(ask=ask_form('venue-results.html', 'Show me the venues'),
           n=N, nv=N_VISIT, na=N_ACCOM, cities=CITY_WORDS,
           cards=city_cards, arrow=ARROW, faqs=faq_html)

    html = (head(title, desc, path,
                 extra=ld(crumb_ld) + ld(faq_ld)) +
            chrome + body + footer +
            '\n<script src="assets/js/site.js?v=202609060900" defer></script>'
            '\n<script src="assets/js/finder.js?v=202609061800" defer></script>'
            '\n</body>\n</html>\n')
    io.open(os.path.join(ROOT, path), 'w', encoding='utf-8').write(html)
    return path, len(html)


# ========================================================== venue-results
def build_results():
    path = 'venue-results.html'
    title = 'Venue results | CVBS'
    desc = ('Filter the venues CVBS publishes by destination, delegate numbers and room '
            'layout. A working tool, not an indexed page.')

    island = io.open(DATA, encoding='utf-8').read()

    body = '''<main id="main">

<section class="page-hero" style="padding-bottom:1.5rem">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><b style="color:inherit;font-weight:500">Results</b></nav>
    <h1 class="h2" style="margin-top:1.2rem">Venues that fit.</h1>
    <p class="lead" style="max-width:60ch">Change any answer and the list changes with it. Save the ones worth a look, then send them to us in one go.</p>
    <div style="max-width:1000px;margin-top:1.6rem">
      {ask}
    </div>
  </div>
</section>

<section class="s-white" style="padding-top:1.5rem;padding-bottom:4rem">
  <div class="wrap">

    <div class="vf-refine">
      <button class="vf-refine__toggle" type="button" id="vf-refine-toggle" aria-expanded="false" aria-controls="vf-refine-panel">Refine these {chev}</button>
      <div class="vf-refine__panel" id="vf-refine-panel" hidden>
        <div class="vf-f">
          <label for="vf-q">Venue name</label>
          <input id="vf-q" type="search" placeholder="e.g. Sofitel, Crown, ICC" autocomplete="off" spellcheck="false">
        </div>
        <div class="vf-f">
          <label for="vf-accom">Accommodation</label>
          <select id="vf-accom"><option value="">Either way</option><option value="yes">Needs guest rooms on site</option><option value="no">Bedrooms not needed</option></select>
        </div>
        <div class="vf-f">
          <label for="vf-prec">Part of the destination</label>
          <select id="vf-prec"><option value="">Anywhere in the destination</option></select>
        </div>
        <div class="vf-f">
          <label for="vf-vt">Kind of building</label>
          <select id="vf-vt"><option value="">Any</option><option value="hotel">Hotel</option><option value="conv">Convention centre</option><option value="event">Event venue</option><option value="resort">Resort</option></select>
        </div>
        <div class="vf-f">
          <label for="vf-seen">Our own experience</label>
          <select id="vf-seen"><option value="">Everything we publish</option><option value="seen">We have walked through it</option><option value="worked">We have booked it before</option></select>
        </div>
      </div>
    </div>

    <div id="vf-chips" class="vf-chips" aria-label="Filters applied"></div>

    <div class="vf-head" style="margin-top:1.4rem">
      <p class="vf-count" id="vf-count" role="status" aria-live="polite"></p>
      <div class="vf-sort">
        <label for="vf-sort">Order</label>
        <select id="vf-sort">
          <option value="fit">Closest fit first</option>
          <option value="largest">Largest room first</option>
          <option value="rooms">Most guest rooms</option>
          <option value="name">Venue name</option>
        </select>
      </div>
    </div>

    <div id="vf-results"></div>

    <p id="vf-cmp-max" hidden style="margin-top:1rem;color:#8A5A16;font-size:.9rem">Four venues is as many as fit side by side and still stay readable. Uncheck one to add another.</p>

    <div class="vidx-handoff" style="margin-top:3rem">
      <p class="vidx-handoff__q">Not seeing the right building?</p>
      <p class="vidx-handoff__s">What we publish is a fraction of what we book. Tell us the dates, the numbers and what the day has to do, and we will go and find it.</p>
      <a class="btn btn--teal" href="submit-a-brief.html">Tell us about your event {arrow}</a>
    </div>

  </div>
</section>
</main>

<div class="vf-tray" id="vf-tray" role="region" aria-label="Your shortlist">
  <div class="vf-tray__in">
    <div>
      <p class="vf-tray__n" data-tray-n></p>
      <p class="vf-tray__names" data-tray-names></p>
    </div>
    <div class="vf-tray__acts">
      <a class="btn btn--light" data-tray-review href="venue-results.html?view=saved">Review shortlist</a>
      <button class="btn btn--light" type="button" data-tray-compare hidden>Compare</button>
      <button class="btn btn--light" type="button" data-share>Copy shareable link</button>
      <a class="btn btn--teal" data-tray-send href="submit-a-brief.html">Ask CVBS about these {arrow}</a>
      <button class="btn btn--ghost-light" type="button" data-tray-clear>Clear</button>
    </div>
  </div>
</div>

<div class="vf-modal" id="vf-compare" role="dialog" aria-modal="true" aria-label="Compare venues">
  <div class="vf-modal__bg" data-cmp-close></div>
  <div class="vf-modal__box">
    <div class="vf-modal__head">
      <h2>Side by side</h2>
      <button class="vf-modal__x" type="button" data-cmp-close aria-label="Close the comparison">{x}</button>
    </div>
    <div class="vf-modal__body" data-cmp-body></div>
    <div class="vf-modal__foot">
      <p>We can get day delegate rates, room rates and availability on all of these in one go.</p>
      <a class="btn btn--teal" data-cmp-send href="submit-a-brief.html">Ask CVBS about these {arrow}</a>
    </div>
  </div>
</div>

<script type="application/json" id="vf-data">{island}</script>
'''.format(ask=ask_form('venue-results.html', 'Update'), chev=CHEV, arrow=ARROW,
           x=X, island=island)

    html = (head(title, desc, path, robots='noindex, follow') +
            chrome.replace('<body>', '<body class="vf-page">', 1) + body + footer +
            '\n<script src="assets/js/site.js?v=202609060900" defer></script>'
            '\n<script src="assets/js/finder.js?v=202609061800" defer></script>'
            '\n</body>\n</html>\n')
    io.open(os.path.join(ROOT, path), 'w', encoding='utf-8').write(html)
    return path, len(html)


if __name__ == '__main__':
    for p, n in (build_results(),):
        print('wrote %-24s %7d bytes' % (p, n))
