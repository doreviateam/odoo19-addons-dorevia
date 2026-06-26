Fiche de cadrage — Boutique C-Kréyòl V1
Ce qui change / Ce qui ne change pas
Projet : C-Kréyòl — Évolution des pages catégories boutique
Date : 26 juin 2026
Rédigé par : Produit / UX
Destinataires : Dev, QA, Lead Tech
Statut : À valider par Dev & QA avant conception détaillée

    Gouvernance : Ce document ne prescrit pas l'implémentation technique. Il fixe l'expérience cible et les comportements attendus. Le Dev et la QA restent responsables de proposer l'approche la plus robuste.

1. Direction produit validée
C-Kréyòl est une boutique de sélection, pas une marketplace ou un catalogue filtrable de masse. Le design doit refléter cette posture : peu de références, mais choisies, qualifiées, avec origine et producteur identifiables.
2. Ce qui change côté UX
Table
#	Changement	Description	Impact utilisateur
2.1	Suppression de la sidebar permanente	La colonne "Affiner ma sélection" à gauche disparaît des pages catégories C-Kréyòl.	La grille produit gagne toute la largeur. Plus d'impression de page vide sur les catégories peu fournies.
2.2	Passage à une grille pleine largeur	La grille produit occupe 100 % de la largeur disponible (container standard C-Kréyòl).	Meilleure lisibilité, meilleure utilisation de l'espace, plus d'équilibre visuel.
2.3	Filtres déplacés dans un drawer / panneau repliable	Les filtres natifs Odoo (attributs, prix, étiquettes) restent accessibles via un bouton "Filtrer" qui ouvre un panneau latéral (offcanvas) ou un drawer.	Les filtres ne sont pas supprimés, juste rendus secondaires. L'utilisateur les trouve quand il en a besoin.
2.4	Affichage conditionnel des sous-catégories	Les sous-catégories visuelles (ronds avec image + label) ne s'affichent que si la catégorie courante possède des enfants.	Épicerie les affiche ; Boissons, Soin, Artisanat ne les affichent pas. Pas d'espace vide inutile.
2.5	Bloc de rebond pour catégories peu fournies	Si une catégorie contient moins de 3 produits en état initial (pas de recherche active, pas de filtre actif), un bloc de réassurance s'affiche sous la grille : message + CTA vers le shop général ou une catégorie sœur.	Transforme l'impression "page vide" en "sélection en cours d'enrichissement". Le bloc ne s'affiche pas après une recherche ou un filtre ayant réduit les résultats.
2.6	Toolbar compacte	Une seule ligne regroupant : bouton Filtrer, champ Recherche (inline), Tri (dropdown).	Navigation plus légère, moins de scroll, plus de cohérence entre les catégories.
2.7	Card produit sans ligne vide	Tous les champs optionnels (origine, producteur, poids, prix au kg) disparaissent proprement de la card si non renseignés.	Pas de conteneur HTML vide qui crée un espace blanc. La card reste compacte et élégante.
2.8	Responsive mobile 390 px	Aucun overflow horizontal. La toolbar s'adapte (colonne ou ligne compressée). La grille passe en 1 colonne. Le drawer de filtres prend l'écran.	Expérience mobile fluide et sans frustration.
3. Ce qui ne change pas
Table
#	Élément	Justification
3.1	Logique native website_sale d'Odoo	On ne modifie pas le calcul des prix, des stocks, du panier, du checkout, ni la logique de recherche interne d'Odoo.
3.2	Filtres, tri, recherche et pagination	Les mécanismes fonctionnels restent identiques. Seul le conteneur visuel des filtres change (sidebar → drawer). La pagination native Odoo est conservée.
3.3	Composant card C-Kréyòl existant	Le design de la card produit (image, badge, cœur, nom, prix, bouton panier) reste le même. On affinera uniquement la gestion des champs optionnels.
3.4	Données produit existantes	Aucune modification des fiches produit, des catégories publiques, des attributs, des étiquettes. On s'appuie sur ce qui est déjà en base.
3.5	Pas de nouveau modèle métier	Pas de création de modèles ckreyol.category.block, ckreyol.origin, etc. dans cette itération.
3.6	Pas de nouveaux champs origine / producteur	La logique origine/producteur déjà en place dans C-Kréyòl reste inchangée. On n'ajoute pas de champs spécifiques dans ce lot.
3.7	Pas de bannière administrable par catégorie	Le header de catégorie reste simple (titre + description optionnelle). Pas de champ image bannière ou couleur personnalisée en BO dans ce lot.
3.8	Pas d'impact sur les autres univers	Éditorial, Communautaire, Espace pro, et les autres modules C-Kréyòl ne sont pas touchés.
3.9	Pas de modification du back-office	Aucune vue BO à créer ou modifier. Le travail se fait uniquement sur le front (templates, assets).
4. Les états à recetter (checklist QA)
4.1 Par catégorie

    [ ] Boutique générale (/shop) : grille pleine largeur, pas de sidebar, toolbar visible, filtres accessibles via drawer.
    [ ] Épicerie créole (slug Odoo réel à confirmer par Dev, ex. /shop/category/epicerie-creole-1) : sous-catégories visuelles affichées (Biscuits, Confitures, Farines), grille pleine largeur, pas de sidebar.
    [ ] Boissons (slug Odoo réel à confirmer par Dev, ex. /shop/category/boissons-2) : 1 produit affiché proprement, pas de sidebar, pas de sous-catégories, bloc de rebond présent.
    [ ] Soin & Bien-être (slug Odoo réel à confirmer par Dev, ex. /shop/category/soin-bien-etre-3) : 1 produit avec badge "Agriculture Bio", affichage propre, bloc de rebond présent.
    [ ] Artisanat & culture (slug Odoo réel à confirmer par Dev, ex. /shop/category/artisanat-culture-4) : 1 produit avec badge "Nouveau", affichage propre, bloc de rebond présent.

4.2 Par état fonctionnel

    [ ] Mobile 390 px : aucun overflow horizontal, toolbar lisible, grille en 1 colonne, drawer de filtres plein écran, sous-catégories scrollables horizontalement.
    [ ] Recherche active : recherche inline dans la toolbar fonctionne, résultats affichés en grille pleine largeur.
    [ ] Filtre actif : clic sur "Filtrer" ouvre le drawer, sélection d'un attribut filtre la grille, badge "filtre actif" sur le bouton, possibilité de réinitialiser.
    [ ] Tri actif : changement de tri (prix, nouveautés) fonctionne, grille se met à jour.
    [ ] Pagination : si plus de 20 produits, la pagination native s'affiche correctement en pleine largeur.
    [ ] Catégorie vide (si applicable) : message Odoo natif conservé, pas de bloc rebond en conflit.

4.3 Non-régression

    [ ] Fiche produit détaillée (/shop/product/xxx) : inchangée, pas de régression.
    [ ] Panier : ajout au panier depuis la grille fonctionne, badge panier mis à jour.
    [ ] Checkout : flux de paiement intact.
    [ ] Autres sites (si multi-site) : website_sale natif non impacté sur les autres sites Odoo.
    [ ] Autres pages website_sale : page de recherche globale, page de marque, etc. — vérifier qu'elles ne sont pas affectées par le retrait de la sidebar.

5. Questions ouvertes à soumettre au Dev / QA
5.1 Implémentation technique

    Quelle est l'approche la moins risquée pour supprimer la sidebar ?
        Override du template website_sale.products ?
        Template alternatif sélectionnable par catégorie ?
        Héritage léger avec xpath sur la sidebar ?
        Quel est le risque de régression sur les autres pages website_sale (recherche globale, page marque) ?
    Comment réinjecter les filtres natifs dans un drawer sans les réécrire ?
        Peut-on réutiliser la vue website_sale.products_attributes et l'injecter dans un composant offcanvas ?
        Y a-t-il une dépendance JS/Bootstrap à gérer pour le toggle du drawer ?
        Le drawer doit-il être plein écran sur mobile et latéral sur desktop ?
    Comment éviter l'affichage du bloc rebond après une recherche ou un filtre ?
        Le bloc rebond doit-il s'afficher uniquement sur l'état initial de la catégorie (pas de recherche active, pas de filtre actif) ?
        Quelle est la condition technique la plus sûre : len(products) < 3 AND not search AND not filter_active ?
    La grille adaptative est-elle compatible avec le système de colonnes Odoo/Bootstrap ?
        Peut-on utiliser col-12 col-md-6 col-lg-4 avec une règle de centrage conditionnelle ?
        Ou faut-il passer en CSS Grid pour un contrôle plus fin ?
    Le composant card produit existe-t-il déjà sous forme de t-call réutilisable ?
        Peut-on y ajouter des conditions t-if sur les champs optionnels sans duplication de code ?

5.2 Risques et tests

    Quels sont les tests de non-régression à prévoir ?
        Liste des pages website_sale à tester systématiquement.
        Liste des modules C-Kréyòl à vérifier (y a-t-il un module qui surcharge déjà website_sale.products ?).
    Y a-t-il un impact sur le SEO ?
        La suppression de la sidebar modifie-t-elle la structure HTML (hiérarchie des titres, balises) ?
        La pagination et les URL de filtres restent-elles identiques ?
    Quelle est l'estimation de charge ?
        Peut-on livrer proprement dans un lot court (1 sprint) ?
        Quels sont les prérequis éventuels (nettoyage de code existant, mise à jour de librairie) ?

6. Livrables attendus de la part du Dev / QA
Avant de passer en conception détaillée, nous attendons :

    Faisabilité technique : oui / partiellement / non, avec justification.
    Approche recommandée : template alternatif, override léger, ou autre — avec argumentation sur les risques.
    Estimation : en points ou en jours-homme.
    Plan de tests de non-régression : liste des pages et scénarios à valider.
    Points de vigilance : tout ce qui pourrait bloquer, ralentir, ou créer de la dette technique.

7. Glossaire
Table
Terme	Définition
Sidebar	Colonne latérale fixe "Affiner ma sélection" avec les filtres et attributs produits.
Drawer / Offcanvas	Panneau latéral ou plein écran qui s'ouvre par-dessus le contenu, activé par un bouton.
Grille pleine largeur	Grille produit occupant 100 % de la largeur du container, sans colonne latérale.
Bloc de rebond	Section affichée sous la grille lorsqu'une catégorie a peu de produits en état initial, proposant un CTA vers une autre page. Ne s'affiche pas après une recherche ou un filtre actif.
Toolbar	Barre d'outils compacte regroupant recherche, tri et accès aux filtres.
Card produit	Composant visuel représentant un produit dans la grille (image, nom, prix, bouton).
État initial	État de la page catégorie sans recherche active, sans filtre actif, sans tri modifié.
Document produit / UX — C-Kréyòl
Version 1.1 — 26 juin 2026