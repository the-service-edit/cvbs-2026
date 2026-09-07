#!/usr/bin/env python3
"""
CVBS primary CTA relabel, 7 Sep 2026.
Three CTAs allocated by funnel stage, title case, city pages kept local.

  Group A  Get My Shortlist            main conversion path + site furniture
  Group B  Tell Us About Your Event    consideration pages, where they are still learning
  Group C  Start Your Brief            mid-flow only: the brief-bar widget and form submits

Run with --apply to write. Default is a dry run.
"""
import os, re, sys, collections

APPLY = '--apply' in sys.argv
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Pages where the visitor is still learning. Body CTAs here get Group B.
CONSIDERATION = {
 'about.html','blog-index.html','cbd-vs-resort-conference-venues.html',
 'conference-budget-calculator.html','conference-budget-guide.html',
 'conference-venue-checklist.html','contact.html','faq.html','how-it-works.html',
 'how-much-does-a-conference-venue-cost.html','how-to-brief-a-venue-finder.html',
 'how-to-choose-a-conference-venue.html','how-to-choose-a-venue-finder.html',
 'how-we-are-paid.html','privacy.html','resources.html','terms.html',
 'venue-sourcing-company-vs-booking-direct.html','what-is-conference-venue-sourcing.html',
}
def is_consideration(path):
    b = os.path.basename(path)
    return b in CONSIDERATION or '/venue-visits/' in path.replace(os.sep,'/')

A = 'Get My Shortlist'
B = 'Tell Us About Your Event'
C = 'Start Your Brief'

def live_pages():
    sm = open(os.path.join(ROOT,'sitemap.xml'),encoding='utf-8').read()
    urls = re.findall(r'<loc>([^<]*)</loc>', sm)
    out=[]
    for u in urls:
        rel = re.sub(r'^https?://[^/]*/','',u)
        rel = re.sub(r'^cvbs-2026/','',rel)
        if rel=='' : rel='index.html'
        if rel.endswith('/'): rel += 'index.html'
        p = os.path.join(ROOT, rel)
        if os.path.isfile(p): out.append(p)
    return out

# text node only: must sit straight after a '>' so hrefs and attributes are untouchable
PAT = re.compile(r'(?<=>)(\s*)(?:Start your ((?:[A-Z][A-Za-z]+(?: [A-Z][A-Za-z]+)? )?)brief|Find my venues?|Find your venue)')

def classify(head, path):
    """head is the markup immediately before the match."""
    if re.search(r'<button[^>]*>$', head[-300:]): return 'C','form submit'
    if 'brief-bar' in head[-400:]:            return 'A','brief-bar widget'
    if 'nav-cta' in head[-250:]:              return 'A','nav CTA'
    if 'mobile-menu' in head[-450:]:          return 'A','mobile menu'
    if re.search(r'<footer', head, re.I) and '</footer>' not in head[head.rfind('<footer'):]:
        return 'A','footer link list'
    if is_consideration(path):                return 'B','body CTA, consideration page'
    return 'A','body CTA, conversion page'

def main():
    pages = live_pages()
    counts = collections.Counter(); bycity=collections.Counter()
    detail = collections.defaultdict(list); skipped=[]
    changed_files = 0

    for p in pages:
        s = open(p,encoding='utf-8',errors='replace').read()
        orig = s
        out=[]; last=0
        for m in PAT.finditer(s):
            head = s[:m.start()]
            # never touch the document title or a meta tag
            tail_open = head.rfind('<'); 
            if re.search(r'<(title|meta|option)\b[^>]*>\s*$', head[-120:], re.I):
                skipped.append((p,'title/meta/option')); continue
            if re.search(r'<span[^>]*class="[^"]*eyebrow[^"]*"[^>]*>$', head[-160:]):
                skipped.append((p,'eyebrow label')); continue
            grp, ctx = classify(head, p)
            city = (m.group(2) or '').strip()
            if grp=='A':
                new = 'Get My %s Shortlist' % city if city else A
                if city: bycity[city]+=1
            elif grp=='B':
                new = B
            else:
                new = C
            out.append(s[last:m.start()]); out.append(m.group(1)+new); last=m.end()
            counts[(grp,ctx)] += 1
            if len(detail[(grp,ctx)])<2:
                detail[(grp,ctx)].append('%s :: %s -> %s'%(os.path.relpath(p,ROOT),m.group(0).strip(),new))
        out.append(s[last:])
        s=''.join(out)
        if s!=orig:
            changed_files+=1
            if APPLY: open(p,'w',encoding='utf-8').write(s)

    print('%s  |  %d live pages scanned, %d would change\n' % ('APPLIED' if APPLY else 'DRY RUN', len(pages), changed_files))
    tot=0
    for grp,label in (('A',A),('B',B),('C',C)):
        rows=[(k,v) for k,v in counts.items() if k[0]==grp]
        n=sum(v for _,v in rows); tot+=n
        print('  %s  "%s"   %d buttons' % (grp,label,n))
        for (g,ctx),v in sorted(rows,key=lambda r:-r[1]):
            print('        %-32s %4d' % (ctx,v))
            for d in detail[(g,ctx)]: print('            %s'%d)
    print('\n  total replaced: %d'%tot)
    if bycity:
        print('  city variants kept local: %d across %d cities'%(sum(bycity.values()),len(bycity)))
        print('     ',', '.join('%s(%d)'%(c,n) for c,n in sorted(bycity.items())))
    if skipped:
        print('  skipped (title/meta/option): %d'%len(skipped))

main()
