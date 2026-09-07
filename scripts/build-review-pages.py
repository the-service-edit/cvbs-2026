#!/usr/bin/env python3
"""Rebuild review/pages.json from sitemap.xml.

Run from the repository root:  python3 scripts/build-review-pages.py
"""
import html
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CORE = ["index.html", "services.html", "how-it-works.html", "about.html",
        "how-we-are-paid.html", "results.html", "offers.html", "contact.html",
        "submit-a-brief.html", "destinations.html"]
SERVICE = ["conference-venues-with-accommodation.html", "conference-venue-finding.html",
           "group-accommodation.html", "events.html", "corporate-accommodation.html"]
AUDIENCE = ["association-conference-venues.html", "government-conference-venues.html",
            "medical-conference-venues.html", "corporate-retreat-venues.html",
            "sales-conference-venues.html", "executive-meeting-venues.html"]
ORDER = ["Core pages", "Service pages", "Who we work with", "Destination pages",
         "Venue visits", "Guides and resources", "Legal"]


def rel_of(loc):
    rel = loc.split("/cvbs-2026/", 1)[1] if "/cvbs-2026/" in loc else loc
    if rel == "":
        rel = "index.html"
    if rel.endswith("/"):
        rel += "index.html"
    return rel


def group_of(rel):
    if rel.startswith("venue-visits/"):
        return "Venue visits"
    if rel.startswith("venue-finder-"):
        return "Destination pages"
    if rel in ("privacy.html", "terms.html"):
        return "Legal"
    if rel in CORE:
        return "Core pages"
    if rel in SERVICE:
        return "Service pages"
    if rel in AUDIENCE:
        return "Who we work with"
    return "Guides and resources"


def main():
    sitemap = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    locs = re.findall(r"<loc>([^<]+)</loc>", sitemap)
    pages = []
    for loc in locs:
        rel = rel_of(loc)
        path = os.path.join(ROOT, rel)
        title = ""
        if os.path.isfile(path):
            src = open(path, encoding="utf-8", errors="replace").read(20000)
            m = re.search(r"<title>(.*?)</title>", src, re.S)
            if m:
                title = html.unescape(re.sub(r"\s+", " ", m.group(1))).strip()
        else:
            print("missing from the source tree: " + rel)
        title = re.split(r"\s*\|\s*", title)[0].strip() or rel
        pages.append({"id": rel, "path": "../" + rel, "title": title, "group": group_of(rel)})

    pages.sort(key=lambda r: (ORDER.index(r["group"]), [rel_of(l) for l in locs].index(r["id"])))
    out = os.path.join(ROOT, "review", "pages.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"generated": __import__("datetime").date.today().isoformat(),
                   "pages": pages}, fh, indent=1, ensure_ascii=False)
    print("wrote %d pages to review/pages.json" % len(pages))


if __name__ == "__main__":
    main()
