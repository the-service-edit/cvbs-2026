#!/usr/bin/env python3
"""Put the client review tools (/review/ and /weekly/) into a built STAGING artifact.

    python3 scripts/build.py --env staging --out DIR
    python3 scripts/add-review-tools.py --out DIR

Runs AFTER build.py has verified the artifact, so build.py's rule that no
internal tool ships stays true for production. Staging only: never run this
against a production artifact.

The staging site uses the production layout (about.html is served at /about/),
so review/pages.json is rewritten here to point each page at its staging
address, and carries a "route" so review.js can map a click inside the frame
back to the page id. Page ids stay the source filenames, so every note already
in the Sheet stays attached to its page.
"""
import argparse, csv, io, json, os, re, shutil, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = {
    'review': ['index.html', 'review.js', 'review.css', 'config.js', 'asks.json'],
    'weekly': ['index.html', 'hub.js', 'hub.css', 'config.js', 'bank.json', 'week.json'],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    out = a.out
    if not os.path.isfile(os.path.join(out, '.cvbs-artifact')):
        sys.exit('not a build.py artifact: %s' % out)
    if 'noindex' not in io.open(os.path.join(out, 'index.html'), encoding='utf-8').read()[:4000]:
        sys.exit('refusing: this looks like a production artifact (home page has no noindex)')

    route = {}
    with io.open(os.path.join(ROOT, '_site', 'pages.csv'), encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            if (r.get('source') or '').strip() and r['status'].strip() in ('live', 'preview'):
                route[r['source'].strip()] = r['path'].strip()

    for d, files in TOOLS.items():
        os.makedirs(os.path.join(out, d), exist_ok=True)
        for f in files:
            src = os.path.join(ROOT, d, f)
            if os.path.isfile(src):
                shutil.copyfile(src, os.path.join(out, d, f))

    # review/pages.json -> staging addresses
    pj = json.load(io.open(os.path.join(ROOT, 'review', 'pages.json'), encoding='utf-8'))
    kept, dropped = [], []
    for p in pj['pages']:
        prod = route.get(p['id'])
        target = (prod.lstrip('/') + 'index.html') if prod and prod.endswith('/') else (prod or '').lstrip('/')
        if not prod or not os.path.isfile(os.path.join(out, target)):
            dropped.append(p['id'])
            continue
        p['path'] = '../' + prod.lstrip('/')
        p['route'] = target
        kept.append(p)
    pj['pages'] = kept
    io.open(os.path.join(out, 'review', 'pages.json'), 'w', encoding='utf-8').write(json.dumps(pj, indent=1))

    # weekly json -> staging addresses for any site page it links
    def fix(m):
        src = m.group(2)
        prod = route.get(src)
        return m.group(1) + ('../' + prod.lstrip('/') if prod else '../' + src) + m.group(3)
    for f in ('bank.json', 'week.json'):
        p = os.path.join(out, 'weekly', f)
        if os.path.isfile(p):
            s = io.open(p, encoding='utf-8').read()
            s = re.sub(r'(")\.\./([^"#?]+\.html)([^"]*")', fix, s)
            io.open(p, 'w', encoding='utf-8').write(s)

    # asset stamp so reviewers do not keep a cached copy of the old tool
    print('review: %d pages, %d dropped %s' % (len(kept), len(dropped), dropped))
    if not kept:
        sys.exit('review list is empty')


if __name__ == '__main__':
    main()
