# Note MOA — Clôture CK-HOME-001B — Vedettes + coffret

| Champ | Valeur |
| --- | --- |
| Date | 3 juillet 2026 |
| Projet | C-Kréyòl Marketone — Home |
| Destinataires | MOA, Produit, QA, Dev |
| Statut | **Clôturé — GO recette** |
| Lot | **CK-HOME-001B** (001B-a vedettes + 001B-b coffret) |
| Modules | `dorevia_ck_marketone_content` · `dorevia_ck_theme` (`product_card.scss`) |
| Versions livrées | Livraison **19.0.1.79.0** · sandbox recettée **19.0.1.82.0** / thème **19.0.1.120.0** |
| Base recette | `dorevia_ck_marketone_01` — http://localhost:18079 |
| Ticket | [`TICKET_DEV_HOME_VISUAL_CK_HOME_001B.md`](TICKET_DEV_HOME_VISUAL_CK_HOME_001B.md) |
| État des lieux | [`NOTE_ETAT_DES_LIEUX_CK_HOME_001B_20260703.md`](NOTE_ETAT_DES_LIEUX_CK_HOME_001B_20260703.md) |

**Commits de référence**

| Commit | Rôle |
| --- | --- |
| `43aa89fa` | Livraison 001B — vedettes `<img>`, visuel coffret, migrations `76.0` |
| `4a7fe568` | Hotfix coffrets — markup, `/kits`, CTA sans `stretched-link` (`79.0`) |
| `cc316c05` | Note d'état des lieux post-livraison |
| `ca7d8ff2` | Révision ticket Dev (livré technique) |

---

## Synthèse exécutive

Le lot **CK-HOME-001B** corrige les réserves visuelles P1 héritées de la recette Home Maquette V1 :

- **E1** — images produit visibles sur « Nos coups de cœur » ;
- **E2** — visuel coffret qualifié, sans fallback beige éditorial.

Recette de clôture exécutée le **3 juillet 2026** sur sandbox post-hotfix **`79.0`**, après les livraisons ultérieures **polish Home** (`68a0283b`) et **banner univers** (`a3567caf`). **Aucune régression** détectée sur la Home globale.

**Verdict : GO clôture MOA** — lot exploitable en démo.

---

## Ce que voit le visiteur

| Bloc | Avant (réserve juin) | Après 001B |
| --- | --- | --- |
| **Nos coups de cœur** | Zones image à hauteur `0px` | **4 cartes** avec image produit visible, prix et liens fiche |
| **Coffrets découverte** | Fallback beige `__visual--editorial` | **Photo produit coffret** BO + CTA « Découvrir » vers `/kits` |
| **Ordre Home** | — | Inchangé : Hero → Réassurance → Vedettes → Univers → Coffrets → Dual Pro → Éditorial |

---

## Recette effectuée (post-79.0)

| Zone | Desktop 1280 | Mobile 390 | Commentaire |
| --- | ---: | ---: | --- |
| **1. Vedettes — images visibles** | OK | OK | 4× `ck-product-card__img`, hauteur > 0 (276 px / 356 px) |
| **1. Vedettes — cards propres** | OK | OK | Prix, grille stable, pas de carousel dynamique |
| **2. Coffret — visuel qualifié** | OK | OK | `/web/image/product.template/4583/...` — pas de `--editorial` |
| **3. CTA « Découvrir » → `/kits`** | OK | OK | `href="/kits"` sur `.ck-discovery-pack__cta` · pas de `stretched-link` |
| **3. Redirection `/kits`** | OK | OK | **301** → `/shop?marketone_mode=pack` (navigation Playwright + test HTTP) |
| **4. Mobile — overflow** | n/a | OK | `scrollWidth` = `clientWidth` = **390** |
| **4. Mobile — ordre blocs** | n/a | OK | hero → reassurance → featured → univers → coffret → dual → editorial |
| **5. Non-régression Hero 001A** | OK | OK | Kicker + titre « C-Kréyòl — les saveurs créoles en Europe » |
| **5. Non-régression univers 001C** | OK | OK | Intro « Quatre univers » · 4 cartes |
| **5. Non-régression polish Home** | OK | OK | Dual Pro présent · **pas** de formulaire newsletter sur la Home |
| Routes HTTP | OK | n/a | `/` · `/shop` · `/producteurs` · images produit → **200** |

### Exécution tests automatisés

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --http-port=8079 \
  --test-tags dorevia_ck_marketone_home_lot1,dorevia_ck_marketone_home_lot2,dorevia_ck_marketone_home_lot3 \
  --stop-after-init
```

| Résultat | Détail |
| --- | --- |
| **0 failed / 0 error** | 35 tests (3 juil. 2026) |

### Recette navigateur (Playwright)

Script : [`scripts/ck_home_001b_cloture_recette.mjs`](scripts/ck_home_001b_cloture_recette.mjs)  
Résultats JSON : [`captures/recette_home_001b_cloture_20260703/recette_home_001b_cloture_results.json`](captures/recette_home_001b_cloture_20260703/recette_home_001b_cloture_results.json)

---

## Captures

Dossier : [`captures/recette_home_001b_cloture_20260703/`](captures/recette_home_001b_cloture_20260703/)

| Fichier | Contexte |
| --- | --- |
| [`home_desktop_1280_vedettes.png`](captures/recette_home_001b_cloture_20260703/home_desktop_1280_vedettes.png) | Desktop — section Nos coups de cœur |
| [`home_desktop_1280_coffret.png`](captures/recette_home_001b_cloture_20260703/home_desktop_1280_coffret.png) | Desktop — Coffrets découverte |
| [`home_mobile_390_vedettes.png`](captures/recette_home_001b_cloture_20260703/home_mobile_390_vedettes.png) | Mobile 390 — vedettes |
| [`home_mobile_390_coffret.png`](captures/recette_home_001b_cloture_20260703/home_mobile_390_coffret.png) | Mobile 390 — coffret |
| [`home_mobile_390_full.png`](captures/recette_home_001b_cloture_20260703/home_mobile_390_full.png) | Mobile 390 — page complète |

Captures antérieures (2 juil., pré-hotfix 79) : [`captures/recette_home_20260702/`](captures/recette_home_20260702/) — conservées pour historique.

---

## Hors périmètre (inchangé)

| Sujet | Statut |
| --- | --- |
| **001B-c `/promotions`** | P2 — backlog séparé |
| **Copy éditorial bas de page** | Backlog copy MOA |
| **Bloc producteurs home** | Futur **CK-HOME-002** / **CK-HOME-PRODUCERS-001** |
| **Lot B couleurs banner univers** | **NO GO** |

---

## Contrôles rapides MOA (3 minutes)

Sur `localhost:18079` :

1. **Vedettes** — 4 images visibles · prix · lien fiche produit.
2. **Coffret** — photo coffret (pas de fond beige) · badge « Pack ».
3. **CTA « Découvrir »** — clic → `/kits` → page shop collection pack.
4. **Mobile 390** — pas de scroll horizontal · blocs empilés lisibles.
5. **Hero** — textes 001A inchangés · **pas de newsletter** sur la Home.

---

## Verdict MOA confirmé

```text
CK-HOME-001B Lot A (vedettes + coffret)
→ GO recette clôture (post-79.0, desktop 1280 + mobile 390)
→ Clôturé MOA — exploitable en démo
→ Livraison technique : 43aa89fa + 4a7fe568
→ Documentation : cc316c05 + ca7d8ff2 + présente note
→ 001B-c /promotions et copy éditorial : hors périmètre
```

---

*Note MOA — C-Kréyòl Marketone · Clôture CK-HOME-001B — 3 juillet 2026*
