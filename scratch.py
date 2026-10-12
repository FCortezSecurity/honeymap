import sys

sys.path.insert(0, "src")

from honeymap.normalize import parse_line

with open("data/logs/sample.log") as f:
    for line in f:
        print(parse_line(line))