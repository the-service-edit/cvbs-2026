# CVBS brief store

When someone submits the brief on `submit-a-brief.html`, this records it in a
Google Sheet and emails Karen and Anthony a CVBS branded PDF of that brief.

**The order matters and it is deliberate.** The sheet write happens first, the
email second. If the PDF fails to render or the mail fails to send, the brief is
already banked and Mel gets told. A lead is never lost because of an email
problem.

Files:

| File | What it is |
|---|---|
| `Code.gs` | The whole backend. Paste into Apps Script. |
| `BriefPdf.html` | The PDF layout. Paste into Apps Script as a second file. |
| `_render_sample.py` | Local preview only. Writes `_sample.html` so the layout can be checked in a browser without deploying. Never runs in production. |

---

## Part A. Get briefs arriving (about 20 minutes, nothing to wait on)

Do this first and completely. It works on its own. Part B only changes the
address the email comes from.

**1. Make the sheet.** In Mel's Google account, new Google Sheet, name it
**CVBS Briefs**.

**2. Open Apps Script.** Extensions, Apps Script. Rename the project
**CVBS brief store**.

**3. Paste the code.** Replace everything in `Code.gs` with this folder's
`Code.gs`. Then the **+** next to Files, **HTML**, name it exactly `BriefPdf`
(Apps Script adds the `.html` itself), and paste this folder's `BriefPdf.html`
into it. Save.

**4. Check the recipients.** Near the top of `Code.gs`:

```
var TO = ["karen@conferencevenues.com", "aj@conferencevenues.com"];
```

Note those are `conferencevenues.com`, not `.com.au`. The website is on
`.com.au` and the mailboxes are on `.com`. Confirm both addresses with Karen
before the first real submission.

**5. Authorise, and look at the PDF.** In the editor choose the function
`testRender` and Run. Grant the permissions, including the "Google hasn't
verified this app" screen, which is expected for a self-written script. It
writes `CVBS-brief-sample.pdf` to the root of Google Drive. Open it. That is
exactly what Karen will receive. Fix the layout in `BriefPdf.html` now, not
later.

**6. Deploy.** Deploy, New deployment, type **Web app**.
Execute as **Me**. Who has access **Anyone**. Deploy. Copy the `/exec` URL.

**7. Wire the form.** In `submit-a-brief.html`, near the bottom:

```
var BRIEF_ENDPOINT = "";
```

Paste the `/exec` URL between the quotes. Leave `BRIEF_KEY` alone unless the
value in `Code.gs` is changed to match.

**8. Test it live.** Submit a real brief through the page. Expect: a row in the
sheet, a reference like `CVB-260908-004` on the thank you screen, and an email
with the PDF attached. The email reply-to is set to the enquirer, so replying
goes straight to them.

Until the endpoint is pasted in, the form does not pretend. It shows the
fallback message and sends the visitor to the contact page.

---

## Part B. The right from address (needs CVBS)

Without Part B the email arrives from Mel's Google account. That is fine while
this is internal only, but a notification from an unrelated Google address into
a Microsoft 365 tenant is a strong junk-folder candidate, and a brief in junk is
a lost brief. Part B fixes deliverability, not decoration.

**1. Resend account.** Sign up at resend.com. Free covers 3,000 emails a month,
far more than CVBS will send.

**2. Add the domain as a subdomain: `mail.conferencevenues.com`.**

Use the subdomain, never the root. CVBS already has SPF and DKIM on
`conferencevenues.com` pointing at Microsoft. A second SPF record on the root
would break their normal email. A subdomain leaves their mail untouched.

**3. Ask CVBS for these DNS records.** Resend shows the exact values. They look
like this, and they all go on `conferencevenues.com`:

| Type | Name | Value |
|---|---|---|
| MX | `send.mail` | `feedback-smtp.<region>.amazonses.com` priority 10 |
| TXT | `send.mail` | `v=spf1 include:amazonses.com ~all` |
| TXT | `resend._domainkey.mail` | the long DKIM key Resend gives |

Whoever manages `conferencevenues.com` DNS adds them. Verification usually takes
under an hour.

**4. Store the API key.** In Apps Script: Project Settings, Script Properties,
Add script property. Name **exactly** `RESEND_API_KEY`, value the key.

The key lives here and only here. It is never in the website, never in the
repository. The repository is public.

**5. Redeploy.** See the trap below.

The script picks the key up automatically. If Resend ever fails, it falls back
to sending from the Google account rather than dropping the brief, and emails
`hello@theserviceedit.com` to say so.

---

## The redeploy trap

**Saving is not deploying.** Editing `Code.gs` and pressing save changes nothing
about what the live web app runs. After any edit:

Deploy, Manage deployments, the pencil icon, Version **New version**, Deploy.

The `/exec` URL does not change, so `submit-a-brief.html` never needs touching
again. This caught the review tool in September and it will catch this one.

---

## When something goes wrong

**Nothing arrives and the page shows the fallback.** The endpoint is wrong,
missing, or the deployment is not set to "Anyone". Open the `/exec` URL in a
browser: it should return `{"ok":true,"service":"cvbs-brief-store"}`.

**A row appears but no email.** Look at the `sent` column in the sheet. `resend`
means it went via the domain. `mailapp` means the Google fallback. `FAILED`
means check the inbox at `hello@theserviceedit.com` for the reason.

**The email arrives without the PDF.** The renderer choked on something in the
brief. Every field is still in the sheet and the plain text body carries the
essentials. `BriefPdf.html` is rendered by the Apps Script converter, not by a
browser: it understands tables and simple CSS only. No flexbox, no grid, no CSS
variables, no web fonts. Adding a `<div style="display:flex">` will quietly
collapse the layout.

**Testing from a terminal does not work.** The container cannot reach
`script.google.com`. Test from a real browser tab on the live site.
