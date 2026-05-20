"""Rebuild templates/product.json PDP below-fold. Run from repo root: python tools/rebuild_product_pdp.py"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "product.json"


def load_theme_json(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    raw = re.sub(r"/\*.*?\*/", "", raw, flags=re.DOTALL)
    return json.loads(raw)


def save_theme_json(path: Path, data: dict) -> None:
    header = """/*
 * ------------------------------------------------------------
 * IMPORTANT: The contents of this file are auto-generated.
 *
 * This file may be updated by the Shopify admin theme editor
 * or related systems. Please exercise caution as any changes
 * made to this file may be overwritten.
 * ------------------------------------------------------------
 */
"""
    body = json.dumps(data, indent=2, ensure_ascii=False)
    path.write_text(header + body + "\n", encoding="utf-8")


def main() -> None:
    data = load_theme_json(TEMPLATE)
    sections = data["sections"]

    # --- Improve buy-box delivery tab (headboard lead time + filters) ---
    main = sections["main-product"]
    main["blocks"]["collapsible_tab_6yPCkk"]["settings"]["content"] = (
        "<p><strong>Headboard fulfillment:</strong> AirTulip Sleep is <strong>made to order</strong> with an approximately "
        "<strong>8-week production lead time</strong>. We keep you informed on build progress and your estimated ship date.</p>"
        "<p><strong>Replacement filters:</strong> Typical delivery is within about <strong>two weeks</strong> when ordered separately.</p>"
    )

    # --- New below-fold sections ---
    pdp_trust_signals = {
        "type": "multicolumn-with-icons",
        "blocks": {
            "t1": {
                "type": "column",
                "settings": {
                    "icon": "return",
                    "custom_icon": "",
                    "heading": "30-night sleep trial",
                    "text": "<p>Try it at home. If AirTulip Sleep is not right for you, return within 30 days for a full product refund (<strong>shipping both ways excluded</strong>)—see FAQ for details.</p>",
                    "highlighted_text": "none",
                    "highlighted_scribble": "circle",
                },
            },
            "t2": {
                "type": "column",
                "settings": {
                    "icon": "shield",
                    "custom_icon": "",
                    "heading": "One-year warranty",
                    "text": "<p>Manufacturing defects covered in year one. Pairing with an active <strong>filter subscription</strong> may unlock additional protection on the unit—confirm the current offer in your subscription app or FAQ.</p>",
                    "highlighted_text": "none",
                    "highlighted_scribble": "circle",
                },
            },
            "t3": {
                "type": "column",
                "settings": {
                    "icon": "map_pin",
                    "custom_icon": "",
                    "heading": "Hand-assembled in the U.S.",
                    "text": "<p>Proudly handcrafted in <strong>New York City and Detroit</strong>. Sized and upholstered for your bed—not mass-produced shelves.</p>",
                    "highlighted_text": "none",
                    "highlighted_scribble": "circle",
                },
            },
            "t4": {
                "type": "column",
                "settings": {
                    "icon": "time",
                    "custom_icon": "",
                    "heading": "Transparent lead time",
                    "text": "<p>Because each unit is made to order, expect roughly <strong>8 weeks</strong> before shipment. We communicate milestones so you can plan install and mattress height.</p>",
                    "highlighted_text": "none",
                    "highlighted_scribble": "circle",
                },
            },
        },
        "block_order": ["t1", "t2", "t3", "t4"],
        "settings": {
            "style": "with-border",
            "columns": 4,
            "text_alignment": "left",
            "heading": "Buying a headboard that purifies takes trust",
            "heading_size": "title-lg tracking-heading",
            "heading_alignment": "text-center md:items-center",
            "heading_tag": "h2",
            "subheading": "",
            "description": "",
            "button_label": "",
            "button_link": "",
            "button_external": False,
            "button_icon": True,
            "highlighted_text": "none",
            "highlighted_scribble": "circle",
            "color_text": "#171717",
            "color_background": "#fafafa",
            "gradient_background": "",
            "color_highlight": "",
            "gradient_highlight": "",
            "color_button_text": "",
            "color_button_background": "",
            "color_button_gradient": "",
            "padding_top": 48,
            "padding_bottom": 40,
            "divider": False,
            "full_width": False,
            "rounded": False,
        },
    }

    pdp_value_split = {
        "type": "split-text",
        "blocks": {
            "h1": {
                "type": "heading",
                "settings": {
                    "heading": "A clean-air zone at the headboard—not another floor purifier",
                    "heading_size": "title-lg-xl tracking-heading",
                    "heading_tag": "h2",
                },
            },
            "x1": {
                "type": "text",
                "settings": {
                    "text": "<p>AirTulip Sleep pulls air through industrial-grade filtration and delivers it across the headboard fabric using <strong>laminar, low-turbulence airflow</strong> aimed at your breathing zone—so cleaner air is directed where you actually breathe at night.</p><p>Use the tabs above for full specs; this section is the “why it exists” story serious buyers need before a four-figure decision.</p>",
                    "text_size": "subtext-md",
                },
            },
            "b1": {
                "type": "button",
                "settings": {
                    "button_label": "Read the engineering story",
                    "button_link": "/pages/about",
                    "button_style": "secondary",
                    "button_size": "md",
                    "button_icon": True,
                    "button_external": False,
                },
            },
        },
        "block_order": ["h1", "x1", "b1"],
        "settings": {
            "video_url": "",
            "video_description": "Background video",
            "split_video_autoplay": True,
            "split_video_loop": True,
            "video_mobile": "",
            "video_url_mobile": "",
            "media_flush_edge": False,
            "media_side": "right",
            "media_span_percent": 52,
            "media_shade": False,
            "image_heading_fallback": "",
            "image": "shopify://shop_images/AirTulipProductFrontAngle_square.jpg",
            "image_mobile": "",
            "video": "",
            "cover_image": "",
            "cover_image_mobile": "",
            "color_heading": "#0a1628",
            "color_supporting_text": "#394a60",
            "content_column_background": "#f8f7f6",
            "mobile_stack_background": "#ffffff",
            "desktop_text_align": "left",
            "heading_line_height_pct": 112,
            "content_alignment_mobile": "left",
            "split_overlay_stack_gap_px": 24,
            "min_height_px": 460,
            "min_height_px_mobile": 280,
            "rounded": True,
            "padding_top": 36,
            "padding_bottom": 36,
        },
    }

    pdp_how_it_works = {
        "type": "multicolumn-with-icons",
        "blocks": {
            "w1": {
                "type": "column",
                "settings": {
                    "icon": "lightning",
                    "custom_icon": "",
                    "heading": "Directed laminar airflow",
                    "text": "<p>Laminar delivery helps keep purified air cohesive on its way to you instead of dumping speed into turbulent room corners.</p>",
                    "highlighted_text": "none",
                    "highlighted_scribble": "circle",
                },
            },
            "w2": {
                "type": "column",
                "settings": {
                    "icon": "award",
                    "custom_icon": "",
                    "heading": "Industrial-grade HEPA H14 filtration",
                    "text": "<p>Dual certified HEPA H14 cartridges in steel cassettes (counts adjust for Twin) plus wide activated carbon layers for odors and VOCs.</p>",
                    "highlighted_text": "none",
                    "highlighted_scribble": "circle",
                },
            },
            "w3": {
                "type": "column",
                "settings": {
                    "icon": "organic",
                    "custom_icon": "",
                    "heading": "Whisper-level bedside acoustics",
                    "text": "<p>Published operating points land around <strong>26 dB(A)</strong> in Whisper and <strong>30 dB(A)</strong> in Night mode—engineered for sleep, not showroom CFM contests.</p>",
                    "highlighted_text": "none",
                    "highlighted_scribble": "circle",
                },
            },
        },
        "block_order": ["w1", "w2", "w3"],
        "settings": {
            "style": "with-border",
            "columns": 3,
            "text_alignment": "left",
            "heading": "What you are actually investing in",
            "heading_size": "title-lg tracking-heading",
            "heading_alignment": "text-center md:items-center",
            "heading_tag": "h2",
            "subheading": "",
            "description": "",
            "button_label": "",
            "button_link": "",
            "button_external": False,
            "button_icon": True,
            "highlighted_text": "none",
            "highlighted_scribble": "circle",
            "color_text": "",
            "color_background": "",
            "gradient_background": "",
            "color_highlight": "",
            "gradient_highlight": "",
            "color_button_text": "",
            "color_button_background": "",
            "color_button_gradient": "",
            "padding_top": 56,
            "padding_bottom": 48,
            "divider": False,
            "full_width": False,
            "rounded": False,
        },
    }

    pdp_science = {
        "type": "image-with-text",
        "blocks": {
            "im": {
                "type": "image",
                "settings": {
                    "image_width": "custom",
                    "image_max_width": 50,
                    "image_max_width_mobile": 50,
                },
            },
            "hd": {
                "type": "heading",
                "settings": {
                    "heading": "Performance you can contextualize",
                    "heading_size": "title-lg tracking-heading",
                    "heading_tag": "h2",
                    "highlighted_text": "none",
                    "highlighted_scribble": "circle",
                },
            },
            "tx": {
                "type": "text",
                "settings": {
                    "text": "<p>Marketing surfaces describe a clean-air zone that is <strong>orders of magnitude cleaner</strong> than typical purifier-in-a-room setups. The chart here is a shopper-friendly snapshot—pair it with your About page lab narrative for buyers who want receipts.</p>",
                    "text_font": "body",
                    "text_size": "subtext-md",
                    "text_max_size": 32,
                    "text_line_height": 1.6,
                    "text_letter_spacing": 0,
                    "text_capitalize": False,
                    "secondary_color": False,
                    "highlighted_text": "none",
                    "highlighted_scribble": "circle",
                },
            },
        },
        "block_order": ["im", "hd", "tx"],
        "settings": {
            "image": "shopify://shop_images/graph2.png",
            "image_height": "adapt",
            "image_width": "large",
            "layout": "image_first",
            "text_alignment": "left",
            "content_position": "align-self-center",
            "image_mobile": "",
            "image_height_mobile": "auto",
            "text_alignment_mobile": "left",
            "color_text": "#171717",
            "color_background": "",
            "gradient_background": "",
            "color_background_2": "#f4f7fb",
            "gradient_background_2": "",
            "color_highlight": "",
            "gradient_highlight": "",
            "color_button_text": "",
            "color_button_background": "",
            "color_button_gradient": "",
            "padding_top": 40,
            "padding_bottom": 40,
            "divider": False,
            "full_width": False,
            "rounded": False,
            "enable_parallax": False,
            "parallax_direction": "vertical",
        },
    }

    pdp_press = {
        "type": "logo-list",
        "blocks": {
            "l1": {
                "type": "logo",
                "settings": {
                    "image": "shopify://shop_images/shark-tank-logo-png_seeklogo-447416_1.png",
                    "height": 72,
                    "link": "https://abc.com/episode/0c007adc-1d90-4582-b5ab-a6064c91e1af/playlist/PL553044961",
                },
            },
            "l2": {
                "type": "logo",
                "settings": {
                    "image": "shopify://shop_images/images_1.png",
                    "height": 72,
                    "link": "https://www.forbes.com/sites/forbes-personal-shopper/article/air-quality-and-sleep/",
                },
            },
            "l3": {
                "type": "logo",
                "settings": {
                    "image": "shopify://shop_images/apartment-therapy-logo-vector_1.png",
                    "height": 72,
                    "link": "https://www.apartmenttherapy.com/air-tulip-air-purifying-headboard-review-37481462",
                },
            },
            "l4": {
                "type": "logo",
                "settings": {
                    "image": "shopify://shop_images/design-milk-logo-vector.png",
                    "height": 72,
                    "link": "https://design-milk.com/this-headboard-cleans-the-air-near-you-as-you-sleep/",
                },
            },
            "l5": {
                "type": "logo",
                "settings": {
                    "image": "shopify://shop_images/Fast_Company_Logo.png",
                    "height": 72,
                    "link": "https://www.fastcompany.com/90781651/this-clever-headboard-is-an-air-filter-in-disguise",
                },
            },
            "l6": {
                "type": "logo",
                "settings": {
                    "image": "shopify://shop_images/Eindhoven_University_of_Technology_logo_new.png",
                    "height": 72,
                    "link": "",
                },
            },
        },
        "block_order": ["l1", "l2", "l3", "l4", "l5", "l6"],
        "settings": {
            "layout": "default",
            "grid_horizontal": 60,
            "direction": "left",
            "speed": 6,
            "heading": "Press & research collaborators",
            "heading_size": "title-md",
            "heading_alignment": "text-center md:items-center",
            "heading_tag": "h2",
            "subheading": "",
            "description": "<p>Earned editorial coverage plus partnerships that informed validation work—serious shoppers expect to see both.</p>",
            "button_label": "",
            "button_link": "",
            "button_external": True,
            "button_icon": True,
            "highlighted_text": "none",
            "highlighted_scribble": "circle",
            "color_text": "",
            "color_background": "",
            "gradient_background": "",
            "color_highlight": "",
            "gradient_highlight": "",
            "color_button_text": "",
            "color_button_background": "",
            "color_button_gradient": "",
            "padding_top": 40,
            "padding_bottom": 24,
            "divider": False,
            "full_width": False,
            "rounded": False,
        },
    }

    pdp_video = sections["video_yrA9aV"].copy()
    pdp_video["settings"] = dict(
        pdp_video["settings"],
        **{
            "padding_top": 32,
            "padding_bottom": 32,
            "full_width": True,
            "description": "See AirTulip Sleep in motion",
        },
    )

    pdp_shark = {
        "type": "rich-text",
        "blocks": {
            "sh": {
                "type": "heading",
                "settings": {
                    "heading": "As seen on Shark Tank",
                    "heading_size": "title-md tracking-heading",
                    "heading_tag": "h2",
                    "highlighted_text": "none",
                    "highlighted_scribble": "circle",
                },
            },
            "st": {
                "type": "text",
                "settings": {
                    "text": "<p>Catch how we pitched air you can sleep in—stream the episode on <a href=\"https://abc.com/episode/0c007adc-1d90-4582-b5ab-a6064c91e1af/playlist/PL553044961\" target=\"_blank\" rel=\"noopener\">ABC</a> or <a href=\"https://www.hulu.com/\" target=\"_blank\" rel=\"noopener\">Hulu</a>.</p>",
                    "text_font": "body",
                    "text_size": "subtext-md",
                    "text_max_size": 32,
                    "text_line_height": 1.6,
                    "text_letter_spacing": 0,
                    "text_capitalize": False,
                    "secondary_color": False,
                    "highlighted_text": "none",
                    "highlighted_scribble": "circle",
                },
            },
        },
        "block_order": ["sh", "st"],
        "settings": {
            "text_alignment": "center",
            "text_alignment_mobile": "center",
            "heading": "",
            "heading_size": "title-md",
            "heading_alignment": "text-left md:items-end md:flex-row",
            "heading_width": "small",
            "heading_tag": "h2",
            "subheading": "",
            "description": "",
            "button_label": "",
            "button_link": "",
            "button_external": False,
            "button_icon": True,
            "highlighted_text": "none",
            "highlighted_scribble": "circle",
            "color_text": "",
            "color_background": "#f8f7f6",
            "gradient_background": "",
            "color_highlight": "",
            "gradient_highlight": "",
            "color_button_text": "",
            "color_button_background": "",
            "color_button_gradient": "",
            "padding_top": 28,
            "padding_bottom": 28,
            "divider": False,
            "narrow": True,
            "rounded": False,
        },
    }

    pdp_judge_carousel = json.loads(json.dumps(sections["17373031676a505831"]))
    pdp_judge_carousel["settings"] = dict(
        pdp_judge_carousel["settings"],
        **{"padding_top": 32, "padding_bottom": 32},
    )

    pdp_ownership = {
        "type": "image-with-text",
        "blocks": {
            "im": {
                "type": "image",
                "settings": {
                    "image_width": "custom",
                    "image_max_width": 45,
                    "image_max_width_mobile": 50,
                },
            },
            "hd": {
                "type": "heading",
                "settings": {
                    "heading": "Dial in fabric, filters, and long-term care",
                    "heading_size": "title-lg tracking-heading",
                    "heading_tag": "h2",
                    "highlighted_text": "none",
                    "highlighted_scribble": "circle",
                },
            },
            "tx": {
                "type": "text",
                "settings": {
                    "text": "<p>High-ticket buyers need a plan after checkout. Start with a <strong>free fabric swatch</strong> if you are undecided on Pearl vs Stone, then line up <strong>replacement filters</strong> (HEPA ~12 months, carbon ~6 months for many homes—your environment may vary).</p><p>Subscription programs may include savings and warranty perks—confirm the live offer in your cart or subscription app.</p>",
                    "text_font": "body",
                    "text_size": "subtext-md",
                    "text_max_size": 32,
                    "text_line_height": 1.6,
                    "text_letter_spacing": 0,
                    "text_capitalize": False,
                    "secondary_color": False,
                    "highlighted_text": "none",
                    "highlighted_scribble": "circle",
                },
            },
            "btn_swatch": {
                "type": "button",
                "settings": {
                    "button_label": "Order a free fabric swatch",
                    "button_link": "/products/free-air-purifier-headboard-fabric-color-swatch-box",
                    "button_style": "primary",
                    "button_size": "md",
                    "button_external": False,
                    "button_icon": True,
                },
            },
            "btn_filters": {
                "type": "button",
                "settings": {
                    "button_label": "Shop replacement filters",
                    "button_link": "/products/replacement-filter-set",
                    "button_style": "secondary",
                    "button_size": "md",
                    "button_external": False,
                    "button_icon": True,
                },
            },
        },
        "block_order": ["im", "hd", "tx", "btn_swatch", "btn_filters"],
        "settings": {
            "image": "shopify://shop_images/custom_resized_822219ee-2b7f-4da5-8ace-fbeff72155af.png",
            "image_height": "adapt",
            "image_width": "medium",
            "layout": "text_first",
            "text_alignment": "left",
            "content_position": "align-self-center",
            "image_mobile": "",
            "image_height_mobile": "auto",
            "text_alignment_mobile": "left",
            "color_text": "#171717",
            "color_background": "",
            "gradient_background": "",
            "color_background_2": "#fafafa",
            "gradient_background_2": "",
            "color_highlight": "",
            "gradient_highlight": "",
            "color_button_text": "",
            "color_button_background": "",
            "color_button_gradient": "",
            "padding_top": 56,
            "padding_bottom": 56,
            "divider": False,
            "full_width": False,
            "rounded": False,
            "enable_parallax": False,
            "parallax_direction": "vertical",
        },
    }

    pdp_review_widget = json.loads(json.dumps(sections["1724702857f612c3e2"]))
    pdp_review_widget["settings"] = dict(
        pdp_review_widget["settings"],
        **{"padding_top": 48, "padding_bottom": 48},
    )

    pdp_contact = json.loads(json.dumps(sections["contact_form_WUaLBd"]))
    pdp_contact["settings"] = dict(
        pdp_contact["settings"],
        **{
            "heading": "Need a bespoke headboard?",
            "description": "<p>Discuss custom fronts, contrasting channels, alternate wraps, shelving, or other bespoke requests—we will outline feasibility and timelines after reviewing your note.</p>",
            "padding_top": 56,
            "padding_bottom": 16,
        },
    )

    pdp_faq = json.loads(json.dumps(sections["faq"]))
    pdp_faq["blocks"]["contact"]["settings"]["text"] = (
        "<p>Don't hesitate to contact us—our team replies on weekdays.</p>"
    )

    merged = {
        "countdown_timer_ynng3X": sections["countdown_timer_ynng3X"],
        "main-product": main,
        "pdp_trust_signals": pdp_trust_signals,
        "pdp_value_split": pdp_value_split,
        "pdp_how_it_works": pdp_how_it_works,
        "pdp_science": pdp_science,
        "pdp_press": pdp_press,
        "pdp_explainer_video": pdp_video,
        "pdp_shark_strip": pdp_shark,
        "pdp_judge_carousel": pdp_judge_carousel,
        "pdp_ownership": pdp_ownership,
        "pdp_review_widget": pdp_review_widget,
        "pdp_custom_contact": pdp_contact,
        "pdp_faq": pdp_faq,
    }

    data["sections"] = merged
    data["order"] = [
        "countdown_timer_ynng3X",
        "main-product",
        "pdp_trust_signals",
        "pdp_value_split",
        "pdp_how_it_works",
        "pdp_science",
        "pdp_press",
        "pdp_explainer_video",
        "pdp_shark_strip",
        "pdp_judge_carousel",
        "pdp_ownership",
        "pdp_review_widget",
        "pdp_custom_contact",
        "pdp_faq",
    ]

    save_theme_json(TEMPLATE, data)
    print("Wrote", TEMPLATE)


if __name__ == "__main__":
    main()
