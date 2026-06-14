# Tokens design — Maquette CK V1

| Champ | Valeur |
|-------|--------|
| **Ticket** | `ticket_dev_maquette_01_open_design` |
| **Référence** | `design_01.md` v1.1 |
| **Statut** | Maquette V1 — démonstration, pas DA finale |
| **Artefact** | `/Users/doreviateam/open-design/.od/projects/ck-marketone-maquette-v1/index.html` |

---

## Direction retenue

Palette **marchande alimentaire** : lumineuse, chaude, orientée produit — sans reprise terracotta/sauge/pastel premium ni `warm-editorial`.

---

## Couleurs

| Token | Valeur | Usage |
|-------|--------|-------|
| `--ck-bg` | `#FFFBF7` | Fond page |
| `--ck-bg-soft` | `#F5F0E8` | Zones secondaires, sidebar |
| `--ck-surface` | `#FFFFFF` | Cartes, header |
| `--ck-text` | `#1C1917` | Texte principal |
| `--ck-text-muted` | `#57534E` | Métadonnées, légendes |
| `--ck-border` | `#E7E0D5` | Bordures |
| `--ck-primary` | `#D84315` | CTA principal, accents achat |
| `--ck-primary-hover` | `#BF360C` | Hover CTA |
| `--ck-secondary` | `#2E7D4F` | Origines, badges confiance |
| `--ck-secondary-soft` | `#E8F5E9` | Fond badge origine |
| `--ck-price` | `#1C1917` | Prix (lisibilité max) |
| `--ck-badge-new` | `#F9A825` | Badge nouveauté |
| `--ck-badge-pack` | `#6D4C41` | Badge pack / coffret |
| `--ck-pro` | `#455A64` | Entrée professionnels |
| `--ck-image-zone` | `#FAF6F0` | Zone photo produit (aplats) |

**Règle** : aplats uniquement sur zones produit — pas de dégradés décoratifs sur les tuiles.

---

## Typographies

| Rôle | Police | Fallback | Poids |
|------|--------|----------|-------|
| Display / titres | `Fraunces` | Georgia, serif | 600–700 |
| UI / corps | `DM Sans` | system-ui, sans-serif | 400–600 |
| Prix | `DM Sans` | — | 700 |

Chargement : Google Fonts (maquette uniquement — à arbitrer pour prod Odoo).

---

## Échelle typographique

| Token | Taille | Usage |
|-------|--------|-------|
| `--text-xs` | 12px | Badges, métadonnées |
| `--text-sm` | 14px | Labels, filtres |
| `--text-base` | 16px | Corps |
| `--text-lg` | 18px | Sous-titres |
| `--text-xl` | 22px | Titres section |
| `--text-2xl` | 28px | Hero secondaire |
| `--text-3xl` | 36px | Hero principal (desktop) |
| `--text-hero-mobile` | 28px | Hero mobile |

Line-height corps : `1.5` — titres : `1.2`.

---

## Espacements

| Token | Valeur |
|-------|--------|
| `--space-1` | 4px |
| `--space-2` | 8px |
| `--space-3` | 12px |
| `--space-4` | 16px |
| `--space-5` | 24px |
| `--space-6` | 32px |
| `--space-7` | 48px |
| `--space-8` | 64px |

Conteneur max : `1200px`. Gouttières : `24px` desktop, `16px` mobile.

---

## Radius & ombres

| Token | Valeur | Usage |
|-------|--------|-------|
| `--radius-sm` | 6px | Chips, badges |
| `--radius-md` | 10px | Boutons, inputs |
| `--radius-lg` | 14px | Cartes produit |
| `--shadow-card` | `0 2px 12px rgba(28,25,23,0.06)` | Cartes au repos |
| `--shadow-card-hover` | `0 8px 24px rgba(28,25,23,0.10)` | Hover carte |

---

## Grille responsive

| Breakpoint | Grille `/shop` | Sidebar filtres |
|------------|----------------|-----------------|
| `< 768px` | 1 col (2 si ≥480px) | Drawer / accordéon |
| `768px – 1023px` | 2–3 cols | Panneau repliable |
| `≥ 1024px` | 3–4 cols | Sidebar fixe |

Header mobile : compact, menu burger pour nav secondaire.

---

## Export SCSS (cible Odoo future)

```scss
// Préfixe suggéré : $ck-
$ck-bg: #FFFBF7;
$ck-primary: #D84315;
$ck-secondary: #2E7D4F;
$ck-text: #1C1917;
$ck-radius-lg: 14px;
// … mapping complet depuis :root de l’artefact HTML
```
