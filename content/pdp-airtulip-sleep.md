# PDP copy — AirTulip Sleep (`sleep-air-purifier-headboard`)

Source for `templates/product.json` below-the-fold sections. Align with `.cursor/rules/airtulip-brand-content.mdc`. **Verify prices, legal lines, and claims on the live PDP before publishing.**

---

## Page flow (CRO)

1. **Main product** — gallery, price, financing (Affirm / Shop Pay / TrueMed), buy box, collapsible specs.
2. **Trust strip** — trial, warranty, manufacturing, lead time (reduces anxiety for high-ticket).
3. **Value split** — “breathing zone vs room purifier” (why this product exists).
4. **How it works** — three pillars: laminar zone, HEPA H14, quiet operation.
5. **Science** — one proof block + graph (quantified claim matches approved marketing).
6. **Press + research** — single logo row: media + TU/e (credibility without homepage duplication).
7. **Product video** — one primary explainer (autoplay where theme allows).
8. **Shark Tank** — single compact line + link (social proof, not a full banner).
9. **Judge.me carousel** — short-form social proof.
10. **Ownership** — swatch, filters, subscription framing (post-purchase clarity).
11. **Judge.me review widget** — deep reviews for serious buyers.
12. **Custom headboard** — contact form.
13. **FAQ** — objections and policies.

---

## Section headlines & body (short)

### Trust strip

- **Section heading:** *Why customers invest in AirTulip Sleep*
- **Col 1:** 30-night sleep trial — Return within 30 days for a full product refund (excluding shipping both ways).
- **Col 2:** 1-year warranty — Manufacturing defects covered; see FAQ for filter subscription benefits if applicable on your store.
- **Col 3:** Hand-assembled in the U.S. — Built in Brooklyn and Detroit; made to order for your bed size and fabric.
- **Col 4:** ~8 week lead time — We communicate build progress and your estimated ship date.

### Value split (media + copy)

- **Heading:** The only purifier designed around your sleep
- **Body:** AirTulip Sleep draws air through industrial-grade filtration and delivers it through the headboard fabric using **laminar (low-turbulence) airflow** aimed at your breathing zone—so you’re not gambling on ceiling-to-floor mixing like a traditional room purifier.
- **Button:** Explore the engineering → `/pages/about`

### How it differs (multicolumn)

- **Section heading:** Engineered where it matters most
- **1 — Laminar breathing zone:** A stable, directed flow supports a concentrated clean-air zone near your face—not just “more CFM somewhere in the room.”
- **2 — Industrial HEPA H14 paths:** Dual HEPA H14 filters in metal cassettes on larger sizes capture ultra-fine particulates; activated carbon tackles odors and VOCs (counts vary by Twin vs Queen/King—see specs in the buy box).
- **3 — Built for bedside silence:** Whisper and night modes are tuned for sleep—published levels **26–30 dB(A)** depending on mode.

### Science band

- **Heading:** Measurement-backed performance
- **Body:** Independent university chamber work and visualization partners inform our development; marketing claims on particle reduction belong to your **approved compliance set**—mirror the PDP/About wording your legal team signs off on.

### Ownership band

- **Heading:** Dial in fabric, filters, and long-term care
- **Body:** Order a **free fabric swatch** before you commit. Plan on **replacement filters** on a rhythm that matches your air and usage—the buy box tabs summarize intervals; bundles and subscriptions live in your catalog.

### Shark Tank ribbon

- **Heading:** Seen on Shark Tank
- **Body:** Watch our episode on [ABC](…) or [Hulu](…) *(URLs as on your current marketing)*.

---

## Internal links (handles — confirm on store)

| Use            | Path |
|----------------|------|
| Free swatch    | `/products/free-air-purifier-headboard-fabric-color-swatch-box` |
| Replacement filters | `/products/replacement-filter-set` |
| About / science | `/pages/about` |

---

## Rebuild `product.json`

```bash
python tools/rebuild_product_pdp.py
```

The script regenerates the PDP below-the-fold sections and, when needed, restores app blocks (Judge.me) and-disabled carousels from the last **git** version of `templates/product.json`.

---

## Assets

Prefer existing Shopify files: product hero, `graph2.png`, `Air Tulip Video.mp4`, press logos. Add new imagery to **Content → Files** and swap URLs in `product.json` when ready.
