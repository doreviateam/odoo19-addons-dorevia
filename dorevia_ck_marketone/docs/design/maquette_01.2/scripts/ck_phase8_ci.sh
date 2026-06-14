#!/usr/bin/env bash
# Gate portable Phase 8 — page /recettes M2 · sans Playwright.
#
#   1. upgrade dorevia_ck_theme
#   2. tests Odoo --test-tags=dorevia_ck_theme_phase8
#   3. smoke curl /recettes · non-régression Phases 1–7

set -euo pipefail

DB="${CK_CI_DB:-dorevia_ck_marketone_01}"
CONTAINER="${CK_CI_CONTAINER:-sandbox-odoo19-odoo-1}"
BASE_URL="${CK_CI_BASE_URL:-http://localhost:18079}"
TEST_HTTP_PORT="${CK_CI_TEST_HTTP_PORT:-8077}"
MODULES="dorevia_ck_theme,dorevia_ck_marketone_content"
TEST_TAG="dorevia_ck_theme_phase8"
RECIPES_PATH="/recettes"
PRODUCER_PATH="/producteur/atelier-hauts-goyaviers"

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

curl_smoke_absent() {
  local path="$1"
  shift
  local tmp code
  tmp="$(curl_fetch "$path")"
  code="$(cat "${tmp}.code")"
  rm -f "${tmp}.code"
  [[ "$code" == "200" ]] || fail "Smoke ${path} → HTTP ${code}"
  for needle in "$@"; do
    if grep -qF "$needle" "$tmp"; then
      rm -f "$tmp"
      fail "Smoke ${path} : chaîne interdite présente → ${needle}"
    fi
  done
  rm -f "$tmp"
  printf '  ✓ %s → 200 · absent: %s\n' "$path" "$*"
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

discover_product_path() {
  local shop_tmp code path
  shop_tmp="$(curl_fetch "/shop")"
  code="$(cat "${shop_tmp}.code")"
  rm -f "${shop_tmp}.code"
  [[ "$code" == "200" ]] || fail "Découverte produit : /shop → HTTP ${code}"
  path="$(grep -oE 'href="/shop/[^"/]+-[0-9]+"' "$shop_tmp" | head -1 | sed -E 's/href="([^"]+)"/\1/')"
  rm -f "$shop_tmp"
  [[ -n "$path" ]] || fail "Aucun produit publié sur /shop"
  printf '%s' "$path"
}

resolve_product_path() {
  if [[ -n "${CK_CI_PRODUCT_PATH:-}" ]]; then
    printf '%s' "$CK_CI_PRODUCT_PATH"
    return
  fi
  discover_product_path
}

log "Gate portable Phase 8 · base=${DB} · modules=${MODULES}"

log "1/3 — Upgrade ${MODULES} sur ${DB}"
docker exec "$CONTAINER" odoo -d "$DB" -i dorevia_ck_marketone_content -u "$MODULES" --stop-after-init

if [[ "${CK_CI_SKIP_RESTART:-0}" != "1" ]]; then
  log "Redémarrage conteneur ${CONTAINER}"
  docker restart "$CONTAINER" >/dev/null
  wait_for_odoo
fi

log "2/3 — Tests Odoo --test-tags=${TEST_TAG}"
docker exec "$CONTAINER" odoo -d "$DB" \
  --test-enable \
  --stop-after-init \
  --test-tags="${TEST_TAG}" \
  --http-port="${TEST_HTTP_PORT}"

PRODUCT_PATH="$(resolve_product_path)"
log "3/3 — Smoke curl (sans Playwright) · produit=${PRODUCT_PATH}"

curl_smoke "${RECIPES_PATH}" "ck-recipes-page" "Recettes & savoirs CK" "ck-recipes-cards" "Clafoutis créole au goyavier" "<html" "web.assets_frontend"
curl_smoke_absent "${RECIPES_PATH}" "fiche-produit.html" "website_blog"
curl_smoke "${PRODUCER_PATH}" "ck-producer-page" "Atelier Les Hauts Goyaviers"
curl_smoke "/contactus" "ck-contact-page"
curl_smoke "/a-propos" "ck-about-page"
curl_smoke "/professionnels" "ck-pro-page"
curl_smoke "${PRODUCT_PATH}" "ck-product-page"
curl_smoke "/shop/cart" "o_website_sale_checkout_container"
curl_smoke "/shop" "s_ck_shop_intro"

home_tmp="$(curl_fetch "/")"
home_code="$(cat "${home_tmp}.code")"
rm -f "${home_tmp}.code"
[[ "$home_code" == "200" ]] || fail "Smoke / → HTTP ${home_code}"
grep -qF 'ck-featured-products__grid--stable' "$home_tmp" || fail "Smoke / : vedettes SSR absentes"
rm -f "$home_tmp"
printf "  ✓ / → 200 · vedettes SSR Phase 2\n"

log "Gate portable Phase 8 : OK"
log "Recette UX complémentaire (optionnelle) :"
printf '  node %s/ck_phase8_desktop1280.mjs\n' "$ROOT"
printf '  node %s/ck_phase8_mobile390.mjs\n' "$ROOT"
