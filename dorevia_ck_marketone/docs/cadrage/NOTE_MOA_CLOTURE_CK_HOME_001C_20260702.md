# Note MOA — Clôture CK-HOME-001C — Hygiène visible home (tunnel démo)

| Champ | Valeur |
| --- | --- |
| Date | 2 juillet 2026 |
| Projet | C-Kréyòl Marketone — home |
| Destinataires | MOA, Produit, QA, Dev |
| Statut | **GO recette / GO commit** |
| Module | `dorevia_ck_marketone_content` |
| Version | `19.0.1.74.0` |
| Base recette | `dorevia_ck_marketone_01` |
| URL tunnel | https://assure-violation-markets-factors.trycloudflare.com |

---

## Objet

Lot d'hygiène visible sur la home et pages légales associées, validé en direct sur le tunnel Cloudflare (requêtes fraîches, sans cache).

Quatre chantiers :

1. **Newsletter FR** — invalidation du snapshot home si texte anglais résiduel ; reconstruction depuis la vue native déjà traduite.
2. **Marque C-Kréyòl** — harmonisation `website.name`, `res.company.name` (garde conditionnelle), contenus CMS, footer et vues hors bootstrap.
3. **Carte Boissons** — passage 3 → 4 cartes « Acheter par univers » avec visuel produit (nectar Mont Pelé, 1200×900).
4. **Non-régression** — `/`, `/shop`, `/producteurs`, `/professionnels` → `200`.

---

## Recette

### Contrôles tunnel (QA réseau / DOM)

| Contrôle | Résultat |
| --- | --- |
| Home FR `200` | OK · titre `Home \| C-Kréyòl` |
| Newsletter succès | `Merci pour votre inscription !` · pas de `Thanks for registering` |
| Marque | `0` occurrence `C-Kreyol` sur `/`, `/terms`, `/privacy`, `/legal` |
| Univers 4 cartes | `épicerie`, `boissons`, `soin`, `artisanat` · image `ck_univers_boissons.jpg?v=6` → `200` |
| Non-régression | `/shop`, `/producteurs`, `/professionnels` → `200` |
| Mobile markup | offcanvas présent · `viewport` OK · tunnel FR avec `Accept-Language: fr-FR` |

### Tests automatisés

| Tag | Résultat |
| --- | --- |
| `dorevia_ck_home_001c` | OK |
| `dorevia_ck_marketone_home_section4` | OK (4 cartes, intro « Quatre univers… ») |
| `dorevia_ck_marketone_home_lot4` | OK (newsletter FR, dual Pro) |
| **Total lot** | **29 post-tests, 0 failed, 0 error** |

### Réserve QA visuelle

Desktop / mobile 390 px : markup et réseau validés ; **pas de capture viewport** dans cette recette (à compléter MOA si besoin avant prod).

---

## Périmètre livré

| Fichier | Modification |
| --- | --- |
| `home_dual_engage.py` | Invalidation snapshot newsletter anglais · validation FR assouplie (placeholder e-mail) |
| `hooks.py` | `bootstrap_brand_name()`, `bootstrap_footer_copyright_brand()` · rendu newsletter en langue site + libellé succès FR |
| `home_univers.py` | Carte Boissons · 4 cartes · intro reformulée · cache-bust `v=6` |
| `home_editorial.py`, `legal_pages.py` | `C-Kreyol` → `C-Kréyòl` |
| `migrations/19.0.1.74.0/post-migrate.py` | Bootstrap lot + `cr.commit()` explicite |
| `static/img/ck_univers_boissons.jpg` | Visuel carte Boissons |
| Tests | `test_ck_home_001c.py` · mise à jour section 4 (4 cartes) |

---

## Point technique exploitation

Sur ce sandbox, un `odoo -u … --stop-after-init` seul peut ne pas persister tous les writes sur champs traduits : la migration `19.0.1.74.0` inclut un `cr.commit()` explicite. En cas de doute post-upgrade, rejouer `bootstrap_ck_catalogue_navigation` / bootstraps home via `odoo shell`.

Vue inactive `website.custom_copyright_ck_phase1` : résidu `C-Kreyol` sans impact visible — non touchée.

---

## Verdict

**CK-HOME-001C est clôturé en GO.**

Prêt à enchaîner sur **CK-HOME-001A** (hero) sur feu vert MOA.
