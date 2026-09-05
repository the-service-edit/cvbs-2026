# Pullman Quay Grand Sydney Harbour: draft index entry

Produced by `_venue-index-source/RESEARCH-PROMPT.md` v2 on 27 Aug 2026, prompted by
Mel's 31 October 2025 visit photographs. Research pass, then an adversarial pass
that overturned three things in the first draft.

**Not added to the index.** Two decisions below are yours. The site visit record
is a separate decision and my recommendation is to hold it, for the reason in the
last section.

## The entry

```python
 dict(
   worked=False, seen=None,
   n="Pullman Quay Grand Sydney Harbour", sp="Lachlan / Macquarie Rooms", pr="Circular Quay", ty="hotel",
   th=120, bq=100, cl=80, ck=140, cab=80, ush=70, bd=40,
   br=3, gr=72, area=170, ceil=2.7, ceilq=None,
   s_name="Macquarie Room", s_th=70,
   note="An all suite hotel on East Circular Quay with one dedicated conference room, the Lachlan and Macquarie pair on level two. Joined they run to 170 square metres and take 120 theatre or 100 for dinner, and they split into two halves of 70 theatre each if a stream has to run alongside a plenary. The 2.7 metre ceiling takes a screen rather than a stage. The larger room is actually the bar and lounge a floor above, 200 square metres, holding 180 for a cocktail function over the harbour.",
   src="https://document-tc.galaxy.tf/wdpdf-37lvpu058mpchoogd9omau1rr/meetings-events_cms-document.pdf",
   src2="https://www.pullmanquaygrandsydneyharbour.com/meetings-and-events"),
```

## The name

Mel called it "Pullman Sydney Grand Quay". The property trades as **Pullman Quay
Grand Sydney Harbour**, 61 Macquarie Street, East Circular Quay. Worth catching,
because there is also a Pullman Sydney Hyde Park and a Pullman at Sydney Olympic
Park already in the index and the three are easy to confuse.

## Two decisions for you

**1. Which space is `sp`.** The prompt says `sp` is the venue's largest event
space. Strictly, that is the level three bar and lounge at 200 square metres, and
Accor's own hotel page says so in as many words: largest room 200 m2. But that
space publishes only cocktail 180 and boardroom 30. Make it `sp` and the venue
appears in a conference index with no theatre, banquet, classroom, cabaret or
U-shape figure at all, and an organiser filtering for 100 theatre never sees it.

I have used the Lachlan and Macquarie pair instead, which is the venue's only room
with a full setup row, and put the 200 square metre space in the note so nothing
is hidden. That is a deliberate departure from the letter of the prompt. Overrule
me if you would rather the index be literal.

**2. How to write the space name.** The capacity chart heads the merged row
"LACHLAN MACQUARIE". The website page titles it "LACHLAN / MACQUARIE ROOMS". The
prompt says the chart wins, but a truncated table heading is not really a
competing name, so I have used the website form because it is what a client would
recognise on a proposal.

## Figure by figure

| Field | Value | Source | Venue's wording | Confidence |
|---|---|---|---|---|
| `th` | 120 | MICE kit capacity chart | Theatre, combined row | High |
| `bq` | 100 | MICE kit capacity chart | Banquet, combined row | High |
| `cl` | 80 | MICE kit capacity chart | Classroom, combined row | High, see arithmetic below |
| `ck` | 140 | MICE kit capacity chart | Cocktail, combined row | High, chart and website agree |
| `cab` | 80 | MICE kit capacity chart | Cabaret, combined row | High |
| `ush` | 70 | MICE kit capacity chart | U-Shape, combined row | High, see arithmetic below |
| `bd` | 40 | MICE kit capacity chart | Boardroom, combined row | Medium, website calls it Hollow Square |
| `area` | 170 | MICE kit capacity chart | Surface 170 m2 | High |
| `ceil` | 2.7 | MICE kit capacity chart | Height 2.7 m | High, MICE kit only |
| `gr` | 72 | Current MICE kit | "72 luxurious apartment style hotel rooms" | High |
| `br` | 3 | Current MICE kit | "3 stunning function venues" | High, published not counted |
| `s_name`, `s_th` | Macquarie Room, 70 | MICE kit capacity chart | Half room row, 85 m2, theatre 70 | High |

`br=3` is the venue's own published figure, not a count. The three are the Lachlan
and Macquarie pair, the level three bar and lounge, and the level two restaurant.
The chart splits those three into twelve rows, most of which are sections.

The suites run 75 to 100 square metres each, per the same kit.

## Where sources disagreed, and how it was settled

**The website page is a mangled render of the chart. Do not use it for numbers.**
The venue's own meetings page lists "U-shape 170" for a room whose theatre capacity
is 120. A U-shape cannot exceed theatre. 170 is the room's floor area, printed in
the U-shape column, and the same row prints the boardroom figure under Hollow
Square.

**The arithmetic proves which version is right.** Each half publishes classroom 40
and U-shape 30. Two halves give 80 and 70, which is exactly what the combined row
says. The same test works on the restaurant: 66 plus 65 plus 24 equals its 155
square metre exclusive figure. The chart is internally consistent and the website
is not, so `cl=80` and `ush=70` are high confidence, not the medium the first draft
gave them.

**Two MICE kits are in circulation.** The older names the bar Hacienda. The current
names it El Vista and adds Flaminia. Use the current one. Both are linked below.

**Suite count, 72 against 73.** Current kit 72, superseded kit 73, hotel website
silent. Newer edition wins.

**Bar cocktail, 180 against 200.** The superseded kit said 200 for the same 200
square metre space. The current kit revised it down to 180 after the refit. Use 180.

## Plausibility check

Run per v2. Nothing nulled.

- **Theatre at 120 in 170 m2 is 1.42 m2 per person**, well above the 0.6 to 1.0
  band. The venue is under-claiming, exactly as Capella was. The half room row says
  the same thing independently at 1.21 m2 per person. Two rows under-claiming in
  the same direction is a room shape constraint, not an error. **Do not correct
  this upward.**
- **Banquet at 83 per cent of theatre** looks high against the 55 to 70 per cent
  rule, but 100 covers at 1.7 m2 per person is normal for rounds. Theatre is
  suppressed, banquet is not inflated. Same pattern as Capella.
- **U-shape 70 and boardroom 40** are both high as a share of a 120 theatre room
  and both are plausible on area. A 40 seat boardroom table needs roughly 14 metres
  of length. Taken with the conservative theatre figure this points to a long
  narrow room formed by joining two 85 m2 halves end to end.
- **Ceiling 2.7 m over 170 m2** is plausible for a level two hotel function room,
  and it is genuinely low. It is in the note because it changes what the room can
  hold, not as a criticism.

The room's length and width would settle the geometry. The venue does not publish
them, so it goes on the question list.

## The full space inventory, for reference

Not all of this belongs in the index, but it is what the venue actually has.

| Space | m2 | Ceiling | Published setups |
|---|---|---|---|
| Lachlan / Macquarie joined | 170 | 2.7 | th 120, bq 100, cl 80, ck 140, cab 80, ush 70, bd 40 |
| Lachlan | 85 | 2.7 | th 70, bq 50, cl 40, ck 70, cab 40, ush 30, bd 26 |
| Macquarie | 85 | 2.7 | as Lachlan |
| Bar and lounge, level 3, exclusive | 200 | 3.5 | ck 180, bd 30 |
| Bar and lounge, northern end | 146 | 3.5 | ck 100 |
| Bar and lounge, third | 75 | 3.5 | ck 70 |
| Bar and lounge, quarter | 50 | 3.5 | ck 50 |
| Bar and lounge, southern end | 30 | 3.5 | ck 25 |
| Restaurant, level 2, exclusive | 155 | 2.5 | ck 120 |
| Restaurant, main room | 66 | 2.7 | ck 50, 47 seated |
| Restaurant, lounge | 65 | 2.5 | ck 50, 38 seated dining |
| Restaurant, private dining | 24 | 2.5 | bd 12 |

Spaces are named generically on purpose. The bar and the restaurant both changed
operator and brand in the last ten months.

## What could not be found

Genuinely unpublished by the venue:

- Room dimensions, length by width, for the Lachlan and Macquarie rooms.
- Theatre, classroom, banquet, U-shape and cabaret for the bar and the restaurant.
  Both publish cocktail only, plus one boardroom figure each.
- Any natural light, blackout or rigging specification.

Deliberately left None:

- `ceilq`. The 2.7 m ceiling is uniform and needs no qualifier.

## The four questions for the venue

Karen is sending a thank you anyway, so these ride along:

1. What are the internal dimensions of the Lachlan and Macquarie rooms, joined and
   separated? The published capacities read as a long narrow room and we want to
   describe it correctly.
2. Is classroom 80 or 50 for the joined room? Your capacity chart and your website
   disagree.
3. Does the joined room have natural light, and is there blackout?
4. How does staging load in to level two, and what is the lift access?

## Status check on the venue

- **The food and beverage has completely changed.** Hacienda, the previous bar and
  lounge, closed. Acapulco El Vista opened in its place on 28 November 2025 on
  level three. Flaminia opened on level two on 5 December 2025. Both run by the
  Maybe Group and Giovanni Pilu under Accor's Table For programme. Neither is named
  in the index note, for exactly this reason.
- **The conference rooms and the restaurant share level two. The bar is a floor
  above on level three.** That is not on any floor plan we can find and it matters
  for a pre dinner drinks flow.
- No rebrand, ownership change or closure at the hotel itself.
- The hotel's website distinguishes refurbished "Deluxe" suites from
  "non-refurbished" standard suites, so a refurbishment programme is part way
  through. Recheck in six months.
- Accor's own page at `pullman.accor.com/.../8779/restaurants/r002.html` is stale.
  Its title still reads "Q Dining & Hyde Hacienda" while the body describes the new
  venues. Do not cite it.

## Why I am not recommending a site visit record

Mel's ten photographs from 31 October 2025 are four plated dishes, one bar, one
dining room and four accommodation shots. Two problems:

1. **Six of the ten are inside Hacienda, which closed four weeks later.**
   Publishing them as a current visit record puts a room on the index that has not
   existed since November 2025.
2. **Not one photograph shows a meeting room.** A conference venue capacity index
   record whose visual evidence is a closed bar and four suites is not the receipt
   the page is for.

`seen` stays None until someone walks level two. Half a day gets a 2026 date, the
rooms an organiser actually books, and a post that is current.

## Sources

Venue published material only, for every figure.

- [Meetings and events](https://www.pullmanquaygrandsydneyharbour.com/meetings-and-events)
- [Lachlan / Macquarie Rooms](https://www.pullmanquaygrandsydneyharbour.com/meetings-and-events/lachlan-macquarie-rooms)
- [MICE kit, current](https://document-tc.galaxy.tf/wdpdf-37lvpu058mpchoogd9omau1rr/meetings-events_cms-document.pdf)
- [MICE kit, superseded](https://document-tc.galaxy.tf/wdpdf-3p3bxgsv3900slwfjy46k9jdc/meetings-events_cms-document.pdf)
- [Accor hotel page, largest room 200 m2](https://all.accor.com/hotel/8779/index.en.shtml)
- [Dining, showing the two current venues](https://www.pullmanquaygrandsydneyharbour.com/restaurants/hacienda)

Trade press, used only to date the food and beverage change and to establish which
floor each venue sits on, never for a capacity figure.

- [Hotel Management, 24 Oct 2025](https://www.hotelmanagement.com.au/2025/10/24/sydney-hotels-to-welcome-new-bars-next-month-as-accors-table-for-gets-rolling/)
- [Hotel Management, 28 Nov 2025, El Vista takes over from Hacienda](https://www.hotelmanagement.com.au/2025/11/28/accors-table-for-and-the-maybe-group-opens-el-vista-in-sydney/)
- [Australian Bartender, 28 Oct 2025](https://australianbartender.com.au/2025/10/28/accor-and-maybe-group-introduce-three-new-venues-this-summer/)
