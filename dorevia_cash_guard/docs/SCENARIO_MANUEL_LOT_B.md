# SCENARIO_MANUEL_LOT_B — `dorevia_cash_guard`

Objectif : valider manuellement le Lot B (securite, workflow, UI, prevu/realise simple) avant passage Lot C.

Contexte de recette :

- URL : `http://localhost:18079`
- Base : `tenant_o8` *(lettre **o**, pas `tenant_08` avec un zéro)*
- Module : `dorevia_cash_guard`

---

## 1. Preparation

Verifier que l'instance dispose de :

- au moins un journal de type `bank` ou `cash` ;
- au moins un poste budgetaire `account.budget.post` avec comptes associes ;
- deux utilisateurs de test :
  - un profil **Cash Guard User** ;
  - un profil **Cash Guard Manager**.

Note :

Si la creation d'utilisateurs de test est perturbee par les contraintes custom `res.users/res.partner`, les controles de droits peuvent etre realises par un administrateur en modifiant temporairement les groupes d'un utilisateur existant, ou par test technique cible.

Verifier aussi que le module est a jour :

```text
-u dorevia_cash_guard
```

---

## 2. Controle securite et acces

1. Se connecter avec un utilisateur sans groupe Cash Guard.
2. Verifier que le menu **Projection de trésorerie** n'est pas accessible.
3. Se connecter avec un utilisateur **Cash Guard User**.
4. Verifier acces menu, points et lignes.
5. Se connecter avec **Cash Guard Manager**.
6. Verifier acces identique + droits manager.

Attendu :

- menu visible pour user/manager uniquement ;
- acces conforme aux ACL ;
- pas d'acces hors regles multi-societe.

---

## 3. Workflow d'etats

1. Creer un point en `draft`.
2. Cliquer **Valider**.
3. Verifier etat `validated`.
4. En profil manager, cliquer **Cloturer**.
5. Verifier etat `closed`.
6. En profil manager, cliquer **Reouvrir**.
7. Verifier retour `draft`.

Attendu :

- transitions valides autorisees ;
- transitions invalides bloquees, soit par bouton non visible, soit par erreur metier explicite.

---

## 4. Verrouillage hors brouillon

1. Mettre un point en `validated`.
2. En profil **user non manager** :
   - tenter de modifier `date_from`, `date_to`, `bank_journal_id`, `alert_threshold` ;
   - tenter d'ajouter/modifier/supprimer une ligne.
3. En profil **manager** :
   - verifier que les actions manager restent possibles selon les regles.

Attendu :

- user non manager bloque hors brouillon ;
- manager autorise selon workflow ;
- pas de modification silencieuse.

---

## 5. Verification UI Lot B

Sur formulaire point de tresorerie :

- boutons visibles selon etat/droits :
  - `Valider` en `draft`,
  - `Cloturer` en `validated` (manager),
  - `Reouvrir` hors `draft` (manager) ;
- champs structurants en lecture seule hors brouillon ;
- onglet lignes en lecture seule hors brouillon.

Attendu :

- comportement UI coherent avec regles metier.

---

## 6. Search views et filtres

### Points

Verifier presence et fonctionnement des filtres :

- Brouillon ;
- Valide ;
- Cloture ;
- Risque.

### Lignes

Verifier presence et fonctionnement des filtres :

- Prevu (`planned`) ;
- Simule (`simulated`) ;
- Rapproche (`reconciled`).

Attendu :

- les vues de recherche sont presentes ;
- ils s'appliquent sans erreur ;
- un filtre peut retourner zero resultat si aucune donnee correspondante n'existe.

---

## 7. Prevu / realise simple (variance)

1. Creer une ligne `planned`.
2. Renseigner `projected_amount` puis `realized_amount`.
3. Actualiser.
4. Verifier :
   - `signed_projected_amount` ;
   - `signed_realized_amount` ;
   - `variance_amount`.

Attendu :

- la variance est calculee correctement selon la direction (`inflow` / `outflow`).

Exemples attendus :

- Entree : prevu `1000`, realise `1200` -> variance `+200`
- Sortie : prevu `1000`, realise `1200` -> variance `-200`

---

## 8. Verdict recette Lot B

| Controle | Resultat | Commentaire |
| --- | --- | --- |
| Menu Cash Guard visible pour user/manager | OK / KO | |
| ACL user/manager appliquees | OK / KO | |
| Regles multi-societe respectees | OK / KO | |
| Transition `draft -> validated` | OK / KO | |
| Transition `validated -> closed` (manager) | OK / KO | |
| Transition `closed -> draft` via `Reouvrir` (manager) | OK / KO | |
| Champs structurants bloques hors brouillon (user) | OK / KO | |
| Lignes bloquees hors brouillon (user) | OK / KO | |
| Boutons workflow visibles selon etat/droits | OK / KO | |
| Search view points operationnelle | OK / KO | |
| Search view lignes operationnelle | OK / KO | |
| Prevu / realise simple et variance | OK / KO | |

## Verdict

- [ ] GO Lot B
- [ ] NO GO Lot B

Commentaires :

```text
...
```

---

## 9. Note de couverture tests

`test_cash_guard_workflow.py` est present dans le module mais non active via `tests/__init__.py` dans l'environnement courant.

Raison :

- contraintes custom `res.users/res.partner` qui perturbent la creation neutre d'utilisateurs de test.

Action ulterieure :

- reactiver l'import des tests workflow des que l'environnement de tests permet une creation users/partners sans effets de bord.
