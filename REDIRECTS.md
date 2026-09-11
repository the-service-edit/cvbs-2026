> **Superseded 11 September 2026.** The legacy map now lives in `migration/url-map.csv` and `_redirects` is generated from it by `scripts/build.py --env production`. Directory URLs changed the targets (for example `/about/` is now KEPT, `/bestvenue/` now goes to `/conference-venue-finding/`). Do not follow the cutover steps below; see `_site/README.md`.

# The cutover map

`conferencevenues.com.au` currently runs WordPress with Divi. When it points at
this build instead, twelve published URLs stop existing. This is where each one
goes.

| Old URL | New destination | Why |
|---|---|---|
| `/bestvenue` | `/destinations.html` | The destinations hub. The venue search is not part of the launch. |
| `/groups` | `/group-accommodation.html` | Same service, current page |
| `/relocation` | `/corporate-accommodation.html` | The service was renamed |
| `/venuereviews` | `/venue-visits/` | The inspections we publish |
| `/get-a-quote` | `/submit-a-brief.html` | The brief replaced the quote form |
| `/about` | `/about.html` | |
| `/about/reviews` | `/results.html` | Client stories |
| `/contact-us` | `/contact.html` | |
| `/privacy` | `/privacy.html` | New page, written 6 Sep 2026 |
| `/booking-terms` | `/terms.html` | Merged into one terms page |
| `/terms` | `/terms.html` | |
| `/feed` | `/blog-index.html` | The old RSS path. Anyone subscribed loses the feed |

## The map lives in three places, and they must agree

- `_redirects` for Netlify or Cloudflare Pages
- `.htaccess` for Apache
- A folder per old URL holding a meta-refresh stub, for GitHub Pages, which has
  no server redirects

Prefer a real 301 wherever the production host supports one. A meta refresh
passes far less signal and shows the visitor a blank moment. The stubs exist so
that a GitHub Pages cutover does not simply 404, not because they are the right
answer.

## Before the domain moves

1. Run `python3 scripts/set-base-url.py https://conferencevenues.com.au`.
2. Run the generator chain in the order in `_venue-index-source/BUILD.md`.
3. Run `python3 scripts/check-site.py`. It fails on any address left on the old
   host, so this is the proof the cutover is complete.
4. Build the artifact with the real form key:
   `WEB3FORMS_ACCESS_KEY=... ./scripts/build-public.sh /tmp/cvbs-prod`
5. Confirm the artifact page count matches the sitemap. The script now fails if
   it does not, which is how two silent omissions were found on 6 Sep 2026: all
   six venue-visits pages, and `how-to-brief-a-venue-finder.html`.
6. Export whatever is worth keeping from the WordPress site first. Once DNS
   moves, it is gone.

## Not covered

Any old URL not in this table 404s. Pull the real list from Search Console and
from the server logs before cutover rather than trusting this table to be
complete: it was built from what the old site links to, not from what Google
has actually indexed.
