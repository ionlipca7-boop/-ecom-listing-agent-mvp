from agent.brain import ListingBrain
from publisher.local_publisher import LocalPublisher


def main():
    product = {
        "name": "USB-C Ladekabel",
        "type": "USB-C Ladekabel",
        "power": "60W",
        "length": "2m",
    }

    brain = ListingBrain()
    listing = brain.create_listing(product)

    bundle = listing["final_listing_bundle"]
    publish_result = LocalPublisher().publish(bundle)

    print("LISTING RESULT:")
    print(listing)
    print("PUBLISH RESULT:")
    print(publish_result)

    listing_quality_score = listing.get("listing_quality_score", listing.get("quality_score", 0)) if isinstance(listing, dict) else 0
    publish_ready = listing.get("publish_ready", False) if isinstance(listing, dict) else False
    listing_warnings = listing.get("listing_warnings", listing.get("warnings", [])) if isinstance(listing, dict) else []
    listing_improvements = listing.get("listing_improvements", listing.get("improvements", [])) if isinstance(listing, dict) else []
    publish_status = publish_result.get("status", "unknown") if isinstance(publish_result, dict) else "unknown"

    print("PIPELINE SUMMARY:")
    print(f"- quality_score: {listing_quality_score}")
    print(f"- publish_ready: {publish_ready}")
    print(f"- warnings_count: {len(listing_warnings) if isinstance(listing_warnings, list) else 0}")
    print(f"- improvements_count: {len(listing_improvements) if isinstance(listing_improvements, list) else 0}")
    print(f"- publish_status: {publish_status}")


if __name__ == "__main__":
    main()
