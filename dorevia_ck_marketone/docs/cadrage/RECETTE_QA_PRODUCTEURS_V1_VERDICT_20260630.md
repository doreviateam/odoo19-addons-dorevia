# Recette QA — Producteurs CK V1 — Verdict

| Champ | Valeur |
| --- | --- |
| Date | 30 juin 2026 |
| Instance | `dorevia_ck_marketone_01` — http://localhost:18079 |
| Référence | `NOTE_MOA_LIVRAISON_PRODUCTEURS_V1_20260630.md` |
| Périmètre | Checklist manuelle "Recette MOA / QA" |
| Verdict | **GO QA / MOA avec réserves non bloquantes de contenu et d'environnement** |

## Synthèse

La recette manuelle du sprint **Producteurs CK V1** est conforme sur le périmètre fonctionnel livré : annuaire producteurs, fiche La Platine, redirections SEO, liens depuis fiche produit, absence de lien producteur sur produit sans `ck_producer_id`, non-régression du tunnel achat FR/EN et responsive mobile 390 px.

Les tests automatisés `dorevia_ck_producers_v1` n'ont pas été relancés, conformément à la note de livraison qui les indique déjà verts `23/23` au 30/06.

## Points Validés

| Contrôle | Résultat |
| --- | --- |
| `/producteurs` | OK — page rendue, card `SARL La Platine`, localisation `Sainte-Anne, Guadeloupe`, compteur `1 produit`, CTA `Découvrir le producteur`. |
| Fiche `SARL La Platine` | OK — titre, localisation, accroche, contenu long, produit `Manio Crackers`, lien retour `Tous nos producteurs`. |
| Lien retour fiche → annuaire | OK — clic vers `http://localhost:18079/producteurs`. |
| Slug obsolète | OK — `/producteur/ancien-nom-1405` redirige vers `/producteur/sarl-la-platine-1405`; log serveur observé en `301` puis `200`. |
| URLs invalides | OK — `/producteur/producteur-fantome-999999999` et `/producteur/slug-sans-id` affichent la page 404 Odoo/C-Kreyol. |
| Chip producteur sur Manio | OK — lien `a.ck-chip.ck-chip--producer` `SARL La Platine` vers `/producteur/sarl-la-platine-1405`, clic validé. |
| Produit sans producteur | OK — `Galettes de manioc` ne contient aucun lien `/producteur/` ni chip producteur lié. |
| Tunnel achat FR | OK — Home → Shop → Manio → panier → adresse → livraison → paiement comptant → confirmation. Commande de recette générée : `S00103`. |
| Tunnel EN | OK — `/en/shop` → `/en/shop/manio-crackers-4` → panier → checkout ; `lang=en-GB`, Manio présent, CTA `Checkout`, champs adresse présents. |
| Mobile 390 px | OK — `/producteurs` et `/producteur/sarl-la-platine-1405` en `fr-FR`, `clientWidth=390`, `scrollWidth=390`, aucun overflow horizontal. |

## Réserves Non Bloquantes

| Sujet | Observation | Décision proposée |
| --- | --- | --- |
| Photo producteur | La fiche La Platine affiche le placeholder/icône producteur, pas une vraie image partenaire `image_1920`. | Réserve contenu MOA déjà couverte par l'action "Ajouter `image_1920` si disponible". Non bloquant Dev. |
| Accès instance en contexte vierge | Une requête brute sans base sélectionnée sur `http://localhost:18079/producteurs` retourne le 404 technique Odoo "No database is selected". En session navigateur attachée à `dorevia_ck_marketone_01`, la page est OK. | Pour QA, ouvrir l'instance avec la base `dorevia_ck_marketone_01` sélectionnée avant d'utiliser les URLs relatives. |
| Logs Odoo globaux | Des erreurs cron existent sur une autre base (`glc-audit-paliers-0-3`, colonne `res_company.glc_default_bank_journal_id` absente). Aucun impact constaté sur `dorevia_ck_marketone_01` pendant la recette Producteurs. | Hors périmètre sprint Producteurs ; à traiter séparément si l'équipe maintient cette base. |

## Conclusion

**GO fonctionnel pour Producteurs CK V1.** Les écarts observés ne bloquent pas la validation du sprint : ils relèvent soit du contenu MOA à enrichir, soit de l'environnement multi-base local.
