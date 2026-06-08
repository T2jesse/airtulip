#!/usr/bin/env python3
"""Extract human-readable inventory from templates/page.about.json."""
import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
path = ROOT / "templates" / "page.about.json"
data = json.loads(path.read_text(encoding="utf-8"))


def strip_html(s: str) -> str:
    if not s:
        return ""
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    return re.sub(r"\s+", " ", s).strip()


def fmt_shopify_asset(val) -> str:
    if not val:
        return "(none)"
    if isinstance(val, str):
        return val.replace("shopify://", "") if val.startswith("shopify://") else val
    return str(val)


lines: list[str] = []
lines.append("=" * 80)
lines.append("AIRTULIP — ABOUT PAGE INVENTORY")
lines.append("Source: templates/page.about.json (live theme #180129235234)")
lines.append("Live URL: https://airtulip.co/pages/about")
lines.append("Generated for rebuild planning — sections, copy, images, CTAs")
lines.append("=" * 80)
lines.append("")
lines.append("SUMMARY")
lines.append("-" * 40)
lines.append(f"Total sections: {len(data['order'])}")
lines.append("Template: page.about")
lines.append("")
lines.append("SECTION ORDER (top to bottom):")
for i, sid in enumerate(data["order"], 1):
    stype = data["sections"][sid]["type"]
    lines.append(f"  {i:2}. [{sid}] -> {stype}")
lines.append("")

types = Counter(data["sections"][s]["type"] for s in data["order"])
lines.append("SECTION TYPE COUNTS:")
for t, c in types.most_common():
    lines.append(f"  - {t}: {c}")
lines.append("")

lines.append("CTA BUTTONS ON PAGE:")
cta_count = 0
for sid in data["order"]:
    sec = data["sections"][sid]
    settings = sec.get("settings", {})
    if settings.get("button_label"):
        cta_count += 1
        lines.append(
            f'  - [{sid}] section: "{settings["button_label"]}" -> '
            f'{fmt_shopify_asset(settings.get("button_link"))}'
        )
    for bid, block in sec.get("blocks", {}).items():
        bs = block.get("settings", {})
        if block.get("type") == "button" and bs.get("button_label"):
            cta_count += 1
            lines.append(
                f'  - [{sid}/{bid}] block: "{bs["button_label"]}" -> '
                f'{fmt_shopify_asset(bs.get("button_link"))}'
            )
lines.append(f"  Total CTAs: {cta_count}")
lines.append("")

lines.append("=" * 80)
lines.append("SECTION-BY-SECTION DETAIL")
lines.append("=" * 80)

for idx, sid in enumerate(data["order"], 1):
    sec = data["sections"][sid]
    stype = sec["type"]
    settings = sec.get("settings", {})
    lines.append("")
    lines.append(f"## {idx}. {sid}")
    lines.append(f"Type: {stype}")

    key_settings = []
    for k in [
        "heading",
        "subheading",
        "description",
        "heading_size",
        "heading_alignment",
        "heading_tag",
        "text_alignment",
        "text_alignment_mobile",
        "layout",
        "image_width",
        "image_height",
        "padding_top",
        "padding_bottom",
        "narrow",
        "full_width",
        "rounded",
        "divider",
        "button_label",
        "button_link",
        "overlay_opacity",
        "heading_position",
    ]:
        if k in settings and settings[k] not in ("", None, False):
            val = settings[k]
            if k == "description" and isinstance(val, str) and len(val) > 220:
                val = strip_html(val)[:220] + "..."
            key_settings.append(f"  {k}: {val}")

    for media_k in ["image", "video", "video_url", "video_url_mobile"]:
        if settings.get(media_k):
            key_settings.append(f"  {media_k}: {fmt_shopify_asset(settings[media_k])}")

    if key_settings:
        lines.append("Settings:")
        lines.extend(key_settings)

    blocks = sec.get("blocks", {})
    block_order = sec.get("block_order", [])
    if blocks:
        lines.append(f"Blocks ({len(block_order)}):")
        for bid in block_order:
            block = blocks[bid]
            btype = block["type"]
            bs = block.get("settings", {})
            lines.append(f"  - [{bid}] type={btype}")
            if bs.get("heading"):
                lines.append(f"      heading: {bs['heading']}")
            if bs.get("text"):
                text_plain = strip_html(bs["text"])
                if len(text_plain) > 600:
                    text_plain = text_plain[:600] + "..."
                lines.append(f"      text: {text_plain}")
            if bs.get("button_label"):
                lines.append(
                    f"      button: {bs['button_label']} -> "
                    f"{fmt_shopify_asset(bs.get('button_link'))}"
                )
            if bs.get("icon_image"):
                lines.append(f"      icon_image: {fmt_shopify_asset(bs['icon_image'])}")

    if stype == "custom-liquid" and settings.get("liquid"):
        imgs = re.findall(r'src=["\']([^"\']+)["\']', settings["liquid"])
        if imgs:
            lines.append("  Embedded images (custom liquid):")
            for img in imgs:
                lines.append(f"    - {img}")

lines.append("")
lines.append("=" * 80)
lines.append("NARRATIVE ARC (current story flow)")
lines.append("=" * 80)
lines.append("")
arcs = [
    ("1. PAGE TITLE", "main-page — H1 About AirTulip"),
    (
        "2. OPENING PITCH",
        "rich-text — Sacred sleep intro + cleanroom bubble headline (centered)",
    ),
    (
        "3. LAMINAR FLOW INTRO",
        "image-with-text — Turbulence/particles + laminar shield + image",
    ),
    ("4. SCIENCE PREAMBLE", "rich-text — Aerospace tools paragraph"),
    ("5. VIDEO", "video — Laser footage MP4 + YouTube fallback"),
    (
        "6. LAMINAR EXPLAINER",
        "image-with-text — Controlled laminar airflow definition",
    ),
    (
        "7. PATENTS + SHOP CTA",
        "rich-text — Cleanroom/ICU context, patents, Shop Now",
    ),
    (
        "8-11. OUR JOURNEY",
        "4x image-with-text — Shark Tank, Matt Judon, Kickstarter/NYC, NY+Detroit + Invest CTA",
    ),
    (
        "12. FOUNDER STORY",
        "image-with-text — Long narrative + Arjen bio (duplicates journey)",
    ),
    (
        "13-15. HOW WE MAKE IT",
        "3x image-with-text — LaVision/TU Delft, TU Eindhoven, Owls + Shop",
    ),
    (
        "16. FOUR PILLARS",
        "lookbook — Hotspot grid (Aerodynamics, Measurement, Simulation, Testing)",
    ),
    (
        "17-22. HEALTH SCIENCE",
        "rich-text + custom images — Air quality, particles, clean zone, Build Differently",
    ),
    (
        "23-25. ENGINEERING",
        "3x image-with-text — 3D printing, H14 filters, manufacturing + Shop",
    ),
]
for title, desc in arcs:
    lines.append(title)
    lines.append(f"  {desc}")
    lines.append("")

lines.append("=" * 80)
lines.append("REBUILD OBSERVATIONS")
lines.append("=" * 80)
lines.append("")
observations = [
    "LENGTH: 25 sections — very long; Shark Tank, Matt Judon, Kickstarter repeat 2-3 times.",
    "STRUCTURE: Mostly image-with-text + rich-text; no chapter nav or progressive disclosure.",
    'CTAs: 6x "Shop Now" + 1x "Invest in AirTulip" scattered mid-page.',
    "DUPLICATION: Founder Story repeats Our Journey almost verbatim.",
    "CUSTOM LIQUID: 2 hardcoded CDN images — not theme-editor friendly.",
    "IMAGE REUSE: custom_resized_55ade92c... used in laminar intro AND Four Pillars lookbook.",
    "LOOKBOOK: Four Pillars hotspot UI may be hard to scan on mobile.",
    "PADDING: Most sections use padding 8px top/bottom — very tight.",
    "MISSING: Consolidated timeline, product specs, subscription/warranty in one place.",
    "STRENGTHS: Strong science partners, health education, credible founder story.",
    "SUGGESTED CHAPTERS: Hero | Science | How it works | Proof | Founder | Build | Health | CTA",
]
for o in observations:
    lines.append(f"- {o}")
lines.append("")

lines.append("=" * 80)
lines.append("ALL IMAGES & MEDIA (deduplicated)")
lines.append("=" * 80)
lines.append("")
media = []
for sid in data["order"]:
    sec = data["sections"][sid]
    s = sec.get("settings", {})
    for k in ["image", "video", "video_url"]:
        if s.get(k):
            media.append((sid, k, fmt_shopify_asset(s[k])))
    for bid, block in sec.get("blocks", {}).items():
        bs = block.get("settings", {})
        if bs.get("icon_image"):
            media.append((f"{sid}/{bid}", "icon_image", fmt_shopify_asset(bs["icon_image"])))
    if sec["type"] == "custom-liquid":
        imgs = re.findall(r'src=["\']([^"\']+)["\']', s.get("liquid", ""))
        for img in imgs:
            media.append((sid, "embedded", img))

seen = set()
for loc, kind, val in media:
    if val in seen:
        continue
    seen.add(val)
    lines.append(f"  [{loc}] {kind}: {val}")

out = ROOT / "content" / "page-about-inventory.txt"
out.write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {out} ({len(lines)} lines)")
