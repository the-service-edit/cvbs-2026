# The venue data pipeline

One dataset, three consumers, one order to run things in.

## Where venue facts live

```
_venue-index-source/venues_sydney.py     54 Sydney venues, sourced capacities
_venue-index-source/venues_extra.py      the non-Sydney venues, plus the joins:
                                         which venue has a page, which has an offer,
                                         which destinations have a page at all
_venue-visits-source/build_venue.py      the deep, room by room data for the five
                                         venues we have walked through
```

Before 6 September 2026 the first and the third could not see each other, so the
same venue could carry two different largest-room figures on two pages with
nothing to catch it. `build_dataset.py` now merges them and refuses to build on a
duplicate id or a duplicate name.

## The venue index is parked

PARKED, 7 September 2026. The "By delegate numbers" block is off the sixteen
destination pages, to be picked up later. Do not run build_city_index.py in a
routine rebuild: it republishes the block. build_destination.py now builds the
pages with or without it, so the rest of the order runs unchanged. To bring the
block back for one city, run build_city_index.py "<City>" then
build_destination.py, in that order, as before.

## The build order

Run these in order. Each one prints what it did and what is still missing.

```
python3 _venue-index-source/build_dataset.py       -> assets/data/venues.json
python3 _venue-index-source/build_city_index.py "<City>"   (PARKED, see below)
python3 _destination-source/build_destination.py   -> the sixteen destination pages
python3 _destination-source/build_hub.py           -> destinations.html card copy
python3 _venue-index-source/build_finder.py        -> find-a-venue.html, venue-results.html
python3 _venue-index-source/build_accom.py         -> conference-venues-with-accommodation.html
python3 _entity-source/gen_entity.py               (always last: it owns the
                                                    Organization, WebSite, Service
                                                    and WebPage nodes on every page
                                                    in sitemap.xml)
python3 scripts/add-image-dimensions.py             (generators do not write
                                                    width/height; this reads the
                                                    real pixel size off each file)
python3 scripts/fix-teal-ink.py                    (teal used as ink, not as fill)
python3 scripts/check-site.py                      (must print 0 failures)
```

Two more, not part of the build, run before a launch:

```
python3 scripts/check-claims.py                    (every absolute claim, with the
                                                    dataset beside it to check against)
./scripts/build-public.sh /tmp/cvbs-check          (fails if the artifact and the
                                                    sitemap disagree)
```

`build_destination.py` MUST run after `build_city_index.py`. It lifts the block
that script writes out of the page, re-bands it from `s-stone` to `s-white` and
puts it back in the right place in the section order. Re-run it after any index
rebuild, or the page will carry two stone bands in a row and the index will sit
in the wrong position.

The venue data for the fifteen destinations outside Sydney lives in
`venues_destinations.py`, in the same shape as `venues_sydney.py`. The page
content, as distinct from the venue facts, lives in
`_destination-source/destinations.py`. No capacity figure is ever typed there:
a featured card names a venue id and the meta line is generated from
`assets/data/venues.json`, so a card and the index cannot disagree.

After re-running `build_venue.py` or `build_westin.py`, also run:

```
python3 scripts/patch-venue-pages.py               (save button, shortlist link, finder assets)
python3 scripts/patch-nav.py                       (Find a venue in the nav)
python3 scripts/fix-faq-schema.py                  (FAQ markup must match the visible question)
```

## The rules the build enforces

- **Never invent a value.** Every field is present in a source file or absent
  from the output. Where a venue publishes nothing, the site says "not
  published" and the build reports the gap under DATA REQUIRED.
- **Provenance travels with the figure.** Every venue carries `src` (capacities),
  `src2` (ceiling, area, extra setups, second space) and `checked` (the date those
  were last read). It does not render to the customer. It exists so a wrong
  number can always be traced.
- **Photographs only where CVBS took them.** A result card gets an image only if
  the venue has a page under `/venue-visits/`, and the image is read off that
  page so the two can never disagree. Stock and generated imagery is not used on
  a card, because there a picture is a claim about the room.
- **Structured data may only name what a reader can see.** `build_city_index.py`
  generates the visible list and the ItemList from the same rows in the same
  pass. `check-site.py` fails the build if an ItemList or FAQPage names something
  the page does not show.
- **The filter tool is not an indexed page.** `venue-results.html` carries
  `noindex, follow`, is not in the sitemap, and has no ItemList. The landing
  pages carry the data as static HTML. That split is the whole indexation
  strategy, and it is why there is no risk of thousands of filter URLs.

## Adding a city

1. Copy `venues_sydney.py` to `venues_<city>.py`, or add rows to
   `VENUES_OTHER` in `venues_extra.py` for a handful.
2. Import them in `build_dataset.py` and run it. The destination drops out of
   the "no venue data at all" report automatically.
3. `build_city_index.py <City>` publishes the full list onto that city's page.
   It refuses below six venues, because a full index of one venue is a venue.
4. Run the adversarial pass described in `cvbs-venue-index` memory before
   shipping: try to refute every superlative in the answer block. The first
   Sydney draft had three wrong.
