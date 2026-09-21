#!/usr/bin/env python3
"""Download the three raw data files build_benchmark.py needs, into data/raw/
(gitignored — nothing here is committed). See README.md for what each file
is, why these specific URLs, and the licence position for each.

This performs the same three downloads recorded in the evidence log
(SP500-0044, SP500-0046, SP500-0048): re-running it refreshes the raw files
with today's data, which is expected to shift the most recent 1-2 years'
figures slightly as later data becomes final. It does not fetch licence
pages — those are quoted once in the evidence log and README, not re-checked
on every data refresh.

Usage: python3 costs/benchmark/fetch_raw_data.py
"""

import sys
import urllib.request
from pathlib import Path

DATA_RAW = Path(__file__).resolve().parents[2] / "data" / "raw"

DAMODARAN_URL = "https://www.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls"
BOE_URL = (
    "https://www.bankofengland.co.uk/boeapps/database/fromshowcolumns.asp"
    "?Travel=NIxAZxSUx&FromSeries=1&ToSeries=50&DAT=RNG&FD=1&FM=Jan&FY=1970"
    "&TD=31&TM=Dec&TY=2026&FNY=&CSVF=TT&html.x=66&html.y=26"
    "&SeriesCodes=XUDLGBD&UsingCodes=Y&Filter=N&title=XUDLGBD&VPD=Y"
)
ONS_URL = "https://www.ons.gov.uk/generator?format=csv&uri=/economy/inflationandpriceindices/timeseries/d7bt/mm23"

FILES = [
    (DAMODARAN_URL, DATA_RAW / "damodaran_histretSP.xls"),
    (BOE_URL, DATA_RAW / "boe_xudlgbd_daily.html"),
    (ONS_URL, DATA_RAW / "ons_cpi_d7bt.csv"),
]

USER_AGENT = "Mozilla/5.0 (compatible; the-investor-brain-benchmark-fetch/1.0)"


def fetch(url, dest):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=60) as response:
        data = response.read()
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    return len(data)


def main():
    DATA_RAW.mkdir(parents=True, exist_ok=True)
    for url, dest in FILES:
        try:
            size = fetch(url, dest)
        except Exception as e:  # noqa: BLE001 - report and continue with the others
            print(f"FAILED: {url} -> {dest.name}: {e}", file=sys.stderr)
            continue
        print(f"OK: {dest.name} ({size:,} bytes) <- {url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
