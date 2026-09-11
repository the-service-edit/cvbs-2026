# CVBS brief store

When someone submits the brief on `submit-a-brief.html`, this records it in a
Google Sheet and emails a CVBS branded PDF of that brief.

**The order matters and it is deliberate.** The sheet write happens first, the
email second. If the PDF fails to render or the mail fails to send, the brief is
already banked and Mel gets told. A lead is never lost because of an email
problem.

## It is live

Built and deployed 8 September 2026 in Mel's Google account,
hello@theserviceedit.com.

- **Script project:** "CVBS brief store" (standalone, not bound to the sheet)
  `https://script.google.com/u/0/home/projects/165IjLqzxz_vmlvbKKw7UquM1nZiqB4XfwMWpDPmQhalmNmt3_m-Z2H_F/edit`
- **Sheet:** "CVBS Briefs", created by the script on first run, id held in Script
  Properties as `SHEET_ID`
  `https://docs.google.com/spreadsheets/d/1jXUa_hgk7VOxVWGUrCq3Wl9U5s5DOnstPHHAFzLuvz8/edit`
- **Web app:** Version 6, executes as hello@theserviceedit.com, access **Anyone**
  `https://script.google.com/macros/s/AKfycbxnRCSlKD_vom6CI6_yJnEAPeoehRM-UD4mY9EpIJMag_QMUohrKL_2p1m9RAoadOxntg/exec`
  That URL is already in `BRIEF_ENDPOINT` in `submit-a-brief.html`.
  Shared key: `cvbs-2026-brief`.

**Verified 8 September 2026** by posting two real briefs from the live
`the-service-edit.github.io` origin: both returned `{"ok":true,"ref":"CVB-..."}`,
both landed in the sheet, both emailed with the PDF attached.

## Two emails go out per brief

1. **The internal copy**, to CVBS. Plain text on purpose: it is a work queue and
   wants to be scannable, not admired. Sender name **CVBS Website Enquiry**.
   Reply-to is the enquirer, so a reply answers the client directly.
2. **The enquirer's copy**, a branded HTML email built on the wave EDM system,
   with their brief attached as a PDF. Sender name **Conference Venues**,
   matching the CVBS rule that the inbox row is the business. Reply-to is CVBS.

### The client email

Lives in `ClientEmail.html`. Three rules govern it.

**It is transactional, not marketing.** No Mailchimp merge tags, no
unsubscribe, no archive link. Merge tags would render literally as `*|UNSUB|*`
because nothing here goes through Mailchimp, and an unsubscribe on a
confirmation someone asked for is wrong anyway.

**Image URLs are cached permanently.** Apple Mail Privacy Protection and Gmail
pre-fetch through a proxy and cache failures forever, so a URL that 404s during
one test stays broken for that recipient. The template reuses the exact `?v=3`
URLs already proven by the EDMs. Verified 200 on 8 Sep 2026. Do not invent a new
version number unless the image itself changed.

**A plain text version is sent alongside the HTML**, and is what a text only
client sees. Change one and change the other.

`ASSET_BASE` in `Code.gs` points the images and links at
`the-service-edit.github.io/cvbs-2026`. Flip it to `https://conferencevenues.com.au`
at cutover.

## Handed over, 8 September 2026

`LIVE = true` and `CLIENT_LIVE = true` in the repository mirror of `Code.gs`.
**Neither takes effect until the same change is made in the Apps Script editor
and the project is redeployed.** The file in this folder is a mirror, not the
running code.

- **Internal brief goes to `aj@conferencevenues.com.au`.** Address confirmed by
  Mel on 8 September 2026. It is `.com.au`, not `.com`. An earlier version of
  this README said the opposite and was wrong.
- **Karen is not a recipient.** `TO` carries AJ only and `CC` is empty. If she
  should receive briefs, add her to `CC` in the same editor session.
- **Client copies are on but gated.** They will not send until
  `RESEND_API_KEY` is set in Script Properties. See "The right from address"
  below. Until then every brief sends Mel a failure notice and a
  `[CLIENT PREVIEW]` copy, and the enquirer receives nothing.

## The redeploy trap

**Saving is not deploying.** Editing `Code.gs` and pressing save changes nothing
about what the live web app runs. After any edit:

Deploy, Manage deployments, the pencil icon, Version **New version**, Deploy.

The `/exec` URL does not change, so `submit-a-brief.html` never needs touching
again. This caught the review tool in September and it will catch this one.

## The PDF, and the one rule that governs it

`BriefPdf.html` is rendered by `Utilities.newBlob(html).getAs('application/pdf')`,
which is **not a browser**. Tested on 8 September 2026:

| Works | Does not work |
|---|---|
| Text colour | **Every background colour.** CSS `background`, `bgcolor`, both ignored |
| Borders and rules | flexbox, grid |
| Tables | CSS variables |
| Images, including data URIs | Web fonts. Inter will not load, it falls back to Helvetica |

The first build used a navy table cell for the header. It came out white on
white with an invisible white logo. **The header is now a baked PNG** with the
navy, the logo and the title already in the pixels, and every other block reads
through borders and type rather than fills.

Do not add `background-color` to this template. It will render white and nobody
will notice until Karen forwards it to a venue.

To change the header, edit and run `build-band.js` in a Chrome console, then
paste the base64 over `__BAND__` in `BriefPdf.html`. The copy in the repo keeps
the placeholder; the copy in the Apps Script editor has the base64 inlined.

Structure, in this order and for a reason: band, reference and timestamp, then
four fact cells (delegates, location, dates, budget), then **the client's own
words pulled up high** rather than buried under "notes", then the brief, then
contact. Karen triages in ten seconds, so the deciding facts come first.

Dates carries a computed **lead time**, "27 weeks away" or "31 days away,
tight". It is arithmetic, not a guess, and it is what turns a printout into a
triage document.

## Still to do: the right from address

**This is now the only thing standing between a submitted brief and the client
receiving their copy.** It is also what stops AJ's notification landing in junk:
a mail from an unrelated Google account into a Microsoft 365 tenant is a strong
junk-folder candidate, and a brief in junk is a lost brief.

1. Sign up at resend.com. Free covers 3,000 emails a month.
2. Add the domain as a **subdomain**: `mail.conferencevenues.com.au`. Use the
   subdomain, never the root. CVBS already has SPF and DKIM on
   `conferencevenues.com.au` pointing at Microsoft, and a second SPF record on the
   root would break their normal email. A subdomain leaves their mail untouched.
3. Ask whoever manages that DNS for the three records Resend shows. They look
   like this and all go on `conferencevenues.com.au`:

| Type | Name | Value |
|---|---|---|
| MX | `send.mail` | `feedback-smtp.<region>.amazonses.com` priority 10 |
| TXT | `send.mail` | `v=spf1 include:amazonses.com ~all` |
| TXT | `resend._domainkey.mail` | the long DKIM key Resend gives |

4. In Apps Script: Project Settings, Script Properties, Add script property,
   name exactly `RESEND_API_KEY`, value the key. It lives there and only there.
   Never in the website, never in the repository. The repository is public.
5. Redeploy.

The script picks the key up on its own. If Resend ever fails it falls back to
the Google account rather than dropping the brief, and emails
`hello@theserviceedit.com` to say so.

## Files

| File | What it is |
|---|---|
| `Code.gs` | The backend. Mirror of what is in the editor. |
| `BriefPdf.html` | The PDF layout, with `__BAND__` where the header image goes. |
| `ClientEmail.html` | The branded HTML email sent to the enquirer. |
| `build-band.js` | Regenerates the header PNG. Run in a Chrome console. |
| `_render_sample.py` | Local preview of the ORIGINAL fills-based layout. Superseded, kept only as a reference for the content order. |

## When something goes wrong

**Nothing arrives and the page shows the fallback.** Open the `/exec` URL in a
browser. It should return `{"ok":true,"service":"cvbs-brief-store"}`. If it asks
for a login, the deployment is not set to "Anyone".

**A row appears but no email.** Look at the `sent` column in the sheet. `resend`
means it went via the domain. `mailapp` means the Google fallback. `FAILED`
means check `hello@theserviceedit.com` for the reason.

**The email arrives without the PDF.** The renderer choked. Every field is still
in the sheet and the plain text body carries the essentials. Read the table
above before changing anything in `BriefPdf.html`.

**Testing from a terminal does not work.** The cloud container cannot reach
`script.google.com`. Test from a browser tab on the live site's own origin.

## Release of 11 September 2026 (not yet deployed)

`Code.gs` and `ClientEmail.html` in this folder were hardened on 11 Sep 2026.
**The live endpoint is unchanged until you do the steps below.**

What changed:

- Every field is checked server-side: unknown fields dropped, each field cut to a
  length ceiling, email format checked, dates must be `YYYY-MM-DD`, and the fields
  echoed back to the enquirer (first name, location detail, delegates) cannot carry
  links, so the form cannot be used to send CVBS-branded mail with someone else's words.
- Malformed or unkeyed requests are answered and never emailed. Real failures alert at
  most once per 15 minutes, with the brief's fields, never the raw request body.
- The PDF escapes every typed value (the budget used to go in unescaped).
- The Sheet formula guard also covers leading tab and carriage return.
- `ASSET_BASE` can be set as a Script Property, so cutover needs no code release.
- The client email links to `/client-stories/` (the old `results.html` no longer
  exists on the rebuilt site).

To deploy, in the Apps Script editor for the brief store:

1. Paste this folder's `Code.gs` over the editor's `Code.gs`, and `ClientEmail.html`
   over `ClientEmail`. Save.
2. **Deploy > Manage deployments > the existing web app > pencil (Edit) > Version:
   New version > Deploy.** Do NOT use "New deployment": that makes a new `/exec`
   URL and the website form silently stops working.
3. Confirm the `/exec` URL shown is still the one in `submit-a-brief.html`
   (`AKfycbxnRCSl...`).
4. Send one test brief from the site using your own address and check: a new Sheet row,
   the internal email and PDF, and the client copy or preview.

At cutover, add Script Property `ASSET_BASE` = `https://www.conferencevenues.com.au`
only after the new site is live there and its `/assets/img/email/` images load.
