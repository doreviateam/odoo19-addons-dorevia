# SCENARIO_MANUEL_LOT_A — `dorevia_cash_guard`

Objectif : verifier rapidement le Lot A (scaffold, modeles, contraintes, moteur de calcul).

---

## 1. Installation

1. Mettre a jour la liste des apps.
2. Installer `dorevia_cash_guard`.
3. Verifier que le menu **Securite Tresorerie** apparait.

Attendu :

- installation sans erreur ;
- modeles `dorevia.cash.guard` et `dorevia.cash.guard.line` presents.

---

## 2. Cas nominal : statut `safe`

1. Creer un point :
   - periode valide ;
   - journal de type banque/caisse ;
   - seuil d'alerte = `1000`.
2. Ajouter deux lignes :
   - ligne 1 : entree `2000`, date J+1 ;
   - ligne 2 : sortie `500`, date J+2.
3. Cliquer **Recalculer**.

Attendu :

- `forecast_min_balance >= alert_threshold` ;
- `risk_status = safe`.

---

## 3. Cas nominal : statut `warning`

1. Reprendre le meme point.
2. Ajuster les lignes pour obtenir un point bas >= 0 et < seuil.
3. Recalculer.

Attendu :

- `forecast_min_balance >= 0` ;
- `forecast_min_balance < alert_threshold` ;
- `risk_status = warning`.

---

## 4. Cas nominal : statut `risk`

1. Ajouter une sortie supplementaire qui fait passer le solde sous 0.
2. Recalculer.

Attendu :

- `forecast_min_balance < 0` ;
- `risk_status = risk`.

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
2. Recalculer.
3. Verifier l'ordre applique : `projection_date`, `sequence`, `id`.

Attendu :

- `balance_after_line` coherent et stable entre deux recalculs.
