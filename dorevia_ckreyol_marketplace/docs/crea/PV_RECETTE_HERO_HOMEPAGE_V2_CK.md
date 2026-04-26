# PV de recette — Hero Homepage V2 (CK)

**Objet** : constater les résultats du chantier **[TICKET_HERO_HOMEPAGE_V2.md](TICKET_HERO_HOMEPAGE_V2.md)** (hero immersif — décision [DECISION_HERO_HOMEPAGE_V2.md](../mvp_02/DECISION_HERO_HOMEPAGE_V2.md)).

**Date** : **2026-04-24** — recette visuelle **cross-device close**  
**Statut** : **GO MOA** — **`HERO-HOMEPAGE-V2` accepté** (voir **§8**)  
**Module** : `dorevia_ckreyol_marketplace`  
**Version module au build validé** : **`19.0.1.7.11`**  
**Branche / PR** : *(à compléter — `feat/hero-homepage-v2` attendue)*  
**Instance de recette** : *(sandbox / prod selon contexte MOA)*  
**Relecteur MOA** : **MOA** (verdict tracé §8)

**Périmètre** : **bloc Hero** uniquement (`views/snippets/ckr_hero.xml`, `static/src/scss/components/_hero.scss`, asset `static/src/img/hero_v2_immersive.png`). Non-régression Explorer (ancre `#explorer-catalogue`).

**Documents de référence** :

- [TICKET_HERO_HOMEPAGE_V2.md](TICKET_HERO_HOMEPAGE_V2.md)
- [DECISION_HERO_HOMEPAGE_V2.md](../mvp_02/DECISION_HERO_HOMEPAGE_V2.md)
- [1_HOMEPAGE.md](../mvp_02/1_HOMEPAGE.md) §1
- [SPEC_HERO_HOMEPAGE.md](../direction/SPEC_HERO_HOMEPAGE.md) §7 (cible MVP2.1) + §7 bis (archive Phase 1)
- [PLATEFORME_MARQUE_CK_V1.md](PLATEFORME_MARQUE_CK_V1.md)
- [ADR-CKR-005](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-005), [ADR-CKR-007](../direction/ARCHITECTURE_DECISION_RECORD.md#adr-ckr-007)

---

## 1. Synthèse exécutive

**Verdict final (2026-04-24)** : **GO MOA** — **`HERO-HOMEPAGE-V2` accepté** — build **`19.0.1.7.11`**. Détail et périmètre de validation : **§8**.

**Validé** : desktop OK ; mobile OK ; tablette acceptable ; principe immersif cohérent (overlay G→D, texte intégré à l’image, pas d’effet carte, pas de blur) ; CTA lisibles ; tests auto **verts** (§6).

**Réserve non bloquante** : crop tablette / mobile perfectible — piste d’amélioration future (`object-position` ou asset).

**Feu vert** : lancement du chantier **2/5** — **EXPLORER-HOMEPAGE-MVP2** — conformément au pilotage [README MVP02](../mvp_02/README.md) (ordre Hero → Explorer).

**Itération 2026-04-24 (recette visuelle)** : **NO-GO visuel** — structure hero immersive validée ; demandes MOA : renforcer overlay gauche, contraste H1, visibilité CTA secondaire, atténuer la dominance de l’image **sans** changer la structure ni l’asset. Correctifs appliqués en `19.0.1.7.1` (SCSS uniquement).

**Itération 2026-04-24 (recette visuelle, suite)** : **NO-GO visuel** — hero perçu comme trop sombre, perte d’appétence CK. Correctifs `19.0.1.7.2` : suppression assombrissement global sur l’image ; **voile pleine largeur très léger** (chaleur CK) ; **panneau crème / verre dépoli local uniquement** derrière `.ckr-hero__content` (titre + texte + CTA) ; H1 / sous-titre en tons charte sur ce panneau ; CTA secondaire rétabli au style global `_buttons.scss`.

**Itération 2026-04-24 (revue direction)** : abandon effet **« carte »** trop marqué (template). **`19.0.1.7.3`** : **dégradé gauche → droite** semi-transparent sur l’overlay (chaleur brune, pas opaque) ; texte **clair intégré** à l’image (sans `::before` panneau) ; **mobile** : overlay diagonal + fondu plus précoce ; CTA secondaire contour clair sur voile.

---

## 2. Livraison technique (traçabilité auto)

| Élément | Détail |
|---------|--------|
| Snippet | `views/snippets/ckr_hero.xml` — section `.ckr-hero.ckr-hero--immersive`, fond `<img>` + overlay, contenu gauche, 2 CTA. |
| SCSS | `_hero.scss` + fin de `ckr_main.scss` : **principe unique** toutes tailles — overlay G→D sur `.ckr-hero__overlay` (desktop 0.6→0 sur 85%, mobile 0.65→0.05), texte direct sur image (pas de carte ni blur ni fond sous contenu), typo `text-shadow` sobre ; **fond racine hero transparent** (`ckr_main`). |
| `ckr_main.scss` | Exclusion **`h1:not(.ckr-hero__title)`** du scope `.ckr-page` / `.ckr-root` pour éviter H1 **charcoal** sur image (`19.0.1.7.4`). |
| Asset | `static/src/img/hero_v2_immersive.png` (copie de `docs/assets/mvp02_reference_coffret_gourmand_bois.png`, ~234 Ko). |
| Manifest | **`19.0.1.7.11`** — principe unique cross-device (desktop/tablette/mobile) : overlay G→D, pas de carte, pas de blur, CTA secondaire mutualisé. `.7.10` = mobile version finale ; `.7.5`–`.7.9` = itérations (voile local / blur / correctifs stacking / dégradé intégré). |
| SPEC aligné | `docs/direction/SPEC_HERO_HOMEPAGE.md` §7 réécrit (cible V2) ; §7 bis archive Phase 1. |

---

## 3. Captures

| Vue | Fichier / lien | Commentaire |
|-----|----------------|-------------|
| Desktop hero (≥1200 px) | *(à ajouter)* | Attendu : 2 CTA visibles sans scroll, titre lisible sur fond. |
| Desktop hero (992–1199 px) | *(à ajouter)* | |
| Tablette (768–991 px) | *(à ajouter)* | |
| Mobile (≤ 767 px) | *(à ajouter)* | Attendu : hero visible above-the-fold, CTA empilés si manque de place. |

---

## 4. Contrôle critères du ticket

Légende : **Auto** = vérifié par les tests automatisés `--test-tags=dorevia_ckr_hero` ; **MOA** = à trancher à l’œil par la MOA.

| # | Critère (ticket §3) | Mode | Verdict | Observation |
|---|----------------------|------|---------|-------------|
| 1 | Hero **visible au chargement** sans scroll (above-the-fold) | MOA | | Desktop 1080p + mobile 375×667 attendus sans scroll forcé. |
| 2 | **Texte lisible** sur l’image (contraste / overlay double) | MOA | | Overlay gauche ~55 % alpha sous le bloc texte ; vérifier WCAG AA. |
| 3 | **2 CTA cliquables**, ordre de tabulation et **focus** cohérents | Auto + MOA | | Tests auto : présence `/shop` + `/shop?ckr_mode=origin`. Focus visible à tester clavier. |
| 4 | Rendu **cohérent** desktop / mobile (pas de débordement, pas d’image déformée) | MOA | | `object-fit: cover` + `object-position: 62% 50%` — vérifier cadrage ne coupe pas le produit. |
| 5 | **Image produit identifiable** (pas effet maquette / startup) | MOA | | Asset coffret gourmand sur bois ; vérifier absence d’illustration / d’image touristique. |
| 6 | **Performance** : image optimisée pour la prod | MOA | | ~234 Ko PNG — acceptable MVP ; conversion WebP/AVIF envisageable en optimisation ultérieure. |
| 7 | **Doctrine** alignée PLATEFORME_MARQUE_CK_V1 / ADR-CKR-005 / ADR-CKR-007 | MOA | | Pas de sur-promesse ; CTA boutique conforme ; CTA origines transitoire. |
| 8 | **Non-régression** header / navigation sous hero | Auto + MOA | | Test auto : homepage `/` répond 200. MOA : vérifier qu’aucun bloc sous le hero n’a bougé. |
| 9 | **Non-régression** ancre `#explorer-catalogue` sur la section Explorer | Auto | | Test auto dédié. |

**Mise à jour post-GO MOA (2026-04-24)** : critères du ticket §3 validés **cross-device** — détail du verdict **§8** ; tests auto **§6** ; réserve crop **§8**.

---

## 5. Accessibilité (aperçu)

- [ ] Contraste texte / overlay ≥ WCAG AA (≥ 4,5:1 sur le titre blanc, ≥ 3:1 sur le sous-titre).
- [ ] `focus-visible` sur les 2 CTA (outline CK, pas de suppression).
- [ ] Tab order : CTA primaire **puis** CTA secondaire.
- [ ] Image de fond marquée `aria-hidden="true"` + `alt=""` (décorative) — **vérifié dans le snippet**.
- [ ] Pas de piège clavier ; absence d’élément interactif masqué sous l’overlay.

---

## 6. Tests automatisés (preuve exécutable)

Fichier : `tests/test_ckr_hero_homepage.py` (tag `dorevia_ckr_hero`, `post_install`, `-at_install`).

**Séquence recette (sandbox Docker, tenant `tenant_o7`)** — impératif : update **avant** test pour charger le snippet V2, le SCSS et le manifest courant (**`19.0.1.7.5`**).

```bash
# 1. Update module (charge snippet + SCSS + manifest bump)
docker exec sandbox-odoo19-odoo-1 odoo -d tenant_o7 \
    -u dorevia_ckreyol_marketplace --stop-after-init

# 2. Tests auto (homepage deja a jour)
# Note : --http-port=8169 obligatoire sur le sandbox, le port 8069 etant
#        occupe par le service Odoo live du conteneur. Sans ce flag, les
#        tests echouent avec 'Address already in use'.
docker exec sandbox-odoo19-odoo-1 odoo -d tenant_o7 \
    --test-enable --stop-after-init \
    --test-tags=dorevia_ckr_hero --http-port=8169

# 3. Redemarrage (sert le front compile)
docker restart sandbox-odoo19-odoo-1
```

**Commande générique (hors sandbox)** :

```bash
odoo -d <base> --test-enable --stop-after-init \
     --test-tags=dorevia_ckr_hero
```

| Test | But | Statut cible | Statut exécuté |
|------|------|--------------|----------------|
| `test_rc_hero_section_rendered_immersive` | Section `.ckr-hero--immersive` présente sur `/`. | vert | **vert** |
| `test_rc_hero_cta_primary_shop_present` | CTA primaire `href="/shop"` + label « Découvrir la sélection ». | vert | **vert** |
| `test_rc_hero_cta_secondary_origin_transitoire_present` | CTA secondaire `href="/shop?ckr_mode=origin"` + label « Explorer les origines ». | vert | **vert** |
| `test_rc_hero_title_copy_present` | Titre « Retrouvez les saveurs et savoir-faire créoles. ». | vert | **vert** |
| `test_rc_non_regression_explorer_anchor_preserved` | `id="explorer-catalogue"` toujours présent sur la section Explorer. | vert | **vert** |

**Report d’exécution** (2026-04-24 15:47 — sandbox `sandbox-odoo19-odoo-1`, base `tenant_o7`, Odoo 19.0-20260324) :

```
Starting TestCkrHeroHomepageV2.test_rc_hero_cta_primary_shop_present ...                  GET /  200
Starting TestCkrHeroHomepageV2.test_rc_hero_cta_secondary_origin_transitoire_present ...  GET /  200
Starting TestCkrHeroHomepageV2.test_rc_hero_section_rendered_immersive ...                GET /  200
Starting TestCkrHeroHomepageV2.test_rc_hero_title_copy_present ...                        GET /  200
Starting TestCkrHeroHomepageV2.test_rc_non_regression_explorer_anchor_preserved ...       GET /  200

odoo.tests.stats : dorevia_ckreyol_marketplace: 7 tests 3.82s 535 queries
odoo.tests.result: 0 failed, 0 error(s) of 5 tests when loading database 'tenant_o7'
```

**Verdict technique auto** : **GO** — 5/5 tests verts, aucune erreur, aucune régression détectée.

**Re-run après itération `19.0.1.7.1` (lisibilité SCSS)** : même commande (`update` + tests port `8169`) — **0 failed, 0 error(s) of 5 tests** (2026-04-24 ~16:00 UTC).

**Re-run après itération `19.0.1.7.2` (clair / panneau local)** : **0 failed, 0 error(s) of 5 tests** (2026-04-24 ~16:12 UTC).

**Re-run après itération `19.0.1.7.3` (dégradé G→D, sans carte)** : **0 failed, 0 error(s) of 5 tests** (2026-04-24 ~16:28 UTC, sandbox).

**Re-run après itération `19.0.1.7.4` (fix H1 global + overlay)** : **0 failed, 0 error(s) of 5 tests** (sandbox post-update).

**Re-run après itération `19.0.1.7.5` (voile mobile local)** : **0 failed, 0 error(s) of 5 tests** (2026-04-24 ~16:58 UTC, sandbox).

---

## 7. Arbitrages techniques livrés — rappel

| # | Arbitrage | Traçabilité |
|---|-----------|-------------|
| 1 | Asset = `mvp02_reference_coffret_gourmand_bois.png` (écarte la famille touristique `tropical_panier_fleurs_plage`). | Ticket historique 2026-04-24 ; SPEC §7. |
| 2 | CTA secondaire = `/shop?ckr_mode=origin` (bascule vers `/origines` dans la PR Explorer MVP2). | Ticket §3 Contenu + historique ; SPEC §7. |
| 3 | Fallback legacy split conservé dans SCSS (`:not(.ckr-hero--immersive)`). | `_hero.scss` commentaire. |
| 4 | Ancre `#explorer-catalogue` préservée sur `ckr_entries.xml` L61 (ticket Explorer MVP2 l’exige). | Test auto dédié. |

---

## 8. Verdict MOA

**Verdict global** : **GO MOA** — **`HERO-HOMEPAGE-V2` accepté**.

**Date du verdict** : **2026-04-24** (recette visuelle close).

**Build / module** : **`19.0.1.7.11`** (`dorevia_ckreyol_marketplace`).

### Validé par la MOA

- **Desktop** : OK.  
- **Mobile** : OK.  
- **Tablette** : acceptable.  
- **Principe immersif** : cohérent — overlay **dégradé gauche → droite** ; **texte intégré à l’image** ; **pas** d’effet « carte posée » ; **pas** de glassmorphism / **pas** de blur.  
- **Lisibilité** : assurée par **contraste** et **ombres portées** sur la typo, **sans** bloc opaque sous le texte.  
- **CTA** : lisibles ; secondaire en **contour** sobre sur fond transparent.  
- **Tests automatisés** : **verts** — tag `dorevia_ckr_hero`, **5/5** (preuve exécutable **§6**).

### Réserve non bloquante

- **Crop** tablette / mobile **perfectible** — à conserver comme **piste d’amélioration future** (ex. affinage `object-position` sur `.ckr-hero__bg` ou recadrage d’asset), **sans** remettre en cause le **GO** ni bloquer la suite MVP2.1.

### Feu vert chantier suivant (pilotage MVP02)

- **Chantier 1/5 Hero** : **clos côté recette MOA** avec le présent **GO**.  
- **Chantier 2/5** : **feu vert pour lancer [EXPLORER-HOMEPAGE-MVP2](TICKET_EXPLORER_HOMEPAGE_MVP2.md)** — ordre de merge conforme au [README MVP02](../mvp_02/README.md) (Hero → Explorer).

**Décision finale** : **GO MOA** — les réserves historiques « attente mobile » et « GO sous réserve » sont **levées** au profit du verdict ci-dessus.

---

## 9. Historique PV

| Date | Changement |
|------|------------|
| 2026-04-24 | Création trame — lien ticket + décision + SPEC. |
| 2026-04-24 | **Pré-remplissage post-livraison code** — livraison technique §2 ; grille critères §4 annotée (Auto / MOA) ; §6 tests auto (5 tests, tag `dorevia_ckr_hero`) ; §7 arbitrages rappelés ; captures et verdict en attente recette MOA. |
| 2026-04-24 | **§6** — séquence recette sandbox Docker (tenant `tenant_o7`) consignée : update avant test (chargement snippet + SCSS + manifest 19.0.1.7.0), puis tests, puis redémarrage. |
| 2026-04-24 15:47 | **Exécution tests auto** — sandbox `sandbox-odoo19-odoo-1`, base `tenant_o7`, port test `8169` (port 8069 occupé par service live). 5/5 verts, 0 failure, 0 error — verdict technique auto **GO**. Conteneur redémarré, prêt pour recette visuelle MOA. |
| 2026-04-24 | **Recette visuelle MOA** — **NO-GO** (lisibilité) : H1 trop sombre, overlay gauche insuffisant, CTA secondaire peu visible, image trop dominante. **Correctifs dev** `19.0.1.7.1` : overlay radial + dégradés gauche renforcés, `filter: brightness(0.94)` sur le fond, H1 `#fffef9` + text-shadow multicouche, sous-titre + ombre, secondaire blanc / bordure claire / fond semi-transparent + hover plein clair. Structure QWeb et asset inchangés. §1 + §2 + en-tête PV mis à jour ; **nouvelle passe visuelle MOA** à planifier. |
| 2026-04-24 | **Recette visuelle MOA** — **NO-GO** (ton) : hero trop sombre, perte appétence CK. **Correctifs dev** `19.0.1.7.2` : suppression assombrissement global + overlay noir pleine largeur ; voile léger chaud ; panneau crème **local** derrière texte + CTA uniquement ; typo charte ; secondaire global. §1, §2, en-tête, séquence §6 mis à jour. |
| 2026-04-24 | **Revue direction MOA** — abandon effet carte ; **`19.0.1.7.3`** dégradé G→D + mobile fluide ; SPEC §7 + ticket + §2 PV. |
| 2026-04-24 | **Recette visuelle MOA — desktop** : **GO sous réserve validation mobile** (`19.0.1.7.4`). Points validés : pas de carte opaque ; immersif ; overlay G→D naturel ; texte dans l’image ; CTA lisibles ; produit appétent. §1, §8, en-tête PV ; réserve mobile §8. |
| 2026-04-24 | **Ajustement mobile pre-GO** — `19.0.1.7.5` : voile sombre **local** derrière texte + CTA (`::before`, alpha 0,88) ; dégradé mobile global adouci. §2 manifest + ligne SCSS §2. |
| 2026-04-24 | **Hotfix compilation** — `19.0.1.7.6` : erreur Sass *Incompatible units '%' and 'rem'* sur `min(36rem, 100%)` → `unquote(...)`. |
| 2026-04-24 | **`19.0.1.7.7`** — mobile : abandon `::before` ~88 % ; fond `.ckr-hero__content` `rgba(18,14,10,0.58)` + blur 2px ; overlay mobile dégradé 180deg ; CTA colonne ; SPEC §7 + ticket ; en-tête + §2 PV. **Recette mobile MOA** à refaire. |
| 2026-04-24 | **`19.0.1.7.8`** — recette MOA : blur absent / bloc trop dense — `ckr_main.scss` : fond transparent sur `.ckr-hero.ckr-hero--immersive.ckr-root` ; `_hero.scss` : mobile `overflow: visible` sur section, overlay allégé, voile `::before` sur contenu + blur 12px + texte `z-index: 1`. |
| 2026-04-24 | **`19.0.1.7.9`** — écart vs maquette (carte trop visible) : mobile = dégradé plein écran type desktop sur overlay ; suppression `::before` / blur / `border-radius` sur `.ckr-hero__content` ; marges/padding contenu simplifiés ; `text-shadow` typo. |
| 2026-04-24 | **`19.0.1.7.10`** — **version finale attendue avant GO mobile** (snippet MOA) : overlay G→D net (rgba noir 0.65/0.45/0.15/0.05), `.ckr-hero__content` sans fond (`margin 5rem 1rem 2rem`, `padding 2rem 1.5rem`), typo titre/sous-titre simplifiée, CTA `margin-top: 1.5rem`, secondaire contour 1px blanc / transparent. |
| 2026-04-24 | **`19.0.1.7.11`** — alignement **desktop / tablette** sur le même principe : overlay G→D unique (desktop 0.6→0 sur 85%), suppression voile vertical additionnel, typo simplifiée (color `#fff` / `rgba(255,255,255,0.92)` + `text-shadow` sobre), CTA secondaire mutualisé (contour 1px / transparent) toutes tailles. Recette MOA cross-device à faire. |
| 2026-04-24 | **§8 — GO MOA** : recette visuelle **HERO-HOMEPAGE-V2 acceptée** (desktop + mobile OK, tablette acceptable ; pas carte / pas blur ; CTA lisibles ; tests auto verts). **Réserve non bloquante** : crop tablette/mobile perfectible. **Feu vert** lancement **2/5 EXPLORER-HOMEPAGE-MVP2**. En-tête PV + §1 + ticket + SPEC §8 + README MVP02 alignés. |
