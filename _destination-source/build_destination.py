#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build the destination pages from _destination-source/destinations.py.

    python3 _destination-source/build_destination.py            # all sixteen
    python3 _destination-source/build_destination.py Melbourne  # just one

WHAT IT DOES
    Rebuilds the <main> of each destination page in one deterministic order,
    lifting the page chrome, the hero, the walked-through band and the
    generated venue index out of the page it is rewriting, so the header,
    nav, footer and entity graph can never drift and the venue figures can
    never contradict the index.

    Sydney is in patch mode. Its page is already deep and bespoke, so only the
    three sections the rest of the section gained are added to it: the
    trade-offs, the longer FAQ and the related destinations.

RUN ORDER
    build_dataset.py  ->  build_city_index.py <City>  ->  THIS  ->  gen_entity.py

    build_city_index must run first, because this script moves the block it
    writes into position and re-bands it. If you re-run build_city_index
    afterwards, run this again.

WHAT IT WILL NOT DO
    Type a capacity. Every figure on a featured card is read out of
    assets/data/venues.json at build time. That is the fix for the August 2026
    bug where a Sydney featured card and the verified index disagreed.
"""
import io, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, '_destination-source'))
from destinations import DEST, FREE_A, FAST_A, GROUP_A, WHY_CARD_2, WHY_CARD_3

DATA = json.loads(io.open(os.path.join(ROOT, 'assets', 'data', 'venues.json'),
                          encoding='utf-8').read())
BY_ID = dict((v['id'], v) for v in DATA['venues'])

ARROW = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
         'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
         '<path d="M5 12h14M13 6l6 6-6 6"/></svg>')
TICK = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
        'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<circle cx="12" cy="12" r="9"/><path d="M8.5 12.5l2.5 2.5 4.5-5"/></svg>')
PIN = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
       'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
       '<path d="M12 21s7-6.5 7-11a7 7 0 1 0-14 0c0 4.5 7 11 7 11z"/>'
       '<circle cx="12" cy="10" r="2.5"/></svg>')
PLUS = ('<span class="pm"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" '
        'stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" '
        'aria-hidden="true"><path d="M12 5v14M5 12h14"/></svg></span>')
ICON_SHIELD = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
               'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
               '<path d="M12 3l8 3v6c0 5-3.4 7.7-8 9-4.6-1.3-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/></svg>')
ICON_CHAT = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
             'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<path d="M20 14.5a2.5 2.5 0 0 1-2.5 2.5H9l-4 3.5V6.5A2.5 2.5 0 0 1 7.5 4h10A2.5 2.5 0 0 1 20 6.5z"/>'
             '<path d="M12.5 8v3.6"/><path d="M12.5 13.9v.1"/></svg>')
ICON_COIN = ('<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" '
             'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
             '<circle cx="12" cy="12" r="9"/><path d="M14.6 9.3A2.8 2.8 0 0 0 12 8c-1.6 0-2.7.8-2.7 2s1.1 1.7 '
             '2.7 2 2.7.9 2.7 2-1.1 2-2.7 2a2.8 2.8 0 0 1-2.6-1.3"/><path d="M12 6.1v1.7M12 16.2v1.7"/></svg>')


def esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;')
            .replace('>', '&gt;').replace('"', '&quot;'))


def n(x):
    return '{:,}'.format(x) if isinstance(x, (int, float)) else x


def q(s):
    """URL fragment for a query string value."""
    return s.replace(' ', '%20').replace('&', '%26').replace("'", '%27')


def slug_of(city):
    return city.lower().replace(' ', '-')


def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s)


# --------------------------------------------------------------- venue meta
def venue_meta(v):
    """The scannable meta line for a featured card, generated from the dataset."""
    bits = [v['pr']]
    if v.get('gr'):
        bits.append('%s rooms' % n(v['gr']))
    cap = None
    for k, label in (('th', 'theatre'), ('bq', 'banquet'), ('ck', 'cocktail'),
                     ('cl', 'classroom'), ('bd', 'boardroom')):
        if v.get(k):
            cap = '%s to %s %s' % (v.get('sp') or 'largest space', n(v[k]), label)
            break
    if cap:
        bits.append(cap)
    elif v.get('area'):
        bits.append('%s sqm in %s' % (n(v['area']), v.get('sp') or 'its largest space'))
    else:
        bits.append('capacities not published by the venue')
    if v.get('br'):
        bits.append('%s event rooms' % n(v['br']))
    return ' &middot; '.join(bits)


# ------------------------------------------------------------------ sections
def sec_snapshot(city, d):
    paras = '\n        '.join('<p>%s</p>' % p for p in d['snapshot'])
    # No .vidx-lede grid here. That grid is a two column layout built for the
    # Sydney page, where the second column holds the at-a-glance rail rendered
    # from the data island. These pages have no rail, so the grid would leave a
    # third of the band empty. The answer block carries its own reading measure
    # instead and sits on the page left rail.
    return '''<section class="s-stone pad" id="{slug}-snapshot">
  <div class="wrap">
    <div class="vidx-answer" style="max-width:76ch">
      <span class="vidx-answer__tag">{city}, in short</span>
      {paras}
    </div>
  </div>
</section>'''.format(slug=slug_of(city), city=esc(city), paras=paras)


def sec_sources(city, d, intro):
    ticks = ''.join('<li>%s %s</li>' % (TICK, esc(s)) for s in d['sources'])
    pins = ''.join('<li>%s %s</li>' % (PIN, esc(p)) for p in d['precincts'])
    return '''<section class="s-white"><div class="wrap hero-grid" style="align-items:start">
  <div class="prose reveal">{intro}
    <h2>What we source in {city}</h2><ul class="ticks" style="margin-top:1rem">{ticks}</ul>
    <div class="btn-row mt-2"><a class="btn btn--teal" href="submit-a-brief.html?dest={q}">Start your {city} brief {arrow}</a></div>
  </div>
  <aside class="form-card reveal" data-d="1">
    <span class="eyebrow">Where we source in {city}</span>
    <ul class="ticks" style="margin-top:1rem;font-size:.97rem">{pins}</ul>
    <p class="form-note">We source across the whole {city} market, in every precinct, not a fixed list.</p>
  </aside>
</div></section>'''.format(city=esc(city), ticks=ticks, pins=pins, intro=intro,
                           q=q(city), arrow=ARROW)


def sec_featured(city, d):
    cards = []
    for vid, suits in d['featured']:
        v = BY_ID.get(vid)
        if not v:
            sys.exit('%s: featured venue id not in the dataset: %s' % (city, vid))
        name = esc(v['n'])
        if v.get('visit'):
            name = '<a href="venue-visits/%s/">%s</a>' % (esc(v['visit']), name)
        cards.append(
            '<div class="card reveal"><h3 class="h4">{name}</h3>'
            '<p class="muted" style="margin-top:.35rem;font-size:.9rem">{meta}</p>'
            '<p style="margin-top:.6rem">{suits}</p>'
            '<a class="link-arrow mt-1" href="submit-a-brief.html?dest={q}&amp;venue={vq}">'
            'Ask us about it {arrow}</a></div>'.format(
                name=name, meta=venue_meta(v), suits=esc(suits),
                q=q(city), vq=q(v['n']), arrow=ARROW))
    return '''<section class="s-stone pad" id="{slug}-featured"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Where we would start</span>
    <h2 class="h2">A few {city} venues, and what each one is really for.</h2>
    <p class="lead">A spread rather than a ranking, chosen so you can see the shape of the market. Every figure below is the one the venue publishes for itself. We source right across {city}, so treat this as a starting point.</p></div>
  <div class="grid g-3">{cards}</div>
</div></section>'''.format(slug=slug_of(city), city=esc(city), cards=''.join(cards))


def sec_start(city, d):
    rows = ''.join('<div class="dl-row"><div class="dl-need">%s</div>'
                   '<div class="dl-pick">%s</div></div>' % (need, pick)
                   for need, pick in d['start'])
    return '''<section class="s-stone pad" id="{slug}-suitability"><div class="wrap wrap--narrow">
  <div class="section-head"><span class="eyebrow">Where to start</span><h2 class="h2">Not sure where in {city} your event belongs?</h2>
    <p class="lead">A quick steer, based on what you are running. Tell us the detail and we will shortlist what suits it, rather than the obvious names.</p></div>
  <p class="muted" style="font-size:.86rem;margin:-.5rem 0 1.2rem">Based on venue suitability alone.</p>
  <div class="dl">{rows}</div>
</div></section>'''.format(slug=slug_of(city), city=esc(city), rows=rows)


def sec_local(city, d):
    cards = ''.join('<div class="card"><h3 class="h4">%s</h3>'
                    '<p class="muted" style="margin-top:.35rem">%s</p></div>'
                    % (esc(a), esc(b)) for a, b in d['local'])
    return '''<section class="s-white pad" id="{slug}-local"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Local knowledge</span><h2 class="h2">Where in {city} to hold it.</h2>
    <p class="lead">The area you choose shapes everything from how easily delegates arrive to what you will pay for dinner. These are the ones we source across most, and what each is good for.</p></div>
  <div class="grid g-3">{cards}</div>
</div></section>'''.format(slug=slug_of(city), city=esc(city), cards=cards)


def sec_tradeoffs(city, d):
    cards = ''.join('<div class="card"><h3 class="h4">%s</h3>'
                    '<p class="muted" style="margin-top:.35rem">%s</p></div>'
                    % (esc(a), esc(b)) for a, b in d['tradeoffs'])
    return '''<section class="s-stone pad" id="{slug}-tradeoffs"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Worth knowing first</span><h2 class="h2">The parts of {city} we would raise before you commit.</h2>
    <p class="lead">No destination is right for every brief, and the useful conversation is about where the limits are. These are the ones that change a {city} program most often.</p></div>
  <div class="grid g-3">{cards}</div>
</div></section>'''.format(slug=slug_of(city), city=esc(city), cards=cards)


def sec_why(city, d):
    return '''<section class="s-white pad" id="{slug}-why"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Why CVBS in {city}</span><h2 class="h2">{h2}</h2></div>
  <div class="team-grid">
    <div class="team-photo reveal">
      <img src="assets/img/team/karen.jpg" alt="Karen Jepson, Director, CVBS" loading="lazy" onerror="this.closest('.team-photo').remove()">
    </div>
    <div class="team-copy reveal" data-d="1">
      <h3>One brief. A real person on the other end.</h3>
      <p>Everything above this point is information. It is genuinely useful, and no other venue finder in Australia publishes it. But it is not the thing you are actually buying.</p>
      <p>What you are buying is someone who has already had the conversation with the person who holds that room, knows what they will move on and when, and will pick up the phone rather than send you a portal login. Whoever takes your {city} brief stays your point of contact from the first call through to the final invoice.</p>
      <p class="who">Karen, Anthony, Chantelle and Rychelle<span>Sourcing Australian conference venues since 1989</span></p>
      <div class="btn-row mt-2"><a class="btn btn--teal" href="submit-a-brief.html?dest={q}">Start your {city} brief {arrow}</a>
      <a class="btn btn--ghost" href="about.html">Meet the team</a></div>
    </div>
  </div>

  <div class="grid g-3">
    <div class="card reveal"><div class="icon">{i1}</div><h3 class="h4">Venues we can speak for</h3><p>{lead}</p></div>
    <div class="card reveal" data-d="1"><div class="icon">{i2}</div><h3 class="h4">The drawbacks as well as the pitch</h3><p>{c2}</p></div>
    <div class="card reveal" data-d="2"><div class="icon">{i3}</div><h3 class="h4">Free to you</h3><p>{c3}</p></div>
  </div>
</div></section>'''.format(slug=slug_of(city), city=esc(city), h2=d['why_h2'], q=q(city),
                           arrow=ARROW, lead=d['why_lead'], c2=WHY_CARD_2, c3=WHY_CARD_3,
                           i1=ICON_SHIELD, i2=ICON_CHAT, i3=ICON_COIN)


def faq_pairs(city, d):
    out = []
    for question, answer in d['faqs']:
        if answer == 'FREE':
            answer = FREE_A.format(city=city)
        elif answer == 'FAST':
            answer = FAST_A.format(city=city)
        elif answer == 'GROUP':
            answer = GROUP_A.format(city=city)
        out.append((question, answer))
    return out


def sec_faq(city, d):
    items = ''.join('<details><summary>%s%s</summary><div class="ans">%s</div></details>'
                    % (question, PLUS, answer) for question, answer in faq_pairs(city, d))
    return '''<section class="s-stone pad" id="{slug}-faq"><div class="wrap wrap--narrow">
      <div class="section-head center"><span class="eyebrow eyebrow--center">FAQ</span><h2 class="h2">{city} venue finding, common questions</h2></div>
      <div class="faq reveal">{items}</div></div></section>'''.format(
        slug=slug_of(city), city=esc(city), items=items)


def sec_related(city, d):
    cards = ''.join(
        '<div class="card"><h3 class="h4">%s</h3>'
        '<p class="muted" style="margin-top:.35rem">%s</p>'
        '<a class="link-arrow mt-1" href="%s">%s %s</a></div>'
        % (esc(label), esc(why), href, 'Read on', ARROW)
        for href, label, why in d['related'])
    return '''<section class="s-white pad" id="{slug}-related"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Nearby and next</span><h2 class="h2">Places and pages worth a look before you decide.</h2></div>
  <div class="grid g-3">{cards}</div>
</div></section>'''.format(slug=slug_of(city), cards=cards)


def sec_cta(city):
    return '''<section class="cta-band pad">
  <div class="wrap">
    <span class="eyebrow eyebrow--center">Ready when you are</span>
    <h2 class="mt-1">Planning something in {city}? Tell us about it.</h2>
    <p class="lead">You will have {city} options to consider within 48 hours.</p>
    <div class="btn-row"><a class="btn btn--teal" href="submit-a-brief.html?dest={q}">Start your brief {arrow}</a>
    <a class="btn btn--ghost" href="how-it-works.html" style="color:#fff">See how it works</a></div>
  </div>
</section>'''.format(city=esc(city), q=q(city), arrow=ARROW)


# --------------------------------------------------------------------- head
def patch_head(s, city, d):
    s = re.sub(r'<title>.*?</title>', '<title>%s</title>' % d['title'], s, count=1, flags=re.S)
    s = re.sub(r'<meta name="description" content="[^"]*"',
               '<meta name="description" content="%s"' % d['meta'], s, count=1)
    s = re.sub(r'<meta property="og:title" content="[^"]*"',
               '<meta property="og:title" content="%s"' % d['title'], s, count=1)
    s = re.sub(r'<meta property="og:description" content="[^"]*"',
               '<meta property="og:description" content="%s"' % d['meta'], s, count=1)
    # FAQ schema, generated from exactly the questions and answers on the page
    faq = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": question,
                           "acceptedAnswer": {"@type": "Answer", "text": strip_tags(answer)}}
                          for question, answer in faq_pairs(city, d)],
           "publisher": {"@id": "https://conferencevenues.com.au/#organization"},
           "about": {"@id": "https://conferencevenues.com.au/#organization"}}
    blob = ('<script type="application/ld+json">' + json.dumps(faq, ensure_ascii=False)
            + '</script>')
    old = re.search(r'<script type="application/ld\+json">\{"@context":"https://schema\.org",'
                    r'"@type":"FAQPage".*?</script>', s, re.S)
    if not old:
        old = re.search(r'<script type="application/ld\+json">\{"@context": "https://schema\.org", '
                        r'"@type": "FAQPage".*?</script>', s, re.S)
    if old:
        s = s[:old.start()] + blob + s[old.end():]
    else:
        s = s.replace('</head>', blob + '\n</head>', 1)
    return s


def grab(s, pattern):
    m = re.search(pattern, s, re.S)
    return m.group(0) if m else None


def build_full(city, d):
    path = os.path.join(ROOT, d['file'])
    s = io.open(path, encoding='utf-8').read()
    slug = slug_of(city)

    i = s.index('<main id="main">')
    j = s.index('</main>')
    head, main, tail = s[:i], s[i + len('<main id="main">'):j], s[j:]

    hero = grab(main, r'<section class="page-hero.*?</section>\s*')
    if not hero:
        sys.exit('%s: no hero section found' % d['file'])
    hero = re.sub(r'<h1>.*?</h1>', '<h1>%s</h1>' % d['h1'], hero, count=1, flags=re.S)
    hero = re.sub(r'<p class="lead">.*?</p>', '<p class="lead">%s</p>' % esc(d['lead']),
                  hero, count=1, flags=re.S)

    walked = grab(main, r'<section [^>]*id="%s-walked".*?</section>\s*' % re.escape(slug))
    subband = grab(main, r'<section class="sub-band">.*?</section>\s*')
    index = grab(main, r'<!-- city index, generated by build_city_index\.py -->.*?<!-- /city index -->')
    if not index:
        sys.exit('%s: no venue index block. Run build_city_index.py "%s" first.' % (d['file'], city))
    index = index.replace('<section class="s-stone pad" id="%s-index">' % slug,
                          '<section class="s-white pad" id="%s-index">' % slug, 1)

    intro = grab(main, r'<p class="lead" style="color:#37444f">.*?</p>') or ''

    parts = [hero]
    if walked:
        parts.append(walked)
    parts += [sec_snapshot(city, d),
              sec_sources(city, d, intro),
              sec_featured(city, d),
              index,
              sec_start(city, d),
              sec_local(city, d),
              sec_tradeoffs(city, d),
              sec_why(city, d),
              sec_faq(city, d),
              sec_related(city, d),
              sec_cta(city)]
    if subband:
        parts.append(subband)

    out = head + '<main id="main">\n\n' + '\n'.join(p.strip() for p in parts) + '\n\n' + tail
    out = patch_head(out, city, d)
    io.open(path, 'w', encoding='utf-8').write(out)
    print('%-42s rebuilt: %d featured, %d FAQs, %d trade-offs%s'
          % (d['file'], len(d['featured']), len(d['faqs']), len(d['tradeoffs']),
             ', walked band kept' if walked else ''))


def build_patch(city, d):
    """Sydney. Add only what the page is missing, touch nothing else."""
    path = os.path.join(ROOT, d['file'])
    s = io.open(path, encoding='utf-8').read()
    slug = slug_of(city)

    # Replace the existing FAQ band with the longer one.
    old_faq = grab(s, r'<section class="s-stone pad"><div class="wrap wrap--narrow">\s*'
                      r'<div class="section-head center"><span class="eyebrow eyebrow--center">FAQ.*?</section>')
    if old_faq:
        s = s.replace(old_faq, sec_faq(city, d), 1)
    elif ('id="%s-faq"' % slug) not in s:
        sys.exit('%s: could not find the FAQ band to replace' % d['file'])
    else:
        s = re.sub(r'<section class="s-stone pad" id="%s-faq".*?</section>' % re.escape(slug),
                   sec_faq(city, d), s, count=1, flags=re.S)

    # Trade-offs and related, immediately before the closing CTA band.
    for sec_id, builder in ((slug + '-tradeoffs', sec_tradeoffs),
                            (slug + '-related', sec_related)):
        block = builder(city, d)
        existing = grab(s, r'<section [^>]*id="%s".*?</section>' % re.escape(sec_id))
        if existing:
            s = s.replace(existing, block, 1)
        else:
            anchor = '<section class="cta-band pad">'
            k = s.index(anchor)
            s = s[:k] + block + '\n' + s[k:]

    # Keep the white / stone band rhythm on a page that already alternates:
    # why (white) -> trade-offs (stone) -> FAQ (white) -> related (stone) -> CTA.
    s = s.replace('<section class="s-stone pad" id="%s-faq"' % slug,
                  '<section class="s-white pad" id="%s-faq"' % slug, 1)
    s = s.replace('<section class="s-white pad" id="%s-related"' % slug,
                  '<section class="s-stone pad" id="%s-related"' % slug, 1)
    faq_block = grab(s, r'<section [^>]*id="%s-faq".*?</section>' % re.escape(slug))
    tr_block = grab(s, r'<section [^>]*id="%s-tradeoffs".*?</section>' % re.escape(slug))
    if faq_block and tr_block and s.index(tr_block) > s.index(faq_block):
        s = s.replace(tr_block, '', 1)
        s = s.replace(faq_block, tr_block + '\n' + faq_block, 1)

    s = patch_head(s, city, d)
    io.open(path, 'w', encoding='utf-8').write(s)
    print('%-42s patched: %d FAQs, %d trade-offs, %d related'
          % (d['file'], len(d['faqs']), len(d['tradeoffs']), len(d['related'])))


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for city in sorted(DEST):
        if only and city.lower() != only.lower():
            continue
        d = DEST[city]
        if d.get('mode') == 'patch':
            build_patch(city, d)
        else:
            build_full(city, d)


if __name__ == '__main__':
    main()
