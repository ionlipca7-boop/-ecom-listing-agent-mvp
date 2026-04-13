from app.input_parser import InputParser

parser = InputParser()

samples = [
    "USB-C cable 2m 60W fast charging",
    "usb c cable 2m 60w",
]

for raw_text in samples:
    print(raw_text, "->", parser.parse_text(raw_text))
