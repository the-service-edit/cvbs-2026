# Venue research prompt

Paste this into Claude, replacing the two fields at the top. It returns a data
entry ready to paste into `venues_sydney.py`, plus a report of what it could not
verify. Add the entry, then run `python3 scripts/sync-venue-data.py`.

It researches **published data only**. It must never write a site visit note or
anything that reads like firsthand observation. That comes from whoever was in
the room.

Version 2, 27 Aug 2026. Every rule marked **[v2]** was added after a live test
run on Capella Sydney, where version 1 would have nulled the two most important
figures in the record and nearly published two phantom ones.

---

VENUE: <venue name>
CITY: Sydney

You are researching one venue for a conference venue capacity index. The index
is used by event organisers to judge whether a room fits their event, and it is
read by AI assistants answering venue questions, so a wrong figure is worse than
a missing one. Accuracy beats completeness every time.

## The one sourcing rule

**Every figure must come from the venue's own published material**: its capacity
chart, fact sheet, floor plan, technical specification, conference brochure or
its own website. Fetch and read those documents, including PDFs.

**Never take a figure from a directory or aggregator.** Not Cvent, VenueNow,
Tagvenue, EventConnect, Peerspace, Hire Space, a convention bureau, a hotel
booking site, or any "top 10 venues" article. You may use them to find the
venue's own documents. You may not use them as a source for a number.

If the venue does not publish something, the answer is `None`. A gap is
acceptable. An estimate is not. Never infer a capacity from a floor area, never
convert between setups, never round a competitor's number.

**[v2] Read every capacity chart at least twice, with differently worded
prompts, before you use a figure from it.** PDF extraction is lossy and often
cannot be done locally. On the test run the two passes disagreed, and that
disagreement is what revealed that a row of numbers were per-section figures for
a divisible room rather than whole-room capacities. Treat any disagreement
between your own passes as unresolved until a second venue document settles it.
Say in your report that you did this.

## [v2] When sources disagree

Weigh them, do not simply null:

1. A capacity chart, floor plan, fact sheet or technical specification outranks
2. a website page, which outranks
3. a press release, brochure prose or marketing copy.

Null the field only when documents of **comparable authority** conflict, or when
a conflict survives the majority. Where three capacity documents say 420 and one
press release says "up to 400", use 420 and note it.

**A rounded figure is not a conflict.** "536 m²" against "536.83 m²", or
"up to 400" against 420, is a precision difference. Use the precise one.

## Before anything else, check the venue is still what it says it is

Search for the venue's current status and report anything you find on:

- Rebrands and ownership changes. Sydney examples that caught us out: Radisson
  Blu became Paradox Sydney, Primus became Kimpton Margot, Aware Super Theatre
  became the TikTok Entertainment Centre, Vibe Rushcutters Bay closed.
- Restaurant, bar or rooftop operators changing hands. Space names often belong
  to the operator, not the hotel, and go stale when the operator leaves. If an
  operator change is under way, **name the space generically** (for example
  "Rooftop, exclusive hire") rather than by the restaurant brand.
- Refurbishments, closures, or spaces **not yet open**.

Report all of this even if it does not change a number.

## [v2] One venue or two

Sometimes the largest space is not in the building the venue is named after: an
adjacent heritage building, a new events precinct, a sub-brand with its own
trade listings.

**Treat them as one record when the venue publishes them in a single capacity
chart or fact sheet. Otherwise create two records.** Either way, say in your
report which you did and why, and say it in the `note` if a delegate would have
to walk between buildings. Getting this wrong puts the same venue in the index
twice.

## What to return

### 1. The data entry

Return exactly this shape, filled in, ready to paste. **[v2] Keep the `worked`
and `seen` keys with the defaults shown. Do not delete them and do not change
them.**

```python
 dict(
   worked=False, seen=None,
   n="", sp="", pr="", ty="",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=None,
   br=None, gr=None, area=None, ceil=None, ceilq=None,
   s_name=None, s_th=None,
   note="",
   src="",
   src2=""),
```

- `n` the venue name as the venue writes it.
- `sp` the venue's **largest** event space, named as the venue names it. Where
  the venue's own documents name it two different ways, use the one that appears
  in the capacity chart.
- `pr` the precinct. Use one of these if it fits, otherwise propose a new one and
  say so: Barangaroo, Circular Quay, Darling Harbour, Eastern Suburbs, Epping,
  Lilyfield, Marsfield, Milsons Point, Moore Park, Mosman, North Sydney,
  Pyrmont, Redfern and Eveleigh, Surry Hills & Central, Sydney Airport,
  Sydney CBD, Sydney Olympic Park, The Rocks, Woolloomooloo.
  **[v2] Where two fit, use the one an organiser would use to judge whether
  delegates can walk there**, which is usually the tighter one. Circular Quay
  beats Sydney CBD for an address at Circular Quay, whatever the venue calls
  itself in its own marketing.
- `ty` one of `conv` (convention centre), `hotel`, `event` (dedicated event venue).
- `th bq cl ck cab ush bd` capacities for the space named in `sp`, in theatre,
  banquet, classroom, cocktail, cabaret, U-shape and boardroom. Integers or None.
  **[v2] For a divisible room, these are whole-room figures.** Per-section
  numbers in a chart are not capacities for `sp`. If the only U-shape or
  boardroom figures are per-section, both fields are `None`.
- `br` the number of meeting and event rooms. **[v2] Count the bookable spaces
  the venue's own capacity chart lists as rows, counting a combinable pair
  ("Smith Rooms 1 & 2") as the marketed unit and not counting the divisible
  sections of a larger room.** A count is permitted here even though it is not
  a published figure, because every venue lists its rooms and almost none states
  a total. Say in your report that it is a count and what you counted.
- `gr` number of guest rooms, `0` if the venue has no accommodation, `None` if it
  has some but publishes no count.
- `area` floor area of `sp` in square metres. `ceil` its ceiling height in metres
  as a float. **[v2] Keep the venue's published decimals, do not round.**
- `ceilq` a short qualifier **only** where a bare ceiling number would mislead.
  Real example: Sydney Showground's Dome publishes 42m, which is the apex, so
  `ceilq="at the dome apex; 9m to the rigging star"`. A uniform ceiling needs no
  qualifier, and leaving it None is the right answer, not a failure.
- `s_name` and `s_th` the second largest space and its theatre capacity. This
  matters because it tells an organiser whether a plenary plus a concurrent
  stream fits.
- `src` the source for the capacities. `src2` the source for ceiling, floor area,
  extra setups and the second space. Direct URLs, PDFs included.

### 2. A figure by figure source table

Every non-null figure, the exact URL it came from, the wording the venue used,
and **[v2] a confidence of high, medium or low**. High means two or more venue
documents agree. Low means one lossy read and no corroboration. We need to know
which figures to check before we lean on them.

### 3. A plausibility check

**[v2] Run these checks, but null only where a figure is implausibly HIGH for
the space. A conservative figure is not an error.**

- Theatre against floor area at roughly 0.6 to 1.0 sqm per person.
- Banquet at roughly 55 to 70 per cent of theatre.
- Ceiling plausible for the span.

**[v2] When a figure comes in LOW against these, do not null it. Go and find the
room's published length and width first.** On the test run a ballroom read at
1.79 sqm per person, nearly double the upper bound, because the room is 9 metres
wide and 54 metres long and cannot seat a wide bank of chairs. The venue was
under-claiming. Nulling it would have thrown away the most important number in
the record. Report the aspect ratio whenever a check fails.

Where a figure is implausibly high, or where the venue's own documents conflict
at comparable authority, set it to `None` and record the reason. Real examples:
ICC Sydney's own PDFs gave 2,880 and 3,100 sqm for the same hall, so the field is
None. A hotel published a 2.64m ceiling on a 264 sqm room seating 250 theatre,
which reads as a typo, so it is None until the venue confirms.

### 4. What you could not find

List every field left `None` and say which of these it is:

- genuinely unpublished by the venue,
- published but you could not locate it,
- **[v2] deliberately left None** (a uniform ceiling needs no `ceilq`, a venue
  with no second space needs no `s_name`).

These become the questions we put to the venue, so the distinction matters.

## Writing the `note`

Two or three sentences, **[v2] 60 to 90 words**, on what the venue is actually
good for and who it does not suit. Written for an event organiser, in the voice
of an experienced hospitality professional talking across a table.

- Australian English. No em dashes.
- Full sentences. Never a spec list, never "Up to 700 delegates, reduced rates
  plus value-adds".
- No stacked luxury adjectives, no "state of the art", "premier", "iconic",
  "world class", "tailored solutions".
- Say the constraint as well as the strength. "Inner west site with no station
  nearby, so delegates need cars or coach transfers" is exactly right.
- Frame limits as fit, not fault. The venue may read this.
- **[v2] The note may mention spaces other than `sp`**, and should where it
  changes the decision: a room that divides into three, a space in a separate
  building, a wing still under construction, an opening date inside the last
  twelve months. These facts have no field of their own and the note is where
  they live.

## Two things you must not do

**Do not set `worked` or `seen`.** `worked` is a claim about CVBS's booking
history and `seen` is a claim that a named person stood in the room on a named
date. Both are confirmed by the client, never researched. Leave the defaults.

**Do not write any superlative you have not tested.** If you want to say
"largest ballroom in Sydney" or "the only venue that can do X", first go looking
for the counter-example and report what you found. Three superlatives in the
first Sydney draft were wrong for exactly this reason.
