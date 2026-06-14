# Points à arbitrer — avant traduction Odoo

> Mise à jour 2026-06-13 — ticket 01 clôturé côté socle · phase CMS MOA · **pause home note_05**.

---

## État projet

```text
Référentiel technique : Odoo 19 CE · snippets first · pas de surcouche autonome
Arbitrages §10 : tranchés côté MOA
Maquette V1.1.1 : validée QA
Note approche thème : validée MOA
Ticket dorevia_ck_theme_01 : clôturé côté socle (2026-06-12)
Squelette dorevia_ck_theme : livré · validé QA
Instance recette : dorevia_ck_marketone_01 · http://localhost:18079
Phase : maquette V1.2 **livrée Dev** — recette QA en attente
Home complète Odoo : EN PAUSE — reprise post-verdict QA maquette V1.2
Verrou Odoo : levé ticket 01 uniquement · GO général CK non donné
```

```text
Phase CMS MOA ≠ autorisation Dev
Pas d’extension · pas de surcouche · pas de B2B custom
Website Builder + contenus BO + snippets CK Marketone uniquement
```

---

## Évolution maquette — lecture MOA

```text
Maquette V1.1.1 = validée QA (adaptation Pro MOA) — base esthétique
Note d’itération MOA : note_05.md — doctrine boutique élégante · conversion
Cible suivante : Maquette CK V1.2 « Boutique élégante » — avant reprise home Odoo
Recette V1.1.1 : recette_qa_maquette_01_1.md — VALIDÉ V1.1.1
Architecture Odoo = verrouillée
```

**Exemples illustratifs** (textes Pro post-arbitrage — non engagement) :

```text
Vous êtes producteur ou transformateur créole ?
Proposez vos produits et structurez votre offre avec CK.

Vous êtes boutique, restaurant, hôtel ou distributeur ?
Référencez des produits créoles et approvisionnez votre point de vente.

Les prix affichés publiquement correspondent au canal B2C CK.
Les partenaires professionnels qualifiés peuvent bénéficier de conditions commerciales personnalisées via Odoo.
```

---

## Tranché MOA — maquette & design (V1.1)

| # | Sujet | Décision MOA |
|---|-------|--------------|
| 1 | **Palette** | Corail `#D84315` + vert `#2E7D4F` — base V1, pas DA finale |
| 2 | **Typo maquette** | Fraunces + DM Sans — réévaluation avant prod Odoo |
| 3 | **Périmètre produit** | Agro-transformation créole — inclut Maison & bien-être (savon OK) |
| 4 | **Catégories** | Arborescence `product.public.category` cible |
| 5 | **Quick-add** | **Non retenu** phase 1 — action « Voir » |
| 6 | **Packs maquette** | 1 produit / 1 carte / 1 prix |

---

## Tranché MOA — arbitrages §10 (grille Odoo)

| # | Sujet | Décision MOA |
|---|-------|--------------|
| 1 | **Packs `non_detailed`** | ✅ 1 produit Odoo = 1 ligne panier |
| 2 | **Origines** | ✅ Attribut produit phase 1 |
| 3 | **Collections** | ✅ Catégories / tags d’abord |
| 4 | **Filtre prix** | ✅ Natif / simplifié ; report si extension prématurée |
| 5 | **Entrée pro** | ✅ CMS + `website_crm` · double cible · nature de la demande |
| 6 | **Typo production** | ✅ Réévaluer avant build thème |
| 7 | **Textes brick & mortar** | ✅ Doctrine validée · micro-évolution textuelle autorisée |
| 8 | **Verrou Odoo** | ✅ **Maintenu** |

---

## Doctrine prix B2C / B2B (MOA)

```text
Prix publics affichés = canal B2C CK (visiteur non identifié)
Partenaire B2B qualifié = conditions via product.pricelist Odoo (back-office)
Pas d’exposition publique des prix B2B en phase 1
Pas de portail B2B transactionnel complet en phase 1
```

```text
Prix publics B2C affichés sur le site ≠ conditions B2B personnalisées via listes de prix Odoo
```

---

## Entrée pro — décision MOA (rappel)

```text
Page Pro unique + deux blocs + deux CTA distincts
+ formulaire unique (Nature de la demande professionnelle)
+ CMS + website_crm
```

```text
Formulaire Pro → lead CRM → qualification → partenaire → rôles selon flux réels
```

Le champ qualifie la **demande**, pas le rôle définitif du partenaire.

---

## Encore ouvert

| # | Sujet | Statut |
|---|-------|--------|
| 1 | **Instance Odoo 19 CE** | **Disponible** — base `dorevia_ck_marketone_01` · [`REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md`](../REFERENCE_INSTANCE_RECETTE_DOREVIA_CK_THEME_01.md) |
| 2 | **Recette QA ticket 01** | ✅ **Clôturé socle** — [`recette_qa_dorevia_ck_theme_01_visuelle_post_correction.md`](../recette_qa_dorevia_ck_theme_01_visuelle_post_correction.md) |
| 3 | **Correction `layout_ck_theme` (`ck-theme`)** | ✅ **OK QA** |
| 4 | **Typo production** | ⚠️ Fallbacks système · Fraunces/DM Sans = arbitrage prod |
| 5 | **Composition CMS MOA** | ⏸ **Home en pause** ([`note_05.md`](../../cadrage/note_05.md)) · V1.2 requise — [`ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md`](../ticket_moa_composition_cms_ck_01_accueil_vedettes_page_pro.md) |

---

## Limites de la maquette V1.1

```text
Données produit, prix, stock = fictifs HTML.
Filtres sidebar = démo JS locale (non spec Odoo).
Badge panier header = décoratif.
Pas de panier ni checkout maquettés.
Pas d’état vide catalogue montré.
Pas de variante produit (taille/format) sur fiche démo unique.
```

---

## Suite

```text
1. ✅ QA maquette V1.1.1 validée
2. ✅ Validation MOA note approche (Odoo 19 CE · snippets first)
3. ✅ Ticket 01 validé MOA — GO exécution encadré
4. ✅ Verrou levé ticket 01 uniquement
5. ✅ Squelette dorevia_ck_theme livré — validé QA statique
6. ✅ Instance `dorevia_ck_marketone_01` — socle installé
7. ✅ Ticket composition CMS CK 01 — validé MOA
8. ✅ Note d’itération MOA — note_05 · pause home complète
9. ✅ Maquette CK V1.2 livrée Dev — [`LIVRAISON_V1_2.md`](../maquette_01.2/LIVRAISON_V1_2.md) · recette [`recette_qa_maquette_01_2.md`](../maquette_01.2/recette_qa_maquette_01_2.md)
10. ⏳ CMS partiel hors pause : /professionnels · menu Pro · recette [`recette_qa_composition_cms_ck_01.md`](../recette_qa_composition_cms_ck_01.md)
11. ☐ Reprise composition home V1.2 · verdict OK / KO
12. Extensions : ticket séparé + arbitrage MOA uniquement
```
