#!/usr/bin/env python3
"""Build tidy incident and narrative tables from the VCDB combined JSON."""

from __future__ import annotations

import json
import re
import zipfile
import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
DERIVED = ROOT / "data" / "derived"

ACTION_TYPES = ("error", "social", "hacking", "malware", "misuse", "physical", "environmental")
NAICS_LABELS = {
    "11": "Agriculture, forestry, fishing and hunting", "21": "Mining, quarrying, and oil and gas extraction",
    "22": "Utilities", "23": "Construction", "31": "Manufacturing", "32": "Manufacturing", "33": "Manufacturing",
    "42": "Wholesale trade", "44": "Retail trade", "45": "Retail trade", "48": "Transportation and warehousing",
    "49": "Transportation and warehousing", "51": "Information", "52": "Finance and insurance",
    "53": "Real estate and rental and leasing", "54": "Professional, scientific, and technical services",
    "55": "Management of companies and enterprises", "56": "Administrative and support and waste management",
    "61": "Educational services", "62": "Health care and social assistance", "71": "Arts, entertainment, and recreation",
    "72": "Accommodation and food services", "81": "Other services", "92": "Public administration",
}


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def strings(value: Any) -> list[str]:
    return [str(item) for item in as_list(value) if item not in (None, "", "Unknown", "unknown")]


def values(records: Any, key: str) -> list[str]:
    result: list[str] = []
    for record in as_list(records):
        if isinstance(record, dict):
            result.extend(strings(record.get(key)))
    return result


def nested_values(container: Any, collection_key: str, value_key: str) -> list[str]:
    """Read a field from a VERIS object whose records live under collection_key."""
    result: list[str] = []
    for container_item in as_list(container):
        if isinstance(container_item, dict):
            result.extend(values(container_item.get(collection_key), value_key))
    return result


def unique_join(items: list[str]) -> str:
    return ";".join(dict.fromkeys(item for item in items if item))


def get_path(record: dict[str, Any], *keys: str) -> Any:
    value: Any = record
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value


def action_varieties(action: dict[str, Any], action_type: str) -> list[str]:
    item = action.get(action_type)
    if not isinstance(item, dict):
        return []
    return strings(item.get("variety"))


def first_scalar(value: Any) -> str:
    vals = strings(value)
    return vals[0] if vals else ""


def extract_victim(victim: Any) -> tuple[str, str, str]:
    industries: list[str] = []
    countries: list[str] = []
    for item in as_list(victim):
        if not isinstance(item, dict):
            continue
        industries.extend(strings(item.get("industry")))
        countries.extend(strings(item.get("country")))
    industry = first_scalar(industries)
    match = re.search(r"\d{2}", industry)
    code = match.group(0) if match else ""
    return code, NAICS_LABELS.get(code, ""), first_scalar(countries)


def extract_record_count(incident: dict[str, Any]) -> Any:
    value = get_path(incident, "attribute", "confidentiality", "data_total")
    if isinstance(value, (int, float)):
        return value
    # Old records occasionally only provide a range/value under data_disclosure.
    value = get_path(incident, "attribute", "confidentiality", "data_disclosure")
    if isinstance(value, dict):
        value = value.get("amount") or value.get("value")
    return value if isinstance(value, (int, float, str)) else ""


def discovery_method(value: Any) -> tuple[str, str]:
    """discovery_method is a dict keyed by category (external/internal/partner/other/unknown),
    with an optional nested variety list; 'unknown'/'other' map to bare True."""
    categories: list[str] = []
    varieties: list[str] = []
    for item in as_list(value):
        if not isinstance(item, dict):
            continue
        for key, val in item.items():
            if val in (None, False):
                continue
            categories.append(str(key))
            if isinstance(val, dict):
                varieties.extend(strings(val.get("variety")))
    return unique_join(categories), unique_join(varieties)


def actor_categories(actor: Any) -> list[str]:
    """VERIS actor categories are the keys (external, internal, partner, ...)."""
    categories: list[str] = []
    for item in as_list(actor):
        if isinstance(item, dict):
            categories.extend(str(key) for key, value in item.items() if value is not None)
    return categories


def load_incidents() -> list[dict[str, Any]]:
    zip_path = RAW / "vcdb.json.zip"
    if not zip_path.exists():
        raise FileNotFoundError(f"Missing {zip_path}; run pipeline/fetch.py first.")
    with zipfile.ZipFile(zip_path) as archive:
        json_names = [name for name in archive.namelist() if name.endswith(".json")]
        if len(json_names) != 1:
            raise ValueError(f"Expected one JSON file in {zip_path}, found {json_names}")
        with archive.open(json_names[0]) as source:
            data = json.load(source)
    if not isinstance(data, list):
        raise ValueError("VCDB combined JSON must be an array of incidents")
    return data


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]), extrasaction="raise")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    incidents = load_incidents()
    rows: list[dict[str, Any]] = []
    narrative_rows: list[dict[str, Any]] = []
    # VCDB quirk: 23 incident_ids are shared by distinct incidents (44 rows affected),
    # so rows get a synthetic unique row_id: the incident_id, suffixed #2, #3... on repeats.
    seen_ids: dict[str, int] = {}
    for incident in incidents:
        action = incident.get("action") if isinstance(incident.get("action"), dict) else {}
        error = action_varieties(action, "error")
        social = action_varieties(action, "social")
        summary = str(incident.get("summary") or "").strip()
        industry, industry_label, country = extract_victim(incident.get("victim"))
        timeline = incident.get("timeline") if isinstance(incident.get("timeline"), dict) else {}
        incident_time = timeline.get("incident") if isinstance(timeline.get("incident"), dict) else {}
        human_element = "error" in action or "social" in action
        incident_id = str(incident.get("incident_id") or incident.get("id") or "")
        seen_ids[incident_id] = seen_ids.get(incident_id, 0) + 1
        row_id = incident_id if seen_ids[incident_id] == 1 else f"{incident_id}#{seen_ids[incident_id]}"
        discovery_categories, discovery_varieties = discovery_method(incident.get("discovery_method"))
        row: dict[str, Any] = {
            "row_id": row_id,
            "incident_id": incident_id,
            "year": incident_time.get("year", ""), "month": incident_time.get("month", ""),
            **{f"action_{kind}": kind in action for kind in ACTION_TYPES},
            "error_varieties": unique_join(error), "social_varieties": unique_join(social),
            "actor_categories": unique_join(actor_categories(incident.get("actor"))),
            "asset_varieties": unique_join(nested_values(incident.get("asset"), "assets", "variety")),
            "victim_industry_naics2": industry, "victim_industry_label": industry_label,
            "victim_country": country,
            "data_varieties_disclosed": unique_join(values(get_path(incident, "attribute", "confidentiality", "data"), "variety")),
            "record_count": extract_record_count(incident),
            "discovery_categories": discovery_categories,
            "discovery_varieties": discovery_varieties,
            "timeline_incident_present": bool(timeline.get("incident")),
            "timeline_discovery_present": bool(timeline.get("discovery")),
            "timeline_containment_present": bool(timeline.get("containment")),
            "has_summary": bool(summary), "summary_word_count": len(summary.split()),
        }
        rows.append(row)
        narrative_rows.append({"row_id": row_id, "incident_id": incident_id, "human_element": human_element,
                               "error_varieties": row["error_varieties"], "social_varieties": row["social_varieties"],
                               "summary": summary})

    DERIVED.mkdir(parents=True, exist_ok=True)
    row_ids = [row["row_id"] for row in rows]
    if not all(row_ids) or len(row_ids) != len(set(row_ids)):
        raise ValueError("row_id must be present and unique")
    write_csv(DERIVED / "incidents.csv", rows)
    write_csv(DERIVED / "narratives.csv", narrative_rows)
    print(f"Built {len(rows)} incidents and {len(narrative_rows)} narratives in {DERIVED.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
