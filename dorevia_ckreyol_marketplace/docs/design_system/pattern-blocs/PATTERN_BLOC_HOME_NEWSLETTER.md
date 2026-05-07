# Pattern-bloc — Home « Newsletter »

Ce document décrit le bloc **Newsletter** de la homepage C-Kreyol comme **captation douce** : inscription simple sans interrompre le parcours marchand principal, ni transformer la Home en tunnel d’acquisition agressif.

Ce n’est pas un ticket d’implémentation : **aucune évolution** de logique emailing, **aucun nouveau système**, **aucun snippet Odoo déposable** n’est prescrit ici — **documentation uniquement**.

**Vocabulaire** : [`../README.md`](../README.md)

---

## 1. Intention produit

Le bloc doit :

- **Proposer une inscription** en un clic (email + envoi), avec libellés **calmes** et lecture rapide au scroll ;
- **Capter l’intérêt** sans concurrencer hero, Explorer ou tunnel panier ;
- Rester **sobre**, **premium**, aligné charte CK — pas de promesse commerciale démesurée ;
- **Ne pas** faire de la Home une page d’acquisition « growth » (popups, multi-champs, pression psychologique).

Position dans le parcours : après les blocs d’orientation et de preuve produit, **conversion douce** pour les visiteurs pas encore prêts à acheter.

---

## 2. Structure attendue

**Source QWeb** : `views/snippets/ckr_circle.xml` (id template `ckr_snippet_circle` — nom historique « circle », rendu = newsletter homepage).

1. **Section** : `ckr-section ckr-section--soft ckr-newsletter`, titre de section accessible via `aria-labelledby="ckr-newsletter-heading"`.
2. **Messages de retour** (affichés si query `cc_nl` présente, voir §3) :
   - **ok** — succès ;
   - **dup** — doublon / déjà inscrit (opt-in actif) ;
   - **invalid** — email invalide ou vide après normalisation ;
   - **err** — échec technique (message générique, pas de trace serveur côté utilisateur).
3. **Copy** : eyebrow « NEWSLETTER », **titre** court (marque affichée ; variante accentuée « C-Kréyòl » possible selon copy).
4. **Formulaire** `POST` :
   - `action="/ckr/circle/subscribe"` ;
   - champ `email` (`type="email"`, `required`, `autocomplete="email"`) ;
   - bouton **S’inscrire** ;
   - champs cachés : **`csrf_token`** (`request.csrf_token()`), **`redirect`** (chemin courant pour revenir sur la même page après traitement).
5. **Mention rassurante** (`#ckr-newsletter-legal`) : usage limité aux nouvelles / sélections / offres, possibilité de désabonnement — liée au champ via `aria-describedby`.

---

## 3. Implémentation actuelle de référence

| Couche | Fichiers / artefacts |
| --- | --- |
| Template | `views/snippets/ckr_circle.xml` |
| Styles | `static/src/scss/components/_newsletter.scss` |
| Contrôleur HTTP | `controllers/ckr_circle.py` |
| Liste de diffusion Odoo | `data/ckr_mailing_list_newsletter.xml` — `mailing.list` **« Newsletter C-Kréyòl »** (`ckr_mailing_list_newsletter_ck`, `is_public`) |
| Tests de non-régression | `tests/test_ckr_circle.py` (tag `dorevia_ckr_circle`) |

### Route POST et flux

- **Route** : `POST /ckr/circle/subscribe`
- Déclaration : `website=True`, `auth="public"`, **`csrf=True`** (protection CSRF native Odoo sur le POST).
- **Pas de rendu HTML d’erreur HTTP « brut »** pour les cas fonctionnels habituels : le contrôleur répond par **redirection HTTP 303** vers l’URL de retour (`redirect` posté, validée par `_ckr_safe_redirect_path` : chemin relatif commençant par `/`, pas d’open redirect `//`).
- **Paramètre de retour** : `cc_nl` dans la query (`ok` | `dup` | `invalid` | `err`). Le template relit `request.httprequest.args.get('cc_nl')` pour afficher le message adapté.

### Lien avec `mass_mailing`

L’inscription homepage **alimente la liste** `mailing.list` **Newsletter C-Kréyòl** via :

- résolution de la liste par **xmlid** `dorevia_ckreyol_marketplace.ckr_mailing_list_newsletter_ck` (repli recherche par nom si besoin) ;
- création / mise à jour **`mailing.contact`** et **`mailing.subscription`** dans `_ckr_subscribe_mailing_list` (gestion **opt_out** réactivé si contact existait désabonné).

Les tests HTTP vérifient la présence du **`mailing.contact`** et son appartenance à la liste.

### Modèle `ckr.circle.subscriber`

Un modèle **`ckr.circle.subscriber`** existe toujours dans le module (normalisation email, token désinscription, contraintes site) et est utilisé notamment par la route **désinscription** `/ckr/circle/unsubscribe/<token>`. **Le POST newsletter homepage documenté ici ne persiste pas dans ce modèle** : la source de vérité d’inscription front pour la liste éditoriale est **`mass_mailing`** comme ci-dessus. Ne pas fusionner les deux dans la doc produit sans ticket d’alignement explicite.

### Gestion des cas

| Cas | Comportement |
| --- | --- |
| Email vide / invalide après normalisation | Redirection `cc_nl=invalid` |
| Déjà inscrit (abonnement actif à la liste) | `cc_nl=dup` |
| Réinscription après opt-out | Traité comme succès côté liste (`ok`) |
| Exception technique | Log serveur + `cc_nl=err` (message utilisateur générique) |

Cela évite d’exposer une **500** au visiteur pour les chemins couverts par le contrôleur (les tests couvrent succès, invalide, doublon).

---

## 4. Règles responsive

Implémentation : `_newsletter.scss`.

- **Mobile** : formulaire en **colonne** — champ pleine largeur, bouton **pleine largeur** sous le champ (`ckr-newsletter__row` en `flex-direction: column`), zone tactile confortable (padding bouton / input).
- **≥ 768px** : disposition **horizontale** — copy à gauche (largeur max ~28rem), formulaire à droite avec champ + bouton sur **une ligne** ; marge haute du formulaire alignée optiquement avec la promesse.
- **Messages** : bloc `ckr-newsletter__messages` avec espacement vertical ; couleurs distinctes ok / info / erreur pour lecture immédiate sans casser la grille.
- **Hauteur globale** : section en `ckr-section--soft` ; padding bas du bloc newsletter **modéré** et **réduction du padding-top de la section suivante** (« En pratique ») via sélecteur adjacent `.ckr-newsletter + .ckr-section` — évite un empilement trop lourd après le bloc légal RGPD.

---

## 5. GO / NO GO

### GO

- Inscription **compréhensible** en un coup d’œil ; formulaire utilisable au clavier ; **messages de retour** clairs (**ok**, **doublon**, **invalide**, **erreur générique**).
- **CSRF** présent ; **redirect** sécurisé (pas de fuite vers domaine externe).
- Pas d’erreur serveur exposée comme page 500 pour les cas nominaux invalides/doublon (redirection avec `cc_nl`).
- Alignement fonctionnel avec **Odoo Email Marketing** (liste **`mailing.list`** + **`mailing.contact`**).

### NO GO

- Promesses marketing **excessives** ou collecte intrusive (champs multiples non justifiés).
- Formulaire dominant la Home ou **spam visuel**.
- Messages d’**erreur technique** compréhensibles uniquement par un dev ou stack trace exposée au public.
- Bloc **trop dense** en mobile : petits champs, CTA microscopic, légal illisible.
- **Absence totale de feedback** après soumission (`cc_nl` non géré ou query ignorée).

---

## 6. Points de vigilance

- **Ne pas rouvrir** la logique newsletter dans une passe cosmétique : tout changement de route, de persistance ou de liste = **ticket** + mise à jour des **tests** `test_ckr_circle.py`.
- **Ne pas créer** de second pipeline d’emailing parallèle : rester sur **`mass_mailing`** pour la liste éditoriale **Newsletter C-Kréyòl**.
- Garder **`csrf_token`** et la validation **`redirect`** si le formulaire évolue.
- Harmoniser au besoin copie FR **marque** (C-Kreyol technique vs C-Kréyòl affiché) avec les assertions de tests existantes (regex **`C-K(?:reyol|réyòl)`** sur la ligne de promesse newsletter).
- **Snippet Odoo déposable** : hors périmètre ; le bloc est assemblé par `t-call` homepage.
- Cohérence **accessibilité** : label réel masqué visuellement (`ckr-newsletter__label-vh`), `aria-describedby` vers le paragraphe légal, `aria-invalid` sur le champ lorsque `cc_nl=invalid`.

---

## Statut du document

**Créé** — décrit le comportement **tel que livré** (template, SCSS, contrôleur, liste `mailing.list`, paramètre `cc_nl`) comme **pattern-bloc UX** et **référence de recette**, sans modifier le code.
