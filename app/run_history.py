import json
from datetime import datetime
from pathlib import Path


class RunHistoryArchive:
    def __init__(self, history_dir="history"):
        self.history_dir = Path(history_dir)

    def save_run(
        self,
        *,
        raw_input,
        parsed_product,
        listing_result,
        publish_result,
        pipeline_summary,
    ):
        self.history_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        history_path = self.history_dir / f"run_{timestamp}.json"
        counter = 1
        while history_path.exists():
            history_path = self.history_dir / f"run_{timestamp}_{counter}.json"
            counter += 1

        history_record = {
            "timestamp": timestamp,
            "raw_input": raw_input,
            "parsed_product": parsed_product,
            "listing_result": listing_result,
            "publish_result": publish_result,
            "pipeline_summary": pipeline_summary,
        }

        with history_path.open("w", encoding="utf-8") as f:
            json.dump(history_record, f, ensure_ascii=False, indent=2)

        return str(history_path)
