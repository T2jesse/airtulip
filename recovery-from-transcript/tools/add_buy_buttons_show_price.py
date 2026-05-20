"""One-off: ensure buy_buttons.settings.show_price exists in all locale schema files."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCALES = ROOT / "locales"

COPY: dict[str, dict[str, str]] = {
    "en.default": {
        "label": "Show price in this block",
        "info": "Turn on if customers only see price here. Turn off when the Price block is in the product column so the amount is not shown twice.",
    },
    "de": {
        "label": "Preis in diesem Block anzeigen",
        "info": "Aktivieren, wenn der Preis nur hier erscheinen soll. Deaktivieren, wenn der Preisblock in der Produktspalte verwendet wird, damit der Betrag nicht doppelt angezeigt wird.",
    },
    "fr": {
        "label": "Afficher le prix dans ce bloc",
        "info": "Activez si le prix n’apparaît qu’ici. Désactivez si le bloc Prix est dans la colonne produit pour éviter un doublon.",
    },
    "es": {
        "label": "Mostrar el precio en este bloque",
        "info": "Actívalo si el precio solo debe verse aquí. Desactívalo si ya usas el bloque Precio en la columna del producto para no duplicarlo.",
    },
    "it": {
        "label": "Mostra il prezzo in questo blocco",
        "info": "Attivalo se il prezzo compare solo qui. Disattivalo se usi già il blocco Prezzo nella colonna del prodotto per evitare duplicati.",
    },
    "vi": {
        "label": "Hiển thị giá trong khối này",
        "info": "Bật nếu giá chỉ hiển thị ở đây. Tắt nếu đã dùng khối Giá ở cột thông tin sản phẩm để tránh hiển thị hai lần.",
    },
}


def split_prefix(raw: str) -> tuple[str, str]:
    m = re.match(r"^(/\*[\s\S]*?\*/\s*)", raw)
    if m:
        return m.group(1), raw[m.end() :]
    return "", raw


def copy_for(filename: str) -> dict[str, str]:
    stem = Path(filename).stem.replace(".schema", "")
    # en.default.schema.json -> en.default
    if stem == "en.default.schema":
        key = "en.default"
    else:
        key = stem.replace(".schema", "")
    if key in COPY:
        return COPY[key]
    return COPY["en.default"]


def main() -> None:
    for path in sorted(LOCALES.glob("*.schema.json")):
        raw = path.read_text(encoding="utf-8")
        prefix, body = split_prefix(raw)
        data = json.loads(body)
        main_blocks = (
            data.get("sections", {}).get("main-product", {}).get("blocks", {})
        )
        bb = main_blocks.get("buy_buttons")
        if not bb or "settings" not in bb:
            continue
        s = bb["settings"]
        if "show_price" in s:
            continue
        new_settings: dict = {}
        strings = copy_for(path.name)
        for k, v in s.items():
            new_settings[k] = v
            if k == "show_quantity_selector":
                new_settings["show_price"] = {
                    "label": strings["label"],
                    "info": strings["info"],
                }
        if "show_price" not in new_settings:
            # buy_buttons existed but no quantity_selector (unlikely)
            new_settings = {"show_price": strings, **new_settings}
        bb["settings"] = new_settings
        out = prefix + json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        path.write_text(out, encoding="utf-8")
        print("updated", path.name)


if __name__ == "__main__":
    main()
