"""
Populate empty Shopify collections with products mapped from
collection-product-mapping.json. Uses the Shopify Admin REST API.

Setup (one-time):
  1. In Shopify admin -> Settings -> Apps and sales channels -> Develop apps
  2. Create app -> "Collection Populator"
  3. Configure Admin API scopes: write_products, write_publications, read_products
  4. Install app -> copy the Admin API access token (shpat_...)
  5. Save token as env var:  set SHOPIFY_ADMIN_TOKEN=shpat_xxxxxxxxxx
     (PowerShell: $env:SHOPIFY_ADMIN_TOKEN="shpat_xxxxxxxxxx")

Run:
  python populate-collections.py
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error

STORE = "prm-herbovilla.myshopify.com"
API_VERSION = "2024-10"
TOKEN = os.environ.get("SHOPIFY_ADMIN_TOKEN")
MAPPING_FILE = os.path.join(os.path.dirname(__file__), "collection-product-mapping.json")


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
        print(f"  HTTP {e.code}: {e.read().decode()}", file=sys.stderr)
        raise


def get_product_id_by_handle(handle):
    res = api("GET", f"products.json?handle={handle}&fields=id,handle")
    products = res.get("products", [])
    return products[0]["id"] if products else None


def add_product_to_collection(collection_id, product_id):
    body = {"collect": {"collection_id": collection_id, "product_id": product_id}}
    return api("POST", "collects.json", body)


def main():
    if not TOKEN:
        print("ERROR: SHOPIFY_ADMIN_TOKEN env var not set. See header for setup steps.", file=sys.stderr)
        sys.exit(1)

    with open(MAPPING_FILE, encoding="utf-8") as f:
        mapping = json.load(f)

    handle_to_id = {}
    failures = []

    for coll_handle, coll in mapping["collections"].items():
        collection_id = coll["id"]
        print(f"\n=== {coll_handle} (id={collection_id}) ===")
        for product_handle in coll["products"]:
            if product_handle not in handle_to_id:
                pid = get_product_id_by_handle(product_handle)
                if not pid:
                    print(f"  SKIP product not found: {product_handle[:80]}")
                    failures.append((coll_handle, product_handle))
                    continue
                handle_to_id[product_handle] = pid
                time.sleep(0.3)
            pid = handle_to_id[product_handle]
            try:
                add_product_to_collection(collection_id, pid)
                print(f"  OK  pid={pid}  {product_handle[:70]}")
            except urllib.error.HTTPError as e:
                if e.code == 422:
                    print(f"  EXISTS pid={pid}  {product_handle[:70]}")
                else:
                    failures.append((coll_handle, product_handle))
            time.sleep(0.4)

    if failures:
        print("\n--- FAILURES ---")
        for c, p in failures:
            print(f"  {c} <- {p}")
    else:
        print("\nAll products added successfully.")


if __name__ == "__main__":
    main()
