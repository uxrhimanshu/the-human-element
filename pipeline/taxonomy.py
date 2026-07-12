#!/usr/bin/env python3
"""Assign the design-failure taxonomy to the derived incident tables."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DERIVED = ROOT / "data" / "derived"

CLASS_RULES = {
    "C1": ("error_varieties", ("Misdelivery",)),
    "C2": ("error_varieties", ("Publishing error",)),
    "C3": ("error_varieties", ("Misconfiguration",)),
    "C4": ("error_varieties", ("Loss",)),
    "C5": ("error_varieties", ("Disposal error",)),
    "C6": ("error_varieties", ("Gaffe",)),
    "C7": ("error_varieties", ("Data entry error", "Classification error")),
    "C8": ("social_varieties", ("Phishing",)),
    "C9": ("social_varieties", ("Pretexting",)),
}

SUBMECHANISM_RULES = {
    "C1": {
        "channel:email": ("email", "e-mail"),
        "channel:postal": ("letter", "envelope", "mailed", "mailing", " mail ", "postal"),
        "channel:fax": ("fax",),
        "wrong-attachment": ("attach",),
    },
    "C2": {
        "web-posting": ("website", "web site", "online", "posted", "published", "uploaded"),
        "search-indexed": ("google", "search engine", "indexed"),
        "ambient-display": (r"re:\bmonitors?\b", r"re:\bscreens?\b", r"re:\bdisplays?\b"),
    },
    "C3": {
        "open-datastore": ("elasticsearch", "mongodb", "s3", "bucket", "database", "rsync"),
        "during-change": ("upgrade", "migration", "updated", "update"),
        "no-auth": ("password", "unsecured", "unprotected"),
    },
    "C4": {
        "paper": ("paper", "document", "folder", "binder", "clipboard", r"re:\bforms?\b", "records"),
        "device-media": ("laptop", "usb", "thumb drive", "flash drive", "phone", r"re:\bcds?\b",
                         "disk", "tape", "computer", "hard drive", "external drive"),
    },
    "C5": {
        "trash-stream": ("dumpster", "trash", "recycl", "landfill", "curb"),
        "resale-abandonment": ("sold", "auction", "donated", "storage unit", "abandoned"),
        "shred-failure": ("shred",),
    },
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def split_values(value: object) -> set[str]:
    return {item for item in str(value or "").split(";") if item}


def is_true(value: object) -> bool:
    return str(value or "").lower() == "true"


def assigned_classes(row: dict[str, str]) -> list[str]:
    classes = [class_name for class_name, (column, values) in CLASS_RULES.items()
               if split_values(row.get(column)) & set(values)]
    if not classes and (is_true(row.get("action_error")) or is_true(row.get("action_social"))):
        classes.append("C0")
    return sorted(classes)


def keyword_matches(keyword: str, text: str) -> bool:
    """Keywords prefixed 're:' are regex patterns; everything else is a plain substring."""
    if keyword.startswith("re:"):
        return re.search(keyword[3:], text) is not None
    return keyword in text


def assigned_submechanisms(classes: list[str], summary: str) -> list[str]:
    text = summary.lower()
    tokens = [f"{class_name}:{name}" for class_name in classes
              for name, keywords in SUBMECHANISM_RULES.get(class_name, {}).items()
              if any(keyword_matches(keyword, text) for keyword in keywords)]
    return sorted(tokens)


def main() -> None:
    incidents_path, narratives_path = DERIVED / "incidents.csv", DERIVED / "narratives.csv"
    if not incidents_path.exists() or not narratives_path.exists():
        raise FileNotFoundError("Missing derived CSVs; run pipeline/build.py first.")
    incidents, narratives = read_csv(incidents_path), read_csv(narratives_path)
    summaries = {row["row_id"]: row.get("summary", "") for row in narratives}
    if len(summaries) != len(narratives):
        raise ValueError("narratives.csv row_id values must be unique")

    coded: list[dict[str, str]] = []
    class_counts: Counter[str] = Counter()
    submechanism_counts: Counter[str] = Counter()
    human_element_no_class = 0
    for incident in incidents:
        classes = assigned_classes(incident)
        submechanisms = assigned_submechanisms(classes, summaries.get(incident["row_id"], ""))
        human_element = is_true(incident.get("action_error")) or is_true(incident.get("action_social"))
        if human_element and not classes:
            human_element_no_class += 1
        class_counts.update(classes)
        submechanism_counts.update(submechanisms)
        coded.append({"row_id": incident["row_id"], "classes": ";".join(classes),
                      "submechanisms": ";".join(submechanisms),
                      "human_element": str(human_element)})

    output_path = DERIVED / "coded.csv"
    with output_path.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=["row_id", "classes", "submechanisms", "human_element"])
        writer.writeheader()
        writer.writerows(coded)
    stats = {"class_counts": {name: class_counts[name] for name in sorted(class_counts)},
             "submechanism_counts": dict(sorted(submechanism_counts.items())),
             "human_element_rows_without_class": human_element_no_class}
    stats_path = DERIVED / "taxonomy_stats.json"
    stats_path.write_text(json.dumps(stats, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("Class      Incidents")
    print("---------- ---------")
    for name in sorted(stats["class_counts"]):
        print(f"{name:<10} {stats['class_counts'][name]:>9,}")
    print(f"Human-element rows with no class: {human_element_no_class:,}")
    print(f"Wrote {output_path.relative_to(ROOT)} and {stats_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
