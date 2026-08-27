#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CVBS site visit intake.

WHAT THIS IS FOR
    The site visit log stayed empty because filling in a spreadsheet is a chore
    nobody does. The team already sends photographs. Every photograph carries
    the date it was taken, so this script reads the log out of the photos
    instead of asking anyone to write it down.

HOW IT IS USED
    1. Make a folder per venue inside "_DROP PHOTOS HERE/site-visits/",
       named after the venue. "icc-sydney", "ICC Sydney", "icc sydney" all work.
    2. Drop the photographs in. Phone photos are fine. HEIC is fine.
    3. Run:  python3 scripts/site-visit-intake.py
       First run writes a notes.txt into each folder, already filled in with the
       visit date it found and the photos in the order they were taken.
    4. Write one line per photo in notes.txt. A thirty second voice note
       transcribed is fine. Uncaptioned photos are not published.
    5. Run it again. It resizes, strips the location data, writes the record
       into the page, and tells you what it did.

    Add --dry-run to see what it would do without writing anything.

THE ONE RULE FOR CAPTIONS
    Write fit, not fault. Venues pay our commission. "Comfortable at 200, tight
    at 400" reads as expertise and a venue would happily forward it. "The room
    is too small" reads as a review. Say what the room suits and who it does not
    suit, never what is wrong with it.

WHAT IT NEVER DOES
    It never types a date. The date is read off the photograph. If a photo has
    no date in its metadata the script says so and refuses to guess, because a
    guessed visit date is a fabricated claim and one of those costs the page
    everything it is for.
    It never publishes GPS. Coordinates are printed here for you to check the
    photo really is the venue, then stripped from every published file.
"""

import io, json, os, re, subprocess, sys, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DROP = os.path.join(ROOT, '_DROP PHOTOS HERE', 'site-visits')
OUT_DIR = os.path.join(ROOT, 'assets', 'img', 'site-visits')
JSON_PATH = os.path.join(ROOT, '_venue-index-source', 'site_visits.json')
PAGES = {'Sydney': os.path.join(ROOT, 'venue-finder-sydney.html')}

WIDTHS = [('s', 900), ('l', 1600)]
QUALITY = 82
DRY = '--dry-run' in sys.argv

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June',
          'July', 'August', 'September', 'October', 'November', 'December']

try:
    from PIL import Image, ImageOps
    from PIL.ExifTags import TAGS, GPSTAGS
except ImportError:
    sys.exit('Pillow is not installed. Run:  python3 -m pip install --user Pillow')


def slug(s):
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', s.lower())).strip('-')


def say(*a):
    print(*a)


# ---------------------------------------------------------------- venue names
def venue_names(page):
    """Read the venue names straight out of the page, so this script and the
    index can never disagree about what a venue is called."""
    s = io.open(page, encoding='utf-8').read()
    m = re.search(r'<script type="application/json" id="vidx-data">(.*?)</script>', s, re.S)
    if not m:
        return []
    return [v['n'] for v in json.loads(m.group(1))]


# --------------------------------------------------------------------- photos
def to_jpeg(path):
    """HEIC straight off an iPhone. Converted with sips, which every Mac has."""
    if not path.lower().endswith(('.heic', '.heif')):
        return path
    out = os.path.splitext(path)[0] + '.__conv.jpg'
    if os.path.exists(out):
        return out
    try:
        subprocess.run(['sips', '-s', 'format', 'jpeg', path, '--out', out],
                       check=True, capture_output=True)
        return out
    except Exception:
        say('    ! could not convert %s. Convert it to JPEG and run again.'
            % os.path.basename(path))
        return None


def read_exif(path):
    """Returns (datetime string or None, 'lat, lon' or None)."""
    try:
        im = Image.open(path)
        ex = im.getexif()
    except Exception:
        return None, None
    when = None
    for tag in (36867, 36868, 306):          # DateTimeOriginal, Digitized, DateTime
        if ex.get(tag):
            when = str(ex.get(tag))
            break
    gps = None
    try:
        g = ex.get_ifd(0x8825)
        if g and 2 in g and 4 in g:
            def dd(v, ref):
                d = float(v[0]) + float(v[1]) / 60 + float(v[2]) / 3600
                return -d if str(ref).upper() in ('S', 'W') else d
            gps = '%.5f, %.5f' % (dd(g[2], g.get(1, 'N')), dd(g[4], g.get(3, 'E')))
    except Exception:
        pass
    return when, gps


def human_month(stamp):
    m = re.match(r'(\d{4})[:\-](\d{2})', stamp or '')
    if not m:
        return None, None
    y, mo = int(m.group(1)), int(m.group(2))
    if not 1 <= mo <= 12:
        return None, None
    return '%s %d' % (MONTHS[mo - 1], y), '%04d-%02d' % (y, mo)


# ---------------------------------------------------------------------- notes
def read_notes(folder):
    p = os.path.join(folder, 'notes.txt')
    if not os.path.exists(p):
        return None
    data = {'by': '', 'note': '', 'caps': {}}
    for line in io.open(p, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        m = re.match(r'\s*([^:]+?)\s*:\s*(.*)$', line)
        if not m:
            continue
        k, val = m.group(1).strip(), m.group(2).strip()
        low = k.lower()
        if low in ('by', 'who', 'walked by'):
            data['by'] = val
        elif low in ('note', 'what the floor plan does not tell you'):
            data['note'] = val
        elif low in ('when', 'date'):
            pass          # deliberately ignored, the photo is the source of truth
        else:
            data['caps'][k] = val
    return data


NOTES_HEADER = """# Site visit notes. One line per photograph.
#
# THE ONE RULE: write fit, not fault. Venues pay our commission.
#   Good:  "Comfortable at 200 theatre. 400 is a squeeze and the back row loses the screen."
#   Bad:   "The room is too small and the sightlines are poor."
# Say what the room suits, and who it does not suit. Never what is wrong with it.
#
# A photograph with no line against it is not published, so a blank line here is
# a decision, not an oversight. Leave one blank on purpose if a shot is only for
# the file.
#
# Do not add a date. The date below was read off the photographs themselves.
"""


def write_notes_template(folder, by_guess, when_human, shots):
    lines = [NOTES_HEADER, '',
             '# Visit date read from the photographs: %s' % (when_human or 'NOT FOUND'),
             '',
             'by: %s' % (by_guess or ''),
             'note: ',
             '']
    for name, when, gps in shots:
        lines.append('# taken %s%s' % (when or 'date unknown',
                                       ('  ~  ' + gps) if gps else ''))
        lines.append('%s: ' % name)
        lines.append('')
    io.open(os.path.join(folder, 'notes.txt'), 'w', encoding='utf-8').write('\n'.join(lines))


# --------------------------------------------------------------------- resize
def emit(src, dest_dir, stem):
    """Write the web sizes with every scrap of metadata removed."""
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)
    if im.mode not in ('RGB', 'L'):
        im = im.convert('RGB')
    out, done = {}, {}
    for key, w in WIDTHS:
        c = im.copy()
        if c.width > w:
            c = c.resize((w, max(1, round(c.height * w / c.width))), Image.LANCZOS)
        if c.width in done:
            # the original was smaller than this size, so do not write the same
            # picture twice under two names
            out[key] = done[c.width]
            continue
        rel = os.path.join('assets', 'img', 'site-visits', os.path.basename(dest_dir),
                           '%s-w%d.jpg' % (stem, c.width))
        if not DRY:
            # rebuild the pixels on a fresh canvas so nothing from the camera
            # survives into the published file, GPS above all
            clean = Image.frombytes(c.mode, c.size, c.tobytes())
            clean.save(os.path.join(ROOT, rel), 'JPEG', quality=QUALITY,
                       optimize=True, progressive=True)
        out[key] = done[c.width] = rel.replace(os.sep, '/')
        if key == 's':
            out['w'], out['h'] = c.width, c.height
    return out


# ----------------------------------------------------------------------- main
def main():
    if not os.path.isdir(DROP):
        os.makedirs(DROP)
        say('Made %s. Put a folder per venue in there and run this again.' % DROP)
        return

    names = venue_names(PAGES['Sydney'])
    by_slug = {slug(n): n for n in names}
    records, problems, published = {}, [], 0

    folders = sorted(d for d in os.listdir(DROP)
                     if os.path.isdir(os.path.join(DROP, d)) and not d.startswith('.'))
    if not folders:
        say('Nothing in %s yet.' % DROP)
        return

    for d in folders:
        folder = os.path.join(DROP, d)
        venue = by_slug.get(slug(d))
        say('\n%s' % d)
        if not venue:
            near = [n for n in names if slug(d).split('-')[0] in slug(n)][:4]
            problems.append('%s does not match a venue in the index.%s'
                            % (d, ('  Did you mean: ' + ', '.join(near)) if near else ''))
            say('  ! not in the index. %s' % ('Close: ' + ', '.join(near) if near else ''))
            continue
        say('  venue: %s' % venue)

        raw = sorted(f for f in os.listdir(folder)
                     if f.lower().endswith(('.jpg', '.jpeg', '.png', '.heic', '.heif'))
                     and not f.endswith('.__conv.jpg') and not f.startswith('.'))
        if not raw:
            say('  ! no photographs in the folder')
            continue

        shots = []
        for f in raw:
            src = to_jpeg(os.path.join(folder, f))
            if not src:
                continue
            when, gps = read_exif(src)
            shots.append((f, when, gps, src))
        shots.sort(key=lambda t: (t[1] or '9999'))

        dated = [s for s in shots if s[1]]
        if not dated:
            problems.append('%s: no photograph carries a date, so there is no visit '
                            'date to publish. Not published.' % venue)
            say('  ! no dates in the metadata. Refusing to guess a visit date.')
            continue
        when_human, when_sort = human_month(dated[0][1])
        say('  visit date from the photographs: %s' % when_human)
        for f, w, g, _ in shots:
            say('    %-28s %s%s' % (f[:28], w or 'no date', ('   ' + g) if g else ''))

        notes = read_notes(folder)
        if notes is not None:
            # New photographs dropped into a folder that already has a notes.txt
            # would otherwise be skipped in silence. Append a stub line for each
            # one instead, so the file always lists everything in the folder.
            fresh = [f for f, w, g, _ in shots if f not in notes['caps']]
            if fresh:
                if not DRY:
                    with io.open(os.path.join(folder, 'notes.txt'), 'a', encoding='utf-8') as fh:
                        fh.write('\n')
                        for f in fresh:
                            when = dict((a, b) for a, b, _, _ in
                                        [(x[0], x[1], None, None) for x in shots]).get(f)
                            fh.write('\n# added %s%s\n%s: \n'
                                     % (os.path.basename(folder), '  taken ' + when if when else '', f))
                say('  > %d new photo%s added to notes.txt, needs a line each'
                    % (len(fresh), '' if len(fresh) == 1 else 's'))
                for f in fresh:
                    problems.append('%s: no caption yet for %s' % (venue, f))

        if notes is None:
            if not DRY:
                write_notes_template(folder, '', when_human,
                                     [(f, w, g) for f, w, g, _ in shots])
            say('  > wrote notes.txt. Add one line per photograph, then run this again.')
            problems.append('%s: waiting on captions in %s/notes.txt' % (venue, d))
            continue

        captioned = [(f, src) for f, w, g, src in shots if notes['caps'].get(f, '').strip()]
        if not captioned:
            say('  ! notes.txt has no captions yet. Nothing published for this venue.')
            problems.append('%s: notes.txt is still blank' % venue)
            continue
        skipped = len(shots) - len(captioned)
        if skipped:
            say('  - %d photo%s skipped, no caption' % (skipped, '' if skipped == 1 else 's'))

        dest_dir = os.path.join(OUT_DIR, slug(venue))
        if not DRY:
            os.makedirs(dest_dir, exist_ok=True)
        photos = []
        for i, (f, src) in enumerate(captioned, 1):
            sizes = emit(src, dest_dir, '%02d' % i)
            sizes['c'] = notes['caps'][f].strip()
            photos.append(sizes)
        say('  + %d photograph%s published' % (len(photos), '' if len(photos) == 1 else 's'))

        records[venue] = {
            'by': notes['by'].strip() or 'CVBS',
            'when': when_human,
            'on': when_sort,
            'note': notes['note'].strip(),
            'photos': photos,
        }
        published += 1
        if not notes['by'].strip():
            problems.append('%s: nobody named in notes.txt, the record will read '
                            '"Walked by CVBS" instead of a person. A name is worth more.' % venue)
        if not notes['note'].strip():
            problems.append('%s: no "note:" line. The record works without it, but the '
                            'note is the part a floor plan cannot give anyone.' % venue)

    # ---- write the record and push it into the page -------------------------
    if records and not DRY:
        blob = json.load(io.open(JSON_PATH, encoding='utf-8')) if os.path.exists(JSON_PATH) else {'cities': {}}
        blob.setdefault('cities', {}).setdefault('Sydney', {}).update(records)
        io.open(JSON_PATH, 'w', encoding='utf-8').write(
            json.dumps(blob, ensure_ascii=False, indent=2))
        update_page(PAGES['Sydney'], blob['cities']['Sydney'])

    say('\n' + '-' * 66)
    say('%d venue%s published.%s' % (published, '' if published == 1 else 's',
                                     '  (dry run, nothing written)' if DRY else ''))
    if problems:
        say('\nStill needed:')
        for p in problems:
            say('  - %s' % p)
    say('-' * 66)


def update_page(page, city_records):
    """Merge the visit records into the page's data island. Touches the visit
    and seen fields only. Capacity data is never rewritten from here."""
    s = io.open(page, encoding='utf-8').read()
    m = re.search(r'(<script type="application/json" id="vidx-data">)(.*?)(</script>)', s, re.S)
    if not m:
        say('! could not find the data island in %s' % os.path.basename(page))
        return
    venues = json.loads(m.group(2))
    for v in venues:
        rec = city_records.get(v['n'])
        v['visit'] = rec or v.get('visit') or None
        if v['visit']:
            v['seen'] = '%s, %s' % (v['visit'].get('by', 'CVBS'), v['visit'].get('when', ''))
    island = json.dumps(venues, ensure_ascii=False, separators=(',', ':'))
    shutil.copyfile(page, page + '.bak')
    io.open(page, 'w', encoding='utf-8').write(s[:m.start(2)] + island + s[m.end(2):])
    say('\nUpdated %s  (previous version kept as %s.bak)'
        % (os.path.basename(page), os.path.basename(page)))


if __name__ == '__main__':
    main()
