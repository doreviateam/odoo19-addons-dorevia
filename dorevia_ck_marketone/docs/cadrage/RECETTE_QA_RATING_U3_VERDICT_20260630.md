# Recette QA — Rating-U3 — Verdict

| Champ | Valeur |
| --- | --- |
| Date | 30 juin 2026 |
| Instance | `dorevia_ck_marketone_01` — http://localhost:18079 |
| Module | `dorevia_ck_theme` |
| Version livrée | `19.0.1.110.0` |
| Verdict | **GO QA / MOA** |

## Actions Réalisées

Upgrade thème sur la base recette :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --http-port=8079 \
  -u dorevia_ck_theme --stop-after-init
```

Résultat : upgrade terminé proprement, vues `website_sale_product_card.xml` et `website_sale_product_page.xml` chargées, registre rechargé.

Redémarrage worker :

```bash
docker restart sandbox-odoo19-odoo-1
```

Résultat : conteneur `sandbox-odoo19-odoo-1` redémarré.

## Contrôles Réalisés

| Critère | Résultat |
| --- | --- |
| Fiche produit avec avis — `/shop/confiture-de-goyave-3` | OK — rendu compact `★ 4,8 · 1 avis`, via `.ck-card-rating`, valeur `.ck-rating-value=4,8`, compteur `.ck-rating-count=1 avis`. |
| Ancien widget natif | OK — aucune trace de `.o_website_rating_static`, `rating_widget_stars_static` ou étoiles vertes natives dans le HTML fiche/card contrôlé. |
| Lien vers les avis | OK — le rating reste dans `<a href="#o_product_page_reviews" class="o_product_page_reviews_link">`; clic validé, la zone `Avis clients` arrive dans le viewport. |
| Card shop | OK — card `Confiture de goyave` inchangée, `★ 4,8 · 1 avis` rendu via `.ck-card-rating`. |
| Card home | OK — card home `Confiture de goyave` rend le même rating compact. |
| Produit sans avis — `/shop/galettes-de-manioc-20` | OK — aucun `.ck-card-rating`, aucun lien rating, aucun faux `0,0` / `0 avis`. |
| Mobile 390 px | OK — fiche Confiture en `390 px`, `clientWidth=390`, `scrollWidth=390`, rating visible et contenu dans le viewport (`x=32`, `right=358`). |
| Console navigateur | OK — aucune erreur console sur la fiche active. |

## Captures

| Capture | Fichier |
| --- | --- |
| Produit sans avis | `/private/tmp/rating_u3_no_reviews_galettes.png` |
| Mobile 390 px — rating centré | `/private/tmp/rating_u3_mobile_confiture_390_centered.png` |

## Réserves Non Bloquantes

| Sujet | Observation | Impact |
| --- | --- | --- |
| Contexte multi-base local | Les requêtes `curl` sans base sélectionnée restent ambiguës sur cette sandbox multi-DB ; les contrôles HTTP ont été faits avec `X-Odoo-Database: dorevia_ck_marketone_01` ou via navigateur avec la base sélectionnée. | Non bloquant. |
| Logs Odoo globaux | Des erreurs cron persistent sur une autre base (`glc-audit-paliers-0-3`, colonne `res_company.glc_default_bank_journal_id` absente). | Hors périmètre Rating-U3 ; aucun impact constaté sur `dorevia_ck_marketone_01`. |

## Conclusion

**GO fonctionnel.** Rating-U3 aligne bien la fiche produit sur le rendu compact des cards Home/Boutique, conserve la navigation vers les avis, et ne crée pas de faux rating pour les produits sans avis.

Tests automatisés non relancés pendant cette recette manuelle.
