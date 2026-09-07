# CVBS Website Review

A review shell for the whole cvbs-2026 site. Karen and Anthony open one link,
walk the 58 live pages one at a time, click anything they want changed, and
type what they want instead. Every note is pinned to the exact element, signed
with their name, and lands in one place.

Live at: `https://the-service-edit.github.io/cvbs-2026/review/`

It is `noindex, nofollow`, and `scripts/build-public.sh` only copies pages
listed in `sitemap.xml`, so this folder never reaches the production domain.

---

## Files

| File | What it is |
|---|---|
| `index.html` | the shell |
| `review.css` | styling, CVBS brand tokens |
| `review.js` | all the logic: pinning, notes, sync, export |
| `config.js` | **the only file you edit.** Endpoint, key, reviewer names |
| `pages.json` | the 58 pages, generated from `sitemap.xml` |
| `asks.json` | the starter list of things we need from CVBS, one per page |
| `apps-script.gs` | the Google Sheet backend, paste-and-deploy |

## The shared sheet is already on

Set up 7 Sep 2026. Nothing to do here unless something breaks.

- **Sheet:** CVBS Website Review, in hello@theserviceedit.com's Drive.
  https://docs.google.com/spreadsheets/d/1-7NTF0ey1EFwmB9Rq151Viw_VTIZeAh8_iQNWWy6TIM/edit
- **Script:** CVBS review store, bound to that sheet. Extensions, Apps Script.
- **Deployment:** web app, Version 1, executing as hello@theserviceedit.com,
  access set to Anyone. The URL is already in `config.js`.

Verified end to end from the live site's own origin: a note posts, reads back,
and a wrong key is refused.

**If you ever edit `apps-script.gs`,** paste it into the script and then
**Deploy, Manage deployments, edit the pencil, Version: New version, Deploy.**
A plain save does not change what the web app serves.

**If the tool starts saying "Offline, will retry",** open the sheet, check the
script still exists, and confirm the deployment is still on Version 1 with
access set to Anyone.

The sheet fills a row per note. You can read it, sort it, and tick things off
there if you prefer that to the tool.

If you ever change `key` in `config.js`, change `SHARED_KEY` in the Apps Script
to match and redeploy.

## Regenerating the page list

If pages are added to or removed from `sitemap.xml`, rebuild `pages.json`:

```bash
python3 scripts/build-review-pages.py
```

Existing notes stay attached to their pages, because they key off the file
path, not the position in the list.

## The requests, "What we need from you"

Each page can carry requests: the pieces only CVBS holds. They show at the top
of the notes panel on the page they belong to, and every one of them is listed
together under the **To do** tab and in **All feedback**. Karen or Anthony types
the answer in the box and hits **Mark supplied**, or **Save for now** if they
are part way through. The count in the top bar is how many are still open.

`asks.json` seeds ten of them, taken from the two supply documents written
on 19 August: `CVBS-What-Karen-Must-Supply.html` and
`CVBS-Being-Chosen-Supply-List.html`. Some may already be closed, so delete the
stale ones the first time you open the tool.

**Seeding happens once.** Each request is written into the shared store under a
fixed id, then it lives there like any other record. Editing `asks.json` after
that does nothing, and deleting a request in the tool sticks. Add new ones from
inside the tool instead: sign in as a name listed in `team` in `config.js` and
use **+ Add a request for this page**.

An open request does not stop a page being approved. They are two separate
questions: is the page right, and what are we still waiting on. The rail shows
both, a gold badge for open notes and a teal one for open requests.

## What the client sees

- **Left**: all 58 pages, grouped, with a dot each. Grey not looked at,
  gold changes wanted, green approved. A badge counts open notes.
- **Middle**: the real page in a frame, at desktop, tablet or phone width.
- **Point at something**: turns on pin mode. Hover highlights whatever is
  under the cursor, click drops a numbered pin, they type the change.
- **Add a note**: for anything about the page as a whole, with nothing to point
  at. Those show a square marker in the list and no pin on the page.
- **Right**: the requests for this page, the notes on it, everything still
  needed across the site under **To do**, and every open note under
  **Everything**.
- **Approve page** moves them to the next unreviewed page automatically.
- **All feedback**: the running total, plus **Copy for Mel** and a CSV.

Keyboard: `c` toggles pin mode, `]` jumps to the next unreviewed page,
`Esc` gets out of anything.

## Notes on how it works

- Notes are anchored by CSS selector plus a percentage offset inside the
  element, so a pin stays on its headline when the page reflows to mobile.
  If the element is ever deleted, the pin falls back to its original
  coordinates rather than disappearing.
- Everything is written to `localStorage` first and then pushed to the sheet,
  so a dropped connection never costs a note. The status light in the top bar
  says which state it is in.
- The sheet is polled every 25 seconds, so two people reviewing at the same
  time see each other's notes.
- The shared key in the URL is a soft gate, not security. Anyone with the
  review link and the key can read the notes. Do not put anything in there
  you would not put in an email.
