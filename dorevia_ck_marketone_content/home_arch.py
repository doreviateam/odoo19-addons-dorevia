# -*- coding: utf-8 -*-
"""Socle commun de manipulation d'arch — dédoublonnage et guard de re-seed CMS.

Centralise les utilitaires partagés (PR-2) :
- ``_arch_as_string`` : normalise ``arch_db`` (chaîne ou dict de traductions) en chaîne ;
- ``_arch_fingerprint`` : empreinte sha256 stable (guard anti-écrasement des pages CMS) ;
- ``should_reseed_home_section`` : règle B1 fournie en helper *futur* — pas câblée sur les
  bootstrappers home dans PR-2 (home pilotée code / self-healing conservé).

Module socle sans dépendance interne (importable partout sans cycle).
"""
import hashlib


def _arch_as_string(arch):
    """Normalise une arch (chaîne ou dict de traductions) en chaîne."""
    if isinstance(arch, dict):
        return next(iter(arch.values()), '')
    return arch or ''


def _arch_fingerprint(arch):
    """Empreinte sha256 stable d'une arch normalisée (guard anti-écrasement CMS)."""
    return hashlib.sha256(_arch_as_string(arch).encode('utf-8')).hexdigest()


def should_reseed_home_section(view, is_valid_fn):
    """Règle B1 (helper futur, non câblé en PR-2) : True si la section doit être (re)bootstrappée.

    - arch absente/vide → re-seed ;
    - arch invalide selon ``is_valid_fn`` → re-seed (self-healing après changement de markup) ;
    - arch valide → on ne touche pas (éditions MOA conservant une arch valide préservées).
    """
    arch = _arch_as_string(view.arch_db or view.arch)
    if not arch.strip():
        return True
    return not is_valid_fn(arch)
