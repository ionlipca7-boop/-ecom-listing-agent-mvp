from app.input_parser import InputParser

parser = InputParser()

samples = [
    "USB-C cable 2m 60W fast charging",
    "usb c cable 2m 60w",
    "67w usb c charger with 2m cable",
    "usb c ladegerät 67w mit 2m kabel",
]

for raw_text in samples:
    print(raw_text, "->", parser.parse_text(raw_text))
