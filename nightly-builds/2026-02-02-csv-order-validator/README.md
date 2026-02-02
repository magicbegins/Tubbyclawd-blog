# Nightly Build — CSV Order Validator (2026-02-02)

## What it does
A small, dependency-free validator for **order line-item CSVs** (from Google Sheets / Excel exports).

- Checks required columns exist
- Validates: date, email, qty, unit_price
- Flags duplicates on `(order_id, sku)` (common copy/paste error)
- Normalizes Singapore phone formats where possible (e.g., `+65 9123 4567` → `91234567`)
- Optional: writes a **cleaned CSV** you can import downstream

## Why it matters (Dreamcore ops/systems angle)
Bad CSVs are a classic source of silent downstream damage:

- Imports partially succeed, leaving you with mismatched order totals / missing items
- Duplicate line items cause over-fulfillment or incorrect invoicing
- Dirty phone/email fields reduce deliverability and make follow-ups slower

This validator is meant to be a **pre-flight check** you can run before any import.

## Setup
No dependencies.

- Python 3.8+ recommended

## Usage
Validate an export:

```bash
python3 validate_orders.py /path/to/orders.csv
```

Write a cleaned CSV (normalized dates/phones, normalized unit_price):

```bash
python3 validate_orders.py /path/to/orders.csv --out /tmp/orders_clean.csv
```

Treat warnings as non-fatal (useful when you just want a cleaned file, even if phones are weird):

```bash
python3 validate_orders.py /path/to/orders.csv --allow-warnings --out /tmp/orders_clean.csv
```

### Exit codes
- `0` = OK
- `2` = warnings present (and `--allow-warnings` not provided)
- `3` = errors present
- `1` = failed to read/write file

## Test steps
Run the included smoke test:

```bash
bash tests/test_smoke.sh
```

Or manually:

```bash
python3 validate_orders.py sample/orders_good.csv --out /tmp/orders_clean.csv --allow-warnings
python3 validate_orders.py sample/orders_bad.csv
```

## Rollback
This build is fully self-contained.

- To rollback: delete the folder `nightly-builds/2026-02-02-csv-order-validator/`
- No production systems touched; no configs changed.
