# -*- coding: utf-8 -*-
"""Modèle CK « profil origine » — porte Origines (`/shop?ckr_mode=origin`).

Couche CK **légère** (pas A5) qui **décore** et **route** la lecture
visiteur de la porte Origines (voir
``docs/mvp_01/CONTRAT_URL_ORIGINES.md`` §13 et
``docs/mvp_01/SPEC_IMPL_ORIGINES.md`` §2.2 / §2.3) :

* la **vérité catalogue** « ce produit est rattaché à telle origine »
  reste portée par le **socle standard Odoo** — un
  ``product.attribute.value`` dédié (attribut « Origine ») référencé
  depuis les ``product.template`` via les lignes d'attribut standard
  (``attribute_line_ids.value_ids``) ;
* ``ckr.shop.origin`` ne **duplique pas** la liste des produits : il
  ne porte que les **métadonnées éditoriales §3.1** (nom visiteur,
  phrase de contexte, slug stable, ordre, publication) — utilisées
  pour le **bandeau**, la **fiche produit** et le **routage URL**.

Contraintes SQL verrouillées (**SPEC_IMPL §2.2**) :

* ``unique(website_id, slug)`` → unicité logique du slug par site
  (multi-site prévu ; v1 = ``website_id`` renseigné si fourni, NULL
  accepté si mono-site).
* ``unique(website_id, attribute_value_id)`` → une seule ligne CK par
  valeur catalogue et par site (pas de doublon de profil).

Droits (**SPEC_IMPL §2.3** + ``security/ir.model.access.csv``) :

* employés (``base.group_user``) : lecture seule ;
* éditeurs site (``website.group_website_designer``) : CRUD ;
* aucun accès public — le contrôleur lit en ``sudo()``.
"""
import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


# Caractères autorisés dans un slug stable (même règle que la
# normalisation habituelle Odoo : minuscules ASCII + chiffres + tirets).
# Volontairement strict : évite toute collision avec les séparateurs
# d'URL et les encodages visuels équivoques ("_" exclu pour réserver
# le tiret comme seul séparateur intra-slug).
_CKR_ORIGIN_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class CkrShopOrigin(models.Model):
    _name = "ckr.shop.origin"
    _description = "C-Kreyol — Profil éditorial d'origine (porte /shop?ckr_mode=origin)"
    _order = "sequence, name_visitor, id"

    # ------------------------------------------------------------------
    # Lien à la valeur catalogue (source de vérité du rattachement produit)
    # ------------------------------------------------------------------
    attribute_value_id = fields.Many2one(
        comodel_name="product.attribute.value",
        string="Valeur d'attribut « Origine »",
        required=True,
        ondelete="cascade",
        index=True,
        help=(
            "Valeur d'attribut catalogue (attribut « Origine ») qui porte "
            "le rattachement produit ↔ origine. La vérité métier "
            "« ce produit est rattaché à telle origine » reste côté "
            "standard Odoo ; ce profil ne fait que décorer cette valeur."
        ),
    )

    # ------------------------------------------------------------------
    # Métadonnées éditoriales §3.1 (CONTRAT_URL_ORIGINES)
    # ------------------------------------------------------------------
    name_visitor = fields.Char(
        string="Nom visiteur",
        translate=True,
        help=(
            "Libellé affiché au visiteur (bandeau, fiche produit). À défaut, "
            "fallback sur le nom de la valeur d'attribut."
        ),
    )
    context_phrase = fields.Char(
        string="Phrase de contexte",
        translate=True,
        help=(
            "Phrase courte affichée sous le titre du bandeau lorsqu'une "
            "seule origine est active. Optionnelle ; repli sur la copy "
            "par défaut (cf. SPEC_IMPL §6.1)."
        ),
    )
    slug = fields.Char(
        string="Slug",
        required=True,
        index=True,
        help=(
            "Identifiant stable utilisé dans l'URL (`ckr_origin=<slug>`). "
            "Minuscules, chiffres et tirets uniquement."
        ),
    )
    sequence = fields.Integer(
        string="Ordre d'affichage",
        default=10,
        help="Ordre d'affichage dans les listes éditoriales (tri secondaire).",
    )
    website_id = fields.Many2one(
        comodel_name="website",
        string="Site web",
        ondelete="cascade",
        index=True,
        help=(
            "Site web sur lequel le profil est exposé. Laisser vide "
            "pour un profil non scopé (mono-site / disponible partout)."
        ),
    )
    website_published = fields.Boolean(
        string="Publié",
        default=True,
        help="Si décoché, le profil est ignoré par les contrôleurs front.",
    )

    # ------------------------------------------------------------------
    # Champs calculés (affichage liste back-office)
    # ------------------------------------------------------------------
    display_name_visitor = fields.Char(
        string="Nom visiteur (affiché)",
        compute="_compute_display_name_visitor",
        help=(
            "Nom visiteur effectif : `name_visitor` si renseigné, sinon "
            "nom de la valeur d'attribut liée."
        ),
    )

    # ------------------------------------------------------------------
    # Contraintes SQL (SPEC_IMPL §2.2) — API ``models.Constraint`` Odoo 19
    # ------------------------------------------------------------------
    _ckr_shop_origin_slug_website_uniq = models.Constraint(
        "unique(website_id, slug)",
        "Le slug d'une origine doit être unique par site.",
    )
    _ckr_shop_origin_value_website_uniq = models.Constraint(
        "unique(website_id, attribute_value_id)",
        "Une seule ligne CK par valeur d'attribut et par site.",
    )

    # ------------------------------------------------------------------
    # Validation Python (normalisation slug)
    # ------------------------------------------------------------------
    @api.constrains("slug")
    def _check_slug_format(self):
        for record in self:
            slug = (record.slug or "").strip()
            if not slug:
                raise ValidationError(_("Le slug d'origine ne peut pas être vide."))
            if not _CKR_ORIGIN_SLUG_RE.match(slug):
                raise ValidationError(
                    _(
                        "Le slug d'origine « %s » n'est pas valide : "
                        "minuscules ASCII, chiffres et tirets uniquement, "
                        "pas de tiret en début/fin."
                    )
                    % slug
                )

    @api.constrains("slug", "website_id")
    def _check_slug_scope_uniqueness(self):
        """Empêche les doublons de slug en scope global ``website_id=NULL``."""
        for record in self:
            slug = (record.slug or "").strip()
            if not slug:
                continue
            domain = [("id", "!=", record.id), ("slug", "=", slug)]
            if record.website_id:
                domain.append(("website_id", "=", record.website_id.id))
                scope_label = _("sur le site « %s »") % (record.website_id.name,)
            else:
                domain.append(("website_id", "=", False))
                scope_label = _("dans le périmètre global (sans site)")
            if self.sudo().search_count(domain):
                raise ValidationError(
                    _("Le slug d'origine « %(slug)s » existe déjà %(scope)s.")
                    % {"slug": slug, "scope": scope_label}
                )

    @api.depends("name_visitor", "attribute_value_id.name")
    def _compute_display_name_visitor(self):
        for record in self:
            record.display_name_visitor = (
                record.name_visitor or record.attribute_value_id.name or ""
            )

    # ------------------------------------------------------------------
    # Résolution pour le contrôleur (SPEC_IMPL §3.2 / §5)
    # ------------------------------------------------------------------
    @api.model
    def _ckr_sidebar_origin_prefer(self, new_o, old_o, website=None):
        """Choisit le profil à afficher quand plusieurs lignes partagent la même valeur catalogue."""

        def tier(rec):
            if website and rec.website_id and rec.website_id.id == website.id:
                return 0
            if not rec.website_id:
                return 1
            return 2

        tn, to = tier(new_o), tier(old_o)
        if tn != to:
            return new_o if tn < to else old_o
        if new_o.sequence != old_o.sequence:
            return new_o if new_o.sequence < old_o.sequence else old_o
        return new_o if new_o.id < old_o.id else old_o

    @api.model
    def _ckr_merge_sidebar_origins(self, origins, website=None):
        """Dédoublonne le rail Origines (même ``attribute_value_id``, ex. profil global + profil site)."""
        if not origins:
            return origins
        best_by_value = {}
        for o in origins:
            vid = o.attribute_value_id.id
            prev = best_by_value.get(vid)
            if prev is None:
                best_by_value[vid] = o
            else:
                best_by_value[vid] = self._ckr_sidebar_origin_prefer(
                    o, prev, website=website
                )
        merged = self.browse([best_by_value[k].id for k in sorted(best_by_value.keys())])
        return merged.sorted(
            key=lambda r: (r.sequence, r.name_visitor or "", r.id),
        )

    @api.model
    def _ckr_resolve_published_slugs(self, slugs, website=None):
        """Résout un itérable de slugs en profils publiés (sans doublons).

        :param slugs: itérable de chaînes ``slug``.
        :param website: ``website.website`` ou ``None``. Si fourni, restreint
            la résolution aux profils scopés sur ce site ou non scopés
            (``website_id = NULL``). Si ``None``, aucune restriction site.

        :returns: ``ckr.shop.origin`` (recordset) des profils publiés
            trouvés, dans l'ordre d'apparition des slugs en entrée
            (dédupliqué). Les slugs inconnus sont ignorés — la gestion
            du repli HTTP 302 (§3.3) est à la charge du contrôleur.
        """
        normalized = []
        seen = set()
        for raw in slugs or ():
            value = (raw or "").strip().lower()
            if not value or value in seen:
                continue
            seen.add(value)
            normalized.append(value)
        if not normalized:
            return self.browse()

        domain = [("slug", "in", normalized), ("website_published", "=", True)]
        if website is not None:
            domain.append(("website_id", "in", [False, website.id]))

        records = self.sudo().search(domain)
        if not records:
            return records

        by_slug = {rec.slug: rec for rec in records}
        ordered_ids = [by_slug[s].id for s in normalized if s in by_slug]
        return self.browse(ordered_ids)
