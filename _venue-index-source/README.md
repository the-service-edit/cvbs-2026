# Venue index, source of truth

The venue index on `venue-finder-sydney.html` is generated, not hand written.

- `venues_sydney.py` — the data. One dict per venue, with the primary source URL
  every capacity was read from. This is the file to edit.
- `gen.py` — builds the HTML section, the JSON data island, the schema.org
  ItemList and the source register comment from that data.

The renderer lives in `assets/js/site.js` (search `vidx-data`) and the styles in
`assets/css/site.css` (search `.vidx`). Both are city agnostic.

## Adding another city

1. Copy `venues_sydney.py` to `venues_<city>.py`, change `CITY`, replace the
   venue list, rewrite the four answer block paragraphs in `gen.py`.
2. Run `gen.py`, paste the section into the city page, paste the data island
   before the `site.js` tag, and replace the page's existing ItemList schema.
3. No CSS or JS changes. The precinct filter and the at a glance numbers build
   themselves from the data.

## Rules that keep this citable

- Every figure comes off the venue's own published capacity chart. Where a venue
  does not publish one, the field is `None` and the page prints "Not published".
  Never estimate.
- The answer block leads with a definitive first sentence containing numbers.
- Re-check figures before any venue rebrand, refurbishment or annual copy review.
  Last checked: 14 August 2026.
