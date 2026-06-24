# CVBS EDM templates — Mailchimp

Email-safe, on-brand templates (teal/navy/stone, Inter). Built for Mailchimp's **Code your own → Paste in code**. Tested structure: tables + inline CSS, 600px, mobile-responsive, bulletproof Outlook buttons.

| File | Use it for |
|------|-----------|
| `cvbs-venue-offer.html` | One venue, one campaign. Handles tiered offers (worked example: Hyatt Caribbean Park). |
| `cvbs-offers-roundup.html` | Monthly "current offers" — 3-4 venues in compact cards. Keeps you in inboxes between big offers. |

## Paste into Mailchimp
1. **Campaigns → Create → Email → Regular.**
2. Set audience, **subject line** + **preview text**.
3. Template step → **Code your own → Paste in code**.
4. Copy the whole `.html` file, paste, **Save**.
5. **Send a test to yourself** (check on mobile — most opens are there).
6. Once happy, **Save as template** so next month is two clicks.

## The offer template — how it's built
The design leads with the deal, in this order: **deal band** (one-line hook) → **spec strip** (3 facts that decide relevance) → **offer panel(s)** → **deadline** → **CTA** → **brief-capture block** → **personal sign-off**.

**Tiered offers (the Hyatt pattern).** The example splits a messy two-part offer into two clear panels: "Booking an event?" (with $5k / $10k spend tiers) and "Booking group rooms?" (room-night rewards). For a **simple offer**, delete the second panel and replace the tier lines with a plain ✓ list. For a **single-number offer** (e.g. Kimpton $110pp), put the number in the deal band and keep one short panel.

**Brief-capture block** — the stone box near the bottom. This is the highest-value part: it converts everyone who doesn't want *this specific venue* but is still planning an event. Don't delete it. It links to `submit-a-brief.html`.

**Personal sign-off** — set to "Karen, Anthony, Chantelle & Rychelle" in your voice. Swap names per sender.

## The roundup template — how it's built
Intro → 3 offer cards (image + 2-line summary + "View offer") → a navy **brief-capture band** as the main CTA → sign-off. Duplicate or delete a card row to change the count. Aim for 3-4; more than that and nothing stands out.

## Edit checklist each send
- **Hero / card images** — swap the `src`. Ideally 600px wide (1200px for retina); cards crop to 190px.
- **Deal band, eyebrow, headline, spec strip** — the scannable top.
- **Offer panels** — tier labels and value-adds.
- **Deadline / "Book by"** — real dates, or delete the amber strip.
- **CTA links** — the proposal button appears in 2 places (MSO + standard); the brief block + footer have their own. Point them where you want.
- **Fine print** — real T&Cs.

## Already wired (don't remove)
Merge tags `*|UNSUB|*`, `*|UPDATE_PROFILE|*`, `*|HTML:LIST_ADDRESS_HTML|*` (your physical address — legally required), `*|ARCHIVE|*`. Mailchimp fills these automatically and **won't send without** the unsubscribe + address.

## Two things to confirm before first send
1. **Images are hosted.** They point at `the-service-edit.github.io/cvbs-2026/...`. Open one in a browser — if it loads, you're fine. If the new site isn't public yet, upload images to **Mailchimp → Content Studio** and replace each `src`. This also future-proofs against any site change.
2. **Contact details.** Set to `+61 414 784 999` / `aj@conferencevenues.com.au` / `conferencevenues.com.au` (from your live Hyatt send). Change if a different team member is the sender.

## Get the most out of these (priority order)
1. **Segment before sending** — send each offer only to the region/size/type likely to care. Relevance beats design.
2. **Sequence each offer** — initial → resend to non-openers with a new subject → "dates closing" nudge.
3. **Authenticate your domain** (SPF/DKIM/DMARC in Mailchimp) and send from a person, not a generic inbox — or design doesn't matter, you land in spam.

## Subject line ideas
**Offer:** "Hyatt Caribbean Park — 5,000 points + a free perk on your event" · "Reward your delegates *and* your budget (Melbourne)"
**Roundup:** "3 venue offers worth holding dates for" · "This month's deals — points, rates and value-adds"
Keep ~6-9 words; strongest detail first.
