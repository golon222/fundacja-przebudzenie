# Fundacja „Przebudzenie” – strona www

Statyczna strona (HTML + CSS, bez WordPressa) hostowana na GitHub Pages pod domeną **fundacjaprzebudzenie.com**.

## Pliki

- `index.html` – strona główna
- `polityka-prywatnosci.html` – polityka prywatności (RODO)
- `404.html` – strona błędu
- `assets/` – logo, favicony, styl, czcionka Montserrat (lokalnie, bez Google Fonts)
- `CNAME` – domena dla GitHub Pages
- `tresci.md` – wszystkie teksty fundacji przepisane z wydruków

## Przed publikacją – UZUPEŁNIJ

W `index.html` (sekcja „Dane fundacji”) i w `polityka-prywatnosci.html` (punkt 1) są żółte pola **UZUPEŁNIJ**:

- adres siedziby
- numer KRS
- NIP
- REGON

Wyszukaj w plikach słowo `UZUPEŁNIJ` i podmień, usuwając też `<span class="todo">…</span>`.

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
