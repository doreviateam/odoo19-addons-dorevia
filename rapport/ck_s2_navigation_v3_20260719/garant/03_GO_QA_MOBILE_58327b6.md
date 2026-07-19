# Verdict Garant — GO QA mobile (`58327b6`)

**Verdict : GO QA**

Contre-recette mobile conforme sur le commit exact
`58327b68faa80404a006df7417809bb3953790ea` (parent `77197a3`).

Environnement : Chromium (API Playwright), viewport réel **390 × 844**.

| Contrôle | Résultat |
|---|---|
| Upgrade `1.98 → 1.99` + double resync | Conforme |
| Premier item | Icône `fa-home`, sans texte visible |
| Nom accessible | `aria-label="Accueil"` et `title="Accueil"` |
| « Boutique » visible dans le drawer | Absent |
| Ordre | Maison · Épicerie · Producteurs · Professionnels |
| Sous-catégories | Sucrée et salée visibles |
| Six liens parent/enfant | Clics et destinations conformes |
| Fermeture après sélection | Conforme |
| Retour navigateur | Conforme |
| Bouton de fermeture | Conforme |
| Doublon / niveau vide | Aucun |
| Chevauchement / troncature | Aucun |
| Scroll horizontal | Aucun |
| Scroll vertical si dépassement | Vérifié |
| Overlay | Backdrop intercepte la page |
| Console JavaScript | 0 erreur |
| HTTP destinations | Tous en `200` |

Note overlay : le toucher du backdrop ne ferme pas le drawer ; il bloque la page sous-jacente. Fermeture assurée par le bouton prévu — critère satisfait.

Preuves : `captures/01_*` … `03_*` et `results/go_qa_mobile_390_58327b6.json`.

```text
s2_mobile_qa_verdict       = GO_QA
tested_sha                 = 58327b68faa80404a006df7417809bb3953790ea
tested_version             = 19.0.1.99.0
ready_for_MOA_arbitrage    = yes
```

Aucun checkout, code, commit, push, PR ou déploiement effectué pendant ce contrôle.
Instance Docker QA et données temporaires détruites ; preuves conservées dans cette archive.
