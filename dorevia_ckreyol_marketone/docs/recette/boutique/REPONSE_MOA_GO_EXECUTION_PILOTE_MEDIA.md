# Réponse MOA — GO exécution pilote média catalogue

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-20 |
| **Ticket** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) |
| **Décision** | **GO exécution pilote média** |
| **Volume** | **50 SKU** |
| **Recette** | `ck_shop_tile_v1.1` |
| **Périmètre** | Tuiles commerce `/shop` uniquement |

---

## Contrôles MOA pré-exécution

| Contrôle | Résultat |
|----------|----------|
| Fichiers dans `tools/ck_image_normalizer/input/pilote/` | **50** |
| Lignes de données dans `manifest.pilote.csv` | **50** |
| Correspondance manifest → fichiers | **OK** |
| Profils valides (`packshot` / `lifestyle`) | **OK** |
| Répartition profils | **38 packshot · 12 lifestyle** |
| Code Odoo demandé | **Non** |
| Remplacement `image_1920` demandé | **Non** |
| Industrialisation automatique | **Non** |

---

## Signal MOA

```text
GO exécution pilote média — 50 SKU sélectionnés — manifest prêt
```

Le batch CLI peut être lancé sur :

```text
tools/ck_image_normalizer/input/pilote/
tools/ck_image_normalizer/manifest.pilote.csv
```

avec la recette :

```text
recipes/ck_shop_tile_v1.1.yaml
```

---

## Suite attendue

Le run pilote doit produire :

- rapport JSON / CSV ;
- WebP + JPEG ;
- previews avant / après ;
- grille de contrôle desktop / mobile si disponible ;
- synthèse des statuts `OK`, `OK_WITH_WARNINGS`, `NEEDS_REVIEW`, `REJECTED`.

Décision post-run attendue :

```text
GO pilote exploitable
GO avec réserves
NO GO / pause
```

---

## Post-exécution (2026-05-20)

Batch **`pilote_20260520`** terminé.

| Statut | Nombre |
|--------|-------:|
| OK | 18 |
| OK_WITH_WARNINGS | 3 |
| NEEDS_REVIEW | 29 |
| REJECTED | 0 |

**Décision provisoire MOA** : ~~pas de GO exploitation~~ → **GO pilote avec réserves** (P4 clôturé).

→ [`RAPPORT_P4_PILOTE_MEDIA_50SKU_20260520.md`](./RAPPORT_P4_PILOTE_MEDIA_50SKU_20260520.md)
