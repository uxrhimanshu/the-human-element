# The Human Element — spec

## What this is
A public design-research study of real security incidents: where interfaces, defaults,
warnings, and workflows set humans up to fail. The deliverable is a polished interactive
research report (static site, eventually on himanshukalra.com / Netlify) with a
transparent method section. The positioning goal: serious enterprise UXR practitioner —
"took a massive messy corpus of real human-failure data and produced a rigorous,
opinionated analysis with a defensible method."

Working title: **The Human Element — what 3,000 security incidents reveal about design.**
(Title to be finalized at write-up.)

## Data sources (verified live 2026-07-12)
1. **VCDB** — VERIS Community Database, github.com/vz-risk/VCDB (open dataset behind
   Verizon's DBIR). Combined file: `data/joined/vcdb.json.zip` (raw.githubusercontent.com,
   4.6 MB zip → 21 MB JSON, last updated 2026-07-03).
   - 10,042 incidents; 9,523 with free-text `summary` narratives.
   - Human-element core: `action.error` present in 2,681 incidents; `action.social` in 644.
   - Error varieties: Misdelivery 973, Loss 415, Publishing error 397, Misconfiguration 336,
     Disposal error 321, Programming error 60, Gaffe 41, Data entry error 6, others small.
   - Social varieties: Phishing 431, Pretexting 70, Bribery 59, Extortion 37, others small.
   - Known limitation: coverage peaks 2010–2019, thins after 2020. Must be stated in method.
2. **CISA KEV** — Known Exploited Vulnerabilities feed,
   cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json (1.5 MB, HTTP 200
   verified). Secondary/contextual source; may be cut if it doesn't earn its place.

## Analytical spine (Claude-owned)
Map VERIS human-element varieties to a **design-failure taxonomy** (v0, to be refined
against real narratives in Phase 2):

| VERIS variety | Design-failure class | Canonical mechanism |
|---|---|---|
| Misdelivery | Wrong-recipient affordances | email autocomplete, bulk-mail merge, CC/BCC |
| Publishing error | Visibility-state illegibility | public/private state not legible at point of action |
| Misconfiguration | Unsafe defaults & config complexity | open-by-default storage, sprawling consoles |
| Disposal error | End-of-life process design | no forcing function at decommission |
| Loss | Unprotected portability | device/media loss; encryption-by-default absent |
| Data entry error | Input error prevention | validation, confirmation design |
| Gaffe | Disclosure friction absent | oversharing in public channels |
| Phishing / Pretexting (social) | Trust-cue failure | authenticity illegible; warning fatigue |

Framing: shift blame from "user error" to system design — Norman / Reason's Swiss-cheese
model, error-prevention heuristics. Each taxonomy class gets: prevalence, trend, industry
skew, exemplar narratives (verbatim quotes), and the design pattern that would have
prevented it.

## Phases
- **P0 — source verification.** DONE 2026-07-12 (numbers above).
- **P1 — data pipeline** (Codex, terra/medium): fetch + tidy + profile. See "P1 contract".
- **P2 — taxonomy & coding** (Claude): refine taxonomy against real narratives; rule-based
  assignment from VERIS fields; select exemplar narratives per class.
- **P3 — analysis** (Codex compute, Claude direction/review): prevalence, trends,
  industry × variety, asset × variety, discovery-method analysis (how long before
  error-caused breaches are noticed, and by whom — likely a headline finding).
- **P4 — interactive report site** (Codex build, dataviz skill for charts, Claude review):
  long-form scrollytelling-lite static page; no framework lock-in decided yet.
- **P5 — method section, editing, deploy** (Claude-owned quality gate). Netlify deploy via
  deploy.sh pattern respecting deploy limits.

## P1 contract (Codex)
Build in `pipeline/`, Python 3, pandas allowed, deterministic, no other heavy deps:
1. `fetch.py` — download VCDB zip + KEV feed into `data/raw/` (skip if present & fresh;
   `--force` to re-fetch). Record source URLs + fetch date in `data/raw/MANIFEST.json`.
2. `build.py` — parse VCDB → tidy tables in `data/derived/`:
   - `incidents.csv` — one row per incident: incident_id, year, month, action types
     (bool cols), error varieties, social varieties (list-cols as `;`-joined), actor
     categories, asset varieties, victim industry (NAICS 2-digit + label), victim country,
     data varieties disclosed, record count, discovery_method, timeline fields present,
     has_summary, summary word count. Schema documented in `pipeline/README.md`.
   - `narratives.csv` — incident_id, human_element flag, error/social varieties, summary.
3. `profile.py` — emit `data/derived/stats.json` (counts, cross-tabs: variety×year,
   variety×industry, variety×asset, discovery_method×error-variety) and a human-readable
   `data/derived/PROFILE.md` with the headline tables + 3 sample narratives per major
   error/social variety.
4. `README.md` in `pipeline/` — how to run end-to-end; note VERIS schema quirks found.
Quality bar: numbers in PROFILE.md must reconcile with the P0 counts above (±0 —
same source file).

## Division of labor
Codex carries bulk build (pipeline, site scaffolding, chart implementation, analysis
compute). Claude owns spec, taxonomy, findings narrative, method section, and the
quality gate on everything Codex produces.
