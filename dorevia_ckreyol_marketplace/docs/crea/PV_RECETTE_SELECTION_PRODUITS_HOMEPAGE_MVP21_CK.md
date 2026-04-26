# PV — Recette Sélection produits Homepage MVP2.1

**Ticket** : [TICKET_SELECTION_PRODUITS_HOMEPAGE_MVP21.md](TICKET_SELECTION_PRODUITS_HOMEPAGE_MVP21.md)  
**Décision** : [DECISION_PRODUITS_HOMEPAGE_MVP21.md](../mvp_02/DECISION_PRODUITS_HOMEPAGE_MVP21.md)  
**Date recette (clôture)** : **2026-04-24**  
**Instance** : *(selon déploiement MOA — ex. tenant de recette / sandbox)*  
**Relecteur MOA** : **MOA**  
**Module** : `dorevia_ckreyol_marketplace`  
**Version module au verdict** : **≥ 19.0.1.9.7** (visuels vitrine + migration binaires ; logique sélection 19.0.1.9.2+)

**Verdict (2026-04-24)** : **GO MOA avec réserves mineures** — **contrat MVP2.1 pour le bloc Sélection est rempli** (quatre produits dynamiques `website_sale`, images, prix, CTA fiche, sans panier sur la grille).

**Réserves non bloquantes** (pistes d’itération hors gel MVP2.1) :

- produits / images de **test** encore perfectibles (remplacement par fiches et packshots définitifs) ;
- rendu **desktop** un peu **léger** visuellement (densité, contraste, rythme — charte) ;
- **libellés** des fiches vitrine / catalogue à **affiner** avec les **vrais** produits commerciaux.

**Feu vert chantier suivant** : **4/5 — Inscription / cercle C-Kreyol** — [TICKET_INSCRIPTION_HOMEPAGE_MVP21.md](TICKET_INSCRIPTION_HOMEPAGE_MVP21.md) ; pilotage [README MVP 02](../mvp_02/README.md).

---

## 1. Grille et données

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| **4** emplacements produit en desktop (ou comportement documenté si moins de 4 publiés) | [x] | [ ] | [ ] | **OK** — quatre cartes affichées. |
| Données **dynamiques** Odoo (pas de prix / nom statique de démo) | [x] | [ ] | [ ] | **OK** — prix / noms issus des fiches. |
| Image, nom, prix cohérents avec la **fiche produit** | [x] | [ ] | [ ] | **OK** — liens fiche produit ; visuels présents. |

---

## 2. Parcours et CTA

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Clic **carte** → fiche produit `website_sale` | [x] | [ ] | [ ] | **OK** |
| Clic **Voir le produit** → même fiche | [x] | [ ] | [ ] | **OK** |
| **Pas** d’ajout panier sur la grille | [x] | [ ] | [ ] | **OK** |
| Pas de redirection **forcée** carte → `/shop` seul | [x] | [ ] | [ ] | **OK** |
| Lien de section vers catalogue (si présent) distinct et assumé | [x] | [ ] | [ ] | **OK** — CTA secondaire section « Voir tous les produits ». |

---

## 3. Label secondaire (origine / type / badge)

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Homogénéité sur les 4 cartes **ou** masquage global (§9.4 proposition) | [x] | [ ] | [ ] | **Conforme** à la règle §9.4 (affichage ou masquage global selon couverture). |

---

## 4. Mobile et accessibilité

| Critère | OK | NOK | N/A | Commentaire |
|--------|:--:|:---:|:---:|-------------|
| Grille lisible sans surcharge | [x] | [ ] | [ ] | **OK** — mobile / tablette **acceptables** (réserves mineures desktop, § verdict). |
| Focus clavier / ordre de tabulation | [x] | [ ] | [ ] | **Acceptable** recette. |
| `alt` images pertinents | [x] | [ ] | [ ] | **OK** (nom produit). |

---

## 5. Verdict

- [ ] **Validé** (sans réserve)
- [x] **Validé sous réserve** — réserves : voir en-tête (*produits/images de test, rendu desktop, libellés*).
- [ ] **Refusé** *(motifs)*

**Synthèse** : le périmètre **MVP2.1** (grille 4, `website_sale`, image, prix dynamique, CTA fiche, pas d’ajout panier) est **atteint**. Les réserves ne **bloquent** pas le gel du chantier **Sélection** ni le passage au chantier **Inscription (4/5)**.

**Signature / date** : **MOA — 2026-04-24**
