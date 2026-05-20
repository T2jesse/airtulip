"""
Patch locale schema JSON: Shop Pay installments block + remove legacy price setting.
Preserves leading /* ... */ comment if present.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LOCALES = REPO / "locales"

SHOP_PAY_BLOCK = {
    "name": "Shop Pay installments",
    "settings": {
        "paragraph": {
            "content": (
                "Shows installment messaging when Shop Pay installments are available. "
                "Add this block once, then drag it anywhere in the product information column."
            )
        }
    },
}


def split_prefix(raw: str) -> tuple[str, str]:
    m = re.match(r"^(/\*[\s\S]*?\*/\s*)", raw)
    if m:
        return m.group(1), raw[m.end() :]
    return "", raw


def patch_data(data: dict) -> bool:
    """Return True if modified."""
    sec = data.get("sections", {}).get("main-product")
    if not sec or "blocks" not in sec:
        return False
    blocks = sec["blocks"]
    changed = False
    if "price" in blocks and "settings" in blocks["price"]:
        if blocks["price"]["settings"].pop("show_shop_installments", None) is not None:
            changed = True
    if "shop_pay_installments" in blocks:
        return changed
    new_blocks: dict = {}
    inserted = False
    for k, v in blocks.items():
        new_blocks[k] = v
        if k == "price":
            new_blocks["shop_pay_installments"] = SHOP_PAY_BLOCK
            inserted = True
            changed = True
    if not inserted:
        new_blocks["shop_pay_installments"] = SHOP_PAY_BLOCK
        changed = True
    sec["blocks"] = new_blocks
    return changed


def main() -> None:
    for path in sorted(LOCALES.glob("*.schema.json")):
        raw = path.read_text(encoding="utf-8")
        prefix, body = split_prefix(raw)
        data = json.loads(body)
        if not patch_data(data):
            continue
        out = prefix + json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        path.write_text(out, encoding="utf-8")
        print("patched", path.name)


if __name__ == "__main__":
    main()
