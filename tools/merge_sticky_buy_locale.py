"""Merge sticky_buy_button settings into all locale schema files (preserves comments)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOCALES = ROOT / "locales"

EXTRA: dict[str, dict] = {
    "en": {
        "layout": {
            "label": "Layout",
            "options__1": {"label": "Full width bottom bar"},
            "options__2": {"label": "Floating card"},
        },
        "show_thumbnail": {"label": "Show product thumbnail"},
        "desktop_max_width_percent": {
            "label": "Desktop max width",
            "info": "For full width layout only. Limits how wide the bar is on large screens (the bar stays centered).",
        },
    },
    "de": {
        "layout": {
            "label": "Layout",
            "options__1": {"label": "Volle Breite unten"},
            "options__2": {"label": "Schwebende Karte"},
        },
        "show_thumbnail": {"label": "Produktminiatur anzeigen"},
        "desktop_max_width_percent": {
            "label": "Maximale Breite (Desktop)",
            "info": "Nur bei Layout „Volle Breite“. Begrenzt die Balkenbreite auf großen Bildschirmen (mittig ausgerichtet).",
        },
    },
    "fr": {
        "layout": {
            "label": "Mise en page",
            "options__1": {"label": "Barre pleine largeur en bas"},
            "options__2": {"label": "Carte flottante"},
        },
        "show_thumbnail": {"label": "Afficher la miniature du produit"},
        "desktop_max_width_percent": {
            "label": "Largeur max. sur ordinateur",
            "info": "Uniquement pour la barre pleine largeur. Limite la largeur sur grands écrans (la barre reste centrée).",
        },
    },
    "es": {
        "layout": {
            "label": "Diseño",
            "options__1": {"label": "Barra inferior a todo el ancho"},
            "options__2": {"label": "Tarjeta flotante"},
        },
        "show_thumbnail": {"label": "Mostrar miniatura del producto"},
        "desktop_max_width_percent": {
            "label": "Ancho máx. en escritorio",
            "info": "Solo para la barra a todo el ancho. Limita el ancho en pantallas grandes (la barra sigue centrada).",
        },
    },
    "it": {
        "layout": {
            "label": "Layout",
            "options__1": {"label": "Barra inferiore a tutta larghezza"},
            "options__2": {"label": "Scheda flottante"},
        },
        "show_thumbnail": {"label": "Mostra anteprima prodotto"},
        "desktop_max_width_percent": {
            "label": "Larghezza massima (desktop)",
            "info": "Solo per il layout a tutta larghezza. Limita la larghezza su schermi grandi (la barra resta centrata).",
        },
    },
    "vi": {
        "layout": {
            "label": "Bố cục",
            "options__1": {"label": "Thanh dưới cùng full width"},
            "options__2": {"label": "Thẻ nổi"},
        },
        "show_thumbnail": {"label": "Hiển thị ảnh thu nhỏ sản phẩm"},
        "desktop_max_width_percent": {
            "label": "Chiều rộng tối đa trên desktop",
            "info": "Chỉ áp dụng cho bố cục full width. Giới hạn độ rộng thanh trên màn hình lớn (thanh được căn giữa).",
        },
    },
}


def split_prefix(raw: str) -> tuple[str, str]:
    m = re.match(r"^(/\*[\s\S]*?\*/\s*)", raw)
    if m:
        return m.group(1), raw[m.end() :]
    return "", raw


def lang_key(filename: str) -> str:
    base = filename.replace(".schema.json", "")
    if base == "en.default" or base.startswith("en."):
        return "en"
    # pt-BR → pt (falls back to EN in merge_strings if not in EXTRA)
    if "-" in base:
        return base.split("-")[0]
    return base


def merge_strings(filename: str) -> dict:
    lk = lang_key(filename)
    if lk in EXTRA:
        return EXTRA[lk]
    # pt-BR, zh-CN, etc. → English
    return EXTRA["en"]


def main() -> None:
    for path in sorted(LOCALES.glob("*.schema.json")):
        raw = path.read_text(encoding="utf-8")
        prefix, body = split_prefix(raw)
        data = json.loads(body)
        blocks = data.get("sections", {}).get("main-product", {}).get("blocks", {})
        sticky = blocks.get("sticky_buy_button")
        if not sticky or "settings" not in sticky:
            continue
        extra = merge_strings(path.name)
        for k, v in extra.items():
            sticky["settings"][k] = v
        out = prefix + json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        path.write_text(out, encoding="utf-8")
        print("merged", path.name)


if __name__ == "__main__":
    main()
