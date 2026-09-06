# -*- coding: utf-8 -*-
"""Move every inline "teal as ink" declaration onto --teal-ink.

--teal-deep measures 2.85:1 against white and 2.60:1 against the stone band.
That fails 4.5:1 for body text and 3:1 for icons and large text, so anywhere it
was used as a foreground it was unreadable by the standard, not only on the
primary button. The stylesheet was moved on 6 September 2026; this does the same
for the inline styles in the pages and, more importantly, in the generators that
write them, so a rebuild cannot put the old colour back.

Only `color:` declarations change. `background:` and `border-color:` keep
--teal-deep, because nothing has to be read off a fill.

Safe to re-run.

Usage: python3 scripts/fix-teal-ink.py
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP = ('_backup', '_to_delete', '_hero-review', '_original-backup', '_preview',
        '_vvcheck', '_superseded', 'Claude outputs', 'public-dist', '.git',
        '__pycache__', 'node_modules')
EXTS = ('.html', '.py', '.js')

# color:var(--teal-deep) in any spacing, but never background or border.
PAT = re.compile(r'(?<!-)\bcolor\s*:\s*var\(--teal-deep\)')

changed, total = [], 0
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if not any(s in d for s in SKIP)]
    if any(s in dirpath for s in SKIP):
        continue
    for fn in filenames:
        if not fn.endswith(EXTS) or fn == 'fix-teal-ink.py':
            continue
        path = os.path.join(dirpath, fn)
        if path.endswith(os.path.join('assets', 'css', 'site.css')):
            continue
        try:
            s = io.open(path, encoding='utf-8').read()
        except (UnicodeDecodeError, IOError):
            continue
        n = len(PAT.findall(s))
        if not n:
            continue
        io.open(path, 'w', encoding='utf-8').write(PAT.sub('color:var(--teal-ink)', s))
        changed.append((os.path.relpath(path, ROOT), n))
        total += n

changed.sort(key=lambda x: -x[1])
print('%d declarations moved to --teal-ink across %d files' % (total, len(changed)))
for rel, n in changed[:12]:
    print('   %4d  %s' % (n, rel))
if len(changed) > 12:
    print('   ... and %d more files' % (len(changed) - 12))
