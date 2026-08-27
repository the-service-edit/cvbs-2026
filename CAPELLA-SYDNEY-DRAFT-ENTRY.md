# Capella Sydney: draft index entry

Produced by the test run of `_venue-index-source/RESEARCH-PROMPT.md` on 27 Aug 2026.
**Not added to the index.** Two decisions below are yours, and one figure wants a
human eye on the PDF before we lean on it.

## The entry

```python
 dict(
   worked=False, seen=None,
   n="Capella Sydney", sp="The Capella Ballroom", pr="Circular Quay", ty="hotel",
   th=300, bq=240, cl=152, ck=420, cab=210, ush=None, bd=None,
   br=10, gr=192, area=536.83, ceil=4.6, ceilq=None,
   s_name="The Liberty Ballroom", s_th=145,
   note="The pull here is a heritage ballroom with 4.6 metre ceilings and real daylight, sitting a few steps from a 192 room hotel, so it suits board level conferences, gala dinners and product launches where the room does the talking and the delegation is compact. The Capella Ballroom is long and narrow rather than square and it caps at 300 theatre, so plenaries above that number, trade exhibitions or anything needing one wide sightline will sit better elsewhere. Worth knowing the event spaces are on Level Two of the Lands building next door rather than inside the hotel, and the rest of that building is still opening through late 2026.",
   src="https://capellahotels.com/assets/img/site_images/sydney/Capella_Sydney_Meeting__Events_Brochure_2026.pdf",
   src2="https://capellahotels.com/assets/docs/sydney/Capella_Sydney_Factsheet.pdf?V1.02="),
```

## Two decisions for you

**1. One record or two.** Capella Sydney the hotel tops out at 80 guests. The
300 person ballroom is in The Lands by Capella, a separate heritage building next
door that opened 2 February 2026 under its own sub-brand, and which has its own
listings on BESydney and IMEX. They publish one combined capacity chart, so the
research treated them as one venue. If you would rather split them, say so.

**2. The Lands is half open.** The venue's own material says the full 10,000 sqm
building, with restaurants, retail and cultural spaces, completes late 2026. Only
Level Two is trading. The note says so, which is honest, but it also means this
entry needs rechecking in about six months.

## What to check before trusting it

- **The capacity chart PDF.** It had to be read through a summariser rather than
  extracted, and two passes disagreed. That disagreement is what caught a row of
  numbers ("22 24 24", "18 18 18") being per-section figures for the ballroom's
  three sections rather than whole-room U-shape and boardroom capacities. Both
  fields are correctly `None` now, but someone should eyeball the chart.
- **`br=10` is a count, not a published figure.** Ten rows in the venue's own
  chart. Split the combinable pairs and it is 12.
- **Cocktail 420 against a press release saying 400.** Three capacity documents
  say 420, one pre-opening press release says 400. Version 2 of the prompt now
  says the chart outranks the press release, so 420 stands.

## Two flags that look wrong and are not

- Theatre at 300 in 536.83 sqm is 1.79 sqm per person, roughly double the normal
  upper bound. The room is 9 metres wide and 54 metres long, so theatre is
  limited by sightlines, not floor area. The venue is under-claiming. **Do not
  correct this upward.**
- Banquet at 80 per cent of theatre looks high, for the same reason. Theatre is
  suppressed, banquet is not inflated. Absolutely it is 2.24 sqm per person,
  which is normal for rounds.

## Sources

Capella's own material only: [meetings and events](https://capellahotels.com/en/capella-sydney/meetings-events) ·
[M&E brochure 2026 PDF](https://capellahotels.com/assets/img/site_images/sydney/Capella_Sydney_Meeting__Events_Brochure_2026.pdf) ·
[fact sheet PDF](https://capellahotels.com/assets/docs/sydney/Capella_Sydney_Factsheet.pdf?V1.02=) ·
[The Capella Ballroom](https://capellahotels.com/en/capella-sydney/thelands/thecapellaballroom) ·
[The Liberty Ballroom](https://capellahotels.com/en/capella-sydney/thelands/thelibertyballroom) ·
[The Lands by Capella](https://capellahotels.com/en/capella-sydney/thelands)
