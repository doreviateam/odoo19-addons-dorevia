# Règles de recommandations simplifiées — MVP2.4 Lot 2

**Référence ticket** : [TICKET_PRODUCT_PAGE_MERCHANDISING_MVP24_LOT2.md](TICKET_PRODUCT_PAGE_MERCHANDISING_MVP24_LOT2.md)  
**Date** : 2026-04-28  
**Statut** : version opérationnelle v1

---

## 1) Objectif

Structurer des recommandations produit lisibles et utiles, sans introduire d’algorithme complexe non natif Odoo.

Le principe :

- prioriser des règles métiers simples ;
- exploiter les données déjà disponibles ;
- masquer le bloc si la donnée fiable manque.

---

## 2) Règles d’éligibilité (ordre recommandé)

Les recommandations se construisent dans cet ordre :

1. **Même famille produit**  
   - privilégier des produits comparables ou proches.

2. **Complémentarité d’usage**  
   - proposer ce qui se consomme ensemble (ex : crackers + tartinable).

3. **Même origine** (si donnée fiable)  
   - cohérence éditoriale et découverte.

4. **Même collection** (si disponible)  
   - continuité d’univers C-Kreyol.

---

## 3) Règles de filtrage minimales

Un produit recommandé doit être :

- actif ;
- publiable ;
- disponible pour le canal web ;
- différent du produit courant.

Exclusion :

- tout produit non publiable ou non pertinent métier.

---

## 4) Règles de quantité et ordre d’affichage

- cible d’affichage : 4 produits (si disponibles) ;
- minimum acceptable : 1 produit ;
- ordre simple : pertinence métier puis cohérence éditoriale ;
- pas de rotation dynamique complexe.

---

## 5) Règle de fallback

Si aucune recommandation fiable :

- masquer proprement le bloc `Vous aimerez aussi` ;
- ne pas afficher de placeholder vide ;
- ne pas injecter de produits aléatoires.

---

## 6) Gouvernance d’alimentation

Rôles :

- **Contenu / merchandising** : relie les produits selon les règles simples.
- **MOA** : valide la pertinence métier et la cohérence marque.
- **Tech** : garantit le rendu propre et le fallback.

Rythme recommandé :

- revue hebdomadaire des fiches sans recommandations ;
- enrichissement progressif par priorité backlog.

---

## 7) Checklist recette recommandations

- [ ] Le bloc s’affiche seulement quand la donnée fiable existe.
- [ ] Les produits proposés respectent au moins une règle métier simple.
- [ ] Aucun produit incohérent (hors famille/hors usage) n’est poussé.
- [ ] Le bloc est masqué proprement si aucune donnée exploitable.
- [ ] Aucun mécanisme de scoring complexe custom n’a été introduit.

---

## 8) Hors périmètre explicite

- moteur de recommandation algorithmique ;
- scoring comportemental ;
- personnalisation en temps réel ;
- règles conditionnelles complexes hors Odoo natif.

---

## 9) Historique

| Date | Changement |
|------|------------|
| 2026-04-28 | Création des règles de recommandations simplifiées Lot 2 MVP2.4 (compatibilité Odoo, fallback propre). |
