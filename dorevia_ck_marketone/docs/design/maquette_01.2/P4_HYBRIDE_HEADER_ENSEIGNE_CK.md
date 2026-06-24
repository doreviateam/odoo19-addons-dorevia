# P4 hybride — Header enseigne CK (livré)

| Champ | Valeur |
| --- | --- |
| Date | 2026-06-23 |
| Périmètre | Arbitrage MOA suite à `P4_AUDIT_HEADER_ENSEIGNE_CK.md` — intensité piste A, logo piste B, mega-menu éditorial gouverné en BO, bandeau de preuves corrigé |
| Modules | `dorevia_ck_theme` **19.0.1.46.0** · `dorevia_ck_marketone_content` **19.0.1.31.0** |
| Statut | **Implémenté et conservé** (contrairement aux pistes A/B de l'audit, qui ont été retirées après captures) |

---

## 1. Ce qui a été fait, point par point sur la demande Dev

| Demande | Réalisé |
| --- | --- |
| 1. Header desktop, présence enseigne renforcée | Plaque N2/N3 unifiée (teinte `$ck-bg-soft` sur tout le header, séparateur N2/N3 retiré) — **desktop ≥992px uniquement** |
| 2. Logo sans macaron, plus signé | Wordmark agrandi (1.3125rem → 1.4375rem) + trait d'accent terracotta sous la baseline. Aucun macaron. |
| 3. Mega-menu visuel éditorial maîtrisé | Nouveau modèle BO `ck.mega.menu.rayon.visual` — voir §2 |
| 4. Bandeau de preuves proprement composé | Reconstruit en mini-pills (fond, padding, puce) — voir §3 |
| 5. Mobile fermé inchangé ou non dégradé | Vérifié : fond header mobile toujours blanc (`rgb(255,255,255)`), seul ajout = le même trait d'accent logo (mobile-safe, déjà validé en piste B) |

---

## 2. Note de gouvernance — gestion du visuel de rayon

### Le problème identifié par la MOA

La piste A de l'audit utilisait une photo produit **codée en dur dans le Python** (`nav_mega_menu.py`) — pas une sélection automatique au sens algorithmique, mais un choix que seul un déploiement Dev pouvait changer. La MOA a explicitement écarté cette approche : *« ne pas choisir automatiquement un produit publié comme visuel par défaut sans contrôle MOA/BO »*.

### Solution retenue

Nouveau modèle **`ck.mega.menu.rayon.visual`** (fichier `models/ck_mega_menu_rayon_visual.py`), distinct de `ck.mega.menu.visual.block` :

| | `ck.mega.menu.visual.block` (existant) | `ck.mega.menu.rayon.visual` (nouveau) |
| --- | --- | --- |
| Rôle | Campagne commerciale datée | Identité visuelle permanente du rayon |
| Champs dates | `date_start` / `date_end` | Aucun — pas une campagne |
| Lien commercial | `target_url` + `cta_label` | Aucun — pas un CTA d'achat |
| Qui l'édite | Équipe contenu, via BO (`Site Web > Configuration > Blocs visuels mega-menu`) | Équipe contenu, via BO (`Site Web > Configuration > Visuels rayon mega-menu (identité)`) |

**Priorité d'affichage dans le mega-menu** (`_visual_column`, `nav_mega_menu.py`) :

1. Campagne active (`ck.mega.menu.visual.block`) si une existe pour ce rayon — inchangé, prioritaire.
2. **Visuel d'identité du rayon** (`ck.mega.menu.rayon.visual`) si curaté en BO — nouveau.
3. Carte de marque texte seul (aucune image) — filet de sécurité si rien n'est saisi.

Le formulaire BO du nouveau modèle porte un avertissement explicite : *« Ce visuel illustre le rayon (ambiance, territoire, sélection) — il ne doit pas représenter un produit unique présenté comme emblématique du rayon entier. »* Le titre/sous-titre affichés restent toujours éditoriaux (nom du rayon, jamais le nom du produit utilisé comme image).

### Sur les visuels actuellement en place

Pour produire les captures demandées, deux enregistrements ont été créés via une migration (`migrations/19.0.1.31.0/post-migrate.py`) en réutilisant **une seule fois**, comme point de départ, une photo produit déjà publiée (Épicerie : confiture de goyave · Boissons : jus Mont-Pelé). Ce n'est :

- **ni** un choix automatique au rendu (c'est une donnée BO statique, modifiable à tout moment dans l'interface) ;
- **ni** un enfermement définitif (un membre de l'équipe contenu peut remplacer l'image et le texte sans intervention Dev, dès maintenant).

**Mais ce sont des placeholders de démonstration**, pas le résultat d'un brief photo validé. Avant un GO MOA final sur cet axe, il faudra trancher : photo de territoire, mise en scène éditoriale, illustration — et fournir (ou faire produire) les visuels définitifs par rayon.

---

## 3. Bandeau de preuves — correctif

**Problème constaté** (piste B, audit P4) : les trois preuves s'affichaient à la suite sans séparation visible.

**Correctif :** chaque preuve est désormais une pill indépendante (fond `rgba(primary, 0.07)`, padding, radius, puce ronde terracotta), avec un espacement garanti entre pills (`gap`) qui ne dépend plus uniquement de l'espacement inter-mots. Vérifié par mesure DOM réelle (pas seulement visuel) : les trois pills ont des rectangles disjoints avec un espace mesuré de 8px entre chaque.

---

## 4. Vérifications effectuées (pas seulement supposées)

- Teinte plaque desktop : `getComputedStyle` → `rgb(245, 240, 232)` (= `$ck-bg-soft`) à 1280px.
- Fond header mobile : `getComputedStyle` → `rgb(255, 255, 255)` à 390px — confirmé non dégradé.
- Image du visuel rayon : vérifiée servie correctement (`Content-Type: image/webp`, 181 Ko) après un faux positif initial dû à un cache de registre Odoo resté sur l'ancien état (corrigé par redémarrage du serveur — nouveau modèle non reconnu par le worker HTTP avant rechargement complet).
- Pills du bandeau de preuves : rectangles DOM mesurés, espacement réel confirmé (pas de chevauchement).

---

## 5. Captures

Dossier : `captures/recette_header_v22/p4_hybride/`

| Fichier | Contenu |
| --- | --- |
| `desktop_initial.png` | Header au chargement — plaque N2/N3, logo signé |
| `mega_epicerie.png` | Épicerie (seed pauvre) — visuel rayon BO + bandeau de preuves |
| `mega_boissons.png` | Boissons — visuel rayon BO + bandeau de preuves |
| `mobile_ferme.png` | Mobile chrome fermé — non dégradé vs P3 |

---

## 6. Prochaine étape

GO MOA sur cette base, ou ajustements ciblés avant validation finale. Point en suspens identifié par ce document : remplacer les 2 visuels placeholder par des visuels de rayon définitifs (brief à cadrer avec la MOA/Contenu).
