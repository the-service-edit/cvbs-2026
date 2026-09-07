# CVBS production build prompt

Paste this whole file as the first message of a fresh session working in
`/Users/melly_1/APPS/cvbs-2026/CVBS JUNE 2026`. It supersedes any earlier
instruction that this build is a mockup.

---

## Who you are and what changed

You are working with Mel Cox of The Service Edit on the Conference Venues &
Booking Service website. Until 6 September 2026 the build at
`the-service-edit.github.io/cvbs-2026/` was a pitch mockup. **The client has
approved it. It is now a production build that will replace
`conferencevenues.com.au`.**

Everything that was previously "fine, it is only a mockup" is now real: the
placeholder form key, the GitHub canonicals, the missing privacy and terms
pages, the orphaned legacy URLs, the copied venue statistics. Treat all of them
as live-site defects.

Your job is to work through the consolidated website audit of 6 September 2026
(28 prioritised actions, P0 to P3) and take the build to a defensible launch,
then past it. You are also producing the client decision sheet for the items the
build cannot decide on its own.

## The three things that must never slip

**1. Never invent a fact.** No capacity, room count, ceiling height, floor area,
distance, transfer time or price is ever typed from inference. Every figure
comes from a source file with `src` and `checked` fields, or the site says "not
published" and the build reports the gap. If you cannot source it, you say so
and stop. A wrong capacity at the enquiry point is the single most damaging
thing this site can do, because CVBS sells judgement.

**2. The voice is locked.** Warm, plain, written by a hospitality operator, not
a marketer. No em dashes anywhere, ever. Do not use the word "index" in
customer-facing site copy. No punchlines, no SaaS lines, no "unlock", "elevate",
"seamless", "in today's landscape". Short sentences. Say the useful thing and
stop. Match the voice already in `venues_sydney.py` note fields, which is the
reference.

**3. Nothing ships without the build check passing.** `python3
scripts/check-site.py` must print `0 failures` before you tell Mel a phase is
done. If your change made it fail, you fix it, you do not lower the check.

## How the site is actually built

This is a generated static site, not hand-edited HTML. 528 HTML files, 190
venues in `assets/data/venues.json`, 16 destination pages, 5 venue detail pages
under `/venue-visits/`.

Facts live here:

```
_venue-index-source/venues_sydney.py        54 Sydney venues with sourced capacities
_venue-index-source/venues_destinations.py  the other 15 destinations
_venue-index-source/venues_extra.py         the joins: which venue has a page, an offer, a destination
_venue-visits-source/build_venue.py         room by room data for the 5 inspected venues
_destination-source/destinations.py         destination page copy, never capacity figures
```

Build order, always in this order:

```
python3 _venue-index-source/build_dataset.py
python3 _venue-index-source/build_city_index.py "<City>"    (PARKED 7 Sep, skip it)
python3 _destination-source/build_destination.py            (runs with or without the index)
python3 _destination-source/build_hub.py
python3 _venue-index-source/build_finder.py
python3 _venue-index-source/build_accom.py
python3 _entity-source/gen_entity.py                        (always last)
python3 scripts/check-site.py                               (must print 0 failures)
```

After `build_venue.py` or `build_westin.py`, also run `patch-venue-pages.py`,
`patch-nav.py` and `fix-faq-schema.py`.

Read `_venue-index-source/BUILD.md` in full before your first change.

**If a fix can be made in a generator, make it there.** Editing output HTML that
a script will overwrite is the mistake that has already produced most of the
contradictions in the audit.

## How to work

- Work on Mel's machine with `device_bash`. Do not stage files into the
  container unless you need to view an image or a PDF.
- Back up before any destructive pass, using the existing convention:
  `_backup-pre-<change>-<ddmmm>`.
- You cannot push. Mel pushes from her own terminal. Tell her exactly what to
  push and when.
- **Work one phase at a time and stop at each gate.** Show what changed, show
  the check output, wait. Do not run ahead into the next phase.
- Anything that needs a CVBS decision goes on the sign-off sheet. Do not invent
  a commercial claim to unblock yourself.

---

## Phase 0. Ground truth and release process

**Audit action 1 (P0).**

Before touching content, make the deployment trustworthy.

1. Capture the current deployed state so a regression is detectable. During the
   audit `assets/js/finder.js` and `assets/css/finder.css` returned 404 on the
   live URL while existing locally, and the results page was empty. Local file
   existence is not proof the site works.
2. Get `scripts/build-public.sh` and the GitHub Actions workflow actually live:
   Pages source switched to GitHub Actions, `WEB3FORMS_ACCESS_KEY` set as a repo
   secret. Until that is done the branch deploy publishes the placeholder key
   across 341 files.
3. Add a release smoke test: referenced assets exist on the deployed URL, a
   search returns results, the form posts. Keep the recovered 404 incident as a
   regression case.

**Gate: a deployed URL you can verify, and a repeatable way to deploy it.**

---

## Phase 1. P0 launch blockers and quick wins

**Audit actions 2, 3, 4, 5, plus the 12 quick wins.**

1. **Brief and newsletter delivery (action 2).** Replace the placeholder
   configuration with approved credentials. Test one authorised non-production
   enquiry and one subscription through receipt, error, retry and duplicate
   click. Never show success until the recipient service confirms acceptance.
   The existing handlers already follow that principle. Keep it.
2. **Venue enquiry panels (action 3).** Crown Towers Sydney's figures
   (390 theatre / 340 banquet / 349 rooms) are copied into Pullman Bunker Bay,
   Hotel Indigo Melbourne Little Collins and Pullman Quay Grand Sydney Harbour.
   Hotel Indigo is a 12 person boardroom hotel. Fix this in `build_venue.py` so
   every panel is generated from that venue's own record, then rebuild. This is
   the most urgent single item in the audit.
3. **Brief draft handling (action 4).** A Bunker Bay enquiry survived into a
   Melbourne comparison, then a Hamilton Island offer retained Melbourne as
   preferred location. Implement explicit new versus resume state, isolate event
   context, separate generated venue notes from user written notes, and show a
   review summary before submission. Do not silently erase a client's draft.
4. **Unfinished modules (action 5).** Remove or replace the draft price tables
   and the unfinished case module on the conference sourcing and cost guide
   pages. "Placeholder values" and "DD Month 2026" must not exist in a public
   page. Removing the word "Draft" is not a fix.
5. **The quick wins.** Correct the venue visits hub count (it says 58, the
   finder has 190, and they measure different things: say "five published venue
   inspections"). Mark the expired August offers expired and pull them from
   current promotion. Deduplicate the destination select options, which double
   because the script appends counted options to existing HTML options. Darken
   the primary CTA fill: white on `rgb(40,168,182)` measures about 2.85:1
   against a 4.5:1 requirement. Add autocomplete attributes to name, email,
   telephone and organisation. Make homepage destination tiles link to their own
   detail pages rather than the hub. Add "Find a venue" to the mobile menu and
   internal page headers. Rename client "Results" to "Client stories".

**Gate: nothing on the public site is a placeholder, a draft, or a fact
belonging to a different venue.**

---

## Phase 2. Production domain and cutover

**Audit action 14 (P1), plus the items the mockup status was hiding.**

The destination is `conferencevenues.com.au`, replacing the existing
WordPress/Divi site. Mel has said there is a lot to do before that point, so
build the cutover, do not execute it.

1. Rewrite canonicals, OG URLs, sitemap URLs and schema `url` values. 406 pages
   currently canonicalise to `the-service-edit.github.io`. This must be a
   generator level change with a single configurable base URL, not a find and
   replace.
2. Deploy a correctly located root `robots.txt`. The current file at
   `/cvbs-2026/robots.txt` is not read by crawlers as an origin robots file and
   its rules point at root paths that do not exist on the project host.
3. Exclude internal working files from the public artifact: the Digital Hub,
   strategy documents, prototypes, email previews, backup folders and standalone
   tools. `build-public.sh` already allowlists from `sitemap.xml`. Verify it.
4. Map the 12 legacy URLs that a cutover would orphan: `/bestvenue`, `/groups`,
   `/relocation`, `/venuereviews`, `/get-a-quote`, `/about`, `/about/reviews`,
   `/contact-us`, `/privacy`, `/booking-terms`, `/terms`, `/feed`. Produce a
   redirect map with a destination for each. Flag any that have no equivalent.
5. Write privacy policy and terms pages. The build has none. The old site has
   three. This is a legal requirement, not a nicety, and needs CVBS approval.
6. Fix `client-1.jpg` and `client-2.jpg`, currently used as Karen and Anthony on
   the homepage and as anonymous clients "Sarah M." and "David R." on the
   results page. That is a credibility failure on a trust page.
7. Keep `venue-results.html` at `noindex, follow` and out of the sitemap. That
   split is the whole indexation strategy.

**Gate: a written cutover plan with a redirect map, and a build that would be
correct the moment DNS changes.**

---

## Phase 3. One venue truth

**Audit actions 6, 7, 8, 19 (P1). This is the expensive phase and the one that
protects the commercial position.**

1. **Venue data reconciliation (action 6).** Crown shows 11 event rooms in
   results and three bookable spaces on its detail page. Ceiling and area are
   known in one template and "not published" in another. Perth still promotes
   Hyatt Regency Perth, which ended Hyatt management on 31 August 2024 and now
   trades as Residence on Langley Park. Reconcile identity, capacities, room
   definitions, ceiling and area, and accommodation. Prioritise the five detail
   venues, Perth and Melbourne. Record source, date and conflict status on every
   figure.
2. **Shared fact rendering (action 7).** Generate result cards, venue panels,
   comparison rows, factual FAQ answers and JSON-LD from the same records in the
   same pass. Manual duplication is what recreated the contradictions. The
   pipeline already does this for destination cards. Extend it to venue detail
   pages and enquiry panels.
3. **Accommodation model (action 8).** Eligibility currently depends on a known
   numeric room count, so Crown Melbourne, Westin Perth and Pullman Quay Grand
   drop out of the accommodation filter despite having confirmed accommodation.
   Model existence, relationship to the venue (same building, onsite complex,
   adjacent, offsite), inventory and availability as four separate things.
   Yes / no / unknown, and unknown is not no.
4. **Editorial claims (action 19).** Review every "the only", "no answer",
   "effectively blocked", "unavailable", "nobody can go home" and every largest
   claim. Replace with scoped statements: "Among the venues currently verified
   in our research" or "Check availability early during". Differentiate
   standing, theatre, banquet, bedroom inventory and sleeping capacity, which are
   five different measures currently used interchangeably. Add verification
   dates to substantial destination claims. Run the adversarial pass in the
   `cvbs-venue-index` memory: try to refute every superlative before shipping.

**Gate: no two pages disagree about the same venue, and every superlative
survives an attempt to refute it.**

---

## Phase 4. Discovery, matching and handoff

**Audit actions 9, 10, 11, 12, 15, 16, 17, 18, 21, 22.**

1. **Navigation (action 9).** One shared header and footer. Finder and shortlist
   on every template family, mobile especially. Correct the brief footer service
   links and the duplicate skip links on venue pages. Standardise "Corporate
   accommodation" versus "Corporate relocation".
2. **Finder controls (action 10).** One source for select options. Validate
   before updating the URL or rendering. Entering 99,999 currently produces both
   a validation message and rendered results.
3. **Finder matching (action 15).** Rank by the best matching room at the
   selected layout, not by headline venue capacity. Melbourne Museum's 200
   delegate result currently leads with a 600 seat foyer while its own copy
   describes a 214 seat theatre. Model combined and divided room relationships.
4. **Venue name search and cards (action 16).** There is no venue name lookup.
   Add name and alias search. Let truncated card notes expand rather than
   sending users to an external PDF. Add a "View details" route where a profile
   exists.
5. **Shortlist handoff (action 11).** Save and Compare currently maintain
   separate selections. Unify them or make the distinction explicit. Carry exact
   headcount, layout and accommodation need into the brief. Flag mixed
   destinations and confirm the shortlist before handoff.
6. **Offers (action 12).** Centralise booking and event expiry. Two of three
   headline offers have expired and are still promoted as current. Tie
   promotional badges to real offer detail routes. Fix the Hamilton Island
   location handoff.
7. **Venue profiles (action 17).** Most of the 190 venues have no detail page.
   Build complete profiles for venues frequently needed at 100 to 300 delegates,
   Melbourne first. Do not mass produce thin profiles.
8. **Destination templates (action 18).** Move browse, filter and jump links
   above the repeated featured sections. Consolidate duplicate venue summaries.
   Sydney is the worst offender.
9. **Shareable comparison (action 21).** Read only shortlist link and a print
   output with no personal contact data in the URL. An EA needs to send this to
   a manager. This is how CVBS enters the internal approval process.
10. **Brief and calculator (action 22).** Pass calculator inputs, assumptions and
    estimate into the brief. Add conditional rooms per night, occupancy and date
    fields.

**Gate: a user can search, understand, shortlist, compare, share and enquire
without a fact changing under them.**

---

## Phase 5. Trust, quality and measurement

**Audit actions 13, 20, 23, 24, 25, 26, 27, 28.**

1. **Buttons and contrast (action 13).** Default, hover, focus and gradient
   states.
2. **Mobile comparison and tables (action 20).** Prioritise the requested setup
   and the differences. Add visible scroll cues to contained horizontal scroll.
   Retain row and header context.
3. **Visit publishing (action 23).** Named inspector, visit date, scope,
   observations and photo captions as separate fields. Link inspection to venue
   to destination bidirectionally. Do not imply Karen inspected a venue because
   her portrait sits beside the CTA. Do not claim the five published inspections
   are every venue CVBS has ever visited.
4. **Trust and service wording (action 24).** Standardise the business name: the
   build uses both "Conference Venues & Booking Service" and "Conference Venues
   and Booking Services". Approve the payment, savings, turnaround, contract and
   case study claims. The 14 percent saving needs a basis or it comes off.
5. **Guides and collections (action 25).** Answer the question before asking for
   a brief. Publish approved cost answers. Consolidate overlapping selection
   articles.
6. **Performance and accessibility (action 26).** Throttled mobile LCP, INP and
   CLS on homepage, results, a long destination page, a venue and the brief.
   Contrast, focus, keyboard and zoom audits. Do not lazy load the above the
   fold hero. Replace the animated counters' raw HTML zero, which is visible in
   source as "0 years" and "0 hours".
7. **Measurement (action 27).** Track research to shortlist to brief to
   confirmed receipt to qualified enquiry, with data minimisation. Review after
   30 days.
8. **Expansion (action 28).** Curated city and need collections only after
   inventory and conversion quality stabilise. Not before.

---

## Do not build

The audit is explicit and Mel agrees: no mandatory accounts, no CRM style client
portal, no loyalty system, no chatbot, no opaque fit scores, no automated "best
venue" ranking, no live booking calendar or instant quote presented as
authoritative, and no thousands of capacity by city by event type landing pages.
Human judgement is the product. Do not automate away the thing being sold.

---

## The client sign-off sheet

Produce `CVBS-Client-Decisions-Sep-2026.docx` alongside the work. One page, one
question per row, each with the options and the consequence of each. It covers
everything the build cannot decide:

- The approved legal and trading entity name, and the CVBS abbreviation.
- The operational promise: is 48 hours an initial response or a costed
  shortlist, business hours or elapsed, and what are the exceptions.
- The approved account of how CVBS is paid: who pays, what is commissionable,
  whether exceptions exist, how recommendations are selected, who contracts.
  Note that "commissions are broadly similar" does not establish independence
  and a corporate buyer will challenge it.
- Whether the 14 percent saving is a real anonymised engagement or an
  illustration, and if real, the comparison basis and date.
- Approved rate bands and worked examples for the cost guide, with currency,
  GST treatment, dates and inclusions.
- Whether CVBS wants "worldwide" retained, and how international sourcing is
  described relative to the Australian inventory.
- Privacy policy and terms content, and who is the data controller.
- The production Web3Forms recipient inbox and who monitors it.
- Which venues CVBS wants profiled first at 100 to 300 delegates.

Write it in Mel's first person commercial voice. No em dashes.

---

## First message back

Do not start work. Reply with:

1. Your read of the current repository state against Phase 0, from actually
   running the build and the check, not from this document.
2. Anything in the audit you think is wrong, and why.
3. What you propose to do in Phase 1, as a numbered list with file names.

Then stop and wait.
