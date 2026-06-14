# Rapport QA proxy — SEO portes `/shop` · Chantier B · 2026-06-14

| Champ | Valeur |
|-------|--------|
| **Chantier** | **B — `dorevia_ckreyol_marketone`** · **SEO portes shop uniquement** |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079 |
| **Module** | **19.0.19.0.1** (post-merge PR #62 · commit `388e515`) |
| **Doctrine MOA** | [`DECISION_MOA_SEO_PORTES_SHOP.md`](../../cadrage2/DECISION_MOA_SEO_PORTES_SHOP.md) · D1–D6 |
| **Rôle** | QA temporaire · proxy · **ne clôt pas MOA** |
| **Exécuteur** | QA Cursor · 2026-06-14 |

```text
Périmètre autorisé MOA : canonical / noindex · portes /promotions et /kits · modes promo / pack / origin / featured
· cohérence D1–D6 · observations techniques · réserves éventuelles.
Contexte : verdicts intermédiaires 6.3a et 6.3b favorables recette navigateur · lots non clôturés.
```

---

## Synthèse proxy

| Nature | Verdict proxy |
|--------|---------------|
| Tests auto `dorevia_marketone_seo_portes_shop` | ✅ **8/8** |
| D1 alias 301 | ✅ **4/4** |
| D6/T0 `/shop` nu | ✅ |
| D2/T2 portes simples | ✅ **4/4** |
| D3/T3 origine facettée (1 slug) | ✅ **3/3** slugs publiés |
| D3 multi-slugs | ✅ |
| D4/T4 bruit (order · search · origin+order) | ✅ **3/3** |
| D5/T5 pagination | ✅ **2/2** |
| Contenu portes alias `/promotions` · `/kits` | ✅ |
| Slug origine invalide | ✅ 302 → `/shop` nu |

**Recommandation QA → MOA** : base **favorable** pour recette navigateur SEO portes shop · **ne pas clôturer** sur ce rapport seul · enchaîner avec recette navigateur complète 6.3a + 6.3b + SEO.

---

## Tests automatisés

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf -d ckr-marketone-01 \
  --test-enable --stop-after-init --http-port=18086 \
  --test-tags=dorevia_marketone_seo_portes_shop
```

| Métrique | Résultat |
|----------|----------|
| post-tests | **8** |
| failed | **0** |
| error(s) | **0** |
| Date | 2026-06-14 10:18 UTC |

Couverture auto : T0 · T2 · T3 · T4 · multi-origin · alias 301 · non-régression layout accueil.

---

## Grille D1–D6 (proxy HTTP live)

| # | Scénario | Proxy | Preuve / note | MOA |
|---|----------|-------|---------------|-----|
| **D1** | Alias `/promotions` | ✅ | HTTP **301** · `Location: /shop?marketone_mode=promo` | ☐ |
| **D1** | Alias `/kits` | ✅ | HTTP **301** · `Location: /shop?marketone_mode=pack` | ☐ |
| **D1** | Alias `/incontournables` | ✅ | HTTP **301** · `Location: /shop?marketone_mode=featured` | ☐ |
| **D1** | Alias `/origines` | ✅ | HTTP **301** · `Location: /shop?marketone_mode=origin` | ☐ |
| **D6/T0** | `/shop` nu | ✅ | canonical self `http://localhost:18079/shop` · pas de `meta robots` | ☐ |
| **D2/T2** | Porte featured | ✅ | canonical self · pas noindex | ☐ |
| **D2/T2** | Porte promo | ✅ | canonical self · pas noindex | ☐ |
| **D2/T2** | Porte pack | ✅ | canonical self · pas noindex | ☐ |
| **D2/T2** | Porte origin (sans facette) | ✅ | canonical self · pas noindex | ☐ |
| **D3/T3** | Origine `guadeloupe` | ✅ | canonical self normalisé · `marketone_mode=origin&marketone_origin=guadeloupe` · indexable | ☐ |
| **D3/T3** | Origine `martinique` | ✅ | idem slug `martinique` | ☐ |
| **D3/T3** | Origine `reunion` | ✅ | idem slug `reunion` | ☐ |
| **D3** | Multi-slugs GU+MQ | ✅ | `noindex, follow` · canonical porte seule `/shop?marketone_mode=origin` | ☐ |
| **D4/T4** | Promo + `order` | ✅ | `noindex, follow` · canonical `/shop?marketone_mode=promo` · `order` exclu | ☐ |
| **D4/T4** | Pack + `search` | ✅ | `noindex, follow` · canonical `/shop?marketone_mode=pack` · `search` exclu | ☐ |
| **D4/T4** | Origin T3 + `order` | ✅ | `noindex, follow` · canonical T3 sans `order` | ☐ |
| **D5/T5** | Promo `page=2` | ✅ | `noindex, follow` · canonical porte promo sans `page` | ☐ |
| **D5/T5** | Pack `page=2` | ✅ | `noindex, follow` · canonical porte pack sans `page` | ☐ |

### Slugs origine publiés (BO `ckr-marketone-01`)

| Slug | Libellé visiteur |
|------|------------------|
| `guadeloupe` | Guadeloupe |
| `martinique` | Martinique |
| `reunion` | La Réunion |

Les slugs ne sont **pas** exposés dans le HTML sidebar de la porte origin seule ; contrôle T3 effectué via URLs directes et profils BO publiés (3 enregistrements `website_published=True`).

### Slug invalide (hors matrice D1–D6 · rappel cadrage)

| URL | Comportement proxy |
|-----|-------------------|
| `/shop?marketone_mode=origin&marketone_origin=invalid-slug-xyz` | HTTP **302** → `/shop` · final **200** catalogue nu |

---

## Portes alias — contenu après redirect

| Alias | Intro attendue | Proxy |
|-------|------------------|-------|
| `/promotions` (follow) | `.marketone-shop-promo-intro` | ✅ |
| `/kits` (follow) | `.marketone-shop-pack-intro` | ✅ |

Canonical post-redirect : self porte T2 correspondante (`promo` · `pack`).

---

## Cohabitation modes promo / pack (rappel 6.3a · 6.3b)

| Scénario | Proxy | Note |
|----------|-------|------|
| Priorité pack > promo (URL double mode) | ✅ | Intro pack · canonical pack · non régression SEO |
| Chips header Promotions + Kits | ✅ | Liens alias 301 conservés |

Non-régression smoke R1–R4 (catalogue · sidebar · tuiles · panier) : **non rejouée** dans ce lot SEO · couverte rapports 6.3a/6.3b.

---

## Observations techniques

| Sujet | Observation |
|-------|-------------|
| **Canonical HTML** | `href` échappe `&` en `&amp;` — comportement Odoo normal · parsing QA via `html.unescape` |
| **D1 curl sans `-L`** | `urllib`/curl follow redirect masque le 301 — utiliser `curl -I` ou `allow_redirects=False` |
| **Slugs origine dans DOM** | Absents du HTML porte origin seule — ne pas inférer l’absence de profils BO depuis le front seul |
| **Implémentation** | Head tags only · extension `website._get_canonical_url` + `robots` layout (v1 MOA) |
| **Hors périmètre v1** | Sitemap XML custom · refonte UX · collections Lot B |

---

## Réserves / points MOA

| Sujet | Traitement |
|-------|------------|
| Clôture lot SEO | **Non** — recette navigateur MOA requise |
| K6 (6.3b) · P4/P6 (6.3a) | Doctrine inchangée · non rejoués proxy |
| Recette navigateur SEO | Vérifier visuellement head tags (View Source) sur 1280 · contrôler alias depuis chips header |
| Chantier A | **Priorité MOA maintenue** — A1 header · pas d’A7 avant verdict A1 |

---

## Verdict MOA — **clôturé · navigateur 2026-06-14**

| Date | Verdict proxy QA | Verdict MOA navigateur |
|------|------------------|------------------------|
| 2026-06-14 | ✅ **Favorable · D1–D6 proxy OK** | ✅ **GO clôture Chantier B · SEO portes/shop validé** |

```text
Doctrine P4/P6/K6 (MOA 2026-06-14) : acceptés non rejoués — voir rapport clôture.
Arbitrage N2 : OK release 6.3 — chips Promotions + Kits cohabitants.
Rapport clôture : RAPPORT_RECETTE_NAVIGATEUR_CHANTIER_B_20260614.md
```

---

## Gouvernance versionnement

| Décision MOA | Statut |
|--------------|--------|
| Clôture navigateur MOA | ✅ **Actée 2026-06-14** |
| Commit docs dédié | ☐ En attente acte MOA séparé |

**Aucun commit docs** sans acte MOA dédié.

---

## Documents liés

| Document | Rôle |
|----------|------|
| [`DECISION_MOA_SEO_PORTES_SHOP.md`](../../cadrage2/DECISION_MOA_SEO_PORTES_SHOP.md) | Doctrine D1–D6 |
| [`RAPPORT_RECETTE_NAVIGATEUR_CHANTIER_B_20260614.md`](./RAPPORT_RECETTE_NAVIGATEUR_CHANTIER_B_20260614.md) | Clôture navigateur |
| [`CADRAGE_SEO_PORTES_SHOP.md`](../../cadrage2/CADRAGE_SEO_PORTES_SHOP.md) | Matrice URLs T0–T5 |
| [`RAPPORT_QA_PROXY_LOT6_3A_20260614.md`](./RAPPORT_QA_PROXY_LOT6_3A_20260614.md) | Proxy 6.3a |
| [`RAPPORT_QA_PROXY_LOT6_3B_20260614.md`](./RAPPORT_QA_PROXY_LOT6_3B_20260614.md) | Proxy 6.3b · verdict intermédiaire MOA |
| [`tests/test_marketone_seo_portes_shop.py`](../../../tests/test_marketone_seo_portes_shop.py) | Suite auto |

**Hors périmètre** : Chantier A · A1 header · clôture MOA · commit docs sans demande explicite.

---

*Rapport QA proxy SEO portes shop · Chantier B · clôture navigateur MOA 2026-06-14.*
