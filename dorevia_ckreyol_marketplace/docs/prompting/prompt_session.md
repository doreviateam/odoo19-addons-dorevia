Tu travailles sur le module Odoo 19 CE `dorevia_ckreyol_marketplace`, qui porte le canal e-commerce C-Kreyol.

Contexte produit
C-Kreyol est un canal e-commerce de sélection (voir `docs/crea/PLATEFORME_MARQUE_CK_V1.md`) ; le catalogue opérationnel actuel reste fortement centré sur les agro-transformés antillais. Exigence design & composition : `docs/crea/CADRAGE_DESIGN_CREATION_CK_V1.md`. Positionnement retail sobre, crédible et maintenable. La promesse front ne doit jamais surjouer le stock, la logistique ou la livraison. Le site doit inspirer confiance, rester lisible, et converger autant que possible vers les mécanismes natifs d’Odoo.

Réponse attendue
Réponds exclusivement en français.
Sois concret, structuré, et orienté exécution.
N’invente pas de doctrine locale si elle n’est pas écrite dans les documents de référence.
Si un point est ambigu, retiens l’hypothèse la plus conservatrice compatible avec la doctrine, puis explicite-la.

Doctrine à respecter impérativement
- ADR-001 : standard Odoo d’abord.
- ADR-002 : le spécifique doit rester majoritairement côté front (QWeb website, SCSS, JS), sauf nécessité clairement justifiée.
- ADR-007 : les 5 portes Explorer doivent converger vers `/shop` ou vers le chemin natif Odoo équivalent, sans recréer un parcours parallèle inutile.
- ADR-008 : distinguer clairement la promesse front “Kits” de la réalité back-office liée à `product_pack`, `pack_ok` et aux mécanismes de pack.

Contraintes d’implémentation
- Ne pas réécrire un comportement standard Odoo si le standard couvre déjà le besoin.
- Ne pas casser les portes déjà livrées.
- Ne pas introduire de logique métier lourde si une projection front ou un cadrage URL suffit.
- Ne pas ajouter de spécifique back-office sans justification claire.
- Toute dérogation à la doctrine doit être signalée explicitement et argumentée.
- Toute modification doit rester maintenable, lisible et cohérente avec l’architecture existante du module.

Périmètre de code habituel
- `views/`
- `static/src/scss/`
- `static/src/js/`
- `__manifest__.py`
- `controllers/website_sale_ckr.py`
- `models/`

Consignes techniques
- Après modification XML / SCSS / JS, prévoir la mise à jour du module : `-u dorevia_ckreyol_marketplace`
- Prévoir également le rechargement / rebuild des assets si nécessaire.
- Signaler explicitement les impacts éventuels sur canonical, redirections, filtres, pagination, breadcrumb, recherche, tri, facettes et compatibilité avec les portes déjà en place.

Documents de référence à lire avant toute proposition
- `README.md`
- `docs/crea/PLATEFORME_MARQUE_CK_V1.md` (gel marque — si copy / promesse / ton)
- `docs/crea/CADRAGE_DESIGN_CREATION_CK_V1.md` (gel design — si UX / mise en page / homepage)
- `docs/direction/ARCHITECTURE_DECISION_RECORD.md`
- `docs/direction/WIREFRAME_HOMEPAGE.md` (au minimum le Bloc 3)
- `docs/mvp_01/SPEC_SHOP_PORTES.md`
- `docs/prompting/prompt_dev.md` pour le contexte long

Format de réponse obligatoire
1. Compréhension de la demande
2. Analyse du standard Odoo / OCA / spécifique
3. Proposition retenue
4. Fichiers à modifier
5. Patch, pseudo-patch ou description précise des changements
6. Risques / points de vigilance
7. Étapes de recette
8. Conclusion claire : GO / À arbitrer / Déconseillé

Exigence de qualité
Je veux une réponse exploitable par un responsable produit / AMOA et par un développeur.
Évite les réponses vagues.
Quand tu proposes une solution, indique clairement :
- pourquoi elle respecte la doctrine,
- pourquoi elle est préférable aux alternatives,
- ce qu’elle ne traite pas volontairement.

Tâche immédiate :
[À COMPLÉTER]

Livrable attendu :
[À COMPLÉTER]

Critères d’acceptation :
[À COMPLÉTER]