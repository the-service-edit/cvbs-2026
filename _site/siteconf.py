# -*- coding: utf-8 -*-
"""Addresses and identity for every generator, read from site.config.json.

    import sys, os
    sys.path.insert(0, os.path.join(ROOT, '_site'))
    from siteconf import BASE, ORG_ID, WEBSITE_ID

BASE is the PRODUCTION origin with a trailing slash. Generators write source
files on it, using the source file path (venue-visits/qt-perth/, about.html).
scripts/build.py turns those into production paths (/venues/qt-perth/,
/about/) through _site/pages.csv, and into staging addresses for a staging
build. Nothing in the source tree ever carries the staging host.

IDENTITY never changes. Every @id hangs off it, in every environment.
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(ROOT, 'site.config.json'), encoding='utf-8') as _fh:
    CFG = json.load(_fh)

IDENTITY = CFG['identity'].rstrip('/')
ORIGIN = CFG['environments']['production']['origin'].rstrip('/')
BASE = ORIGIN + '/'
ORG_ID = IDENTITY + '/#organization'
WEBSITE_ID = IDENTITY + '/#website'
SERVICE_ID = IDENTITY + '/#service'
LOGO_ID = IDENTITY + '/#logo'
LEGACY_HOSTS = [h.rstrip('/') for h in CFG.get('legacyHosts', [])]


def env(name):
    """The settings block for one environment, with origin and basePath tidied."""
    e = dict(CFG['environments'][name])
    e['origin'] = e['origin'].rstrip('/')
    bp = '/' + e.get('basePath', '/').strip('/') + '/'
    e['basePath'] = '/' if bp == '//' else bp
    return e
