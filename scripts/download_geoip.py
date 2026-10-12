import gzip
import shutil
import urllib.error
import urllib.request
from datetime import date, timedelta
from pathlib import Path

OUT = Path("data/geoip")
OUT.mkdir(parents=True, exist_ok=True)


def months_to_try():
    """This month's file first; fall back to last month if it isn't published yet."""
    today = date.today()
    last_month = today.replace(day=1) - timedelta(days=1)
    return [today.strftime("%Y-%m"), last_month.strftime("%Y-%m")]


def download(kind):
    dest = OUT / f"dbip-{kind}-lite.mmdb"
    for month in months_to_try():
        url = f"https://download.db-ip.com/free/dbip-{kind}-lite-{month}.mmdb.gz"
        request = urllib.request.Request(url, headers={"User-Agent": "honeymap-learning-project"})
        try:
            with urllib.request.urlopen(request) as response, open(dest, "wb") as out:
                with gzip.GzipFile(fileobj=response) as unzipped:
                    shutil.copyfileobj(unzipped, out)
        except urllib.error.HTTPError as error:
            print(f"{url} -> HTTP {error.code}, trying the previous month")
            continue
        print(f"{kind}: saved {dest} (data from {month})")
        return
    print(f"{kind}: could not download. Check your connection or db-ip.com")


download("city")
download("asn")