#!/usr/bin/env python3
"""Fetch the source datasets used by the Human Element pipeline."""

from __future__ import annotations

import argparse
import json
import shutil
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
SOURCES = {
    "vcdb": {
        "url": "https://raw.githubusercontent.com/vz-risk/VCDB/master/data/joined/vcdb.json.zip",
        "filename": "vcdb.json.zip",
    },
    "cisa_kev": {
        "url": "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json",
        "filename": "known_exploited_vulnerabilities.json",
    },
}


def download(url: str, destination: Path) -> None:
    """Atomically download a URL using only the Python standard library."""
    temporary = destination.with_suffix(destination.suffix + ".part")
    request = urllib.request.Request(url, headers={"User-Agent": "human-element-pipeline/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=90) as response, temporary.open("wb") as output:
            shutil.copyfileobj(response, output)
        temporary.replace(destination)
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--force", action="store_true", help="Re-download files even when present.")
    args = parser.parse_args()

    RAW.mkdir(parents=True, exist_ok=True)
    manifest_path = RAW / "MANIFEST.json"
    previous = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    files = previous.get("files", {})
    fetched_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    for name, source in SOURCES.items():
        path = RAW / source["filename"]
        if path.exists() and not args.force:
            print(f"Keeping existing {path.name}")
        else:
            print(f"Downloading {path.name}")
            download(source["url"], path)
            files[name] = {"url": source["url"], "filename": path.name, "fetched_at": fetched_at}
        # Preserve provenance even for files that were already supplied locally.
        files.setdefault(name, {"url": source["url"], "filename": path.name, "fetched_at": fetched_at})

    manifest_path.write_text(json.dumps({"files": files}, indent=2, sort_keys=True) + "\n")
    print(f"Wrote {manifest_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
