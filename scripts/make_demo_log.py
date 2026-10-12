import ipaddress
import json
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

rng = random.Random(42)
now = datetime.now(timezone.utc)
start = now - timedelta(days=3)
span = (now - start).total_seconds()

SERVICES = {"ssh": (4002, 2222), "http": (3001, 8080), "ftp": (2000, 2121)}
USERS = ["root", "admin", "ubuntu", "test", "oracle", "pi"]
PASSWORDS = ["123456", "password", "admin", "qwerty", "letmein"]


def random_public_ip():
    while True:
        ip = ipaddress.IPv4Address(rng.getrandbits(32))
        if ip.is_global and not ip.is_multicast:
            return str(ip)


def make_line(ts, ip, service):
    logtype, port = SERVICES[service]
    stamp = ts.strftime("%Y-%m-%d %H:%M:%S.%f")
    return json.dumps(
        {
            "dst_host": "10.0.0.5",
            "dst_port": port,
            "local_time": stamp,
            "local_time_adjusted": stamp,
            "logdata": {"USERNAME": rng.choice(USERS), "PASSWORD": rng.choice(PASSWORDS)},
            "logtype": logtype,
            "node_id": "honeymap-demo",
            "src_host": ip,
            "src_port": rng.randint(1024, 65535),
            "utc_time": stamp,
        }
    )


lines = []

# Background noise: one probe each from many different IPs
for _ in range(150):
    ts = start + timedelta(seconds=rng.random() * span)
    lines.append((ts, make_line(ts, random_public_ip(), rng.choice(list(SERVICES)))))

# Brute-force bursts: one IP hammering one service
for _ in range(5):
    ip = random_public_ip()
    service = rng.choice(["ssh", "ftp"])
    burst_start = start + timedelta(seconds=rng.random() * span)
    for i in range(rng.randint(15, 60)):
        ts = burst_start + timedelta(seconds=i * rng.uniform(0.5, 5))
        lines.append((ts, make_line(ts, ip, service)))

lines.sort()
out = Path("data/logs/demo.log")
out.write_text("\n".join(line for _, line in lines) + "\n")
print(f"wrote {len(lines)} synthetic events to {out}")