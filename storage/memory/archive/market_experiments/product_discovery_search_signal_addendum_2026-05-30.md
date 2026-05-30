# Product Discovery Search-Signal Addendum — ECOM OS Agent Upgrade

Date: 2026-05-30
Operator: Ion / ION
Project: ECOM OS / ECOM LISTING AGENT MVP
Related lesson: UD24 eBay Listing Value-Signal Experiment
Purpose: upgrade future product discovery / product research agents with search-signal logic

---

## 1. Core idea

The UD24 experiment showed that marketplace-visible search signals are not only useful after a product is listed. They can also be used **before buying or sourcing a product**.

If eBay shows item-specific fields with search-count indicators such as:

```text
Produktart ~25,366 Suchen
Anzeige ~6,438 Suchen
Anzeigetyp ~6,329 Suchen
Test-/Messfunktionen ~596 Suchen
Eigenschaften ~236 Suchen
Widerstand Messauflösung ~148 Suchen
```

then these fields reveal what buyers actively use to search/filter the category. A product research agent should use this data to understand demand language and category structure before selecting new products.

This means product discovery should not only ask:

```text
Can we buy this cheaply?
Can we resell it with margin?
Are competitors selling it?
```

It must also ask:

```text
Do buyers search for the attributes this product has?
Can the product fill high-search item-specific fields truthfully?
Does the product have value signals that move it out of low-price clusters?
Can we build a strong title/description/gallery from confirmed features?
```

---

## 2. Why this matters

The UD24 listing proved that a product can be under-valued if it is described in generic language. Simple words like `USB Tester`, `Ladegerät`, `Kabel`, `Voltmeter`, `Amperemeter` may be understandable but can place the product in a cheap accessory cluster.

The stronger structure was:

```text
Brand + Model + USB DC Messgerät + Bluetooth + Power Meter + Spannung Strom + PD QC
```

This means product discovery must look for products where a **value-language bridge** exists:

```text
simple buyer search terms + technical/premium value terms + category-specific filters
```

For future sourcing, a product is more attractive if it has:

```text
- high buyer-intent search terms
- high-value differentiators
- clear category-specific item specifics
- enough confirmed data to fill eBay/Amazon fields
- good visual story for photos
- stable margin after fees, shipping, ads, and returns
```

---

## 3. New product discovery agent upgrade

Proposed agent name:

```text
PRODUCT_DISCOVERY_SEARCH_SIGNAL_AGENT_V1
```

This agent should work together with the existing product input / product passport / marketplace value-signal agents.

Repository already has product-related pipeline elements such as:

```text
run_build_next_product_input_v1.py
run_registry_get_product_v1.py
run_build_product_registry_lookup_call_v1.py
storage/tools/ecom_os_v3/agents/product_passport_agent_v1.py
storage/rules/product_input_validation_gate_v1.json
```

This addendum does not replace those parts. It adds a demand/search-signal layer before and during product selection.

---

## 4. Agent mission

The agent's mission:

```text
Find products that are not only cheap to source, but also match real buyer search behavior and marketplace item-specific demand signals.
```

It should identify products where ECOM OS can build:

```text
1. Strong title formula
2. High-signal item specifics
3. Real feature-based description
4. Premium photo gallery
5. Clear buyer use case
6. Stable price/margin strategy
7. Promoted listing plan
```

---

## 5. Data sources the agent should use

### Marketplace-internal signals

```text
eBay item-specific search counts shown in listing editor
Suggested item specifics
Category filters
Sold listings
Similar active listings
Terapeak/product research where available
Recommended price panel
Promoted listing competition/ad-rate hints
Photo/order/layout of top competitors
Competitor titles and their word order
Competitor item specifics
Competitor delivery policy
Competitor price range and sold price
```

### Search-engine demand signals

```text
Google Trends relative interest
Google autocomplete / suggest queries
Google Shopping/product snippets if available
Search terms from normal buyer language
YouTube/TikTok/Reddit style problem-language if relevant
```

Google Trends is useful for comparing relative interest over time/region, not for exact absolute search volume. The agent must not treat Google Trends score as exact demand quantity.

### Supplier/source signals

```text
Supplier price
Supplier photos
Manual/spec sheet availability
Confirmed package contents
Shipping time/cost
Defect/return risk
Whether supplier claims can be verified
Whether product has unique features competitors show
```

---

## 6. Search-signal scoring model

The agent should create a product opportunity score from multiple blocks.

### A. Demand/search-language score

Questions:

```text
Do buyers search for this product class?
Are there high-search item-specific fields?
Do Google/eBay queries show real buyer intent?
Are buyer terms simple enough to write a clear title?
```

Examples:

```text
USB Messgerät
Power Meter
Bluetooth Tester
PD QC Tester
Spannung Strom messen
Ladegerät prüfen
Powerbank testen
```

### B. Value-signal score

Questions:

```text
Does the product have premium differentiators?
Can it avoid cheap commodity clustering?
Does it have confirmed features that increase perceived value?
```

UD24 example:

```text
Bluetooth
Power Meter
Farbdisplay
5–32 V / 0–5.1 A
PD/QC support
Metallbox
USB/DC measurement
```

### C. Specifics-fill score

Questions:

```text
Can we truthfully fill the high-search item-specific fields?
Are the exact values confirmed by manual/rear label?
Which fields must remain blank because values are unconfirmed?
```

High score = many important eBay fields can be filled safely.

### D. Visual-story score

Questions:

```text
Can we create 8–10 strong gallery images?
Can photos show real value quickly?
Can we show use cases without false accessories?
Is there a truth layer from real photos?
```

### E. Margin/market score

Questions:

```text
Supplier cost vs realistic sale price?
Fees/ad/shipping included?
Can price survive 6–8% ad rate?
Can returns or misunderstandings destroy margin?
```

### F. Risk score

Risks:

```text
Unverified specs
Regulated product
Fake brand/counterfeit risk
Weak manual/data
Battery/safety/legal risk
Misleading supplier photos
No clear buyer demand
Too many cheap competitors
```

---

## 7. Product discovery workflow

The agent should follow this controlled route:

```text
1. Input seed product or category.
2. Collect competitor active listings and sold listings.
3. Extract repeated title words and title word order.
4. Open/create draft listing if needed to see eBay item-specific search-count fields.
5. Record all fields with visible search signals.
6. Compare field demand with supplier product features.
7. Search Google/Google Trends/autocomplete for buyer-language demand.
8. Build buyer-language map:
   - simple buyer words
   - professional/technical words
   - premium/value words
   - protocol/range/spec words
9. Build candidate title formulas.
10. Estimate whether product falls into cheap cluster or higher-value cluster.
11. Score product opportunity.
12. Recommend: reject / watchlist / test listing / buy sample / list.
13. Log all evidence and assumptions.
```

---

## 8. Buyer-language map

The agent must translate between three languages:

### 1. Simple buyer language

What a normal buyer might search:

```text
Ladegerät prüfen
Kabel testen
Powerbank testen
Spannung messen
Strom messen
Volt Ampere anzeigen
USB Tester Handy
```

### 2. Marketplace/category language

What eBay fields/categories understand:

```text
Produktart
Anzeige
Anzeigetyp
Test-/Messfunktionen
Eigenschaften
Anschlüsse
Messauflösung
Modell
Herstellernummer
```

### 3. Value-class language

What moves product away from cheap cluster:

```text
Power Meter
Digital Tester
USB/DC Messgerät
Bluetooth
Farbdisplay
PD/QC
5–32 V
0–5.1 A
Metallbox
```

The best title/listing combines all three safely.

---

## 9. Product discovery output format

For every product candidate, the agent should output:

```json
{
  "product_candidate": "ATORCH UD24-like USB/DC tester",
  "marketplace": "ebay.de",
  "simple_buyer_queries": [
    "Ladegerät prüfen",
    "USB Tester Handy",
    "Spannung Strom messen",
    "Powerbank testen"
  ],
  "marketplace_field_signals": {
    "Produktart": "high",
    "Anzeige": "high",
    "Anzeigetyp": "high",
    "Test-/Messfunktionen": "medium",
    "Eigenschaften": "medium",
    "Widerstand Messauflösung": "potential but needs source"
  },
  "value_signals": [
    "Bluetooth",
    "Power Meter",
    "Farbdisplay",
    "PD/QC",
    "5–32 V / 0–5.1 A",
    "Metallbox"
  ],
  "cheap_cluster_risk": "high if title starts generic USB Tester",
  "recommended_title_formula": "Brand + Model + USB DC Messgerät + Bluetooth + Power Meter + Spannung Strom + PD QC",
  "specifics_fill_score": "good if manual/rear label confirms fields",
  "visual_story_score": "good if real photos + package truth available",
  "decision": "test listing / source carefully / monitor competitors"
}
```

---

## 10. How it connects to MARKET_VALUE_SIGNAL_AGENT_V1

Two agents should work together:

### PRODUCT_DISCOVERY_SEARCH_SIGNAL_AGENT_V1

Before product purchase/listing:

```text
Find products with demand and fillable value signals.
Use eBay/Google/competitor signals to decide whether the product is worth testing.
```

### MARKET_VALUE_SIGNAL_AGENT_V1

After product exists/listing draft exists:

```text
Optimize actual listing using title, item specifics, description, photos, price, delivery, and ads.
```

The discovery agent finds opportunities. The value agent turns those opportunities into optimized listings.

---

## 11. Rules for the future product search agent

```text
Do not search only for cheap supplier products.
Do not trust supplier titles as final marketplace titles.
Do not ignore item-specific search-count fields.
Do not ignore normal buyer language.
Do not ignore professional/value language.
Do not buy products where high-signal fields cannot be filled safely.
Do not select products only because competitors list them.
Do not assume high views equal high profit.
Do not ignore ad/shipping/return cost.
Do not use false features to match search demand.
```

---

## 12. Practical product discovery formula

A product is attractive when this equation is positive:

```text
Buyer search demand
+ Marketplace item-specific demand
+ Confirmed value features
+ Strong visual story
+ Margin after fees/shipping/ads
- Cheap cluster risk
- Claim/legal/return risk
= Product opportunity score
```

For UD24, the opportunity improved when the listing revealed:

```text
Bluetooth + Power Meter + PD/QC + Farbdisplay + Metallbox + complete item specifics
```

The same logic should be used to discover future products before buying inventory.

---

## 13. Internet/source note

External search/SEO context confirms the logic that keyword research is about finding actual search terms and intent, while Google Trends is mainly a relative-interest comparison tool, not exact search volume. eBay guidance also emphasizes listing quality, item specifics, accurate title/description/photos, and seller terms as part of marketplace visibility. Promoted listings/ad rates depend on item attributes, seasonality, past performance, and competition, so ads must be considered after the listing opportunity and quality are assessed.

Sources to re-check periodically:

```text
https://www.ebay.com/help/selling/listings/listing-tips/optimising-listings-best-match?id=4166
https://www.ebay.com/help/selling/ebay-advertising/promoted-listings/general-campaign-strategy?id=4164
https://trends.google.com/trends/
```

---

## 14. Current implementation status

Status:

```text
IDEA_ACCEPTED_AS_AGENT_UPGRADE
ARCHIVED_AS_PRODUCT_DISCOVERY_SEARCH_SIGNAL_ADDENDUM
```

Next project integration after core ECOM OS is stable:

```text
Add PRODUCT_DISCOVERY_SEARCH_SIGNAL_AGENT_V1 to agent map.
Connect it to product passport / product input pipeline.
Add experiment logs for demand signals, title formulas, item-specific search counts, and supplier truth checks.
```

End of addendum.
