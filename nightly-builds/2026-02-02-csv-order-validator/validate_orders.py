#!/usr/bin/env python3
"""Dreamcore Order CSV Validator

Validates a CSV export (e.g., from Google Sheets/Excel) before it is imported into
any downstream system (HubSpot, accounting, fulfillment tooling).

Design goals:
- Fail loudly (non-zero exit) on hard errors
- Produce a human-readable report for ops
- Provide an optional cleaned CSV output

No external deps.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "customer_name",
    "phone",
    "email",
    "sku",
    "qty",
    "unit_price",
]


@dataclass
class Issue:
    severity: str  # ERROR|WARN
    row: int       # 1-indexed data row (excluding header); 0 for file-level
    column: str
    message: str


def normalize_phone_sg(raw: str) -> Tuple[str, Optional[str]]:
    """Return (normalized, warning_message).

    Normal form: 8 digits (e.g., 91234567). Accepts formats with +65, spaces,
    hyphens. Does not attempt to normalize non-SG numbers.
    """
    s = (raw or "").strip()
    if not s:
        return s, None

    # Remove common separators
    t = re.sub(r"[\s\-()]+", "", s)

    # Strip +65 / 65 prefix
    if t.startswith("+65"):
        t = t[3:]
    elif t.startswith("65") and len(t) > 8:
        t = t[2:]

    if len(t) == 8 and t.isdigit() and t[0] in {"6", "8", "9"}:
        if t != s:
            return t, f"Normalized phone from '{s}' -> '{t}'"
        return t, None

    # If it's digits but not SG shape, leave it and warn
    if any(ch.isdigit() for ch in t):
        return s, "Phone not normalized (non-SG or unexpected format)"

    return s, "Phone contains no digits"


def parse_date(raw: str) -> Tuple[Optional[str], Optional[str]]:
    """Return (iso_date, error_message)."""
    s = (raw or "").strip()
    if not s:
        return None, "Missing order_date"

    # Common spreadsheet formats
    fmts = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%m/%d/%Y",
        "%Y/%m/%d",
    ]
    for fmt in fmts:
        try:
            dt = datetime.strptime(s, fmt)
            return dt.date().isoformat(), None
        except ValueError:
            pass

    return None, f"Unparseable date '{s}' (expected YYYY-MM-DD or DD/MM/YYYY etc.)"


def read_csv(path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError("CSV appears to have no header row")
        headers = [h.strip() for h in reader.fieldnames]
        rows: List[Dict[str, str]] = []
        for row in reader:
            # Normalize keys to stripped header names
            normalized = {k.strip(): (v or "").strip() for k, v in row.items() if k is not None}
            rows.append(normalized)
        return headers, rows


def validate(headers: List[str], rows: List[Dict[str, str]], allow_warnings: bool) -> Tuple[List[Issue], List[Dict[str, str]]]:
    issues: List[Issue] = []
    cleaned_rows: List[Dict[str, str]] = []

    header_set = {h for h in headers if h}
    for col in REQUIRED_COLUMNS:
        if col not in header_set:
            issues.append(Issue("ERROR", 0, col, "Missing required column"))

    # If required columns missing, stop early (cleaning depends on them)
    if any(i.severity == "ERROR" and i.row == 0 for i in issues):
        return issues, cleaned_rows

    seen_line_items = set()  # (order_id, sku)

    for idx, row in enumerate(rows, start=1):
        cleaned = dict(row)

        # Detect empty rows (common in exports)
        if all((row.get(c, "").strip() == "") for c in headers):
            issues.append(Issue("WARN", idx, "*", "Empty row"))
            if allow_warnings:
                continue

        # order_id
        order_id = row.get("order_id", "").strip()
        if not order_id:
            issues.append(Issue("ERROR", idx, "order_id", "Missing order_id"))

        # sku
        sku = row.get("sku", "").strip()
        if not sku:
            issues.append(Issue("ERROR", idx, "sku", "Missing sku"))

        if order_id and sku:
            key = (order_id, sku)
            if key in seen_line_items:
                issues.append(Issue("ERROR", idx, "order_id/sku", f"Duplicate line item for order_id={order_id}, sku={sku}"))
            else:
                seen_line_items.add(key)

        # date
        iso, err = parse_date(row.get("order_date", ""))
        if err:
            issues.append(Issue("ERROR", idx, "order_date", err))
        else:
            cleaned["order_date"] = iso or row.get("order_date", "")

        # email
        email = row.get("email", "").strip()
        if not email:
            issues.append(Issue("ERROR", idx, "email", "Missing email"))
        elif not EMAIL_RE.match(email):
            issues.append(Issue("ERROR", idx, "email", f"Invalid email '{email}'"))

        # customer_name
        name = row.get("customer_name", "").strip()
        if not name:
            issues.append(Issue("ERROR", idx, "customer_name", "Missing customer_name"))

        # phone
        phone_raw = row.get("phone", "").strip()
        if not phone_raw:
            issues.append(Issue("WARN", idx, "phone", "Missing phone"))
        else:
            normalized, warn = normalize_phone_sg(phone_raw)
            cleaned["phone"] = normalized
            if warn:
                issues.append(Issue("WARN", idx, "phone", warn))

        # qty
        qty_raw = row.get("qty", "").strip()
        try:
            qty = int(qty_raw)
            if qty <= 0:
                issues.append(Issue("ERROR", idx, "qty", "qty must be > 0"))
        except ValueError:
            issues.append(Issue("ERROR", idx, "qty", f"qty must be an integer (got '{qty_raw}')"))

        # unit_price
        price_raw = row.get("unit_price", "").strip()
        try:
            price = float(price_raw)
            if price < 0:
                issues.append(Issue("ERROR", idx, "unit_price", "unit_price must be >= 0"))
            # Normalize to 2dp string
            cleaned["unit_price"] = f"{price:.2f}"
        except ValueError:
            issues.append(Issue("ERROR", idx, "unit_price", f"unit_price must be a number (got '{price_raw}')"))

        cleaned_rows.append(cleaned)

    return issues, cleaned_rows


def print_report(issues: List[Issue]) -> None:
    errors = [i for i in issues if i.severity == "ERROR"]
    warns = [i for i in issues if i.severity == "WARN"]

    print("=== Order CSV Validation Report ===")
    print(f"Errors: {len(errors)} | Warnings: {len(warns)}")

    if issues:
        print("\nDetails:")
        for i in issues:
            where = "file" if i.row == 0 else f"row {i.row}"
            print(f"- {i.severity:<5} {where:<6} col={i.column}: {i.message}")


def write_clean_csv(out_path: Path, headers: List[str], cleaned_rows: List[Dict[str, str]]) -> None:
    # Preserve original header order; include required columns even if not in original order
    header_order = list(dict.fromkeys(headers + REQUIRED_COLUMNS))
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=header_order)
        writer.writeheader()
        for row in cleaned_rows:
            writer.writerow({h: row.get(h, "") for h in header_order})


def main(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(description="Validate Dreamcore order CSV exports before importing.")
    ap.add_argument("csv_path", type=Path, help="Path to input CSV")
    ap.add_argument("--out", type=Path, default=None, help="Optional path to write a cleaned CSV")
    ap.add_argument("--allow-warnings", action="store_true", help="Do not fail (exit 2) on warnings")
    args = ap.parse_args(argv)

    if not args.csv_path.exists():
        print(f"Input file not found: {args.csv_path}", file=sys.stderr)
        return 1

    try:
        headers, rows = read_csv(args.csv_path)
    except Exception as e:
        print(f"Failed to read CSV: {e}", file=sys.stderr)
        return 1

    issues, cleaned_rows = validate(headers, rows, allow_warnings=args.allow_warnings)
    print_report(issues)

    if args.out:
        try:
            write_clean_csv(args.out, headers, cleaned_rows)
            print(f"\nWrote cleaned CSV: {args.out}")
        except Exception as e:
            print(f"Failed to write cleaned CSV: {e}", file=sys.stderr)
            return 1

    errors = [i for i in issues if i.severity == "ERROR"]
    warns = [i for i in issues if i.severity == "WARN"]

    if errors:
        return 3
    if warns and not args.allow_warnings:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
