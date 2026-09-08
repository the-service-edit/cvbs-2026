# -*- coding: utf-8 -*-
"""Fix white-on-teal fills in pages that carry their own inline palette.

Several pages ship a <style> block with their own copy of the palette rather
than using assets/css/site.css. Fixing the shared stylesheet on 6 September 2026
therefore left those pages behind, still painting white text on --teal-deep at
2.85:1 against a 4.5:1 requirement. The brief page's own header CTA was one of
them, which is the last button a visitor presses before enquiring.

Only public pages are touched. Internal tools and working documents keep their
own look.

Safe to re-run.

Usage: python3 scripts/fix-inline-palette.py
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Public pages only: sitemap plus the working filter page, which is noindex and
# therefore not in the sitemap but is very much part of the site.
def public_pages():
    sm = io.open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
    rels = []
    for loc in re.findall(r'<loc>([^<]+)</loc>', sm):
        rel = loc.split('/cvbs-2026/')[-1] or 'index.html'
        if rel.endswith('/'):
            rel += 'index.html'
        rels.append(rel)
    rels.append('venue-results.html')
    return [(r, os.path.join(ROOT, r)) for r in rels if os.path.exists(os.path.join(ROOT, r))]


# 7 Sep 2026: button fills reverted to the original brand teal at Mel's
# request. --teal-ink stays dark, it is text and has to stay readable.
ADD = ('--teal-btn:#32D9F3;--teal-btn-hover:#1FC4E0;--teal-ink:#197683;')

fixed = []
for rel, path in public_pages():
    s = io.open(path, encoding='utf-8').read()
    orig = s

    # 1. make the accessible tokens available inside the page's own palette
    if '--teal-deep:#32D9F3' in s and '--teal-btn:' not in s:
        s = s.replace('--teal-deep:#32D9F3;', '--teal-deep:#32D9F3;' + ADD, 1)

    # 2. any fill that carries white text moves to the readable teal
    s = re.sub(r'background:var\(--teal-deep\)(\s*;\s*(?:border-color:var\(--teal-deep\);\s*)?color:#fff)',
               r'background:var(--teal-btn)\1', s)
    s = re.sub(r'background:\s*var\(--teal-deep\)(\s*;\s*color:\s*#fff)',
               r'background:var(--teal-btn)\1', s)
    # hover states that darken from the same token
    s = s.replace('.nav-cta:hover{background:var(--teal-deep)', '.nav-cta:hover{background:var(--teal-btn-hover)')

    # 3. teal as ink inside an inline block
    s = s.replace('color:var(--teal-deep)', 'color:var(--teal-ink)')

    if s != orig:
        io.open(path, 'w', encoding='utf-8').write(s)
        fixed.append(rel)

print('%d public pages had their inline palette corrected' % len(fixed))
for r in fixed[:15]:
    print('   ' + r)
if len(fixed) > 15:
    print('   ... and %d more' % (len(fixed) - 15))
