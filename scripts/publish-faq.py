#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Put an invisible FAQPage onto the page it belongs to.

    python3 scripts/publish-faq.py

THE PROBLEM IT SOLVES
    how-to-choose-a-venue-finder.html carried six question and answer pairs in
    structured data and showed none of them to a reader. That is the same
    Google violation the ItemList rule exists for, and it was throwing away
    good content: those six answers are the most quotable writing on the site,
    and they were only ever addressed to a parser.

WHAT IT DOES
    Renders the page's own FAQPage entries as a visible section, in the site's
    existing details/summary FAQ pattern, immediately before the closing call
    to action. Nothing is rewritten. The answer text on the page is the answer
    text in the markup, which is the point.

Idempotent, and does nothing to a page that already shows its questions.
"""
import io, json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def visible(html):
    body = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    return re.sub(r'<[^>]+>', ' ', body)


def main():
    pages = sorted(glob.glob(os.path.join(ROOT, '*.html')))
    done = []
    for p in pages:
        rel = os.path.basename(p)
        if rel.startswith(('_', 'CVBS-', 'cvbs-strategy', 'cvbs-landing', 'index-')):
            continue
        s = io.open(p, encoding='utf-8').read()
        if '"FAQPage"' not in s:
            continue
        if 'id="published-faq"' in s:
            continue

        faq = None
        for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', s, re.S):
            try:
                d = json.loads(m.group(1))
            except Exception:
                continue
            if isinstance(d, dict) and d.get('@type') == 'FAQPage':
                faq = d
                break
        if not faq:
            continue

        text = visible(s)
        missing = [q for q in faq['mainEntity'] if q['name'] not in text]
        # Only step in when the page shows none of them. A page with a partial
        # mismatch is a wording problem, and fix-faq-schema.py handles that.
        if len(missing) != len(faq['mainEntity']):
            continue

        items = ''.join(
            '<details class="faq"><summary>%s</summary><div><p>%s</p></div></details>'
            % (q['name'], q['acceptedAnswer']['text']) for q in faq['mainEntity'])

        block = '''
<section class="s-stone pad" id="published-faq">
  <div class="wrap wrap--narrow">
    <span class="eyebrow">Common questions</span>
    <h2 class="h2">Choosing a venue finder, answered plainly.</h2>
    <div style="margin-top:2rem">%s</div>
  </div>
</section>
''' % items

        m = re.search(r'<section class="cta-band pad">', s)
        if not m:
            m = re.search(r'<footer class="site-footer">', s)
        if not m:
            continue
        s = s[:m.start()] + block + s[m.start():]
        io.open(p, 'w', encoding='utf-8').write(s)
        done.append('%s (%d questions)' % (rel, len(faq['mainEntity'])))

    print('FAQ blocks published: %d' % len(done))
    for d in done:
        print('  ' + d)


if __name__ == '__main__':
    main()
