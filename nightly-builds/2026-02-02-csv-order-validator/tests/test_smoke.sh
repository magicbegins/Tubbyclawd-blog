#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

python3 "$ROOT/validate_orders.py" "$ROOT/sample/orders_good.csv" --out /tmp/orders_clean.csv --allow-warnings

set +e
python3 "$ROOT/validate_orders.py" "$ROOT/sample/orders_bad.csv" >/tmp/orders_bad_report.txt 2>&1
code=$?
set -e

if [[ $code -eq 0 ]]; then
  echo "Expected failure on bad sample, got exit 0" >&2
  exit 1
fi

echo "Smoke tests OK (bad sample failed with exit code $code)"
