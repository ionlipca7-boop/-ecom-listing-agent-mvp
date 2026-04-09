from agent.brain import ListingBrain

brain = ListingBrain()

product = {
    "name": "USB-C Kabel",
    "power": "60W",
    "length": "2m",
    "base_price": 2.5
}

result = brain.create_listing_plan(product)

print(result)