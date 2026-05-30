# UD24 eBay Listing Value-Signal Experiment — FULL ROUTE / TEACHER LESSON

Date: 2026-05-30
Operator: Ion / ION
Project: ECOM OS / ECOM LISTING AGENT MVP
Archive type: full route lesson for future marketplace/value agents
Product: ATORCH UD24 USB/DC Digital Tester
Marketplace: eBay.de

This file is not a short summary. It is a full reusable learning route for future ECOM OS agents. The goal is to prevent the system from forgetting the small but important details discovered during manual testing.

The experiment showed that eBay listing value is not controlled by title alone. The price/value signal improved only after title, category, item specifics, real photo gallery, description, package truth layer, and promoted listing logic worked together as one marketplace signal system.

---

## 0. Why this archive exists

The operator noticed that the same product can be interpreted by eBay in different value clusters depending on wording and listing completeness.

Low-value cluster example:

```text
USB Tester für Ladegerät Kabel...
USB Messgerät für Ladegerät Kabel...
Generic Voltmeter / Amperemeter title...
```

These titles made eBay compare the item with cheap generic USB testers and led to low recommended price indications around 7–10 EUR.

Higher-value cluster result:

```text
ATORCH UD24 USB DC Messgerät Bluetooth Power Meter Spannung Strom PD QC
```

After this title was combined with enriched item specifics, stronger description, correct image gallery, real package contents, and confirmed Bluetooth/Power Meter signals, eBay showed a recommended price around **20.24 EUR**.

The listing price was kept at **22.99 EUR**, quantity **2**, promoted listing ad rate **7%**.

---

## 1. Product truth layer — what the real product actually is

Future agents must always start from the real product truth layer, not from supplier fantasy images.

### Confirmed from real photos and manual

```text
Brand: ATORCH
Model: UD24
Product class: USB/DC Digital Tester / USB/DC Messgerät / Power Meter
Color: Schwarz
Display: color display / Farbdisplay
Body: black rectangular central device
Side covers: two rounded detachable black side covers
USB-A connector/input: present
USB-C / Type-C connector: present
Micro-USB input marking: present
DC5.5 markings/input-output: present
Buttons: M/+ and OK/- visible
Power indicator: visible
Bluetooth symbol: visible on device/manual/supplier references
Rear label: confirms model and electrical range
Storage: silver metal box included
Manual: printed user manual included
```

### Confirmed included package contents

```text
1x ATORCH UD24 USB/DC Tester
1x Metallbox
1x Bedienungsanleitung
```

### Explicitly not included

The operator corrected the earlier supplier/accessory-image direction. The real package does **not** include the accessory kit shown in some supplier images.

Do not show or claim:

```text
Kabelset
Adapterset
Trigger-Boards
DC splitters
Krokodilkabel
Temperature probe
Extra accessory kit
Zubehör-Set
```

This matters because false accessories may increase returns, buyer disputes, negative feedback, and marketplace trust penalties.

---

## 2. First false direction — why simple buyer-friendly titles failed

At first, we tried to make the title understandable for normal buyers who search things like:

```text
USB Tester für Ladegerät Kabel
USB Messgerät für Ladegerät Kabel Spannung Strom
USB Ladegerät Tester Volt Ampere
USB Spannungsmesser Strommesser für Handy Kabel
```

This sounded understandable for a non-technical buyer, but it had a hidden marketplace problem: it made the product look like a cheap commodity accessory.

### Lesson

For technical products, being too simple can reduce perceived value.

A title that only says `USB Tester`, `Ladegerät`, `Kabel`, `Voltmeter`, `Amperemeter` may get broad search reach but can place the listing in a low-price comparison group.

The buyer may understand it, but the marketplace algorithm may compare it to 2–10 EUR generic USB testers.

### Rule for future agents

Do not use only low-value generic terms. Combine simple search terms with value-class terms.

Bad weak direction:

```text
USB Tester für Ladegerät Kabel Strom Spannung Volt Ampere Messgerät
USB Messgerät für Ladegerät Kabel Spannung Strom Voltmeter Amperemeter
USB Spannungsmesser Strommesser Tester für Ladegerät Kabel Handy
```

Better direction:

```text
Brand + Model + USB/DC Messgerät + Bluetooth + Power Meter + Spannung/Strom + PD/QC
```

---

## 3. The successful title formula

Final working title:

```text
ATORCH UD24 USB DC Messgerät Bluetooth Power Meter Spannung Strom PD QC
```

This title is valuable because every word has a role.

### Word-by-word logic

1. `ATORCH`
   - Brand signal.
   - Stops eBay from seeing only a generic no-name tester.
   - Useful when the model exists in comparable listings.

2. `UD24`
   - Model signal.
   - Identifies the exact device class.
   - Helps eBay match with similar UD24 listings and not with simple USB dongle testers.

3. `USB DC`
   - Connection/use class.
   - Shows this is not only a simple USB charger meter; it also supports DC measurement context.

4. `Messgerät`
   - German high-value product class.
   - Stronger than only `Tester` because it sounds like measuring equipment, not only an accessory.

5. `Bluetooth`
   - Premium differentiator.
   - Confirmed by manual and device symbol.
   - Important because many cheap USB testers do not have app/BLE-style function.

6. `Power Meter`
   - Value-class term.
   - Raises product class from simple tester to power measuring device.

7. `Spannung Strom`
   - Plain German buyer intent words.
   - Helps normal buyers who want to measure voltage/current.

8. `PD QC`
   - Protocol/value terms.
   - Distinguishes fast-charge/USB protocol testing from simple meters.

### Reusable title formula

```text
[Brand] [Model] [USB DC] [German product class] [premium differentiator] [value-class term] [buyer intent measurements] [protocol/value terms]
```

For UD24:

```text
ATORCH UD24 USB DC Messgerät Bluetooth Power Meter Spannung Strom PD QC
```

### Alternative test variants

```text
ATORCH UD24 USB DC Bluetooth Power Meter Messgerät Spannung Strom PD QC
ATORCH UD24 USB DC Digital Tester Bluetooth Power Meter PD QC Messgerät
ATORCH UD24 USB DC Tester Bluetooth Voltmeter Amperemeter Power Meter
ATORCH UD24 USB DC Messgerät Bluetooth Leistungsmesser Spannung Strom PD QC
```

Important: after the listing was enriched, changing between close title variants did **not** move recommended price much. That suggests the value cluster had already been set by the full listing state, not title alone.

---

## 4. Title-order lesson for future agents

The order matters because early words are likely stronger for marketplace interpretation and buyer scanning.

Recommended order for technical products:

```text
1. Brand / Marke
2. Model / Modell
3. Core interface or product family
4. German category/product class
5. Premium feature / differentiator
6. High-value function class
7. Buyer intent measurement words
8. Protocol / compatibility / range terms
```

For this product:

```text
1. ATORCH
2. UD24
3. USB DC
4. Messgerät
5. Bluetooth
6. Power Meter
7. Spannung Strom
8. PD QC
```

Why not start with `USB Tester`?

Because `USB Tester` is too broad and cheap. It can pull the listing into a low-value cluster. For cheap accessories this may be acceptable. For UD24 it is harmful because it hides the advanced identity.

Why not remove brand/model?

Removing brand/model made the title more generic and pushed the product closer to the cheap commodity category. For technical devices where the model is a known signal, keep brand/model.

---

## 5. Item specifics — the most important lesson

The operator observed that eBay shows search-count signals beside several item-specific fields. These are not decorative fields. They are marketplace-visible filter/search/value signals.

Observed high-signal fields:

```text
Produktart ~25,366 Suchen
Anzeige ~6,438 Suchen
Anzeigetyp ~6,329 Suchen
Test-/Messfunktionen ~596 Suchen
Eigenschaften ~236 Suchen
Widerstand Messauflösung ~148 Suchen
```

### Interpretation

Fields with search counts should become priority fields for the agent. If the field has a search count, buyers are likely filtering/searching with it. Leaving such fields blank reduces the listing's ability to match buyer intent.

### Required agent behavior

When the agent opens/edit-checks an eBay listing, it must scan for item-specific fields with visible marketplace signals such as `Suchen` counts. It must rank them by count and fill safely from confirmed product data.

### Priority for UD24

1. Produktart
2. Anzeige
3. Anzeigetyp
4. Test-/Messfunktionen
5. Eigenschaften / Besonderheiten
6. Widerstand Messauflösung — high potential, but not confirmed
7. Anschlüsse
8. Modell
9. Farbe
10. Lieferumfang

---

## 6. Recommended item specifics for UD24

Use these when the dropdown allows them. If exact option not available, choose the closest correct German option.

```text
Marke: ATORCH
EAN: Nicht zutreffend
Produktart: USB/DC Messgerät
Anzeige: Digital
Anzeigetyp: Farbdisplay / Digital / LCD, depending on dropdown
Herstellernummer: UD24
Modell: UD24
Test-/Messfunktionen: Spannung, Strom, Leistung, Kapazität, Widerstand
Messfunktionen: Spannung, Strom, Leistung, Kapazität, Widerstand
Eigenschaften: Bluetooth, Farbdisplay, Metallbox, USB-C, DC5.5-Anschluss
Besonderheiten: Bluetooth, E-Test App laut Anleitung, Farbdisplay, Metallbox
Anschlüsse: USB-A, USB-C/Type-C, Micro-USB, DC5.5
Farbe: Schwarz
Typ: USB-Tester / USB/DC Messgerät, depending on field
Einheit: Stück
Lieferumfang: USB/DC Tester, Metallbox, Bedienungsanleitung
Batterietyp: Nicht zutreffend
Wasserschutz: Nicht zutreffend / Nicht wasserdicht if available
```

### Do not guess these fields

```text
Widerstand Messauflösung
Genauigkeit
Messkategorie / CAT rating
Sicherheitsniveau
Maximale AC Spannung
Maximaler AC Strom
Gleichstrom Messauflösung
Kapazität Messauflösung
Temperatur Messauflösung
Exact resistance/capacity/current resolution
```

### Widerstand Messauflösung special rule

The field showed about 148 searches. This means it may matter. But the exact resolution was not confirmed in the real photos/manual sections inspected during the chat.

Agent rule:

```text
If Widerstand Messauflösung is available but exact value is not confirmed:
- Do not invent 0.001 Ω / 1 mΩ / 0.01 Ω.
- Mark field as NEEDS_SOURCE.
- Search manual, official page, rear label, or trusted supplier document.
- If no exact source is found, leave blank or select Keine Angabe / Nicht zutreffend if appropriate.
- Still include Widerstand in Messfunktionen if the device display/manual confirms Res/Widerstand measurement.
```

---

## 7. Bluetooth discovery and value impact

Bluetooth was initially underweighted. The operator correctly pointed out that real photos/manual showed a Bluetooth symbol and the blue/instruction sheet described app connection.

Confirmed manual context:

```text
How to connect to E-Test APP via mobile phone Bluetooth
Android phone version 5.0 or higher
UD24-BLE signal
Support Bluetooth computer connection and wired connection
WIN7 / WIN10 mentioned
```

### Why Bluetooth matters

Bluetooth is a premium differentiator. It separates the product from cheap screen-only USB testers.

### How to state Bluetooth safely

Use conservative wording:

```text
Bluetooth / E-Test App laut beiliegender Anleitung
```

Description block:

```text
Laut beiliegender Anleitung unterstützt das Gerät die Verbindung mit der E-Test App per Bluetooth. In der Anleitung wird ein UD24-BLE Signal sowie Android ab Version 5.0 oder höher erwähnt. Zusätzlich wird eine Bluetooth-Computerverbindung sowie eine kabelgebundene Verbindung für WIN7/WIN10 beschrieben.
```

Do not overclaim:

```text
Works with all phones
Guaranteed app support forever
Official app currently maintained
All iOS/Android versions supported
```

Unless verified from current official source.

---

## 8. Description formula

The first short description was too weak:

```text
ATORCH UD24 USB Tester mit 2,4 Zoll Display für USB-C/DC Messungen...
```

It did not fully communicate value. The improved description must support the same value signals as the title and item specifics.

### Effective description order

1. Product identity
2. Core measurement functions
3. Use cases
4. Confirmed technical range
5. Confirmed protocols
6. Bluetooth/app function
7. Connections
8. Package contents
9. Explicit exclusion of accessory kit
10. Buyer safety note: verify purpose/connection/range

### Description content structure

```text
ATORCH UD24 USB/DC Digital Tester zur Anzeige von Spannung, Strom, Leistung, Kapazität und Widerstand.

Das Messgerät eignet sich zur Prüfung von USB- und DC-Quellen wie Ladegeräten, Powerbanks, USB-Kabeln und passenden USB-Verbrauchern. Über das Farbdisplay lassen sich wichtige Messwerte übersichtlich ablesen.

Wichtige Merkmale:
- USB/DC Messgerät mit digitalem Farbdisplay
- Anzeige von Spannung, Strom, Leistung, Kapazität und Widerstand
- Spannungs-/Strombereich laut Geräteaufdruck: 5–32 V / 0–5,1 A
- Unterstützt laut Geräteaufdruck: PD2.0 / PD3.0 / PD4.0, QC2.0 / QC3.0, BC1.2, Apple
- Bluetooth / E-Test App laut beiliegender Anleitung
- Anschlüsse: USB-A, USB-C/Type-C, Micro-USB, DC5.5
- Kompaktes Gerät mit Metallbox zur Aufbewahrung

Lieferumfang:
1x ATORCH UD24 USB/DC Tester
1x Metallbox
1x Bedienungsanleitung

Hinweis:
Es ist kein Zubehör-Kit enthalten. Kabel, Adapter, Trigger-Boards oder weitere Zubehörteile sind nicht Bestandteil dieses Angebots.
```

### HTML lesson

After item specifics + title + description were already enriched, changing HTML style did not visibly change the recommended price in the tested moment. Therefore, HTML is likely more important for buyer conversion/trust than for the price recommendation itself.

Agent rule:

```text
HTML improves readability and conversion, not necessarily immediate recommended price.
Do not treat HTML as the main value lever.
Use clean mobile-friendly HTML without scripts.
```

---

## 9. Gallery/image generation route

The gallery was a major part of the listing value system. The operator wanted the product to look like a real higher-value device, not a cheap loose USB tester.

### Source hierarchy for image generation

1. Real operator photos = truth layer.
2. Real manual/rear label = feature/spec truth layer.
3. Supplier clean image = visual style/reference only.
4. Old supplier accessory image = blocked for package contents.

### Critical correction

Earlier supplier images showed many accessories. The operator clarified that the real product does not include those accessories. The successful gallery therefore removed cables/adapters/triggers and focused only on:

```text
UD24 tester
metal box
manual
side covers as part of the product
```

### Successful gallery structure

1. Hero image
   - ATORCH UD24 USB- & DC-Tester
   - manual behind product
   - metal box included
   - `Ohne Zubehör-Kit` badge
   - safe callouts: 5–32 V, 0–5.1 A, Strom/Spannung/Kapazität/Leistung, USB/DC Anschlüsse

2. Produktübersicht
   - Callouts for real visible connectors
   - USB-Eingang
   - Micro-USB-Eingang
   - DC5.5-Eingang
   - Power Supply / NTC 5–30 V
   - Type-C-Eingang
   - USB-Ausgang
   - Type-C-Ausgang
   - DC5.5-Ausgang

3. Details im Fokus
   - M/+ Taste
   - OK/- Taste
   - Power-Anzeige
   - Farbdisplay
   - Bedienseite / Steuerung

4. Technische Angaben
   - Use rear-label-based data only
   - Model UD24
   - 5–32 V / 0–5.1 A
   - USB/DC measurement for current, voltage, capacity, power
   - PD/QC/BC1.2/Apple support according to device label

5. So wird es angeschlossen
   - Source -> tester -> device/load
   - Simple German steps
   - No impossible wiring

6. Praktisch im Alltag
   - Clean desk/workstation lifestyle scene
   - Monitoring charging process
   - Does not imply accessories included

7. Vielseitig einsetzbar
   - USB-Netzteil
   - Powerbank
   - Smartphone / USB-Gerät
   - DC5.5-Quelle
   - No universal compatibility claim

8. Sicher verstaut
   - Metal box open/closed
   - Clean storage / compact format / transport

9. Lieferumfang
   - 1x ATORCH UD24 Tester
   - 1x Metallbox
   - 1x Bedienungsanleitung
   - No cables/adapters/triggers

10. Ihre Vorteile auf einen Blick
   - Farbdisplay
   - USB- & DC-Anschlüsse
   - Metallbox inklusive
   - Kompaktes Messgerät

### Image prompt rules for future agents

```text
Use German text only.
Preserve real geometry.
Do not invent ports.
Do not invent accessories.
Do not show kit items that are not included.
Do not overpromise compatibility.
Use real photo truth layer for package contents.
Use supplier images only for polish/styling, not factual package claims.
Prefer clean white/light-gray background, black/gold premium design.
Main image should communicate value immediately: device + metal box + manual + no accessory kit.
```

---

## 10. Marketplace algorithm lesson from official eBay guidance

Official eBay Best Match guidance states that eBay considers multiple factors including how closely a listing matches buyer search terms, item popularity, price, listing quality such as description/photos, listing completeness, service terms such as returns/handling time, and seller track record.

For ECOM OS, interpret this as:

```text
Title alone is not enough.
The agent must optimize the whole listing system.
```

Official eBay guidance also recommends complete and accurate listings, clear concise titles with no more than 80 characters, accurate descriptions, high-quality photos, item specifics, right category, selling terms, and positive seller history.

Promoted Listings official guidance states that dynamic/suggested ad rates can be based on item attributes, seasonality, past performance, and current competition. This confirms that ads are not independent: they also depend on item/listing quality and competitive context.

Source notes used for this archive:

```text
https://www.ebay.com/help/selling/listings/listing-tips/optimising-listings-best-match?id=4166
https://www.ebay.com/help/selling/ebay-advertising/promoted-listings/general-campaign-strategy?id=4164
```

---

## 11. Delivery and advertising lesson

The eBay page showed sold-offer comparison and free shipping percentage. For this item, the panel showed a strong free shipping signal in sold offers.

### Delivery interpretation

Delivery likely affects conversion and buyer comparison more than the immediate product identity, but it is still part of Best Match and value perception.

Agent rule:

```text
If comparable sold offers show high free-shipping share, evaluate whether shipping should be included in item price.
Do not blindly set free shipping without margin calculation.
Record delivery policy and shipping cost in experiment log.
```

### Advertising interpretation

The operator chose 7% ad rate. This is acceptable as a starting experiment.

Agent logic for ads:

```text
Start: 6–7% after listing is already optimized.
If no impressions after 3–5 days: check category/title/item specifics first, then consider +1% ad rate.
If impressions but no clicks: main image/title mismatch likely; revise hero/photo order/title.
If clicks but no sales: check price, delivery, description trust, package clarity, returns.
If sales with acceptable margin: keep stable and observe.
```

Important: do not increase ad rate endlessly to fix a weak listing. Fix the listing first.

---

## 12. What exactly must be logged by the future agent

Every experiment must produce a structured log. Without logging, the system forgets and repeats mistakes.

### Required log fields

```json
{
  "experiment_id": "UD24_2026_05_30_TITLE_SPEC_PHOTO_VALUE_SIGNAL",
  "product": "ATORCH UD24",
  "marketplace": "ebay.de",
  "category": "Multimeter",
  "listing_id": null,
  "timestamp": "2026-05-30",
  "operator": "ION",
  "title": "ATORCH UD24 USB DC Messgerät Bluetooth Power Meter Spannung Strom PD QC",
  "title_formula": "Brand + Model + USB DC Messgerät + Bluetooth + Power Meter + Spannung/Strom + PD/QC",
  "title_character_count": 71,
  "recommended_price_before_eur": "~7-10 for weak generic titles, ~15 for earlier partial versions",
  "recommended_price_after_eur": 20.24,
  "listing_price_eur": 22.99,
  "quantity": 2,
  "ad_rate_percent": 7,
  "photo_gallery_state": "premium_gallery_real_truth_layer_no_accessory_kit",
  "item_specifics_state": "enriched_high_signal_fields",
  "description_state": "safe_confirmed_value_claims_with_bluetooth",
  "delivery_signal": "free shipping observed in sold-offer comparison panel",
  "changed_variables": [
    "title",
    "item_specifics",
    "description",
    "photo_gallery",
    "ad_rate"
  ],
  "blocked_claims": [
    "accessory kit included",
    "cables included",
    "exact resistance resolution",
    "high precision without source",
    "waterproof without source"
  ],
  "result_note": "Full value-signal enrichment moved listing from cheap generic USB tester cluster toward higher-value UD24/Bluetooth/Power Meter cluster."
}
```

### Post-publish observation log

After publishing, record:

```text
Day 0: title, price, ad rate, item specifics, photo order, description snapshot
Day 3–5: impressions, clicks, watchers, ad impressions, ad clicks, recommended price drift
Day 7–14: sales, conversion, watchers, buyer messages, need for revision
After sale: sale price, ad fee, net margin, buyer feedback/return risk
```

---

## 13. Future agent: MARKET_VALUE_SIGNAL_AGENT_V1

This agent should be added to ECOM OS as a marketplace optimization specialist.

### Mission

Increase perceived and algorithmic listing value without false claims.

### Inputs

```text
Product photos
Supplier data
Manual / rear label / package photos
Current eBay listing state
Category
Item specifics fields and search-count signals
Current title
Current description
Current price
Delivery policy
Ad rate
Seller performance data
Marketplace comparable/sold data when available
```

### Outputs

```text
Value-signal audit
Safe title variants
Item-specifics fill plan
Photo order plan
Description improvement plan
Ad-rate recommendation
Experiment log
Approval request
Post-change verification plan
```

### Workflow

1. Read current listing.
2. Detect category and compare whether category is correct.
3. Extract high-search item-specific fields shown by marketplace.
4. Build truth layer from real photos/manual/rear label.
5. Fill high-signal fields safely.
6. Flag unconfirmed fields as NEEDS_SOURCE.
7. Generate title formula and variants.
8. Predict risk: cheap cluster vs premium cluster.
9. Propose one controlled change batch.
10. Wait for operator approval.
11. Apply update through API or UI-assisted process.
12. Read-only verify.
13. Log recommended price / impressions / clicks / results.
14. Learn formula for product class.

### Safety gates

```text
No live revise without approval.
No invented specs.
No fake accessories.
No false compatibility.
No changing category blindly.
No deleting photos without backup.
No title testing without logging current recommended price.
No multi-variable test without recording what changed.
```

---

## 14. Future teacher/updater agent

The operator also requested a teacher/updater layer so the system keeps learning when marketplaces change.

Proposed agent:

```text
MARKETPLACE_RULES_TEACHER_AGENT_V1
```

Responsibilities:

```text
Monitor marketplace rule changes.
Search official eBay/Amazon documentation when behavior changes.
Update optimization rules.
Store lessons in memory archive.
Convert lessons into agent instructions.
Separate stable lessons from temporary experiments.
```

This agent must not blindly trust old formulas. It should periodically verify marketplace documentation and live behavior.

---

## 15. General formula for future technical products

For technical/electronic measurement products, use this framework:

### Title formula

```text
Brand + Model + Product class + Premium differentiator + Core measurement/function + Range/protocol/value terms
```

Examples:

```text
ATORCH UD24 USB DC Messgerät Bluetooth Power Meter Spannung Strom PD QC
[Brand] [Model] [USB DC Messgerät] [Bluetooth] [Power Meter] [Spannung Strom] [PD QC]
```

### Item specifics formula

```text
1. Brand/model identifiers
2. Product type
3. Display type
4. Measurement functions
5. Premium features
6. Connections/interfaces
7. Range values from label/manual
8. Supported protocols from label/manual
9. Package contents
10. Exclusions if needed
```

### Image formula

```text
1. Truth-based hero
2. Connection overview
3. Display / values
4. Technical specs
5. How-to-use
6. Lifestyle/use case
7. Package contents
8. Storage/quality
9. Final benefit summary
```

### Description formula

```text
Identity -> Purpose -> Measurements -> Range -> Protocols -> Premium function -> Connections -> Package -> Exclusions -> Buyer note
```

---

## 16. What not to do in future

This section is important. It prevents repeating the same errors.

Do not:

```text
1. Build title only for simple buyer language and ignore value class.
2. Remove brand/model when they help value recognition.
3. Use supplier accessory images as package truth.
4. Claim cable/adapters/triggers if not included.
5. Guess exact measurement resolution.
6. Treat HTML as the main value lever.
7. Keep changing title after the value cluster is already established without logging.
8. Ignore item specifics with visible search-count signals.
9. Assume all eBay price recommendation changes come from title only.
10. Publish live changes without operator approval.
11. Optimize ads before listing quality is complete.
12. Increase ad rate to hide weak listing structure.
```

---

## 17. Current final action for this product

The operator decided:

```text
Save/publish current optimized UD24 listing.
Keep title stable.
Keep photo order stable.
Keep ad rate at 7%.
Observe future performance.
Return to core ECOM OS project before doing more product experiments.
```

Current title to keep:

```text
ATORCH UD24 USB DC Messgerät Bluetooth Power Meter Spannung Strom PD QC
```

Current price:

```text
22.99 EUR
```

Current recommended price observed:

```text
20.24 EUR
```

Current learning state:

```text
PASS: value signal improved enough for current experiment.
NEXT: publish/observe, then return to ECOM OS core work.
```

---

## 18. Compact agent rule card

For fast future reference:

```text
If technical product has low eBay recommended price:
1. Do not only rewrite title.
2. Read category + item specifics + visible search-count fields.
3. Build real truth layer from photos/manual/label.
4. Fill high-signal specifics safely.
5. Use title formula: Brand + Model + Product Class + Premium Feature + Value Function + Buyer Intent + Protocols.
6. Use photos to show value: hero, ports, specs, use case, package truth.
7. Description must repeat confirmed value signals.
8. Block fake accessories and unsupported claims.
9. Use ads only after listing quality is strong.
10. Log recommended price before/after every change.
```

End of full route archive.
