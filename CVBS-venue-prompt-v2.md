# The weekly venue prompt, v2

Paste this, drop the photos in, answer two questions. One venue in, four assets
out: the website record, the Instagram and Facebook carousel, the LinkedIn
re-cut, and the post copy.

---

## THE PROMPT

> Build the venue record for **[VENUE NAME]**, **[CITY]**.
>
> Photos are in `site-visits/[venue-slug]/` in the project folder.
>
> Here is what I know: **[paste anything you have. The visitor's name, the date,
> which rooms they were in, what they said about it, who they met. If you have
> nothing, say "nothing, photos only".]**
>
> Research the rest yourself from the venue's own current published material.
> Then produce all four:
>
> 1. The website record at `venue-visits/[venue-slug]/index.html`, wired into the
>    hub and the [city] band.
> 2. The Instagram and Facebook carousel, my Post Designer templates, 2160x2700.
> 3. The LinkedIn re-cut, 2400x1256.
> 4. The post copy: IG caption, first comment, and Karen's LinkedIn draft.
>
> Publish what you can verify. Drop anything you cannot. Do not ask me to fill
> gaps before it ships.

---

## The rule that governs everything

**Publish what is verified. Omit what is not. Never advertise the gap.**

There is no draft state, no noindex holding pen, no "pending" badge and no
placeholder text. A field we cannot verify is simply absent from the page. The
record ships on what it has.

A **verified negative about the venue** still gets stated, but once, quietly, in
the collapsed source note under the capacity table. "Crown does not publish its
ballroom floor area" explains why the table has dashes in it. It does not get a
section of its own. See the commercial rule below.

The distinction, every time:

| | |
|---|---|
| **Our own hole** ("we do not know who visited") | Disappears without trace |
| **The venue's non-disclosure** ("Crown publishes no floor area") | One line in the collapsed source note |

## Write about the venue, and nothing else

A client landed on a venue page to read about that venue. They do not care about
our filing, our method, or how many photographs we hold. Everything on the page
must be a fact about the building or a judgement about what it suits.

Cut on sight: photo counts, "we index it as", "we would rather say that here
than have you find out at the shortlist", any heading naming our process ("why
we check every number"), and any section that is really about other venues
wearing this venue's name.

**Never criticise a venue's own website.** Site visits are often comped or
discounted by the venue. A section dissecting the errors, contradictions or
stale pages on a host's website is the wrong thing to publish whatever it does
for an answer engine, and it reads as ungrateful to the people who let us in.
Where a venue's own sources disagree, use the current one, say so once in a
neutral line inside the collapsed source note, and move on. This was got wrong
twice on 5 September 2026 and corrected both times.

State a limit as a fact about the building, not as a verdict. "This is a hotel
built for delegates to sleep in rather than to meet in" is a fact. "Everything
above twelve people needs another building" is us telling them off.

## The commercial rule: never publish the questions

**Do not publish a list of questions to put to the venue, and never publish what
we ask before holding a room block.** Read from a client's chair, a list like
"ballroom floor area and its length by width, clear ceiling height under the rig,
rigging points and floor load, block release terms and the attrition point" is a
briefing document for ringing the venue directly and booking without us. The
second list is worse: it is the negotiation playbook.

CVBS is paid a commission by the venue on bookings it brokers. A page that
teaches a client to self-serve is a page that costs money, whatever it does for
an answer engine. This was got wrong once and corrected on 5 September 2026.

**Publish what is already published online for the spaces and the accommodation**,
plus our judgement on fit. The capacity table, the room and villa data, what the
building suits, where it stops working, which rooms in that city are larger, and
what has changed recently. That is unique, it is quotable, and none of it hands
over the job.

## What we may claim

Someone from CVBS inspects the venue. **They will not always see every room.**

- Say **"Inspected by CVBS"**. True on every record.
- Then name **only the spaces we actually stood in**, and say plainly which ones
  we did not: *"We have stood in the Pearl Ballroom and the Pre-Function Foyer.
  We have not been inside the Opal Suite or The Pavilion, so their figures come
  from the venue's chart rather than from us."*
- **Never** "we walked the venue" as a blanket claim.
- Add the date **only if it is read off the photograph's own capture data or Mel
  states it**. Never typed, never inferred, and where absent the record simply
  does not mention a date.

## Photographs

- Process to 900px, strip metadata by rebuilding pixels on a fresh canvas, write
  to `assets/img/venue-visits/[slug]/`. Originals stay in `site-visits/`, which
  is gitignored.
- **No captions.** A caption is a claim, and describing a photo you did not take
  is guessing. Alt text carries the venue name, plus the room name **only** where
  the space has been confirmed against the venue's own published imagery.
- Group by track: event floor, accommodation, rest of the building.
- **Ask once, before processing: are these ours?** A batch that is uniformly
  sized with all metadata stripped, every frame level and every room dressed and
  empty, is a professional shoot. If it is not ours it cannot be published.
- Watch for a third party's branded event in frame. Flag it before it leads.

## Two tracks, not one

Every record carries an **event track** and an **accommodation track**,
independently. Guest room photos are not a failed event record, they are a
complete accommodation record. Group accommodation is half of what CVBS sells at
a hotel and the half a floor plan says nothing about.

The accommodation section carries what the venue publishes: room or villa count,
types and sizes, and anything it discloses about the block. It does not carry the
questions we would ask before holding one. Link out to
`group-accommodation.html` and `corporate-accommodation.html`.

## Research, in order

1. **Capacities off the venue's own chart only.** Never a directory.
2. **Check the copyright year on every source.** Venues leave old pages up. Crown
   runs two official sites that disagree by 40 seats, the older one carrying a
   2019 to 2022 copyright. The Westin's Marriott fact sheet is dated 2017 and
   predates the building.
3. **Open every asset, do not trust its label.** The file marked "Floorplan of
   Pearl Ballroom" on Crown's own page is a map of Barangaroo.
4. **If the venue list page renders empty**, pull the space list from the site's
   `sitemap.xml`.
5. **Staleness check, always.** Rebrand, operator change, closed restaurants and
   bars in the last 24 months. This caught Settimo at the Westin and Oncore at
   Crown, and it is the highest value ten minutes in the job.
6. **Refute every superlative before publishing it.** Name the rooms in that city
   that are larger, each off its own venue's material, and say plainly that the
   market was not surveyed comprehensively.

## Why this still works for SEO, AEO and DEO

Stripping unverifiable detail does not weaken the page, because none of the three
ever depended on it.

- **SEO.** The page is indexable from the day it ships instead of sitting in
  noindex. Unique first-party photography, a capacity table no directory has, and
  internal links to the city page and both accommodation services.
- **AEO.** Answer engines want short, attributable, quotable facts. The FAQ
  schema answers the five questions organisers actually ask, each in one
  self-contained paragraph with the figure in it. Placeholder text is the enemy
  here: "DATE PENDING" is quotable, and quoting it is a disaster.
- **DEO.** The entity graph ties the record to the CVBS organisation, the venue
  as a `Hotel` with its `MeetingRoom` children, and photographs credited to CVBS.
  Never `Review` or `AggregateRating`, because CVBS is paid commission by the
  venue and a score from a paid party is worthless.

The strongest AEO asset on these pages is **Recent changes**, kept strictly to
facts about the venue: a restaurant that closed, an outlet now trading under a
new name, a seasonal bar shut until a given date. Nobody else tracks it and it
proves the page is current. It is not a place to point out that a venue's own
website is wrong.

## The four assets

**1. The record.** `_venue-visits-source/build_venue.py`, one VENUE dict per
venue. Chrome, nav, footer and entity graph are lifted from
`venue-finder-sydney.html` at build time, so pages cannot drift. Re-run every
builder after any nav change. Then `build_hub.py`, then the city band, then add
the URL to `sitemap.xml`.

**2 and 3. The carousels.** Do not design anything. Drive Mel's own tool:
stage `Post-Designer/CVBS-Post-Designer.html` into the container, open it in
headless chromium, set `carousel.slides` from `newSlide(template)`, inject photos
as data URIs, call the tool's own `shot()` per slide. `carousel.format` is `ig`
for 2160x2700 and `wide` for 2400x1256. Output is identical to what Mel would
make by hand.

Seven slides that work: `venue` cover with three verified numbers, `photocap`
on the best room, `stattrio` for the shape of the building, `photocap` on
accommodation, `textnavy` on what the room suits, `textnavy` on what changed
recently, `cta`. Do not use the `checklist` template for questions to ask a
venue, and do not build a slide about a venue's website being wrong.

**4. The copy.** IG caption is two or three sentences, no hashtag stack, site at
the end. Karen's LinkedIn is first person, her judgement, one specific thing she
would not have known from a website, and no CTA. Mel ghost-writes, Karen
approves, it goes out in her name.

## Never

- No rates, ever. What a venue does on a day delegate package is what CVBS
  negotiates.
- No question lists, on the page or in a carousel. See the commercial rule.
- No criticism of a venue's own website, anywhere. They often host us for free.
- No ratings, no scores, no `Review` schema.
- Fit, not fault. "Comfortable at 200, tight at 400" is expertise. "The room is
  too small" is a review that earns Karen a phone call.
- No em dashes.
- Claude cannot push. Hand Mel the command block.
- Never run git in the mounted folder, not even `git status`. The mount cannot
  unlink, so it leaves a lock that breaks Mel's own terminal.
