#!/usr/bin/env bash
# Gate portable Phase 3 — shop CK · sans Playwright.
#
# Prouve le contrat module après -u dorevia_ck_theme :
#   1. upgrade module
#   2. tests Odoo taggés dorevia_ck_theme_phase3
#   3. smoke curl minimal / · /shop · catégorie Épicerie créole
#
# Usage :
#   ./ck_phase3_ci.sh
#   CK_CI_DB=ma_base CK_CI_BASE_URL=http://localhost:8069 ./ck_phase3_ci.sh
#
# Variables :
#   CK_CI_DB              Base Odoo (défaut : dorevia_ck_marketone_01)
#   CK_CI_CONTAINER       Conteneur Docker Odoo (défaut : sandbox-odoo19-odoo-1)
#   CK_CI_BASE_URL        URL front (défaut : http://localhost:18079)
#   CK_CI_CATEGORY_PATH   Chemin catégorie smoke (défaut : /shop/category/epicerie-creole-1)
#   CK_CI_TEST_HTTP_PORT  Port HTTP tests Odoo (défaut : 8072)
#   CK_CI_SKIP_RESTART    Si "1", ne pas redémarrer le conteneur après upgrade
#
# Playwright (ck_phase3_desktop1280.mjs · mobile390) : recette UX complémentaire, hors gate.

set -euo pipefail

DB="${CK_CI_DB:-dorevia_ck_marketone_01}"
CONTAINER="${CK_CI_CONTAINER:-sandbox-odoo19-odoo-1}"
BASE_URL="${CK_CI_BASE_URL:-http://localhost:18079}"
CATEGORY_PATH="${CK_CI_CATEGORY_PATH:-/shop/category/epicerie-creole-1}"
TEST_HTTP_PORT="${CK_CI_TEST_HTTP_PORT:-8072}"
MODULES="dorevia_ck_theme,dorevia_ck_marketone_content"
TEST_TAG="dorevia_ck_theme_phase3"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

log() { printf '\n▶ %s\n' "$*"; }
fail() { printf '\n✗ %s\n' "$*" >&2; exit 1; }

curl_fetch() {
  local path="$1"
  local tmp
  tmp="$(mktemp)"
  local code
  code="$(curl -sS -o "$tmp" -w '%{http_code}' \
    -H "X-Odoo-Database: ${DB}" \
    "${BASE_URL}${path}")"
  printf '%s\n' "$code" > "${tmp}.code"
  echo "$tmp"
}

curl_smoke() {
  local path="$1"
  shift
  local tmp code
  tmp="$(curl_fetch "$path")"
  code="$(cat "${tmp}.code")"
  rm -f "${tmp}.code"
  if [[ "$code" != "200" ]]; then
    rm -f "$tmp"
    fail "Smoke ${path} → HTTP ${code} (attendu 200)"
  fi
  for needle in "$@"; do
    if ! grep -qF "$needle" "$tmp"; then
      rm -f "$tmp"
      fail "Smoke ${path} : chaîne absente → ${needle}"
    fi
  done
  rm -f "$tmp"
  printf '  ✓ %s → 200 · %s\n' "$path" "$*"
}

wait_for_odoo() {
  local attempt
  for attempt in $(seq 1 30); do
    if curl -sS -o /dev/null -w '%{http_code}' -H "X-Odoo-Database: ${DB}" "${BASE_URL}/web" | grep -qE '200|303|302'; then
      return 0
    fi
    sleep 2
  done
  fail "Odoo inaccessible sur ${BASE_URL} après redémarrage"
}

log "Gate portable Phase 3 · base=${DB} · modules=${MODULES}"

log "1/3 — Upgrade ${MODULES} sur ${DB}"
docker exec "$CONTAINER" odoo -d "$DB" -i dorevia_ck_marketone_content -u "$MODULES" --stop-after-init

if [[ "${CK_CI_SKIP_RESTART:-0}" != "1" ]]; then
  log "Redémarrage conteneur ${CONTAINER} (registry vues)"
  docker restart "$CONTAINER" >/dev/null
  wait_for_odoo
fi

log "2/3 — Tests Odoo --test-tags=${TEST_TAG}"
docker exec "$CONTAINER" odoo -d "$DB" \
  --test-enable \
  --stop-after-init \
  --test-tags="${TEST_TAG}" \
  --http-port="${TEST_HTTP_PORT}"

log "3/3 — Smoke curl (sans Playwright)"

home_tmp="$(curl_fetch "/")"
home_code="$(cat "${home_tmp}.code")"
rm -f "${home_tmp}.code"
[[ "$home_code" == "200" ]] || fail "Smoke / → HTTP ${home_code}"
grep -qF 'ck-featured-products__grid--stable' "$home_tmp" || fail "Smoke / : grille SSR stable absente"
grep -qF 's_ck_shop_intro' "$home_tmp" && fail "Smoke / : s_ck_shop_intro ne doit pas être sur la home"
rm -f "$home_tmp"
printf "  ✓ / → 200 · vedettes SSR · pas d'intro shop\n"

curl_smoke "/shop" "s_ck_shop_intro" "ck-shop-page" "Boutique C-Kreyol"
curl_smoke "${CATEGORY_PATH}" "o_wsale_category_description"

log "Gate portable Phase 3 : OK"
log "Recette UX complémentaire (optionnelle, hors gate) :"
printf '  node %s/ck_phase3_desktop1280.mjs\n' "$ROOT"
printf '  node %s/ck_phase3_mobile390.mjs\n' "$ROOT"
