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
ORDER = ["Core pages", "Current offers", "Service pages", "Destination pages",
         "Venue visits", "Guides and resources", "Legal"]

# Nothing is kept out of sitemap.xml and still shown here any more.
# venue-results.html used to sit in this list. It was deleted from the site
# on 10 Sep with the venue finder, so the review tool must not list it or
# the client clicks a 404 inside the frame.
EXTRA = []


def rel_of(loc):
    rel = loc.split("/cvbs-2026/", 1)[1] if "/cvbs-2026/" in loc else loc
    if rel == "":
        rel = "index.html"
    if rel.endswith("/"):
        rel += "index.html"
    return rel


def group_of(rel):
    if rel.startswith("offer-"):
        return "Current offers"
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

    for extra_rel, extra_group, after_id, extra_title in EXTRA:
        extra_path = os.path.join(ROOT, extra_rel)
        if not os.path.isfile(extra_path):
            print("extra page missing from the source tree: " + extra_rel)
            continue
        if any(p["id"] == extra_rel for p in pages):
            continue
        esrc = open(extra_path, encoding="utf-8", errors="replace").read(20000)
        em = re.search(r"<title>(.*?)</title>", esrc, re.S)
        etitle = html.unescape(re.sub(r"\s+", " ", em.group(1))).strip() if em else extra_rel
        etitle = re.split(r"\s*\|\s*", etitle)[0].strip() or extra_rel
        at = next((i for i, p in enumerate(pages) if p["id"] == after_id), len(pages) - 1)
        pages.insert(at + 1, {"id": extra_rel, "path": "../" + extra_rel,
                              "title": extra_title or etitle, "group": extra_group})

    out = os.path.join(ROOT, "review", "pages.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump({"generated": __import__("datetime").date.today().isoformat(),
                   "pages": pages}, fh, indent=1, ensure_ascii=False)
    print("wrote %d pages to review/pages.json" % len(pages))


if __name__ == "__main__":
    main()
