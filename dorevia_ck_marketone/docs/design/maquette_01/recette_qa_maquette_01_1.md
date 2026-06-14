# Recette QA — Maquette CK V1.1.1 (adaptation Pro MOA)

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` |
| **Livraison** | Maquette V1.1.1 — adaptation Pro MOA |
| **Ticket source** | [`ticket_maquette_adaptation_pro_moa_01.md`](./ticket_maquette_adaptation_pro_moa_01.md) |
| **Référence MOA** | [`note_transmission_arbitrage_david_01_v1_1.md`](./note_transmission_arbitrage_david_01_v1_1.md) |
| **Suite de** | [`recette_qa_maquette_01.md`](./recette_qa_maquette_01.md) (V1.1 validée) |
| **Artefact** | `/Users/doreviateam/open-design/.od/projects/ck-marketone-maquette-v1/index.html` |
| **URL test** | `http://127.0.0.1:8765/index.html` |
| **Date** | 2026-06-12 |
| **Statut QA** | **Validé V1.1.1** |

---

## 1. Objet du contrôle

Vérifier que la micro-évolution textuelle Pro est conforme aux décisions MOA §10, **sans régression** sur V1.1.

```text
Cette validation QA est prérequis à une éventuelle levée du verrou Odoo.
Validation QA V1.1.1 ≠ GO Dev automatique.
```

---

## 2. Périmètre

### Contrôlé

- Section `#pro` (Espace professionnel)
- Hero CTA Pro
- Bandeau `/shop` (`#pro-banner`)
- Note prix B2C intro boutique
- Navigation vers `#pro`
- Non-régression V1.1 : bouton `Voir`, burger, drawer filtres, responsive, catégories, savon vétiver

### Hors périmètre inchangé

```text
Aucun Odoo · aucun module · aucun QWeb/SCSS
Pas de portail B2B · pas de prix B2B publics
```

---

## 3. Méthode

Contrôles réalisés :

- relecture de [`LIVRAISON_V1_1_1.md`](./LIVRAISON_V1_1_1.md) ;
- relecture du ticket d’adaptation ;
- inspection HTML de l’artefact ;
- test navigateur sur `http://127.0.0.1:8765/index.html` ;
- test mobile viewport `390x844`.

Résultats navigateur notables :

```text
Section #pro présente.
Menu mobile → lien Professionnels vers #pro.
Drawer filtres mobile fonctionnel.
Section Pro responsive en 1 colonne mobile.
Boutons cartes = Voir ; aucun quick-add restant.
```

---

## 4. Checklist — double cible Pro

| # | Critère | Statut | Note |
|---|---------|--------|------|
| 1 | Deux blocs distincts : producteur/transformateur **et** distributeur | OK | Blocs “Je suis producteur ou transformateur créole” et “Je suis distributeur, boutique, restaurant ou hôtel”. |
| 2 | CTA « Proposer vos produits » présent | OK | Présent, lien vers `#pro-form`. |
| 3 | CTA « Référencer des produits créoles » présent | OK | Présent, lien vers `#pro-form`. |
| 4 | Distributeurs cités : boutiques, restaurants, hôtels, revendeurs | OK | Cités dans doctrine Pro et bandeau `/shop`. |
| 5 | Pas de formulation « achat en volume » seul comme entrée Pro | OK | Aucune occurrence détectée ; l’entrée Pro parle référencement, approvisionnement, qualification. |
| 6 | Pas de « portail B2B » ou parcours transactionnel pro suggéré | OK | Mention explicite “pas un portail B2B transactionnel en phase 1”. |

---

## 5. Checklist — doctrine & prix

| # | Critère | Statut | Note |
|---|---------|--------|------|
| 7 | Doctrine brick & mortar visible (producteurs + distributeurs physiques) | OK | Section Pro explicite la connexion fournisseurs créoles / distributeurs européens et la distribution physique. |
| 8 | Porte de qualification commerciale — pas portail B2B phase 1 | OK | Formulation visible dans `#pro` et bandeau `/shop`. |
| 9 | Rappel discret : prix affichés = canal B2C CK | OK | Note visible dans l’intro `/shop` et footnote Pro. |
| 10 | Conditions B2B = qualification / back-office — pas tarifs publics B2B | OK | Footnote Pro mentionne conditions personnalisées via Odoo back-office, hors exposition publique. |
| 11 | Champ « Nature de la demande professionnelle » (pas « famille partenaire » figée) | OK | Libellé exact présent dans le formulaire. |
| 12 | Valeurs demande alignées MOA (fournisseur, distributeur, conditions, partenariat) | OK | Options : proposer une offre, référencer/approvisionner, demander conditions commerciales, partenariat/autre. |

---

## 6. Checklist — UX & non-régression

| # | Critère | Statut | Note |
|---|---------|--------|------|
| 13 | Pas de refonte UX lourde — layout V1.1 reconnaissable | OK | Ajout textuel Pro ; structure globale conservée. |
| 14 | Accueil, `/shop`, fiche produit inchangés structurellement | OK | Hero, boutique, fiche produit et grille conservés. |
| 15 | Action carte « Voir » conservée | OK | 13 CTA `Voir`, aucun `.quick-add`. |
| 16 | Burger mobile + drawer filtres fonctionnels | OK | Burger ouvre le menu mobile ; filtres ouvrent sidebar + overlay. |
| 17 | Responsive mobile section `#pro` | OK | Deux blocs Pro passent en 1 colonne ; formulaire largeur mobile OK. |
| 18 | Savon vétiver — Maison & bien-être · Savons | OK | Produit conservé et catégorisé. |

---

## 7. Points d’attention QA

Aucun blocage détecté.

Deux rappels de gouvernance restent importants :

```text
Validation QA V1.1.1 ≠ GO Dev.
GO Dev = validation QA V1.1.1 + levée explicite verrou MOA.
```

La mention “pas de tarifs B2B publics” est conforme à la doctrine ; elle ne constitue pas une exposition de tarifs B2B.

---

## 8. Verdict QA

```text
VALIDÉ V1.1.1
```

La micro-évolution Pro MOA est conforme aux arbitrages §10 et ne crée pas de régression visible sur la maquette V1.1.

QA valide :

- la section Pro double cible ;
- la qualification commerciale via formulaire ;
- la distinction prix publics B2C / conditions B2B back-office ;
- la non-régression UX ;
- le maintien du verrou Odoo.

QA ne valide pas :

- le démarrage d’une base Odoo ;
- la création de `dorevia_ck_theme` ;
- l’écriture de QWeb / SCSS ;
- une extension origines / collections / filtre prix ;
- un portail B2B transactionnel.

---

## 9. Suite après verdict

| Verdict | Suite |
|---------|-------|
| Validé | Levée verrou Odoo soumise à décision MOA explicite |
| Validé | Si GO ultérieur : ticket `dorevia_ck_theme` borné, tokens + layout uniquement |
| Validé | **Toujours pas de GO Dev sans décision MOA explicite de levée du verrou** |

Décision projet actuelle :

```text
Verrou Odoo maintenu.
Aucun Odoo · aucune base · aucun module · aucun QWeb/SCSS.
```
