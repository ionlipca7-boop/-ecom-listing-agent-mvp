import sys

from agent.brain import ListingBrain
from app.input_parser import InputParser
from app.listing_optimizer import ListingOptimizer
from app.run_history import RunHistoryArchive
from publisher.local_publisher import LocalPublisher


def main():
    if len(sys.argv) > 1:
        raw_text = " ".join(sys.argv[1:])
    else:
        raw_text = "USB-C cable 2m 60W fast charging"

    product = InputParser().parse_text(raw_text)

    brain = ListingBrain()
    listing = brain.create_listing(product)

    optimizer = ListingOptimizer()
    listing = optimizer.optimize(listing)
    listing["final_listing_bundle"] = brain.generate_final_listing_bundle(listing)
    optimization_notes = listing.get("optimization_notes", [])
    if isinstance(optimization_notes, list):
        optimization_notes.append("Final listing bundle rebuilt after optimization")
        listing["optimization_notes"] = optimization_notes

    bundle = listing["final_listing_bundle"]
    publish_result = LocalPublisher().publish(bundle)

    print("LISTING RESULT:")
    print(listing)
    print("PUBLISH RESULT:")
    print(publish_result)

    listing_quality_score = listing.get("listing_quality_score", listing.get("quality_score", 0)) if isinstance(listing, dict) else 0
    publish_ready = listing.get("publish_ready", False) if isinstance(listing, dict) else False
    approval_status = listing.get("status", "unknown") if isinstance(listing, dict) else "unknown"
    quality_gate_ready = listing.get("quality_gate_ready", False) if isinstance(listing, dict) else False
    listing_warnings = listing.get("listing_warnings", listing.get("warnings", [])) if isinstance(listing, dict) else []
    listing_improvements = listing.get("listing_improvements", listing.get("improvements", [])) if isinstance(listing, dict) else []
    publish_status = publish_result.get("status", "unknown") if isinstance(publish_result, dict) else "unknown"

    pipeline_summary = {
        "quality_score": listing_quality_score,
        "approval_status": approval_status,
        "quality_gate_ready": quality_gate_ready,
        "publish_ready": publish_ready,
        "warnings_count": len(listing_warnings) if isinstance(listing_warnings, list) else 0,
        "improvements_count": len(listing_improvements) if isinstance(listing_improvements, list) else 0,
        "optimization_notes_count": len(listing.get("optimization_notes", [])) if isinstance(listing, dict) else 0,
        "publish_status": publish_status,
    }

    history_path = RunHistoryArchive().save_run(
        raw_input=raw_text,
        parsed_product=product,
        listing_result=listing,
        publish_result=publish_result,
        pipeline_summary=pipeline_summary,
    )

    print("PIPELINE SUMMARY:")
    print(f"- quality_score: {pipeline_summary['quality_score']}")
    print(f"- approval_status: {pipeline_summary['approval_status']}")
    print(f"- quality_gate_ready: {pipeline_summary['quality_gate_ready']}")
    print(f"- publish_ready: {pipeline_summary['publish_ready']}")
    print(f"- warnings_count: {pipeline_summary['warnings_count']}")
    print(f"- improvements_count: {pipeline_summary['improvements_count']}")
    print(f"- optimization_notes_count: {pipeline_summary['optimization_notes_count']}")
    print(f"- publish_status: {pipeline_summary['publish_status']}")
    print(f"- history_path: {history_path}")


if __name__ == "__main__":
    main()
