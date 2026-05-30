# Audit code Odoo — `dorevia_glc_analytics`

Date : 2026-05-30  
Module audité : `dorevia_glc_analytics`  
Version manifest initiale lue : `19.0.14.1.0`  
Version après correctif Lot A : `19.0.14.1.1`  
Version après correctif Lot A suite : `19.0.14.1.2`
Version après correctif Lot B perf initial : `19.0.14.2.0`
Version après correctif Lot B suite : `19.0.14.2.1`
Version après correctif Lot C périmètre analytique : `19.0.14.3.0`
Version après correctif Lot D UX / sémantique : `19.0.14.4.0`
Type d'audit : audit statique expert Odoo, orienté développeur.

## 1. Verdict synthétique

**Verdict : GO fonctionnel avec réserves techniques à traiter avant montée en volume.**

Le module est cohérent fonctionnellement : il consolide la nomenclature analytique GLC, expose un cockpit de contrôle de gestion, sépare correctement exploitation / trésorerie / qualité / paiements, et documente bien la doctrine métier récente.

La principale réserve concerne la robustesse industrielle du cockpit : le calcul repose encore beaucoup sur des recherches Odoo répétées, des filtrages Python et des garde-fous silencieux. C'est acceptable en sandbox et en petite volumétrie, mais il faut durcir avant usage réel avec un historique comptable dense.

## 2. Périmètre audité

Fichiers principaux relus :

- `__manifest__.py`
- `models/glc_coverage_cockpit.py`
- `models/glc_quality_mixin.py`
- `models/glc_coverage_cockpit_quality.py`
- `models/glc_analytic_anomaly_wizard.py`
- `models/account_analytic_account.py`
- `models/res_company.py`
- `hooks.py`
- `security/glc_security.xml`
- `security/ir.model.access.csv`
- `views/glc_coverage_cockpit_views.xml`
- `views/glc_menus.xml`
- `static/src/js/glc_coverage_cockpit_form_view.esm.js`
- `static/src/js/glc_coverage_detail_widget.esm.js`
- `static/src/js/glc_coverage_synthesis_widget.esm.js`
- `tests/`
- `migrations/`

Cet audit ne remplace pas un rejeu serveur complet. Il cible la conception, la maintenabilité, les risques Odoo et les demandes d'amélioration pour le développeur.

## 3. Points forts

### 3.1 Architecture métier lisible

Le module a une orientation métier claire :

- nomenclature analytique GLC unique ;
- cockpit exploitation : ressources, cumul RH, dépenses, solde ;
- trésorerie séparée par compte bancaire de référence ;
- contrôles qualité Q1/Q2/Q3 ;
- détail visuel par axe analytique et par mois ;
- mode "Payé uniquement" cantonné au détail.

Le choix de ne pas générer d'écriture comptable ou analytique depuis le cockpit reste sain. Le cockpit est une lecture, pas une couche de production comptable.

### 3.2 Bonne séparation exploitation / trésorerie

Le module distingue correctement :

- les KPI d'exploitation, issus des lignes analytiques et des axes GLC ;
- l'onglet Trésorerie, issu du compte bancaire observé ;
- les virements internes 580 qualifiés analytiquement.

La règle métier "changer le compte bancaire ne modifie pas les KPI exploitation" est bien portée par l'architecture.

### 3.3 Doctrine qualité/paiement bien intégrée

La doctrine Q1 est désormais meilleure que l'ancienne approche par facture : elle mesure les lignes comptables pilotables, y compris les écritures bancaires sans facture.

Q2 et Q3 apportent une réponse pertinente à la question MOA : "combien est non payé, en cours de paiement, payé, lettré ou non lettré ?"

### 3.4 Migrations idempotentes dans l'intention

Les hooks de renommage et de normalisation analytique sont écrits en SQL idempotent. C'est approprié pour corriger des bases sandbox ou historiques qui ont connu plusieurs états de nomenclature.

## 4. Risques et constats prioritaires

### P1 — Vérifier l'import réel des tests récents

Constat : `tests/__init__.py` importe seulement :

- `test_analytic_setup`
- `test_analytic_anomaly`
- `test_coverage_cockpit`

Or plusieurs fichiers de tests importants existent :

- `test_coverage_cockpit_treasury.py`
- `test_coverage_cockpit_quality.py`
- `test_coverage_cockpit_synthesis_document_quality.py`
- `test_coverage_cockpit_detail_paid.py`
- `test_coverage_cockpit_detail_paid_recette.py`

Dans un module Odoo classique, les fichiers de tests doivent être importés par `tests/__init__.py` pour être chargés dans un rejeu standard du module. Si le runner local les lance explicitement par un autre mécanisme, c'est acceptable, mais il faut le prouver.

Demande développeur :

- confirmer que le rejeu standard `-u dorevia_glc_analytics` charge bien tous les fichiers de tests ;
- sinon, importer explicitement tous les fichiers de tests dans `tests/__init__.py` ;
- ajouter cette vérification dans le plan de recette technique.

Impact : risque de faux vert CI / sandbox si seuls les anciens tests sont chargés.

### P1 — Performance cockpit à durcir avant volumétrie réelle

Le calcul cockpit exécute de nombreuses recherches Odoo dans des boucles :

- `_sum_lines()` et `_sum_lines_matching()` font un `search()` puis une somme Python ;
- `_sum_lines_paid()` filtre aussi en Python ;
- `_action_refresh_single()` boucle par mois puis par compte analytique ;
- `_internal_transfer_amounts_for_account()` rappelle `_aggregate_treasury_internal_buckets()` à chaque compte ;
- `_aggregate_quality_analytic()` charge les lignes puis filtre en Python ;
- `_payment_moves()` charge toutes les factures postées de la société puis filtre en Python.

Sur une base réelle avec plusieurs années d'écritures, le cockpit peut devenir lent.

Demande développeur :

- mutualiser les domaines par période ;
- privilégier `read_group`, SQL ciblé ou agrégation par lots ;
- calculer les buckets de virements internes une seule fois par période, puis les réutiliser ;
- éviter les `search()` dans les boucles mois × axes ;
- ajouter un test ou script de performance avec un volume minimal réaliste.

Critère cible :

- ouverture/recalcul cockpit inférieur à 2 secondes sur un exercice complet ;
- inférieur à 5 secondes sur trois exercices historiques.

### P2 — Clé de refresh incomplète

`_current_refresh_key()` encode actuellement :

- `date_from`
- `date_to`
- `reference_bank_journal_id`

Mais les filtres cockpit incluent aussi :

- `company_id`
- `activity_account_id`

Le `write()` déclenche bien un recalcul quand ces champs changent, mais la clé de fraîcheur ne représente pas tout le périmètre fonctionnel. Cela fragilise la détection de données obsolètes, notamment lors d'ouvertures, de restaurations de transient ou de comportements client atypiques.

Demande développeur :

- intégrer `company_id` et `activity_account_id` à `_current_refresh_key()`;
- ajouter un test de non-régression : changement axe analytique puis réouverture cockpit sans modification des dates.

### P2 — Garde-fous silencieux sur les lignes transient

Les modèles :

- `glc.coverage.cockpit.line`
- `glc.coverage.cockpit.treasury.line`

retournent silencieusement `True` ou un recordset vide si `create/write/unlink` est appelé hors contexte `glc_cockpit_auto_refreshing`.

Cette protection a probablement été ajoutée pour neutraliser des écritures parasites du client web. Elle évite des plantages, mais elle masque aussi les erreurs : un appel RPC peut sembler réussir alors qu'il n'a rien fait.

Demande développeur :

- remplacer les no-op silencieux par un comportement explicite ;
- option recommandée : lever une `AccessError` ou `UserError` claire hors contexte autorisé ;
- option alternative : conserver le no-op mais journaliser un warning technique ;
- vérifier que les vues restent en `create="0" edit="0" delete="0"` et que le JS ne tente plus d'écrire ces lignes.

### P2 — Droits d'accès trop larges sur des modèles techniques

`ir.model.access.csv` donne aux utilisateurs GLC les droits CRUD complets sur :

- `glc.coverage.cockpit`
- `glc.coverage.cockpit.line`
- `glc.coverage.cockpit.treasury.line`

Comme ce sont des `TransientModel`, le risque de persistance est limité. Mais le cockpit est un écran calculé : les utilisateurs devraient lire et modifier les filtres, pas créer/supprimer librement des lignes techniques.

Demande développeur :

- réduire les droits des lignes cockpit à lecture seule si possible ;
- conserver l'écriture uniquement sur le modèle cockpit principal si nécessaire pour les filtres ;
- valider les parcours JS après réduction des ACL.

### P2 — Périmètre analytique très large

`_cockpit_analytic_accounts()` récupère tous les comptes analytiques de la société ou globaux, hors codes exclus.

Ce choix permet d'englober des axes hors plan unique si nécessaire, mais il peut aussi faire remonter des comptes analytiques non GLC si la base contient d'autres usages analytiques.

Statut Lot C : **corrigé en `19.0.14.3.0`**. Le cockpit est désormais borné au plan analytique officiel `GLC - Activités`, qui porte les activités, ressources, financements et virements internes du plan unique GLC.

Demande développeur :

- décider explicitement si le cockpit doit lire uniquement le plan `GLC - Activités` ;
- si oui, ajouter le filtre `plan_id`;
- si non, documenter la règle "tous plans analytiques sauf exclusions" et ajouter un test avec un compte analytique hors GLC.

### P2 — Domaine des actions Q1/Q3 matérialisé par liste d'IDs

Plusieurs actions ouvrent des listes via des domaines `("id", "in", ids)` après calcul Python.

Exemples :

- lignes à qualifier ;
- écritures concernées ;
- factures période ;
- factures ouvertes.

Sur une petite base, c'est pratique. Sur une grosse base, les domaines à milliers d'IDs deviennent lourds et moins lisibles.

Demande développeur :

- préférer des domaines dynamiques reproductibles quand c'est possible ;
- réserver les listes d'IDs aux cas où la logique Python est vraiment indispensable ;
- documenter les cas où le domaine ne peut pas être exprimé en pur domaine Odoo.

### P2 — Cohérence sémantique des champs de qualité documentaire

Les champs suivants sont des `Integer`, mais gardent un suffixe `amount` :

- `revenue_eligible_amount`
- `revenue_invoiced_amount`
- `expense_eligible_amount`
- `expense_invoiced_amount`

Le libellé UI précise maintenant "lignes", mais le nom technique reste ambigu.

Statut Lot D : **corrigé en `19.0.14.4.0`**. Les champs explicites `*_line_count` sont ajoutés et utilisés par les vues. Les anciens champs `*_amount` restent alimentés comme alias transitoires pour compatibilité.

Demande développeur :

- renommer techniquement vers `*_line_count` lors d'un prochain lot contrôlé ;
- ou ajouter un commentaire explicite et ne plus exposer ces noms dans les développements futurs.

### P3 — Q2 est un stock à date, pas un flux de période

La vue l'indique : "Q2 — Lettrage tiers (stock à fin période)". Le code calcule bien les lignes jusqu'à `date_to`, sans borne `date_from`.

C'est pertinent pour un taux de lettrage, mais il faut éviter l'ambiguïté avec les autres KPI du cockpit, majoritairement bornés `date_from/date_to`.

Statut Lot D : **corrigé en `19.0.14.4.0`**. La vue rappelle explicitement que les lignes antérieures à la période restent prises en compte si elles sont ouvertes à la date de fin.

Demande développeur :

- maintenir ce wording partout ;
- ajouter une aide courte côté champ ou doc : "les lignes antérieures à la période restent prises en compte si elles sont ouvertes à date de fin".

### P3 — Préférences JS stockées globalement dans le navigateur

Le mode "Payé uniquement" est stocké dans `localStorage` avec la clé :

- `glc_cockpit_detail_paid_only`

La clé n'est pas segmentée par base, société, utilisateur ou environnement.

Impact limité, mais possible surprise si le même navigateur navigue entre sandbox, prod, plusieurs sociétés ou plusieurs utilisateurs.

Statut Lot D : **corrigé en `19.0.14.4.0`**. La clé active est segmentée par base, utilisateur et société : `glc_cockpit_detail_paid_only:<db>:<uid>:<company_id>`. L'ancienne clé reste lue uniquement comme valeur initiale de migration.

Demande développeur :

- intégrer au minimum la base ou la société dans la clé ;
- idéalement stocker la préférence côté utilisateur Odoo si elle devient structurante.

### P3 — Migrations nombreuses et répétitives

Plusieurs versions de migration rappellent `migrate_glc_analytic_nomenclature()`.

C'est rassurant pour restaurer une base polluée, mais cela crée une impression de rattrapage permanent. Il faut maintenant figer une stratégie.

Demande développeur :

- conserver l'idempotence ;
- documenter pourquoi les migrations `19.0.8.0.0` à `19.0.8.0.4` rappellent la même normalisation ;
- ajouter un test ou script de migration rejouable sur base déjà conforme.

## 5. Sécurité et droits Odoo

### Constat

Le groupe `Utilisateur GLC` implique `analytic.group_analytic_accounting`. Le cockpit interroge aussi :

- `account.move`
- `account.move.line`
- `account.analytic.line`
- `account.journal`
- `account.account`

Les agrégations sont exécutées avec les droits de l'utilisateur courant, pas systématiquement en `sudo()`.

### Risque

Selon la configuration réelle des groupes comptables, un utilisateur GLC peut :

- voir le menu cockpit mais ne pas avoir assez de droits pour lire toutes les lignes nécessaires ;
- obtenir des KPI incomplets si des règles d'accès filtrent des écritures ;
- rencontrer une erreur d'accès lors des drill-down Q1/Q2/Q3.

### Demande développeur

- définir clairement le profil cible : contrôleur de gestion, comptable, gestionnaire GLC ;
- vérifier les droits minimaux requis sur les modèles comptables lus ;
- si le cockpit doit être fiable pour un profil non-comptable, envisager des calculs `sudo()` contrôlés, avec drill-down limité par droits utilisateur ;
- ajouter un test d'accès avec un utilisateur `group_glc_user` sans droits comptables larges.

## 6. Qualité code et maintenabilité

### Points positifs

- Les constantes métier sont centralisées dans `glc_constants.py`.
- Les libellés MOA sont présents et généralement compréhensibles.
- Les méthodes métier importantes sont nommées clairement.
- Les vues empêchent l'édition directe des listes calculées.
- Les widgets OWL restent spécialisés et lisibles.

### Points à améliorer

Le fichier `glc_coverage_cockpit.py` est devenu très volumineux et cumule plusieurs responsabilités :

- filtres et état transient ;
- agrégation exploitation ;
- agrégation trésorerie ;
- qualité documentaire ;
- lignes de détail ;
- logique de rafraîchissement ;
- protections client web.

Demande développeur :

- extraire progressivement des mixins :
  - `GlcCoverageAggregationMixin`
  - `GlcCoverageTreasuryMixin`
  - `GlcCoverageRefreshMixin`
  - `GlcCoverageDetailLineMixin`
- conserver une API publique stable sur `glc.coverage.cockpit`;
- ne pas refactorer en même temps qu'une modification fonctionnelle.

## 7. Demandes d'amélioration proposées

### Lot A — Fiabilisation tests et sécurité

Objectif : éviter les faux GO techniques.

À faire :

- vérifier/importer tous les fichiers de tests dans `tests/__init__.py` — fait dans l'addendum Lot A ;
- ajouter un test utilisateur `group_glc_user` ;
- réduire les droits CRUD sur les lignes transient ;
- rendre explicites les erreurs d'écriture hors refresh.

Priorité : haute.

### Lot B — Performance cockpit

Objectif : rendre le cockpit robuste sur données réelles.

À faire :

- remplacer les sommes Python répétées par des agrégations groupées ;
- mémoïser les buckets de virement interne par période ;
- éviter les recherches de factures sans domaine de date ;
- ajouter un script de benchmark.

Priorité : haute avant exploitation avec historique important.

### Lot C — Périmètre analytique et nomenclature

Objectif : verrouiller ce que le cockpit lit.

Statut : **réalisé en `19.0.14.3.0`** pour le périmètre cockpit.

Traité :

- décider "plan GLC uniquement" ou "tous plans sauf exclusions" ;
- tester le comportement avec un compte analytique non GLC ;
- documenter le périmètre plan GLC officiel.

Reste hors Lot C :

- documenter les codes exclus et les comptes legacy ;
- stabiliser la stratégie migration nomenclature.

Priorité : moyenne à haute.

### Lot D — UX et sémantique

Objectif : réduire les ambiguïtés pour la MOA.

Statut : **réalisé en `19.0.14.4.0`** pour les points principaux.

Traité :

- renommer techniquement les champs `*_amount` qui sont des compteurs ;
- renforcer l'aide Q2 "stock à fin période" ;
- segmenter la préférence navigateur "Payé uniquement" ;

Reste hors Lot D :

- vérifier le retour responsive de la phrase Q1 avec `text-nowrap`.

Priorité : moyenne.

## 8. Points à ne pas casser

Le développeur doit préserver explicitement :

- aucune écriture comptable générée par le cockpit ;
- aucune écriture analytique générée par le cockpit ;
- invariant compte bancaire : exploitation inchangée, trésorerie recalculée ;
- mode "Payé uniquement" limité au détail, sans modifier les KPI de synthèse ;
- exclusion des flux bilan/trésorerie du calcul exploitation, sauf virements internes qualifiés selon doctrine ;
- Q1 par lignes comptables contrôlées, pas par factures.

## 9. Checklist développeur avant prochain merge

- Tous les tests attendus sont réellement chargés par le runner standard.
- Un utilisateur GLC non administrateur peut ouvrir le cockpit sans erreur d'accès.
- Changement de société, période, axe et compte bancaire force un refresh complet.
- Les KPI exploitation sont identiques avant/après changement de compte bancaire.
- Le mode "Payé uniquement" ne modifie pas les KPI de synthèse.
- Les actions de drill-down Q1/Q2/Q3 restent utilisables sur une base volumineuse.
- Les migrations nomenclature sont rejouables sur une base déjà conforme.

## 10. Addendum correctif Lot A

Après audit, le Lot A minimal a été traité immédiatement :

- les 5 fichiers de tests absents du runner standard sont importés dans `tests/__init__.py` ;
- `_current_refresh_key()` encode désormais `company_id` et `activity_account_id`, en plus de `date_from`, `date_to` et `reference_bank_journal_id` ;
- un test de non-régression vérifie que la clé de refresh couvre société et axe analytique ;
- le test de nomenclature analytique a été réaligné sur la nomenclature actuelle à 12 axes, incluant `VIR_INT` ;
- la version module est passée à `19.0.14.1.1`.

Validation exécutée :

```text
docker compose exec -T odoo odoo -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import -u dorevia_glc_analytics \
  --test-enable --test-tags /dorevia_glc_analytics \
  --stop-after-init --http-port=18089
```

Résultat :

```text
dorevia_glc_analytics: 114 tests
0 failed
0 error(s)
98 post-tests exécutés
```

Le P1 "tests non importés" est donc corrigé. Le P2 "clé de refresh incomplète" est également corrigé pour le périmètre identifié.

## 11. Addendum correctif Lot A suite — droits / ACL

**Décision MOA :** le profil cible **Utilisateur GLC** (`group_glc_user`) doit pouvoir ouvrir et recalculer le **Contrôle de gestion** sans être administrateur. Il inclut :

- `analytic.group_analytic_accounting` ;
- `account.group_account_readonly` *(lecture `account.move` / `account.move.line` — implicite depuis `19.0.14.1.2`)* ;
- `analytic.group_analytic_accounting` *(déjà implicite — lecture `account.analytic.line`)*.

Les **drill-down Q1/Q2/Q3** restent soumis aux droits utilisateur sur `account.move` / `account.move.line`. Un profil **analytique seul** (sans lecture comptable) produit des KPI incomplets — comportement documenté et testé.

Correctifs livrés :

- ACL **lecture seule** sur `glc.coverage.cockpit.line` et `glc.coverage.cockpit.treasury.line` ;
- recalcul cockpit : création/suppression des lignes via **`sudo()`** + contexte `glc_cockpit_auto_refreshing` ;
- **no-op silencieux remplacé** par `AccessError` explicite hors recalcul ;
- fichier `tests/test_glc_user_access.py` — ouverture, refresh, drill-down, CRUD interdit, profil insuffisant.

## 12. Addendum correctif Lot B — performance initiale

Objectif : réduire les recalculs inutiles sans modifier la doctrine KPI.

Correctifs livrés en première passe :

- les buckets de virements internes 580 sont calculés une fois pour la période globale puis réutilisés pour :
  - les agrégats exploitation période ;
  - les KPI de qualité documentaire ;
  - les lignes de trésorerie internes ;
- les buckets 580 sont calculés une fois par mois, puis réutilisés pour tous les axes du mois dans le détail ;
- `_sum_internal_transfer_inflow()` et `_sum_internal_transfer_outflow()` agrègent directement les buckets, au lieu de rappeler `_internal_transfer_amounts_for_account()` pour chaque axe ;
- `_analytic_accounts_from_move_line()` ne recherche plus deux fois les mêmes `account.analytic.line` ;
- ajout du script `scripts/benchmark_cockpit_refresh.py` pour mesurer le temps de recalcul cockpit sur une période donnée.

Effet attendu : le coût des virements internes passe de plusieurs scans répétés `mois × axes` à un scan par période utile. Les sommes analytiques principales restent à optimiser dans un lot ultérieur via agrégations groupées.

Commande benchmark :

```text
docker compose exec -T odoo odoo shell -c /etc/odoo/odoo.conf \
  -d glc-rgl-test-import --no-http \
  < /Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_glc_analytics/scripts/benchmark_cockpit_refresh.py
```

Résultat sandbox `glc-rgl-test-import` après upgrade `19.0.14.2.0` :

- période benchmark : `2026-01-01` → `2026-05-30` ;
- lignes détail activité : `30` ;
- lignes trésorerie interne : `2` ;
- temps recalculs : `1.818s`, `1.838s`, `1.796s` ;
- meilleur temps : `1.796s` ;
- temps moyen : `1.817s`.

### 12.1 Addendum correctif Lot B suite — agrégats exploitation / qualité

Objectif : poursuivre la réduction des boucles `mois × axes` et limiter les chargements globaux côté qualité / paiement.

Correctifs livrés :

- pré-agrégation des lignes analytiques par `(mois, axe)` sur toute la période pour le détail cockpit :
  - recettes ;
  - recettes payées ;
  - dépenses ;
  - dépenses payées ;
  - cumul RH ;
  - cumul RH payé ;
- remplacement des recherches répétées par axe et par mois par des lectures dans ces maps pré-agrégées ;
- Q1 confiance analytique : domaine SQL plus sélectif dès la recherche `account.move.line` et recherche groupée des `account.analytic.line` liés, au lieu d'un `search_count()` par ligne comptable ;
- Q3 tiers / paiements : agrégation des factures par `_read_group()` sur `payment_state`, avec domaine de période SQL équivalent à `invoice_date or date` ;
- actions de drill-down Q3 basées sur un domaine direct, sans préchargement des factures en Python.

Validation sandbox `glc-rgl-test-import` après upgrade `19.0.14.2.1` :

- tests module : `122 tests`, `104 post-tests`, `0 failed`, `0 error(s)` ;
- post-tests : `58.62s`, `47 443` requêtes ;
- comparaison indicative avant ce lot : `203.45s`, `84 002` requêtes ;
- benchmark YTD `2026-01-01` → `2026-05-30` : meilleur `0.194s`, moyen `0.205s` ;
- benchmark 3 exercices `2024-01-01` → `2026-05-30` : meilleur `0.170s`, moyen `0.175s`.

Points restant à traiter dans un futur lot performance :

- transformer les agrégats analytiques principaux en `_read_group()` lorsque le traitement `abs(line.amount)` et les multi-plans pourront être couverts sans changer la doctrine métier ;
- benchmarker explicitement un historique de 3 exercices lorsque la volumétrie réelle complète sera disponible.

### 12.2 Addendum correctif Lot C — périmètre analytique officiel

Objectif : fermer la dette P2 sur le périmètre analytique du cockpit.

Décision implémentée :

- le cockpit lit uniquement les comptes analytiques du plan officiel `GLC - Activités` ;
- ce plan unique contient les activités opérationnelles, les axes de ressources / financements et `VIR_INT` ;
- les comptes analytiques non-GLC, même rattachés à la société et porteurs d'écritures classe 6/7, ne doivent pas alimenter les KPI ni le détail ;
- le filtre `activity_account_id` reste limité au même plan GLC ;
- le filtrage ne s'appuie pas sur `glc_report_active`, afin de ne pas exclure `VIR_INT` des contrôles de trésorerie / virement interne.

Correctifs livrés :

- ajout de `_cockpit_analytic_plan()` ;
- `_cockpit_analytic_accounts()` applique désormais `plan_id = analytic_plan_glc_activites` ;
- test `test_non_glc_analytic_plan_is_excluded_from_cockpit` : une ligne analytique sur un plan externe ne remonte pas dans le cockpit.

Validation sandbox `glc-rgl-test-import` après upgrade `19.0.14.3.0` :

- tests module : `123 tests`, `105 post-tests`, `0 failed`, `0 error(s)` ;
- benchmark YTD `2026-01-01` → `2026-05-30` : meilleur `0.189s`, moyen `0.196s`.

### 12.3 Addendum correctif Lot D — UX / sémantique

Objectif : fermer les dettes P3 sans modifier les KPI métier.

Correctifs livrés :

- nouveaux champs de qualité documentaire :
  - `revenue_eligible_line_count` ;
  - `revenue_invoiced_line_count` ;
  - `expense_eligible_line_count` ;
  - `expense_invoiced_line_count` ;
- les anciens champs `*_amount` restent alimentés comme alias transitoires ;
- les vues utilisent les champs `*_line_count` ;
- la préférence navigateur `Payé uniquement` est segmentée par base, utilisateur et société ;
- l'onglet Q2 précise que le lettrage est un stock à date de fin, pas un flux borné à la période.

Validation sandbox `glc-rgl-test-import` après upgrade `19.0.14.4.0` :

- tests module : `123 tests`, `105 post-tests`, `0 failed`, `0 error(s)` ;
- benchmark YTD `2026-01-01` → `2026-05-30` : meilleur `0.160s`, moyen `0.166s`.

## 13. Conclusion

Le module est mûr fonctionnellement, mais il porte désormais un cockpit central. Il faut donc le traiter comme un composant de pilotage sensible : fiable, rapide, auditable et prévisible.

La priorité n'est pas d'ajouter de nouvelles fonctionnalités. La priorité est de consolider :

1. le chargement réel des tests ;
2. les performances d'agrégation ;
3. les droits d'accès ;
4. la clé de refresh ;
5. le périmètre analytique officiel.

Une fois ces points traités, le module sera beaucoup plus confortable à maintenir et à faire évoluer vers les prochains raffinements de contrôle de gestion.
