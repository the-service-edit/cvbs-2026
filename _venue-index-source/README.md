# Venue index, source of truth

The venue index on `venue-finder-sydney.html` is generated, not hand written.

- `venues_sydney.py` — the data. One dict per venue, with TWO source URLs each:
  `src` for the capacity figures, `src2` for the ceiling height, floor area,
  extra setups and second space. This is the file to edit.
- `gen.py` — builds the HTML section, the JSON data island, the schema.org
  ItemList and the source register comment from that data.

The renderer lives in `assets/js/site.js` (search `vidx-data`) and the styles in
`assets/css/site.css` (search `.vidx`). Both are city agnostic.

## Adding another city

1. Copy `venues_sydney.py` to `venues_<city>.py`, change `CITY`, replace the
   venue list, rewrite the four answer block paragraphs and the boundary
   paragraph in `gen.py`.
2. Run `gen.py`, paste the section into the city page, paste the data island
   before the `site.js` tag, and replace the page's existing ItemList schema.
3. No CSS or JS changes. The precinct filter, the at a glance numbers and the
   "ceiling heights published by N of the M" line all build themselves from the
   data, so they can never contradict the table.

## The rules that keep this citable

- Every figure comes off the venue's own published capacity chart, fact sheet,
  floor plan or technical spec. Never a directory, never an estimate.
- Where a venue publishes nothing, the field is `None` and the page prints
  "Not published". A gap is an asset here, not an embarrassment.
- `ceilq` carries an honest qualifier wherever a bare ceiling number would
  mislead. Sydney Showground's 42m is the dome apex, not a working height, and
  the page says so.
- Any figure that fails a plausibility check gets nulled, not published. Two
  are currently withheld on that basis and the reasons are in the file header.
- The answer block leads with a definitive first sentence containing numbers.
  Before shipping a new city, run an adversarial pass that tries to REFUTE every
  superlative in it. The first Sydney draft had three wrong.
- The boundary paragraph must say what the index excludes. An index that implies
  it is exhaustive when it is not will get caught.

Last checked: 14 August 2026.
