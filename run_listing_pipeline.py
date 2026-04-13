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


if __name__ == "__main__":
    main()
