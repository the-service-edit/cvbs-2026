# How the CVBS site is addressed, built and deployed

Set up 11 September 2026. GitHub Pages is **staging**. `www.conferencevenues.com.au`
is **production**. Everything in this repository is built for production.

## The three files that decide everything

| File | What it holds |
|---|---|
| `site.config.json` | The permanent identity (`https://www.conferencevenues.com.au`), and the origin, base path, indexing and brief endpoint for each environment. The only place a host is written. |
| `_site/pages.csv` | Every public page: its source file, its production path, family, status and legacy URL. `about.html` is served at `/about/`; `venue-visits/qt-perth/` at `/venues/qt-perth/`. |
| `migration/url-map.csv` | Every URL the old WordPress site published, with KEEP, 301, 410 or REVIEW. Generates `_redirects`. |

## Rules

1. **Source always carries production addresses.** Generators read `_site/siteconf.py`
   (`BASE`, `ORG_ID`, `WEBSITE_ID`). Never type a host into a generator or a page.
2. **Source keeps its file layout.** Generators keep writing `about.html` and
   `venue-visits/<slug>/`. The production URL of a page lives in `_site/pages.csv` only.
3. **An `@id` never leaves the identity host**, in any environment. One Organization,
   `https://www.conferencevenues.com.au/#organization`, on every page.
4. **Nothing is switched at cutover.** `scripts/set-base-url.py` is retired. It is the
   script that moved the identity onto GitHub on 6 Sep.
5. **Only the build is deployed.** The repository root is never published.

## Adding a page

1. Build it as today and add it to `sitemap.xml` as today.
2. Add one row to `_site/pages.csv` with its production path. The build **fails** if
   a sitemap page has no row, so every page gets a deliberate URL.
   Families: `/destinations/<slug>/`, `/venues/<slug>/`, `/guides/<slug>/`,
   `/offers/<slug>/`, otherwise `/<slug>/`. Lowercase, hyphens, trailing slash, no dates.
3. Preview pages (noindex, staging only) take `status` = `preview`.
   A closed offer takes `status` = `retired` and `redirect_to` = `/offers/`.

## Building

```
python3 scripts/build.py --env staging    --out /tmp/cvbs-staging
python3 scripts/build.py --env production --out /tmp/cvbs-production
python3 scripts/build.py --env production --out /tmp/cvbs-production --strict   (cutover)
```

The build copies only manifest pages and the assets they use (plus email images,
downloads and icons), rewrites every link to the production layout, and verifies the
artifact. It exits non-zero on any failure. Staging adds `noindex, follow` to every page
and a redirect stub at every old address (`about.html`, `venue-visits/<slug>/`,
`offer-<slug>.html`) because Karen, AJ and sent EDMs hold those links. Production adds
the sitemap index, `_redirects`, `_headers` (CSP is report-only for now) and `404.html`.

CI (`.github/workflows/deploy-public.yml`) builds both on every push to `main`,
publishes staging, and blocks the deploy if either build fails.

## Not published, by design

`review/`, `weekly/`, `hub/`, the three designers, `presentation/`, `brief-store/`,
`email-templates/`, every `_*` folder, every Markdown, CSV, spreadsheet and Python file.
They need a private home (see the Cutover Readiness Plan, decision D5).

## Still to do before cutover

See `Claude outputs/production-migration/CVBS-Cutover-Readiness-Plan.html`, section 12.
