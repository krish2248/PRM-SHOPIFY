"""
Apply the new MRP pricing from `price-mapping.json` to Shopify product variants.

Source of truth: "NEW MRP (2).xls"  ->  price-mapping.json
Rule: listing price = per-unit MRP x pack count in the product title.

Setup (one-time):
  1. Shopify admin -> Settings -> Apps and sales channels -> Develop apps
  2. Create app -> "Price Updater"
  3. Admin API scopes: read_products, write_products
  4. Install app -> copy the Admin API access token (shpat_...)
  5. PowerShell:  $env:SHOPIFY_ADMIN_TOKEN="shpat_xxxxxxxxxx"

Run:
  python update-prices.py                 # DRY RUN - prints what would change, writes nothing
  python update-prices.py --apply         # actually writes prices
  python update-prices.py --apply --include-decisions   # also applies the needs_decision rows
  python update-prices.py --rollback backup-YYYY.json   # restore prices from a backup file

Every --apply run writes a timestamped backup of the previous prices first.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

STORE = "prm-herbovilla.myshopify.com"
API_VERSION = "2024-10"
TOKEN = os.environ.get("SHOPIFY_ADMIN_TOKEN")
HERE = os.path.dirname(os.path.abspath(__file__))
MAPPING_FILE = os.path.join(HERE, "price-mapping.json")


def api(method, path, body=None):
    url = f"https://{STORE}/admin/api/{API_VERSION}/{path}"
    headers = {
        "X-Shopify-Access-Token": TOKEN,
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read().decode()[:400]}", file=sys.stderr)
        raise


def fetch_product(handle):
    res = api("GET", f"products.json?handle={handle}")
    products = res.get("products", [])
    return products[0] if products else None


def pick_variant(product, variant_title):
    """Return the variant matching variant_title, or the sole variant if unspecified."""
    variants = product["variants"]
    if variant_title:
        for v in variants:
            if v["title"].strip().lower() == variant_title.strip().lower():
                return v
        return None
    if len(variants) == 1:
        return variants[0]
    return None  # ambiguous - refuse to guess


def set_price(variant_id, price):
    body = {"variant": {"id": variant_id, "price": f"{price:.2f}"}}
    return api("PUT", f"variants/{variant_id}.json", body)


def resolve(rows):
    """Look up each mapping row against the live store. Returns (plan, problems)."""
    plan, problems = [], []
    for row in rows:
        handle = row["handle"]
        product = fetch_product(handle)
        time.sleep(0.3)
        if not product:
            problems.append((row["excel"], f"product not found: {handle[:70]}"))
            continue
        variant = pick_variant(product, row.get("variant"))
        if not variant:
            problems.append((row["excel"], f"variant '{row.get('variant')}' not resolvable ({len(product['variants'])} variants)"))
            continue
        plan.append({
            "excel": row["excel"],
            "title": product["title"],
            "handle": handle,
            "variant_id": variant["id"],
            "variant_title": variant["title"],
            "live_price": float(variant["price"]),
            "new_price": float(row["new_price"]),
            "mrp": row["mrp"],
            "pack": row["pack"],
        })
    return plan, problems


def print_plan(plan):
    print(f"\n{'EXCEL ITEM':<32} {'MRP':>5} {'x':>2} {'LIVE':>9} {'->':^4} {'NEW':>9}   {'DELTA':>9}")
    print("-" * 92)
    changed = 0
    for p in plan:
        delta = p["new_price"] - p["live_price"]
        flag = "" if abs(delta) > 0.001 else "  (no change)"
        if abs(delta) > 0.001:
            changed += 1
        print(f'{p["excel"][:31]:<32} {p["mrp"]:>5} {p["pack"]:>2} {p["live_price"]:>9.2f} {"->":^4} {p["new_price"]:>9.2f}   {delta:>+9.2f}{flag}')
    print("-" * 92)
    print(f"{len(plan)} variants resolved, {changed} would change.")
    return changed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="write prices (default is dry run)")
    ap.add_argument("--include-decisions", action="store_true", help="also apply needs_decision rows")
    ap.add_argument("--rollback", metavar="BACKUP_JSON", help="restore prices from a backup file")
    args = ap.parse_args()

    if not TOKEN:
        print("ERROR: SHOPIFY_ADMIN_TOKEN env var not set. See the header of this file.", file=sys.stderr)
        sys.exit(1)

    if args.rollback:
        with open(args.rollback, encoding="utf-8") as f:
            backup = json.load(f)
        print(f"Restoring {len(backup)} variant prices from {args.rollback} ...")
        for b in backup:
            set_price(b["variant_id"], b["live_price"])
            print(f'  {b["excel"][:40]:<42} -> {b["live_price"]:.2f}')
            time.sleep(0.4)
        print("Rollback complete.")
        return

    with open(MAPPING_FILE, encoding="utf-8") as f:
        mapping = json.load(f)

    rows = list(mapping["confident"])
    if args.include_decisions:
        rows += mapping["needs_decision"]
    else:
        print(f"NOTE: skipping {len(mapping['needs_decision'])} needs_decision rows "
              f"(pass --include-decisions to apply them).")
    if mapping["not_on_store"]:
        print(f"NOTE: {len(mapping['not_on_store'])} sheet rows have no matching store product: "
              + ", ".join(r["excel"] for r in mapping["not_on_store"]))

    print(f"\nResolving {len(rows)} rows against {STORE} ...")
    plan, problems = resolve(rows)

    if problems:
        print("\n--- UNRESOLVED ---")
        for name, why in problems:
            print(f"  {name}: {why}")

    changed = print_plan(plan)

    if not args.apply:
        print("\nDRY RUN - nothing written. Re-run with --apply to commit these prices.")
        return

    stamp = time.strftime("%Y%m%d-%H%M%S")
    backup_path = os.path.join(HERE, f"price-backup-{stamp}.json")
    with open(backup_path, "w", encoding="utf-8") as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)
    print(f"\nBackup of current prices written to {backup_path}")

    if changed == 0:
        print("Nothing to change.")
        return

    print(f"\nApplying {changed} price updates ...")
    failures = []
    for p in plan:
        if abs(p["new_price"] - p["live_price"]) < 0.001:
            continue
        try:
            set_price(p["variant_id"], p["new_price"])
            print(f'  OK  {p["excel"][:40]:<42} {p["live_price"]:.2f} -> {p["new_price"]:.2f}')
        except urllib.error.HTTPError:
            failures.append(p["excel"])
        time.sleep(0.4)

    if failures:
        print("\n--- FAILED ---")
        for name in failures:
            print(f"  {name}")
        print(f"\nRollback with:  python update-prices.py --rollback {os.path.basename(backup_path)}")
    else:
        print(f"\nAll {changed} prices updated. "
              f"Rollback with:  python update-prices.py --rollback {os.path.basename(backup_path)}")


if __name__ == "__main__":
    main()
