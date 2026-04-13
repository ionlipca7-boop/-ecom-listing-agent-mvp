import json
from datetime import datetime
from pathlib import Path


class LocalPublisher:
    def publish(self, listing):
        logs_dir = Path("logs")
        logs_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        is_publish_ready = bool(listing.get("publish_ready"))

        publish_result = {
            "published": True if is_publish_ready else False,
            "channel": "local_simulator",
            "title": listing.get("title"),
            "category": listing.get("category"),
            "price": listing.get("price"),
            "timestamp": timestamp,
            "status": "published" if is_publish_ready else "failed",
        }

        publish_path = logs_dir / f"publish_{timestamp}.json"
        counter = 1
        while publish_path.exists():
            publish_path = logs_dir / f"publish_{timestamp}_{counter}.json"
            counter += 1

        with publish_path.open("w", encoding="utf-8") as f:
            json.dump(publish_result, f, ensure_ascii=False, indent=2)

        return publish_result
