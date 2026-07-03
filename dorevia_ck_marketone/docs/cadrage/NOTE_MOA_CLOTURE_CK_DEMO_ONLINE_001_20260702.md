# Note MOA — Clôture CK-DEMO-ONLINE-001 — Démo publique tunnel Cloudflare

| Champ | Valeur |
| --- | --- |
| Date | 2 juillet 2026 |
| Projet | C-Kréyòl Marketone — démo en ligne |
| Destinataires | MOA, Produit, QA, Dev |
| Statut | **GO démo avec réserves connues** |
| Base | `dorevia_ck_marketone_01` |
| URL locale | http://localhost:18079 |
| URL publique recette | https://basename-prev-keith-panels.trycloudflare.com |
| Tunnel | Cloudflare quick tunnel — **relancé le 3 juillet 2026** (ancienne URL `assure-violation-markets-factors.trycloudflare.com` expirée) · **laisser actif** tant que la démo est ouverte |

---

## Objet

Exposer la boutique C-Kréyòl Marketone via un tunnel public pour démonstration MOA / acheteur, sans déploiement prod.

Parcours validé sur l’URL publique : Home → navigation header → Shop → fiche produit → Producteurs → Professionnels.

---

## Décision MOA

**GO démo** — réserves documentées ci-dessous, non bloquantes pour une présentation live.

---

## Recette

### Contrôles validés

| Zone | Résultat |
| --- | --- |
| Home FR | `200` · titre `Home \| C-Kreyol` · rendu desktop OK |
| Header NAV (Option C) | `Boutique` (icône maison, libellé accessibilité OK) · `Épicerie` · `Boissons` · `Soin & Bien-être` · `Artisanat` · `Producteurs` · `Professionnels` |
| `/shop` | `200` |
| Fiche produit `/shop/confiture-de-goyave-3` | `200` |
| `/producteurs` | `200` · visuels chargés après chargement complet · pas de broken image |
| `/professionnels` | `200` |
| Assets | CSS `200` (~1,13 Mo) · JS `200` · logo SVG `200` |
| Mobile simulé 390 px | Home FR · drawer OK · pas d’overflow horizontal |
| Sécurité DB | `odoo.conf` : `dbfilter = ^dorevia_ck_marketone_01$` · `/web/database/selector` accessible mais ne liste que `dorevia_ck_marketone_01` |

### Réserves maintenues (non bloquantes)

| Réserve | Impact | Action si démo prolongée |
| --- | --- | --- |
| Meta / canonical / OG → `localhost:18079` | Partage réseaux sociaux / SEO incorrects sur URL publique | Configurer `web.base.url` ou override canonical sur l’URL tunnel |
| Curl sans `Accept-Language` → `/en` | Bots / crawlers sans locale arrivent en EN | Comportement Odoo attendu · navigateur mobile simulé reste FR |
| `/web/database/selector` accessible | Surface réduite par `dbfilter` · endpoint toujours visible | Acceptable démo interne · à durcir en prod |
| Tunnel actif | URL publique dépend du processus tunnel | Ne pas couper tant que la démo est ouverte |

---

## Doctrine exploitation

- **Présentation live MOA / acheteur** : exploitable telle quelle.
- **Partage externe** (email, réseaux) : signaler explicitement que les meta pointent encore vers `localhost:18079`.
- **Ordre navigation** : référence MOA Option C — `Boutique · Épicerie · Boissons · Soin & Bien-être · Artisanat · Producteurs · Professionnels` (cf. réalignement séquences du 2 juillet 2026).

---

## Verdict

**CK-DEMO-ONLINE-001 est clôturé en GO démo avec réserves connues.**
