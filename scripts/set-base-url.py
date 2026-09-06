# -*- coding: utf-8 -*-
"""Move the whole site from one address to another, in one command.

    python3 scripts/set-base-url.py https://conferencevenues.com.au

Every fetchable address on this site is built from one base: canonicals,
og:url, the sitemap, the robots Sitemap line, the structured data url fields
and the BASE constant inside each generator. Before 6 September 2026 those
were not in agreement. The canonicals said the GitHub host while every piece
of structured data said conferencevenues.com.au, so each page claimed two
different addresses and one of them was always wrong.

This script is the cutover. It rewrites all of them together, refuses to run
on a malformed base, and prints what it touched. Run the generator chain
afterwards, then scripts/check-site.py, which fails if any address is left
pointing at a host that is no longer the base.

Entity identifiers are deliberately NOT rewritten. The @id values in the
entity graph are names, not addresses, and they stay on conferencevenues.com.au
for the life of the business. See the note at the top of _entity-source/entity.py.
"""
import io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Every host this site has ever been served from. Anything found here is moved
# onto the new base. Add to this list rather than editing history.
KNOWN = [
    "https://the-service-edit.github.io/cvbs-2026",
    "https://conferencevenues.com.au",
]

SKIP_DIRS = ("_backup", "_to_delete", "_hero-review", "_original-backup",
             "_preview-site-visits", "_vvcheck", "__pycache__", ".git",
             "Claude outputs", "_superseded", "public-dist", "node_modules")

EXTS = (".html", ".xml", ".txt", ".py", ".js", ".sh")

ID_TAIL = re.compile(r'^/#(organization|website|service|logo|[a-z]+-[a-z]+)$')


def walk():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if not any(s in d for s in SKIP_DIRS)]
        if any(s in dirpath for s in SKIP_DIRS):
            continue
        for fn in filenames:
            if fn.endswith(EXTS):
                yield os.path.join(dirpath, fn)


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    new = sys.argv[1].rstrip("/")
    if not re.match(r'^https://[a-z0-9.-]+\.[a-z]{2,}(/[A-Za-z0-9._~/-]*)?$', new):
        print("Refusing a base that is not a plain https address: %r" % new)
        sys.exit(1)

    olds = [h for h in KNOWN if h != new]
    changed, total = [], 0

    for path in walk():
        rel = os.path.relpath(path, ROOT)
        if rel == os.path.join("scripts", "set-base-url.py"):
            continue
        try:
            s = io.open(path, encoding="utf-8").read()
        except (UnicodeDecodeError, IOError):
            continue
        orig = s
        hits = 0

        if rel.replace(os.sep, "/").endswith("_entity-source/entity.py"):
            s2 = re.sub(r'^SERVE = "[^"]*"', 'SERVE = "%s"' % new, s, flags=re.M)
            if s2 != s:
                hits += 1
            s = s2

        for old in olds:
            if old not in s:
                continue
            n_before = len(re.findall(re.escape(old), s))

            def repl(m):
                tail = m.group(1) or ""
                if ID_TAIL.match(tail):
                    return m.group(0)
                return new + tail

            s = re.sub(re.escape(old) + r'(/[^\s"\'<>)\]]*)?', repl, s)
            hits += n_before - len(re.findall(re.escape(old), s))

        if s != orig:
            io.open(path, "w", encoding="utf-8").write(s)
            changed.append((rel, hits))
            total += hits

    changed.sort(key=lambda x: -x[1])
    print("Base URL is now: %s" % new)
    print("%d files rewritten, %d addresses moved" % (len(changed), total))
    for rel, n in changed[:15]:
        print("   %5d  %s" % (n, rel))
    if len(changed) > 15:
        print("   ... and %d more files" % (len(changed) - 15))
    print()
    print("Now run the generator chain in the order in _venue-index-source/BUILD.md,")
    print("then scripts/check-site.py. It will fail if any address was missed.")


if __name__ == "__main__":
    main()
