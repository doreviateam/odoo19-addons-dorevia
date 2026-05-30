# Release note — Simplification pilotage GLC (`19.0.13.0.0` → `19.0.14.1.0`)

**Date :** 2026-05-30  
**Module :** `dorevia_glc_analytics` uniquement  
**Décision MOA :** pilotage sur **réalisé comptable analytique** ; retrait des overlays budget, ventilations RH et saisie prévisionnelle.

---

## Synthèse

| Avant | Après |
|---|---|
| Cockpit réalisé + budget + contrôle ventilations RH | **Contrôle de gestion** — réalisé seul |
| Menus Coûts salariés · Ventilations · *(retiré — budgets)* | **Supprimés** |
| Module `dorevia_glc_budget` | **Supprimé du dépôt** |
| Libellés « Cockpit couverture… » · « Anomalies analytiques » | **Contrôle de gestion** · **Audit** |
| Pilotage GLC en fin de barre Facturation | Entre **Fournisseurs** et **Comptabilité** |

---

## Versions

| Version | Contenu |
|---|---|
| `19.0.12.0.5` | Dernière version avec budget cockpit (non mergée longtemps) |
| `19.0.13.0.0` | PR #50 — retrait budget UI, Palier 2, financements A3 |
| `19.0.14.0.0` | PR #51 — retrait `dorevia_glc_budget` |
| `19.0.14.0.1` | Position menu Pilotage GLC (barre Facturation) |
| `19.0.14.1.0` | PR #52 — renommage menus · ordre sous-menus |

---

## Migration bases existantes

1. **Désinstaller** `dorevia_glc_budget` si encore installé (Apps).
2. Déployer le code `main` ≥ `19.0.14.1.0`.
3. `-u dorevia_glc_analytics`.
4. Vérifier menus **Pilotage GLC** (3 entrées seulement).
5. Données Palier 2 / budget : tables orphelines possibles en base — sans impact sur le module actif.

---

## Tests

Module seul : `/dorevia_glc_analytics` — recette sandbox post-merge (61/62 verts ; échec préexistant nomenclature 11 axes).

Plus de tests `/dorevia_glc_analytics`.
