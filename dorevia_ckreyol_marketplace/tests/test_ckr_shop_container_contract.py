# -*- coding: utf-8 -*-
"""Contrat `/shop` conteneur unique — chips, sidebar, canonical, hero retail.

Référence produit : une seule grille boutique sur ``/shop`` ; « Toute la sélection » = reset
global ; ``Toutes`` = neutre par groupe ; ``Mi Boutik La`` = titre hero
éditorial sur le **cadre catalogue** : les facettes sidebar (``ckr_collection``,
``ckr_origin``, ``ckr_category``…) **filtrent** la grille sans changer de page métier ni
substituer le hero « porte » Collections / Origines — sauf recherche ou chemin hors
socle boutique (cf. §4).

Les tests HTTP vérifient le HTML rendu et les en-têtes ; la logique JS
mutualiste est couverte ici via l’état **serveur** des cases à cocher pour
des URLs données, et via les marqueurs de classe attendus dans le DOM.

Les méthodes ``test_contract_inv_*`` verrouillent l’invariant produit :
facettes multi-sélection sur ``/shop`` sans ``ckr_mode=origin`` imposé pour
les origines (facette ≠ porte « Origines »), sans routes parallèles dans le rail,
avec canonical cohérent et hero vitrine lorsque pertinent.

PV recette sandbox (commande, base, résultat) :
``docs/mvp_02/PV_RECETTE_SHOP_CONTAINER_CONTRACT.md``.

Exécution ciblée ::

    odoo -d <base> --test-enable --stop-after-init \\
        --test-tags=dorevia_ckr_shop_contract
"""
import html
import re
from urllib.parse import parse_qs, urlparse

from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install", "dorevia_ckr_shop", "dorevia_ckr_shop_contract")
class TestCkrShopContainerContract(HttpCase):
    """Non-régression machine d’état boutique CK (chips + sidebar + canonical)."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref("website.default_website")

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _canonical_href(self, html_text):
        m = re.search(
            r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
            html_text,
            re.I,
        )
        self.assertTrue(m, "Balise canonical absente.")
        # Le HTML échappe les ``&`` en ``&amp;`` : sans déséchappement,
        # ``parse_qs`` fusionne à tort plusieurs ``ckr_mode``.
        return html.unescape(m.group(1))

    def _shortcut_chip_hrefs(self, html_text):
        m = re.search(
            r'class="ckr-shop-shortcuts__chips"[^>]*>(.*?)</div>\s*<div class="ckr-shop-shortcuts__right"',
            html_text,
            re.DOTALL,
        )
        self.assertTrue(m, "Bloc chips introuvable.")
        return re.findall(r'<a[^>]+href="([^"]+)"', m.group(1))

    def _explorer_shortcuts_chips_markup(self, html_text):
        """Fragment HTML du conteneur ``ckr_shop_explorer_shortcuts`` — rangée chips.

        Ciblage aligné sur le gabarit : ``nav.ckr-shop-shortcuts`` puis
        ``.ckr-shop-shortcuts__chips`` (pas d’identifiant de template Odoo dans le rendu).
        """
        nav = re.search(
            r'<nav[^>]*class="[^"]*\bckr-shop-shortcuts\b[^"]*"[^>]*>',
            html_text,
            re.I,
        )
        self.assertTrue(
            nav,
            "Barre explorer ``nav.ckr-shop-shortcuts`` (template ckr_shop_explorer_shortcuts) absente.",
        )
        tail = html_text[nav.start() :]
        m = re.search(
            r'class="ckr-shop-shortcuts__chips"[^>]*>(.*?)</div>\s*<div class="ckr-shop-shortcuts__right"',
            tail,
            re.DOTALL,
        )
        self.assertTrue(
            m,
            "Conteneur ``.ckr-shop-shortcuts__chips`` introuvable sous la nav explorer.",
        )
        return m.group(1)

    def _explorer_shortcuts_chip_label_hrefs(self, html_text):
        """Couples (libellé texte, href) dans l’ordre d’affichage des chips."""
        inner = self._explorer_shortcuts_chips_markup(html_text)
        pairs = []
        for m in re.finditer(
            r'<a\b[^>]*\bhref="([^"]+)"[^>]*>([\s\S]*?)</a>',
            inner,
            re.I,
        ):
            raw_label = html.unescape(m.group(2))
            label = re.sub(r"<[^>]+>", "", raw_label).strip()
            pairs.append((label, html.unescape(m.group(1).strip())))
        self.assertGreaterEqual(len(pairs), 1, "Aucune ancre chip dans le bloc explorer.")
        return pairs

    def _chip_paths_forbidden_strict(self):
        """Routes marketing **autonomes** : interdites comme cible du href des chips."""
        return ("/promotions", "/kits", "/incontournables")

    def _input_has_checked(self, attrs_fragment):
        return bool(re.search(r"\bchecked\b", attrs_fragment))

    def _assert_sidebar_all_neutral(self, html, msg=""):
        """``Toutes`` cochée pour catégories, collections, origines (serveur)."""
        for cls_fragment, label in (
            ("ckr-sidebar-cat-all", "catégories"),
            ("ckr-sidebar-collection-all", "collections"),
            ("ckr-sidebar-origin-all", "origines"),
        ):
            m = re.search(
                rf'<input([^>]*class="[^"]*{cls_fragment}[^"]*"[^>]*)>',
                html,
            )
            self.assertTrue(m, "%s : case « Toutes » absente (%s)." % (msg, label))
            self.assertTrue(
                self._input_has_checked(m.group(1)),
                "%s : « Toutes » non cochée (%s)." % (msg, label),
            )

    def _forbidden_chip_paths(self):
        return ("/promotions", "/kits", "/incontournables", "/collections", "/origines")

    def _forbidden_sidebar_facet_paths(self):
        """Routes parallèles interdites pour la navigation des facettes CK."""
        return (
            "/collections",
            "/origines",
            "/promotions",
            "/kits",
            "/shop/category/",
        )

    def _canonical_query_dict(self, html_text):
        canon = self._canonical_href(html_text)
        return parse_qs(urlparse(canon).query), canon

    def _assert_canonical_has_no_ckr_mode_origin(self, html_text, msg=""):
        qs, _canon = self._canonical_query_dict(html_text)
        modes = qs.get("ckr_mode", [])
        self.assertNotIn(
            "origin",
            modes,
            (msg or "Canonical")
            + " : pas de ckr_mode=origin forcé pour une facette origine pure.",
        )

    def _assert_specific_facet_checked(self, html_text, kind, slug):
        """Checkbox serveur cochée pour une facette (hors ligne « Toutes »)."""
        if kind == "origin":
            needle_cls = "ckr-sidebar-origin-check"
            all_cls = "ckr-sidebar-origin-all"
            slug_needles = ('data-slug="%s"' % slug, "data-slug='%s'" % slug)
        elif kind == "collection":
            needle_cls = "ckr-sidebar-collection-check"
            all_cls = "ckr-sidebar-collection-all"
            slug_needles = ('data-slug="%s"' % slug, "data-slug='%s'" % slug)
        elif kind == "category":
            needle_cls = "ckr-sidebar-cat-check"
            all_cls = "ckr-sidebar-cat-all"
            slug_needles = (
                'data-category-slug="%s"' % slug,
                "data-category-slug='%s'" % slug,
            )
        else:
            raise ValueError(kind)
        for m in re.finditer(r"<input\s+([^>]+)>", html_text, flags=re.I):
            attrs = m.group(1)
            if needle_cls not in attrs or all_cls in attrs:
                continue
            if not any(n in attrs for n in slug_needles):
                continue
            self.assertTrue(
                self._input_has_checked(attrs),
                "Facette %s : slug %r doit être coché côté serveur." % (kind, slug),
            )
            return
        self.fail("Aucune checkbox %s trouvée pour le slug %r." % (kind, slug))

    def _ck_sidebar_facet_markup_chunks(self, html_text):
        """HTML des blocs facettes **CK** (checkboxes), pas le rail Odoo entier.

        Le rail peut encore contenir des liens natifs ``/shop/category/…`` hors
        gabarit CK ; le contrat porte sur les filtres sidebar pilotés par
        ``ckr_shop_sidebar.js``.
        """
        chunks = []
        for m in re.finditer(
            r"<ul\b[^>]*\bckr-shop-sidebar-catchecks\b[^>]*>[\s\S]*?</ul>",
            html_text,
            re.I,
        ):
            chunks.append(m.group(0))
        m_open = re.search(
            r"<div\b[^>]*\bckr-shop-sidebar-ck\b[^>]*>",
            html_text,
            re.I,
        )
        if m_open:
            start = m_open.start()
            i = m_open.end()
            depth = 1
            lower = html_text.lower()
            while i < len(html_text) and depth > 0:
                op = lower.find("<div", i)
                cl = lower.find("</div>", i)
                if cl == -1:
                    break
                if op != -1 and op < cl:
                    depth += 1
                    i = op + 4
                else:
                    depth -= 1
                    i = cl + 6
            chunks.append(html_text[start:i])
        return "\n".join(chunks)

    def _assert_sidebar_facet_hrefs_clean(self, html_text):
        """Aucune route parallèle dans les blocs facettes CK (checkboxes)."""
        scoped = self._ck_sidebar_facet_markup_chunks(html_text)
        self.assertTrue(
            scoped.strip(),
            "Marqueurs sidebar CK introuvables (catchecks / bloc collections+origines).",
        )
        for attr in ("href", "action", "formaction"):
            for hit in re.finditer(
                r"\b%s=[\"']([^\"']+)[\"']" % attr, scoped, flags=re.I
            ):
                url = html.unescape(hit.group(1))
                if url.strip().startswith("#") or url.strip().lower().startswith(
                    "javascript:"
                ):
                    continue
                path = urlparse(url).path
                for bad in self._forbidden_sidebar_facet_paths():
                    self.assertFalse(
                        path.startswith(bad) or bad in path,
                        "Attribut %s sidebar interdit %r (path %r) pour une "
                        "facette /shop." % (attr, url, path),
                    )

    # ------------------------------------------------------------------
    # 1 — /shop neutre
    # ------------------------------------------------------------------
    def test_contract_01_neutral_shop_hero_tout_sidebar_toutes(self):
        resp = self.url_open("/shop", timeout=60)
        self.assertEqual(resp.status_code, 200)
        html = resp.text
        self.assertIn("Mi Boutik La", html)
        self.assertRegex(
            html,
            r"<h1[^>]*>[\s\S]*Mi Boutik La[\s\S]*</h1>",
            "Le titre éditorial doit être dans le h1 hero.",
        )
        self.assertRegex(
            html,
            r'ckr-sidebar-cat-all[\s\S]{0,220}Toutes',
            "Libellé « Toutes » attendu sur la ligne neutre catégories.",
        )
        self.assertIsNone(
            re.search(
                r'ckr-sidebar-cat-all[\s\S]{0,120}Mi Boutik La',
                html,
            ),
            "« Mi Boutik La » ne doit pas être la ligne « Toutes » catégories.",
        )
        self._assert_sidebar_all_neutral(html, msg="neutre")

    # ------------------------------------------------------------------
    # 2 — Chip « Toute la sélection » (reset grille)
    # ------------------------------------------------------------------
    def test_contract_02_chip_tout_targets_plain_shop(self):
        resp = self.url_open("/shop?ckr_mode=promo&ckr_collection_scope=all", timeout=60)
        self.assertEqual(resp.status_code, 200)
        hrefs = self._shortcut_chip_hrefs(resp.text)
        self.assertTrue(hrefs, "Aucun chip.")
        self.assertTrue(
            hrefs[0].endswith("/shop")
            and "ckr_mode" not in hrefs[0]
            and "ckr_collection" not in hrefs[0],
            "Le premier chip (Toute la sélection) doit cibler /shop nu : %r" % hrefs[0],
        )
        self.assertEqual(
            urlparse(hrefs[0]).query,
            "",
            "Contrat chip Toute la sélection : aucune query (reset global, pas de paramètres résiduels) : %r"
            % hrefs[0],
        )

    # ------------------------------------------------------------------
    # 3 — Chips commerciaux → /shop?…
    # ------------------------------------------------------------------
    def test_contract_03_commercial_chips_stay_on_shop(self):
        resp = self.url_open("/shop", timeout=60)
        self.assertEqual(resp.status_code, 200)
        pairs = self._explorer_shortcuts_chip_label_hrefs(resp.text)
        label_to_href = {lab: href for lab, href in pairs}
        self.assertIn("Toute la sélection", label_to_href)
        reset_href = label_to_href["Toute la sélection"]
        self.assertEqual(
            urlparse(reset_href).query,
            "",
            "Contrat chip Toute la sélection : aucune query sur page neutre non plus : %r"
            % reset_href,
        )
        commercial = (
            ("Promotions", "promo"),
            ("Incontournables", "featured"),
            ("Kits / Packs", "pack"),
        )
        for label, mode in commercial:
            if label not in label_to_href:
                continue
            href = label_to_href[label]
            self.assertIn(
                "ckr_mode=%s" % mode,
                href,
                "Chip %r : ``ckr_mode`` attendu dans href %r." % (label, href),
            )
        for _label, href in pairs:
            path = urlparse(href).path
            self.assertTrue(
                path == "/shop" or path.endswith("/shop"),
                "Chaque chip doit cibler la grille boutique (chemin …/shop) : %r" % href,
            )
            for bad in self._forbidden_chip_paths():
                self.assertNotIn(
                    bad,
                    href,
                    "Pas de lien chip vers route parallèle %s : %r" % (bad, href),
                )

    def test_contract_03b_recipe_html_explorer_shortcuts_shop_grammar(self):
        """Recette HTML : grammaire boutique — pas de stubs marketing dans les chips.

        Rend `/shop`, parse le bloc ``ckr_shop_explorer_shortcuts`` (nav
        ``.ckr-shop-shortcuts`` + ``.ckr-shop-shortcuts__chips``) et vérifie que :

        * aucune cible chip n’est une route parallèle ``/promotions``, ``/kits``,
          ``/incontournables`` ;
        * chaque cible est bien la grille ``…/shop`` avec les ``ckr_mode``
          attendus sur les trois chips commerciaux ;
        * « Toute la sélection » recharge ``/shop`` sans ``ckr_mode``.
        """
        resp = self.url_open("/shop", timeout=60)
        self.assertEqual(resp.status_code, 200, "GET /shop doit répondre 200.")
        body = resp.text
        specs = self._explorer_shortcuts_chip_label_hrefs(body)
        commercial_ordered = (
            ("Promotions", "promo"),
            ("Incontournables", "featured"),
            ("Kits / Packs", "pack"),
        )
        self.assertGreaterEqual(len(specs), 1, "Au minimum la chip reset boutique.")
        label0, href0 = specs[0]
        self.assertEqual(
            label0,
            "Toute la sélection",
            "Premier chip : reset catalogue attendu, obtenu %r." % label0,
        )
        pu0 = urlparse(href0)
        path0 = pu0.path.rstrip("/") or "/"
        self.assertTrue(
            path0 == "/shop" or path0.endswith("/shop"),
            "Chip reset : grille …/shop attendue, obtenu %r." % href0,
        )
        self.assertFalse(
            [m for m in parse_qs(pu0.query).get("ckr_mode", []) if m != ""],
            "« Toute la sélection » : pas de ``ckr_mode`` dans href %r." % href0,
        )
        commercial_specs = specs[1:]
        labels_expected_order = [lab for lab, _m in commercial_ordered]
        labels_got = [lab for lab, _h in commercial_specs]
        self.assertEqual(
            labels_got,
            [lab for lab in labels_expected_order if lab in labels_got],
            "Ordre maquette des chips commerciaux **affichés** (segments vides masqués).",
        )
        mode_by_label = dict(commercial_ordered)
        for label, href in commercial_specs:
            exp_mode = mode_by_label.get(label)
            self.assertTrue(
                exp_mode,
                "Libellé chip inconnu ou commercial hors contrat : %r." % label,
            )
            pu = urlparse(href)
            path = pu.path.rstrip("/") or "/"
            for stub in self._chip_paths_forbidden_strict():
                self.assertNotEqual(
                    path,
                    stub,
                    "Chip %r pointe vers la route stub interdite %r : %r"
                    % (label, stub, href),
                )
                self.assertFalse(
                    path.endswith(stub),
                    "Chip %r — path interdit finissant par %r : %r"
                    % (label, stub, href),
                )
            self.assertTrue(
                path == "/shop" or path.endswith("/shop"),
                "Chip %r doit cibler la grille boutique (chemins terminant par …/shop), "
                "obtenu %r (href %r)." % (label, path, href),
            )
            qs = parse_qs(pu.query)
            modes = [m for m in qs.get("ckr_mode", []) if m != ""]
            self.assertEqual(
                sorted(modes),
                [exp_mode],
                "Chip %r doit n’emporter que ``ckr_mode=%s`` (href %r)."
                % (label, exp_mode, href),
            )

    # ------------------------------------------------------------------
    # 4 — Hero retail (vitrine Mi Boutik La) sur `/shop`
    #
    #     * Chips promo / featured / pack : même hero vitrine qu’à l’accueil.
    #     * Facettes sidebar collections / origines : **filtre catalogue** uniquement,
    #       même hero vitrine (pas de rupture avec une page « porte »).
    #     * Recherche : pas de hero CK vitrine ; alias ``/shop/category/…`` → query :
    #       même hero vitrine que les facettes ``ckr_category`` (cf. ``04b``).
    # ------------------------------------------------------------------
    def test_contract_04_hero_retail_shop_neutral_and_commercial_chips(self):
        """``/shop`` nu + chips commerciaux : classe ``ckr-shop-hero--retail``."""
        neutral = self.url_open("/shop", timeout=60)
        self.assertEqual(neutral.status_code, 200)
        self.assertIn("ckr-shop-hero--retail", neutral.text)

        for qs in ("ckr_mode=promo", "ckr_mode=pack"):
            r = self.url_open("/shop?%s" % qs, timeout=60)
            self.assertEqual(r.status_code, 200, qs)
            self.assertIn(
                "ckr-shop-hero--retail",
                r.text,
                "Les chips commerciaux gardent la vitrine boutique initiale : %s" % qs,
            )
            self.assertNotIn("ckr-shop-hero--context", r.text, qs)
        r_in = self.url_open("/shop?ckr_mode=featured", timeout=60)
        self.assertEqual(r_in.status_code, 200)
        if "ckr-shop-hero" in r_in.text:
            self.assertIn(
                "ckr-shop-hero--retail",
                r_in.text,
                "Incontournables : même principe — pas de rupture avec l’accueil boutique.",
            )
            self.assertNotIn(
                "ckr-shop-hero--context",
                r_in.text,
            )

    def test_contract_04b_search_hides_hero_category_alias_keeps_retail_hero(self):
        """Recherche « réelle » : pas de hero CK vitrine ; ``/shop/category/…`` redirige vers
        ``/shop?ckr_category=…`` — même hero vitrine Mi Boutik La que les facettes sidebar."""
        r_search = self.url_open("/shop?search=manioc", timeout=60)
        self.assertEqual(r_search.status_code, 200)
        self.assertNotIn("ckr-shop-hero--retail", r_search.text)

        cat = self.env["product.public.category"].search(
            [
                "|",
                ("website_id", "=", False),
                ("website_id", "=", self.website.id),
            ],
            limit=1,
        )
        if cat:
            path = "/shop/category/%s" % self.env["ir.http"].sudo()._slug(cat)
            r_cat = self.url_open(path, timeout=60)
            self.assertEqual(r_cat.status_code, 200)
            self.assertIn("ckr-shop-hero--retail", r_cat.text)
            self.assertNotIn("ckr-shop-hero--context", r_cat.text)

    def test_contract_04c_hero_retail_keeps_with_collection_or_origin_sidebar_facet(
        self,
    ):
        """Facettes sidebar : même cadre vitrine boutique (pas de hero « porte »)."""
        coll = self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_shop_collection_demo_saint_anne",
            raise_if_not_found=False,
        )
        if coll and coll.slug:
            r = self.url_open("/shop?ckr_collection=%s" % coll.slug, timeout=60)
            self.assertEqual(r.status_code, 200)
            self.assertIn("ckr-shop-hero--retail", r.text)
            self.assertNotIn("ckr-shop-hero--context", r.text)

        origin = self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_shop_origin_demo_guadeloupe",
            raise_if_not_found=False,
        )
        if origin and origin.slug:
            r2 = self.url_open(
                "/shop?ckr_origin=%s" % origin.slug,
                timeout=60,
            )
            self.assertEqual(r2.status_code, 200)
            self.assertIn("ckr-shop-hero--retail", r2.text)
            self.assertNotIn("ckr-shop-hero--context", r2.text)

    # ------------------------------------------------------------------
    # 5 — Catégories (état serveur + requête multi-slugs = OU côté domaine)
    #
    # Sidebar multi-sélection sur ``/shop`` (sans navigation exclusive). Le
    # test ``05b`` verrouille le moteur HTTP multi-``ckr_category`` + canonical.
    # La non-régression du clic réel multi-sélection relève d’une tour navigateur.
    # ------------------------------------------------------------------
    def test_contract_05_category_facet_unchecks_toutes_server_side(self):
        cats = self.env["product.public.category"].search(
            [
                "|",
                ("website_id", "=", False),
                ("website_id", "=", self.website.id),
            ],
            limit=2,
        )
        if not cats:
            self.skipTest("Aucune catégorie publique pour le test facette.")
        IrHttp = self.env["ir.http"].sudo()
        slug = IrHttp._slug(cats[0])
        r = self.url_open("/shop?ckr_category=%s" % slug, timeout=60)
        self.assertEqual(r.status_code, 200)
        self.assertIn("ckr-shop-hero--retail", r.text)
        self.assertNotIn("ckr-shop-hero--context", r.text)
        m_all = re.search(
            r'<input([^>]*class="[^"]*ckr-sidebar-cat-all[^"]*"[^>]*)>',
            r.text,
        )
        self.assertTrue(m_all)
        self.assertFalse(
            self._input_has_checked(m_all.group(1)),
            "« Toutes » catégories doit être décochée quand une facette est active.",
        )

    def test_contract_05b_dual_ckr_category_query_supported(self):
        cats = self.env["product.public.category"].search(
            [
                "|",
                ("website_id", "=", False),
                ("website_id", "=", self.website.id),
            ],
            limit=2,
        )
        if len(cats) < 2:
            self.skipTest("Deux catégories requises pour le test OU query.")
        IrHttp = self.env["ir.http"].sudo()
        s1, s2 = IrHttp._slug(cats[0]), IrHttp._slug(cats[1])
        r = self.url_open(
            "/shop?ckr_category=%s&ckr_category=%s" % (s1, s2),
            timeout=60,
        )
        self.assertEqual(r.status_code, 200)
        self.assertIn("ckr-shop-hero--retail", r.text)
        self.assertNotIn("ckr-shop-hero--context", r.text)
        canon = self._canonical_href(r.text)
        q = parse_qs(urlparse(canon).query)
        self.assertIn("ckr_category", q)
        self.assertGreaterEqual(len(q["ckr_category"]), 2)

    # ------------------------------------------------------------------
    # 6 — Collections : query seule, pas scope=all comme « tout coché »
    # ------------------------------------------------------------------
    def test_contract_06_scope_all_keeps_only_toutes_checked(self):
        r = self.url_open("/shop?ckr_collection_scope=all", timeout=60)
        self.assertEqual(r.status_code, 200)
        for block in re.finditer(
            r'<input([^>]*class="[^"]*ckr-sidebar-collection-check[^"]*"[^>]*)>',
            r.text,
        ):
            attrs = block.group(1)
            if "ckr-sidebar-collection-all" in attrs:
                self.assertTrue(
                    self._input_has_checked(attrs),
                    "« Toutes » collections doit rester cochée avec scope=all.",
                )
            else:
                self.assertFalse(
                    self._input_has_checked(attrs),
                    "Aucune collection spécifique ne doit paraître cochée "
                    "sans `ckr_collection` en query.",
                )

    def test_contract_06b_collection_slug_checks_row_server_side(self):
        coll = self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_shop_collection_demo_saint_anne",
            raise_if_not_found=False,
        )
        if not coll or not coll.slug:
            self.skipTest("Collection démo Saint-Anne absente.")
        r = self.url_open("/shop?ckr_collection=%s" % coll.slug, timeout=60)
        self.assertEqual(r.status_code, 200)
        m_all = re.search(
            r'<input([^>]*class="[^"]*ckr-sidebar-collection-all[^"]*"[^>]*)>',
            r.text,
        )
        self.assertTrue(m_all)
        self.assertFalse(self._input_has_checked(m_all.group(1)))

    def test_contract_06c_dual_collection_query_returns_200(self):
        coll = self.env["ckr.shop.collection"].sudo().search([], limit=2)
        if len(coll) < 2:
            self.skipTest("Deux collections requises.")
        r = self.url_open(
            "/shop?ckr_collection=%s&ckr_collection=%s"
            % (coll[0].slug, coll[1].slug),
            timeout=60,
        )
        self.assertEqual(r.status_code, 200)
        q = parse_qs(urlparse(self._canonical_href(r.text)).query)
        self.assertIn("ckr_collection", q)
        self.assertGreaterEqual(len(q["ckr_collection"]), 2)

    def test_contract_06d_sidebar_facet_counters_never_display_zero(self):
        """Non-régression UX : aucun compteur de facette ne doit afficher ``(0)`` dans le rail.

        Les bornes servent le même domaine que la grille ; un compteur nul est masqué
        (l’exception « ligne cochée » conserve la case sans parens si le résultat courant est vide).
        """
        r = self.url_open("/shop", timeout=60)
        self.assertEqual(r.status_code, 200)
        m_aside = re.search(
            r'<aside\b[^>]*id=["\']products_grid_before["\']',
            r.text,
            re.I,
        )
        fragment = r.text[m_aside.start() :] if m_aside else r.text
        m_close = fragment.find("</aside>")
        if m_close != -1:
            fragment = fragment[: m_close + len("</aside>")]
        # Parenthèses « (0) » uniquement dans le span muted des compteurs de facettes.
        self.assertFalse(
            re.search(
                r'<span[^>]*\btext-muted\b[^>]*\bsmall\b[^>]*>[\s\n]*\(\s*0\s*\)[\s\n]*</span>',
                fragment,
                re.I,
            ),
            "Aucune facette sidebar ne doit rendre un compteur littéral (0).",
        )

    # ------------------------------------------------------------------
    # 7 — Origines
    # ------------------------------------------------------------------
    def test_contract_07_origin_facet_and_multi_slug(self):
        origin = self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_shop_origin_demo_guadeloupe",
            raise_if_not_found=False,
        )
        if not origin or not origin.slug:
            self.skipTest("Origine démo Guadeloupe absente.")
        r = self.url_open(
            "/shop?ckr_origin=%s" % origin.slug,
            timeout=60,
        )
        self.assertEqual(r.status_code, 200)
        m_all = re.search(
            r'<input([^>]*class="[^"]*ckr-sidebar-origin-all[^"]*"[^>]*)>',
            r.text,
        )
        self.assertTrue(m_all)
        self.assertFalse(self._input_has_checked(m_all.group(1)))

        r2 = self.url_open(
            "/shop?ckr_mode=promo&ckr_origin=%s" % origin.slug,
            timeout=60,
        )
        self.assertEqual(r2.status_code, 200)

    def test_contract_07b_dual_ckr_origin_query_supported(self):
        Origin = self.env["ckr.shop.origin"].sudo()
        origins = Origin.search([], limit=2)
        if len(origins) < 2:
            self.skipTest("Deux origines requises pour le test OU query.")
        s1, s2 = origins[0].slug, origins[1].slug
        if not s1 or not s2:
            self.skipTest("Slugs origine manquants.")
        r = self.url_open(
            "/shop?ckr_origin=%s&ckr_origin=%s" % (s1, s2),
            timeout=60,
        )
        self.assertEqual(r.status_code, 200)
        q = parse_qs(urlparse(self._canonical_href(r.text)).query)
        self.assertIn("ckr_origin", q)
        self.assertGreaterEqual(len(q["ckr_origin"]), 2)

    # ------------------------------------------------------------------
    # 8 — Combinaisons sidebar + chips (HTTP 200 + canonical)
    # ------------------------------------------------------------------
    def test_contract_08_combinations_promo_category_collection_origin(self):
        cat = self.env["product.public.category"].search(
            [
                "|",
                ("website_id", "=", False),
                ("website_id", "=", self.website.id),
            ],
            limit=1,
        )
        coll = self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_shop_collection_demo_saint_anne",
            raise_if_not_found=False,
        )
        origin = self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_shop_origin_demo_guadeloupe",
            raise_if_not_found=False,
        )
        if not cat or not coll or not origin:
            self.skipTest("Données démo catégorie / collection / origine incomplètes.")
        IrHttp = self.env["ir.http"].sudo()
        slug_cat = IrHttp._slug(cat)
        url = (
            "/shop?ckr_mode=promo&ckr_category=%s&ckr_collection=%s&ckr_origin=%s"
            % (slug_cat, coll.slug, origin.slug)
        )
        r = self.url_open(url, timeout=60)
        self.assertEqual(r.status_code, 200)
        self.assertIn("ckr-shop-hero--retail", r.text)
        self.assertNotIn("ckr-shop-hero--context", r.text)
        canon = self._canonical_href(r.text)
        qs = parse_qs(urlparse(canon).query)
        self.assertIn("ckr_mode", qs)
        self.assertIn("promo", qs["ckr_mode"])
        self.assertIn("ckr_category", qs)
        self.assertIn("ckr_collection", qs)
        self.assertIn("ckr_origin", qs)

    # ------------------------------------------------------------------
    # 9 — Redirections vers /shop
    # ------------------------------------------------------------------
    def test_contract_09_collections_entry_redirects_to_shop(self):
        r = self.url_open("/collections", allow_redirects=False, timeout=60)
        self.assertEqual(r.status_code, 301)
        loc = r.headers.get("Location", "")
        self.assertIn("/shop", loc)

    def test_contract_09b_promotions_alias_redirects_to_shop_query(self):
        r = self.url_open("/promotions", allow_redirects=False, timeout=60)
        self.assertEqual(r.status_code, 301)
        loc = r.headers.get("Location", "")
        self.assertIn("/shop", loc)
        self.assertIn("ckr_mode=promo", loc)

    # ------------------------------------------------------------------
    # 10 — Canonical (multi-mode, origine, collection, catégorie)
    # ------------------------------------------------------------------
    def test_contract_10_canonical_multi_ckr_mode_sorted(self):
        r = self.url_open("/shop?ckr_mode=pack&ckr_mode=promo", timeout=60)
        self.assertEqual(r.status_code, 200)
        canon = self._canonical_href(r.text)
        qs = parse_qs(urlparse(canon).query)
        self.assertIn("ckr_mode", qs)
        self.assertGreaterEqual(len(qs["ckr_mode"]), 2)
        self.assertIn("pack", qs["ckr_mode"])
        self.assertIn("promo", qs["ckr_mode"])

    def test_contract_10b_canonical_includes_category_slug(self):
        cat = self.env["product.public.category"].search(
            [
                "|",
                ("website_id", "=", False),
                ("website_id", "=", self.website.id),
            ],
            limit=1,
        )
        if not cat:
            self.skipTest("Aucune catégorie publique.")
        slug = self.env["ir.http"].sudo()._slug(cat)
        r = self.url_open("/shop?ckr_category=%s" % slug, timeout=60)
        self.assertEqual(r.status_code, 200)
        qs = parse_qs(urlparse(self._canonical_href(r.text)).query)
        self.assertIn("ckr_category", qs)
        self.assertIn(slug, qs["ckr_category"])

    def test_contract_11_sidebar_mutual_css_markers_present(self):
        """Classes attendues pour la logique mutualiste (voir ``ckr_shop_sidebar.js``)."""
        r = self.url_open("/shop", timeout=60)
        self.assertEqual(r.status_code, 200)
        for needle in (
            "ckr-sidebar-collection-all",
            "ckr-sidebar-origin-all",
            "ckr-sidebar-cat-all",
        ):
            self.assertIn(needle, r.text)

    # ------------------------------------------------------------------
    # Invariants produit — facettes = query /shop (pas porte / pas page dédiée)
    # ------------------------------------------------------------------

    def test_contract_inv_01_origin_seule_facet_canonical_sans_mode_origin(self):
        origin = self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_shop_origin_demo_guadeloupe",
            raise_if_not_found=False,
        )
        if not origin or not origin.slug:
            self.skipTest("Origine démo Guadeloupe absente.")
        r = self.url_open("/shop?ckr_origin=%s" % origin.slug, timeout=60)
        self.assertEqual(r.status_code, 200)
        self.assertIn("ckr-shop-hero--retail", r.text)
        self.assertNotIn("ckr-shop-hero--context", r.text)
        m_all = re.search(
            r'<input([^>]*class="[^"]*ckr-sidebar-origin-all[^"]*"[^>]*)>',
            r.text,
        )
        self.assertTrue(m_all)
        self.assertFalse(self._input_has_checked(m_all.group(1)))
        self._assert_specific_facet_checked(r.text, "origin", origin.slug)
        qs, _c = self._canonical_query_dict(r.text)
        self.assertIn(origin.slug, qs.get("ckr_origin", []))
        self._assert_canonical_has_no_ckr_mode_origin(r.text)

    def test_contract_inv_02_deux_origines_canonical_sans_mode_origin(self):
        Origin = self.env["ckr.shop.origin"].sudo()
        origins = Origin.search([], limit=2)
        if len(origins) < 2:
            self.skipTest("Deux origines requises.")
        s1, s2 = origins[0].slug, origins[1].slug
        if not s1 or not s2:
            self.skipTest("Slugs origine manquants.")
        r = self.url_open(
            "/shop?ckr_origin=%s&ckr_origin=%s" % (s1, s2),
            timeout=60,
        )
        self.assertEqual(r.status_code, 200)
        self.assertIn("ckr-shop-hero--retail", r.text)
        self.assertNotIn("ckr-shop-hero--context", r.text)
        qs, _c = self._canonical_query_dict(r.text)
        self.assertGreaterEqual(len(qs.get("ckr_origin", [])), 2)
        self._assert_canonical_has_no_ckr_mode_origin(r.text)

    def test_contract_inv_03_promo_plus_origine_sans_second_mode_origin(self):
        origin = self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_shop_origin_demo_guadeloupe",
            raise_if_not_found=False,
        )
        if not origin or not origin.slug:
            self.skipTest("Origine démo Guadeloupe absente.")
        r = self.url_open(
            "/shop?ckr_mode=promo&ckr_origin=%s" % origin.slug,
            timeout=60,
        )
        self.assertEqual(r.status_code, 200)
        self.assertIn("ckr-shop-hero--retail", r.text)
        self.assertNotIn("ckr-shop-hero--context", r.text)
        qs, _c = self._canonical_query_dict(r.text)
        self.assertIn("promo", qs.get("ckr_mode", []))
        self.assertIn(origin.slug, qs.get("ckr_origin", []))
        self.assertNotIn(
            "origin",
            qs.get("ckr_mode", []),
            "Pas de ckr_mode=origin cumulé au chip promo pour une facette.",
        )

    def test_contract_inv_04_collection_seule_facette_canonical(self):
        coll = self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_shop_collection_demo_saint_anne",
            raise_if_not_found=False,
        )
        if not coll or not coll.slug:
            self.skipTest("Collection démo Saint-Anne absente.")
        r = self.url_open("/shop?ckr_collection=%s" % coll.slug, timeout=60)
        self.assertEqual(r.status_code, 200)
        self.assertIn("ckr-shop-hero--retail", r.text)
        self.assertNotIn("ckr-shop-hero--context", r.text)
        m_all = re.search(
            r'<input([^>]*class="[^"]*ckr-sidebar-collection-all[^"]*"[^>]*)>',
            r.text,
        )
        self.assertTrue(m_all)
        self.assertFalse(self._input_has_checked(m_all.group(1)))
        self._assert_specific_facet_checked(r.text, "collection", coll.slug)
        qs, _c = self._canonical_query_dict(r.text)
        self.assertIn(coll.slug, qs.get("ckr_collection", []))
        self.assertNotIn(
            "collection",
            qs.get("ckr_mode", []),
            "Facette collection : pas de ckr_mode=collection imposé par le canonical.",
        )

    def test_contract_inv_05_deux_collections_et_scope_all_neutralise_pas_toutes(self):
        coll = self.env["ckr.shop.collection"].sudo().search([], limit=2)
        if len(coll) < 2:
            self.skipTest("Deux collections requises.")
        s1, s2 = coll[0].slug, coll[1].slug
        if not s1 or not s2:
            self.skipTest("Slugs collection manquants.")
        r = self.url_open(
            "/shop?ckr_collection=%s&ckr_collection=%s&ckr_collection_scope=all"
            % (s1, s2),
            timeout=60,
        )
        self.assertEqual(r.status_code, 200)
        self.assertIn("ckr-shop-hero--retail", r.text)
        self.assertNotIn("ckr-shop-hero--context", r.text)
        qs, _c = self._canonical_query_dict(r.text)
        self.assertGreaterEqual(len(qs.get("ckr_collection", [])), 2)
        m_all = re.search(
            r'<input([^>]*class="[^"]*ckr-sidebar-collection-all[^"]*"[^>]*)>',
            r.text,
        )
        self.assertTrue(m_all)
        self.assertFalse(
            self._input_has_checked(m_all.group(1)),
            "« Toutes » collections ne doit pas être cochée quand des slugs "
            "ckr_collection sont actifs, même avec scope=all.",
        )
        self._assert_specific_facet_checked(r.text, "collection", s1)
        self._assert_specific_facet_checked(r.text, "collection", s2)

    def test_contract_inv_06_categorie_ck_query_sans_redirect_category_path(self):
        cats = self.env["product.public.category"].search(
            [
                "|",
                ("website_id", "=", False),
                ("website_id", "=", self.website.id),
            ],
            limit=1,
        )
        if not cats:
            self.skipTest("Aucune catégorie publique.")
        IrHttp = self.env["ir.http"].sudo()
        slug = IrHttp._slug(cats[0])
        r = self.url_open(
            "/shop?ckr_category=%s" % slug,
            allow_redirects=False,
            timeout=60,
        )
        self.assertEqual(
            r.status_code,
            200,
            "La facette CK catégorie ne doit pas rediriger vers /shop/category/…",
        )
        m_all = re.search(
            r'<input([^>]*class="[^"]*ckr-sidebar-cat-all[^"]*"[^>]*)>',
            r.text,
        )
        self.assertTrue(m_all)
        self.assertFalse(self._input_has_checked(m_all.group(1)))
        self._assert_specific_facet_checked(r.text, "category", slug)
        qs, _c = self._canonical_query_dict(r.text)
        self.assertIn(slug, qs.get("ckr_category", []))

    def test_contract_inv_shop_category_path_redirects_to_container(self):
        """Doctrine boutique : le conteneur unique est ``/shop?…``, pas ``/shop/category/…``."""
        cats = self.env["product.public.category"].search(
            [
                "|",
                ("website_id", "=", False),
                ("website_id", "=", self.website.id),
            ],
            limit=1,
        )
        if not cats:
            self.skipTest("Aucune catégorie publique.")
        IrHttp = self.env["ir.http"].sudo()
        slug = IrHttp._slug(cats[0])
        path = "/shop/category/%s" % slug
        r = self.url_open(path, allow_redirects=False, timeout=60)
        self.assertEqual(r.status_code, 302, path)
        loc = (r.headers.get("Location") or "").replace("\\", "")
        self.assertIn("ckr_category", loc)
        self.assertNotIn(
            "/shop/category/",
            loc.split("?")[0],
            "La redirection doit viser le préfixe /shop nu : %s" % loc,
        )
        ok = self.url_open(path, timeout=60)
        self.assertEqual(ok.status_code, 200)
        self._assert_specific_facet_checked(ok.text, "category", slug)

    def test_contract_inv_07_deux_categories_canonical_et_sans_mode_parasite(self):
        cats = self.env["product.public.category"].search(
            [
                "|",
                ("website_id", "=", False),
                ("website_id", "=", self.website.id),
            ],
            limit=2,
        )
        if len(cats) < 2:
            self.skipTest("Deux catégories requises.")
        IrHttp = self.env["ir.http"].sudo()
        s1, s2 = IrHttp._slug(cats[0]), IrHttp._slug(cats[1])
        r = self.url_open(
            "/shop?ckr_category=%s&ckr_category=%s" % (s1, s2),
            timeout=60,
        )
        self.assertEqual(r.status_code, 200)
        qs, _c = self._canonical_query_dict(r.text)
        self.assertGreaterEqual(len(qs.get("ckr_category", [])), 2)
        parasite_modes = {"origin", "collection"} & set(qs.get("ckr_mode", []))
        self.assertFalse(
            parasite_modes,
            "Pas de mode porte parasite sur une requête catégories seule : %s" % qs,
        )

    def test_contract_inv_08_combinaison_complete_promo_deux_cat_collection_origine(self):
        cats = self.env["product.public.category"].search(
            [
                "|",
                ("website_id", "=", False),
                ("website_id", "=", self.website.id),
            ],
            limit=2,
        )
        coll = self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_shop_collection_demo_saint_anne",
            raise_if_not_found=False,
        )
        origin = self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_shop_origin_demo_guadeloupe",
            raise_if_not_found=False,
        )
        if len(cats) < 2 or not coll or not origin or not coll.slug or not origin.slug:
            self.skipTest("Données démo insuffisantes (2 catégories, collection, origine).")
        IrHttp = self.env["ir.http"].sudo()
        s1, s2 = IrHttp._slug(cats[0]), IrHttp._slug(cats[1])
        url = (
            "/shop?ckr_mode=promo&ckr_category=%s&ckr_category=%s"
            "&ckr_origin=%s&ckr_collection=%s"
            % (s1, s2, origin.slug, coll.slug)
        )
        r = self.url_open(url, timeout=60)
        self.assertEqual(r.status_code, 200)
        self.assertIn("ckr-shop-hero--retail", r.text)
        self.assertNotIn("ckr-shop-hero--context", r.text)
        qs, _c = self._canonical_query_dict(r.text)
        self.assertIn("promo", qs.get("ckr_mode", []))
        self.assertGreaterEqual(len(qs.get("ckr_category", [])), 2)
        self.assertIn(origin.slug, qs.get("ckr_origin", []))
        self.assertIn(coll.slug, qs.get("ckr_collection", []))
        self.assertNotIn("origin", qs.get("ckr_mode", []))

    def test_contract_inv_09_chip_tout_reset_sans_parametres_residuels(self):
        # ``search=`` masque la barre chips (``ckr_shop_show_shortcuts``) : on
        # vérifie min/max + facettes CK sans terme de recherche.
        r = self.url_open(
            "/shop?ckr_mode=promo&ckr_collection_scope=all"
            "&min_price=1&max_price=999",
            timeout=60,
        )
        self.assertEqual(r.status_code, 200)
        hrefs = self._shortcut_chip_hrefs(r.text)
        self.assertTrue(hrefs)
        first = html.unescape(hrefs[0])
        p = urlparse(first)
        self.assertTrue(
            p.path == "/shop" or p.path.endswith("/shop"),
            "Chip Toute la sélection : chemin boutique nu attendu, obtenu %r" % first,
        )
        q = parse_qs(p.query)
        for key in (
            "ckr_mode",
            "ckr_origin",
            "ckr_collection",
            "ckr_category",
            "search",
            "min_price",
            "max_price",
        ):
            self.assertNotIn(
                key,
                q,
                "Reset global : aucun paramètre résiduel %s dans %r" % (key, first),
            )

    def test_contract_inv_10_legacy_url_ckr_mode_origin_encore_valide(self):
        origin = self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_shop_origin_demo_guadeloupe",
            raise_if_not_found=False,
        )
        if not origin or not origin.slug:
            self.skipTest("Origine démo Guadeloupe absente.")
        r = self.url_open(
            "/shop?ckr_mode=origin&ckr_origin=%s" % origin.slug,
            timeout=60,
        )
        self.assertEqual(r.status_code, 200)
        m_all = re.search(
            r'<input([^>]*class="[^"]*ckr-sidebar-origin-all[^"]*"[^>]*)>',
            r.text,
        )
        self.assertTrue(m_all)
        self.assertFalse(self._input_has_checked(m_all.group(1)))
        self._assert_specific_facet_checked(r.text, "origin", origin.slug)

    def test_contract_inv_11_sidebar_facet_hrefs_pas_de_routes_paralleles(self):
        r = self.url_open("/shop", timeout=60)
        self.assertEqual(r.status_code, 200)
        self._assert_sidebar_facet_hrefs_clean(r.text)

    def test_contract_inv_12_dom_marqueurs_facettes_pour_js(self):
        r = self.url_open("/shop", timeout=60)
        self.assertEqual(r.status_code, 200)
        low = r.text
        def _facet_input_tags(fragment, needle, exclude=None):
            """Balises `<input>` contenant ``needle`` en classe hors ``exclude``."""
            exclude = exclude or ""
            tags = []
            for m in re.finditer(r"<input\b[^>]*>", fragment, flags=re.I):
                tag = m.group(0)
                tl = tag.lower()
                if needle.lower() in tl and exclude.lower() not in tl:
                    tags.append(tag)
            return tags

        if self.env["product.public.category"].search(
            [
                "|",
                ("website_id", "=", False),
                ("website_id", "=", self.website.id),
            ],
            limit=1,
        ):
            for tag in _facet_input_tags(
                low, "ckr-sidebar-cat-check", exclude="ckr-sidebar-cat-all"
            ):
                self.assertRegex(
                    tag,
                    r"data-category-slug\s*=",
                    "Attribut data-category-slug requis pour le JS catégories.",
                )

        if self.env["ckr.shop.collection"].sudo().search([], limit=1):
            for tag in _facet_input_tags(
                low,
                "ckr-sidebar-collection-check",
                exclude="ckr-sidebar-collection-all",
            ):
                self.assertRegex(
                    tag,
                    r"data-slug\s*=",
                    "Attribut data-slug requis pour les collections.",
                )

        if self.env["ckr.shop.origin"].sudo().search([], limit=1):
            for tag in _facet_input_tags(
                low,
                "ckr-sidebar-origin-check",
                exclude="ckr-sidebar-origin-all",
            ):
                self.assertRegex(
                    tag,
                    r"data-slug\s*=",
                    "Attribut data-slug requis pour les origines.",
                )

        if not (
            self.env["product.public.category"].search(
                [
                    "|",
                    ("website_id", "=", False),
                    ("website_id", "=", self.website.id),
                ],
                limit=1,
            )
            or self.env["ckr.shop.collection"].sudo().search([], limit=1)
            or self.env["ckr.shop.origin"].sudo().search([], limit=1)
        ):
            self.skipTest("Aucune facette CK en base pour data-*.")

    def test_contract_inv_13_price_slider_value_matches_query_selection(self):
        """Le double curseur Prix reflète la sélection ``min_price`` / ``max_price`` de l’URL.

        Régression : les paramètres de route ne sont pas dans ``post`` passé à
        ``_get_additional_shop_values`` ; sans lecture de la query HTTP, le serveur
        pouvait injecter ``available_max_price`` dans ``value=`` alors que la grille
        appliquait bien le plafond demandé.
        """
        r = self.url_open("/shop?min_price=1.8&max_price=3.2", timeout=60)
        self.assertEqual(r.status_code, 200)
        m = re.search(
            r'<input[^>]*class="[^"]*\bform-range\b[^"]*\brange-with-input\b[^"]*"[^>]*value="([^"]+)"',
            r.text,
            re.I,
        )
        self.assertTrue(m, "Input « range-with-input » du bloc Prix introuvable.")
        parts = m.group(1).split(",")
        self.assertEqual(len(parts), 2, "Attendu value« min,max » pour le double curseur.")
        low, high = float(parts[0]), float(parts[1])
        self.assertAlmostEqual(low, 1.8, places=2)
        self.assertAlmostEqual(high, 3.2, places=2)
