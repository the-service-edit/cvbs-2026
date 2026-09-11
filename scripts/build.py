# -*- coding: utf-8 -*-
"""Build the public CVBS website for one environment.

    python3 scripts/build.py --env staging     [--out DIR]
    python3 scripts/build.py --env production  [--out DIR] [--strict]

This is the only way the site leaves the repository. It replaces
scripts/build-public.sh and the retired scripts/set-base-url.py.

WHAT IT DOES
  1. Reads site.config.json (addresses), _site/pages.csv (every public page
     and its production path) and migration/url-map.csv (legacy URLs).
  2. Copies ONLY the pages in the manifest, each to its production path:
     about.html becomes /about/, venue-visits/qt-perth/ becomes /venues/qt-perth/.
  3. Rewrites every internal link, image and script path to that layout, and
     every absolute address to the environment's origin. An @id is never moved
     off the identity host, in any environment.
  4. Copies only the assets those pages, their CSS and their scripts actually
     use, plus a short explicit allowlist (email images, downloads, icons).
     Dotfiles, backups, READMEs, source originals and working files are
     refused even if something references them.
  5. Generates robots.txt, and for production the sitemap index, _redirects
     and _headers. Staging gets noindex on every page and a redirect stub at
     every old address, because Karen, AJ and sent emails hold old links.
  6. Verifies the artifact and exits non-zero on any failure. CI runs this, so
     a failing check blocks the deploy.

SOURCE STAYS AS IT IS. Generators keep writing about.html and
venue-visits/<slug>/ exactly as before. The production URL of each page lives
in _site/pages.csv and nowhere else. A page in sitemap.xml that is missing from
the manifest stops the build: every new page gets a deliberate URL.
"""
import argparse, csv, html, io, json, os, posixpath, re, shutil, sys, tempfile
from collections import defaultdict, OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, '_site'))
import siteconf as C                                                   # noqa: E402

FAIL = defaultdict(list)
WARN = defaultdict(list)

# Files that must be public even though no page links to them: images inside
# emails already sent, downloadable files, and the icons browsers ask for.
ASSET_ALLOW_DIRS = ('assets/img/email/', 'assets/downloads/')
ASSET_ALLOW_FILES = ('assets/img/favicon.png', 'assets/img/apple-touch-icon.png',
                     'assets/img/logo.png', 'favicon.ico')

# Never published, whatever references them.
DENY = re.compile(r'(^|/)(\.[^/]+|_[^/]*|README[^/]*|[^/]*\.(bak|md|py|pyc|gs|sh|csv|xlsx|docx|zip|txt|orig)'
                  r'|[^/]*\.pre-[^/]*|[^/]*\.fuse_hidden[^/]*)$|(^|/)_source/|(^|/)mock/', re.I)
DENY_OK = {'robots.txt', '_redirects', '_headers', '.nojekyll', '.cvbs-artifact'}
INTERNAL_DIRS = ('review/', 'weekly/', 'hub/', 'presentation/', 'Quote-Generator/',
                 'Post-Designer/', 'EDM-Designer/', 'brief-store/', 'email-templates/')

URL_ATTRS = re.compile(r'(\s(?:href|src|srcset|imagesrcset|poster|action|data-[a-z-]+|content)=)(["\'])(.*?)\2', re.S)
LD_BLOCK = re.compile(r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.S | re.I)
SCRIPT_BLOCK = re.compile(r'(<script\b(?![^>]*\bsrc=)(?![^>]*ld\+json)[^>]*>)(.*?)(</script>)', re.S | re.I)
URLISH = re.compile(r'^[\w./%-]+\.(html?|jpe?g|png|webp|avif|svg|gif|ico|pdf|mp4|webm|json|css|js)([?#].*)?$|^[\w./-]*/([?#].*)?$', re.I)


# --------------------------------------------------------------------- inputs
def load_manifest():
    rows = []
    with io.open(os.path.join(ROOT, '_site', 'pages.csv'), encoding='utf-8') as fh:
        for r in csv.DictReader(fh):
            r = {k: (v or '').strip() for k, v in r.items()}
            if not r.get('source'):
                continue
            p = r['path']
            if not (p.startswith('/') and (p.endswith('/') or p.endswith('.html'))):
                FAIL['manifest path must start with / and end with /'].append(p)
            rows.append(r)
    seen = defaultdict(list)
    for r in rows:
        seen[r['path']].append(r['source'])
    for p, s in seen.items():
        if len(s) > 1:
            FAIL['two pages claim one production path'].append('%s <- %s' % (p, ', '.join(s)))
    return rows


def sitemap_sources():
    s = io.open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8').read()
    out = OrderedDict()
    for block in re.findall(r'<url>(.*?)</url>', s, re.S):
        loc = re.search(r'<loc>(.*?)</loc>', block).group(1).strip()
        lm = re.search(r'<lastmod>(.*?)</lastmod>', block)
        rel = strip_host(loc)
        if rel is None:
            FAIL['sitemap entry on an unknown host'].append(loc)
            continue
        src = rel if rel and not rel.endswith('/') else rel + 'index.html'
        out[src] = lm.group(1).strip() if lm else ''
    return out


def load_legacy():
    p = os.path.join(ROOT, 'migration', 'url-map.csv')
    if not os.path.exists(p):
        return []
    with io.open(p, encoding='utf-8') as fh:
        return [{k: (v or '').strip() for k, v in r.items()} for r in csv.DictReader(fh)]


# ------------------------------------------------------------------ addresses
HOSTS = sorted({C.IDENTITY, C.ORIGIN} | set(C.LEGACY_HOSTS), key=len, reverse=True)


def strip_host(u):
    """Site-relative path for an absolute URL on any host this site has used, else None."""
    for h in HOSTS:
        if u == h:
            return ''
        if u.startswith(h + '/') or u.startswith(h + '#') or u.startswith(h + '?'):
            rest = u[len(h):]
            return rest[1:] if rest.startswith('/') else rest
    return None


class Mapper(object):
    def __init__(self, rows, env_name, env):
        self.env_name, self.env = env_name, env
        self.origin, self.base = env['origin'], env['basePath']
        self.pages = {}                     # source path -> production path
        for r in rows:
            if r['status'] == 'retired':
                target = r['redirect_to'] or '/'
            elif r['status'] == 'preview' and env_name == 'production':
                continue
            else:
                target = r['path']
            src = r['source']
            self.pages[src] = target
            if src.endswith('/index.html'):
                self.pages[src[:-len('index.html')]] = target
        self.pages.setdefault('index.html', '/')
        self.pages[''] = self.pages['index.html']
        self.assets = set()
        self.unresolved = defaultdict(set)

    def site_path(self, u, page_src):
        """Resolve u to (site-relative path, query+fragment) or None if external."""
        if not u or u.startswith(('#', 'mailto:', 'tel:', 'javascript:', 'data:', 'blob:', '//', '{', '$')):
            return None
        if re.match(r'^[a-z][a-z0-9+.-]*:', u, re.I):
            rel = strip_host(u)
            if rel is None:
                return None
            path = rel
        else:
            path = u if u.startswith('/') else posixpath.join(posixpath.dirname(page_src), u)
            if u.startswith('/'):
                path = path.lstrip('/')
                if self.base != '/' and ('/' + path).startswith(self.base):
                    path = ('/' + path)[len(self.base):]
        m = re.match(r'^([^?#]*)(.*)$', path)
        p, tail = m.group(1), m.group(2)
        if p:
            trailing = p.endswith('/')
            p = posixpath.normpath(p)
            p = '' if p == '.' else p
            if p.startswith('..'):
                return ('!' + p, tail)
            if trailing and p:
                p += '/'
        return (p, tail)

    def prod_path(self, p, page_src, where):
        if p in self.pages:
            return self.pages[p]
        if p.endswith('/') and p + 'index.html' in self.pages:
            return self.pages[p + 'index.html']
        clean = p.split('?')[0]
        if clean.startswith('assets/') or clean == 'favicon.ico':
            if os.path.isfile(os.path.join(ROOT, clean)):
                self.assets.add(clean)
            else:
                self.unresolved['missing file'].add('%s  (in %s)' % (clean, page_src))
            return '/' + clean
        self.unresolved[where].add('%s  (in %s)' % (p or '/', page_src))
        return '/' + p

    def address(self, prod):
        return self.origin + self.base + prod.lstrip('/')

    def local(self, prod):
        return self.base + prod.lstrip('/')

    def identity(self, prod):
        return C.IDENTITY + '/' + prod.lstrip('/')

    def map(self, u, page_src, kind='local', where='link to a page that is not published'):
        sp = self.site_path(u, page_src)
        if sp is None:
            return u
        p, tail = sp
        if p.startswith('!'):
            self.unresolved['link climbs above the site root'].add('%s  (in %s)' % (u, page_src))
            return u
        prod = self.prod_path(p, page_src, where)
        if kind == 'id':
            return self.identity(prod) + tail
        if kind == 'abs':
            return self.address(prod) + tail
        return self.local(prod) + tail


# ------------------------------------------------------------------ transform
def rewrite_ld(raw, mp, page_src):
    try:
        data = json.loads(raw)
    except Exception:
        WARN['JSON-LD block that does not parse, left as is'].append(page_src)
        return raw

    def walk(node, key=None):
        if isinstance(node, dict):
            return {k: walk(v, k) for k, v in node.items()}
        if isinstance(node, list):
            return [walk(v, key) for v in node]
        if isinstance(node, str) and re.match(r'^https?://', node) and strip_host(node) is not None:
            return mp.map(node, page_src, 'id' if key == '@id' else 'abs', 'structured data names an unpublished page')
        return node
    return json.dumps(walk(data), ensure_ascii=False, separators=(',', ':'))


JS_PAGE = re.compile(r'''(['"])((?:\.\./)*(?:[a-z0-9][a-z0-9-]*/)*[a-z0-9][a-z0-9-]*\.html)(?=[?#'"])''')
JS_ASSET = re.compile(r'''(['"])(?:\.\./|\./)*(assets/[A-Za-z0-9_./-]+)''')


def rewrite_js(js, mp, page_src):
    def page(m):
        target = posixpath.normpath(posixpath.join(posixpath.dirname(page_src), m.group(2)))
        if target in mp.pages:
            return m.group(1) + mp.local(mp.pages[target])
        return m.group(0)

    def asset(m):
        a = m.group(2)
        if os.path.isfile(os.path.join(ROOT, a)):
            mp.assets.add(a)
        return m.group(1) + mp.base + a
    return JS_ASSET.sub(asset, JS_PAGE.sub(page, js))


def transform(s, page_src, prod, mp, row):
    s = LD_BLOCK.sub(lambda m: m.group(1) + rewrite_ld(m.group(2), mp, page_src) + m.group(3), s)
    s = SCRIPT_BLOCK.sub(lambda m: m.group(1) + rewrite_js(m.group(2), mp, page_src) + m.group(3), s)

    # Script bodies are done. Park them so the attribute pass below cannot read
    # markup built inside a JS string (href="...' + x + '") as a real attribute.
    stash = []

    def park(m):
        stash.append(m.group(2))
        return m.group(1) + '\x00%d\x00' % (len(stash) - 1) + m.group(3)
    s = re.sub(r'(<script\b[^>]*>)(.*?)(</script>)', park, s, flags=re.S | re.I)

    def attr(m):
        name, q, val = m.group(1).strip()[:-1], m.group(2), m.group(3)
        raw = html.unescape(val)
        if name == 'content':
            if not re.match(r'^https?://', raw) or strip_host(raw) is None:
                return m.group(0)
            out = mp.map(raw, page_src, 'abs')
        elif name.startswith('data-') and not URLISH.match(raw) and strip_host(raw) is None:
            return m.group(0)
        elif name in ('srcset', 'data-srcset', 'imagesrcset'):
            parts = []
            for part in raw.split(','):
                bits = part.strip().split(None, 1)
                if bits:
                    bits[0] = mp.map(bits[0], page_src)
                    parts.append(' '.join(bits))
            out = ', '.join(parts)
        elif name == 'href' and re.search(r'rel=["\']canonical', m.string[max(0, m.start() - 60):m.start()]):
            out = mp.address(prod)
        else:
            absolute = bool(re.match(r'^https?://', raw))
            out = mp.map(raw, page_src, 'abs' if absolute else 'local')
        return m.group(1) + q + html.escape(out, quote=True).replace('&#x27;', "'") + q
    s = URL_ATTRS.sub(attr, s)
    s = re.sub('\x00(\\d+)\x00', lambda m: stash[int(m.group(1))], s)

    # canonical and og:url always name this page at its production path
    s = re.sub(r'(<link\s+rel=["\']canonical["\']\s+href=["\'])[^"\']*', lambda m: m.group(1) + mp.address(prod), s)
    s = re.sub(r'(<meta\s+property=["\']og:url["\']\s+content=["\'])[^"\']*', lambda m: m.group(1) + mp.address(prod), s)

    # robots
    want_noindex = (not mp.env['indexable']) or row.get('index') == 'no'
    robots = re.search(r'<meta\s+name=["\']robots["\']\s+content=["\']([^"\']*)["\'][^>]*>', s, re.I)
    if want_noindex:
        if robots and 'noindex' not in robots.group(1):
            s = s.replace(robots.group(0), '<meta name="robots" content="noindex, follow">')
        elif not robots:
            s = re.sub(r'(<head[^>]*>)', r'\1\n<meta name="robots" content="noindex, follow">', s, count=1)
    elif robots and 'noindex' in robots.group(1):
        FAIL['indexable page carries noindex'].append(row['source'])

    ep = mp.env.get('briefEndpoint')
    if ep and page_src == 'submit-a-brief.html':
        s, n = re.subn(r'(var BRIEF_ENDPOINT\s*=\s*")[^"]*(")', r'\g<1>%s\g<2>' % ep, s)
        if not n:
            FAIL['brief endpoint could not be set'].append(page_src)
    return s


def stub(target_local, target_abs, title):
    t = html.escape(title)
    return ('<!doctype html>\n<html lang="en-AU"><head><meta charset="utf-8">\n'
            '<title>%s | Moved</title>\n<meta name="robots" content="noindex, follow">\n'
            '<link rel="canonical" href="%s">\n<meta http-equiv="refresh" content="0; url=%s">\n'
            '<script>location.replace(%s + location.search + location.hash);</script>\n'
            '</head><body><p>This page has moved to <a href="%s">%s</a>.</p></body></html>\n'
            % (t, target_abs, target_local, json.dumps(target_local), target_local, target_abs))


def page_404(mp):
    src = io.open(os.path.join(ROOT, 'how-we-are-paid.html'), encoding='utf-8').read()
    main = re.search(r'<main\b.*?</main>', src, re.S)
    body = ('<main id="main"><section class="s-white"><div class="wrap" style="padding:96px 0 120px">'
            '<h1>We could not find that page</h1>'
            '<p>The address may be mistyped, or the page may have moved when this site was rebuilt.</p>'
            '<p><a class="btn btn--teal" href="index.html">Go to the home page</a> '
            '&nbsp; <a href="destinations.html">Browse destinations</a> &nbsp; '
            '<a href="submit-a-brief.html">Send us a brief</a></p></div></section></main>')
    s = src[:main.start()] + body + src[main.end():] if main else src
    s = LD_BLOCK.sub('', s)
    s = re.sub(r'<title>.*?</title>', '<title>Page not found | CVBS</title>', s, flags=re.S)
    s = re.sub(r'\s*<link\s+rel=["\']canonical["\'][^>]*>', '', s)
    s = re.sub(r'\s*<meta\s+property=["\']og:[^>]*>', '', s)
    s = re.sub(r'<meta\s+name=["\']robots["\'][^>]*>', '', s)
    s = re.sub(r'(<head[^>]*>)', r'\1\n<meta name="robots" content="noindex">', s, count=1)
    return s


# ---------------------------------------------------------------- generators
def headers_file(env):
    if not env.get('securityHeaders'):
        return '/*\n  X-Robots-Tag: noindex\n'
    csp = ("default-src 'self'; "
           "script-src 'self' 'unsafe-inline' https://conferencevenues.us8.list-manage.com; "
           "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
           "font-src 'self' https://fonts.gstatic.com; "
           "img-src 'self' data: https:; "
           "connect-src 'self' https://script.google.com https://script.googleusercontent.com; "
           "form-action 'self' https://conferencevenues.us8.list-manage.com; "
           "frame-ancestors 'none'; base-uri 'self'; object-src 'none'")
    return ('# Generated by scripts/build.py. The CSP is REPORT-ONLY until the inline\n'
            '# handlers are moved into site.js and a clean report period has passed.\n'
            '/*\n'
            '  Strict-Transport-Security: max-age=31536000\n'
            '  X-Content-Type-Options: nosniff\n'
            '  Referrer-Policy: strict-origin-when-cross-origin\n'
            '  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()\n'
            '  X-Frame-Options: DENY\n'
            '  Content-Security-Policy-Report-Only: %s\n'
            '/assets/*\n'
            '  Cache-Control: public, max-age=604800\n' % csp)


def sitemaps(out, rows, mp, lastmods):
    fam = OrderedDict()
    order = {'home': 'pages', 'core': 'pages', 'legal': 'pages'}
    for r in rows:
        if r['status'] != 'live' or r['index'] == 'no':
            continue
        name = order.get(r['family'], r['family'] + 's' if not r['family'].endswith('s') else r['family'])
        fam.setdefault(name, []).append(r)
    idx = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for name, rs in fam.items():
        fn = 'sitemap-%s.xml' % name
        lines = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
        latest = ''
        for r in rs:
            lm = lastmods.get(r['source'], '')
            latest = max(latest, lm)
            lines.append('<url><loc>%s</loc>%s</url>' % (mp.address(r['path']),
                         '<lastmod>%s</lastmod>' % lm if lm else ''))
        lines.append('</urlset>')
        write(out, fn, '\n'.join(lines) + '\n')
        idx.append('<sitemap><loc>%s</loc>%s</sitemap>' % (mp.address('/' + fn),
                   '<lastmod>%s</lastmod>' % latest if latest else ''))
    idx.append('</sitemapindex>')
    write(out, 'sitemap.xml', '\n'.join(idx) + '\n')
    return sum(len(v) for v in fam.values())


def redirects_file(rows, legacy, strict):
    lines = ['# Generated by scripts/build.py from _site/pages.csv and migration/url-map.csv.',
             '# Host-level rules (http to https, bare domain to www) belong in the host settings.']
    gone = []
    for r in rows:
        if r['status'] == 'retired':
            lines.append('%-48s %-40s 301' % (r['path'], r['redirect_to'] or '/'))
    lines.append('%-48s %-40s 301' % ('/venues/', '/venue-visits/'))
    for r in legacy:
        old, new, act = r.get('old_url', ''), r.get('new_path', ''), r.get('action', '').upper()
        if not old.startswith('/') or '*' in old or ',' in old:
            continue
        if act == '301' and new:
            lines.append('%-48s %-40s 301' % (old, new))
            if old.endswith('/') and old != '/':
                lines.append('%-48s %-40s 301' % (old.rstrip('/'), new))
        elif act == '410':
            gone.append(old)
        elif act == 'REVIEW':
            (FAIL if strict else WARN)['legacy URL still marked REVIEW'].append(old)
    if gone:
        lines.append('# 410 Gone, to be served by a host rule (not expressible in _redirects):')
        lines += ['#   %s' % g for g in gone]
    return '\n'.join(lines) + '\n'


# ---------------------------------------------------------------------- util
def write(out, rel, content):
    p = os.path.join(out, *rel.split('/'))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with io.open(p, 'w', encoding='utf-8') as fh:
        fh.write(content)


def out_file(prod):
    if prod.endswith('/'):
        return (prod.lstrip('/') + 'index.html')
    return prod.lstrip('/')


# -------------------------------------------------------------------- verify
def verify(out, mp, env_name, expected_pages):
    files = []
    for dp, dn, fn in os.walk(out):
        for f in fn:
            files.append(os.path.relpath(os.path.join(dp, f), out).replace(os.sep, '/'))
    fileset = set(files)
    for f in files:
        if DENY.search(f) and f not in DENY_OK:
            FAIL['file that must never be published'].append(f)
        if f.startswith(INTERNAL_DIRS):
            FAIL['internal tool in the public artifact'].append(f)
    org_ids = set()
    pages = [f for f in files if f.endswith('.html')]
    for f in pages:
        s = io.open(os.path.join(out, f), encoding='utf-8').read()
        is_stub = 'http-equiv="refresh"' in s[:800]
        if env_name == 'production' and ('github.io' in s or '/cvbs-2026/' in s):
            FAIL['staging address in the production artifact'].append(f)
        if env_name == 'staging' and not is_stub:
            if re.search(r'rel=["\']canonical["\']\s+href=["\']https://www\.conferencevenues', s):
                FAIL['staging page with a production canonical'].append(f)
            if not re.search(r'<meta name="robots" content="noindex', s):
                FAIL['staging page without noindex'].append(f)
        if f != '404.html' and not is_stub and len(re.findall(r'rel=["\']canonical', s)) != 1:
            FAIL['page without exactly one canonical'].append(f)
        for i in re.findall(r'"@id":"([^"]*#organization)"', s):
            org_ids.add(i)
        body = re.sub(r'(<script\b[^>]*>).*?(</script>)', r'\1\2', s, flags=re.S | re.I)
        refs = []
        for attr, u in re.findall(r'\s(href|src|srcset|imagesrcset|data-src|poster)=["\']([^"\']+)["\']', body):
            if attr in ('srcset', 'imagesrcset'):
                refs += [(attr, part.strip().split(' ')[0]) for part in u.split(',') if part.strip()]
            else:
                refs.append((attr, u))
        for attr, u in refs:
            if u.startswith(('#', 'mailto:', 'tel:', 'data:', 'javascript:')) or re.match(r'^[a-z]+://', u, re.I):
                continue
            if not u.startswith(mp.base) or u.startswith('//'):
                FAIL['relative or foreign-rooted internal reference left in a page'].append('%s -> %s' % (f, u))
                continue
            rel = u[len(mp.base):].split('#')[0].split('?')[0]
            cand = rel + 'index.html' if (rel == '' or rel.endswith('/')) else rel
            if cand not in fileset:
                FAIL['internal link or asset that does not resolve'].append('%s -> %s' % (f, u))
    bad = org_ids - {C.ORG_ID}
    if bad:
        FAIL['more than one Organization identity'].extend(sorted(bad))
    for f in ('robots.txt',):
        if f not in fileset:
            FAIL['missing generated file'].append(f)
    if env_name == 'production':
        for f in ('sitemap.xml', '_redirects', '_headers', '404.html'):
            if f not in fileset:
                FAIL['missing generated file'].append(f)
        red = io.open(os.path.join(out, '_redirects'), encoding='utf-8').read()
        for line in red.splitlines():
            if line.startswith('#') or not line.strip():
                continue
            target = line.split()[1]
            if out_file(target) not in fileset:
                FAIL['redirect to a page that is not in the artifact'].append(line.strip())
    n = len([p for p in pages if p in expected_pages])
    if n != len(expected_pages):
        FAIL['page count does not match the manifest'].append('%d of %d' % (n, len(expected_pages)))
    for f in files:
        if f.startswith('assets/img/') and os.path.getsize(os.path.join(out, f)) > 600 * 1024 \
                and not f.startswith('assets/img/email/'):
            WARN['image over 600 KB (performance budget)'].append('%s %d KB' % (f, os.path.getsize(os.path.join(out, f)) // 1024))
    return files


# ---------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--env', required=True, choices=sorted(C.CFG['environments']))
    ap.add_argument('--out')
    ap.add_argument('--strict', action='store_true', help='cutover mode: REVIEW rows in the legacy map fail the build')
    a = ap.parse_args()
    env = C.env(a.env)
    out = a.out or os.path.join(tempfile.gettempdir(), 'cvbs-%s' % a.env)
    out = os.path.abspath(out)
    if out in (ROOT, '/') or out.startswith(ROOT + os.sep) and not out.startswith(os.path.join(ROOT, 'public-dist')):
        sys.exit('Refusing to build inside the source tree: %s (use public-dist/ or a folder outside it)' % out)
    if os.path.exists(out):
        if not os.path.isfile(os.path.join(out, '.cvbs-artifact')):
            sys.exit('Refusing to replace %s: it is not a previous CVBS artifact.' % out)
        shutil.rmtree(out)
    os.makedirs(out)
    write(out, '.cvbs-artifact', a.env + '\n')

    rows = load_manifest()
    lastmods = sitemap_sources()
    live_sources = {r['source'] for r in rows if r['status'] == 'live'}
    for src in lastmods:
        if src not in live_sources:
            FAIL['in sitemap.xml but not in _site/pages.csv (give it a production path)'].append(src)
    for src in live_sources:
        if src not in lastmods:
            WARN['live in the manifest but missing from sitemap.xml'].append(src)

    mp = Mapper(rows, a.env, env)
    ship = []
    for r in rows:
        if r['status'] == 'live' or (r['status'] == 'preview' and a.env == 'staging'):
            if not os.path.isfile(os.path.join(ROOT, r['source'])):
                (WARN if r['status'] == 'preview' else FAIL)['manifest page missing on disk'].append(r['source'])
                continue
            ship.append(r)

    expected = set()
    for r in ship:
        s = io.open(os.path.join(ROOT, r['source']), encoding='utf-8').read()
        dest = out_file(r['path'])
        write(out, dest, transform(s, r['source'], r['path'], mp, r))
        expected.add(dest)

    write(out, '404.html', transform(page_404(mp), '404.html', '/404.html', mp, {'index': 'no', 'source': '404.html'}))

    # staging only: a stub at every old address, so bookmarks and sent emails still land
    stubs = 0
    if a.env == 'staging':
        for r in rows:
            if r['status'] == 'preview' and r not in ship:
                continue
            old = r['source']
            target = r['redirect_to'] if r['status'] == 'retired' else r['path']
            if out_file(target) == old or old == 'index.html':
                continue
            if os.path.exists(os.path.join(out, *old.split('/'))):
                continue
            write(out, old, stub(mp.local(target), mp.address(target), r['source']))
            stubs += 1

    # scripts and styles the pages load, with their own references followed
    queue = sorted(a_ for a_ in mp.assets if a_.endswith(('.js', '.css')))
    done = set()
    while queue:
        f = queue.pop()
        if f in done:
            continue
        done.add(f)
        txt = io.open(os.path.join(ROOT, f), encoding='utf-8').read()
        if f.endswith('.css'):
            for u in re.findall(r'url\(\s*["\']?([^"\')]+)', txt):
                if u.startswith(('data:', 'http', '#')):
                    continue
                t = posixpath.normpath(posixpath.join(posixpath.dirname(f), u.split('?')[0].split('#')[0]))
                if os.path.isfile(os.path.join(ROOT, t)):
                    mp.assets.add(t)
                else:
                    WARN['stylesheet points at a missing file'].append('%s -> %s' % (f, t))
            write(out, f, txt)
        else:
            before = set(mp.assets)
            write(out, f, rewrite_js(txt, mp, 'index.html'))
            queue += [x for x in mp.assets - before if x.endswith(('.js', '.css'))]

    for d in ASSET_ALLOW_DIRS:
        for dp, dn, fn in os.walk(os.path.join(ROOT, d)):
            for fname in fn:
                mp.assets.add(os.path.relpath(os.path.join(dp, fname), ROOT).replace(os.sep, '/'))
    for f in ASSET_ALLOW_FILES:
        if os.path.isfile(os.path.join(ROOT, f)):
            mp.assets.add(f)
    refused = []
    for f in sorted(mp.assets):
        if f in done:
            continue
        if DENY.search(f):
            refused.append(f)
            continue
        dst = os.path.join(out, *f.split('/'))
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(os.path.join(ROOT, f), dst)
    if refused:
        WARN['referenced but refused by the deny list'].extend(refused)

    # generated files
    if env['indexable']:
        n_sm = sitemaps(out, rows, mp, lastmods)
        write(out, 'robots.txt', 'User-agent: *\nAllow: /\n\nSitemap: %s\n' % mp.address('/sitemap.xml'))
    else:
        n_sm = 0
        write(out, 'robots.txt', '# Staging. Every page carries noindex; crawling stays open so it can be read.\n'
                                 'User-agent: *\nAllow: /\n')
    if a.env == 'production':
        write(out, '_redirects', redirects_file(rows, load_legacy(), a.strict))
    write(out, '_headers', headers_file(env))
    write(out, '.nojekyll', '')

    for where, items in mp.unresolved.items():
        WARN[where].extend(sorted(items))

    files = verify(out, mp, a.env, expected)

    print('CVBS %s build -> %s' % (a.env, out))
    print('  origin %s%s' % (env['origin'], env['basePath']))
    print('  %d pages, %d old-address stubs, %d assets, %d sitemap URLs, %d files in total'
          % (len(expected), stubs, len(mp.assets), n_sm, len(files)))
    for title, bucket in (('warn', WARN), ('FAIL', FAIL)):
        for k, v in bucket.items():
            print('%s  %s  (%d)' % (title, k, len(v)))
            for x in v[:12]:
                print('        ' + x)
            if len(v) > 12:
                print('        ... and %d more' % (len(v) - 12))
    if FAIL:
        print('\n%d failure types. Do not deploy this artifact.' % len(FAIL))
        sys.exit(1)
    print('\n0 failures.')


if __name__ == '__main__':
    main()
