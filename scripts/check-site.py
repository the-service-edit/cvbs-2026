#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Whole site check: links, metadata, schema, indexation, orphans.

    python3 scripts/check-site.py

Runs over every page in sitemap.xml plus the venue pages, and reports anything
that would embarrass the site in front of a crawler or a person: a link that
goes nowhere, a page with two canonicals, structured data that names something
the page does not show, a page nothing links to.

Exit code 1 if anything in the FAIL list is non-empty.
"""
import io, json, os, re, sys, glob
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# The base is owned by _entity-source/entity.py. Reading it here means this
# check follows a cutover automatically instead of quietly validating the old
# host after scripts/set-base-url.py has moved the site.
sys.path.insert(0, os.path.join(ROOT, '_entity-source'))
import entity as _E                                            # noqa: E402
BASE = _E.SERVE.rstrip('/') + '/'
IDENTITY = _E.SITE.rstrip('/')

# Hosts this site has been served from. Any of them still appearing in a
# fetchable address after a cutover is a failure, not a warning: it means a
# page is telling Google it lives somewhere it does not.
FOREIGN_HOSTS = [h for h in ('https://the-service-edit.github.io/cvbs-2026',
                             'https://conferencevenues.com.au')
                 if not BASE.startswith(h)]

SKIP_PREFIX = ('_backup', '_original', '_preview', '_vv', '_hero', '_superseded',
               'CVBS-', 'cvbs-strategy', 'cvbs-landing', 'cvbs-services',
               'index-pro', 'index-video', 'index-strip', 'index-everlab',
               # offer-*.html are meta refresh stubs kept so old offer links
               # still land somewhere. They carry noindex and no content, and
               # holding them to page rules produces noise, not findings.
               'offer-')
SKIP_DIR = ('presentation', 'hub', 'Quote-Generator', 'Post-Designer', 'EDM-Designer',
            'email-templates', 'instagram-carousels', '_venue-index-source',
            '_venue-visits-source', '_entity-source', '_edm-source', '_scope-source',
            '_skills', '_to_delete', 'CVBS-Website-Presentation', 'Claude outputs',
            'site-visits', '_DROP PHOTOS HERE')

FAIL = defaultdict(list)
WARN = defaultdict(list)


def site_pages():
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, '*.html'))):
        b = os.path.basename(p)
        if any(b.startswith(s) for s in SKIP_PREFIX):
            continue
        out.append(p)
    out += sorted(glob.glob(os.path.join(ROOT, 'venue-visits', '*.html')))
    out += sorted(glob.glob(os.path.join(ROOT, 'venue-visits', '*', 'index.html')))
    return out


def rel_of(p):
    return os.path.relpath(p, ROOT).replace(os.sep, '/')


def main():
    pages = site_pages()
    print('checking %d pages\n' % len(pages))

    sm = io.open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
    sitemap = set(re.findall(r'<loc>([^<]+)</loc>', sm))
    sitemap_rel = set(u.replace(BASE, '') for u in sitemap)

    robots = io.open(os.path.join(ROOT, 'robots.txt'), encoding='utf-8').read()
    disallowed = set(l.split(':', 1)[1].strip().lstrip('/')
                     for l in robots.splitlines() if l.startswith('Disallow:'))

    inbound = defaultdict(set)

    for p in pages:
        rel = rel_of(p)
        s = io.open(p, encoding='utf-8').read()
        base_dir = os.path.dirname(p)

        # --- head basics
        if len(re.findall(r'<title>', s)) != 1:
            FAIL['title'].append(rel)
        if len(re.findall(r'rel="canonical"', s)) != 1:
            FAIL['canonical count'].append(rel)

        # --- one address for the whole site
        can = re.search(r'rel="canonical" href="([^"]+)"', s)
        if can and not can.group(1).startswith(BASE):
            FAIL['canonical on the wrong host'].append('%s -> %s' % (rel, can.group(1)))
        og = re.search(r'property="og:url" content="([^"]+)"', s)
        if og and not og.group(1).startswith(BASE):
            FAIL['og:url on the wrong host'].append('%s -> %s' % (rel, og.group(1)))
        for host in FOREIGN_HOSTS:
            for m in set(re.findall(r'"url":\s*"(%s[^"]*)"' % re.escape(host), s)):
                if not m.startswith(IDENTITY + '/#'):
                    FAIL['structured data on the wrong host'].append('%s -> %s' % (rel, m))
        if not re.search(r'<meta name="description" content="[^"]{40,}"', s):
            FAIL['meta description'].append(rel)
        if len(re.findall(r'<h1[ >]', s)) != 1:
            n = len(re.findall(r'<h1[ >]', s))
            (FAIL if n == 0 else WARN)['h1 count'].append('%s (%d)' % (rel, n))

        robots_meta = re.search(r'<meta name="robots" content="([^"]*)"', s)
        noindex = bool(robots_meta and 'noindex' in robots_meta.group(1))

        # --- indexation coherence
        if noindex and rel in sitemap_rel:
            FAIL['noindex page in sitemap'].append(rel)
        if not noindex and rel not in sitemap_rel and rel.endswith('.html') \
                and '/' not in rel and rel not in disallowed:
            WARN['indexable but not in sitemap'].append(rel)

        # --- schema
        for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', s, re.S):
            try:
                json.loads(m.group(1))
            except Exception as e:
                FAIL['invalid JSON-LD'].append('%s: %s' % (rel, e))

        # ItemList entries must be visible in the page text
        text = re.sub(r'<script.*?</script>', ' ', s, flags=re.S)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = text.replace('&amp;', '&').replace('&rsquo;', '’').replace('&#39;', "'")
        for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', s, re.S):
            try:
                d = json.loads(m.group(1))
            except Exception:
                continue
            if isinstance(d, dict) and d.get('@type') == 'ItemList':
                miss = [it['item']['name'] for it in d.get('itemListElement', [])
                        if it.get('item', {}).get('name')
                        and it['item']['name'].replace('&', '&') not in text]
                if miss:
                    FAIL['ItemList names not visible'].append('%s: %s' % (rel, miss[:4]))
                if d.get('numberOfItems') and d['numberOfItems'] != len(d.get('itemListElement', [])):
                    FAIL['ItemList numberOfItems wrong'].append(rel)
            if isinstance(d, dict) and d.get('@type') == 'FAQPage':
                miss = [q['name'] for q in d.get('mainEntity', [])
                        if q.get('name') and q['name'].replace('&#39;', "'") not in text]
                if miss:
                    FAIL['FAQ questions not visible'].append('%s: %s' % (rel, miss[:3]))

        # --- internal links
        for href in re.findall(r'href="([^"]+)"', s):
            if href.startswith(('http', 'mailto:', 'tel:', '#', 'data:', '//')):
                continue
            clean = href.split('#')[0].split('?')[0]
            if not clean:
                continue
            target = os.path.normpath(os.path.join(base_dir, clean))
            if os.path.isdir(target):
                target = os.path.join(target, 'index.html')
            if not os.path.exists(target):
                FAIL['broken link'].append('%s -> %s' % (rel, href))
            else:
                inbound[rel_of(target)].add(rel)

        for src in re.findall(r'src="([^"]+)"', s):
            if src.startswith(('http', 'data:', '//')):
                continue
            clean = src.split('?')[0]
            t = os.path.normpath(os.path.join(base_dir, clean))
            if not os.path.exists(t):
                FAIL['missing asset'].append('%s -> %s' % (rel, src))

    # --- orphans
    for p in pages:
        rel = rel_of(p)
        if rel in ('index.html',):
            continue
        if not inbound.get(rel):
            WARN['orphan, nothing links to it'].append(rel)

    # --- sitemap targets exist
    for u in sorted(sitemap):
        r = u.replace(BASE, '')
        t = os.path.join(ROOT, r)
        if r.endswith('/'):
            t = os.path.join(t, 'index.html')
        if not os.path.exists(t):
            FAIL['sitemap points at a missing file'].append(r)

    print('=' * 62)
    for k in sorted(FAIL):
        print('FAIL  %-38s %d' % (k, len(FAIL[k])))
        for v in FAIL[k][:12]:
            print('        ' + v)
        if len(FAIL[k]) > 12:
            print('        ... and %d more' % (len(FAIL[k]) - 12))
    for k in sorted(WARN):
        print('warn  %-38s %d' % (k, len(WARN[k])))
        for v in WARN[k][:12]:
            print('        ' + v)
        if len(WARN[k]) > 12:
            print('        ... and %d more' % (len(WARN[k]) - 12))
    print('=' * 62)
    print('%d failures, %d warnings' % (sum(len(v) for v in FAIL.values()),
                                        sum(len(v) for v in WARN.values())))
    sys.exit(1 if FAIL else 0)


if __name__ == '__main__':
    main()
