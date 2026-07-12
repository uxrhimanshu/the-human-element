# P1 data pipeline

Run from the repository root:

```sh
python3 pipeline/fetch.py
python3 pipeline/build.py
python3 pipeline/profile.py
```

`fetch.py --force` downloads fresh copies of both inputs. Without it, existing raw files
are retained. Source provenance and the download timestamp are in `data/raw/MANIFEST.json`.

The pipeline uses only the Python 3 standard library. It is deterministic after the input
files have been fetched: ordering follows the combined VCDB JSON input order, including
the three narrative samples for each variety.

## Outputs

`data/derived/incidents.csv` has exactly one row per VCDB incident and these columns:

| Column | Meaning |
| --- | --- |
| `row_id` | Unique row key: `incident_id`, suffixed `#2`, `#3`… when VCDB reuses an id. |
| `incident_id` | VCDB's incident identifier (not unique — see normalization notes). |
| `year`, `month` | `timeline.incident` year and month, when supplied. |
| `action_error`, `action_social`, `action_hacking`, `action_malware`, `action_misuse`, `action_physical`, `action_environmental` | Whether that VERIS action object is present. |
| `error_varieties`, `social_varieties` | Semicolon-joined VERIS varieties. |
| `actor_categories` | Semicolon-joined actor categories. |
| `asset_varieties` | Semicolon-joined asset varieties. |
| `victim_industry_naics2`, `victim_industry_label` | Two-digit NAICS prefix and its broad sector label. |
| `victim_country` | First supplied victim country. |
| `data_varieties_disclosed` | Semicolon-joined confidentiality data varieties. |
| `record_count` | `attribute.confidentiality.data_total` when supplied. |
| `discovery_categories` | Semicolon-joined discovery categories (`external`, `internal`, `partner`, `other`, `unknown`). |
| `discovery_varieties` | Semicolon-joined discovery varieties nested under those categories (e.g. `Actor disclosure`, `Reported by employee`). |
| `timeline_incident_present`, `timeline_discovery_present`, `timeline_containment_present` | Whether each timeline block is present. |
| `has_summary`, `summary_word_count` | Narrative presence and whitespace-delimited word count. |

`data/derived/narratives.csv` contains `row_id`, `incident_id`, `human_element`, `error_varieties`,
`social_varieties`, and source `summary`. `human_element` is true when `action.error` or
`action.social` is present. `stats.json` contains counts and variety cross-tabs; `PROFILE.md`
is the readable profile and sample narratives.

## VERIS normalization notes

- `variety` fields are lists, even when an incident has a single variety; list fields are
  exported as semicolon-joined strings.
- Older VCDB records can express `victim`, `actor`, and `asset` as either a dictionary or a
  list of dictionaries. The builder accepts both and uses the first victim industry/country.
- Victim industry values are NAICS codes stored as strings; the builder takes the first
  two digits and supplies a broad NAICS sector label.
- `incident_id` is not unique in the source: 23 ids are shared across 44 rows, almost all
  distinct incidents wrongly sharing an id (2 are byte-identical duplicate records). All
  rows are kept; `row_id` is the synthetic unique key.
- `discovery_method` is a dict keyed by category, with varieties nested per category;
  `unknown`/`other` carry a bare `true` instead of a nested object.
- The literal string `Unknown` is filtered out of all variety/value lists (e.g. the 50
  `action.error.variety = Unknown` incidents still count toward `action_error` but list no
  variety). Presence booleans are unaffected.
- Missing fields are exported as empty CSV values. CSV text is quoted per RFC 4180 by the
  `csv` module, so summaries containing commas or newlines remain readable with
  `pandas.read_csv`.
