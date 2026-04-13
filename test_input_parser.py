from app.input_parser import InputParser

raw_text = "USB-C cable 2m 60W fast charging"
print(InputParser().parse_text(raw_text))
