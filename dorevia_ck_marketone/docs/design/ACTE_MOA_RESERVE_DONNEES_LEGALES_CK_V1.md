# Acte MOA — Mise en réserve des données légales CK · V1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` · C-Kreyol / CK |
| **Objet** | Mise en réserve des contenus légaux réels |
| **Date** | 2026-06-19 |
| **Statut** | **Acté MOA** |
| **Impact** | Aucun blocage technique · blocage publication publique légale maintenu |
| **Références** | [`NOTE_MOA_CONFORMITE_A11Y_RGPD_CK_V1.md`](./NOTE_MOA_CONFORMITE_A11Y_RGPD_CK_V1.md) · [`RECETTE_CONFORMITE_A11Y_RGPD_CK_V1.md`](./RECETTE_CONFORMITE_A11Y_RGPD_CK_V1.md) |
| **Modules (lot conformité)** | `dorevia_ck_theme` **19.0.1.36.14** · `dorevia_ck_marketone_content` **19.0.1.25.33** |

```text
GO technique conformité — lot livré et conservé.
NO GO publication publique /legal /terms /privacy tant que données réelles absentes.
Poursuite des lots fonctionnels non bloquée.
Données légales réelles → lot dédié ultérieur (injection contenus), sans refonte structurelle.
```

---

## 1. Décision MOA

La MOA confirme ne pas être prête à fournir les **données légales réelles** de l’entreprise exploitant CK.

Les pages `/legal`, `/terms` et `/privacy` restent **techniquement disponibles**, mais ne doivent **pas** être considérées comme publiables en l’état si elles contiennent des données fictives, génériques ou incomplètes.

**Consigne Dev :** ne pas compléter, enrichir ni « polir » les données légales fictives. Ne pas rouvrir le lot conformité accessibilité / RGPD / rétractation.

---

## 2. État du lot conformité

Le lot conformité accessibilité / RGPD / rétractation est considéré comme **livré côté technique**.

Les corrections apportées restent **utiles et conservées** :

- accessibilité (carrousel, formulaires, focus, champs obligatoires) ;
- structure RGPD (mentions + liens `/privacy`) ;
- mentions et formulaire de rétractation sur `/terms` ;
- liens footer légaux ;
- pages légales structurées (coquilles prêtes) ;
- mécanisme de propagation par snapshot / `bootstrap_*_page`.

**Verdict technique :** GO — mergeable (cf. recette dev : 39/39 tests périmètre conformité, 0 régression introduite).

---

## 3. Réserve maintenue

La réserve suivante reste **ouverte** :

> Les données légales réelles de l’entreprise exploitant CK ne sont pas encore fournies par la MOA.

| Effet | Portée |
|-------|--------|
| **Bloque** | Publication publique juridique des pages `/legal`, `/terms`, `/privacy` |
| **Ne bloque pas** | Poursuite des travaux fonctionnels, UI, catalogue, fiche produit, home, shop, blog, contenus éditoriaux, back-office |

---

## 4. Conséquence projet

Le projet peut continuer sur les lots suivants, à condition de maintenir explicitement le statut suivant :

| Statut | Décision |
|--------|----------|
| Conformité technique | **GO** |
| Publication publique légale | **NO GO** |
| Données légales réelles | **En attente MOA** |

---

## 5. Lot futur — injection contenus légaux (hors périmètre actuel)

Lorsque la MOA fournira les informations réelles (raison sociale, SIRET, siège, contact DPO, hébergeur, etc.), un **lot dédié d’injection contenus légaux** pourra :

- alimenter les pages existantes via les fonctions `bootstrap_*_page` déjà en place ;
- rejouer les snapshots concernés (même procédure que le lot conformité — cf. recette dev §2) ;
- retirer les bandeaux d’avertissement « contenu fictif » le cas échéant.

**Aucune refonte structurelle** des pages légales, du footer ou du mécanisme bootstrap n’est attendue à ce stade.

---

## 6. Prochaine action recommandée

- **Ne pas** demander au Dev de compléter les données légales fictives.
- **Conserver** les pages légales comme structure prête à recevoir les vraies informations plus tard.
- **Prioriser** les prochains lots CK non dépendants de l’identité juridique réelle.

---

*Acte MOA · réserve données légales CK · clôture décision ouverte dans NOTE_MOA_CONFORMITE · V1.*
