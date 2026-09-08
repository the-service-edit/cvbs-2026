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
- **Web app:** Version 4, executes as hello@theserviceedit.com, access **Anyone**
  `https://script.google.com/macros/s/AKfycbxnRCSlKD_vom6CI6_yJnEAPeoehRM-UD4mY9EpIJMag_QMUohrKL_2p1m9RAoadOxntg/exec`
  That URL is already in `BRIEF_ENDPOINT` in `submit-a-brief.html`.
  Shared key: `cvbs-2026-brief`.

**Verified 8 September 2026** by posting two real briefs from the live
`the-service-edit.github.io` origin: both returned `{"ok":true,"ref":"CVB-..."}`,
both landed in the sheet, both emailed with the PDF attached.

## Two emails go out per brief

1. **The internal copy**, to CVBS. Reply-to is the enquirer, so a reply answers
   the client directly.
2. **The enquirer's copy**, their own brief back as a PDF, with the same
   reference. Reply-to is CVBS.

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
