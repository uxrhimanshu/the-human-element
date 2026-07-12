# The Human Element — status

## Context
Design-research study of the VERIS Community Database (VCDB, ~10k security incidents,
~3.3k human-element) → interactive research report positioning Himanshu as a serious
enterprise UXR practitioner. Chosen 2026-07-12 from the sociological-projects brainstorm
(idea #14). Full working contract in `SPEC.md`.

## Done
- 2026-07-12: Sources verified live (VCDB fresh as of 3 Jul 2026; CISA KEV 200 OK).
  Dataset profiled: 10,042 incidents, 9,523 with narratives; error 2,681 / social 644.
  Design-failure taxonomy v0 drafted (SPEC.md). Project scaffolded, git init.
- 2026-07-12: P1 pipeline delegated to Codex (gpt-5.6-terra, medium).
- 2026-07-12: P1 DONE. Codex built fetch/build/profile (stdlib-only; couldn't run live —
  sandbox has no network). Claude ran it, found + fixed two data-shape bugs
  (discovery_method is a nested dict; 23 incident_ids shared across 44 rows → row_id).
  All ground-truth counts reconcile exactly (10,042 / 9,523 / 2,681 / 644; Misdelivery 973
  … Pretexting 70). Outputs: data/derived/{incidents,narratives}.csv, stats.json, PROFILE.md.

- 2026-07-12: P2 DONE. TAXONOMY.md v1 (9 classes + C0, exemplars, VA-bias caveat);
  taxonomy.py (Codex luna built; Claude fixed keyword false-positives with word-boundary
  regex; class counts verified; exemplars spot-checked). Gotcha: backgrounded codex exec
  hung on stdin once — always append </dev/null.
- 2026-07-12: P3 core DONE. FINDINGS.md F1–F6: 78% external discovery (customer #1);
  postal misdelivery 2x email; 26.4% purely self-inflicted; blast-radius ladder
  (misdelivery median 2 records vs misconfiguration median 700,000); failure modes
  migrate physical→cloud; industry skews.

## To-do
- P3 wrap: sanity-review F1–F6 numbers once more when writing the report; decide
  whether CISA KEV earns its place (leaning cut).
- P4: interactive report site (dataviz skill for charts; Codex builds; scrollytelling-lite).
- P5: method section, edit, Netlify deploy, link from portfolio.

## Awaiting
- Nothing from Himanshu right now.

## Next step
P4: spec the report site (structure: hook → taxonomy walk with exemplars → F1/F3/F4/F5
charts → method), then delegate the build to Codex with the dataviz skill loaded.
