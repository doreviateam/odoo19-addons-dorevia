# Réception MOA — Phase B `sale_product_pack` · lexique GO et prochaine marche

| Champ | Valeur |
|-------|--------|
| **Date réception** | 2026-06-08 |
| **Ticket** | [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md) |
| **Décision MOA** | [`DECISION_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](./DECISION_MOA_PHASE_B_SALE_PRODUCT_PACK.md) |
| **Atelier** | [`ATELIER_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](./ATELIER_MOA_PHASE_B_SALE_PRODUCT_PACK.md) — clôturé |
| **Recette BO** | [`RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md`](../recette/maintenance/RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md) |
| **Verdict** | **Clôturé MOA** — **GO doctrine `non_detailed`** · `sale_product_pack` **veille technique** |
| **Doctrine pack CK** | [`DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md`](./DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md) |
| **Pilote contrôlé** | [`DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md`](./DECISION_MOA_PILOTE_CONTROLE_SALE_PRODUCT_PACK.md) |
| **Cadre observation** | [`CADRE_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md`](./CADRE_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md) |
| **Exécution observation** | [`NOTE_EXECUTION_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md`](./NOTE_EXECUTION_OBSERVATION_PILOTE_PACK7_SALE_PRODUCT_PACK.md) |

---

## Réponse MOA

Position MOA **confirmée** sur la Phase B `sale_product_pack`.

```text
Odoo exécute. Marketone habille et oriente.
Aucun moteur Odoo remplacé.
```

---

## Lexique GO — validé MOA

| Niveau | Signification | Statut |
|--------|---------------|--------|
| **1. GO lancement recette BO** | Autorisation d’**exécuter** la recette après merge PR #1 | ☑ **Exécuté** |
| **2. GO recette BO** | Validation de la grille **B1–B6** après exécution et signature | ☑ **Avec réserve perf sandbox** |
| **3. GO activation prod** | Décision distincte, post-recette, après arbitrage pilote / généralisation | ☐ **NO GO** |
| **4. GO pilote contrôlé** | Observation métier encadrée pack **7** avant généralisation | ☑ **Accordé** |
| **5. GO généralisation** | Bascule `detailed` catalogue pack CK | ☑ **NON** — doctrine `non_detailed` |
| **6. Doctrine pack CK** | Pack = article · `non_detailed` cible | ☑ **GO MOA** |

---

## État confirmé

| Point | Statut |
|-------|--------|
| Lot **6.3a** Promo | **Clôturé MOA** |
| Lot **6.3b** Kits & Coffrets | **Clôturé MOA** |
| Phase B ne rouvre **pas** le front 6.3b | ✓ |
| **Marketone** inchangé · pas de nouveau `depends` · pas de moteur pack | ✓ |
| PR plateforme [#1](https://github.com/doreviateam/odoo19-addons-oca/pull/1) | **MERGED** `789fda8` |
| Sandbox plateforme | Chaîne `sale_product_pack` + `stock_product_pack` + `sale_stock_product_pack` installée |
| Prep Phase B | Doctrine cible : packs **7**/**8** **`non_detailed`** · pack **8** = référence métier |
| Smoke Dev B1–B5 | **OK** rollback — détail [`NOTE_EXECUTION_ETAPE1_PHASE_B_SALE_PRODUCT_PACK.md`](./NOTE_EXECUTION_ETAPE1_PHASE_B_SALE_PRODUCT_PACK.md) |
| Non-régression 6.3b | Fonctionnelle OK · tests auto relancés avec timeouts HTTP 12 s sandbox |
| Activation prod | **NO GO** |
| Recette BO B1–B6 | **Exécutée** — GO avec réserve perf sandbox |

---

## Clôture MOA — doctrine pack = article

**Verdict final** : [`DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md`](./DECISION_MOA_DOCTRINE_PACK_ARTICLE_NON_DETAILED.md)

| # | Action | Statut |
|---|--------|--------|
| 1 | Doctrine **`non_detailed`** — pack = article commercial | ☑ **GO MOA** |
| 2 | **`product_pack`** Marketone maintenu · porte Kits | ✓ |
| 3 | **`sale_product_pack`** veille technique · **NO GO activation CK** | ✓ |
| 4 | Restaurer config catalogue `non_detailed` (packs 7/8) | Voir doctrine doc |

---

## Points non rouverts

| Sujet | Décision maintenue |
|-------|-------------------|
| Front Marketone 6.3b | **Clôturé** — smoke non-régression uniquement |
| `website_sale_product_pack` (#229) | **Hors Phase B** |
| `dorevia_ckreyol_marketone` | **Aucune modification** à ce stade |
| Moteur pack Marketone | **Interdit** |

---

## Verdict réception

| Date | Verdict |
|------|---------|
| 2026-06-08 | ☑ **GO doctrine `non_detailed` packs CK** · ☑ **`sale_product_pack` veille technique** · ☐ **GO activation prod CK** |
