# Note MOA — Clôture CK-HOME-001A — Repositionnement hero Home

| Champ | Valeur |
| --- | --- |
| Date | 2 juillet 2026 |
| Projet | C-Kréyòl Marketone — home |
| Destinataires | MOA, Produit, QA, Dev |
| Statut | **GO recette / GO commit** |
| Module | `dorevia_ck_marketone_content` |
| Version | `19.0.1.75.0` |
| Base recette | `dorevia_ck_marketone_01` |
| URL tunnel | https://assure-violation-markets-factors.trycloudflare.com |
| Commit de référence | `feat(ck-home): CK-HOME-001A repositionner le hero` |

---

## Objet

Repositionner la promesse du hero d'accueil : produits créoles, producteurs et savoir-faire en Europe — sans refonte visuelle (fond, typo, carrousel, structure conservés).

Complément logique de CK-HOME-001C (hygiène visible).

---

## Texte livré

| Élément | Valeur |
| --- | --- |
| Kicker | `Produits créoles · Producteurs · Savoir-faire` |
| Titre | `C-Kréyòl — les saveurs créoles en Europe` |
| Sous-titre | `Une sélection de produits, producteurs et savoir-faire créoles, à découvrir depuis la France et l'Europe.` |
| CTA principal | `Découvrir la boutique` → `/shop` |
| CTA secondaire | `Voir les producteurs` → `/producteurs` |

---

## Recette

### Contrôles tunnel / localhost

| Contrôle | Résultat |
| --- | --- |
| Nouveau titre hero | Présent |
| Ancien titre (`Les saveurs créoles, prêtes à commander.`) | Absent |
| Nouveau kicker | Présent |
| Ancien kicker (`Boutique créole · Livraison…`) | Absent |
| CTA `Découvrir la boutique` | OK |
| CTA `Voir les producteurs` → `/producteurs` | OK |
| `/shop`, `/producteurs` | `200` |
| Tunnel public | `200` |

### Tests automatisés

| Tag | Résultat |
| --- | --- |
| `dorevia_ck_marketone_home_lot1` | 12 post-tests, 0 failed, 0 error |

### CA6 — Mobile 390 px (hero, contrôle distinct du tunnel desktop)

Recette Playwright dédiée sur le tunnel public (`390×844`, `fr-FR`, `Accept-Language: fr-FR`) — **périmètre hero uniquement**, séparée du smoke tunnel desktop § ci-dessus.

| Contrôle | Résultat |
| --- | --- |
| `clientWidth` / `scrollWidth` | `390` / `390` — pas d'overflow horizontal |
| Kicker 001A | `Produits créoles · Producteurs · Savoir-faire` |
| Titre 001A | `C-Kréyòl — les saveurs créoles en Europe` |
| CTA principal | `Découvrir la boutique` → `/shop` |
| CTA secondaire | `Voir les producteurs` → `/producteurs` |
| Empilement mobile | 2 CTA empilés verticalement (`ctaStacked: true`) |
| Grille hero | 1 colonne (`gridTemplateColumns: 366px`) |
| Visuel carrousel | Visible (`visualHeight > 80`) |

**Capture** : [`ck_home_001a_hero_mobile_390.png`](../design/maquette_01.2/captures/ck_home_001a_20260702/ck_home_001a_hero_mobile_390.png)

**Métriques JSON** : [`metrics.json`](../design/maquette_01.2/captures/ck_home_001a_20260702/metrics.json)

> Le drawer header mobile est couvert par CK-DEMO-ONLINE-001 ; ce contrôle CA6 documente explicitement le **rendu hero 001A** en viewport 390 px.

---

## Périmètre livré

| Fichier | Modification |
| --- | --- |
| `home_hero.py` | Constantes kicker/titre/sous-titre/CTA · `href="/producteurs"` |
| `migrations/19.0.1.75.0/post-migrate.py` | `bootstrap_home_hero()` + `cr.commit()` |
| `tests/test_ck_home_lot1_hooks.py` | Assertions mises à jour |
| `tests/test_ck_home_lot1_compose.py` | Assertions mises à jour |
| `__manifest__.py` | `19.0.1.75.0` |

**Hors périmètre** (inchangé) : thème SCSS, snippet `ck_snippet_hero.xml` (fallback thème seul), bloc dual Pro/Newsletter (`/professionnels` conservé).

---

## Verdict

**CK-HOME-001A est clôturé en GO.**

Le hero porte désormais la promesse élargie produits + producteurs + savoir-faire, alignée sur l'annuaire `/producteurs` livré en V1.
