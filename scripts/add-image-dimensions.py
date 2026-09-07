# -*- coding: utf-8 -*-
"""Write each image's real pixel size into its <img> tag.

229 of the 364 images on the public site carried no width and height. The
stylesheet has `img{max-width:100%;height:auto}`, so intrinsic dimensions
reserve the right space and the page stops jumping as photographs arrive.

The numbers are read off the files themselves, never estimated, so a tag can
never claim a shape the image does not have. An <img> whose src does not
resolve to a real file is left alone and reported: a missing dimension is a
performance problem, a wrong one is a layout bug.

Images inside a container that already fixes the shape (aspect-ratio, or
object-fit with width and height at 100%) are still given their intrinsic size.
That is harmless, because the CSS wins, and it is correct if the CSS ever moves.

Safe to re-run.

Usage: python3 scripts/add-image-dimensions.py [--dry-run]
"""
import io, os, re, sys

# An <img> tag is NOT `<img[^>]*>`. Several tags on this site carry an onerror
# fallback whose value contains a literal '>', e.g.
#   onerror="this.outerHTML='<div class=&quot;vrow__ph&quot;>ICC Sydney</div>'"
# A naive [^>]* match stops at that inner '>' and the dimensions get written
# INSIDE the attribute value with raw quotes, which closes the img tag early,
# leaks the fallback markup as visible text and emits a stray closing tag.
# That is what broke the Sydney destination page. Match quote-aware instead.
IMG_TAG = re.compile(r'''<img\b(?:[^>"']|"[^"]*"|'[^']*')*>''')

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRY = '--dry-run' in sys.argv
SKIP = ('_backup', '_to_delete', '_hero-review', '_original-backup', '_preview',
        '_vvcheck', '_superseded', 'Claude outputs', 'public-dist', '.git',
        '__pycache__')

try:
    from PIL import Image
except ImportError:
    Image = None

SIZE_CACHE = {}


def size_of(path):
    if path in SIZE_CACHE:
        return SIZE_CACHE[path]
    out = None
    if Image is not None:
        try:
            with Image.open(path) as im:
                out = im.size
        except Exception:
            out = None
    SIZE_CACHE[path] = out
    return out


def pages():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not any(s in d for s in SKIP)]
        if any(s in dirpath for s in SKIP):
            continue
        for fn in filenames:
            if fn.endswith('.html') and not fn.startswith('_backup'):
                yield os.path.join(dirpath, fn)


added = 0
unresolved = []
touched = []

for path in pages():
    s = io.open(path, encoding='utf-8').read()
    base = os.path.dirname(path)
    out = []
    last = 0
    n_here = 0

    for m in IMG_TAG.finditer(s):
        tag = m.group(0)
        # Skip if EITHER dimension is already present. Appending to a tag that
        # already carries height="38" (the logo walls) produced a duplicate
        # attribute pair; the browser kept the first height and the last width,
        # giving a 33:1 aspect ratio and blowing the logos out. 7 Sep 2026.
        if re.search(r'\bwidth=', tag) or re.search(r'\bheight=', tag):
            continue
        src = re.search(r'\bsrc="([^"]+)"', tag)
        if not src:
            continue
        ref = src.group(1).split('?')[0]
        if ref.startswith(('http://', 'https://', 'data:')):
            continue
        target = os.path.normpath(os.path.join(base, ref))
        wh = size_of(target)
        if not wh:
            unresolved.append((os.path.relpath(path, ROOT), ref))
            continue
        new = tag[:-1].rstrip()
        if new.endswith('/'):
            new = new[:-1].rstrip()
        new += ' width="%d" height="%d">' % wh
        if new.count('"') % 2:
            # unbalanced quotes means the tag was mis-parsed; never write it
            unresolved.append((os.path.relpath(path, ROOT), ref + '  [unbalanced quotes, skipped]'))
            continue
        out.append(s[last:m.start()])
        out.append(new)
        last = m.end()
        n_here += 1

    if n_here:
        out.append(s[last:])
        if not DRY:
            io.open(path, 'w', encoding='utf-8').write(''.join(out))
        touched.append((os.path.relpath(path, ROOT), n_here))
        added += n_here

touched.sort(key=lambda x: -x[1])
print('%s%d dimensions written across %d files'
      % ('(dry run) ' if DRY else '', added, len(touched)))
for rel, n in touched[:12]:
    print('   %4d  %s' % (n, rel))
if len(touched) > 12:
    print('   ... and %d more files' % (len(touched) - 12))

if unresolved:
    print('\n%d <img> tags whose file could not be read. Left untouched:' % len(unresolved))
    seen = set()
    for rel, ref in unresolved:
        if ref in seen:
            continue
        seen.add(ref)
        print('   %-46s %s' % (ref[:46], rel))
        if len(seen) >= 12:
            print('   ...')
            break
