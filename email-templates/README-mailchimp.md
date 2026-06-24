# CVBS Venue Offer — Mailchimp EDM

Email-safe, on-brand template (teal/navy/stone, Inter). Built for Mailchimp's paste-in HTML editor. Works in Gmail, Apple Mail, Outlook (bulletproof button included).

## Paste it into Mailchimp
1. **Campaigns → Create → Email → Regular.**
2. Pick your audience, set the **subject line** + **preview text** (the template has a hidden preheader, but Mailchimp's preview field overrides it — set both to match).
3. At the template step choose **Code your own → Paste in code**.
4. Open `cvbs-venue-offer.html`, copy everything, paste it in, **Save**.
5. Send a **test email to yourself** before scheduling.

Tip: once it looks right, **Save as template** in Mailchimp so the next offer is two clicks away.

## What to edit each send
Search the file for these and swap them:

- **Hero image** — `hamilton-island.jpg` → your venue image (ideally 600px wide, ~1200px for retina).
- **Eyebrow** — `Spring 2026 • Hamilton Island • Whitsundays, QLD`.
- **Headline + intro** — the `<h1>` and the paragraph under it.
- **Offer box** — "The offer" heading and description.
- **Available dates** — delete the row if not relevant.
- **Inclusions** — the ✓ rows (copy/delete a `<tr>` to add or remove).
- **CTA link** — appears **3 times** (hero image, button MSO + button link). Update all three to the same URL.
- **Footer** — phone, email, intro line.

## Images must be hosted (important)
Email can't use local files. The template points at your live site:
`https://the-service-edit.github.io/cvbs-2026/assets/img/...`

Two options:
- **Keep that** if your GitHub Pages site is live and public — confirm the image opens in a browser.
- **Safer:** upload the hero + logo to **Mailchimp → Content Studio**, then replace each `src="..."` with the Mailchimp-hosted URL. This guarantees images never break and survives any site change.

## Merge tags already wired
`*|UNSUB|*`, `*|UPDATE_PROFILE|*`, `*|HTML:LIST_ADDRESS_HTML|*` (your physical address — legally required), `*|ARCHIVE|*` (view in browser). Mailchimp fills these automatically. Don't remove the unsubscribe or address — Mailchimp blocks the send without them.

## Subject line ideas
- Spring at Hamilton Island — reduced rates for your next conference
- Up to 700 delegates in the heart of the Reef (CVBS rates)
- A spring offer worth holding dates for

Keep ~6–9 words; the strongest detail goes first.
