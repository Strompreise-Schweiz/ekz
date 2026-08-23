#!/usr/bin/env python3
"""Fetch tariff data for every organization in config/orgs.json and store a raw
plus a normalized snapshot per day under data/<slug>/{raw,normalized}/<year>/<date>.json.

Stdlib only, no third-party dependencies, so no install step is needed in CI.
"""
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "orgs.json"
DATA_ROOT = ROOT / "data"

sys.path.insert(0, str(Path(__file__).resolve().parent))
from normalizers import REGISTRY  # noqa: E402

USER_AGENT = "strompreise-schweiz-tariff-archiver/1.0 (+https://github.com/Strompreise-Schweiz/ekz)"


def fetch_bytes(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        if resp.status != 200:
            raise RuntimeError(f"unexpected HTTP status {resp.status} from {url}")
        return resp.read()


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not data.endswith(b"\n"):
        data += b"\n"
    path.write_bytes(data)


def write_json(path: Path, obj) -> None:
    write_bytes(path, json.dumps(obj, indent=2, ensure_ascii=False).encode("utf-8"))


def process_org(org: dict, retrieved_at: str) -> bool:
    slug = org["slug"]
    normalize = REGISTRY.get(org["normalizer"])
    if normalize is None:
        print(f"[{slug}] ERROR: no normalizer registered for '{org['normalizer']}'", file=sys.stderr)
        return False

    try:
        raw_bytes = fetch_bytes(org["api_url"])
        raw_data = json.loads(raw_bytes)
    except (urllib.error.URLError, json.JSONDecodeError, RuntimeError, TimeoutError) as exc:
        print(f"[{slug}] ERROR fetching/parsing {org['api_url']}: {exc}", file=sys.stderr)
        return False

    try:
        normalized = normalize(raw_data, org=org, retrieved_at=retrieved_at)
    except Exception as exc:  # noqa: BLE001 - surface any normalizer bug, keep other orgs running
        print(f"[{slug}] ERROR normalizing: {exc}", file=sys.stderr)
        return False

    date = normalized["date"]
    year = date[:4]

    raw_path = DATA_ROOT / slug / "raw" / year / f"{date}.json"
    normalized_path = DATA_ROOT / slug / "normalized" / year / f"{date}.json"

    write_bytes(raw_path, raw_bytes)
    write_json(normalized_path, normalized)

    print(f"[{slug}] wrote {raw_path.relative_to(ROOT)} and {normalized_path.relative_to(ROOT)}")
    return True


def main() -> int:
    orgs = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    retrieved_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    all_ok = True
    for org in orgs:
        if not process_org(org, retrieved_at):
            all_ok = False

    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
