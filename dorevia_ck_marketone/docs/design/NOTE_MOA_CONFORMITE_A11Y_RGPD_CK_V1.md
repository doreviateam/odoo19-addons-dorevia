# Note MOA — Conformité accessibilité, RGPD et droit de la consommation · V1

| Champ | Valeur |
|-------|--------|
| **Projet** | `dorevia_ck_marketone` · C-Kreyol / CK |
| **Demande MOA** | « Disposer d'une solution totalement conforme pour le commerce en France et en Europe, avec la meilleure expérience utilisateur possible. » |
| **Date** | 2026-06-19 |
| **Statut** | **Clôturée** — décision MOA actée dans [`ACTE_MOA_RESERVE_DONNEES_LEGALES_CK_V1.md`](./ACTE_MOA_RESERVE_DONNEES_LEGALES_CK_V1.md) |
| **Détail technique** | [`RECETTE_CONFORMITE_A11Y_RGPD_CK_V1.md`](./RECETTE_CONFORMITE_A11Y_RGPD_CK_V1.md) |

```text
8 corrections livrées et vérifiées sur l'instance de recette.
0 régression introduite.
1 point reste entièrement entre les mains de la MOA : les informations légales de l'entreprise.
```

---

## 1. Ce qui a été audité

Un audit complet a été mené sur trois volets de conformité, en réponse à l'objectif MOA de disposer d'un site totalement conforme et offrant la meilleure expérience possible :

1. **Accessibilité** (RGAA/WCAG — obligations renforcées pour l'e-commerce en Europe depuis 2025) ;
2. **RGPD** (gestion des données personnelles, consentement, cookies) ;
3. **Droit de la consommation** (mentions légales, CGV, droit de rétractation, affichage des prix).

## 2. Ce qui a été corrigé (livré et vérifié)

| Sujet | Avant | Après |
|---|---|---|
| **Carrousel d'images d'accueil** | Défilement automatique sans moyen de l'arrêter au clavier ou sur mobile/tablette | Bouton pause/lecture ajouté, utilisable au clavier et au tactile |
| **Formulaires (contact, demande professionnelle)** | Bouton d'envoi non activable avec la touche Espace au clavier | Bouton standard, pleinement accessible au clavier |
| **Champs obligatoires des formulaires** | L'astérisque seul n'est pas annoncé clairement par les lecteurs d'écran (utilisés par les personnes malvoyantes) | Mention « obligatoire » ajoutée pour ces technologies d'assistance |
| **Indicateur visuel au clavier** | Sur certains liens, seul un changement de couleur (insuffisant pour les personnes malvoyantes) | Contour visible ajouté |
| **Formulaires de contact / pro** | Aucune mention sur l'usage des données saisies | Phrase + lien vers la politique de confidentialité ajoutés directement sous chaque formulaire |
| **Inscription newsletter** | Mention RGPD présente mais sans lien direct | Lien direct vers la politique de confidentialité ajouté |
| **Conditions générales de vente** | Droit de rétractation mentionné, mais sans le formulaire type que la loi impose de fournir | Formulaire de rétractation officiel ajouté sur la page CGV |
| **Robustesse technique** | Une classe technique était dupliquée à deux endroits (sans impact visible, mais source de confusion pour la maintenance) | Nettoyé |

Un point supplémentaire a été vérifié en détail (mécanisme d'ajout des liens « Mentions légales / Confidentialité / CGV » en pied de page) : il s'est révélé déjà solide, aucune correction n'était nécessaire.

## 3. Ce qui reste à décider par la MOA — bloquant pour une publication publique

Les pages **Mentions légales**, **CGV** et **Politique de confidentialité** existent et sont complètes dans leur structure. Mais elles contiennent des informations d'entreprise **fictives**, clairement signalées comme telles dans le contenu lui-même (un bandeau d'avertissement s'affiche actuellement en haut de ces pages) :

| Information manquante | Exemple actuel (fictif) |
|---|---|
| Adresse du siège | « 12 rue Example, 44000 Nantes » |
| Numéro SIREN / RCS | « 123 456 789 » |
| Numéro de TVA intracommunautaire | « FR 12 123456789 » |
| Téléphone | placeholder |
| Médiateur de la consommation (obligatoire en France) | non désigné |
| Frais de retour, délais de livraison précis | « à préciser » |

```text
Ces informations ne peuvent pas être produites par le développement — elles dépendent de
décisions/données propres à l'entreprise (statut juridique, adresse officielle, médiateur
de la consommation choisi, etc.). Tant qu'elles ne sont pas renseignées, le site ne doit
pas être ouvert au public.
```

**Action demandée à la MOA** : fournir ces informations (ou désigner qui doit les fournir) afin que le développement puisse les intégrer avant toute ouverture publique du site.

> **Mise à jour 2026-06-19** — la MOA a acté la mise en réserve de ce point : voir [`ACTE_MOA_RESERVE_DONNEES_LEGALES_CK_V1.md`](./ACTE_MOA_RESERVE_DONNEES_LEGALES_CK_V1.md). Le lot conformité reste GO et n'est pas rouvert ; les données réelles feront l'objet d'un lot d'injection dédié, sans nouveau développement, le moment venu.

## 4. Ce qui n'a pas été touché

Un chantier indépendant, déjà en cours côté développement avant cette intervention (gestion des prix et des produits mis en avant), a été identifié comme contenant des éléments non finalisés. Il n'est ni la cause ni la conséquence de ce lot de corrections et continue son cours séparément.

## 5. Verdict

```text
GO — corrections accessibilité / RGPD / droit de la consommation déployées et vérifiées.
EN ATTENTE — décision MOA sur les informations légales réelles avant toute ouverture publique.
```

---

*Note MOA — conformité a11y/RGPD/droit de la consommation · 2026-06-19.*
