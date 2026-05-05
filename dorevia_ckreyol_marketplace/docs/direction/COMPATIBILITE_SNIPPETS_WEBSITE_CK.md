# Chantier transverse — Compatibilité snippets Odoo Website (C-Kreyol)

**Nature** : chantier **transverse** — il traverse les vagues MVP et les lots fonctionnels ; il n’est **pas** un remplacement des tickets produit par section.  
**Pilotage ordre global** : [CHANTIERS_CK_ORDRE.md](CHANTIERS_CK_ORDRE.md).

---

## Intention

À mesure que les sections C-Kreyol **se stabilisent**, les rendre **compatibles** avec la logique **Odoo Website** : snippets, blocs éditables, options de configuration et **réutilisation** propre dans le Website Builder lorsque c’est **pertinent**.

---

## Sections concernées (orientation)

- bloc **newsletter** ;
- page **demande compte professionnel** ;
- bloc **« Être rappelé »** ;
- blocs **homepage** ;
- **portes** commerciales ;
- sections **éditoriales Communauté** ;
- futurs blocs **panier / favoris** si exposés côté header ou produit ;
- éventuels blocs **avis clients** / **réassurance**.

La liste évolue avec le produit ; le périmètre exact se fixe **par zone** dans les tickets d’exécution.

---

## Objectifs

- éviter des sections **trop figées** en dur lorsque l’édition métier ou marketing est légitime ;
- permettre des **ajustements** depuis le Website Builder **quand c’est pertinent** ;
- rester **cohérent** avec la **charte CK** ;
- **limiter** le spécifique QWeb lorsque le **standard Odoo** suffit ;
- garder des blocs **réutilisables** et **maintenables**.

---

## Garde-fous

- Ne pas **tout** transformer en snippet **trop tôt**.
- Ne pas rendre **éditable** ce qui relève d’un **contrat fonctionnel** ou d’une **logique métier** (workflows, champs obligatoires, règles CRM, etc.).
- Ne pas **casser** les tests ni la **doctrine catalogue** / intégrité des parcours e-commerce.
- Garder les **composants critiques** maîtrisés **côté code** (tunnel d’achat, règles de prix, conformité).

---

## Priorité et principe de conduite

Ce chantier est **transverse** : à traiter **après stabilisation** des blocs et parcours **principaux** de chaque vague.

> D’abord **stabiliser** le comportement et la DA.  
> Ensuite seulement **transformer** les sections **utiles** en snippets Odoo **propres**.

Les snippets sont un **outil de exploitation**, pas un objectif en soi.
