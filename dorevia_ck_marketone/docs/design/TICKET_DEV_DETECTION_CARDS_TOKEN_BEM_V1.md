# Ticket Dev — Détection cards vedettes token-based (robuste retrait alias BEM) · V1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` · C-Kreyol / CK |
| **Module** | `dorevia_ck_marketone_content` (+ contexte thème `dorevia_ck_theme` 19.0.1.33.0) |
| **Type** | Durcissement / dette technique · périmètre étroit |
| **Priorité** | Moyenne (non bloquant ; prérequis au retrait des alias legacy) |
| **Statut** | **Prêt à recetter** — code QA livré, à committer |
| **Lié à** | Homogénéisation BEM des cards (thème 33.0 · `product_card.scss`) · série propagation Section 3 |

```text
But : que la détection de fraîcheur/validité des cards vedettes survive à la
suppression future des alias legacy product-card-*, finalité de l'homogénéisation BEM.
```

---

## 1. Contexte

L'homogénéisation BEM (thème `19.0.1.33.0`) a introduit des **doubles classes** sur les cards : BEM (`ck-product-card__*`) + alias legacy de compat (`product-card-*`). Les regex de `home_featured.py` (validité de card + détection de péremption cron) étaient couplées à la **chaîne de classes exacte et ordonnée**, ex. :

```python
r'class="(?:ck-product-card__title product-card-title|product-card-title)"[^>]*>([^<]+)'
```

**Risque :** le jour où les alias legacy sont retirés (finalité de l'homogénéisation), `class="ck-product-card__title"` ne matche plus → la détection de péremption devient **silencieusement aveugle** (la home ne se rafraîchit plus sur certaines éditions BO, sans erreur visible).

---

## 2. Travail QA déjà réalisé (à intégrer)

Refonte des regex en **token-based**, ancrées sur les classes **BEM stables** :

- Helper `_ck_class_token_pattern(token)` (bornes `(?<![\w-])` / `(?![\w-])`) → matche le token où qu'il soit dans l'attribut `class`, quel que soit l'ordre, les voisins ou la présence d'alias.
- Regex refaites : titre, prix, méta (capture texte), `card-cta`, `card-cart-cta`, cover, labels block.
- Check littéral `'class="card-cart-cta"' not in arch` → remplacé par `_CARD_CART_CTA_RE.search(arch)`.
- **Verrou de régression** : `tests/test_ck_featured_card_markers.py` (tag `dorevia_ck_marketone_card_markers`) — assert le matching sur HTML **dual actuel + BEM-only futur + réordonné** et l'absence de **faux positif** `card-cta` / `card-cart-cta`.

**Fichiers touchés :**

- `dorevia_ck_marketone_content/home_featured.py` (regex token-based)
- `dorevia_ck_marketone_content/tests/test_ck_featured_card_markers.py` (nouveau)
- `dorevia_ck_marketone_content/tests/__init__.py` (enregistrement)

Vérifs locales : `py_compile` OK · self-test logique vert (dual + BEM-only + anti-faux-positifs).

---

## 3. Demande au Dev

1. **Recetter** sur `dorevia_ck_marketone_01` :
   ```bash
   docker exec sandbox-odoo19-odoo-1 odoo -d dorevia_ck_marketone_01 \
     --test-enable --stop-after-init --no-http \
     --test-tags=dorevia_ck_marketone_card_markers,dorevia_ck_marketone_featured_propagation,dorevia_ck_marketone_home_section3
   ```
2. **Bump version** `dorevia_ck_marketone_content` (incrément suivant) — **pas de migration nécessaire** : changement *detection-only*, HTML généré **inchangé**, snapshots existants restent valides, code rechargé au `-u`.
3. **Committer** : `fix(section3): token-based featured card markers (robust to legacy alias removal)`.

### Étape suivante (désormais sûre) — finalisation homogénéisation

Une fois ce commit passé, le retrait des **alias legacy `product-card-*`** du HTML (home `home_featured.py` + snippets thème + `product_card.scss`) peut être planifié : la détection token-based + le verrou `dorevia_ck_marketone_card_markers` garantissent qu'aucune régression silencieuse ne passe (le test vire au rouge si le pattern casse).

---

## 4. Critères d'acceptation

- `dorevia_ck_marketone_card_markers` : vert (dual + BEM-only + réordonné + anti-faux-positifs).
- `dorevia_ck_marketone_featured_propagation` + `dorevia_ck_marketone_home_section3` : non-régression verte.
- Recette visuelle home `/fr` : section « Nos coups de cœur » rendue, prix/titres à jour (inchangé fonctionnellement).
- Au retrait futur des alias : le verrou reste vert sans modification des regex.

---

## 5. Hors scope

- Aucune logique métier / prix / panier modifiée.
- Retrait effectif des alias legacy = lot séparé (préparé par ce ticket, pas exécuté ici).
- Aucune migration / re-bootstrap.

---

*Ticket Dev · détection cards token-based · prérequis retrait alias BEM · 2026-06-17.*
