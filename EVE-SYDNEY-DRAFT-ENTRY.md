# The EVE Hotel Sydney: draft index entry

Produced by `_venue-index-source/RESEARCH-PROMPT.md` v2 on 27 August 2026.
**Correction, same day.** The EVE was already in the index, added by an earlier
session, and this run failed to see it before drafting. Record 1 below is
therefore not new. What it did produce is live: the published note claimed a
rooftop hire capacity that stopped being true this week, and `sp` named the
rooftop while the only figure on the record belonged to the boardroom. Both are
now corrected in `venues_sydney.py` and synced. **Record 2, Saltbox, is genuinely
missing and is the decision for you.**

## The short version

The EVE is not a conference venue. Its largest space that the hotel itself runs
and publishes a number for is a fourteen seat rooftop boardroom. Its two larger
food and beverage spaces went dark this week: Lottie closed 23 August 2026 and
Bar Julius on 26 August, with The Apollo Group taking the leases and two new
restaurants due before the end of the year, concepts not announced.

The conference relevant record in that precinct is **Saltbox**, next door at 399
Cleveland Street, which publishes 300 theatre and 400 cocktail. Both entries are
below. Add Saltbox first if you only add one.

## Record 1: The EVE Hotel Sydney (already in the index, now corrected)

```python
 dict(
   worked=False, seen=None,
   n="The EVE Hotel Sydney", sp="Rooftop Boardroom", pr="Redfern and Eveleigh", ty="hotel",
   th=None, bq=None, cl=None, ck=None, cab=None, ush=None, bd=14,
   br=1, gr=102, area=None, ceil=None, ceilq=None,
   s_name=None, s_th=None,
   note="A 102 room hotel in the Wunderlich Lane precinct at Redfern, built for accommodation and small executive meetings rather than conferences. The only space the hotel runs itself is a rooftop boardroom for fourteen. Both restaurant venues changed operators in August 2026 and the replacements are not open yet, so a group needing more room uses Saltbox in the same laneway, which takes 300 theatre. Good for a board offsite with rooms attached, not for a plenary.",
   src="https://theevehotel.com.au/functions-and-events/",
   src2="https://www.tfehotels.com/en/hotels/collection/eve-hotel-sydney/"),
```

## Record 2: Saltbox

```python
 dict(
   worked=False, seen=None,
   n="Saltbox", sp="The Box", pr="Redfern and Eveleigh", ty="event",
   th=300, bq=240, cl=None, ck=300, cab=180, ush=None, bd=None,
   br=3, gr=0, area=330, ceil=None, ceilq=None,
   s_name="Suites One & Two", s_th=110,
   note="A purpose built event venue in the Wunderlich Lane precinct at Redfern, run by the catering business Cook and Waiter and open since May 2025. The Box is a pillarless 330 sqm room with floor to ceiling windows on three sides, which suits conferences to 300 theatre, awards dinners and launches. Two breakout suites and a 119 sqm all weather terrace sit alongside it. There is no accommodation on site, though The EVE Hotel is a few steps away.",
   src="https://saltboxvenue.com.au/spaces/",
   src2="https://saltboxvenue.com.au/wp-content/uploads/2025/04/SALTBOX-Sample-Floorplans_0325.pdf"),
```

## One venue or two

**Two records.** Neither venue publishes the other in its own capacity chart.
Different street addresses (8 Baptist Street versus 399 Cleveland Street),
different owners of the trading business (TFE Hotels operates the hotel for TOGA,
Alder Road Group operates Saltbox), and The EVE's own functions page lists Saltbox
under "partner venues on Wunderlich Lane" rather than among its own spaces. Under
the v2 rule that is two records. Both notes say the other is a short walk, because
a delegate would in practice use them together.

The five other Wunderlich Lane food venues on The EVE's partner list (Vitelli's
Upstairs, Olympus, R by Raita Noda, Regina La Pizzeria and the closed Baptist
Street Rec Club) publish private dining numbers of 15 to 20 and are not index
candidates.

## Status check

- **Lottie closed 23 August 2026. Bar Julius closed 26 August 2026.** Liquid &
  Larder ended an eighteen month partnership. The Apollo Group, which owns Olympus
  Dining in the same lane, takes both spaces and will open two new restaurants
  before the end of 2026, concepts not revealed. This is exactly the operator
  change trap in the prompt, so no space in either record is named after a
  restaurant brand.
- **The hotel itself has not rebranded.** Opened as part of the Wunderlich Lane
  launch in late 2024, Collection by TFE Hotels, 102 rooms, still trading.
- **The fitness space is not finished.** The hotel's own words: "As The EVE's
  dedicated fitness space takes shape, guests enjoy complimentary access to
  leading neighbourhood wellness partners." Not a capacity issue, but it dates
  the record.
- **Saltbox opened May 2025** and is stable.

## Figure by figure sources

### The EVE Hotel Sydney

| Field | Value | Source | Venue wording | Confidence |
|---|---|---|---|---|
| bd | 14 | theevehotel.com.au/functions-and-events/ | "an intimate boardroom for hire, accommodating up to 14 guests" | High. Two reads of the functions page agreed, and the TFE property page lists a Rooftop Boardroom. |
| gr | 102 | tfehotels.com/en/hotels/collection/eve-hotel-sydney/ | "Each of our 102 Guest Rooms and Suites" | Medium. Two differently worded reads of the same page returned the same sentence, but only one document states it. The hotel's own rooms page gives no total. |
| br | 1 | as above | count, not published | Medium. See below. |

### Saltbox

| Field | Value | Source | Venue wording | Confidence |
|---|---|---|---|---|
| th | 300 | saltboxvenue.com.au/spaces/ and the floorplans PDF | "Theatre: 300 Guests" | High. Website and floorplan agree. |
| bq | 240 | same | "Seated: 240 Guests" | Medium. The venue says Seated, not Banquet. The floorplan also gives "Seated (wedding style) 200". Read as banquet, flagged below. |
| ck | 300 | same | "Cocktail: 300 Guests" | High. Agrees across both. Full venue including the terrace is 400. |
| cab | 180 | same | "Cabaret: 180 Guests" | High. |
| area | 330 | floorplans PDF | "330 SQM" | Medium. One document, one lossy read, no corroboration on the website. |
| s_th | 110 | saltboxvenue.com.au/spaces/ | "Theatre: 110 Guests" for Suites One & Two | Low. The floorplan PDF disagrees, see below. |
| br | 3 | capacity listing | count, not published | Medium. |

## Reads, conflicts and how they were settled

**Every capacity source was read twice with differently worded prompts.**

- The EVE's functions page: both passes returned 104 for rooftop exclusive hire,
  28 for the West Wing, 14 for the boardroom. No disagreement.
- Saltbox spaces page: both passes returned identical tables. No disagreement.
- **The Saltbox floorplans PDF failed its two pass test on the breakout suites.**
  Pass one returned Suite One "Boardroom 24, Theatre 18". Pass two returned Suite
  One "Boardroom 24, Theatre 18" and Suite Two "Boardroom 20, U-Shape 18", with
  the combined suites carrying both "Theatre 36" and "Theatre 96". A theatre
  figure below the boardroom figure for the same room is not possible, so the
  extraction is scrambling labels, not reporting them. The PDF outranks the
  website under the v2 hierarchy, but only when it can be read. It cannot, so the
  suite figures come from the website and `s_th=110` is marked low confidence.
  The Box figures are unaffected: website and PDF agree on all four setups.

**Not treated as conflicts.** Saltbox's "Full Venue" cocktail 400 against "The
Box" cocktail 300 is not a contradiction, it is the terrace being included. `sp`
is The Box because that is the room, and the note carries the exclusive hire
number instead.

## Plausibility check

**The Box, 330 sqm, 300 theatre = 1.10 sqm per person.** Above the 0.6 to 1.0
band, so the venue is being conservative, not over claiming. Under v2 that is not
a nulling condition. No published dimensions exist to test the aspect ratio, but
the room is described as pillarless with glass on three sides, which usually costs
seats along the glazing line.

**Banquet 240 against theatre 300 is 80 per cent**, above the 55 to 70 band. At
1.38 sqm per person for seated dining this is tight but achievable on long tables,
which is consistent with the venue publishing a separate and lower "wedding style"
figure of 200 for round tables. Kept, flagged medium.

**Cocktail 300 in 330 sqm is 1.10 sqm per person**, roughly half the density most
venues claim for standing. Conservative again. Kept.

**Ceilings.** Neither venue publishes a ceiling height, so no check was possible
and both are `None`.

**Nothing was nulled for implausibility in this run.**

## What could not be found

### The EVE Hotel Sydney

- `th bq cl ck cab ush` **genuinely unpublished.** The hotel publishes no capacity
  chart, fact sheet, floor plan or events kit. Searched the hotel site, the TFE
  property page and the TFE meetings portal, which does not list the property at
  all. The only capacity numbers it publishes anywhere are the three on the
  functions page.
- `area ceil` **genuinely unpublished.**
- `ceilq s_name s_th` **deliberately left None.** No second bookable space exists
  while the restaurants are between operators.
- The rooftop restaurant's "exclusive hire for up to 104 guests" was **not used**.
  It is not attributed to a setup, so it cannot be assigned to a field without
  inventing one, and the operator who published it left four days ago. When the
  new restaurant opens, this is the figure to chase, and if it comes back with a
  setup attached, `sp` should move to the rooftop and the boardroom drops to
  `s_name`.

### Saltbox

- `cl ush` for The Box **published but incomplete.** The venue publishes classroom
  and U-shape for nothing, and U-shape appears only in the unreadable suite block.
- `bd` for The Box **genuinely unpublished.** Boardroom figures exist only for the
  suites, which are per room, not whole venue, so they are not capacities for `sp`.
- `ceil` and `ceilq` **genuinely unpublished.**
- `area` for the suites and the second space **published but not located.** Only
  the terrace's 119 sqm and The Box's 330 sqm appear.

## Questions to put to the venues

**To The EVE:** what will the rooftop restaurant's exclusive hire capacity be
under the new operator, and by which setup; is there a floor area or ceiling
height for the Rooftop Boardroom; and will the hotel publish a capacity chart now
that all three restaurants sit under one operator.

**To Saltbox:** confirm the Suites One & Two theatre figure, since the website
says 110 and the floorplan appears to say 96; confirm whether "Seated 240" is
banquet on rounds or long tables; and ask for The Box's ceiling height, its length
and width, and classroom and U shape figures.

## Two things the prompt asks me to declare

**`worked` and `seen` are untouched** in both records. Karen confirms those.

**No superlative is used in either note.** Saltbox's own homepage calls it
"Sydney's newest event venue" and describes itself as the flagship venue of
"Sydney's leading events catering business". Neither claim was tested, so neither
was repeated.
