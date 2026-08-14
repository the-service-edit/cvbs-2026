# Venue index, source of truth

The Sydney venue index is generated, not hand written.

- `venues_sydney.py` — the data. One dict per venue with TWO source URLs each:
  `src` for the capacity figures, `src2` for the ceiling height, floor area,
  extra setups and second space. This is the file to edit.
- `gen.py` — builds TWO html blocks plus the data island, the schema.org
  ItemList and the source register comment.

The page uses the two blocks in two different places:

- `answer.html` — the short answer plus the at a glance rail. Goes HIGH on the
  page, straight after the intro, because that is where citations are taken from.
- `index.html` — the filters and the table. Goes BELOW the featured venues, so
  the photography leads and the data supports it.

Renderer lives in `assets/js/site.js` (search `vidx-data`), styles in
`assets/css/site.css` (search `.vidx`). Both are city agnostic.

## The worked-with badge

`worked=True` puts a navy "Worked with" badge on the row. It is currently set on
the nine venues the Sydney page already presents as "venues we know inside out"
in its Featured section, plus Kimpton Margot and the two Doltone House venues,
which have live CVBS offer pages.

**KAREN TO CONFIRM AND EXTEND.** Do not set `worked=True` on a venue without her
say-so. It is a claim about CVBS's booking history, and one wrong one costs the
whole page its credibility.

## Adding another city

1. Copy `venues_sydney.py` to `venues_<city>.py`, change `CITY`, replace the
   venue list, rewrite the two answer paragraphs in `gen.py`.
2. Run `gen.py`. Paste `answer.html` after the intro section, `index.html` after
   the featured venues, the data island before the `site.js` tag, and replace
   the page's existing ItemList schema.
3. No CSS or JS changes. The precinct filter and the four at a glance numbers
   derive themselves from the data, and the rail deliberately picks four
   DIFFERENT venues so it never reads as one venue's advert.

## Rules that keep this citable

- Every figure comes off the venue's own published capacity chart, fact sheet,
  floor plan or technical spec. Never a directory, never an estimate.
- Where a venue publishes nothing, the field is `None` and the page prints
  "Not published". A gap is an asset here, not an embarrassment.
- `ceilq` carries a qualifier wherever a bare ceiling number would mislead.
  Sydney Showground's 42m is the dome apex, not a working height. Qualified
  ceilings are excluded from the at a glance rail for the same reason.
- Any figure failing a plausibility check gets nulled, not published. The
  reasons for the current exclusions are in the data file header.
- Before shipping a new city, run an adversarial pass that tries to REFUTE every
  superlative in the answer block. The first Sydney draft had three wrong.
- Check for rebrands. This pass found Radisson Blu is now Paradox, Primus is now
  Kimpton Margot, and Vibe Rushcutters Bay has closed.

Last checked: 14 August 2026.
