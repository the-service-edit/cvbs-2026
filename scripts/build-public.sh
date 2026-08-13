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

while IFS= read -r page; do
  if [[ ! -f "$ROOT_DIR/$page" ]]; then
    echo "Sitemap page is missing from the source tree: $page" >&2
    exit 1
  fi
  cp "$ROOT_DIR/$page" "$DEST_DIR/$page"
done < <(sed -nE 's#.*<loc>https://[^<]+/([^/<]+\.html)</loc>.*#\1#p' "$ROOT_DIR/sitemap.xml")

# Preserve the three legacy offer URLs without exposing prototypes or internal tools.
for page in \
  offer-hamilton-island.html \
  offer-hyatt-place-essendon-fields.html \
  offer-kimpton-margot-sydney.html
do
  cp "$ROOT_DIR/$page" "$DEST_DIR/$page"
done

if [[ -n "${WEB3FORMS_ACCESS_KEY:-}" ]]; then
  if [[ ! "$WEB3FORMS_ACCESS_KEY" =~ ^[0-9A-Fa-f-]{20,}$ ]]; then
    echo "WEB3FORMS_ACCESS_KEY does not match the expected format." >&2
    exit 1
  fi
  export WEB3FORMS_ACCESS_KEY
  find "$DEST_DIR" -type f -name '*.html' -exec perl -pi -e 's/YOUR_WEB3FORMS_ACCESS_KEY/$ENV{WEB3FORMS_ACCESS_KEY}/g' {} +
fi

if find "$DEST_DIR" -type f \( -path '*/hub/*' -o -path '*/Post-Designer/*' -o -path '*/EDM-Designer/*' -o -path '*/Quote-Generator/*' -o -name '*Strategy*.html' -o -name '*strategy*.html' \) | grep -q .; then
  echo "Internal content leaked into the public artifact." >&2
  exit 1
fi

echo "Public artifact built at $DEST_DIR"
