# Cadre d’observation — Pilote contrôlé pack 7 `sale_product_pack`

| Champ | Valeur |
|-------|--------|
| **Décision MOA** | [`DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md`](./DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md) — **GO pilote contrôlé** |
| **Base** | `ckr-marketone-01` |
| **URL BO** | http://localhost:18079/web |
| **Prep** | [`PREP_RECETTE_PHASE_B_SALE_PRODUCT_PACK_BO.md`](./PREP_RECETTE_PHASE_B_SALE_PRODUCT_PACK_BO.md) |
| **Exécution technique** | [`NOTE_EXECUTION_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md`](./NOTE_EXECUTION_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md) |
| **Statut** | **Clôturé MOA** — verdict sortie pilote : **doctrine `non_detailed`** |
| **Doctrine pack CK** | [`DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md`](./DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md) |

---

## Doctrine

```text
Odoo exécute. Marketone habille et oriente.
Aucun moteur Odoo remplacé.
```

---

## Jeu de données pilote

| Rôle | Produit | Template | Config |
|------|---------|----------|--------|
| **Pilote observé** | Maniocookies salés La Platine | **7** | `detailed` · `pack_component_price=ignored` |
| **Témoin comparatif** | Crackers manioc Sainte-Anne | **8** | `non_detailed` · `ignored` |
| **Hors pack** | Pâtes de manioc Mayotte | **9** | `pack_ok=False` |

> Vérifier config avant observation :
> ```bash
> docker exec -i sandbox-odoo19-odoo-1 odoo shell -d ckr-marketone-01 --no-http <<'PY'
> for tid in (7, 8):
>     p = env['product.template'].browse(tid)
>     print(tid, p.display_name, p.pack_type, p.pack_component_price)
> PY
> ```

---

## Périmètre observation

| Inclus | Exclu |
|--------|-------|
| Processus **BO** : vente → stock → prépa → facture | Checkout eCommerce **detailed** (#229) |
| Comparatif pack **7** vs pack **8** | Généralisation catalogue |
| Lisibilité et retours **métier** équipes | Modification Marketone |
| Smoke front porte pack *(non-régression 6.3b)* | Réouverture lot **6.3b** |

---

## Grille d’observation MOA

Pour chaque scénario : exécuter d’abord sur **pack 7**, puis **pack 8** (même quantité, même client test).

| # | Domaine | Action observateur | Points à noter | Pack 7 | Pack 8 | Retour MOA |
|---|---------|-------------------|----------------|--------|--------|------------|
| **O1** | **Commande** | Créer devis · 1 unité | Pack 7 = **6 lignes** · pack 8 = **1 ligne** | ☑ | ☑ | Fait technique |
| **O2** | **Lignes composants** | Ouvrir lignes SO | Pack 7 = 5 composants visibles à **0 €** · pack 8 = aucune ligne composant | ☑ | ☑ | Fait technique |
| **O3** | **Confirmation** | Confirmer commande | Commandes `sale` · pas d’erreur OCA | ☑ | ☑ | Fait technique |
| **O4** | **Préparation / picking** | Suivre transfert · valider qtés | Pack 7 = **6 moves** · pack 8 = **1 move** · pickings `done` | ☑ | ☑ | Fait technique |
| **O5** | **Stock** | Vérifier impact composants | Pack 7 = moves composants · pack 8 = move pack parent | ☑ | ☑ | Fait technique |
| **O6** | **Facturation** | Facturer commande | Pack 7 = **4,17 €** · pack 8 = **25,00 €** · pas de double comptage | ☑ | ☑ | Fait technique |
| **O7** | **Lisibilité BO** | Recueillir avis utilisateur | Ventes · logistique · compta — compréhension immédiate | ☐ | ☐ | À compléter métier |
| **O8** | **Intérêt métier** | Synthèse comparative | **`detailed` apporte-t-il un gain réel vs `non_detailed` ?** | ☐ | — | À arbitrer MOA |

### Attendus de référence *(recette Phase B)*

| Pack | Attendu technique |
|------|-------------------|
| **7** | 6 lignes SO · picking multi-moves · facture ≈ prix parent · composants 0 € |
| **8** | 1 ligne SO · picking pack · facture ligne unique |

---

## Smoke front *(non-régression 6.3b — pas d’observation checkout detailed)*

| # | Action | Attendu | MOA |
|---|--------|---------|-----|
| **F1** | `/shop?marketone_mode=pack` | Porte Kits · packs **7** + **8** visibles | ☑ |
| **F2** | `/kits` | Redirection vers porte pack | ☑ |
| **F3** | Panier pack **8** | **1 ligne** | ☑ |

Lot **6.3b front** : **non rouvert** — smoke uniquement.

---

## Fiche retour MOA *(à compléter en fin de pilote)*

### Synthèse qualitative

| Question | Réponse MOA |
|----------|-------------|
| Le **`detailed`** sur pack **7** améliore-t-il la lecture métier ? | |
| La préparation composants est-elle **utile** ou **pénalisante** ? | |
| La facturation reste-t-elle **claire** pour la compta ? | |
| Par rapport au témoin **8**, le gain justifie-t-il une extension ? | |
| Réserve perf sandbox (tests auto 12 s) : bloquante pour prod ? | |

### Verdict sortie pilote — **MOA 2026-06-08**

| Option | Verdict |
|--------|---------|
| **A — Maintien pilote seul** (pack 7 `detailed`) | ☐ |
| **B — Extension limitée** | ☐ |
| **C — GO généralisation catalogue** | ☐ **NON** |
| **D — Doctrine `non_detailed` catalogue CK** | ☑ **Retenu** — pack **8** = cible métier · pack **7** = preuve technique |

**Décision** : [`DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md`](./DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md) — **pack = article** · **`sale_product_pack` veille technique**.

---

## Durée et responsabilités

| Élément | Proposition MOA |
|---------|-----------------|
| **Durée observation** | À fixer MOA *(ex. 2–4 semaines usage BO encadré)* |
| **Observateurs** | MOA · ventes · logistique · compta *(selon disponibilité)* |
| **Environnement** | Sandbox **`ckr-marketone-01`** |
| **Extension prod pack 7** | **GO MOA distinct** — hors pilote sandbox initial |
| **Activation prod globale** | **NO GO** tant que non arbitré |

---

## Non-régression automatisée *(optionnelle en fin de pilote)*

```bash
docker exec sandbox-odoo19-odoo-1 odoo -d ckr-marketone-01 \
  --test-tags=dorevia_marketone_lot6_3b_pack \
  --stop-after-init --http-port=0
```

Attendu fonctionnel : **13/13 OK** · réserve perf sandbox documentée si timeouts HTTP.

---

## Références

- [`DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md`](./DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md)
- [`ARBITRAGE_MOA_POST_PHASE_B_SALE_PRODUCT_PACK.md`](./ARBITRAGE_MOA_POST_PHASE_B_SALE_PRODUCT_PACK.md)
- [`RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md`](../recette/maintenance/RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md)
