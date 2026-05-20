"""Patch main-product PDP: replace description + accordions with tabbed_content block."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "product.json"

CONTENT = r"""/*
 * ------------------------------------------------------------
 * IMPORTANT: The contents of this file are auto-generated.
 *
 * This file may be updated by the Shopify admin theme editor
 * or related systems. Please exercise caution as any changes
 * made to this file may be overwritten.
 * ------------------------------------------------------------
 */
"""

FEATURES_HTML = "<p><strong>Aerodynamics Technology</strong></p><ul><li>Patent-pending</li><li>Advanced laminar air flow technology</li><li>Particulate-free air zone where you sleep</li></ul><p><strong>3 Modes</strong></p><ul><li>Whisper mode for quietest operation</li><li>Night mode for the most stable bubble</li><li>Day mode for high cleaning power of the entire room</li></ul><p><strong>Advanced Acoustics</strong></p><ul><li>Own fan design using noise reduction technology</li><li>Computer generated curved acoustic insulation channels</li><li>26 dB(A) in whisper mode</li><li>30 dB(A) in night mode</li></ul><p><strong>Cleanroom Filters</strong></p><ul><li>Dual Industrial HEPA-H14 Filters in metal cassettes (single in Twin)</li><li>Dual full-width Active Carbon Filters (single in Twin)</li><li>2 Pre-filters (1 in Twin)</li></ul><p><strong>Local bespoke Production</strong></p><ul><li>All our products are sustainable and handcrafted in New York City</li></ul>"

DIMENSIONS_HTML = "<p></p><p><strong>AirTulip Queen</strong></p><ul><li>Fits Full and Queen size beds</li><li>Width: 70\" | Depth: 11\" | Height: 45\"</li><li>Comes with 2 sets of legs to adjust the height to your mattress</li><li>Weight: 130 lbs</li></ul><p></p><p><strong>AirTulip King</strong></p><ul><li>Fits King and California King beds</li><li>Width: 79\" | Depth: 11\" | Height: 45\"</li><li>Comes with 2 sets of legs to adjust the height to your mattress</li><li>Weight: 130 lbs</li></ul><p></p><p><strong>AirTulip Twin</strong></p><ul><li>Fits Twin size and childrens beds</li><li>Width: 42\" | Depth: 11\" | Height: 45\"</li><li>Comes with 2 sets of legs to adjust the height to your mattress</li><li>Weight: 80 lbs</li></ul>"

DELIVERY_HTML = "<p><strong>Headboard fulfillment:</strong> AirTulip Sleep is <strong>made to order</strong> with an approximately <strong>8-week production lead time</strong>. We keep you informed on build progress and your estimated ship date.</p><p><strong>Replacement filters:</strong> Typical delivery is within about <strong>two weeks</strong> when ordered separately.</p>"


def main():
    raw = TEMPLATE.read_text(encoding="utf-8")
    body = re.sub(r"/\*.*?\*/", "", raw, flags=re.DOTALL)
    data = json.loads(body)

    blocks = data["sections"]["main-product"]["blocks"]
    for key in ["description", "text_DnpMLq", "collapsible_tab_cyMLKH", "collapsible_tab_VnYrLG", "collapsible_tab_6yPCkk"]:
        blocks.pop(key, None)

    blocks["pdp_product_tabs"] = {
        "type": "tabbed_content",
        "settings": {
            "style": "with-border",
            "tab_count": "4",
            "tab_1_show_product_description": True,
            "tab_1_heading": "Overview",
            "tab_1_icon": "none",
            "tab_1_content": "",
            "tab_2_heading": "Features & Details",
            "tab_2_icon": "check_mark",
            "tab_2_content": FEATURES_HTML,
            "tab_2_page": "",
            "tab_3_heading": "Dimensions",
            "tab_3_icon": "map_pin",
            "tab_3_content": DIMENSIONS_HTML,
            "tab_3_page": "headboard-dimensions",
            "tab_4_heading": "Delivery & Shipping",
            "tab_4_icon": "truck",
            "tab_4_content": DELIVERY_HTML,
            "tab_4_page": "",
        },
    }

    order = data["sections"]["main-product"]["block_order"]
    new_order = []
    for bid in order:
        if bid in {
            "description",
            "text_DnpMLq",
            "collapsible_tab_cyMLKH",
            "collapsible_tab_VnYrLG",
            "collapsible_tab_6yPCkk",
        }:
            continue
        new_order.append(bid)
        if bid == "liquid_f9YK6r":
            new_order.append("pdp_product_tabs")
    data["sections"]["main-product"]["block_order"] = new_order

    TEMPLATE.write_text(CONTENT + json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print("patched", TEMPLATE)


if __name__ == "__main__":
    main()
