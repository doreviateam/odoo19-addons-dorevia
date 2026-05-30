# Release note — Livraison MOA `19.0.15.0.0`

**Date :** 2026-05-30  
**Module :** `dorevia_glc_analytics`  
**Statut :** **Gel livraison MOA**

---

## Synthèse

Version de **clôture** du lot Contrôle de gestion GLC : réalisé analytique seul, UX cockpit finalisée MOA, **106 tests automatisés verts**.

Le module est **terminé** pour acceptation MOA. Les lots budget, bénévolat et exports sont **hors périmètre** (cf. [LIVRAISON_MOA.md](./LIVRAISON_MOA.md)).

---

## Périmètre produit livré

- Plan analytique GLC — 11 axes
- **Contrôle de gestion** — Tableau de bord + détail + trésorerie + qualité + paiements
- **Audit** analytique A1–A2, A4–A6
- **Axes analytiques** — paramétrage

---

## Nouveautés UX (`19.0.14.5.x` → `19.0.15.0.0`)

| Sujet | Livraison |
|---|---|
| Période par défaut | 3 derniers mois calendaires, fin = aujourd’hui |
| Sélecteur période | Icône calendrier, dates compactes, recalcul auto |
| Onglet 1 | Renommé **Tableau de bord** |
| Onglets masqués | Ressources, Infos |
| Textes intro | Retirés (Tableau de bord, Détail) |
| Couverture Cumul RH | Couleur = bandeau alerte ; **> 100 %** si taux > 100 % |
| KPI lettrage | **Lettrage clients** / **Lettrage fournisseurs** |
| Détail | Bloc filtres masqué ; tri mois **choix utilisateur** |
| Détail | Option **Payé uniquement** (localStorage) |

---

## Historique versions majeures

| Version | Contenu |
|---|---|
| `19.0.13.0.0` | Cockpit réalisé seul — retrait budget UI et Palier 2 |
| `19.0.14.0.0` | Suppression module `dorevia_glc_budget` |
| `19.0.14.0.2` | Menus MOA — Contrôle de gestion · Audit |
| `19.0.14.1.0` | Alignement documentation |
| `19.0.14.5.x` | Finitions UX cockpit |
| **`19.0.15.0.0`** | **Gel livraison MOA** |

---

## Tests

```text
106 post-tests · 0 failed · 0 error
Base : glc-rgl-test-import
Tag  : /dorevia_glc_analytics
```

---

## Migration

1. Déployer le code ≥ `19.0.15.0.0`
2. `-u dorevia_glc_analytics`
3. Redémarrer Odoo + Ctrl+Shift+R
4. Vérifier **Pilotage GLC** (3 menus)
5. Désinstaller `dorevia_glc_budget` si encore présent (legacy)

---

## Documents

- [LIVRAISON_MOA.md](./LIVRAISON_MOA.md) — checklist acceptation
- [ETAT_MODULE_ACTUEL.md](./ETAT_MODULE_ACTUEL.md) — état technique
