#!/usr/bin/env python3
"""Check source-ledger URLs without treating bot blocks as broken links."""

from __future__ import annotations

import csv
import subprocess
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "03_source_ledger.csv"
OUTPUT = ROOT / "data" / "27_source_url_checks.csv"
CHECKED_AT = "2026-07-18"


def request(url: str) -> tuple[str, str, str]:
    command = [
        "curl", "-L", "-sS", "--range", "0-0", "--connect-timeout", "8",
        "--max-time", "25", "-A", "Mozilla/5.0 BigFourResearchLinkCheck/1.0",
        "-o", "/dev/null", "-w", "%{http_code}\t%{url_effective}", url,
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    payload = result.stdout.strip().split("\t", 1)
    code = payload[0] if payload else "000"
    effective_url = payload[1] if len(payload) > 1 else ""
    return code, effective_url, result.stderr.strip().replace("\n", " ")


def check(row: dict[str, str]) -> dict[str, str]:
    fallback_url = ""
    fallback_code = ""
    try:
        code, effective_url, error = request(row["url"])
        if code in {"404", "410"}:
            fallback_url = row.get("archived_url", "")
            if fallback_url:
                fallback_code, _, fallback_error = request(fallback_url)
            if fallback_code.startswith(("2", "3")):
                status = "warning"
                note = "Primary URL is permanently unavailable; the recorded archive responded successfully."
            else:
                status = "fail"
                note = f"Permanent not-found response and no working archive. {fallback_error if fallback_url else ''}".strip()
        elif code.startswith(("2", "3")):
            status = "pass"
            note = "Source responded successfully."
        elif code in {"401", "403", "405", "406", "429", "451"}:
            status = "warning"
            note = "Access-controlled or automated request blocked; this does not prove the source is broken."
        else:
            status = "warning"
            note = f"Transient or unclassified response; verify manually. {error}".strip()
    except FileNotFoundError:
        code, effective_url, status = "", "", "warning"
        note = "curl is unavailable; URL not tested."
    return {
        "source_id": row["source_id"], "url": row["url"],
        "http_status": code, "effective_url": effective_url,
        "fallback_url": fallback_url, "fallback_http_status": fallback_code,
        "check_status": status, "checked_at": CHECKED_AT, "notes": note,
    }


def main() -> None:
    with INPUT.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(check, rows))
    fields = [
        "source_id", "url", "http_status", "effective_url",
        "fallback_url", "fallback_http_status", "check_status", "checked_at", "notes",
    ]
    with OUTPUT.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)
    counts = {status: sum(row["check_status"] == status for row in results) for status in ("pass", "warning", "fail")}
    print(f"Checked {len(results)} source URLs: {counts}")


if __name__ == "__main__":
    main()
