# QA navigateur S3-B — GO QA AVEC RÉSERVES

| Champ | Valeur |
|---|---|
| SHA | `66973befa34924fd4c0e2c78c5b661ebb5f86bea` |
| Version | `19.0.1.101.0` |
| Date | 2026-07-19 |
| Verdict | **GO QA AVEC RÉSERVES** |

## Checks bloquants

| Check | Résultat |
|---|---|
| Identité (SHA / version / blob JS / clean) | OK |
| Payload `warning` sur `/shop/cart/update` | OK |
| Un toast CK par warning | OK |
| Aucun bandeau `#data_warning` | OK |
| Quantité plafonnée + input mis à jour | OK |
| Message FR conforme | OK |
| Message EN conforme | OK |
| Multi-lignes (gate) | OK |
| Suppression | OK |
| Mobile 390×844 | OK |
| Erreurs console | 0 |

## Preuves clés

- FR : `Vous avez demandé 9, mais seulement 2 est disponible actuellement.`
- EN : `You requested 9, but only 2 is currently available.`
- Multi-lignes : A→2, B→3, pas de confusion / perte / doublon / désync serveur-DOM
- Captures : `captures/desktop_fr_toast.png`, `desktop_en_toast.png`, `desktop_multiline.png`, `mobile_390_*.png`
- JSON : `results/go_qa_avec_reserves_66973be.json`

## Réserves (non bloquantes)

Voir `../backlog/RESERVES.md`.
