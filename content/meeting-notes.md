# AirTulip — meeting notes & direction

Running log of client meetings, Fireflies recaps, and follow-up work. **Update status as items ship.**

---

## 2026-07-27 — Filter subscription shipping & PDP flow (Fireflies)

**Source:** Client meeting recap (Fireflies)  
**Priority:** Fix today — customer waiting to purchase; Arjen to follow up when live.

### Problem summary

1. **$75 shipping on filter subscription renewals** that should receive **free shipping** (matches one-time filter bundle shipping copy: $75 / $45 Twin — likely wrong profile applied on renewal).
2. **Subscription add-to-cart / price display** — one-time vs subscribe toggle, cart line price, checkout totals, and subscription terms must stay accurate.

### Root-cause investigation (2026-07-27)

| Area | Finding | Owner |
|------|---------|--------|
| **Theme / cart add** | Appstle `selling_plan` radios render **outside** the theme `product-form`. Form POST omitted `selling_plan` → cart added at **one-time price** ($674 vs $572.90 subscribe on Queen bundle). **Fix in repo:** `assets/appstle-selling-plan-sync.js` + hidden input in `snippets/buy-buttons.liquid`. | Theme — **ready for staging QA** |
| **PDP price display** | Live site: Appstle **does** update `#Price-*` block when toggling subscribe (discounted price + strikethrough). Re-test after theme deploy. | QA |
| **Renewal shipping ($75)** | Known Appstle + Shopify pattern: renewals use **Shipping & Delivery** profiles; subscription plans need a dedicated **Appstle shipping profile** with **$0** rates, or contracts need **delivery price override**. Not fixable in theme Liquid alone. See [Appstle shipping profiles](https://intercom.help/appstle/en/articles/5212799-how-to-create-shipping-profiles-for-subscription-orders), [community thread on renewal shipping](https://community.shopify.com/t/appstle-subscription-orders-being-shipping-on-subscriptions-with-free-shipping/115391). | **Appstle admin + Shopify Shipping** |
| **ShipZip app** | Installed — confirm it is not adding $75 on subscription renewal orders. | Shopify admin |
| **CLI store access** | Authenticated with expanded read scopes (see `.cursor/rules/airtulip-apps.mdc`). | Done 2026-07-27 |
| **Appstle Admin API** | Gated behind Appstle plan upgrade + store-owner staff permission for API Access. Use **screenshots + guided UI** until upgraded. | Blocked |
| **Cart drawer upsell** | Dual mode works: **Subscribe** adds discounted subscription; **Add [1] to Cart** is one-time only (user clicked wrong button in QA). Kept UX tweak: Subscribe first/primary, one-time labeled **One-time**. | No functional bug — UX only |

### Active subscription stack (storefront)

- **Filter PDP:** `templates/product.filter-replacement.json` — Appstle product-page widget block + theme price block.
- **App embed:** `appstle-subscription-helper` in `config/settings_data.json`.
- **Product:** [replacement-filter-set](https://airtulip.co/products/replacement-filter-set) — selling plan example ID `8960868642` (Annual subscription, Queen variant tested).
- **Other subscription apps in admin** (Utterbond, PayWhirl, Shopify Subscriptions): not on filter PDP; avoid conflicting widgets.

### Task checklist

- [x] Document meeting recap in this file
- [x] Identify cart add bug (missing `selling_plan` in form POST)
- [x] Implement theme fix (`appstle-selling-plan-sync.js`)
- [x] **Developer:** CLI store auth — `read_products,read_orders,read_shipping,read_customers,read_fulfillments,read_discounts,read_purchase_options,read_locations,read_price_rules,read_draft_orders` (2026-07-27)
- [ ] **Deploy theme fix** to staging → QA on filter PDP (developer runs push/publish — agent does not)
- [ ] **Appstle admin:** More → **Shipping Profile** — attach filter subscription plan(s); **Edit on Shopify** → US zone **$0** standard shipping for subscription profile only ([guide](https://intercom.help/appstle/en/articles/5212799-how-to-create-shipping-profiles-for-subscription-orders))
- [ ] **Review active subscriptions** in Appstle merchant portal — upcoming orders showing $75 shipping → bulk fix delivery price to **$0** ([API: update delivery price](https://appstleinc-aeca3e0a.mintlify.app/api-reference/subscription-management/update-delivery-price-for-a-subscription-contract)) or per-contract edit in portal
- [ ] **Test new purchase:** Subscribe → add to cart → cart shows subscription plan name + **$572.90** (Queen) → checkout **$0 shipping** → complete test order if possible
- [ ] **Test renewal:** Place or simulate next billing cycle / review next scheduled order shipping line
- [ ] **Report live to Arjen** so he can contact waiting customer

### QA script (filter subscription)

1. Open `/products/replacement-filter-set` — select **Subscribe and save**.
2. Confirm header price shows discounted amount (not one-time only).
3. Add to cart — line item must show **Annual subscription** (or configured plan name) and discounted price.
4. Checkout — shipping **$0** for subscription; terms/frequency correct.
5. Toggle **One time purchase** — price returns to full; cart add has **no** selling plan.

### References

- Brand promise: **15% off + free shipping + unlimited warranty** on filter subscription — `.cursor/rules/airtulip-brand-content.mdc`
- Appstle JS hooks: [developers.subscription.appstle.com/javascript-hooks](https://developers.subscription.appstle.com/javascript-hooks)
- Apps inventory: `.cursor/rules/airtulip-apps.mdc`

---

## Template for future entries

```markdown
## YYYY-MM-DD — Title (Fireflies / call)

**Attendees:**  
**Decisions:**  
**Action items:**  
**Status:**  
```
