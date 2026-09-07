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
| `apps-script.gs` | the Google Sheet backend, paste-and-deploy |

## Turning on the shared sheet (about five minutes, once)

Until you do this the tool still works, but each person's notes stay in their
own browser and they have to use **Copy for Mel** to send them. Do the setup
and everyone sees the same live list, including you.

1. Go to <https://sheets.new> and name the sheet **CVBS Website Review**.
2. **Extensions → Apps Script**. Delete the sample code.
3. Open `apps-script.gs` from this folder, copy the lot, paste it in, save.
4. **Deploy → New deployment → Type: Web app**.
   - Description: `CVBS review`
   - Execute as: **Me**
   - Who has access: **Anyone**
   - Deploy, then authorise when Google asks. The "unverified app" warning is
     your own script, click **Advanced → Go to project**.
5. Copy the web app URL. It ends in `/exec`.
6. Open `config.js` and paste it in:

   ```js
   endpoint: "https://script.google.com/macros/s/AKfy.../exec",
   ```

7. Commit and push. The top bar should say **Shared and saved** instead of
   **Saved on this computer**.

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

## What the client sees

- **Left**: all 58 pages, grouped, with a dot each. Grey not looked at,
  gold changes wanted, green approved. A badge counts open notes.
- **Middle**: the real page in a frame, at desktop, tablet or phone width.
- **Point at something**: turns on pin mode. Hover highlights whatever is
  under the cursor, click drops a numbered pin, they type the change.
- **Right**: the notes on this page, and every open note across the site.
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
