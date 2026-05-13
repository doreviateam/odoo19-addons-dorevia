# PV de recette manuelle — Trajectoire de trésorerie V1

**Date** : 13 mai 2026  
**Environnement** : `tenant_o8`  
**URL** : `http://localhost:18079`  
**Module** : `dorevia_cash_flow`  
**Version** : `19.0.1.1.0`  
**Run** : `RECETTE CASH FLOW V1 20260513-001`  
**Projection Cash Guard** : id `1407`  
**Plan exécuté** : `docs/RECETTE_MANUELLE_V1.md`

---

## 1. Décision

**GO V1**

La trajectoire de trésorerie V1 est validée : le wizard s'ouvre depuis le menu attendu, la projection hebdomadaire est sélectionnable, le graphique de pilotage affiche une seule trajectoire, les repères de situation et de seuil sont visibles, et la liste des points permet l'audit des valeurs.

---

## 2. Prérequis

| Contrôle | Résultat |
| -------- | -------- |
| Modules `account`, `dorevia_cash_guard`, `dorevia_cash_flow` installés | OK |
| Utilisateur avec droits Cash Guard | OK |
| Projection hebdomadaire avec mailles calculées | OK |
| Date de situation, seuil et solde constaté relevés | OK |

Valeurs relevées :

| Élément | Valeur |
| ------- | ------ |
| Date de situation | `2026-05-13` |
| Seuil d'alerte | `3 000,00 €` |
| Solde constaté | `1 620,67 €` |
| Fin horizon projeté | `2026-08-11` |
| Points générés | `32` (`20` constatés, `12` projetés) |

---

## 3. Tests automatisés

Commande exécutée sur `tenant_o8` :

```text
docker exec sandbox-odoo19-odoo-1 odoo server -c /etc/odoo/odoo.conf -d tenant_o8 -u dorevia_cash_flow --test-enable --test-tags /dorevia_cash_flow --stop-after-init --http-port=18080 --gevent-port=18081 --log-level=test
```

Résultat :

```text
0 failed, 0 error(s) of 4 tests
```

Statut : **OK**

---

## 4. Recette manuelle

| Pas | Contrôle | Résultat | Observation |
| --- | -------- | -------- | ----------- |
| M1 | Menu Comptabilité / Analyse / Trajectoire de trésorerie | OK | Menu observé : `Facturation/Analyse/Trajectoire de trésorerie` |
| M2 | Projection hebdomadaire sélectionnable, date et seuil visibles | OK | `RECETTE CASH FLOW V1 20260513-001` |
| M3 | Bouton `Afficher la trajectoire` ouvre le graphique de pilotage | OK | Action client `dorevia_cash_flow_trajectory_chart` |
| M4 | Une seule ligne de solde, sans courbes concurrentes | OK | Une trajectoire unique, segmentée visuellement |
| M5 | Ligne verticale de situation | OK | Ligne `Situation` visible sur le graphique |
| M6 | Trait plein / pointillé | OK | Constaté plein, projeté pointillé |
| M7 | Ligne horizontale de seuil | OK | Ligne `Seuil d'alerte` visible à `3 000,00 €` |
| M8 | Sous-titre cohérent | OK | Projection, date de situation et seuil affichés |
| M9 | Axe dates chronologique, horizon +90 jours | OK | Dernier point projeté au `2026-08-11` |
| M10 | Axe montants en soldes | OK | Axe en euros, lecture de solde |
| M11 | Point bas et date du point bas | OK | Point bas calculé : `0,00 €` au `2026-01-07` |
| M12 | Liste des points accessible | OK | Liste ouverte : `1-32 / 32` |

---

## 5. Contrôles complémentaires

| Contrôle | Résultat | Observation |
| -------- | -------- | ----------- |
| C1 — Pas de recalcul intempestif | OK | Ouverture en lecture des points générés ; pas de remise à zéro Cash Guard observée |
| C2 — Liste des points vs courbe | OK | Dates triées, segments `Constaté` puis `Projeté`, aucune valeur fantaisiste intercalée |

---

## 6. Cas limites

| Cas | Résultat | Observation |
| --- | -------- | ----------- |
| L1 — Projection non hebdomadaire | OK | Message clair : seules les projections à périodicité `Semaine` sont prises en charge |
| L2 — Projection sans mailles hebdo | OK | Message clair invitant à actualiser le calcul depuis Cash Guard |
| L3 — Horizon projeté | OK | Aucun point projeté au-delà de `situation + 90 jours` |

---

## 7. Preuve visuelle

Capture du graphique de pilotage V1 (fichier attendu dans le dépôt au chemin ci-dessous ; à conserver en versionning avec le PV) :

![Trajectoire de trésorerie V1](captures/recette_cash_flow_trajectory_20260513.png)

La capture montre :

- une trajectoire unique de trésorerie ;
- le segment constaté en trait plein ;
- le segment projeté en pointillé ;
- la ligne verticale `Situation` ;
- la ligne horizontale `Seuil d'alerte` ;
- le sous-titre avec projection, date de situation et seuil.

---

## 8. Conclusion

La recette manuelle V1 décrite dans `RECETTE_MANUELLE_V1.md` est validée.

Décision : **GO V1**
