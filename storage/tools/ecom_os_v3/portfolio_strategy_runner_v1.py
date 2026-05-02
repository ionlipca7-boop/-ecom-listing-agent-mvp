from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parents[2]
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from agents.listing_lifecycle_agent_v1 import ListingLifecycleAgentV1
from agents.promotion_offers_agent_v1 import PromotionOffersAgentV1
from agents.listing_health_dashboard_agent_v1 import ListingHealthDashboardAgentV1
from agents.inventory_reorder_agent_v1 import InventoryReorderAgentV1
from agents.variation_agent_v1 import VariationAgentV1
from agents.cross_sell_bundle_agent_v1 import CrossSellBundleAgentV1


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_portfolio(path: Path) -> List[Dict[str, Any]]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return list(raw.get("portfolio") or [])


def main() -> int:
    input_path = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else CURRENT_DIR / "test_inputs" / "sample_portfolio_v1.json"
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = PROJECT_ROOT / "storage" / "outputs" / "ecom_os_v3" / "portfolio_strategy" / run_id
    out_dir.mkdir(parents=True, exist_ok=True)

    portfolio = load_portfolio(input_path)
    write_json(out_dir / "00_portfolio_input.json", {"portfolio": portfolio})

    dashboard = ListingHealthDashboardAgentV1().run(portfolio).to_dict()
    write_json(out_dir / "01_listing_health_dashboard.json", dashboard)

    lifecycle = ListingLifecycleAgentV1().run(portfolio).to_dict()
    write_json(out_dir / "02_listing_lifecycle_decisions.json", lifecycle)

    promotion = PromotionOffersAgentV1().run(portfolio).to_dict()
    write_json(out_dir / "03_promotion_offer_decisions.json", promotion)

    inventory = InventoryReorderAgentV1().run(portfolio).to_dict()
    write_json(out_dir / "04_inventory_reorder_decisions.json", inventory)

    variation_results = []
    for item in portfolio:
        variation_results.append(VariationAgentV1().run(item).to_dict())
    write_json(out_dir / "05_variation_decisions.json", {"status": "PASS", "items": variation_results})

    cross_sell_results = []
    for item in portfolio:
        cross_sell_results.append(CrossSellBundleAgentV1().run(item, portfolio).to_dict())
    write_json(out_dir / "06_cross_sell_bundle_decisions.json", {"status": "PASS", "items": cross_sell_results})

    summary = {
        "status": "PASS",
        "layer": "ECOM_OS_V3_PORTFOLIO_STRATEGY_RUNNER_V1",
        "run_id": run_id,
        "output_dir": str(out_dir),
        "files": [p.name for p in sorted(out_dir.iterdir())],
        "dashboard_summary": dashboard.get("summary"),
        "next_allowed_action": "REVIEW_PORTFOLIO_STRATEGY_WITH_OPERATOR",
        "no_server": True,
        "no_live_ebay": True,
        "no_delete": True,
    }
    write_json(out_dir / "07_portfolio_strategy_summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
