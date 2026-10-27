#!/usr/bin/env python3
"""Składa strony z src/ do katalogu głównego (GitHub Pages serwuje gotowe pliki HTML).

Użycie:  python3 build.py
Edytuj pliki w src/pages, src/partials i src/layout.html, a potem uruchom skrypt.
"""
import datetime
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
SRC = ROOT / "src"
SITE = "https://fundacjaprzebudzenie.com"

ICONS = {
    "edu": '<path d="M2 8.5l10-5 10 5-10 5z"/><path d="M6 10.6V16c0 1.6 2.7 3 6 3s6-1.4 6-3v-5.4M22 8.5v5"/>',
    "star": '<path d="M12 3.5l2.5 5.3 5.8.7-4.3 4 1.1 5.8L12 16.5l-5.1 2.8 1.1-5.8-4.3-4 5.8-.7z"/>',
    "people": '<circle cx="9" cy="8" r="3.2"/><circle cx="17" cy="9.5" r="2.5"/><path d="M3 19.5c.6-3.2 3-5 6-5s5.4 1.8 6 5M15.5 14.5c2.6-.4 4.9 1.1 5.5 4.3"/>',
    "pulse": '<path d="M3 12h3.5l2.5-6 4 12 2.5-6H21"/>',
    "heart": '<path d="M12 20s-7.5-4.4-7.5-10A4.3 4.3 0 0 1 12 7.4 4.3 4.3 0 0 1 19.5 10c0 5.6-7.5 10-7.5 10z"/>',
    "gift": '<rect x="3.5" y="8.5" width="17" height="11.5" rx="2"/><path d="M12 8.5V20M3.5 12.5h17M12 8.5c-1.5-3-5-3.5-5-1.2 0 1.2 2.5 1.2 5 1.2zm0 0c1.5-3 5-3.5 5-1.2 0 1.2-2.5 1.2-5 1.2z"/>',
    "hand": '<path d="M7 11V6.5a1.5 1.5 0 0 1 3 0V11M10 10V5a1.5 1.5 0 0 1 3 0v5M13 10V6a1.5 1.5 0 0 1 3 0v6"/><path d="M16 9.5a1.5 1.5 0 0 1 3 0V14a7 7 0 0 1-7 7h-.5a6.5 6.5 0 0 1-5.4-2.9L4 14.8a1.6 1.6 0 0 1 2.6-1.8L7 13.5"/>',
    "link": '<path d="M9.5 14.5l5-5"/><path d="M11 6.5l1.7-1.7a4.2 4.2 0 0 1 6 6L17 12.5M13 17.5l-1.7 1.7a4.2 4.2 0 0 1-6-6L7 11.5"/>',
}

ORG_ID = SITE + "/#fundacja"
ORG = {
    "@type": "NGO",
    "@id": ORG_ID,
    "name": "Fundacja Przebudzenie",
    "alternateName": ["Lęborska Fundacja Przebudzenie", "Fundacja „Przebudzenie” Lębork"],
    "legalName": "Lęborska Fundacja Przebudzenie",
    "url": SITE + "/",
    "logo": {"@type": "ImageObject", "url": SITE + "/assets/icon-512.png", "width": 512, "height": 512},
    "image": SITE + "/assets/og-image.jpg",
    "description": "Fundacja wspierająca dzieci i młodzież w odkrywaniu i rozwijaniu ich potencjału: edukacja, rozwój talentów, wychowanie społeczne, sport i zdrowie, wsparcie rodzin w kryzysie oraz pomoc materialna.",
    "slogan": "Budząc potencjał, budzimy przyszłość.",
    "email": "przebudzeniefundacja@gmail.com",
    "taxID": "8411742753",
    "identifier": [
        {"@type": "PropertyValue", "propertyID": "KRS", "value": "0001189157"},
        {"@type": "PropertyValue", "propertyID": "NIP", "value": "8411742753"},
        {"@type": "PropertyValue", "propertyID": "REGON", "value": "542493827"},
    ],
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "ul. Wincentego Witosa 80H/4",
        "postalCode": "84-300",
        "addressLocality": "Lębork",
        "addressRegion": "pomorskie",
        "addressCountry": "PL",
    },
    "areaServed": [{"@type": "City", "name": "Lębork"}, {"@type": "AdministrativeArea", "name": "powiat lęborski"}],
    "knowsAbout": ["pomoc dzieciom", "wsparcie młodzieży", "edukacja", "rozwój talentów", "zajęcia sportowe dla dzieci",
                   "pomoc psychologiczna", "wsparcie rodzin w kryzysie", "wyrównywanie szans edukacyjnych"],
    "member": [
        {"@type": "OrganizationRole", "roleName": "Prezeska Zarządu", "member": {"@type": "Person", "name": "Katarzyna Wilmont"}},
        {"@type": "OrganizationRole", "roleName": "Członkini Zarządu", "member": {"@type": "Person", "name": "Zuzanna Urszula Wilmont"}},
        {"@type": "OrganizationRole", "roleName": "Członkini Zarządu", "member": {"@type": "Person", "name": "Róża Anna Wilmont"}},
    ],
    "contactPoint": {"@type": "ContactPoint", "contactType": "kontakt ogólny", "email": "przebudzeniefundacja@gmail.com", "availableLanguage": "Polish"},
    "sameAs": ["https://www.instagram.com/fundacjaprzebudzenie/"],
}
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#strona", "url": SITE + "/", "name": "Fundacja Przebudzenie",
           "inLanguage": "pl-PL", "publisher": {"@id": ORG_ID}}


def icon(name):
    return ('<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' + ICONS[name] + "</svg>")


def page_hero(args, meta):
    label, title, lead = args.split("|")
    crumb = html.escape(meta.get("crumb", ""))
    return f"""    <section class="page-hero" aria-labelledby="page-title">
      <div class="wrap">
        <nav class="crumbs" aria-label="Okruszki"><ol><li><a href="/">Strona główna</a></li><li aria-current="page">{crumb}</li></ol></nav>
        <h1 id="page-title"><span class="label">{label}</span>{title}</h1>
        <p class="hero-lead">{lead}</p>
      </div>
      <svg class="horizon" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true"><path fill="currentColor" d="M0 90V52C240 18 480 2 720 2s480 16 720 50v38z"/></svg>
    </section>"""


def faq_html(items):
    out = []
    for q, a in items:
        out.append(f"""          <details>
            <summary>{html.escape(q)}</summary>
            <p>{html.escape(a)}</p>
          </details>""")
    return "\n".join(out)


def render(text, meta, partials):
    def sub(m):
        key = m.group(1)
        if key.startswith("icon:"):
            return icon(key[5:])
        if key.startswith("page_hero:"):
            return page_hero(key[10:], meta)
        if key == "faq":
            return faq_html(meta["faq"])
        if key in partials:
            return render(partials[key], meta, partials)
        raise KeyError(f"Nieznany element {{{{{key}}}}} w {meta['path']}")
    return re.sub(r"\{\{([^{}]+)\}\}", sub, text)


def main():
    layout = (SRC / "layout.html").read_text(encoding="utf-8")
    partials = {p.stem: p.read_text(encoding="utf-8").rstrip("\n") for p in (SRC / "partials").glob("*.html")}
    today = datetime.date.today().isoformat()
    sitemap = []

    for src in sorted((SRC / "pages").glob("*.html")):
        raw = src.read_text(encoding="utf-8")
        m = re.match(r"<!--meta\s*(\{.*?\})\s*-->\s*", raw, re.S)
        meta = json.loads(m.group(1))
        body = render(raw[m.end():].rstrip("\n"), meta, partials)

        graph = [ORG, WEBSITE]
        page = {"@type": "WebPage", "@id": meta["url"] + "#strona", "url": meta["url"], "name": meta["title"],
                "description": meta["description"], "inLanguage": "pl-PL", "isPartOf": {"@id": SITE + "/#strona"},
                "about": {"@id": ORG_ID}}
        if meta.get("crumb"):
            page["breadcrumb"] = {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Strona główna", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": meta["crumb"], "item": meta["url"]},
            ]}
        if meta["path"] != "404.html":
            graph.append(page)
        if meta.get("faq"):
            graph.append({"@type": "FAQPage", "@id": meta["url"] + "#pytania", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in meta["faq"]]})
        jsonld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2)

        nav = meta.get("nav", "")
        values = {
            "title": html.escape(meta["title"], quote=True),
            "og_title": html.escape(meta["og_title"], quote=True),
            "description": html.escape(meta["description"], quote=True),
            "url": meta["url"],
            "robots": meta.get("robots", "index, follow, max-image-preview:large"),
            "body_class": meta.get("body_class", ""),
            "jsonld": jsonld,
            "content": body,
        }
        for key in ("o", "dzialania", "pomoc", "wesprzyj", "kontakt"):
            values["nav_" + key] = ' aria-current="page"' if nav == key else ""

        out = re.sub(r"\{\{(\w+)\}\}", lambda mm: values[mm.group(1)], layout)
        (ROOT / meta["path"]).write_text(out, encoding="utf-8")
        if meta.get("robots", "").startswith("noindex"):
            continue
        sitemap.append((meta["url"], today, "1.0" if meta["path"] == "index.html" else "0.8"))
        print("zbudowano", meta["path"])

    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url, mod, prio in sorted(sitemap, key=lambda s: -float(s[2])):
        lines += ["  <url>", f"    <loc>{url}</loc>", f"    <lastmod>{mod}</lastmod>", f"    <priority>{prio}</priority>", "  </url>"]
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("zbudowano sitemap.xml")


if __name__ == "__main__":
    main()
