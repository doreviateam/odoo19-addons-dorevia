#!/usr/bin/env bash
# Gate portable Phase 10 — header / menu / branding · GO §5undecies ciblé.
#
#   1. upgrade dorevia_ck_theme
#   2. tests Odoo --test-tags=dorevia_ck_theme_phase10
#   3. smoke curl header + non-régression routes

set -euo pipefail

DB="${CK_CI_DB:-dorevia_ck_marketone_01}"
CONTAINER="${CK_CI_CONTAINER:-sandbox-odoo19-odoo-1}"
BASE_URL="${CK_CI_BASE_URL:-http://localhost:18079}"
TEST_HTTP_PORT="${CK_CI_TEST_HTTP_PORT:-8077}"
MODULES="dorevia_ck_theme"
TEST_TAG="dorevia_ck_theme_phase10"

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
  [[ "$code" == "200" ]] || fail "Smoke ${path} → HTTP ${code}"
  for needle in "$@"; do
    grep -qF "$needle" "$tmp" || fail "Smoke ${path} : absent → ${needle}"
  done
  rm -f "$tmp"
  printf '  ✓ %s → 200 · %s\n' "$path" "$*"
}

log "Gate Phase 10 header · base=${DB} · module=${MODULES}"

log "1/3 — Upgrade ${MODULES}"
docker exec "$CONTAINER" odoo -d "$DB" -u "$MODULES" --stop-after-init

if [[ "${CK_CI_SKIP_RESTART:-0}" != "1" ]]; then
  docker restart "$CONTAINER" >/dev/null
  sleep 8
fi

log "2/3 — Tests Odoo --test-tags=${TEST_TAG}"
docker exec "$CONTAINER" odoo -d "$DB" \
  --test-enable \
  --stop-after-init \
  --test-tags="${TEST_TAG}" \
  --http-port="${TEST_HTTP_PORT}"

log "3/3 — Smoke header + routes"
curl_smoke "/?qa_ts=phase10" "ck-header" "C-Kreyol" "Boutique" "Découvrir" "o_mega_menu"
curl_smoke "/shop?qa_ts=phase10" "ck-header" "s_ck_shop_intro"
curl_smoke "/professionnels?qa_ts=phase10" "ck-header" "ck-pro-page"
curl_smoke "/contactus?qa_ts=phase10" "ck-header" "ck-contact-page"
curl_smoke "/a-propos?qa_ts=phase10" "ck-header" "ck-about-page"
curl_smoke "/recettes?qa_ts=phase10" "ck-header" "ck-recipes-page"
curl_smoke "/producteur/atelier-hauts-goyaviers?qa_ts=phase10" "ck-header" "ck-producer-page"

log "Gate Phase 10 header : OK"
