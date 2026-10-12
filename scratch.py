import sys

sys.path.insert(0, "src")

from honeymap.normalize import ParseError, parse_line

with open("data/logs/sample.log") as f:
    for number, line in enumerate(f, start=1):
        try:
            print(parse_line(line))
        except ParseError as error:
            print(f"line {number} rejected: {error}")