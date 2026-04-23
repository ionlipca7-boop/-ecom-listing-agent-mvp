import json
from pathlib import Path

def load_json(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return json.loads(Path(p).read_text(encoding="utf-8-sig"))

base = Path(".")
src = load_json(base / "storage" / "memory" / "archive" / "working_listing_baseline_v1.json")
out_path = base / "storage" / "exports" / "improvement_brief_v1.json"

image_urls = src.get("inventory_image_urls", [])

target_title = "USB-C OTG Adapter USB 3.0 Typ C auf USB-A 6A 120W Datenadapter"
target_description = "^<h2^>USB-C OTG Adapter USB 3.0^</h2^>^<p^><b^>Kompakter Adapter fuer Laden und Datenuebertragung.^</b^>^</p^>^<ul^>^<li^>USB-C auf USB-A OTG Adapter^</li^>^<li^>USB 3.0 fuer schnelle Datenuebertragung^</li^>^<li^>Geeignet fuer Smartphone, Tablet, Laptop und Zubehoer^</li^>^<li^>Kompaktes Format fuer unterwegs^</li^>^<li^>Farbe: Schwarz/Orange^</li^>^</ul^>^<p^><b^>Hinweis:^</b^> Bitte vor dem Kauf die Kompatibilitaet Ihres Geraets pruefen.^</p^>^<p^><b^>Schneller Versand aus Deutschland.^</b^>^</p^>"

photo_order = []
labels = [
  "Hero / Hauptbild",
  "Frontansicht",
  "Produkt im Set",
  "Anschluss Detail",
  "Nutzung am Smartphone",
  "Anwendung Beispiel",
  "Seitenansicht",
  "Kompatibilitaet Bild",
  "Zusatzbild / Reserve"
]
for i, u in enumerate(image_urls):
    photo_order.append({"position": i + 1, "label": labels[i] if i < len(labels) else "Bild", "url": u})

data = {
  "status": "OK",
  "decision": "improvement_brief_v1_built",
  "sku": src["sku"],
  "offer_id": src["offer_id"],
  "item_id": src["item_id"],
  "baseline_price": src["price"],
  "baseline_inventory_picture_count": src["inventory_picture_count"],
  "target_title": target_title,
  "target_description_html": target_description,
  "photo_order_plan": photo_order,
  "rules": [
    "do_not_break_working_price",
    "do_not_break_required_aspects",
    "do_not_replace_eps_images_with_external_urls",
    "next_live_step_should_use_full_payload"
  ],
  "next_step": "build_live_improvement_update_v1"
}

out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("IMPROVEMENT_BRIEF_V1_FINAL_AUDIT")
print("status =", data["status"])
print("decision =", data["decision"])
print("sku =", data["sku"])
print("baseline_price =", data["baseline_price"])
print("baseline_inventory_picture_count =", data["baseline_inventory_picture_count"])
print("target_title =", data["target_title"])
print("photo_order_count =", len(data["photo_order_plan"]))
print("next_step =", data["next_step"])
