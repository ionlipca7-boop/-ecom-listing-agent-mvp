# ECOM OS Market Radar + Value Signal Formula V1

Date: 2026-05-30
Operator: Ion / ION
Project: ECOM OS / ECOM LISTING AGENT MVP
Archive type: strategic formula + agent design bridge
Status: FORMULA_ACCEPTED_FOR_EXPERIMENT_AND_FUTURE_AGENT_INTEGRATION

---

## 1. Why this archive exists

This archive consolidates two connected learning routes:

1. The UD24 eBay value-signal experiment.
2. The product discovery / market radar discussion about finding products from search demand, marketplace demand, and listing/algorithm fit.

The goal is to define one reusable formula for future ECOM OS agents before implementation on server/runtime.

---

## 2. Core conclusion

Do not start from a random supplier product.

Correct route:

```text
SEARCH BEHAVIOR
-> DEMAND MAP
-> MARKETPLACE SALES PROOF
-> PRODUCT CANDIDATES
-> VALUE SIGNAL FIT
-> PROFIT/RISK CHECK
-> LISTING ADVANTAGE
-> TEST / WATCH / REJECT
```

Short formula:

```text
SEARCH -> DEMAND -> PRODUCT -> PROFIT -> LISTING -> ALGORITHM -> TEST
```

---

## 3. The buyer-search lesson

Buyers do not search in only one way. ECOM OS must support both patterns.

### A. Problem search

Buyer does not know the exact product yet.

Examples:

```text
Kabel verstecken
Kabelsalat vermeiden
Handy fällt im Auto
Ladegerät prüfen
```

### B. Product search

Buyer already knows the desired item.

Examples:

```text
USB C Kabel 2m
USB C Winkeladapter 100W
Handyhalter Auto MagSafe
Küchenschere Edelstahl
```

### Rule

The future agent must not focus only on problems and must not focus only on product names. It must build a structured search-market map from both.

---

## 4. Germany Demand Map V1

The first market intelligence layer should be:

```text
GERMANY_DEMAND_INTELLIGENCE_AGENT
```

Mission:

```text
Collect and rank what people in Germany search, compare it over time, and detect which searches can become product opportunities.
```

Required views:

```text
1. Top growing searches
2. Top stable searches
3. Top falling searches
4. Top buyer-intent searches
5. Top product-search clusters
6. Top problem-search clusters
7. Top marketplace-sold proof clusters
```

Time windows:

```text
Daily snapshot
7-day trend
30-day trend
90-day trend
```

Why:

```text
One-day data is weak. Trend movement over 5-7 days is stronger. 30/90-day trend protects against short hype.
```

---

## 5. Data sources / tools for future agents

### Search demand sources

```text
Google Trends: relative demand and trend movement by region/time.
Google Keyword Planner / SEO tools: keyword ideas and search-volume estimates.
Google autocomplete/suggest: real buyer wording.
YouTube/TikTok/Reddit/forums: problem language and emerging interest.
```

### Marketplace demand sources

```text
eBay Terapeak / Product Research: sold items, average price, sell-through, competition.
eBay listing editor: item-specific fields with visible search-count signals.
eBay active listings: competitor title/photo/price/item specifics.
eBay sold listings: real sale proof.
Amazon Germany: search/product opportunity, reviews, questions, ranking signals.
```

### Supplier/product sources

```text
1688
Alibaba
AliExpress
Made-in-China
Global Sources
Supplier manuals/spec sheets/package photos
```

---

## 6. Critical lesson from UD24

UD24 proved that title alone is not enough.

The product moved from a cheap generic USB tester cluster toward a higher-value cluster only when multiple signals worked together:

```text
Title
+ item specifics
+ real photo gallery
+ description
+ confirmed package truth
+ Bluetooth / Power Meter / PD-QC value signals
+ ad/delivery logic
```

Weak generic direction:

```text
USB Tester für Ladegerät Kabel
USB Messgerät für Ladegerät Kabel Spannung Strom
Generic Voltmeter / Amperemeter title
```

Stronger UD24 direction:

```text
ATORCH UD24 USB DC Messgerät Bluetooth Power Meter Spannung Strom PD QC
```

Reusable technical title formula:

```text
Brand + Model + Product Class + Premium Feature + Value Function + Buyer Intent + Protocols
```

---

## 7. Product discovery formula

A candidate product is attractive when this equation is positive:

```text
Buyer search demand
+ Product search demand
+ Marketplace item-specific demand
+ Marketplace sold proof
+ Confirmed value features
+ Strong visual story
+ Margin after fees/shipping/ads/returns
+ Listing/algorithm fit
- Cheap cluster risk
- Legal/claim/return risk
= Product opportunity score
```

---

## 8. Scoring model V1

Total: 100 points.

```text
Search Demand: 15
Buyer Intent: 10
Trend Momentum: 10
Marketplace Sales Proof: 15
Profit Reality: 15
Competition Gap: 10
Value Signal Fit: 10
Listing/Photo Advantage: 5
Algorithm Fit: 5
Risk Safety: 5
```

Decision:

```text
85-100 = STRONG TEST
70-84  = TEST / WATCH
55-69  = WATCH
<55    = REJECT
```

Important anti-overfilter rule:

```text
Do not search for one perfect product.
Build a portfolio/watchlist of opportunities.
```

Output buckets:

```text
BUY / TEST NOW
WATCH 7-30 DAYS
REJECT
```

---

## 9. Agent map V1

### 1. GERMANY_DEMAND_INTELLIGENCE_AGENT

Finds what people search in Germany.

Outputs:

```text
Demand map
Keyword clusters
Problem clusters
Product clusters
Trend movement
Buyer intent estimate
```

### 2. PRODUCT_DISCOVERY_SEARCH_SIGNAL_AGENT

Uses demand map to find candidate products.

Outputs:

```text
20-100 product candidates
Search-language map
Marketplace field signals
Supplier candidates
Opportunity score
```

### 3. PROFIT_RISK_AGENT

Calculates real business possibility.

Checks:

```text
Purchase price
China shipping
Germany shipping
eBay fees
Ad rate 6-8%
Packaging
Return/defect reserve
Stock/cashflow speed
```

### 4. MARKET_VALUE_SIGNAL_AGENT

Turns a product into a higher-value listing system.

Outputs:

```text
Title formula
Item specifics plan
Photo/gallery plan
Description plan
Ad/delivery recommendation
Experiment log
```

### 5. EBAY_ALGORITHM_FIT_AGENT

Checks whether eBay can understand and show the listing.

Inputs:

```text
Category
Title keywords
Item specifics
Seller terms
Price
Photo quality
Comparable competitors
Promoted Listing context
```

### 6. DECISION_BOARD_AGENT

Final decision:

```text
STRONG TEST
TEST SMALL LOT
WATCH
REJECT
NEEDS MORE DATA
```

---

## 10. How this connects to ECOM OS

Before product purchase:

```text
Germany Demand Intelligence
-> Product Discovery Search Signal
-> Supplier/Product Passport
-> Profit/Risk
-> Decision Board
```

Before listing:

```text
Product Passport
-> Market Value Signal
-> Listing Agent
-> eBay Algorithm Fit
-> Approval Gate
-> Publish/Revise
-> Read-only verify
```

After listing:

```text
Day 0 log
Day 3-5 impressions/clicks/watchers/ad signals
Day 7-14 sales/conversion/messages/returns
Learning update to archive
```

---

## 11. Required experiment log fields

Every product opportunity must log:

```json
{
  "experiment_id": "MARKET_RADAR_PRODUCT_TEST_YYYYMMDD",
  "marketplace": "ebay.de",
  "category": null,
  "problem_queries": [],
  "product_queries": [],
  "trend_window": "7/30/90 days",
  "marketplace_sold_evidence": null,
  "supplier_cost_eur": null,
  "target_sale_price_eur": null,
  "estimated_net_margin_eur": null,
  "ad_rate_assumption_percent": 7,
  "competition_notes": null,
  "value_signals": [],
  "fillable_item_specifics": [],
  "cheap_cluster_risk": null,
  "photo_advantage": null,
  "decision": "WATCH/TEST/REJECT",
  "assumptions": [],
  "needs_source": []
}
```

---

## 12. What to keep separate

Keep these modules separate:

```text
Market Radar = before purchase, finds opportunity.
Product Passport = product truth layer.
Market Value Signal = creates premium/algorithm-friendly listing.
Listing Agent = executes listing creation/update.
Post-Listing Analytics = learns from impressions, clicks, sales.
```

Do not mix all logic into one agent. Use a controlled pipeline.

---

## 13. What to do next

Next safe project step after this archive:

```text
1. Verify GitHub archive exists.
2. When server eyes are available, sync/record this as a project lesson pointer.
3. Build Germany Demand Map V1 as a manual/ChatGPT experiment first.
4. Test 3 categories:
   - USB-C / Mobile Accessories
   - Home Organization
   - Auto Accessories
5. Generate 20 candidates.
6. Score and reduce to TOP 5.
7. Do not buy until evidence/log is complete.
```

---

## 14. Current status

```text
PASS: formula consolidated.
PASS: UD24 listing lesson connected to product discovery logic.
PASS: future agent map defined.
NEXT: verify archive, then connect GitHub + server + ECOM OS pointers when available.
```
