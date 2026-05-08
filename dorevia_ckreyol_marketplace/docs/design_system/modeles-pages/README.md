# CK — Modèles de page (inventaire documentaire)

## 1. Objet

Ce dossier documente les **modèles de page CK** : composition de briques UX/UI selon un usage métier, sans déclencher de développement.

Ce travail est **documentaire** :

- pas de création de nouvelles pages ;
- pas de modification QWeb ;
- pas de refonte header/drawer ;
- pas de création de snippets Odoo.

---

## 2. Vocabulaire de référence

- **Pattern-bloc** : décrit une brique UX/UI CK.
- **Modèle de page** : décrit une composition de briques selon un usage (marchand, éditorial, transactionnel, légal).
- **Doctrine responsive** : règle de priorisation entre desktop et mobile.
- **Snippet Odoo** : option technique future, seulement si besoin réel.

---

## 3. Doctrine responsive à appliquer dans chaque modèle

Chaque modèle de page doit expliciter sa logique responsive :

- **Desktop** : équilibre visible commerce / éditorial / promotionnel / communautaire.
- **Mobile** : logique **commerce-first**.

Commerce-first mobile ne signifie pas redirection automatique vers `/shop`.  
Cela signifie une composition qui remonte plus vite les accès marchands :

- boutique ;
- recherche ;
- panier ;
- favoris ;
- promotions ;
- kits/packs ;
- collections ;
- origines ;
- sélection produits ;
- réassurance.

L’éditorial et le communautaire restent présents, mais en soutien du parcours marchand.

---

## 4. Structure attendue dans un modèle de page

Chaque fiche `MODELE_PAGE_*` devrait idéalement contenir :

```md
## Logique responsive

### Desktop
- rôle de la page ;
- équilibre commerce / éditorial / promotionnel / communautaire ;
- composition riche si pertinente.

### Mobile
- rôle commerce-first ;
- blocs marchands prioritaires ;
- éditorial en soutien ;
- communautaire différé ;
- accès rapide aux actions clés.
```

---

## 5. Fichier d’inventaire initial

Voir : [`INVENTAIRE_MODELES_PAGES_CK.md`](./INVENTAIRE_MODELES_PAGES_CK.md)

---

## 6. Ce que ce dossier ne fait pas

Ce dossier ne crée pas automatiquement :

- de nouvelles pages Odoo ;
- de templates QWeb ;
- de snippets Odoo ;
- de tickets d’implémentation ;
- de refonte responsive.

Il sert à cadrer les futures pages CK avant toute décision de développement.

---

## 7. Décision

Les modèles de page CK sont retenus comme niveau de cadrage au-dessus des pattern-blocs.

Ils servent à organiser les futures pages autour de structures cohérentes, en intégrant dès le départ la logique responsive desktop/mobile.

Toute création ou refonte de page devra faire l’objet d’un ticket séparé.

