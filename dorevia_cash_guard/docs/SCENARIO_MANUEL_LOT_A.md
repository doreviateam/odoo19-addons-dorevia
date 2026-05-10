# SCENARIO_MANUEL_LOT_A — `dorevia_cash_guard`

Objectif : verifier rapidement le Lot A (scaffold, modeles, contraintes, moteur de calcul).

Contexte de recette :

- URL : `http://localhost:18079`
- Base : `tenant_o8` *(lettre **o**, pas `tenant_08` avec un zéro)*
- Module : `dorevia_cash_guard`

---

## 1. Installation

1. Mettre a jour la liste des apps.
2. Installer `dorevia_cash_guard`.
3. Verifier que le menu **Prévision de trésorerie** apparait.

Attendu :

- installation sans erreur ;
- modeles `dorevia.cash.guard` et `dorevia.cash.guard.line` presents.

---

## 1.1 Preparation des donnees de test

Avant de creer les lignes, verifier que l'instance dispose de :

- au moins un journal de type `bank` ou `cash` ;
- au moins un poste budgetaire `account.budget.post` utilisable ;
- si aucun poste budgetaire n'existe, en creer un manuellement avec au moins un compte comptable associe.

Poste recommande pour test :

- Nom : `Test Cash Guard`
- Comptes associes : un compte de charge ou de produit disponible dans le plan comptable.

Important :

Le solde initial est calcule depuis la comptabilite du journal selectionne.
Les montants attendus dans les scenarios doivent donc etre lus relativement au solde initial affiche.

---

## 2. Cas nominal : statut `safe`

1. Creer un point :
   - periode valide ;
   - journal de type banque/caisse ;
   - seuil d'alerte = `1000`.
2. Ajouter deux lignes :
   - ligne 1 : entree `2000`, date J+1 ;
   - ligne 2 : sortie `500`, date J+2.
3. Cliquer **Actualiser**.

Attendu :

- `forecast_min_balance >= alert_threshold` ;
- `risk_status = safe`.

Exemple de lecture (si `initial_balance = 10 000`) :

- entree `2 000` puis sortie `500` ;
- point bas a `10 000`, donc statut `safe` si seuil a `1 000`.

---

## 3. Cas nominal : statut `warning`

1. Reprendre le meme point.
2. Ajuster les lignes pour obtenir un point bas >= 0 et < seuil.
3. Actualiser.

Attendu :

- `forecast_min_balance >= 0` ;
- `forecast_min_balance < alert_threshold` ;
- `risk_status = warning`.

Exemple de lecture (si `initial_balance = 10 000`) :

- sortie `9 500` ;
- point bas a `500`, donc `warning` pour un seuil a `1 000`.

---

## 4. Cas nominal : statut `risk`

1. Ajouter une sortie supplementaire qui fait passer le solde sous 0.
2. Actualiser.

Attendu :

- `forecast_min_balance < 0` ;
- `risk_status = risk`.

Exemple de lecture (si `initial_balance = 10 000`) :

- sortie `11 000` ;
- point bas a `-1 000`, donc `risk`.

---

## 5. Contraintes

Verifier que les creations suivantes sont bloquees :

- `date_from > date_to` ;
- `alert_threshold < 0` ;
- `projected_amount < 0` ;
- `realized_amount < 0` ;
- `sequence < 0` ;
- journal hors types `bank`/`cash`.

---

## 6. Determinisme de calcul

1. Creer plusieurs lignes meme date avec sequences differentes.
2. Actualiser.
3. Verifier l'ordre applique : `projection_date`, `sequence`, `id`.

Attendu :

- `balance_after_line` coherent et stable entre deux recalculs.

---

## 6.1 Simulation

1. Creer une ligne avec `line_type = simulated`.
2. Renseigner une sortie significative.
3. Actualiser.

Attendu :

- la ligne simulee impacte le `forecast_min_balance` ;
- la ligne simulee impacte le `risk_status` en V1.

---

## 7. Cas critique : final positif mais point bas negatif

1. Creer un point avec un solde initial positif.
2. Ajouter une sortie datee J+1 qui fait passer le solde sous zero.
3. Ajouter une entree datee J+2 qui remet le solde final positif.
4. Actualiser.

Attendu :

- `forecast_final_balance > 0` ;
- `forecast_min_balance < 0` ;
- `risk_status = risk`.

Ce cas valide que le module alerte sur le point bas, pas seulement sur le solde final.

---

## 8. Verdict recette Lot A

| Controle | Resultat | Commentaire |
| --- | --- | --- |
| Installation module | OK / KO | |
| Menu visible | OK / KO | |
| Creation point | OK / KO | |
| Journal bank/cash selectionnable | OK / KO | |
| Solde initial calcule | OK / KO | |
| Creation ligne entree | OK / KO | |
| Creation ligne sortie | OK / KO | |
| Poste budgetaire obligatoire | OK / KO | |
| Recalcul operationnel | OK / KO | |
| Ligne simulee prise en compte | OK / KO | |
| Statut safe | OK / KO | |
| Statut warning | OK / KO | |
| Statut risk | OK / KO | |
| Cas point bas negatif / final positif | OK / KO | |
| Contraintes invalides bloquees | OK / KO | |
| Tri deterministe | OK / KO | |

## Verdict

- [ ] GO Lot A
- [ ] NO GO Lot A

Commentaires :

```text
...
```
