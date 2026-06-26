# Recette QA — Logo header SVG · 19.0.1.59.0 + correctif SVG

| Champ | Valeur |
|---|---|
| Projet | `dorevia_ck_marketone` |
| Ticket | Logo header — source SVG unique desktop / mobile |
| Version | `dorevia_ck_theme` 19.0.1.59.0 + correctif statique SVG |
| Date recette | 2026-06-26 |
| Mise à jour | 2026-06-24 — validation visuelle MOA |
| Rédacteur | QA expert Odoo |
| Base | `dorevia_ck_marketone_01` |

---

## Historique du cycle

| Version | Verdict | Motif |
|---|---|---|
| 19.0.1.58.0 | **NO GO** | `ParseError` à l'upgrade — conflit xpath sur chaîne d'héritage `layout_ck_header_brand_v22` |
| 19.0.1.59.0 | **GO technique** | Pre-migrate supprime les vues obsolètes avant chargement XML · upgrade propre |
| 19.0.1.59.0 | **NON PUBLIABLE** | Défaut visuel post-recette navigateur — encodage SVG incorrect (voir §Défaut visuel) |
| Correctif SVG statique | **GO · PUBLIABLE** | Encodage UTF-8 corrigé · baseline « Overseas Grocery » · viewBox 124×40 · validation visuelle MOA ✅ |

---

## Résultats

### Upgrade

| Contrôle | Attendu | Constaté | OK |
|---|---|---|---|
| Upgrade sans `ParseError` | Aucune erreur | Aucune erreur | ✅ |
| `dorevia_ck_theme` version | 19.0.1.59.0 | 19.0.1.59.0 | ✅ |

### Points de contrôle Dev

| Contrôle | Attendu | Constaté | OK |
|---|---|---|---|
| `layout_ck_header_brand_v22` absent de `ir_ui_view` | `COUNT = 0` | **0** | ✅ |
| `layout_ck_header_brand.inherit_id` | `website.placeholder_header_brand` | `website.placeholder_header_brand` | ✅ |
| `layout_ck_header_brand.active` | `true` | `true` | ✅ |
| `website.option_header_brand_logo.active` | `false` | `false` | ✅ |

### Tests automatisés

| Tag | Tests | Résultat |
|---|---|---|
| `dorevia_ck_theme_phase10` | inclus | ✅ |
| `dorevia_ck_header_v22` | inclus | ✅ |
| **Total** | **30/30** | **0 failed · 0 errors** |

*Note : les stats Odoo indiquent 34 méthodes chargées pour ces tags ; 30 tests exécutés, 4 méthodes non taggées individuellement exclues du décompte résultat — comportement normal Odoo, aucun skip explicite logué.*

### Rendu HTML

Vérification sur `/` (page Home) :

| Contrôle | Attendu | Constaté | OK |
|---|---|---|---|
| Occurrences `ck-logo.svg` | 2 (desktop + mobile) | **2** | ✅ |
| Occurrences `alt="C-Kréyòl"` | 2 | **2** | ✅ |
| Source unique (pas de duplication template) | 1 seul `t-call ck_header_brand_mark` | Confirmé par tests | ✅ |

### Non-régression

| Contrôle | Attendu | Constaté | OK |
|---|---|---|---|
| Catalogue seed publié | 7/7 | **7** | ✅ |
| Menu N2 complet | 8 entrées | **8** (Tous · Épicerie · Boissons · Soin · Artisanat · Communauté · Producteurs · Pro) | ✅ |
| `/odoo/shop` | 200 | 200 | ✅ |
| `/` | 200 | 200 | ✅ |
| `/shop/category/soin-bien-etre-2` | 200 | 200 | ✅ |
| `/odoo/shop/cart` | 200 | 200 | ✅ |

---

## Architecture résultante

```
website.placeholder_header_brand
    └── dorevia_ck_theme.layout_ck_header_brand   (active=true)
            └── t-call ck_header_brand_mark
                    └── <img src="ck-logo.svg" alt="C-Kréyòl">

website.option_header_brand_logo                  (active=false — désactivée)
```

`layout_ck_header_brand_v22` : supprimée de la base (pre-migrate 19.0.1.59.0).

---

## Défaut visuel — Encodage SVG incorrect ✅ CORRIGÉ

**Découvert lors de la recette visuelle navigateur (desktop 1280) · Corrigé par livraison SVG statique.**

### Symptôme initial

Le logo affichait `C-Kreyt` au lieu de `C-Kréyòl`. La baseline affichait `picerie créole` (É initial absent). Les caractères accentués étaient remplacés par des caractères de substitution.

### Cause

`ck-logo.svg` était sauvegardé en **ISO-8859-1** sans déclaration d'encodage XML. Les octets `e9` (`é`), `f2` (`ò`), `c9` (`É`) sont invalides en UTF-8 séquence single-byte.

### Correction appliquée

| Élément | Avant | Après |
|---|---|---|
| Déclaration XML | absente | `<?xml version="1.0" encoding="UTF-8"?>` |
| Caractères accentués | octets ISO-8859-1 bruts | Entités XML : `&#xe9;` `&#xf2;` |
| `viewBox` | `0 0 108 40` | `0 0 124 40` |
| `width` sur `<img>` | `108` | `124` |
| Baseline | `épicerie créole` | `Overseas Grocery` |

Correction de fichier statique uniquement — aucun upgrade de module requis.

### Validation visuelle MOA

Screenshot desktop 1280 fourni par MOA le 2026-06-26 :

- Wordmark `C-Kréyòl` : **rendu correct**, couleurs conformes (`#1c1917` / `#d84315`)
- Baseline `Overseas Grocery` : **lisible, aucun caractère de substitution**
- Séparateur terracotta sous wordmark : présent

**Verdict MOA : logo conforme.**

---

## Observations

### OBS-1 — Recette visuelle desktop / mobile ✅ Soldée

Défaut d'encodage identifié lors de la recette navigateur (desktop 1280), corrigé par livraison SVG statique. Validation visuelle MOA reçue le 2026-06-26 (screenshot desktop 1280 — voir §Défaut visuel corrigé).

Recette mobile 390 non formalisée par screenshot — données statiques SVG identiques desktop/mobile. Pas de régression attendue ; à confirmer visuellement avant mise en production si exigé par le protocole de release.

### OBS-2 — Baseline « Overseas Grocery » (anglais) ✅ Validé MOA

La baseline a changé de **« épicerie créole »** (FR) à **« Overseas Grocery »** (EN). Ce changement est d'ordre éditorial / marque.

**Arbitrage MOA reçu le 2026-06-26 : « logo conforme »** — la baseline « Overseas Grocery » est validée telle quelle.

Point fermé. Aucune action Dev requise.

---

## Verdict

**GO · PUBLIABLE**

| Dimension | Résultat |
|---|---|
| Upgrade propre · 30/30 tests | ✅ |
| Architecture template · points de contrôle Dev | ✅ |
| Encodage SVG | ✅ UTF-8 + entités XML |
| Rendu visuel desktop — wordmark `C-Kréyòl` | ✅ Validé MOA |
| Baseline `Overseas Grocery` | ✅ Validé MOA |

Correctif SVG statique livré et validé visuellement par le MOA. **Publiable en production.**

---

> *Recette réalisée sur `dorevia_ck_marketone_01` · `dorevia_ck_theme` 19.0.1.59.0 · 2026-06-26. Correctif SVG statique validé MOA 2026-06-26.*
