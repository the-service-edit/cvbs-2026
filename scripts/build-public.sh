#!/usr/bin/env bash
# Retired 11 Sep 2026: scripts/build.py replaced this. Kept so old instructions
# still work. Usage: ./scripts/build-public.sh [OUT_DIR]   (CVBS_ENV=staging for staging)
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
exec python3 "$ROOT_DIR/scripts/build.py" --env "${CVBS_ENV:-production}" --out "${1:-/tmp/cvbs-public}"
