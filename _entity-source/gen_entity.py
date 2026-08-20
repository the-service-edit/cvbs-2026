# -*- coding: utf-8 -*-
"""
Generates the CVBS entity graph from entity.py and injects it into every
page in sitemap.xml. Idempotent: re-running replaces the previous block.

    python3 _entity-source/gen_entity.py

Removes the old standalone Organization / WebSite / Service blocks, because
three unlinked nodes describing the same business is worse than one linked
one. Leaves BreadcrumbList, FAQPage and the venue ItemList alone.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import entity as E

TAG_ID = "cvbs-entity"
OWNED = {"Organization", "WebSite", "Service", "ProfessionalService", "WebPage"}


def clean(d):
    """Drop None, empty list/dict and empty string, recursively."""
    if isinstance(d, dict):
        out = {}
        for k, v in d.items():
            v = clean(v)
            if v is None or v == [] or v == {} or v == "":
                continue
            out[k] = v
        return out
    if isinstance(d, list):
        return [clean(v) for v in d if clean(v) not in (None, [], {}, "")]
    return d


def same_as():
    return [u for u in E.SAME_AS.values() if u]


def identifiers():
    out = []
    if E.ABN:
        out.append({"@type": "PropertyValue", "propertyID": "ABN", "value": E.ABN})
    if E.ACN:
        out.append({"@type": "PropertyValue", "propertyID": "ACN", "value": E.ACN})
    return out


def address():
    if not E.EMIT_ADDRESS or not E.ADDRESS:
        return None
    a = E.ADDRESS
    return {"@type": "PostalAddress", "streetAddress": a["street"],
            "addressLocality": a["locality"], "addressRegion": a["region"],
            "postalCode": a["postcode"], "addressCountry": a["country"]}


def people_nodes():
    out = []
    for p in E.PEOPLE:
        out.append({"@type": "Person", "@id": E.SITE + "/#" + p["name"].lower().replace(" ", "-"),
                    "name": p["name"], "jobTitle": p.get("job"),
                    "email": p.get("email"), "telephone": p.get("tel"),
                    "worksFor": {"@id": E.ORG_ID}})
    return out


def org_node():
    return {
        "@type": ["Organization", "ProfessionalService"],
        "@id": E.ORG_ID,
        "name": E.NAME,
        "alternateName": E.ALT_NAMES,
        "legalName": E.LEGAL_NAME,
        "url": E.SITE + "/",
        "logo": {"@type": "ImageObject", "@id": E.LOGO_ID, "url": E.LOGO["url"],
                 "width": E.LOGO["width"], "height": E.LOGO["height"]},
        "image": {"@id": E.LOGO_ID},
        "description": E.DESCRIPTION,
        "slogan": E.SLOGAN,
        "foundingDate": E.FOUNDING_DATE,
        "identifier": identifiers(),
        "sameAs": same_as(),
        "address": address(),
        "telephone": E.TELEPHONE,
        "email": E.EMAIL,
        "openingHours": E.OPENING_HOURS,
        "priceRange": "Free to the organiser",
        "areaServed": E.AREA_SERVED,
        "knowsAbout": E.KNOWS_ABOUT,
        "employee": [{"@id": E.SITE + "/#" + p["name"].lower().replace(" ", "-")} for p in E.PEOPLE],
        "memberOf": [{"@type": "Organization", "name": m["name"], "url": m.get("url")} for m in E.MEMBER_OF],
        "award": E.AWARDS,
        "aggregateRating": E.AGGREGATE_RATING,
        "review": E.REVIEWS,
        "makesOffer": {"@type": "Offer", "price": E.OFFER["price"],
                       "priceCurrency": E.OFFER["currency"],
                       "description": E.OFFER["description"],
                       "itemOffered": {"@id": E.SERVICE_ID}},
        "contactPoint": [{"@type": "ContactPoint", "contactType": "sales",
                          "telephone": E.TELEPHONE, "email": E.EMAIL,
                          "areaServed": "AU", "availableLanguage": "en-AU"}],
        "hasOfferCatalog": {
            "@type": "OfferCatalog", "name": "Venue sourcing services",
            "itemListElement": [
                {"@type": "Offer", "price": E.OFFER["price"], "priceCurrency": E.OFFER["currency"],
                 "itemOffered": {"@type": "Service", "name": n, "description": d,
                                 "url": E.SITE + "/" + u}}
                for n, u, d in E.SERVICES]},
    }


def service_node():
    return {
        "@type": "Service", "@id": E.SERVICE_ID,
        "name": "Conference venue sourcing",
        "serviceType": "Venue finding and venue sourcing",
        "description": E.DESCRIPTION,
        "provider": {"@id": E.ORG_ID},
        "areaServed": E.AREA_SERVED,
        "audience": {"@type": "BusinessAudience",
                     "audienceType": "Event organisers, executive assistants, "
                                     "associations, government and corporate event teams"},
        "offers": {"@type": "Offer", "price": E.OFFER["price"],
                   "priceCurrency": E.OFFER["currency"],
                   "description": E.OFFER["description"]},
    }


def website_node():
    return {"@type": "WebSite", "@id": E.WEBSITE_ID, "url": E.SITE + "/",
            "name": E.NAME, "alternateName": "CVBS", "inLanguage": "en-AU",
            "publisher": {"@id": E.ORG_ID}}


def page_node(fname, title, desc):
    url = E.SITE + "/" + ("" if fname == "index.html" else fname)
    return {"@type": "WebPage", "@id": url + "#webpage", "url": url,
            "name": title, "description": desc,
            "isPartOf": {"@id": E.WEBSITE_ID},
            "about": {"@id": E.ORG_ID},
            "publisher": {"@id": E.ORG_ID},
            "inLanguage": "en-AU"}


def graph_for(fname, title, desc):
    g = [org_node(), website_node(), service_node(), page_node(fname, title, desc)] + people_nodes()
    return clean({"@context": "https://schema.org", "@graph": g})


LD = re.compile(r'[ \t]*<script type="application/ld\+json"[^>]*>(.*?)</script>\n?', re.S)


def strip_owned(src):
    """Remove our previous block and any legacy Organization/WebSite/Service blocks."""
    def repl(m):
        raw = m.group(1)
        if 'id="%s"' % TAG_ID in m.group(0):
            return ""
        try:
            d = json.loads(raw)
        except Exception:
            return m.group(0)
        if "@graph" in d:
            return ""
        t = d.get("@type")
        t = t if isinstance(t, list) else [t]
        return "" if OWNED & set(t) else m.group(0)
    return LD.sub(repl, src)



# ---------------------------------------------------------------------------
# Second pass: collapse duplicate CVBS stubs in the OTHER schema blocks.
# BlogPosting/FAQPage etc. each carried their own unlinked "Organization"
# node. Three stubs with the same name are three entities to a parser, not
# one. Every one of them now points at the single @id.
# ---------------------------------------------------------------------------
OLD_HOST = "https://the-service-edit.github.io/cvbs-2026/"
CVBS_NAMES = {E.NAME, "CVBS", "Conference Venues & Booking Services"}


def rewire(node):
    if isinstance(node, list):
        return [rewire(n) for n in node]
    if not isinstance(node, dict):
        if isinstance(node, str) and node.startswith(OLD_HOST):
            return E.SITE + "/" + node[len(OLD_HOST):]
        return node
    t = node.get("@type")
    t = t if isinstance(t, list) else [t]
    if ("Organization" in t or "ProfessionalService" in t) and node.get("name") in CVBS_NAMES:
        return {"@id": E.ORG_ID}
    return {k: rewire(v) for k, v in node.items()}


ENTITY_AWARE = {"BlogPosting", "Blog", "FAQPage", "ItemList", "WebApplication", "Article"}


def rewire_others(src):
    def repl(m):
        if 'id="%s"' % TAG_ID in m.group(0):
            return m.group(0)
        try:
            d = json.loads(m.group(1))
        except Exception:
            return m.group(0)
        t = d.get("@type")
        t = t if isinstance(t, list) else [t]
        if not (ENTITY_AWARE & set(t)):
            return m.group(0)
        d = rewire(d)
        d.setdefault("publisher", {"@id": E.ORG_ID})
        if "FAQPage" in t or "ItemList" in t:
            d.setdefault("about", {"@id": E.ORG_ID})
        indent = re.match(r"[ \t]*", m.group(0)).group(0)
        return indent + '<script type="application/ld+json">%s</script>\n' % json.dumps(
            d, ensure_ascii=False, separators=(",", ":"))
    return LD.sub(repl, src)


def main():
    pages = re.findall(r"<loc>(.*?)</loc>", open(os.path.join(ROOT, "sitemap.xml")).read())
    names = [p.rsplit("/", 1)[-1] or "index.html" for p in pages]
    done, skipped = 0, []
    for n in names:
        path = os.path.join(ROOT, n)
        if not os.path.exists(path):
            skipped.append(n); continue
        src = open(path, encoding="utf-8").read()
        title = re.search(r"<title>(.*?)</title>", src, re.S)
        desc = re.search(r'<meta name="description" content="(.*?)"', src, re.S)
        title = title.group(1).strip() if title else E.NAME
        desc = desc.group(1).strip() if desc else E.DESCRIPTION
        src = strip_owned(src)
        src = rewire_others(src)
        block = ('<script type="application/ld+json" id="%s">%s</script>\n'
                 % (TAG_ID, json.dumps(graph_for(n, title, desc), ensure_ascii=False,
                                       separators=(",", ":"))))
        src = src.replace("</head>", block + "</head>", 1)
        open(path, "w", encoding="utf-8").write(src)
        done += 1
    print("entity graph written to %d pages" % done)
    if skipped:
        print("missing, skipped:", ", ".join(skipped))
    missing = [k for k, v in E.SAME_AS.items() if not v]
    print("\nSTILL UNSUPPLIED (each one weakens the recommendation):")
    print("  sameAs:", ", ".join(missing) if missing else "none, complete")
    for label, val in [("ABN", E.ABN), ("legal name", E.LEGAL_NAME),
                       ("memberships", E.MEMBER_OF), ("reviews", E.REVIEWS)]:
        if not val:
            print("  %s: not supplied" % label)


if __name__ == "__main__":
    main()
