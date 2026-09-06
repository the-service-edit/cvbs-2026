#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Make every FAQPage question match the question the page actually asks.

    python3 scripts/fix-faq-schema.py [--dry]

THE RULE THIS ENFORCES
    Google, General Structured Data Guidelines: "Don't mark up content that is
    not visible to readers of the page." The project already applies that rule
    to the venue ItemList. It was not being applied to the FAQ blocks.

WHAT WAS WRONG
    Several pages carried a FAQPage whose questions had been expanded for
    search and no longer matched the words on the page. The venue pages ask
    "What size conference can it hold?" on screen and claimed "What size
    conference can The Westin Brisbane hold?" in the markup. The answers were
    identical, so nothing was being faked, but the questions were markup a
    reader could not see, which is the violation.

WHAT IT DOES
    For each page, reads the visible question headings (.vg-q h3, summary,
    .faq h3/h4), then rewrites each FAQPage question to the visible wording it
    most closely matches. A schema question with no visible counterpart at all
    is removed and reported, because there is nothing on the page to back it.

    Answers are never touched. If an answer is wrong, that is a content
    problem, not a markup one.
"""
import io, json, os, re, sys, glob, difflib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = '--dry' in sys.argv

ENT = [('&amp;', '&'), ('&rsquo;', '’'), ('&lsquo;', '‘'),
       ('&ldquo;', '“'), ('&rdquo;', '”'), ('&#39;', "'"),
       ('&quot;', '"'), ('&nbsp;', ' '), ('&ndash;', '–'), ('&mdash;', '—')]


def unent(s):
    for a, b in ENT:
        s = s.replace(a, b)
    return s


def norm(s):
    s = unent(s).lower()
    s = re.sub(r'[^a-z0-9 ]+', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def visible_questions(html):
    out = []
    body = re.sub(r'<script.*?</script>', ' ', html, flags=re.S)
    for pat in (r'<div class="vg-q"[^>]*>\s*<h3[^>]*>(.*?)</h3>',
                r'<summary[^>]*>(.*?)</summary>',
                r'<h3 class="[^"]*faq[^"]*"[^>]*>(.*?)</h3>'):
        for m in re.finditer(pat, body, re.S):
            t = re.sub(r'<[^>]+>', '', m.group(1)).strip()
            if t and t not in out:
                out.append(t)
    return out


def main():
    pages = (sorted(glob.glob(os.path.join(ROOT, '*.html'))) +
             sorted(glob.glob(os.path.join(ROOT, 'venue-visits', '*', 'index.html'))))
    rewritten, dropped, clean = [], [], 0

    for p in pages:
        rel = os.path.relpath(p, ROOT)
        if rel.startswith(('_', 'CVBS-', 'cvbs-strategy', 'cvbs-landing', 'index-pro',
                           'index-video', 'index-strip', 'index-everlab')):
            continue
        s = io.open(p, encoding='utf-8').read()
        if '"FAQPage"' not in s:
            continue
        vis = visible_questions(s)
        # Values are stored decoded. JSON-LD is not HTML: an entity left in a
        # question is read literally, so a parser sees "ballroom&rsquo;s".
        vis_norm = dict((norm(v), unent(v)) for v in vis)
        changed = False

        def fix(m):
            nonlocal changed
            raw = m.group(0)
            inner = m.group(1)
            try:
                d = json.loads(inner)
            except Exception:
                return raw
            if not (isinstance(d, dict) and d.get('@type') == 'FAQPage'):
                return raw
            keep = []
            for q in d.get('mainEntity', []):
                name = q.get('name', '')
                n = norm(name)
                if unent(name) != name:
                    q['name'] = unent(name)
                    name = q['name']
                    changed = True
                a = q.get('acceptedAnswer', {})
                if isinstance(a, dict) and unent(a.get('text', '')) != a.get('text', ''):
                    a['text'] = unent(a['text'])
                    changed = True
                if n in vis_norm:
                    if unent(name) != vis_norm[n]:
                        q['name'] = vis_norm[n]
                        changed = True
                    keep.append(q)
                    continue
                near = difflib.get_close_matches(n, list(vis_norm), 1, 0.5)
                if near:
                    q['name'] = vis_norm[near[0]]
                    changed = True
                    rewritten.append('%s: "%s" -> "%s"' % (rel, name, q['name']))
                    keep.append(q)
                else:
                    dropped.append('%s: "%s"' % (rel, name))
                    changed = True
            d['mainEntity'] = keep
            if not keep:
                return ''
            return ('<script type="application/ld+json">' +
                    json.dumps(d, ensure_ascii=False, separators=(',', ':')) + '</script>')

        # An answer may legitimately contain a link, so the block cannot be
        # matched with a no-angle-bracket pattern. Match any JSON-LD script and
        # let fix() decide from the parsed @type.
        out = re.sub(r'<script type="application/ld\+json"[^>]*>(.*?)</script>',
                     fix, s, flags=re.S)
        if changed and not DRY:
            io.open(p, 'w', encoding='utf-8').write(out)
        if not changed:
            clean += 1

    print('pages already matching: %d' % clean)
    print('\nquestions rewritten to the visible wording: %d' % len(rewritten))
    for r in rewritten:
        print('  ' + r)
    print('\nquestions dropped, nothing on the page asks them: %d' % len(dropped))
    for d in dropped:
        print('  ' + d)
    if DRY:
        print('\n(dry run, nothing written)')


if __name__ == '__main__':
    main()
