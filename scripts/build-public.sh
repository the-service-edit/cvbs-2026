#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST_DIR="${1:-$ROOT_DIR/public-dist}"

if [[ -z "$DEST_DIR" || "$DEST_DIR" == "/" || "$DEST_DIR" == "$ROOT_DIR" ]]; then
  echo "Refusing unsafe public build destination: $DEST_DIR" >&2
  exit 1
fi
if [[ -e "$DEST_DIR" ]]; then
  echo "Public build destination already exists: $DEST_DIR" >&2
  exit 1
fi

mkdir -p "$DEST_DIR"
cp "$ROOT_DIR/.nojekyll" "$ROOT_DIR/robots.txt" "$ROOT_DIR/sitemap.xml" "$ROOT_DIR/favicon.ico" "$DEST_DIR/"
cp -R "$ROOT_DIR/assets" "$DEST_DIR/assets"

# Every URL in the sitemap, not only the ones ending in .html. Six of them are
# directories: the venue visits hub and the five inspection records. The old
# pattern here matched "*.html" only, so it dropped all six from the artifact
# while the sitemap kept pointing at them. That is six 404s and the loss of the
# entire firsthand section, silently, on every build.
SITE_BASE_TRIM="$(sed -nE 's/^SERVE = "(.*)"$/\1/p' "$ROOT_DIR/_entity-source/entity.py")"
COPIED=0
while IFS= read -r loc; do
  rel="${loc#${SITE_BASE_TRIM}/}"
  [[ "$rel" == "$loc" ]] && rel="${loc##*/cvbs-2026/}"
  [[ -z "$rel" ]] && rel="index.html"
  [[ "$rel" == */ ]] && rel="${rel}index.html"
  if [[ ! -f "$ROOT_DIR/$rel" ]]; then
    echo "Sitemap page is missing from the source tree: $rel" >&2
    exit 1
  fi
  mkdir -p "$DEST_DIR/$(dirname "$rel")"
  cp "$ROOT_DIR/$rel" "$DEST_DIR/$rel"
  COPIED=$((COPIED + 1))
done < <(grep -o '<loc>[^<]*</loc>' "$ROOT_DIR/sitemap.xml" | sed -E 's#</?loc>##g')

SITEMAP_COUNT="$(grep -o '<loc>' "$ROOT_DIR/sitemap.xml" | wc -l | tr -d ' ')"
if [[ "$COPIED" != "$SITEMAP_COUNT" ]]; then
  echo "Copied $COPIED pages but the sitemap lists $SITEMAP_COUNT. Every sitemap URL must be in the artifact." >&2
  exit 1
fi
echo "Copied $COPIED pages, matching the sitemap."

# Preserve the three legacy offer URLs without exposing prototypes or internal tools.
for page in \
  offer-hamilton-island.html \
  offer-hyatt-place-essendon-fields.html \
  offer-kimpton-margot-sydney.html
do
  cp "$ROOT_DIR/$page" "$DEST_DIR/$page"
done

# The twelve URLs the old WordPress site published. Each is a folder holding a
# meta-refresh stub, because GitHub Pages has no server redirects. If the
# production host does have them, _redirects and .htaccess carry the same map
# and should be used instead. See REDIRECTS.md.
for legacy in bestvenue groups relocation venuereviews get-a-quote about \
              about/reviews contact-us privacy booking-terms terms feed
do
  if [[ -f "$ROOT_DIR/$legacy/index.html" ]]; then
    mkdir -p "$DEST_DIR/$legacy"
    cp "$ROOT_DIR/$legacy/index.html" "$DEST_DIR/$legacy/index.html"
  fi
done
for cfg in _redirects .htaccess; do
  [[ -f "$ROOT_DIR/$cfg" ]] && cp "$ROOT_DIR/$cfg" "$DEST_DIR/$cfg"
done

# The artifact holds only the pages in sitemap.xml, so the long Disallow list in
# the repository robots.txt names files that do not exist here. Publishing it
# would advertise internal filenames to anyone who reads robots.txt. Generate a
# short one instead, pointed at whatever base the site is actually served from.
SITE_BASE="$(sed -nE 's/^SERVE = "(.*)"$/\1/p' "$ROOT_DIR/_entity-source/entity.py")"
if [[ -z "$SITE_BASE" ]]; then
  echo "Could not read SERVE from _entity-source/entity.py" >&2
  exit 1
fi
cat > "$DEST_DIR/robots.txt" <<ROBOTS
User-agent: *
Allow: /

# venue-results.html is deliberately not disallowed. It carries
# <meta name="robots" content="noindex, follow"> and a crawler has to be able
# to fetch it to read that. Blocking it here would leave the URL indexable by
# reference with no way to see the noindex.

Sitemap: ${SITE_BASE}/sitemap.xml
ROBOTS

if [[ -n "${WEB3FORMS_ACCESS_KEY:-}" ]]; then
  if [[ ! "$WEB3FORMS_ACCESS_KEY" =~ ^[0-9A-Fa-f-]{20,}$ ]]; then
    echo "WEB3FORMS_ACCESS_KEY does not match the expected format." >&2
    exit 1
  fi
  export WEB3FORMS_ACCESS_KEY
  find "$DEST_DIR" -type f -name '*.html' -exec perl -pi -e 's/YOUR_WEB3FORMS_ACCESS_KEY/$ENV{WEB3FORMS_ACCESS_KEY}/g' {} +
fi

if grep -rql 'YOUR_WEB3FORMS_ACCESS_KEY' "$DEST_DIR" 2>/dev/null; then
  echo "The form placeholder key is still in the artifact. Set WEB3FORMS_ACCESS_KEY before building for production." >&2
  echo "(Building without it is fine for a preview, but do not deploy this artifact.)" >&2
fi

if find "$DEST_DIR" -type f \( -path '*/hub/*' -o -path '*/Post-Designer/*' -o -path '*/EDM-Designer/*' -o -path '*/Quote-Generator/*' -o -name '*Strategy*.html' -o -name '*strategy*.html' \) | grep -q .; then
  echo "Internal content leaked into the public artifact." >&2
  exit 1
fi

echo "Public artifact built at $DEST_DIR"
