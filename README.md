# Fundacja „Przebudzenie” – strona www

Statyczna strona (HTML + CSS, bez WordPressa) hostowana na GitHub Pages pod domeną **fundacjaprzebudzenie.com**.

## Pliki

- `index.html` – strona główna
- `polityka-prywatnosci.html` – polityka prywatności (RODO)
- `404.html` – strona błędu
- `assets/` – logo, favicony, styl, czcionka Montserrat (lokalnie, bez Google Fonts)
- `CNAME` – domena dla GitHub Pages
- `tresci.md` – wszystkie teksty fundacji przepisane z wydruków

## Dane fundacji

Lęborska Fundacja Przebudzenie, ul. Wincentego Witosa 80H/4, 84-300 Lębork
KRS 0001189157 · NIP 8411742753 · REGON 542493827

## Włączenie GitHub Pages

1. Repozytorium → **Settings → Pages**.
2. *Source*: **Deploy from a branch**, branch `main` (po zmergowaniu) lub ten branch, folder `/ (root)`.
3. *Custom domain*: `fundacjaprzebudzenie.com` → Save. Gdy DNS zacznie działać, zaznacz **Enforce HTTPS**.

## DNS domeny (u rejestratora, np. LH.pl)

| Typ   | Nazwa | Wartość               |
|-------|-------|-----------------------|
| A     | @     | 185.199.108.153       |
| A     | @     | 185.199.109.153       |
| A     | @     | 185.199.110.153       |
| A     | @     | 185.199.111.153       |
| AAAA  | @     | 2606:50c0:8000::153   |
| AAAA  | @     | 2606:50c0:8001::153   |
| AAAA  | @     | 2606:50c0:8002::153   |
| AAAA  | @     | 2606:50c0:8003::153   |
| CNAME | www   | golon222.github.io    |

Usuń stare rekordy A/CNAME wskazujące na dawny hosting.

## SEO – po uruchomieniu domeny

1. **Google Search Console** (search.google.com/search-console) → Dodaj usługę → *Domena* `fundacjaprzebudzenie.com`.
   Google poda rekord TXT – dodaj go w Cloudflare (DNS → Add record → TXT, Name `@`).
2. W Search Console: **Mapy witryn** → wpisz `sitemap.xml` → Prześlij.
3. **Sprawdzanie adresu URL** → `https://fundacjaprzebudzenie.com/` → *Poproś o zindeksowanie*.
4. **Profil firmy w Google** (business.google.com) – załóż wizytówkę „Fundacja Przebudzenie”, kategoria *Organizacja charytatywna* / *Fundacja*, adres w Lęborku, link do strony.
5. Dodaj link do strony w bio na Instagramie.

Przy zmianie treści zaktualizuj datę `lastmod` w `sitemap.xml`.
