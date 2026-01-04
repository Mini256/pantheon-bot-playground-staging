#!/usr/bin/env bash
set -euo pipefail

FILE="index.html"

if [[ ! -f "$FILE" ]]; then
  echo "ERROR: $FILE not found" >&2
  exit 1
fi

if ! grep -iq '<h1[^>]*> *hello world *</h1>' "$FILE"; then
  echo "ERROR: Missing <h1>Hello World</h1> in $FILE" >&2
  exit 1
fi

echo "index.html contains the expected Hello World heading."
