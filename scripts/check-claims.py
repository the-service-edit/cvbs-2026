# -*- coding: utf-8 -*-
"""List every absolute claim on the public site, with its page and its sentence.

    python3 scripts/check-claims.py            everything
    python3 scripts/check-claims.py --strict   exit 1 if any unscoped claim is found

CVBS sells judgement. A superlative that turns out to be wrong does more damage
here than a slow page or an ugly button, because it is the product failing, not
the website. The 6 September 2026 audit found several: a whole city described as
"effectively blocked" for two months, a region with "no answer" above a capacity
we had simply not verified, and "every mainland delegate flies".

This is a review list, not a build gate. Read it before a launch and before
publishing a new destination, and either evidence each claim or scope it.

A claim is treated as SCOPED, and left alone, when the sentence around it says
whose knowledge it is: "we publish", "we have verified", "we have found",
"among the venues", "currently", "as at", or a named source. That is the
distinction the audit asked for: say what you know, not what exists.
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLAIMS = [
    (r'\bthe only\b',                'the only'),
    (r'\bno answer\b',               'no answer'),
    (r'\beffectively blocked\b',     'effectively blocked'),
    (r'\bunavailable\b',             'unavailable'),
    (r'\bnobody\b',                  'nobody'),
    (r'\bimpossible\b',              'impossible'),
    (r'\bevery\s+\w+\s+(?:delegate|venue|hotel|room)\b', 'every X'),
    (r'\bguarantee[ds]?\b',          'guarantee'),
    (r'\balways\b',                  'always'),
    (r'\bcannot be found\b',         'cannot be found'),
    (r'\bthe largest\b',             'the largest'),
    (r'\bthe biggest\b',             'the biggest'),
    (r'\bthe best\b',                'the best'),
]

# Wording that makes a claim honest: it says whose knowledge this is.
SCOPE = re.compile(
    r'\b(we publish|we have verified|we have found|we have not|among the|'
    r'currently|as at|verified|of the venues|we would|in our|that we|'
    r'publishes|published|according to|on file|we know of)\b', re.I)


def public_pages():
    sm = io.open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
    out = []
    for loc in re.findall(r'<loc>([^<]+)</loc>', sm):
        rel = loc.rstrip().split('/')[-1] or 'index.html'
        rel = loc.split('/cvbs-2026/')[-1] if '/cvbs-2026/' in loc else rel
        if rel.endswith('/'):
            rel += 'index.html'
        if not rel:
            rel = 'index.html'
        p = os.path.join(ROOT, rel)
        if os.path.exists(p):
            out.append((rel, p))
    return out


def sentences(html):
    body = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    body = re.sub(r'<style.*?</style>', ' ', body, flags=re.S)
    text = re.sub(r'<[^>]+>', ' ', body)
    text = re.sub(r'&[a-z]+;|&#\d+;', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return re.split(r'(?<=[.!?])\s+', text)


def main():
    strict = '--strict' in sys.argv
    unscoped, scoped = [], 0
    for rel, path in public_pages():
        for sent in sentences(io.open(path, encoding='utf-8').read()):
            for pat, label in CLAIMS:
                if re.search(pat, sent, re.I):
                    if SCOPE.search(sent):
                        scoped += 1
                    else:
                        unscoped.append((rel, label, sent.strip()[:200]))
                    break

    by_page = {}
    for rel, label, sent in unscoped:
        by_page.setdefault(rel, []).append((label, sent))

    print('=' * 74)
    print('ABSOLUTE CLAIMS ON THE PUBLIC SITE')
    print('=' * 74)
    print('%d scoped and fine. %d to review, across %d pages.\n'
          % (scoped, len(unscoped), len(by_page)))
    for rel in sorted(by_page, key=lambda r: -len(by_page[r])):
        print('%s  (%d)' % (rel, len(by_page[rel])))
        for label, sent in by_page[rel][:6]:
            print('   [%s] %s' % (label, sent))
        if len(by_page[rel]) > 6:
            print('   ... and %d more' % (len(by_page[rel]) - 6))
        print()
    print('Each one is either evidenced, or rewritten to say whose knowledge it is.')
    print('"The only venue in Sydney that..." becomes "the only one we publish that...".')

    # The truth to check the superlatives against, from the same dataset the
    # pages are built from. On 6 September 2026 a Cairns venue note claimed it
    # was the only room in the region above 650 while this table showed two
    # others in the same search market at 941 and 850.
    import json
    dp = os.path.join(ROOT, 'assets', 'data', 'venues.json')
    if os.path.exists(dp):
        rows = json.load(io.open(dp, encoding='utf-8'))['venues']
        cities = {}
        for v in rows:
            cities.setdefault(v['city'], []).append(v)
        print()
        print('=' * 74)
        print('THE THREE LARGEST WE PUBLISH IN EACH MARKET, TO CHECK CLAIMS AGAINST')
        print('=' * 74)
        for city in sorted(cities):
            top = sorted(cities[city], key=lambda v: -(v.get('th') or 0))[:3]
            top = [v for v in top if v.get('th')]
            if not top:
                print('%-22s no published theatre figures' % city)
                continue
            print('%-22s %s' % (city, ';  '.join(
                '%s %s theatre (%s)' % (v['n'], format(v['th'], ','), v['pr'])
                for v in top)))
    sys.exit(1 if (strict and unscoped) else 0)


if __name__ == '__main__':
    main()
