#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"

index="$root/index.html"
css="$root/styles.css"

fail() {
  echo "ERROR: $*" >&2
  exit 1
}

[[ -f "$index" ]] || fail "Missing index.html"
[[ -f "$css" ]] || fail "Missing styles.css"

grep -Eiq "<!doctype html>" "$index" || fail "Missing HTML5 doctype"
grep -Eiq "<html[^>]*lang=" "$index" || fail "Missing <html lang=...>"
grep -Eiq "<meta[^>]*charset=" "$index" || fail "Missing <meta charset=...>"
grep -Eiq "name=['\\\"]viewport['\\\"]" "$index" || fail "Missing viewport meta"
grep -Eiq "name=['\\\"]description['\\\"]" "$index" || fail "Missing description meta"
grep -Eiq "name=['\\\"]theme-color['\\\"]" "$index" || fail "Missing theme-color meta"
grep -Eiq "<link[^>]*rel=['\\\"]stylesheet['\\\"][^>]*href=['\\\"]styles\\.css['\\\"]" "$index" || fail "Missing stylesheet link to styles.css"
grep -Eq "Hello World" "$index" || fail "Missing 'Hello World' text"

echo "OK: basic HTML structure checks passed."
