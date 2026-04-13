from agent.brain import ListingBrain
from publisher.local_publisher import LocalPublisher


brain = ListingBrain()

product = {
    "name": "USB-C Kabel",
    "power": "60W",
    "length": "2m",
    "base_price": 2.5,
}

listing = brain.create_listing(product)
publish_result = LocalPublisher().publish(listing["final_listing_bundle"])

print(publish_result)
