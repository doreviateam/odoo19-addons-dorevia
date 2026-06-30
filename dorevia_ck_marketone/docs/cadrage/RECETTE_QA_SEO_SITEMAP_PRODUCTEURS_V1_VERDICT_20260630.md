# Recette QA — SEO / Sitemap Producteurs V1 — Verdict

| Champ | Valeur |
| --- | --- |
| Date | 30 juin 2026 |
| Instance | `dorevia_ck_marketone_01` — http://localhost:18079 |
| Module | `dorevia_ck_marketone_content` |
| Version livrée | `19.0.1.70.1` |
| Tag tests auto de référence | `dorevia_ck_producers_seo_v1` — annoncé `11/11` vert |
| Verdict | **GO QA / MOA** |

## Actions Réalisées

Upgrade module sur la base recette :

```bash
docker exec sandbox-odoo19-odoo-1 odoo -c /etc/odoo/odoo.conf \
  -d dorevia_ck_marketone_01 --http-port=8079 \
  -u dorevia_ck_marketone_content --stop-after-init
```

Résultat : upgrade terminé proprement, registre rechargé et signalé.

Redémarrage worker :

```bash
docker restart sandbox-odoo19-odoo-1
```

Résultat : conteneur `sandbox-odoo19-odoo-1` redémarré.

## Contrôles Sitemap

Sitemap contrôlé via :

```bash
curl -sS -H 'X-Odoo-Database: dorevia_ck_marketone_01' \
  http://localhost:18079/sitemap.xml
```

| Contrôle | Résultat |
| --- | --- |
| `/sitemap.xml` répond | OK — `HTTP/1.1 200 OK`, `Content-Type: application/xml;charset=utf-8`. |
| `/producteurs` présent | OK — entrée `http://localhost:18079/producteurs`. |
| Fiche canonique La Platine présente | OK — entrée `http://localhost:18079/producteur/sarl-la-platine-1405` avec `lastmod` au 30/06/2026. |
| `/nos-producteurs` absent | OK — aucune occurrence dans le sitemap généré. |
| Fiches pilotes legacy `/producteur/...` sans suffixe `-<id>` absentes | OK — seule URL `/producteur/` indexée : `/producteur/sarl-la-platine-1405`. |
| Redirection legacy `/nos-producteurs` | OK — `HTTP/1.1 301 MOVED PERMANENTLY`, `Location: /producteurs`. |

## Réserves

| Sujet | Observation | Impact |
| --- | --- | --- |
| Contexte multi-base local | Les requêtes `curl` sans base sélectionnée retournent le 404 technique Odoo "No database is selected". Les contrôles sitemap ont donc été faits avec `X-Odoo-Database: dorevia_ck_marketone_01`. | Non bloquant pour la recette ; préciser au QA d'utiliser la base recette sélectionnée. |
| Logs Odoo globaux | Des erreurs cron persistent sur une autre base (`glc-audit-paliers-0-3`, colonne `res_company.glc_default_bank_journal_id` absente). | Hors périmètre SEO/Sitemap Producteurs ; aucun impact constaté sur `dorevia_ck_marketone_01`. |

## Conclusion

**GO fonctionnel.** Le sitemap dynamique Producteurs V1 expose l'annuaire et la fiche producteur canonique attendue, tout en retirant les pages CMS legacy du périmètre indexable.

Les tests automatisés `dorevia_ck_producers_seo_v1` n'ont pas été relancés pendant cette recette manuelle ; ils étaient annoncés `11/11` verts dans la livraison.
