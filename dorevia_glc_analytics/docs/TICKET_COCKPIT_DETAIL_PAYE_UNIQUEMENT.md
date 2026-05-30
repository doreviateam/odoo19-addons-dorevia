# Ticket — Filtre « Payé uniquement » · tableau détail cockpit

**Module :** `dorevia_glc_analytics` · version **`19.0.9.0.1`**  
**Statut :** **GO complet MOA** · serveur OK · validation visuelle OK

## Objectif

Deux lectures complémentaires sur le tableau **Détail par axe analytique** :

| Mode | Question métier |
|------|-----------------|
| Décoché (défaut) | Tout ce qui est **engagé / comptabilisé** sur la période |
| **Payé uniquement** | Ce qui est **effectivement encaissé ou réglé** |

## UI

- Case **« Payé uniquement »** à côté de **« Budget ? »** (persistée en `localStorage`).
- Recalcule **Ressource · Cumul RH · Dépense · Solde**, sous-totaux mensuels et total période (même règle sur toutes les lignes — correctif `19.0.9.0.1`).
- **Recharger le cockpit** après mise à jour module pour alimenter les champs `*_paid` en base.
- **Budget** inchangé ; écarts recalculés sur la base des montants payés si les deux cases sont cochées.

## Règle technique « payé »

Implémentée dans `glc_quality_mixin._glc_analytic_line_is_paid_for_cockpit()` :

| Source | Règle |
|--------|--------|
| Factures clients / fournisseurs / avoirs | `payment_state = paid` **uniquement** (pas `partial` ni `in_payment`) |
| Écriture sur compte **512 / 53 / 580** | Payée |
| Écriture contenant une ligne banque | Payée |
| Ligne lettrée avec un compte banque / caisse | Payée |
| Ligne analytique **sans** `move_line_id` | **Exclue** de la vue payée |
| Virement interne **580** qualifié (VIR_INT…) | **Toujours payé** (flux bancaire direct) |

### Cumul RH

- Facture fournisseur paie → incluse si `paid`.
- OD paie sans facture → incluse seulement si lettrée banque ou écriture banque.
- Lignes analytiques paie créées manuellement sans pièce → **hors vue payée**.

## Hors périmètre (v1)

- Colonnes Payé / Non payé par ligne
- Drill-down
- Paiements partiels dans l’interface
- Modification des KPI onglets Ressources / Charges (filtre **limité au tableau détail**)

## Tests auto

- `DET-PAY-01` — facture impayée → `revenue_realized_paid = 0`
- `DET-PAY-02` — facture payée → ressource payée = engagée
- `DET-PAY-03` — virement interne 580 → toujours en vue payée
- **Recette manuelle :** [RECETTE_MANUELLE_COCKPIT_DETAIL_PAYE_UNIQUEMENT.md](recette/RECETTE_MANUELLE_COCKPIT_DETAIL_PAYE_UNIQUEMENT.md) · rejeu serveur `TestGlcCoverageCockpitDetailPaidRecette` (RT-PAY-01 … 10)

## Validation MOA

**Date :** 2026-05-30  
**Verdict :** **GO complet MOA**

| Contrôle | Résultat |
|---|---|
| Rejeu RT-PAY serveur | **2/2 OK** |
| Rejeu DET-PAY serveur | **3/3 OK** |
| Vue complète décochée | **OK visuel MOA** |
| Vue **Payé uniquement** cochée | **OK visuel MOA** |
| Sous-totaux / total période recalculés visuellement | **OK** |
| Ergonomie visuelle | **OK** |

Commentaire MOA :

```text
Pour moi d'un point de vue visuel, ça va.
```
