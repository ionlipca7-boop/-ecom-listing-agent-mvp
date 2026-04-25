import json, pathlib, sys
root=pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0,str(root))
from agent.brain import ListingBrain
brain=ListingBrain()
input_payload={"name":"USB-C Ladekabel","power":"60W","length":"2m","category":"Kabel"}
listing=brain.create_listing(input_payload)
out={"status":"OK","layer":"RUN_LISTING_FLOW_V1","project":"ECOM_LISTING_AGENT_MVP","input_payload":input_payload,"listing_output":listing,"publish_allowed":False,"real_ebay_api_call_allowed":False,"next_allowed_action":"build_approval_decision_record_v1"}
p=root/r"storage\state_control\run_listing_flow_v1_result.json"
p.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
print(json.dumps(out,ensure_ascii=False,indent=2))
