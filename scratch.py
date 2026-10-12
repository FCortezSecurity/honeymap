import json

with open("data/logs/sample.log") as f:
    for line in f:
        record = json.loads(line)
        print(record["src_host"], record["dst_port"], record["logtype"])