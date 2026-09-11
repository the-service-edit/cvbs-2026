# -*- coding: utf-8 -*-
"""RETIRED 11 September 2026. Do not bring this back.

This script rewrote every host it knew across the whole source tree. On
6 September it was run with the GitHub address and, because it could not tell
an identity from an address, it moved the permanent CVBS entity (SITE in
_entity-source/entity.py) onto the-service-edit.github.io. Every page then
declared the business twice, on two hosts.

Addresses now live in site.config.json only. Source always carries the
production address. A staging or production site is produced by:

    python3 scripts/build.py --env staging
    python3 scripts/build.py --env production

Nothing is ever switched at cutover. See _site/README.md.
"""
import sys
sys.stderr.write(__doc__)
sys.exit(1)
